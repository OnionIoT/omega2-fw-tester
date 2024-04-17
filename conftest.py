import pytest
import sys

def pytest_addoption(parser):
    # Define a command-line option for the JSON configuration file
    parser.addoption("--json-config", action="store", required=True,
                     help="Path to the JSON file containing test cases.")

@pytest.fixture(scope="session")
def json_config(request):
    # Retrieve the JSON config file path
    config_path = request.config.getoption("--json-config")
    if not config_path:
        print("ERROR: --json-config option is required. Please specify a JSON file path.")
        sys.exit(1)  # Exit the test session if no config path is provided
    return config_path
