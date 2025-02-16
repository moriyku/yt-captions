import os
import unittest
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import functions from get_captions.py
from get_captions import clean_captions

class TestCleanCaptions(unittest.TestCase):
    def test_remove_timestamps_html_and_duplicates(self):
        raw_text = (
            "00:01:23.456 --> 00:01:25.789\n"
            "<c>Hello</c>\n"
            "\n"
            "<c>Hello</c>\n"
            "This is a test.\n"
            "This is a test.\n"
        )
        # Expected result:
        # - Timestamp lines are removed.
        # - HTML tags (now using <c>) are stripped, leaving "Hello".
        # - Empty lines and consecutive duplicate lines are removed.
        expected = "Hello\nThis is a test."
        result = clean_captions(raw_text)
        self.assertEqual(result, expected)

    def test_clean_captions_no_change(self):
        # Text that doesn't need any changes should be returned as is.
        raw_text = "Just some text."
        expected = "Just some text."
        result = clean_captions(raw_text)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
