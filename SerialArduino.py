import serial
import time

class SerialArduino:
    def __init__(self, com_port='COM3', baudrate=9600, timeout=None):
        self.com_port=com_port
        self.baudrate=baudrate
        self.timeout=timeout

    def send_command(self, command) -> str:
        ser = serial.Serial(self.com_port, self.baudrate, timeout=self.timeout)  # Set timeout to prevent blocking
        time.sleep(2)  # Wait for Arduino to initialize
        ser.flushInput()  # Clear buffer
        ser.write(command)  # Send command
        time.sleep(0.1)  # Give Arduino time to process
        response = ser.readline().decode('utf-8').strip()
        ser.close()  # Always close the port when done
        return response

