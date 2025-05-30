#!/usr/bin/env python3
"""
Unit and integration tests for GithubOrgClient
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import fixtures

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient - Tasks 5 to 7"""

    @patch("client.GithubOrgClient.org", new_callable=Mock)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url property using mocked org data"""
        expected_url = "https://api.github.com/orgs/test_org/repos"
        mock_org.return_value = {"repos_url": expected_url}
        client = GithubOrgClient("test_org")
        self.assertEqual(client._public_repos_url, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos method with mocked API response and property"""
        payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "other"}},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = payload

        # Patch the private property to avoid actual HTTP
        with patch.object(GithubOrgClient, "_public_repos_url", return_value="mocked_url") as mock_url:
            client = GithubOrgClient("test_org")
            result = client.public_repos("apache-2.0")
            self.assertEqual(result, ["repo1"])
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand([
        ("repo_with_matching_license", {"license": {"key": "my_license"}}, "my_license", True),
        ("repo_with_non_matching_license", {"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, name, repo, license_key, expected):
        """Test static method has_license with different inputs"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    fixtures.TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos using fixtures - Task 8"""

    @classmethod
    def setUpClass(cls):
        """Set up class-level mock to patch requests.get using side_effect"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Return org_payload first, then repos_payload
        cls.mock_get.side_effect = [
            Mock(json=Mock(return_value=cls.org_payload)),
            Mock(json=Mock(return_value=cls.repos_payload))
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop the get patcher after all tests are done"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected repo list from fixture"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters repos correctly by license key"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
