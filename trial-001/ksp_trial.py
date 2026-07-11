#!/usr/bin/env python3
"""Independent reference receiver for KSP Trial 001."""

import argparse
import hashlib
import hmac
import json
import os
from pathlib import Path
import secrets
import stat
import sys


PROTOCOL = "ksp/0.1"
PROFILE = "responsible-succession/1"
FORBIDDEN_KEYS = {
    "script", "code", "executable", "binary", "command_line", "weights"
}
REQUIRED_EVIDENCE = {
    "design.observed",
    "alternative.rejected",
    "claim.made",
    "claim.verified",
    "culture.practice",
}
PROTECTED_TYPES = {"seed.manifest", "capability.declared"}


class TrialError(Exception):
    pass


def canonical(value):
    return json.dumps(
        value, ensure_ascii=True, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()


def forbidden_paths(value, path="$"):
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = "%s.%s" % (path, key)
            if str(key).lower() in FORBIDDEN_KEYS:
                found.append(child_path)
            found.extend(forbidden_paths(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(forbidden_paths(child, "%s[%d]" % (path, index)))
    return found


def load_seed(path):
    raw = Path(path).read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise TrialError("seed is not UTF-8: %s" % exc) from exc

    events = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise TrialError("line %d is not valid JSON: %s" % (line_number, exc)) from exc
        if not isinstance(event, dict):
            raise TrialError("line %d must be a JSON object" % line_number)
        events.append(event)
    validate_events(events)
    return raw, events


def validate_events(events):
    if not events:
        raise TrialError("seed contains no events")

    seen_ids = set()
    seen_seqs = set()
    previous_seq = 0
    types = []
    for index, event in enumerate(events, 1):
        if set(event) != {"id", "seq", "type", "payload"}:
            raise TrialError("event %d has unexpected or missing top-level fields" % index)
        event_id = event["id"]
        seq = event["seq"]
        event_type = event["type"]
        if not isinstance(event_id, str) or not event_id:
            raise TrialError("event %d has an invalid id" % index)
        if event_id in seen_ids:
            raise TrialError("duplicate event id: %s" % event_id)
        if isinstance(seq, bool) or not isinstance(seq, int) or seq < 1:
            raise TrialError("event %s has an invalid seq" % event_id)
        if seq in seen_seqs or seq <= previous_seq:
            raise TrialError("event seq values must be unique and increasing")
        if not isinstance(event_type, str) or not event_type:
            raise TrialError("event %s has an invalid type" % event_id)
        if not isinstance(event["payload"], dict):
            raise TrialError("event %s payload must be an object" % event_id)
        forbidden = forbidden_paths(event)
        if forbidden:
            raise TrialError("event %s contains forbidden field(s): %s" % (
                event_id, ", ".join(forbidden)
            ))
        seen_ids.add(event_id)
        seen_seqs.add(seq)
        previous_seq = seq
        types.append(event_type)

    if types[0] != "seed.manifest" or types.count("seed.manifest") != 1:
        raise TrialError("seed must begin with exactly one seed.manifest")
    manifest = events[0]["payload"]
    expected = {
        "protocol": PROTOCOL,
        "tier": 3,
        "flavor": "capability",
        "profile": PROFILE,
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            raise TrialError("manifest %s must be %r" % (key, value))
    if not isinstance(manifest.get("seed_id"), str) or not manifest["seed_id"]:
        raise TrialError("manifest seed_id must be a non-empty string")
    lineage = manifest.get("lineage")
    if not isinstance(lineage, list) or not lineage or not all(
        isinstance(item, str) and item for item in lineage
    ):
        raise TrialError("manifest lineage must contain source identifiers")

    declarations = [event for event in events if event["type"] == "capability.declared"]
    if len(declarations) != 1:
        raise TrialError("seed must contain exactly one capability.declared")
    declaration = declarations[0]["payload"]
    if declaration.get("profile") != PROFILE:
        raise TrialError("capability declaration profile does not match manifest")
    verbs = declaration.get("verbs")
    if not isinstance(verbs, dict) or set(verbs) != {"claim", "verify", "bequeath"}:
        raise TrialError("capability must declare exactly claim, verify, and bequeath")

    missing = REQUIRED_EVIDENCE - set(types)
    if missing:
        raise TrialError("seed is missing evidence types: %s" % ", ".join(sorted(missing)))

    claim_ids = {
        event["payload"].get("claim_id")
        for event in events
        if event["type"] == "claim.made"
    }
    for event in events:
        if event["type"] == "claim.verified":
            payload = event["payload"]
            if payload.get("claim_id") not in claim_ids:
                raise TrialError("seed verification references an unknown claim")
            if payload.get("result") not in {"pass", "fail"}:
                raise TrialError("seed verification result must be pass or fail")


def load_policy(path):
    if path is None:
        return {"reject_types": [], "remap_types": {}}
    try:
        policy = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TrialError("cannot read policy: %s" % exc) from exc
    if not isinstance(policy, dict):
        raise TrialError("policy must be an object")
    reject = policy.get("reject_types", [])
    remap = policy.get("remap_types", {})
    if not isinstance(reject, list) or not all(isinstance(item, str) for item in reject):
        raise TrialError("policy reject_types must be a string array")
    if not isinstance(remap, dict) or not all(
        isinstance(key, str) and isinstance(value, str) and value
        for key, value in remap.items()
    ):
        raise TrialError("policy remap_types must map strings to non-empty strings")
    protected = PROTECTED_TYPES.intersection(set(reject) | set(remap))
    if protected:
        raise TrialError("policy cannot reject or remap protected types: %s" % (
            ", ".join(sorted(protected))
        ))
    return {"reject_types": reject, "remap_types": remap}


def read_key(home):
    try:
        return bytes.fromhex((home / ".receiver-key").read_text(encoding="ascii").strip())
    except (OSError, ValueError) as exc:
        raise TrialError("receiver key is missing or invalid") from exc


def append_local(home, key, event_type, payload):
    log_path = home / "events.jsonl"
    records = read_local_records(log_path)
    previous = records[-1]["hash"] if records else "0" * 64
    core = {
        "seq": len(records) + 1,
        "type": event_type,
        "payload": payload,
        "prev": previous,
    }
    record_hash = digest_bytes(canonical(core))
    record = dict(core)
    record["hash"] = record_hash
    record["sig"] = hmac.new(key, record_hash.encode("ascii"), hashlib.sha256).hexdigest()
    with log_path.open("a", encoding="utf-8") as stream:
        stream.write(canonical(record).decode("ascii") + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    return record


def read_local_records(path):
    if not path.exists():
        return []
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise TrialError("local log line %d is invalid: %s" % (line_number, exc)) from exc
        records.append(record)
    return records


def verify_local_log(home, key):
    records = read_local_records(home / "events.jsonl")
    previous = "0" * 64
    required = {"seq", "type", "payload", "prev", "hash", "sig"}
    for index, record in enumerate(records, 1):
        if not isinstance(record, dict) or set(record) != required:
            raise TrialError("local event %d has an invalid shape" % index)
        if record["seq"] != index or record["prev"] != previous:
            raise TrialError("local event %d breaks sequence or hash chain" % index)
        core = {key_name: record[key_name] for key_name in ("seq", "type", "payload", "prev")}
        expected_hash = digest_bytes(canonical(core))
        expected_sig = hmac.new(
            key, expected_hash.encode("ascii"), hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(record["hash"], expected_hash):
            raise TrialError("local event %d hash is invalid" % index)
        if not hmac.compare_digest(record["sig"], expected_sig):
            raise TrialError("local event %d signature is invalid" % index)
        previous = record["hash"]
    return records


ARTIFACT_TEMPLATE = r'''#!/usr/bin/env python3
"""Receiver-authored responsible succession capability."""
import hashlib
import hmac
import json
import os
from pathlib import Path
import sys

HOME = Path(__file__).resolve().parent

def canonical(value):
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True).encode("utf-8")

def load():
    records = []
    path = HOME / "events.jsonl"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                records.append(json.loads(line))
    return records

def append(event_type, payload):
    key = bytes.fromhex((HOME / ".receiver-key").read_text(encoding="ascii").strip())
    records = load()
    previous = records[-1]["hash"] if records else "0" * 64
    core = {"seq": len(records) + 1, "type": event_type, "payload": payload, "prev": previous}
    record_hash = hashlib.sha256(canonical(core)).hexdigest()
    record = dict(core)
    record["hash"] = record_hash
    record["sig"] = hmac.new(key, record_hash.encode("ascii"), hashlib.sha256).hexdigest()
    with (HOME / "events.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(canonical(record).decode("ascii") + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    return record

def die(message):
    print(message, file=sys.stderr)
    raise SystemExit(2)

if len(sys.argv) < 3:
    die("usage: responsible-succession claim <text> | verify <claim-id> <pass|fail> <evidence> | bequeath <text>")

verb = sys.argv[1]
records = load()
if verb == "claim":
    text = " ".join(sys.argv[2:]).strip()
    if not text:
        die("claim text is required")
    claim_number = 1 + sum(1 for record in records if record.get("type") == "claim.made")
    claim_id = "local-%d" % claim_number
    append("claim.made", {"claim_id": claim_id, "text": text})
    print(claim_id)
elif verb == "verify":
    if len(sys.argv) < 5:
        die("verify requires claim-id, pass|fail, and evidence")
    claim_id, result = sys.argv[2], sys.argv[3]
    evidence = " ".join(sys.argv[4:]).strip()
    if result not in ("pass", "fail") or not evidence:
        die("verification requires pass|fail and non-empty evidence")
    claims = {record.get("payload", {}).get("claim_id") for record in records if record.get("type") == "claim.made"}
    if claim_id not in claims:
        die("unknown claim: %s" % claim_id)
    append("claim.verified", {"claim_id": claim_id, "result": result, "evidence": evidence})
    print("recorded %s for %s" % (result, claim_id))
elif verb == "bequeath":
    text = " ".join(sys.argv[2:]).strip()
    if not text:
        die("bequest text is required")
    append("bequest.left", {"text": text})
    print("bequest recorded")
else:
    die("unknown verb: %s" % verb)
'''


def plant(seed_path, home_path, policy_path):
    raw, events = load_seed(seed_path)
    policy = load_policy(policy_path)
    home = Path(home_path).resolve()
    if home.exists() and any(home.iterdir()):
        raise TrialError("receiver home must be absent or empty")
    home.mkdir(parents=True, exist_ok=True)
    incoming = home / "incoming"
    incoming.mkdir()

    key = secrets.token_bytes(32)
    key_path = home / ".receiver-key"
    key_path.write_text(key.hex() + "\n", encoding="ascii")
    key_path.chmod(stat.S_IRUSR | stat.S_IWUSR)

    seed_copy = incoming / "seed.jsonl"
    seed_copy.write_bytes(raw)
    (incoming / "policy.json").write_bytes(canonical(policy) + b"\n")
    seed_digest = digest_bytes(raw)
    append_local(home, key, "seed.received", {
        "sha256": seed_digest,
        "bytes": len(raw),
        "protocol": PROTOCOL,
        "profile": PROFILE,
    })

    transformed = []
    rejected = set(policy["reject_types"])
    remapped = policy["remap_types"]
    for event in events:
        if event["type"] in rejected:
            append_local(home, key, "seed.event.rejected", {
                "source_id": event["id"],
                "source_type": event["type"],
                "reason": "receiver policy reject_types",
            })
            continue
        local_event = json.loads(json.dumps(event))
        local_type = remapped.get(event["type"], event["type"])
        local_event["type"] = local_type
        transformed.append(local_event)
        append_local(home, key, "seed.event.accepted", {
            "source_id": event["id"],
            "source_type": event["type"],
            "local_type": local_type,
            "transformed": local_type != event["type"],
        })

    planted_path = home / "planted-seed.jsonl"
    planted_path.write_text(
        "".join(canonical(event).decode("ascii") + "\n" for event in transformed),
        encoding="ascii",
    )
    artifact = home / "responsible-succession"
    artifact.write_text(ARTIFACT_TEMPLATE, encoding="utf-8")
    artifact.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    artifact_digest = digest_bytes(artifact.read_bytes())
    artifact_sig = hmac.new(key, artifact_digest.encode("ascii"), hashlib.sha256).hexdigest()
    receipt = {
        "artifact": artifact.name,
        "sha256": artifact_digest,
        "sig": artifact_sig,
        "authored_by": "trial-001 reference receiver",
        "source": "receiver-owned fixed template",
        "seed_sha256": seed_digest,
    }
    (home / "artifact.receipt.json").write_bytes(canonical(receipt) + b"\n")
    append_local(home, key, "capability.rebuilt", receipt)
    append_local(home, key, "seed.planted", {
        "accepted": len(transformed),
        "rejected": len(events) - len(transformed),
        "artifact": artifact.name,
    })
    verify_home(home)
    return home, receipt


def verify_home(home_path):
    home = Path(home_path).resolve()
    key = read_key(home)
    records = verify_local_log(home, key)
    try:
        receipt = json.loads((home / "artifact.receipt.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TrialError("artifact receipt is missing or invalid") from exc
    artifact = home / receipt.get("artifact", "")
    if not artifact.is_file():
        raise TrialError("generated artifact is missing")
    artifact_digest = digest_bytes(artifact.read_bytes())
    expected_sig = hmac.new(key, artifact_digest.encode("ascii"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(receipt.get("sha256", ""), artifact_digest):
        raise TrialError("generated artifact digest is invalid")
    if not hmac.compare_digest(receipt.get("sig", ""), expected_sig):
        raise TrialError("generated artifact signature is invalid")

    raw, _ = load_seed(home / "incoming" / "seed.jsonl")
    if digest_bytes(raw) != receipt.get("seed_sha256"):
        raise TrialError("received seed no longer matches artifact receipt")
    received = [record for record in records if record["type"] == "seed.received"]
    if len(received) != 1 or received[0]["payload"].get("sha256") != digest_bytes(raw):
        raise TrialError("local log does not bind the received seed")
    if not any(record["type"] == "capability.rebuilt" for record in records):
        raise TrialError("local log has no capability reconstruction receipt")
    return records


def show_home(home_path):
    records = verify_home(home_path)
    claims = {}
    bequests = []
    for record in records:
        payload = record["payload"]
        if record["type"] == "claim.made":
            claims[payload["claim_id"]] = {"text": payload["text"], "checks": []}
        elif record["type"] == "claim.verified" and payload.get("claim_id") in claims:
            claims[payload["claim_id"]]["checks"].append({
                "result": payload["result"], "evidence": payload["evidence"]
            })
        elif record["type"] == "bequest.left":
            bequests.append(payload["text"])
    output = {"claims": claims, "bequests": bequests, "events": len(records)}
    print(json.dumps(output, indent=2, sort_keys=True))


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate", help="validate a seed")
    validate_parser.add_argument("seed")
    plant_parser = subparsers.add_parser("plant", help="plant into a fresh receiver home")
    plant_parser.add_argument("seed")
    plant_parser.add_argument("--home", required=True)
    plant_parser.add_argument("--policy")
    verify_parser = subparsers.add_parser("verify", help="verify a receiver home")
    verify_parser.add_argument("--home", required=True)
    show_parser = subparsers.add_parser("show", help="show claims and bequests")
    show_parser.add_argument("--home", required=True)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.command == "validate":
            raw, events = load_seed(args.seed)
            print("valid: %d events, sha256 %s" % (len(events), digest_bytes(raw)))
        elif args.command == "plant":
            home, receipt = plant(args.seed, args.home, args.policy)
            print("planted: %s" % home)
            print("artifact sha256: %s" % receipt["sha256"])
        elif args.command == "verify":
            records = verify_home(args.home)
            print("verified: %d locally signed events" % len(records))
        elif args.command == "show":
            show_home(args.home)
    except (OSError, TrialError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
