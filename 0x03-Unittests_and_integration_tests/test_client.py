#!/usr/bin/env python3
"""Unit test for utils and GithubOrgClient modules"""

import os
import sys
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock

# Add the project root to the Python path to enable imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

# Local import after setting sys.path
from utils import access_nested_map, get_json, memoize
from client import GithubOrgClient
import fixtures

class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function"""

    @parameterized.expand([
        ("simple_path", {"a": 1}, ("a",), 1),
        ("nested_path", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("deep_path", {"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, name, nested_map, path, expected):
        """Test valid access of nested maps and expected return values"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ("missing_key", {}, ("a",)),
        ("missing_nested_key", {"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, name, nested_map, path):
        """Test that KeyError is raised for missing keys in path"""
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
        with patch('utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator"""

    def test_memoize(self):
        """Ensure that memoize caches method result after first call"""

        class TestClass:
            # Simple method returning a constant value
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()  # Should only call a_method once due to memoization

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()
            result1 = obj.a_property  # First call triggers a_method
            result2 = obj.a_property  # Second call uses cached result

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()  # Ensure method was only called once


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get):
        """Test that org returns correct org payload"""
        expected_payload = {"login": org_name}
        mock_get.return_value = expected_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_payload)
        mock_get.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch('client.GithubOrgClient.org', new_callable=Mock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns repos_url from org payload"""
        expected_url = "https://api.github.com/orgs/test_org/repos"
        mock_org.return_value = {"repos_url": expected_url}
        client = GithubOrgClient("test_org")
        self.assertEqual(client._public_repos_url, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns filtered repo names from payload"""
        repos_payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "other"}},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = repos_payload

        # Patch the _public_repos_url to avoid hitting actual endpoint
        with patch.object(GithubOrgClient, "_public_repos_url", return_value="dummy_url") as mock_url:
            client = GithubOrgClient("test_org")
            result = client.public_repos("apache-2.0")
            self.assertEqual(result, ["repo1"])
            mock_get_json.assert_called_once()  # Ensure get_json was called once
            mock_url.assert_called_once()  # Ensure URL was accessed

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns True if license matches, else False"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    fixtures.TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class-level mock for requests.get to use fixture payloads"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Simulate responses in sequence for org then repos
        cls.mock_get.side_effect = [
            Mock(json=Mock(return_value=cls.org_payload)),
            Mock(json=Mock(return_value=cls.repos_payload)),
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patcher after tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test full integration: public_repos returns expected repo names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by license key"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)


if __name__ == '__main__':
    unittest.main()