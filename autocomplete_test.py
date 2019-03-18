# Author: Cameron Brown
# Date: 16/03/2019
# Purpose: Test query autocomplete implementation.

import unittest
from autocomplete import QueryAutoCompleter

class TestQueryAutoCompleter(unittest.TestCase):
    TEST_KEYWORD = "test"
    TEST_KEYWORDS = ["apple", "bannana", "avacado"]
    TEST_KEYWORDS_2 = ["broil", "broiler", "broker", "broccoli", "broadsword"]

    def test_empty(self):
        assert QueryAutoCompleter(self.TEST_KEYWORDS).auto_complete("") == []

    def test_single(self):
        assert QueryAutoCompleter(["test"]).auto_complete("test") == ["test"]

    def test_multi(self):
        assert QueryAutoCompleter(self.TEST_KEYWORDS).auto_complete("a") == ["apple", "avacado"]
        assert QueryAutoCompleter(self.TEST_KEYWORDS).auto_complete("b") == ["bannana"]
        assert QueryAutoCompleter(self.TEST_KEYWORDS).auto_complete("avacado") == ["avacado"]
        assert QueryAutoCompleter(self.TEST_KEYWORDS).auto_complete("avacadoo") == []

    def test_multi2(self):
        assert QueryAutoCompleter(self.TEST_KEYWORDS_2).auto_complete("b") == self.TEST_KEYWORDS_2
        assert QueryAutoCompleter(self.TEST_KEYWORDS_2).auto_complete("br") == self.TEST_KEYWORDS_2
        assert QueryAutoCompleter(self.TEST_KEYWORDS_2).auto_complete("bro") == self.TEST_KEYWORDS_2
        assert QueryAutoCompleter(self.TEST_KEYWORDS_2).auto_complete("broi") == ["broil", "broiler"]
        assert QueryAutoCompleter(self.TEST_KEYWORDS_2).auto_complete("broil") == ["broil", "broiler"]
        assert QueryAutoCompleter(self.TEST_KEYWORDS_2).auto_complete("broile") == ["broiler"]
        assert QueryAutoCompleter(self.TEST_KEYWORDS_2).auto_complete("broc") == ["broccoli"]
        assert QueryAutoCompleter(self.TEST_KEYWORDS_2).auto_complete("broa") == ["broadsword"]
        assert QueryAutoCompleter(self.TEST_KEYWORDS_2).auto_complete("broo") == []

if __name__ == '__main__':
    unittest.main()