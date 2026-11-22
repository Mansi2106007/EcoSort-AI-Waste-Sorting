![Uploading image.png…]()

# EcoSort AI
## Intelligent Waste Inspection & Recycling Stream Quality Control

**EcoSort AI** is a deep-learning prototype built to inspect packaging waste and evaluate the quality of recycling streams.

Instead of stopping at *“What type of waste is this?”*, EcoSort AI asks a second question:

> **“Does this waste actually belong in the recycling stream it is entering?”**

The system combines object detection, instance segmentation and material-level reasoning to identify waste objects, group them by material, detect contaminants, estimate stream purity and generate an operator-oriented decision.

---

## The Problem

A recycling line may be intended for a particular material such as **plastic**, but real waste streams are rarely perfectly clean.

For example, a plastic stream may contain:

- plastic film
- plastic bottles
- tissue
- metal lids
- paper packaging

Detecting an object alone does not tell an operator whether the overall stream is suitable for further processing.

EcoSort AI therefore treats waste inspection as a **recycling quality-control problem**.

Given a waste image and an expected material stream, the system attempts to determine:

1. What objects are present?
2. Where are they located?
3. What material does each detected category represent?
4. Which objects belong to the expected stream?
5. Which objects are contaminants?
6. How pure is the stream?
7. Should the stream be accepted, inspected or re-sorted?

---

# How EcoSort AI Works

```text
                    Waste Image
                         │
                         ▼
               ┌──────────────────┐
               │  YOLO Detection  │
               └────────┬─────────┘
                        │
                        ▼
             ┌──────────────────────┐
             │ Instance Segmentation│
             └──────────┬───────────┘
                        │
                        ▼
              Waste Category Labels
                        │
                        ▼
           ┌─────────────────────────┐
           │ Material Mapping Engine │
           │ Plastic / Paper / Metal │
           │          / Other        │
           └────────────┬────────────┘
                        │
                        ▼
             Expected Stream Check
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
           Accepted           Contaminant
            Objects             Objects
              └─────────┬─────────┘
                        ▼
               Stream Purity (%)
                        │
                        ▼
          Quality Score + Risk Level
                        │
                        ▼
             Operator Recommendation
```

The final output is therefore not only a set of bounding boxes. It is a **recycling-stream assessment**.

---

# What the System Reports

For every inspection, EcoSort AI can present:

| Output | Purpose |
|---|---|
| Detected waste objects | Identifies objects visible in the image |
| Instance segmentation | Shows estimated object regions |
| Waste category | Predicts the PackWISE category |
| Material group | Maps the category to Plastic, Paper, Metal or Other |
| Contaminants | Highlights materials inconsistent with the selected stream |
| Stream purity | Estimates the proportion of accepted detected objects |
| Quality score | Converts purity into an interpretable score |
| Contamination risk | LOW / MODERATE / HIGH |
| Operator recommendation | ACCEPT / MANUAL INSPECTION / RE-SORT |

---

# Deep Learning Pipeline

## 1. Waste Object Detection

The primary detector is a trained **YOLO-based object detection model**.

It receives a waste image and predicts:

- bounding boxes
- waste classes
- confidence scores

YOLO was selected as the final detector because its single-stage architecture provides a practical balance between detection capability and inference efficiency for an interactive prototype.

---

## 2. Instance Segmentation

Object detection identifies *where an object approximately exists*.

Instance segmentation goes further by estimating the **pixel-level region belonging to individual waste objects**.

EcoSort AI uses a YOLO segmentation model to provide this additional visual evidence.

---

## 3. Material Mapping

PackWISE contains detailed waste categories, while a recycling operator may care primarily about the material stream.

EcoSort AI therefore maps predicted categories into:

**Plastic | Paper | Metal | Other**

This mapping is an **EcoSort project layer** and is not presented as an original PackWISE annotation.

---

## 4. Recycling Quality Intelligence

Suppose the operator selects:

> **Expected Stream = PLASTIC**

and the system detects:

```text
plastic-foil/bag   → Plastic   ✓
plastic-bottle     → Plastic   ✓
tissue             → Paper     ✗
metal-lid          → Metal     ✗
```

EcoSort identifies the paper and metal objects as contaminants.

For the current prototype, purity is based on detected-object counts:

```text
Purity =
Accepted detected objects
───────────────────────── × 100
Total detected objects
```

This result is then translated into a quality score, risk level and operator recommendation.

---

# Advanced Deep Learning Experiments

The main application is supported by additional experiments required to study broader deep-learning concepts.

## LSTM Stream Monitor

Waste composition can also be viewed as a sequence rather than a collection of independent images.

An experimental **LSTM** was therefore developed using sequential material-composition vectors.

The module explores whether recent observations of:

```text
Plastic | Paper | Metal | Other
```

can provide information about the next stream composition.

The LSTM remains an **experimental temporal-analysis component** and is not used as an autonomous conveyor controller.

---

## Variational Autoencoder for Rare Waste

Some PackWISE categories contain substantially fewer examples than common categories.

A convolutional **Variational Autoencoder (VAE)** was explored for rare-category representation learning.

The experiment includes:

- image reconstruction
- latent representations
- generated samples
- latent-space visualization

The VAE is treated as a research experiment for representation learning and potential future augmentation rather than as the live EcoSort decision engine.

---

# PackWISE Dataset

EcoSort AI uses **PackWISE v2 — Packaging Waste Instance Segmentation Dataset for Model Training and Evaluation**.

PackWISE contains packaging-waste imagery collected in a realistic waste-sorting context and provides both object-level and pixel-level annotations.

### Dataset Profile

| Item | Value |
|---|---:|
| Images | **586** |
| Waste categories | **23** |
| Training images | **410** |
| Validation images | **88** |
| Test images | **88** |
| Native resolution | **4096 × 4096** |
| Annotation format | **COCO** |
| Annotation information | **Bounding boxes + instance masks** |

### Project Annotation Counts

| Split | Images | Annotations |
|---|---:|---:|
| Train | 410 | 4,669 |
| Validation | 88 | 990 |
| Test | 88 | 1,054 |

---

## Dataset Source & License

**Dataset:** PackWISE: Packaging Waste Instance Segmentation Dataset for Model Training and Evaluation  
**Publishers:** Fraunhofer IOSB and Fraunhofer IIS  
**Repository:** Fordatis  
**Version:** PackWISE v2  
**DOI:** `10.24406/fordatis/420.2`  
**License:** Creative Commons Attribution 4.0 International (**CC BY 4.0**)

PackWISE attribution should be retained when the dataset or derived work is redistributed as required by its license.

---

# Data Preparation

The original annotations are provided in COCO format.

For EcoSort AI:

- COCO bounding boxes were converted into YOLO detection labels.
- COCO instance masks were converted for YOLO segmentation.
- Images were resized by the training pipeline to the configured model input resolution.
- Training augmentation was applied during model development.
- Train, validation and test partitions were kept separate.
- The unseen test partition was reserved for final evaluation.

---

# Leakage Verification

Exact-image leakage can make evaluation results appear better than they really are.

EcoSort therefore performed a **SHA-256 exact duplicate check**.

| Check | Duplicate Images |
|---|---:|
| Within Train | 0 duplicate groups |
| Within Validation | 0 duplicate groups |
| Within Test | 0 duplicate groups |
| Train ↔ Validation | **0** |
| Train ↔ Test | **0** |
| Validation ↔ Test | **0** |

**Leakage Check: PASS**

No exact cross-split image leakage was detected.

---

# Detection Performance

The final detector was evaluated using the unseen PackWISE test partition.

| Metric | Final Result |
|---|---:|
| Precision | **38.93%** |
| Recall | **36.47%** |
| mAP@50 | **31.32%** |
| mAP@50-95 | **26.40%** |
| Matched Detection Macro-F1 | **0.3767** |

These values are reported as measured results rather than being presented as production-level performance.

---

# Segmentation & Runtime Evidence

| Measurement | Result |
|---|---:|
| Sampled segmentation mean IoU | **0.374** |
| Inference latency | **121.97 ms/image** |
| Throughput | **8.20 FPS** |
| Peak GPU memory | **133.94 MB** |
| Automated engineering checks | **7 / 7 PASS** |

The IoU value represents the project's **sampled segmentation evaluation**, not a claim of full-dataset segmentation performance.

---

# Robustness & Failure Analysis

A model should also be evaluated when input quality changes.

The detector was tested under several visual transformations.

| Input Condition | Observation |
|---|---|
| Original | Baseline detections retained |
| Darkened | Detections retained |
| Brightened | Detections retained |
| Blurred | Detections retained |
| Strong additive noise | **Detection failure observed** |

This experiment identified strong image noise as a concrete weakness of the current model.

The failure is intentionally documented instead of being hidden.

---

# Architecture Exploration

EcoSort AI was developed alongside comparisons and demonstrations involving several important deep-learning architectures.

### Detection architectures considered

- YOLO
- Faster R-CNN
- RetinaNet
- R-CNN concepts
- Fast R-CNN concepts

### CNN architectures explored

- ResNet
- GoogLeNet

YOLO was retained as the final project detector.

Faster R-CNN and RetinaNet were used as architecture-level candidate comparisons; their parameter counts should not be interpreted as PackWISE performance results unless separately trained and evaluated.

---

# Neural Network Fundamentals

The project notebook also contains controlled implementations and demonstrations of core deep-learning concepts.

### Tensor Mathematics

- tensor operations
- reshaping
- broadcasting
- inner products
- matrix operations
- singular value decomposition
- numerical gradient checking

### Neural Networks

- McCulloch-Pitts neuron
- sigmoid neuron
- multilayer perceptron
- forward propagation
- loss computation
- backpropagation
- parameter vs hyperparameter tracking

### Optimization

- Batch Gradient Descent
- Stochastic Gradient Descent
- Momentum
- Nesterov optimization

### Training Behaviour

- initialization
- normalization
- regularization
- augmentation
- overfitting
- generalization

### Learning Rules

- Hebbian learning
- modified Hebbian learning
- competitive learning
- error-correction learning
- compact energy/Boltzmann demonstration

### Additional Visual Experiments

- Step vs Sigmoid vs Tanh
- 2D convolution
- 3D convolution

---

# EcoSort Interactive Application

The final system is exposed through an interactive **Streamlit application**.

A user can:

1. Upload a waste image or choose a provided test sample.
2. Select the expected recycling material.
3. Adjust the detection-confidence threshold.
4. Run the AI inspection.
5. Compare the original and AI-analyzed image.
6. Review detected waste objects.
7. Inspect material composition.
8. Identify contaminants.
9. View purity and quality score.
10. Receive an operator recommendation.

The repository includes **12 unseen PackWISE test samples** to make controlled demonstrations easier.

---

# Repository Layout

```text
EcoSort-AI-Waste-Sorting/
│
├── app.py
├── README.md
├── requirements.txt
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
│   ├── sample_02.jpg
│   ├── ...
│   └── sample_12.jpg
│
└── notebooks/
    └── Waste_Sorting_PBL_Final.ipynb
```

---

# Running EcoSort AI

## 1. Clone the repository

```bash
git clone https://github.com/Mansi2106007/EcoSort-AI-Waste-Sorting.git
cd EcoSort-AI-Waste-Sorting
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Launch the application

```bash
streamlit run app.py
```

---

# Saved Models

The repository contains the trained weights required by the application and experimental modules:

```text
models/detection.pt
models/segmentation.pt
models/lstm.pth
models/vae.pth
```

Live retraining is not required to run the final inference application.

---

# Reproducibility Record

The recorded project environment included:

| Setting | Recorded Value |
|---|---|
| Random seed | **42** |
| Python | **3.13.16** |
| PyTorch | **2.14.1+cu130** |
| Ultralytics | **8.4.216** |
| CUDA | **Available** |
| GPU | **Tesla T4** |

The final reproducibility verification confirmed the availability of the dataset assets, test set, trained detection model, trained segmentation model and application.

**Recorded Reproducibility Check: PASS**

---

# Where EcoSort Currently Fails

EcoSort AI is an academic prototype, not a finished industrial sorting system.

Important limitations include:

1. **Dataset scale**  
   586 images across 23 categories is relatively small for a highly variable real-world detection task.

2. **Class imbalance**  
   Several rare categories contain limited examples.

3. **Moderate detection performance**  
   The unseen-test detection metrics leave substantial room for improvement.

4. **Variable segmentation quality**  
   Mask quality differs significantly between objects.

5. **Noise sensitivity**  
   Strong image noise caused complete detection failure in the tested robustness case.

6. **Purity definition**  
   Current purity is object-count based. Industrial material purity may require area-, mass- or process-based measurements.

7. **Experimental advanced models**  
   The LSTM and VAE demonstrate sequence and generative modeling but are not autonomous production controllers.

8. **Domain shift**  
   Performance may change with different conveyor systems, cameras, lighting, waste composition and facilities.

---

# Deployment Decision

## GO — Current Appropriate Use

EcoSort AI is suitable for:

- academic evaluation
- controlled demonstrations
- deep-learning experimentation
- recycling-AI research prototypes
- operator decision-support exploration

## NO-GO — Current Inappropriate Use

The current model should **not** be used as the sole decision maker for:

- autonomous industrial sorting
- safety-critical operations
- regulatory material classification
- unsupervised production deployment

Production use would require broader real-world datasets, stronger robustness, improved detection and segmentation performance, calibration and controlled facility trials.

---

# Responsible Use

EcoSort AI analyzes visual waste information.

It does **not** directly measure:

- chemical composition
- physical mass
- hazardousness
- regulatory recyclability
- material safety

Predictions should therefore be treated as visual AI estimates rather than guaranteed physical measurements.

Human verification remains appropriate for uncertain or operationally important decisions.

---

# Development & AI Assistance Disclosure

AI tools were used as **supporting development tools** for tasks such as:

- implementation guidance
- debugging
- explanation of deep-learning concepts
- documentation assistance
- interface refinement

The project pipeline was executed and evaluated using the actual project dataset and saved experimental results.

Generated suggestions were reviewed, tested and modified according to the requirements of EcoSort AI.

The final project is intended to be technically explainable and reproducible rather than an external AI API wrapper.

---

# Current Project Status

| Area | Status |
|---|---|
| Dataset preparation | Complete |
| Leakage verification | Complete |
| Detection training | Complete |
| Instance segmentation | Complete |
| LSTM experiment | Complete |
| VAE experiment | Complete |
| Evaluation package | Complete |
| Robustness analysis | Complete |
| Streamlit application | Complete |
| Saved model weights | Available |
| Academic prototype | **READY** |
| Autonomous industrial deployment | **NOT READY** |

---

# Project Scope

**Project:** Waste Sorting and Recycling Quality Controller  
**Domain:** Circular Economy  
**Course:** Deep Learning — Semester V

---

## EcoSort AI

**Detect waste. Understand the stream. Evaluate recycling quality.**
