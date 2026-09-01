# FruitCheck — Deployment Guide (Streamlit Community Cloud)

## Project Structure (Clean)

```
FruitsCheck-CNN-Fruit-Freshness/
├── app.py              ← Streamlit app (UI + CNN inference)
├── requirements.txt    ← Python dependencies
├── CNN.ipynb           ← Training notebook
├── download_model.py   ← Helper to re-download dataset
├── README.md
└── .gitignore
```

---

## STEP 1 — Upload Model to Hugging Face Model Hub (Free)

The model (`fruits_classification.keras`, ~508 MB) is too large for GitHub.
Store it on HF Model Hub — completely free, unlimited size.

1. Go to → **https://huggingface.co/new** (select "Model")
2. **Repository name:** `fruitcheck-model`
3. **Visibility:** Public
4. Click **Create model**
5. On the model page click **"Add file"** → **Upload file**
6. Upload `C:\DL\CNN\fruits_classification.keras`
7. Your model URL will be:
   ```
   https://huggingface.co/Raj1908/fruitcheck-model
   ```

---

## STEP 2 — Deploy on Streamlit Community Cloud

1. Go to → **https://share.streamlit.io**
2. Click **"Sign in with GitHub"**
3. Click **"New app"**
4. Fill in:

   | Field | Value |
   |-------|-------|
   | **Repository** | `Raj-Rathod-Ai/FruitsCheck-CNN-Fruit-Freshness` |
   | **Branch** | `main` |
   | **Main file path** | `app.py` |

5. Click **"Advanced settings"** → **Secrets** tab
6. Add:
   ```toml
   HF_MODEL_REPO = "Raj1908/fruitcheck-model"
   ```
7. Click **"Deploy!"**

Your app will be live at:
```
https://raj1908-fruitcheck.streamlit.app
```

---

## STEP 3 — Local Development

```powershell
# Install dependencies
pip install -r requirements.txt

# Place model in project root
# (copy fruits_classification.keras to C:\DL\CNN\)

# Run app
python -m streamlit run app.py
# → http://localhost:8501
```

---

## Health Endpoint

Streamlit Community Cloud automatically provides:
```
https://your-app.streamlit.app/_stcore/health
→ {"status": "ok"}
```

No extra code needed — it's built into Streamlit.

---

## Model Recovery

If model file is lost, regenerate it:
```powershell
# Option 1: Re-train via notebook
pip install kagglehub tensorflow jupyter
jupyter notebook CNN.ipynb   # Run all cells

# Option 2: Download dataset only
python download_model.py
```

---

## Label Mapping (verified from CNN.ipynb)

| Classes | Binary | Sigmoid Output |
|---------|--------|---------------|
| freshapples, freshbanana, freshoranges | `0` → **Fresh** | `< 0.5` |
| rottenapples, rottenbanana, rottenoranges | `1` → **Rotten** | `≥ 0.5` |
