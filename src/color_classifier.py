# From color_classifier.py
import numpy as np
import cv2
import json
import os

class ColorClassifier:
    def __init__(self, calibration_file="calibration.json"):
        self.ref_colors = {}  # HSV reference color values for each sticker color
        self.calibration_file = calibration_file
        self.load_calibration()

    def calibrate(self, frame, coords, label_order):
        """Extracts HSV color values from specific locations in a frame and stores them as references."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, w, _ = frame.shape
        cx, cy = w // 2, h // 2

        for label, (dx, dy) in zip(label_order, coords):
            pixel = hsv[cy + dy, cx + dx]
            self.ref_colors[label] = pixel.astype(np.float32)

        print("Calibration complete. Reference HSV values:")
        for color, hsv_val in self.ref_colors.items():
            print(f"  {color}: {hsv_val}")
        self.save_calibration()

    def classify(self, hsv_pixel):
        """Find the closest reference color in HSV space."""
        min_dist = float('inf')
        best_color = 'U'
        for color, ref in self.ref_colors.items():
            dist = np.linalg.norm(hsv_pixel.astype(np.float32) - ref)
            if dist < min_dist:
                min_dist = dist
                best_color = color
        return best_color

    def color2bgr(self, color):
        """Maps cube color codes to BGR colors for drawing."""
        mapping = {
            'R': (0, 0, 255),
            'O': (0, 100, 255),
            'Y': (0, 255, 255),
            'G': (0, 210, 100),
            'B': (219, 70, 29),
            'W': (255, 255, 255),
            'U': (0, 0, 0)
        }
        return mapping.get(color, (0, 0, 0))

    def save_calibration(self):
        """Saves the calibration data to a JSON file."""
        ref_serialized = {k: v.tolist() for k, v in self.ref_colors.items()}
        with open(self.calibration_file, "w") as f:
            json.dump(ref_serialized, f)
        print("Calibration data saved.")

    def load_calibration(self):
        """Loads the calibration data from a JSON file."""
        if os.path.exists(self.calibration_file):
            with open(self.calibration_file, "r") as f:
                data = json.load(f)
                self.ref_colors = {k: np.array(v, dtype=np.float32) for k, v in data.items()}
            print("Loaded saved calibration data.")
            return True
        print("No saved calibration found.")
        return False
