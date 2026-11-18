import cv2
import numpy as np
import config


_clahe = cv2.createCLAHE(
    clipLimit=config.CLAHE_CLIP_LIMIT,
    tileGridSize=config.CLAHE_TILE_GRID_SIZE,
)


def normalize_lighting(frame_bgr: np.ndarray) -> np.ndarray:
    """Normalizes luminance using CLAHE in LAB space while preserving true colors."""
    lab = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)
    l_norm = _clahe.apply(l_channel)
    merged = cv2.merge((l_norm, a_channel, b_channel))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


def sample_grid_colors(
    frame_bgr: np.ndarray,
    frame_hsv: np.ndarray,
    grid_centers: list[tuple[int, int]],
) -> tuple[list[tuple[int, int, int]], list[tuple[int, int, int]]]:
    """Samples median BGR and HSV inside the center patch of each 3x3 cell."""
    r = config.SAMPLE_RADIUS
    h_img, w_img = frame_bgr.shape[:2]

    bgr_samples: list[tuple[int, int, int]] = []
    hsv_samples: list[tuple[int, int, int]] = []

    for cx, cy in grid_centers:
        y1, y2 = max(0, cy - r), min(h_img, cy + r)
        x1, x2 = max(0, cx - r), min(w_img, cx + r)

        patch_bgr = frame_bgr[y1:y2, x1:x2]
        patch_hsv = frame_hsv[y1:y2, x1:x2]

        # Median rejects bright white specular glare pixels far better than mean
        med_bgr = np.median(patch_bgr.reshape(-1, 3), axis=0)
        med_hsv = np.median(patch_hsv.reshape(-1, 3), axis=0)

        bgr_samples.append(tuple(int(v) for v in med_bgr))
        hsv_samples.append(tuple(int(v) for v in med_hsv))

    return bgr_samples, hsv_samples