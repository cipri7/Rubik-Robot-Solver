# From main.py
import subprocess
import cv2
from scan_cube import run_scanner

def main():
    print("=== Rubik Cube Solver App ===")

    # Step 1: Scan the cube
    run_scanner()

    # Step 2: Launch the visualizer for confirmation/modification
    subprocess.run(["python", "visualize_cube.py"])

    print("Done. Cube should now be solved if [S] was pressed in visualizer.")

if __name__ == "__main__":
    main()
