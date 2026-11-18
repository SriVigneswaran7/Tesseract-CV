import cv2
import numpy as np
import config


def get_grid_centers(frame_width: int, frame_height: int) -> list[tuple[int, int]]:
    """Returns 9 (cx, cy) centers in row-major order (top-left to bottom-right)."""
    center_x = frame_width // 2
    center_y = frame_height // 2
    step = config.GRID_CELL_SIZE + config.GRID_GAP

    centers: list[tuple[int, int]] = []
    for row in (-1, 0, 1):
        for col in (-1, 0, 1):
            centers.append((center_x + col * step, center_y + row * step))
    return centers


def draw_scan_hud(
    frame: np.ndarray,
    grid_centers: list[tuple[int, int]],
    bgr_samples: list[tuple[int, int, int]],
    hsv_samples: list[tuple[int, int, int]],
    clahe_enabled: bool,
) -> np.ndarray:
    """Draws the tactical 3x3 targeting reticle and live HSV diagnostics."""
    h, w = frame.shape[:2]
    half = config.GRID_CELL_SIZE // 2
    r = config.SAMPLE_RADIUS

    # Semi-transparent top and bottom HUD bars
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 52), config.COLOR_BG_BAR, -1)
    cv2.rectangle(overlay, (0, h - 52), (w, h), config.COLOR_BG_BAR, -1)
    cv2.addWeighted(overlay, 0.78, frame, 0.22, 0, frame)

    # Top bar: title + CLAHE status
    cv2.putText(
        frame,
        "TESSERACT-CV // VISION PIPELINE",
        (20, 33),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        config.COLOR_ACCENT,
        2,
        cv2.LINE_AA,
    )
    clahe_label = "CLAHE: ON" if clahe_enabled else "CLAHE: OFF"
    clahe_color = config.COLOR_SUCCESS if clahe_enabled else config.COLOR_WARN
    cv2.putText(
        frame,
        clahe_label,
        (w - 150, 33),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        clahe_color,
        2,
        cv2.LINE_AA,
    )

    # 3x3 Grid cells + center sample zone + live color swatch
    for idx, (cx, cy) in enumerate(grid_centers):
        x1, y1 = cx - half, cy - half
        x2, y2 = cx + half, cy + half

        border_color = config.COLOR_ACCENT if idx == 4 else config.COLOR_WHITE
        thickness = 2 if idx == 4 else 1

        # Outer sticker box
        cv2.rectangle(frame, (x1, y1), (x2, y2), border_color, thickness)

        # Inner sample target (where the camera actually reads color)
        cv2.rectangle(frame, (cx - r, cy - r), (cx + r, cy + r), border_color, 1)

        # Live sampled color preview swatch in top-left corner of each cell
        swatch_bgr = bgr_samples[idx]
        cv2.rectangle(frame, (x1 + 4, y1 + 4), (x1 + 20, y1 + 20), swatch_bgr, -1)
        cv2.rectangle(frame, (x1 + 4, y1 + 4), (x1 + 20, y1 + 20), config.COLOR_BG_BAR, 1)

    # Bottom bar: center sticker live HSV readout + controls
    center_hsv = hsv_samples[4]
    cv2.putText(
        frame,
        f"CENTER HSV: H={center_hsv[0]:3d}  S={center_hsv[1]:3d}  V={center_hsv[2]:3d}",
        (20, h - 18),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        config.COLOR_WHITE,
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "[C] Toggle CLAHE   |   [Q] Quit",
        (w - 340, h - 18),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        config.COLOR_MUTED,
        1,
        cv2.LINE_AA,
    )

    return frame