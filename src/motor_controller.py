# From motor_controller.py
import serial
import time

class MotorController:
    def __init__(self, port, baud_rate=115200):
        self.port = port
        self.baud_rate = baud_rate
        self.arduino = None

    def connect(self):
        try:
            self.arduino = serial.Serial(self.port, self.baud_rate)
            time.sleep(2)  # Wait for Arduino to initialize
            print("Connected to Arduino.")
            return True
        except serial.SerialException as e:
            print(f"Error connecting to Arduino: {e}")
            return False

    def disconnect(self):
        if self.arduino:
            self.arduino.close()
            print("Disconnected from Arduino.")

    def send_solution(self, solution):
        if not self.arduino:
            print("Not connected to Arduino.")
            return

        print("Sending solution to Arduino:", solution)
        self.arduino.write((solution + '\n').encode())

        # Wait for Arduino to respond with "Done"
        while True:
            if self.arduino.in_waiting:
                line = self.arduino.readline().decode().strip()
                print("Arduino:", line)
                if "Done" in line:
                    break
