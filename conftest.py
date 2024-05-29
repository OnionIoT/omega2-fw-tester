import pytest
import sys

def pytest_addoption(parser):
    # Define a command-line option for the JSON configuration file
    parser.addoption("--json-config", nargs='+', action="store",
                     help="Path to the JSON file(s) containing test cases.")
    parser.addoption("--run-all", action="store_true", default=False, 
                     help="Run all tests from JSON files in test_cases directory.")
