import pytest
import json
import os
import pathlib
from serial_communication import DeviceCommunicator

def load_test_cases(json_files):
    tests = []
    for json_file in json_files.split(" "):
        with open(json_file, 'r') as file:
            test_cases = json.load(file)
            for test_case in test_cases:
                test_case['json_file_path'] = os.path.basename(json_file)
            tests+=test_cases
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
    print(metafunc.fixturenames)
    if "test_case" in metafunc.fixturenames:
        if metafunc.config.getoption("--run-all"):
            test_case_dir = os.listdir('test_cases')
            test_case_dir.sort()
            tc_except_list = []
            if metafunc.config.getoption("--except"):
                # Convert path to OS format
                tc_except_list = [os.path.normpath(tc) for tc in metafunc.config.getoption("--except")]

            all_json_files = [os.path.join('test_cases', file) for file in test_case_dir if file.endswith('.json')]
            json_files_to_load = [file for file in all_json_files if file not in tc_except_list]
        elif metafunc.config.getoption("--json-config"):
            json_files_to_load = metafunc.config.getoption("--json-config")
        
        test_cases_list = []
        for json_config in json_files_to_load:
            test_cases = load_test_cases(json_config)  # Load test cases from the JSON file
            test_cases_list += test_cases
        # Pretty print to have test case name with its number and file name at the beginning. 
        # This also prevents wrong test execution in alphabetical order
        metafunc.parametrize("test_case", test_cases_list, ids=[
            f"{index}-{case['json_file_path']}:{case['test_name']}"
            for index, case
            in enumerate(test_cases_list)
        ])

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