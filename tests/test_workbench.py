import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.fixture = json.loads((ROOT / 'data/workbench.json').read_text())
        self.save()

    def save(self):
        (self.root / 'workbench.json').write_text(json.dumps(self.fixture))

    def run_action(self, action, key=None, succeeds=True):
        args = [sys.executable, '-m', 'app', action, '--data', str(self.root),
                '--ledger', str(self.root / 'receipts.sqlite3')]
        if key is not None:
            args.extend(['--key', key])
        proc = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=5)
        if succeeds:
            self.assertEqual(proc.returncode, 0, proc.stderr)
            return json.loads(proc.stdout)
        self.assertEqual(proc.returncode, 2, proc.stderr)
        return proc.stderr

    def test_stop_and_enrollment_affect_send_eligibility(self):
        self.assertEqual(self.run_action('enrollment')['assigned'], {'short': 2, 'story': 3})
        issued = self.run_action('broadcast')
        self.assertEqual(issued['variant'], 'story')
        self.fixture['stop'] = '2026-06-16T21:00:00Z'
        self.save()
        self.assertEqual(self.run_action('metrics')['story']['opened'], 1)
        self.assertEqual(self.run_action('decision')['variant'], 'undecided')
        self.assertEqual(self.run_action('broadcast', 'craft-week'), issued)
        self.assertIn('曝光量不足', self.run_action('broadcast', succeeds=False))
