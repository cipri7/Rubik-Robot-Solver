# Rubik-Robot-Solver

This project implements a Rubik's Cube solver using a robot. It includes functionality for scanning the cube's faces using a camera, classifying the colors of the stickers, generating a solution using the Kociemba algorithm, and sending the solution to an Arduino-controlled motor system to physically solve the cube.

## Features

- **Cube Scanning:** Captures images of the cube faces using a camera and identifies the colors of each sticker.
- **Color Classification:** Uses a color classifier to determine the color of each sticker based on HSV values.
- **Solution Generation:** Employs the Kociemba algorithm to generate a solution for the scanned cube.
- **Motor Control:** Sends the solution to an Arduino, which controls the motors to perform the necessary moves.
- **Calibration:** Allows calibrating the color classification based on the current lighting conditions.
- **Visualization:** Provides a visual representation of the scanned cube and the solution.

## Usage

Run the main.py script which will first scan the cube using scan_cube.py and then launch the visualize_cube.py script. This script displays the scanned cube state. You can manually edit the scanned state within the visualizer, confirm the state, and then send the solution to the Arduino to solve the cube. Press [S] in the visualizer to send the solution to the Arduino.

## Requirements

- pygame
- pyserial
- kociemba
- numpy
- opencv-python

Install the required packages using:

```bash
pip install -r requirements.txt
```

Upload motor_solver.c to Arduino.

## Credits

This project utilizes the kociemba library for solving the Rubik's Cube.


