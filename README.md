# omega2-fw-tester
Program to test Omega2 firmware functionality (based on sending commands on serial and reading output)

This firmware test program is designed to test the firmware functionality of Omega2 devices connected via USB serial. It uses Python and pytest to automate the sending of commands and the validation of responses from the device under test (DUT).

## Requirements

- Python: Python 3.6 or later.
- Python modules
    - PySerial: Required for serial communication with the device.
    -  pytest: Used for running tests and handling test cases.

## Installation

Setting Up Python Environment

1.Install Python: Ensure Python 3.6+ is installed on your system.
1. Install Dependencies:
    ```
    pip install pyserial pytest
    ```


## Device-Under-Test Connection

> The Device-Under-Test (DUT) is the target Omega2 device

The program expects an Omega2 device (DUT) connected to the computer/device running the testing program by USB serial.

```
                                                        
  ┌────────────────┐                    ┌──────────────┐  
  │ Testing Device │                    │  Omega2 DUT  │  
  │                │     ┌────────┐     │              │  
  │                │     │ USB    │     │              │  
  │             USB├────►│ to     ├────►│UART0         │  
  │                │     │ Serial │     │              │  
  │                │     └────────┘     │              │  
  │                │                    │              │  
  └────────────────┘                    └──────────────┘  
                                                        
```

The default port is `/dev/tty.usbserial-0001`. This can be changed in the `test_device.py` program.

## Test Configuration

There are several tests covering basic functionality. Working principle is simple:
- The Testing Device sends a command(s) to the DUT over serial terminal
- The Testing Device reads responses from the DUT and compares them against expected output (within a timeout)

The tests are defined in a JSON file:

```
[
    {
        "test_name": "TEST_NAME",
        "commands": [
            "COMMAND"
        ],
        "expected_response": "RESPONSE",
        "timeout": 5 // in seconds,
        "if_failed": "Instruction for user"
    },
    ...
]
```

See `sanity_tests.json` for an example.

## Preparation before running the Tests

To verify all basic Omega2 functionality you need to prepare physical env:
- Connect your Omega2 device via USB serial
- Plug **SD card** in to verify SD card related functionality
- Plug **USB device** in to verify USB related functionality
- Connect an **I2C device** to verify I2C related functionality
- Power on your Omega2 device 

Also prepare your system environment:
- Set `WIFI_SSID` environmental variable with value of you Wi-Fi network ssid:
  - `export WIFI_SSID=<your wifi ssid>`
- Set `WIFI_PASSWORD` environmental variable with value of you Wi-Fi network password:
  - `export WIFI_PASSWORD=<your wifi password>`

## Running the Tests

To run the tests, use the following command, specifying the JSON configuration file as needed:

```
pytest -v test_device.py --json-config <JSON TEST FILE1> <JSON TEST FILE2> ...
```

Or run all tests from 'test_cases' directory:
```
pytest -v test_device.py --run-all
```

## Sample Output

The tests in `sanity_tests.json` have one test that is expected to pass, and another that's expected to fail.

To run:
```
pytest -v test_device.py --json-config=sanity_tests.json
```

Sample output:
```
=========================================================================================== test session starts ============================================================================================
platform darwin -- Python 3.8.3, pytest-8.1.1, pluggy-1.4.0 -- /Users/lazar/.pyenv/versions/3.8.3/envs/omega2-fw-tester-3.8.3/bin/python
cachedir: .pytest_cache
rootdir: /Users/lazar/workspace/onion/omega2/omega2-fw-tester
collected 2 items

test_device.py::test_device_responses[sanity_test] PASSED                                                                                                                                            [ 50%]
test_device.py::test_device_responses[expecting_fail] FAILED                                                                                                                                         [100%]

================================================================================================= FAILURES =================================================================================================
__________________________________________________________________________________ test_device_responses[expecting_fail] ___________________________________________________________________________________

test_case = {'commands': ['status', 'query'], 'expected_response': 'Ready', 'test_name': 'expecting_fail', 'timeout': 3}, device = <serial_communication.DeviceCommunicator object at 0x104600310>

    def test_device_responses(test_case, device):
        for command in test_case['commands']:
            device.send_command(command)
        response = device.read_until_response(test_case['expected_response'], test_case['timeout'])
>       assert test_case['expected_response'] in response, f"Expected '{test_case['expected_response']}' within {test_case['timeout']} seconds"
E       AssertionError: Expected 'Ready' within 3 seconds

test_device.py:29: AssertionError
------------------------------------------------------------------------------------------ Captured stdout setup -------------------------------------------------------------------------------------------
> Connecting to device /dev/tty.usbserial-0001
----------------------------------------------------------------------------------------- Captured stdout teardown -----------------------------------------------------------------------------------------
> Closing serial connection
========================================================================================= short test summary info ==========================================================================================
FAILED test_device.py::test_device_responses[expecting_fail] - AssertionError: Expected 'Ready' within 3 seconds
======================================================================================= 1 failed, 1 passed in 3.10s ========================================================================================

```
