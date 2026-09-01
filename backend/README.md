---
title: FruitCheck API
emoji: 🍎
colorFrom: green
colorTo: orange
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# FruitCheck — Fruit Freshness Classification API

Production-grade FastAPI backend for **FruitCheck** — an AI-powered fruit freshness detection system.

## Supported Fruits
- 🍎 Apple
- 🍌 Banana  
- 🍊 Orange

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Service info |
| GET | `/health` | Lightweight health check |
| GET | `/ready` | Model readiness probe |
| POST | `/predict` | Freshness inference |

## POST /predict

**Form fields:**
- `file` — image file (JPG / PNG / WebP)
- `fruit` — `apple`, `banana`, or `orange`

**Response:**
```json
{
  "fruit": "Apple",
  "prediction": "Fresh",
  "confidence": 96.42
}
```

## Model
- Architecture: Custom CNN (Conv2D × 3 → Dense → Sigmoid)
- Input: 224 × 224 × 3 RGB
- Test Accuracy: 96.33%
- Framework: TensorFlow / Keras

## Disclaimer
This model is trained specifically on apples, bananas, and oranges.
This is a visual classification prediction, not a food-safety guarantee.
