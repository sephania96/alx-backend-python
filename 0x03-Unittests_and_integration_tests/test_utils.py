#!/usr/bin/env python3
"""Unit test for utils.access_nested_map"""

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

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
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == '__main__':
    unittest.main()