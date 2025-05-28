📌 Project Overview

This project is focused on understanding and implementing unit tests and integration tests in Python. You'll practice:

Writing test cases using unittest
Parameterizing tests using parameterized
Mocking and patching with unittest.mock
Testing both isolated functions (unit tests) and interconnected components (integration tests)
🎯 Learning Objectives
Understand the difference between unit and integration tests
Master common testing patterns: mocking, parametrizations, fixtures
Test external calls (e.g., HTTP, DB) using mocks
Apply memoization and test it
Build robust test suites for production code
🛠️ Technologies
Python 3.7+
unittest (Standard library)
parameterized for input variation
mock for controlling dependencies
📁 Project Structure
.
├── client.py             # Main GitHubOrgClient logic
├── utils.py              # Utility functions (nested map, JSON fetch, memoize)
├── test_utils.py         # Unit tests for utils.py
├── test_client.py        # Integration tests for GitHubOrgClient
└── fixtures.py           # Static mocked data for testing GitHub API responses
✅ Running the Tests
python3 -m unittest test_utils.py
python3 -m unittest test_client.py
🧪 Example: Unit Test for access_nested_map
@parameterized.expand([
    ("simple", {"a": 1}, ("a",), 1),
    ("nested", {"a": {"b": 2}}, ("a",), {"b": 2}),
    ("deep", {"a": {"b": 2}}, ("a", "b"), 2),
])
def test_access_nested_map(self, _, nested, path, expected):
    self.assertEqual(access_nested_map(nested, path), expected)
🔒 Requirements
Each function and class must be documented
All functions should be type-annotated
Must follow PEP8 coding style
Use mocking for external dependencies
🧠 Tips
Always isolate logic when writing unit tests
Use mocks for any function that connects to the network or database
Integration tests are larger and check system behavior, not just one function
