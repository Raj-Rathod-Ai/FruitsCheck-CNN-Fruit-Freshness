# 🍎 FruitCheck — CNN-Based Fruit Freshness Classifier

<div align="center">

![FruitCheck Banner](https://img.shields.io/badge/FruitCheck-CNN%20Fruit%20Freshness%20Classifier-brightgreen?style=for-the-badge&logo=tensorflow)

[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.21.0-FF6F00?style=flat-square&logo=tensorflow)](https://tensorflow.org)
[![Keras](https://img.shields.io/badge/Keras-3.15.1-D00000?style=flat-square&logo=keras)](https://keras.io)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python)](https://python.org)
[![Dataset](https://img.shields.io/badge/Dataset-Kaggle-20BEFF?style=flat-square&logo=kaggle)](https://www.kaggle.com/datasets/sriramr/fruits-fresh-and-rotten-for-classification)

**A Convolutional Neural Network trained to classify fruit images as Fresh or Rotten.**  
Built from scratch using TensorFlow/Keras, trained on a real-world image dataset with data augmentation, achieving **96.79% validation accuracy** and **96.33% test accuracy**.

[View Notebook](#-notebook-walkthrough) • [Model Architecture](#-model-architecture) • [Training Results](#-training-results) • [How to Run](#-how-to-run-locally)

</div>

---

## 📌 Project Overview

FruitCheck is a **binary image classification** project that uses a custom **Convolutional Neural Network (CNN)** trained end-to-end on a fruit freshness dataset.

The model learns to distinguish **Fresh** vs **Rotten** fruits using visual patterns in images — such as color, texture, and surface degradation — without any hand-crafted features.

### Supported Fruits
| Fruit | Fresh Class | Rotten Class |
|-------|------------|-------------|
| 🍎 Apple | `freshapples` | `rottenapples` |
| 🍌 Banana | `freshbanana` | `rottenbanana` |
| 🍊 Orange | `freshoranges` | `rottenoranges` |

> ⚠️ The model is **trained only on these 3 fruits**. Predictions for other fruits (mango, grapes, etc.) are unsupported and unreliable.

---

## 📊 Dataset

**Source:** [Fruits Fresh and Rotten for Classification — Kaggle](https://www.kaggle.com/datasets/sriramr/fruits-fresh-and-rotten-for-classification)

```
dataset/
├── train/
│   ├── freshapples/     (1693 images)
│   ├── freshbanana/     (1581 images)
│   ├── freshoranges/    (1466 images)
│   ├── rottenapples/    (2342 images)
│   ├── rottenbanana/    (2224 images)
│   └── rottenoranges/   (1595 images)
└── test/
    ├── freshapples/      (395 images)
    ├── freshbanana/      (381 images)
    ├── freshoranges/     (388 images)
    ├── rottenapples/     (601 images)
    ├── rottenbanana/     (530 images)
    └── rottenoranges/    (403 images)
```

| Split | Images | Batches (batch_size=32) |
|-------|--------|------------------------|
| Train (80%) | ~8,721 | 273 |
| Validation (20%) | ~2,180 | 69 |
| Test | 2,698 | 85 |

---

## 🧠 Deep Learning Concepts Used

This project covers the following core Deep Learning / Computer Vision concepts:

### 1. Convolutional Neural Networks (CNN)
CNNs are designed for image data. They use:
- **Convolutional layers** — learn spatial feature maps (edges, textures, shapes)
- **Pooling layers** — downsample feature maps, reduce computation
- **Fully connected layers** — map learned features to output classes

### 2. Binary Classification with Sigmoid
Since the task is **Fresh vs. Rotten** (two classes), the output layer uses a single neuron with **sigmoid activation**:
```
σ(x) = 1 / (1 + e^(-x))
```
- Output `< 0.5` → **Fresh**
- Output `≥ 0.5` → **Rotten**

### 3. Data Normalization
All pixel values normalized to `[0.0, 1.0]` by dividing by 255:
```python
image = tf.cast(image / 255., tf.float32)
```
This stabilizes gradient updates and speeds up convergence.

### 4. Label Mapping (Binary from Multi-class)
The dataset has 6 classes (3 fruits × 2 conditions). We map them to binary:
```python
# Classes 0–2 = Fresh (freshapples, freshbanana, freshoranges)
# Classes 3–5 = Rotten (rottenapples, rottenbanana, rottenoranges)
binary_label = tf.cast(label >= len(class_names) // 2, tf.int32)
```

### 5. Data Augmentation
To prevent **overfitting** and improve generalization, the training set is augmented at runtime:
```python
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip('horizontal'),
    tf.keras.layers.RandomRotation(0.2),
    tf.keras.layers.RandomZoom(0.2),
    tf.keras.layers.RandomContrast(0.2)
])
```
Augmentation artificially increases dataset diversity without collecting new images.

### 6. Early Stopping (Regularization Technique)
Monitors `val_loss` and stops training when it stops improving:
```python
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)
```
- Prevents overfitting
- Restores the best model weights automatically

### 7. Adam Optimizer
Adaptive Moment Estimation — combines momentum and RMSProp:
- Adjusts learning rate per-parameter
- Works well with sparse gradients
- Default learning rate: `1e-3`

### 8. Binary Cross-Entropy Loss
Loss function for binary classification:
```
L = -[y · log(ŷ) + (1−y) · log(1−ŷ)]
```
- Penalizes confident wrong predictions heavily
- Ideal for sigmoid output layers

---

## 🏗️ Model Architecture

```
Input Image: 224 × 224 × 3 (RGB)
       │
       ▼
┌─────────────────────────────────┐
│  Conv2D(32 filters, 3×3, ReLU)  │  ← Learns 32 low-level feature maps
│  MaxPooling2D(2×2)              │  ← Halves spatial dimensions: 112×112
└─────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  Conv2D(64 filters, 3×3, ReLU)  │  ← Learns 64 mid-level features
│  MaxPooling2D(2×2)              │  ← 56×56
└─────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ Conv2D(128 filters, 3×3, ReLU)  │  ← Learns 128 high-level features
│  MaxPooling2D(2×2)              │  ← 28×28
└─────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│          Flatten()              │  ← 28 × 28 × 128 = 100,352 neurons
└─────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│      Dense(512, ReLU)           │  ← Fully connected feature integration
└─────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│    Dense(1, Sigmoid)            │  ← Binary output: Fresh (< 0.5) / Rotten (≥ 0.5)
└─────────────────────────────────┘
       │
       ▼
  Prediction: Fresh / Rotten
```

### Layer-by-Layer Summary

| Layer | Output Shape | Parameters |
|-------|-------------|-----------|
| Conv2D(32, 3×3) | 222 × 222 × 32 | 896 |
| MaxPooling2D(2×2) | 111 × 111 × 32 | 0 |
| Conv2D(64, 3×3) | 109 × 109 × 64 | 18,496 |
| MaxPooling2D(2×2) | 54 × 54 × 64 | 0 |
| Conv2D(128, 3×3) | 52 × 52 × 128 | 73,856 |
| MaxPooling2D(2×2) | 26 × 26 × 128 | 0 |
| Flatten | 86,528 | 0 |
| Dense(512) | 512 | 44,302,848 |
| Dense(1, Sigmoid) | 1 | 513 |
| **Total Trainable** | | **~44.4 M** |

---

## 📈 Training Results

### Training Configuration
```
Optimizer   : Adam (lr=1e-3)
Loss        : Binary Cross-Entropy
Metrics     : Accuracy
Epochs      : Up to 30 (early stopping applied)
Batch Size  : 32
Image Size  : 224 × 224
```

### Epoch-by-Epoch Log

| Epoch | Train Acc | Train Loss | Val Acc | Val Loss | Note |
|-------|-----------|-----------|---------|----------|------|
| 1 | 85.31% | 0.3246 | 91.83% | 0.2002 | Strong start |
| 2 | 91.37% | 0.2094 | 94.68% | 0.1421 | +3% jump |
| 3 | 93.31% | 0.1685 | 93.67% | 0.1639 | Slight val dip |
| 4 | 93.26% | 0.1642 | 94.31% | 0.1321 | Recovering |
| 5 | 93.89% | 0.1486 | 95.60% | 0.1080 | Consistent gain |
| 6 | 94.85% | 0.1250 | 95.18% | 0.1078 | Stable |
| 7 | 94.89% | 0.1273 | 93.07% | 0.1791 | Val spike |
| 8 | 95.22% | 0.1185 | 93.53% | 0.1396 | Recovering |
| 9 | 95.64% | 0.1089 | 96.61% | 0.0877 | Near best |
| **10** | **96.40%** | **0.0909** | **96.79%** | **0.0836** | 🏆 **Best checkpoint** |
| 11 | 96.22% | 0.0972 | 96.42% | 0.0901 | EarlyStopping: +1 |
| 12 | 96.19% | 0.1042 | 95.46% | 0.1126 | EarlyStopping: +2 |
| 13 | 96.46% | 0.0899 | 95.50% | 0.1169 | EarlyStopping: +3 → STOP |

> **Training stopped at Epoch 13.** Best weights from **Epoch 10** restored automatically (`restore_best_weights=True`).

### Learning Curves Analysis

```
Accuracy                        Loss
   %                              
97 |          ●10                 0.08 |          ●10
96 |       ●9    ●11●13           0.09 |       ●9    ●11
95 |    ●6●7    ●12               0.11 |    ●6●7    ●12
94 |  ●4●5                        0.14 |  ●4●5
93 | ●3                           0.16 | ●3
92 | ●2                           0.20 | ●2
91 |●1                            0.32 |●1
   └──────────────────            └──────────────────
        Epoch                          Epoch

─── Val Accuracy/Loss
```

**Key observations:**
- **Epoch 1–5**: Rapid learning phase — both train and val accuracy improve sharply
- **Epoch 6–8**: Slight instability in val_loss (normal with augmented data)
- **Epoch 9–10**: Model reaches optimal generalization
- **Epoch 11–13**: Val loss begins increasing → Early stopping activates

### Final Model Performance

| Metric | Value |
|--------|-------|
| **Best Validation Accuracy** | **96.79%** (Epoch 10) |
| **Best Validation Loss** | **0.0836** (Epoch 10) |
| **Test Accuracy** | **96.33%** |
| **Test Loss** | **0.0917** |
| **Test Images** | 2,698 |

---

## 🔬 Image Preprocessing Pipeline

```
Raw Image (any size, any format)
        │
        ▼
   PIL Image.open()
        │
        ▼
   .convert("RGB")        ← ensures 3-channel (removes alpha, grayscale)
        │
        ▼
   .resize((224, 224))    ← bilinear interpolation to fixed input size
        │
        ▼
   np.array(image)        ← convert to NumPy array: shape (224, 224, 3)
        │
        ▼
   .astype("float32")     ← convert uint8 [0,255] → float32
        │
        ▼
   array / 255.0          ← normalize to [0.0, 1.0]
        │
        ▼
   np.expand_dims(axis=0) ← add batch dimension: (1, 224, 224, 3)
        │
        ▼
   model.predict()        ← CNN inference
        │
        ▼
   sigmoid output [0.0 – 1.0]
        │
   ┌────┴────┐
< 0.5       ≥ 0.5
   │           │
 FRESH       ROTTEN
```

---

## 🗂️ Project Structure

```
FruitsCheck-CNN-Fruit-Freshness/
│
├── app.py               # 🖥️  Streamlit app (UI + CNN inference — all-in-one)
├── requirements.txt     # 📦  Python dependencies for Streamlit Cloud
├── CNN.ipynb            # 📓  Full training notebook
├── download_model.py    # 🔧  Helper to re-download Kaggle dataset
├── DEPLOYMENT.md        # 🚀  Step-by-step deployment guide
└── README.md            # 📖  This file
```

---

## ⚙️ How to Run Locally

### Prerequisites
- Python 3.10+
- TensorFlow 2.15+
- Jupyter Notebook / Jupyter Lab

### 1. Clone the repository
```bash
git clone https://github.com/Raj-Rathod-Ai/FruitsCheck-CNN-Fruit-Freshness.git
cd FruitsCheck-CNN-Fruit-Freshness
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the model (first time)
```bash
# Download dataset from Kaggle and train
jupyter notebook CNN.ipynb
# Run all cells — saves fruits_classification.keras
```

### 4. Run the Streamlit app
```bash
# Place fruits_classification.keras in the project root, then:
streamlit run app.py
# → Open http://localhost:8501
```

---

## 📦 Saved Models

| File | Format | Size | Notes |
|------|--------|------|-------|
| `fruits_classification.keras` | Native Keras | ~508 MB | ✅ Primary — use this |
| `fruits_classification.h5` | HDF5 (legacy) | ~508 MB | Fallback only |

> The large size is due to the Dense(512) layer having ~44M parameters.
> Future optimization: TFLite / INT8 quantization → reduces to ~127 MB.

---

## 🔮 Future Work & Improvements

| Improvement | Description | Expected Gain |
|-------------|-------------|---------------|
| **Transfer Learning** | Replace custom CNN with MobileNetV3 / EfficientNetB0 pretrained on ImageNet | +2–4% accuracy, 10× smaller model |
| **Multi-class output** | Add fruit-type identification head (6-class softmax) | Identify fruit type without user selection |
| **TFLite Quantization** | INT8 post-training quantization | Model size: 508 MB → ~127 MB |
| **More fruit classes** | Expand dataset to mango, strawberry, grape, pineapple | Broader real-world use |
| **Grad-CAM Visualization** | Visualize which image regions the CNN focuses on | Model interpretability |
| **Batch Normalization** | Add BatchNorm after Conv layers | Faster convergence, better regularization |
| **Dropout Regularization** | Add Dropout(0.5) before Dense layers | Reduce overfitting risk |
| **Learning Rate Scheduling** | ReduceLROnPlateau callback | Fine-grained convergence |

---

## 🧪 ML Concepts Reference (for Beginners)

| Concept | Used In Project | Why It Matters |
|---------|----------------|----------------|
| Convolutional Layer | All 3 Conv2D blocks | Extracts spatial features from images |
| Max Pooling | After each Conv block | Reduces spatial size, adds translation invariance |
| ReLU Activation | All hidden layers | Introduces non-linearity, solves vanishing gradient |
| Sigmoid Activation | Output layer | Squashes output to [0,1] for binary probability |
| Batch Normalization | (Future) | Stabilizes training |
| Data Augmentation | Training pipeline | Reduces overfitting, improves generalization |
| Early Stopping | Training callback | Prevents overfitting, saves computation |
| Adam Optimizer | Model compilation | Adaptive learning rates per parameter |
| Binary Cross-Entropy | Loss function | Optimal loss for binary classification |
| Transfer Learning | (Future) | Leverage pre-trained ImageNet knowledge |

---

## 📚 Tech Stack

| Category | Technology | Version |
|----------|-----------|---------|
| Deep Learning | TensorFlow | 2.21.0 |
| Model API | Keras | 3.15.1 |
| Numerical Computing | NumPy | 2.5.1 |
| Image Processing | Pillow | 12.3.0 |
| Web App | Streamlit | 1.59.2 |
| Deployment | Streamlit Community Cloud | Free |

---

## 📖 Notebook Walkthrough

The [`CNN.ipynb`](./CNN.ipynb) notebook covers these sections in order:

1. **Dataset Download** — `kagglehub.dataset_download()`
2. **Dataset Loading** — `tf.keras.utils.image_dataset_from_directory()` with 80/20 train-val split
3. **Class Inspection** — Print original 6 class names
4. **Normalization** — Pixel values `/255.0`
5. **Binary Label Mapping** — Map 6 classes → 2 binary labels (Fresh / Rotten)
6. **Data Augmentation** — Random flip, rotation, zoom, contrast
7. **Model Definition** — Sequential CNN with 3 Conv blocks
8. **Model Summary** — Layer-by-layer parameter count
9. **Model Compilation** — Adam + Binary Cross-Entropy
10. **Model Training** — `model.fit()` with EarlyStopping
11. **Test Evaluation** — `model.evaluate()` on held-out test set
12. **Model Saving** — `.keras` and `.h5` formats

---

## 👤 Author

**Raj Rathod** — AI/ML Engineer (Fresher)  
GitHub: [@Raj-Rathod-Ai](https://github.com/Raj-Rathod-Ai)

---



<div align="center">

⭐ **If this project helped you learn CNNs or image classification, please star it!** ⭐

</div>
