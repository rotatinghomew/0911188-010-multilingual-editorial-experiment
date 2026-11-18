import json
from pathlib import Path
import tempfile
import unittest
from app.service import report
from app.storage import DataError, load

ROOT = Path(__file__).parents[1]

class ProductTests(unittest.TestCase):
    def test_summary_uses_declared_table_and_measure(self):
        result = report(ROOT / 'data')
        self.assertEqual(result['summary'], sorted(result['summary'], key=lambda row: row['group']))
        self.assertTrue(result['summary'])
        self.assertGreater(sum(row['rows'] for row in result['summary']), 0)

    def test_invalid_table_shape_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, 'data.json').write_text(json.dumps({'definition': {}, 'tables': {'bad': {}}}))
            with self.assertRaises(DataError):
                load(directory)

if __name__ == '__main__':
    unittest.main()
