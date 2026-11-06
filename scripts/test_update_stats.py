import unittest
from collections import Counter
from unittest.mock import patch
from update_stats import language_rows, public_repositories


class StatsTests(unittest.TestCase):
    def test_small_language_list(self):
        self.assertEqual(language_rows(Counter({'Python': 20})), [('Python', 20)])

    def test_remainder_preserves_total(self):
        values = Counter({str(i): i+1 for i in range(8)})
        rows = language_rows(values)
        self.assertEqual(len(rows), 6)
        self.assertEqual(rows[-1][0], 'Outras')
        self.assertEqual(sum(n for _, n in rows), sum(values.values()))

    def test_empty_language_list(self):
        self.assertEqual(language_rows(Counter()), [])

    @patch('update_stats.api')
    def test_filters_private_and_fork_repositories(self, api):
        api.return_value = [
            {'private': False, 'fork': False, 'name': 'original'},
            {'private': True, 'fork': False, 'name': 'private'},
            {'private': False, 'fork': True, 'name': 'fork'},
        ]
        self.assertEqual([r['name'] for r in public_repositories('test')], ['original'])

    @patch('update_stats.api')
    def test_pagination(self, api):
        public = {'private': False, 'fork': False}
        api.side_effect = [[public]*100, [public]]
        self.assertEqual(len(public_repositories('test')), 101)
        self.assertIn('page=2', api.call_args.args[0])


if __name__ == '__main__':
    unittest.main()
