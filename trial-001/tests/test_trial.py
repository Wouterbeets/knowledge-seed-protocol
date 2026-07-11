import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


TRIAL_DIR = Path(__file__).resolve().parents[1]
SEED = TRIAL_DIR / "seeds" / "responsible-succession.seed.jsonl"
POLICY = TRIAL_DIR / "policy.example.json"
SPEC = importlib.util.spec_from_file_location("ksp_trial", TRIAL_DIR / "ksp_trial.py")
ksp_trial = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ksp_trial)


class TrialTests(unittest.TestCase):
    def test_fixture_validates_and_contains_no_forbidden_fields(self):
        raw, events = ksp_trial.load_seed(SEED)
        self.assertEqual(10, len(events))
        self.assertEqual([], ksp_trial.forbidden_paths(events))
        self.assertGreater(len(raw), 0)

    def test_rejects_executable_field_at_any_depth(self):
        events = [json.loads(line) for line in SEED.read_text().splitlines()]
        events[4]["payload"]["nested"] = {"script": "print('foreign')"}
        with self.assertRaisesRegex(ksp_trial.TrialError, "forbidden field"):
            ksp_trial.validate_events(events)

    def test_rejects_reordered_stream(self):
        events = [json.loads(line) for line in SEED.read_text().splitlines()]
        events[2], events[3] = events[3], events[2]
        with self.assertRaisesRegex(ksp_trial.TrialError, "increasing"):
            ksp_trial.validate_events(events)

    def test_policy_cannot_remove_declaration(self):
        with tempfile.TemporaryDirectory() as directory:
            policy = Path(directory) / "policy.json"
            policy.write_text(json.dumps({"reject_types": ["capability.declared"]}))
            with self.assertRaisesRegex(ksp_trial.TrialError, "protected"):
                ksp_trial.load_policy(policy)

    def test_end_to_end_rebuild_action_and_replay(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "receiver"
            ksp_trial.plant(SEED, home, POLICY)
            artifact = home / "responsible-succession"
            source = artifact.read_text()
            seed_text = SEED.read_text()
            self.assertNotEqual(seed_text, source)
            self.assertNotIn("self/philosophy:garden", source)

            claim = subprocess.run(
                [str(artifact), "claim", "local reconstruction works"],
                check=True, capture_output=True, text=True,
            )
            self.assertEqual("local-1", claim.stdout.strip())
            subprocess.run(
                [str(artifact), "verify", "local-1", "fail", "first check exposed a gap"],
                check=True, capture_output=True, text=True,
            )
            subprocess.run(
                [str(artifact), "verify", "local-1", "pass", "gap repaired and replay passed"],
                check=True, capture_output=True, text=True,
            )
            subprocess.run(
                [str(artifact), "bequeath", "inspect the failed check too"],
                check=True, capture_output=True, text=True,
            )

            records = ksp_trial.verify_home(home)
            original_claims = [r for r in records if r["type"] == "claim.made"]
            checks = [r for r in records if r["type"] == "claim.verified"]
            self.assertEqual(1, len(original_claims))
            self.assertEqual(["fail", "pass"], [r["payload"]["result"] for r in checks])
            accepted = [r for r in records if r["type"] == "seed.event.accepted"]
            remapped = [r for r in accepted if r["payload"]["transformed"]]
            self.assertEqual(10, len(accepted))
            self.assertEqual("local.culture.practice", remapped[0]["payload"]["local_type"])

    def test_tampering_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "receiver"
            ksp_trial.plant(SEED, home, POLICY)
            artifact = home / "responsible-succession"
            artifact.write_text(artifact.read_text() + "\n# changed\n")
            with self.assertRaisesRegex(ksp_trial.TrialError, "digest"):
                ksp_trial.verify_home(home)

    def test_cli_is_stdlib_only_and_reports_valid_fixture(self):
        result = subprocess.run(
            [sys.executable, str(TRIAL_DIR / "ksp_trial.py"), "validate", str(SEED)],
            check=True, capture_output=True, text=True,
        )
        self.assertIn("valid: 10 events", result.stdout)


if __name__ == "__main__":
    unittest.main()
