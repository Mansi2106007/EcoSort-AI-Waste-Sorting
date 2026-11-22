# EcoSort AI — Waste Sorting & Recycling Quality Controller

**EcoSort AI** is a deep-learning-based waste inspection and recycling quality-control system designed for the **Circular Economy** domain.

The system analyzes waste images, detects and segments individual waste objects, identifies their material type, estimates recycling-stream purity, detects contamination, and provides an operator-oriented quality recommendation.

---

## Problem Statement

Recycling streams can become contaminated when waste made from the wrong material enters a sorting line. Continuous manual inspection of conveyor-belt waste is difficult, especially when objects overlap, vary in appearance, or belong to visually similar categories.

EcoSort AI provides an AI-assisted inspection pipeline that can:

- Detect individual waste objects
- Segment object regions
- Identify waste categories
- Map objects to material groups
- Detect recycling-stream contamination
- Estimate stream purity
- Provide a quality score and operator recommendation

---

## System Workflow

```text
Waste Image
     ↓
YOLO Object Detection
     ↓
Instance Segmentation
     ↓
Waste Category Identification
     ↓
Material Mapping
(Plastic / Paper / Metal / Other)
     ↓
Expected Stream Comparison
     ↓
Purity & Contamination Analysis
     ↓
Quality Score + Risk Level
     ↓
Operator Recommendation
```

---

## Deep Learning Components

### YOLO Object Detection

A trained YOLO model detects waste objects and predicts their waste categories.

### Instance Segmentation

A YOLO segmentation model estimates the pixel-level region occupied by individual waste objects.

### Material Intelligence

The detected waste categories are mapped into four practical recycling groups:

- Plastic
- Paper
- Metal
- Other

### Recycling Quality Controller

Detected materials are compared with the selected recycling stream to calculate purity and identify contaminants.

The application produces:

- Quality Score
- Stream Purity
- Contamination Risk
- Detected Object Count
- Material Composition
- Contaminant Details
- Operator Recommendation

### LSTM Stream Monitoring

An experimental LSTM module analyzes sequential material-composition information to study changes in a recycling stream over time.

### VAE Rare-Waste Analysis

A convolutional Variational Autoencoder (VAE) was explored for representation learning and generation of rare waste-category samples.

---

## Dataset

The project uses **PackWISE v2 — Packaging Waste Instance Segmentation Dataset for Model Training and Evaluation**.

### Dataset Summary

| Property | Value |
|---|---:|
| Total Images | 586 |
| Waste Classes | 23 |
| Training Images | 410 |
| Validation Images | 88 |
| Test Images | 88 |
| Annotation Format | COCO |
| Annotation Types | Bounding Boxes + Instance Masks |
| Native Image Resolution | 4096 × 4096 |

The dataset was converted from COCO annotations to formats suitable for YOLO detection and segmentation.

Exact duplicate and cross-split leakage checks were also performed.

**Cross-split exact image leakage detected: 0**

---

## Final Detection Results

The final object detector was evaluated on the unseen PackWISE test set.

| Metric | Result |
|---|---:|
| Precision | 38.93% |
| Recall | 36.47% |
| mAP@50 | 31.32% |
| mAP@50–95 | 26.40% |
| Matched Detection Macro-F1 | 0.3767 |

---

## Segmentation and Runtime Evaluation

| Metric | Result |
|---|---:|
| Sampled Segmentation Mean IoU | 0.374 |
| Inference Latency | 121.97 ms/image |
| Inference Speed | 8.20 FPS |
| Peak GPU Memory | 133.94 MB |
| Automated Tests | 7/7 Passed |

---

## Robustness Testing

| Test Condition | Result |
|---|---|
| Dark Images | Robust |
| Bright Images | Robust |
| Blurred Images | Robust |
| Strong Image Noise | Failure Observed |

Strong image noise remains an important limitation of the current prototype.

---

## Model Comparison

The project considered multiple deep-learning architectures and detection approaches, including:

- YOLO
- Faster R-CNN
- RetinaNet
- ResNet
- GoogLeNet
- R-CNN / Fast R-CNN concepts

YOLO was retained as the primary detection model because it provides efficient single-stage detection and was trained directly on the PackWISE dataset for the final EcoSort AI pipeline.

---

## Deep Learning Fundamentals

The project also contains controlled experiments demonstrating:

- Tensor operations and reshaping
- Broadcasting
- Inner products
- Singular Value Decomposition (SVD)
- Numerical gradient checking
- McCulloch-Pitts neurons
- Sigmoid neurons
- Multilayer perceptrons
- Forward propagation
- Backpropagation
- Parameter vs hyperparameter tracking
- Batch Gradient Descent
- Stochastic Gradient Descent
- Momentum
- Nesterov optimization
- Initialization methods
- Normalization
- Regularization
- Data augmentation
- Overfitting and generalization
- Hebbian learning
- Modified Hebbian learning
- Competitive learning
- Error-correction learning
- Energy/Boltzmann learning
- Step, Sigmoid and Tanh activation comparison
- 2D and 3D convolution demonstrations

---

## EcoSort AI Application

The final application provides an interactive interface where a user can:

1. Upload a waste image or select a provided test sample.
2. Select the expected recycling stream.
3. Configure the detection confidence threshold.
4. Run AI-based waste inspection.
5. View detection and segmentation results.
6. Inspect material composition.
7. Check recycling-stream purity.
8. Identify contaminants.
9. Receive a quality score and contamination-risk level.
10. Receive an operator recommendation.

---

## Project Structure

```text
EcoSort-AI-Waste-Sorting/
│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── inference.py
│   └── quality_controller.py
│
├── models/
│   ├── detection.pt
│   ├── segmentation.pt
│   ├── lstm.pth
│   └── vae.pth
│
├── demo_samples/
│   ├── sample_01.jpg
│   ├── ...
│   └── sample_12.jpg
│
└── notebooks/
    └── Waste_Sorting_PBL_Final.ipynb
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Mansi2106007/EcoSort-AI-Waste-Sorting.git
cd EcoSort-AI-Waste-Sorting
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## Reproducibility

The recorded reproducibility environment used:

- Random Seed: **42**
- Python: **3.13.16**
- PyTorch: **2.14.1+cu130**
- Ultralytics: **8.4.216**
- CUDA: **Available**
- GPU: **Tesla T4**

The reproducibility check confirmed the availability of:

- Dataset
- Test set
- Detection model
- Segmentation model
- Final application

**Reproducibility Status: PASS**

---

## Known Limitations

The current prototype has several limitations:

- The dataset contains only 586 images across 23 classes.
- Some classes contain relatively few training examples.
- Detection performance on unseen data is moderate.
- Segmentation quality varies across objects.
- Strong image noise can cause detection failure.
- Recycling purity is currently estimated using detected object counts rather than physical mass.
- LSTM and VAE modules are experimental extensions rather than autonomous production controllers.
- Real recycling-facility deployment would require larger-scale validation.

---

## Deployment Recommendation

### GO

For:

- Academic demonstration
- Deep-learning experimentation
- Controlled recycling-quality analysis
- Research prototyping

### NO-GO

For:

- Fully autonomous industrial waste sorting
- Safety-critical recycling decisions
- Unsupervised production deployment

Further dataset expansion, robustness improvement, model optimization and real facility testing are required before production deployment.

---

## Responsible Use

EcoSort AI is designed as an **operator decision-support prototype**.

Its predictions should not be treated as guaranteed physical, chemical, regulatory or safety assessments. Human verification is recommended for uncertain or high-risk outputs.

---

## AI Assistance Disclosure

AI tools were used as supporting tools during development for activities such as code guidance, debugging, explanation and documentation.

All project code and outputs were executed, tested and reviewed using the actual project dataset and experimental results. AI-generated suggestions were verified and modified according to the project requirements.

---

## Project Status

**Academic Prototype: Complete**

**Production Readiness: Further validation required**

---

**EcoSort AI**  
*Waste Intelligence. Better Recycling Decisions.*

