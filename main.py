import cv2
import config
from src.vision.preprocessor import normalize_lighting, sample_grid_colors
from src.ui.hud import get_grid_centers, draw_scan_hud


def main() -> None:
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)

    if not cap.isOpened():
        raise RuntimeError(
            "Could not open webcam. Check macOS Privacy & Security -> Camera permissions "
            "for VS Code / Terminal, or try changing CAMERA_INDEX in config.py."
        )

    clahe_enabled = True

    while True:
        ok, frame = cap.read()
        if not ok:
            print("Failed to grab frame.")
            break

        processed_bgr = normalize_lighting(frame) if clahe_enabled else frame
        frame_hsv = cv2.cvtColor(processed_bgr, cv2.COLOR_BGR2HSV)

        h, w = processed_bgr.shape[:2]
        grid_centers = get_grid_centers(w, h)
        bgr_samples, hsv_samples = sample_grid_colors(
            processed_bgr, frame_hsv, grid_centers
        )

        display = draw_scan_hud(
            processed_bgr.copy(),
            grid_centers,
            bgr_samples,
            hsv_samples,
            clahe_enabled,
        )

        cv2.imshow(config.WINDOW_NAME, display)

        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27):  # q or ESC
            break
        elif key == ord("c"):
            clahe_enabled = not clahe_enabled

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()