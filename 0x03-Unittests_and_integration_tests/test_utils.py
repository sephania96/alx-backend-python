#!/usr/bin/env python3
"""Unit test for utils module"""

import sys
import os
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock

# Add the project root to the Python path to enable imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function"""

    @parameterized.expand([
        # Test with single-level dictionary
        ("simple_path", {"a": 1}, ("a",), 1),
        # Test with nested dictionary, return dict
        ("nested_path", {"a": {"b": 2}}, ("a",), {"b": 2}),
        # Test with nested dictionary, return value
        ("deep_path", {"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, name, nested_map, path, expected):
        """Test valid access of nested maps"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        # Key not found in empty dict
        ("missing_key", {}, ("a",)),
        # Missing second key in nested path
        ("missing_nested_key", {"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, name, nested_map, path):
        """Test KeyError is raised for missing keys in nested maps"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        # Check that the KeyError was raised on the correct key
        self.assertEqual(cm.exception.args[0], path[len(path) - len(cm.exception.args):][0])


class TestGetJson(unittest.TestCase):
    """Tests for get_json function with HTTP mocking"""

    @parameterized.expand([
        # Simulate external API response
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test get_json returns correct payload and calls requests.get once"""
        with patch('utils.requests.get') as mock_get:
            # Create a mock response with .json() returning our test payload
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            # Call the actual function and verify behavior
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


if __name__ == '__main__':
    unittest.main()