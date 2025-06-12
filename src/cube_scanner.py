# From cube_scanner.py
import cv2
import numpy as np
from color_classifier import ColorClassifier

class CubeScanner:
    def __init__(self, classifier, camera_id=0, width=640, height=640):
        self.classifier = classifier
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.cap = None  # Initialize cap to None
        self.face_order = ['U', 'R', 'F', 'D', 'L', 'B']
        self.cube_faces = {face: ["X"] * 9 for face in self.face_order}
        self.coords = [
            (-80, -80), (  0, -80), ( 80, -80),
            (-80,   0), (  0,   0), ( 80,   0),
            (-80,  80), (  0,  80), ( 80,  80),
        ]

    def __enter__(self):
         self.cap = cv2.VideoCapture(self.camera_id)
         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
         if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
         return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()

    def _draw_cube_preview(self, frame):
        size = 24
        gap = 2

        # Centru mai sigur pentru întregul preview
        center_x = frame.shape[1] - 160
        center_y = frame.shape[0] - 160

        face_pos = {
            'U': (center_x,         center_y - (size + gap) * 3),
            'L': (center_x - (size + gap) * 3, center_y),
            'F': (center_x,         center_y),
            'R': (center_x + (size + gap) * 3, center_y),
            'B': (center_x + (size + gap) * 6, center_y),  # mai apropiat
            'D': (center_x,         center_y + (size + gap) * 3),
        }

        for face, face_colors in self.cube_faces.items():
            if face not in face_pos:
                continue
            fx, fy = face_pos[face]
            for i in range(9):
                row, col = divmod(i, 3)
                color = face_colors[i] if face_colors[i] != "X" else "U"
                bgr = self.classifier.color2bgr(color)
                x = fx + col * (size + gap)
                y = fy + row * (size + gap)
                cv2.rectangle(frame, (x, y), (x + size, y + size), bgr, -1)
                cv2.rectangle(frame, (x, y), (x + size, y + size), (0, 0, 0), 1)


    def capture_face(self, color_label):
        """Captures a single face of the Rubik's Cube."""

        print(f"Position {color_label} face in view and press SPACE to capture.")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame from camera.")
                break

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            h, w, _ = frame.shape
            cx, cy = w // 2, h // 2

            colors = []
            for dx, dy in self.coords:
                pixel = hsv[cy + dy, cx + dx]
                color = self.classifier.classify(pixel)
                colors.append(color)

            for i, (dx, dy) in enumerate(self.coords):
                x, y = cx + dx, cy + dy
                bgr_color = self.classifier.color2bgr(colors[i])
                cv2.rectangle(frame, (x-20, y-20), (x+20, y+20), bgr_color, -1)
                cv2.putText(frame, colors[i], (x-10, y+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)

            cv2.rectangle(frame, (cx - 120, cy - 120), (cx + 120, cy + 120), (255, 255, 255), 1)
            cv2.putText(frame, f"{color_label} FACE", (cx - 100, cy - 130), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

            self._draw_cube_preview(frame)
            cv2.imshow("Cube Scanner", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break
            elif key == 32:
                print(f"{color_label} face captured: {colors}")
                self.cube_faces[color_label] = colors
                return colors

        return []

    def scan_cube(self):
        """Scans all faces of the Rubik's Cube."""
        print("\nScan the cube faces in this order: U, R, F, D, L, B")
        for label in self.face_order:
            self.cube_faces[label] = self.capture_face(label)
        return self.cube_faces

    def build_cube_string(self, facelets):
        """Converts the scanned faces to a cube string representation."""
        color_map = {
            'W': 'U', 'R': 'R', 'G': 'F', 'Y': 'D', 'O': 'L', 'B': 'B'
        }
        order = ['U', 'R', 'F', 'D', 'L', 'B']
        full_string = ''
        for face in order:
            for color in facelets[face]:
                full_string += color_map.get(color, 'U')
        return full_string

