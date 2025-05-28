#!/usr/bin/env python3

#Unit test for utils.access_nested_map
from utils import access_nested_map
from parameterized import parameterized
import unittest

##Test cases for access_nested_map function
class TestAccessNestedMap(unittest.TestCase):
    #Test cases for access_nested_map function
    @parameterized.expand([
        ("simple_path", {"a": 1}, ("a",), 1),
        ("nested_path", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("deep_path", {"a": {"b": 2}}, ("a", "b"), 2),
    ])
    #Test cases for access_nested_map function
    def test_access_nested_map(self, name, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == '__main__':
    unittest.main()