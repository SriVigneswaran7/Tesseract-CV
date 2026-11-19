# Tesseract-CV

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Vision-00979D)
![Solver](https://img.shields.io/badge/Solver-Kociemba-red)
![License](https://img.shields.io/badge/License-MIT-green)

Real-time computer vision 3x3 Rubik's Cube scanner and augmented-reality move coach built with Python and OpenCV. Designed to handle real-world room lighting via LAB-space normalization, dynamic HSV calibration, and live directional HUD overlays.

---

## Core Engineering Features

- **Lighting-Adaptive Preprocessing:** Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) strictly to the Luminance (`L`) channel in CIELAB color space, neutralizing shadows and uneven room lighting without distorting hue.
- **Glare-Resistant Sticker Sampling:** Computes median BGR/HSV values across a centered `24x24` pixel patch inside each cell of the 3x3 reticle, rejecting specular highlights on glossy stickerless speedcubes.
- **Parity-Safe Vision Feed:** Processes raw, unmirrored webcam frames to prevent left/right sticker inversion during state reconstruction.
- **Decoupled Architecture:** Strictly separates vision preprocessing, cube state math, and OpenCV HUD rendering so the optimal Kociemba solver can be swapped for a human-style CFOP engine without modifying the vision pipeline.

---

## Processing Pipeline

```mermaid
flowchart LR
    A[Webcam Frame] --> B[LAB-Space CLAHE]
    B --> C[3x3 ROI Median Sampling]
    C --> D[Dynamic HSV Classifier]
    D --> E[54-Sticker State Validator]
    E --> F[Kociemba / CFOP Engine]
    F --> G[Live AR Overlay & HUD]
```

---

## Project Structure

```text
Tesseract-CV/
├── main.py                     # Entry point & main vision loop
├── config.py                   # Camera settings, 3x3 grid geometry & HUD palette
├── requirements.txt            # Locked Python dependencies
├── src/
│   ├── vision/
│   │   ├── preprocessor.py     # LAB-space CLAHE & median patch sampling
│   │   ├── calibrator.py       # Dynamic 6-center HSV baseline capture
│   │   └── scanner.py          # Live sticker classification & face capture
│   ├── solver/
│   │   ├── cube_state.py       # 54-sticker validation & parity checks
│   │   └── engine.py           # Kociemba solver wrapper (CFOP-ready interface)
│   └── ui/
│       ├── hud.py              # 3x3 targeting reticle & live HSV telemetry
│       └── ar_overlay.py       # Directional AR turn arrows
├── data/                       # Runtime lighting profiles (gitignored)
├── assets/                     # Demo captures & visual assets
└── tests/
    └── test_solver.py          # Offline solver & state unit tests
```

---

## Quick Start

### 1. Clone & Set Up Environment
```bash
git clone [https://github.com/SriVigneswaran7/Tesseract-CV.git](https://github.com/SriVigneswaran7/Tesseract-CV.git)
cd Tesseract-CV

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Live Vision Pipeline
```bash
python main.py
```

> **macOS Note:** Grant Camera access to VS Code or Terminal when prompted. If macOS defaults to iPhone Continuity Camera, set `CAMERA_INDEX = 1` in `config.py`.

---

## Controls

| Key | Action |
| :--- | :--- |
| `C` | Toggle LAB-space CLAHE lighting normalization on/off |
| `Q` / `Esc` | Release webcam and exit cleanly |

---

## Roadmap

- [x] **Milestone 1:** Live webcam pipeline, LAB-space CLAHE filter, median sticker sampling, and 3x3 targeting HUD with HSV diagnostics.
- [ ] **Milestone 2:** Dynamic 6-center room-lighting calibration (`calibration.json`) and full 6-face state scanner with live 2D unfolded cube net.
- [ ] **Milestone 3:** 54-sticker parity validation, Kociemba optimal move solver, and directional AR arrow overlays.
- [ ] **Milestone 4:** Custom CFOP coaching engine (Cross, F2L pair guidance, and 4-Look Last Layer).

---

## License

Distributed under the MIT License. See `LICENSE` for details.