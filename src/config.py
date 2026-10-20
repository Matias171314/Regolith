"""
Global Configuration for Regolith.
Windows, colors and physics parameters for the simulator.
"""

# --- Window Configuration ---
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
TITLE = "Regolith: Lunar Settlement Simulator"

# --- Color Palette (RGB) ---
COLOR_BG = (13, 17, 23)          # Background
COLOR_GRID = (48, 54, 61)        # Grid
COLOR_UI_TEXT = (230, 237, 243)  # Text
COLOR_ACCENT = (0, 212, 255)     # Indicators

# --- Pixel Size ---
TILE_SIZE = 64

# --- Interface ---
TOOLBAR_HEIGHT = 80
BOARD_HEIGHT = WINDOW_HEIGHT - TOOLBAR_HEIGHT
