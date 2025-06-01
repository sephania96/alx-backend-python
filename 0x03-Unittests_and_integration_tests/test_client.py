#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
import requests # Needed to mock requests.get

# Assuming client.py and fixtures.py are in the same directory
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        and get_json is called once with the right URL.
        """
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, test_payload)

    @patch("client.get_json")
    def test_org_returns_correct_payload(self, mock_get_json):
        """
        Test that the 'org' property of GithubOrgClient returns the exact JSON payload
        returned by a successful call to client.get_json.
        """
        expected_payload = {"login": "testorg", "id": 12345}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient("testorg")
        actual_payload = client.org # Accessing the 'org' property

        mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg")
        self.assertEqual(actual_payload, expected_payload)

    def test_public_repos_url(self):
        """
        Unit-test GithubOrgClient._public_repos_url.
        Mocks the 'org' property to return a known payload and asserts
        that _public_repos_url returns the correct 'repos_url'.
        """
        test_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("some_org")
            result_url = client._public_repos_url
            mock_org.assert_called_once()
            self.assertEqual(result_url, test_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Unit-test GithubOrgClient.public_repos.
        Mocks get_json to return a payload and
        _public_repos_url property to return a URL.
        Verifies that public_repos returns expected list and mocks were called.
        """
        # Define the payload that mock_get_json will return
        repos_payload_mock = [ # Renamed to avoid conflict with imported fixture
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": None},
            {"name": "repo3", "license": {"key": "apache-2.0"}},
            {"name": "another-repo", "license": {"key": "gpl"}}
        ]
        mock_get_json.return_value = repos_payload_mock

        # Define the URL that _public_repos_url will return
        mock_repos_url = "https://api.github.com/orgs/some_org/repos"

        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = mock_repos_url
            client = GithubOrgClient("some_org")
            result_repos = client.public_repos()

            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_repos_url)
            expected_repo_names = ["repo1", "repo2", "repo3", "another-repo"]
            self.assertEqual(result_repos, expected_repo_names)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": None}, "my_license", False),
        ({"name": "no_license_repo"}, "my_license", False),
        ({}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected_return_value):
        """
        Unit-test GithubOrgClient.has_license static method.
        Tests if the method correctly identifies if a repository has a given license key.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_return_value)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test class for GithubOrgClient.public_repos.
    Mocks external requests (requests.get) to use fixture data.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up the class-level mock for requests.get.
        This mock will have a side_effect to return specific JSON responses
        based on the URL received by requests.get().json().
        """
        # Create a mock response object
        mock_response = MagicMock()

        # Define the side_effect for the .json() method of the mock_response.
        # This will simulate the sequence of JSON payloads returned by API calls.
        mock_response.json.side_effect = [
            cls.org_payload,   # First call to .json() (e.g., from client.org)
            cls.repos_payload  # Second call to .json() (e.g., from client.public_repos)
        ]

        # Start the patcher for requests.get
        # When requests.get is called, it will return our mock_response object.
        cls.get_patcher = patch("requests.get", return_value=mock_response)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        Stop the patcher after all integration tests are done.
        This restores the original requests.get function.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Tests the public_repos method in an integration context.
        Uses mocked requests.get to ensure no external network calls.
        """
        # Instantiate the client with an organization name that matches the org_payload's login
        client = GithubOrgClient(self.org_payload["login"])

        # Call the method under test.
        # This will internally trigger calls to self.org (which fetches org_payload)
        # and then a call to get_json for the repos_url (which fetches repos_payload).
        repos = client.public_repos()

        # Assertions
        # 1. Verify that requests.get was called with the correct URLs in the expected order.
        expected_calls = [
            unittest.mock.call(f"https://api.github.com/orgs/{self.org_payload['login']}"),
            unittest.mock.call(self.org_payload["repos_url"])
        ]
        self.mock_get.assert_has_calls(expected_calls, any_order=False)

        # 2. Verify that the returned list of repository names matches the expected_repos fixture.
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Tests the public_repos method with a license filter in an integration context.
        """
        # Instantiate the client
        client = GithubOrgClient(self.org_payload["login"])

        # Call the method under test with the license filter.
        # This will make the same underlying calls to requests.get as test_public_repos.
        repos = client.public_repos(license="apache-2.0")

        # Assertions
        # The requests.get calls should be identical to the previous test.
        expected_calls = [
            unittest.mock.call(f"https://api.github.com/orgs/{self.org_payload['login']}"),
            unittest.mock.call(self.org_payload["repos_url"])
        ]
        self.mock_get.assert_has_calls(expected_calls, any_order=False)

        # Verify that the filtered list matches the expected apache2_repos fixture.
        self.assertEqual(repos, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()