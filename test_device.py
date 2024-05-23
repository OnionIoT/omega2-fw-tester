import pytest
import json
import os
from serial_communication import DeviceCommunicator

def load_test_cases(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

# Fixture for the device communication, assuming DeviceCommunicator is properly defined elsewhere
@pytest.fixture
def device():
    communicator = DeviceCommunicator('/dev/tty.usbserial-0001', 115200)
    yield communicator
    communicator.close()

# Use pytest to dynamically load test cases based on the command-line argument
def pytest_generate_tests(metafunc):
    # This function is called once for each test function found in the test module
    if "test_case" in metafunc.fixturenames:  # Check if 'test_case' is used in the test
        json_config = metafunc.config.getoption("--json-config")  # Get the JSON config file path
        test_cases = load_test_cases(json_config)  # Load test cases from the JSON file
        metafunc.parametrize("test_case", test_cases, ids=[case['test_name'] for case in test_cases])

# The test function uses the 'device' fixture and the 'test_case' parameter
def test_device_responses(test_case, device):
    for command in test_case['commands']:
        command = command.format(**os.environ)
        if "wait_and_reset_serial_buffers" in command:
            time_s = int(''.join(filter(str.isdigit, command)))
            device.wait_and_reset_serial_buffers(time_s)
            continue
        device.send_command(command)
    response = device.read_until_response(test_case['expected_response'], test_case['timeout'])
    assert test_case['expected_response'] in response, f"Expected '{test_case['expected_response']}' within {test_case['timeout']} seconds\n {test_case['if_failed']}"