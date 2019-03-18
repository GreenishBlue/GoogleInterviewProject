# Author: Cameron Brown
# Date: 19/03/2019
# Purpose: Provides test functionality for parsing queries.

import unittest
from query import QueryParser

class TestQueryParser(unittest.TestCase):
    TEST_KEYWORD = "test"

    def test_empty(self):
        pass
        # assert QueryAutoCompleter(self.TEST_KEYWORDS).auto_complete("") == []

if __name__ == '__main__':
    unittest.main()