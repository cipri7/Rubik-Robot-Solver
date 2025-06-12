# From scan_cube.py
import json
import time
import cv2
import numpy as np
from color_classifier import ColorClassifier
from cube_scanner import CubeScanner
import os

CALIBRATION_FILE = "calibration.json"

def wait_for_calibration_key():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

    print("\nPress 'c' to calibrate colors or any other key to continue with saved calibration.")
    print("Press ESC to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        cv2.putText(frame, "Press 'C' to calibrate or 'any key' to skip", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Calibration Prompt", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            cap.release()
            cv2.destroyAllWindows()
            return True
        elif key != 255:
            cap.release()
            cv2.destroyAllWindows()
            return False


def calibrate_colors(classifier):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

    print("\n=== Color Calibration ===")
    print("You will be prompted to show each face (W, R, G, Y, O, B).")
    print("Center the face and press SPACE to capture its center sticker.\n")

    color_order = ['W', 'R', 'G', 'Y', 'O', 'B']
    center_coord = (0, 0)  # only sample the center

    for color_label in color_order:
        print(f"Show the {color_label} face (centered) and press SPACE to capture.")

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            h, w, _ = frame.shape
            cx, cy = w // 2, h // 2

            # Draw a center square
            x, y = cx + center_coord[0], cy + center_coord[1]
            cv2.rectangle(frame, (x-20, y-20), (x+20, y+20), (255, 255, 255), 2)
            cv2.putText(frame, f"{color_label} face", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Calibration", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                cap.release()
                cv2.destroyAllWindows()
                return False
            elif key == 32:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                pixel = hsv[cy + center_coord[1], cx + center_coord[0]]
                classifier.ref_colors[color_label] = pixel.astype(np.float32)
                print(f"  {color_label} HSV: {pixel}")
                break

    cap.release()
    cv2.destroyAllWindows()
    print("\nCalibration complete.")
    classifier.save_calibration()
    return True



def run_scanner():
    print("Rubik's Cube Face Scanner")
    classifier = ColorClassifier(CALIBRATION_FILE)
    should_calibrate = wait_for_calibration_key()

    if should_calibrate or not classifier.load_calibration():
        if not calibrate_colors(classifier):
            print("Calibration cancelled. Exiting.")
            return None

    with CubeScanner(classifier) as scanner:
        cube_faces = scanner.scan_cube()
        cube_str = scanner.build_cube_string(cube_faces)

    print("Cube string:", cube_str)

    with open("scanned_state.json", "w") as f:
        json.dump(cube_faces, f)

    cv2.destroyAllWindows()
    cv2.waitKey(1)
    time.sleep(1)
    return cube_str


if __name__ == "__main__":
    run_scanner()
