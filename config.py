# Camera configuration
CAMERA_INDEX = 0  # If macOS grabs your iPhone (Continuity Camera), change this to 1
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
WINDOW_NAME = "Tesseract-CV // Live Vision"

# 3x3 Scanning Grid (pixels)
GRID_CELL_SIZE = 75
GRID_GAP = 14
SAMPLE_RADIUS = 12  # Samples a 24x24 patch dead-center inside each sticker

# CLAHE (Lighting Normalization)
CLAHE_CLIP_LIMIT = 2.0
CLAHE_TILE_GRID_SIZE = (8, 8)

# Tactical HUD Palette (BGR format for OpenCV)
COLOR_BG_BAR = (20, 20, 24)
COLOR_ACCENT = (255, 210, 0)    # Electric cyan
COLOR_WHITE = (240, 240, 240)
COLOR_MUTED = (140, 140, 150)
COLOR_SUCCESS = (100, 230, 100)
COLOR_WARN = (60, 165, 255)