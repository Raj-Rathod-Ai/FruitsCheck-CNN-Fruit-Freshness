"""
FruitCheck — Model Download Helper
===================================
The trained model files (fruits_classification.keras / .h5) are NOT
stored in this repository because they exceed GitHub's 100 MB file limit.

Run this script to re-download the dataset from Kaggle and
retrain the model (re-run CNN.ipynb), OR manually place the model files
in the project root before running the FastAPI backend.

Option 1: Re-train via CNN.ipynb
---------------------------------
    pip install kagglehub tensorflow jupyter
    jupyter notebook CNN.ipynb
    # Run all cells — model will be saved as fruits_classification.keras

Option 2: Download dataset only (no training)
----------------------------------------------
    pip install kagglehub
    python download_model.py

This will download the raw dataset to the Kaggle cache directory.
"""

import os

try:
    import kagglehub
    print("Downloading fruits dataset from Kaggle...")
    path = kagglehub.dataset_download("sriramr/fruits-fresh-and-rotten-for-classification")
    print(f"\n✅ Dataset downloaded to: {path}")
    print("\nNext steps:")
    print("  1. Open CNN.ipynb in Jupyter")
    print("  2. Run all cells to train the CNN")
    print("  3. Model will be saved as 'fruits_classification.keras'")
except ImportError:
    print("Please install kagglehub first:")
    print("  pip install kagglehub")
except Exception as e:
    print(f"Download failed: {e}")
    print("\nManual download:")
    print("  https://www.kaggle.com/datasets/sriramr/fruits-fresh-and-rotten-for-classification")
