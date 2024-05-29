import pytest
import json
import os
from serial_communication import DeviceCommunicator

def load_test_cases(json_files):
    tests = []
    for json_file in json_files.split(" "):
        with open(json_file, 'r') as file:
            tests+=json.load(file)
    return tests

# Fixture for the device communication, assuming DeviceCommunicator is properly defined elsewhere
@pytest.fixture
def device():
    communicator = DeviceCommunicator('/dev/tty.usbserial-0001', 115200)
    yield communicator
    communicator.close()

# Use pytest to dynamically load test cases based on the command-line argument
def pytest_generate_tests(metafunc):
    # This function is called once for each test function found in the test module
    if metafunc.config.getoption("--run-all"):
        json_files = [os.path.join('test_cases', file) for file in os.listdir('test_cases') if file.endswith('.json')]    
    elif metafunc.config.getoption("--json-config"):
        json_files = metafunc.config.getoption("--json-config")
    
    test_cases_list = []
    for json_config in json_files:
        test_cases = load_test_cases(json_config)  # Load test cases from the JSON file
        test_cases_list += test_cases
    # Pretty print to have test case name with its number at the beginning. This also prevents wrong test execution in alphabetical order
    metafunc.parametrize("test_case", test_cases_list, ids=[f"{i}_{case['test_name']}" for case, i in zip(test_cases_list, range(len(test_cases_list)))])

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