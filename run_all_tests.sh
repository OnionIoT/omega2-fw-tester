#!/bin/bash

for json_config in test_cases/*.json; do
    echo "Executing $json_config test cases" 
    python3 -m pytest -v test_device.py --json-config=$json_config
done;