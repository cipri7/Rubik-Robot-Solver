# Rubik-Robot-Solver

This project solves a Rubik's Cube using a combination of computer vision and robotics. It scans the cube's faces using a camera, determines the cube's state, calculates the solution, and then sends the solution to an Arduino-controlled robot to execute the moves.

## Prerequisites

Before you begin, ensure you have the following:

*   **Python 3.6+**
*   **pip** (Python package installer)
*   **A webcam** connected to your computer.
*   **An Arduino** connected to your computer.
*   **A Rubik's Cube**

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd Rubik-Robot-Solver
    ```

2.  **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Calibration:**
    *   Run the `scan_cube.py` script to calibrate the color detection. This step is crucial for accurate color recognition.
    *   The script will prompt you to show each face of the cube (W, R, G, Y, O, B) to the camera. Center the face and press SPACE to capture its color.
    *   If you have a pre-existing calibration, you can skip the calibration by pressing any key other than 'c' when prompted.
    *   The calibration data is saved in `src/calibration.json`.

2.  **Arduino Port:**
    *   Modify the `ARDUINO_PORT` variable in [`src/visualize_cube.py`](https://github.com/cipri7/Rubik-Robot-Solver/blob/main/src/visualize_cube.py) to match the serial port of your Arduino.

    ```python
    # From src/visualize_cube.py
    ARDUINO_PORT = "/dev/cu.usbmodem1101"  # Update as needed
    ```

    *   You can usually find the correct port in the Arduino IDE.

## Usage

1.  **Scan the Cube:**

    *   Run the main script to start the scanning process:

    ```bash
    python src/main.py
    ```

    *   The `scan_cube.py` script will guide you through scanning each face of the Rubik's Cube. Follow the on-screen prompts.
    *   The scanned state will be saved in [`src/scanned_state.json`](https://github.com/cipri7/Rubik-Robot-Solver/blob/main/src/scanned_state.json).

2.  **Visualize and Solve:**

    *   After scanning, the `visualize_cube.py` script will open a window displaying the scanned cube.
    *   You can manually correct any misidentified colors by clicking on the tiles and selecting the correct color.
    *   Press `C` to confirm the cube state. This will print the Kociemba string representation of the cube to the console.
    *   Press `S` to solve the cube. This will calculate the solution using the `kociemba` library and send the solution to the Arduino.

## Troubleshooting

*   **Webcam Issues:** If the webcam is not detected, ensure it is properly connected and that no other applications are using it.  You may need to adjust the `camera_id` in [`src/cube_scanner.py`](https://github.com/cipri7/Rubik-Robot-Solver/blob/main/src/cube_scanner.py).
*   **Color Calibration:** If the colors are not being recognized correctly, recalibrate the color detection using the `scan_cube.py` script. Ensure good lighting conditions during calibration.
*   **Serial Communication:** If the solution is not being sent to the Arduino, double-check the `ARDUINO_PORT` in [`src/visualize_cube.py`](https://github.com/cipri7/Rubik-Robot-Solver/blob/main/src/visualize_cube.py) and ensure the Arduino is properly connected and running the appropriate firmware.

## Code Structure

*   [`src/main.py`](https://github.com/cipri7/Rubik-Robot-Solver/blob/main/src/main.py): Main entry point of the application.
*   [`src/scan_cube.py`](https://github.com/cipri7/Rubik-Robot-Solver/blob/main/src/scan_cube.py): Handles cube scanning and color calibration.
*   [`src/cube_scanner.py`](https://github.com/cipri7/Rubik-Robot-Solver/blob/main/src/cube_scanner.py): Contains the `CubeScanner` class for capturing cube faces.
*   [`src/color_classifier.py`](https://github.com/cipri7/Rubik-Robot-Solver/blob/main/src/color_classifier.py): Contains the `ColorClassifier` class for identifying colors.
*   [`src/visualize_cube.py`](https://github.com/cipri7/Rubik-Robot-Solver/blob/main/src/visualize_cube.py): Visualizes the scanned cube and sends the solution to the Arduino.
*   [`src/motor_controller.py`](https://github.com/cipri7/Rubik-Robot-Solver/blob/main/src/motor_controller.py): Manages serial communication with the Arduino.
*   [`src/calibration.json`](https://github.com/cipri7/Rubik-Robot-Solver/blob/main/src/calibration.json): Stores color calibration data.
*   [`src/scanned_state.json`](https://github.com/cipri7/Rubik-Robot-Solver/blob/main/src/scanned_state.json): Stores the scanned state of the cube.

## Credits

This project utilizes the kociemba library for solving the Rubik's Cube.



