import pytest
import sys

def pytest_addoption(parser):
    # Define a command-line option for the JSON configuration file
    parser.addoption("--json-config", nargs='+', action="store",
                     help="Path to the JSON file(s) containing test cases.")
    parser.addoption("--run-all", action="store_true", default=False, 
                     help="Run all tests from JSON files in test_cases directory.")
    parser.addoption("--except", nargs='+', action="store",
                     help="Path to the JSON file(s) with test cases which won't be run.")

def pytest_configure(config):
    json_config = config.getoption("--json-config")
    run_all = config.getoption("--run-all")
    if not json_config and not run_all:
        raise pytest.UsageError("--json-config or --run-all parameter is required")