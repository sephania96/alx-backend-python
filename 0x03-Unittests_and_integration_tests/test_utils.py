#!/usr/bin/env python3
"""Unit test for utils module"""

import os
import sys
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock

# Add the project root to the Python path to enable imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

# Local import after setting sys.path
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function"""

    @parameterized.expand([
        ("simple_path", {"a": 1}, ("a",), 1),
        ("nested_path", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("deep_path", {"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, name, nested_map, path, expected):
        """Test valid access of nested maps and expected return values"""
        # Check if access_nested_map returns correct value for the path
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ("missing_key", {}, ("a",)),
        ("missing_nested_key", {"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, name, nested_map, path):
        """Test that KeyError is raised for missing keys in path"""
        # Use assertRaises to check that missing keys raise KeyError
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        expected_key = path[len(path) - len(cm.exception.args):][0]
        self.assertEqual(cm.exception.args[0], expected_key)


class TestGetJson(unittest.TestCase):
    """Tests for get_json function with HTTP mocking"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test that get_json returns expected payload and calls requests.get once"""
        # Patch 'requests.get' and simulate JSON response
        with patch('utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)  # Ensure it's called with correct URL
            self.assertEqual(result, test_payload)  # Ensure return matches expected


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator"""

    def test_memoize(self):
        """Ensure that memoize caches method result after first call"""

        class TestClass:
            # Basic method returning constant value
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()  # Will be memoized

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()
            result1 = obj.a_property  # First call, should call a_method
            result2 = obj.a_property  # Second call, should return cached result

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()  # Check that method was called only once


if __name__ == '__main__':
    unittest.main()
