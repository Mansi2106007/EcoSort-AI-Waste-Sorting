
# ♻️ EcoSort AI — Waste Sorting & Recycling Quality Controller

EcoSort AI is a deep-learning-based application for automated waste inspection in recycling environments.

## Features

- Waste object detection using YOLO
- Instance segmentation of waste objects
- Material classification into Plastic, Paper, Metal and Other
- Recycling contamination detection
- Recycling stream purity estimation
- LSTM-based waste stream monitoring experiment
- VAE-based rare waste category analysis
- Interactive Streamlit dashboard

## Dataset

The project uses the PackWISE waste dataset containing conveyor-belt waste images with object annotations and segmentation masks.

## Final Object Detection Test Results

| Metric | Result |
|---|---:|
| Precision | 38.93% |
| Recall | 36.47% |
| mAP@50 | 31.32% |
| mAP@50-95 | 26.40% |

## Project Structure

```text
EcoSort-AI-Waste-Sorting/
├── app.py
├── requirements.txt
├── models/
│   ├── detection.pt
│   ├── segmentation.pt
│   ├── lstm.pth
│   └── vae.pth
└── src/
    ├── inference.py
    └── quality_controller.py
