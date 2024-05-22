import serial
import time

class DeviceCommunicator:
    def __init__(self, port, baud_rate, timeout=2):
        print(f"> Connecting to device {port}")
        self.ser = serial.Serial(port, baud_rate, timeout=timeout)
        self.ser.flushInput()

    def send_command(self, command):
        """Send a command to the device."""
        self.ser.write(command.encode() + b'\n')  # Ensure newline is added if needed by your device protocol.

    def read_until_response(self, expected_response, timeout_sec):
        """Read from the device until an expected response is found or the timeout is reached."""
        end_time = time.time() + timeout_sec
        received_data = ''
        while time.time() < end_time:
            if self.ser.in_waiting > 0:
                received_data += self.ser.read(self.ser.in_waiting).decode('utf-8')
                if expected_response in received_data:
                    return received_data
        return received_data  # Return what was received even if it doesn't contain the expected response.
    
    def reset_serial_buffers (self, time_s):
        """Wait for some time and reset I/O serial buffer"""
        print(f"> Waiting for {time_s} secs and resetting I/O buffers")
        time.sleep(time_s)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def close(self):
        """Close the serial connection."""
        self.ser.close()
        print("> Closing serial connection")