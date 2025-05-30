#!/usr/bin/env python3
"""Unit test for utils.access_nested_map"""

import sys
import os

# Add the project root to the Python path to enable imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function"""

    @parameterized.expand([
        ("simple_path", {"a": 1}, ("a",), 1),
        ("nested_path", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("deep_path", {"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, name, nested_map, path, expected):
        """Test valid access of nested maps"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ("missing_key", {}, ("a",)),
        ("missing_nested_key", {"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, name, nested_map, path):
        """Test KeyError is raised for missing keys in nested maps"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        # The raised key will be the first missing one in the path
        self.assertEqual(cm.exception.args[0], path[len(path) - len(cm.exception.args):][0])


if __name__ == '__main__':
    unittest.main()
