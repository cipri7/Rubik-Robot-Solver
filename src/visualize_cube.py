# From visualize_cube.py
import pygame
import json
import time
import serial #delete
import kociemba
from motor_controller import MotorController  # Import the new class

# === Configuration ===
JSON_PATH = "scanned_state.json"
ARDUINO_PORT = "/dev/cu.usbmodem1101"  # Update as needed
BAUD_RATE = 115200
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

# === Color Mappings ===
COLOR_MAP = {
    'W': (255, 255, 255),
    'Y': (255, 255, 0),
    'R': (255, 0, 0),
    'O': (255, 165, 0),
    'G': (0, 255, 0),
    'B': (0, 0, 255),
    'X': (100, 100, 100)
}

COLORS = list(COLOR_MAP.keys())[:-1]  # Exclude 'X'
current_color = 'W'

# === Load scanned state ===
with open(JSON_PATH, 'r') as f:
    faces = json.load(f)

# === Convert scanned state to Kociemba format string ===
def scanned_state_to_kociemba(faces):
    face_order = ['U', 'R', 'F', 'D', 'L', 'B']
    color_to_facelet = {
        'W': 'U',
        'R': 'R',
        'G': 'F',
        'Y': 'D',
        'O': 'L',
        'B': 'B'
    }
    kociemba_string = ''
    for face in face_order:
        for color in faces[face]:
            kociemba_string += color_to_facelet.get(color, 'X')  # 'X' as fallback for invalid/missing colors
    return kociemba_string

def transform_solution(solution):
    solution = solution.replace("'", "3")  # Replace apostrophes with '3'
    solution = solution.replace(" ", "")   # Remove all spaces
    return solution

# === Draw face and detect tiles ===
def draw_face(screen, face_colors, start_x, start_y, face_key, tile_map):
    tile_size = 40
    gap = 2
    for i in range(3):
        for j in range(3):
            idx = i * 3 + j
            color = COLOR_MAP.get(face_colors[idx], COLOR_MAP['X'])
            rect = pygame.Rect(start_x + j * (tile_size + gap), start_y + i * (tile_size + gap), tile_size, tile_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            tile_map.append((rect, face_key, idx))

# === Draw color selector ===
def draw_color_selector(screen):
    tile_size = 30
    gap = 10
    selector_rects = []
    for i, col in enumerate(COLORS):
        rect = pygame.Rect(20 + i * (tile_size + gap), 60, tile_size, tile_size)
        pygame.draw.rect(screen, COLOR_MAP[col], rect)
        if col == current_color:
            pygame.draw.rect(screen, (0, 0, 0), rect, 3)
        else:
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
        selector_rects.append((rect, col))
    return selector_rects

# === Pygame Setup ===
def launch_visualizer():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Rubik's Cube Visualizer")
    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()
    running = True
    current_color = 'W'

    motor_controller = MotorController(ARDUINO_PORT, BAUD_RATE)
    if not motor_controller.connect():
        print("Could not connect to Arduino.  Solution sending disabled.")
        send_solution = False
    else:
        send_solution = True

    while running:
        tile_map = []

        screen.fill((200, 200, 200))

        draw_face(screen, faces['U'], 320, 80, 'U', tile_map)
        draw_face(screen, faces['L'], 200, 200, 'L', tile_map)
        draw_face(screen, faces['F'], 320, 200, 'F', tile_map)
        draw_face(screen, faces['R'], 440, 200, 'R', tile_map)
        draw_face(screen, faces['B'], 560, 200, 'B', tile_map)
        draw_face(screen, faces['D'], 320, 320, 'D', tile_map)
        selector_rects = draw_color_selector(screen)

        text = font.render("[C] Confirm | [S] Send | Click to Edit", True, (0, 0, 0))
        screen.blit(text, (20, 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for rect, col in selector_rects:
                    if rect.collidepoint(mx, my):
                        current_color = col
                for rect, face_key, idx in tile_map:
                    if rect.collidepoint(mx, my):
                        faces[face_key][idx] = current_color
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    print("Cube confirmed.")
                    print("Kociemba string:", scanned_state_to_kociemba(faces))
                elif event.key == pygame.K_s and send_solution:
                    try:
                        kociemba_string = scanned_state_to_kociemba(faces)
                        solution = transform_solution(kociemba.solve(kociemba_string))
                        print("Solution:", solution)
                        motor_controller.send_solution(solution)
                    except Exception as e:
                        print("Error solving cube:", e)

        clock.tick(30)

    motor_controller.disconnect()
    pygame.quit()

if __name__ == "__main__":
    launch_visualizer()
