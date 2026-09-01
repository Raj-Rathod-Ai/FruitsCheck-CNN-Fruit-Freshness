# FruitCheck — Deployment Guide
# Backend → Hugging Face Spaces (FREE)
# Frontend → Netlify (FREE)

---

## 🏗️ Final Architecture

```
User Browser
     │
     ▼
Netlify (Frontend — React + Vite)
  VITE_API_URL = https://YOUR_HF_USERNAME-fruitcheck-api.hf.space
     │
     │  POST /predict
     │  GET  /health
     │  GET  /ready
     ▼
Hugging Face Spaces (Backend — FastAPI + TensorFlow)
  Docker container, port 7860
  Singleton model: fruits_classification.keras
  CNN → Fresh / Rotten
```

---

## ✅ Accounts You Need (all FREE, no credit card)

| Service | Link | Purpose |
|---------|------|---------|
| GitHub | github.com | Code hosting + Git LFS for model |
| Hugging Face | huggingface.co | Backend API hosting (Docker) |
| Netlify | netlify.com | Frontend hosting |

---

## STEP 1 — Install Git + Git LFS

### Install Git
- Download from: https://git-scm.com/download/win
- Install with default settings

### Install Git LFS (required for ~508 MB model file)
- Download from: https://git-lfs.com
- Install, then open PowerShell and run:
```powershell
git lfs install
```

---

## STEP 2 — Push Backend to GitHub (Separate Repo for HF)

Hugging Face Spaces syncs directly from a GitHub repo OR
you can push directly to HF's own Git server.

We will push the BACKEND folder as its own repo to Hugging Face Git.

```powershell
cd C:\DL\CNN\backend

git init
git lfs install
git lfs track "*.keras"
git lfs track "*.h5"
git add .gitattributes
git add .
git commit -m "Initial: FruitCheck FastAPI backend"
```

---

## STEP 3 — Create Hugging Face Space

1. Go to https://huggingface.co → Sign up / Log in (free)
2. Click your profile photo (top right) → **New Space**
3. Fill in:

| Field | Value |
|-------|-------|
| **Space name** | `fruitcheck-api` |
| **License** | MIT |
| **SDK** | **Docker** |
| **Visibility** | Public |

4. Click **Create Space**

5. HF will show you an empty repo with a Git URL like:
   ```
   https://huggingface.co/spaces/YOUR_HF_USERNAME/fruitcheck-api
   ```

---

## STEP 4 — Copy Model into Backend Folder

Before pushing, put the model inside the backend folder:

```powershell
# Create models subfolder in backend
New-Item -ItemType Directory -Path "C:\DL\CNN\backend\models" -Force

# Copy model
Copy-Item "C:\DL\CNN\fruits_classification.keras" `
          "C:\DL\CNN\backend\models\fruits_classification.keras"
```

---

## STEP 5 — Push Backend to Hugging Face Space

```powershell
cd C:\DL\CNN\backend

# Add HF Space as remote
git remote add space https://huggingface.co/spaces/YOUR_HF_USERNAME/fruitcheck-api

# Push (HF will ask for username + password)
# Use your HF username and a HF Access Token as the password
# Get token at: https://huggingface.co/settings/tokens → New token → Write access
git push space main
```

> **Note:** The push uploads the ~508 MB model via Git LFS.
> This may take 5–15 minutes depending on your internet speed.

### Get your HF Access Token:
1. Go to https://huggingface.co/settings/tokens
2. Click **New token**
3. Name: `fruitcheck-deploy`
4. Role: **Write**
5. Copy the token — use it as the password when `git push` asks

---

## STEP 6 — Verify Backend is Running on HF

After push, HF will:
1. Detect the `Dockerfile`
2. Build the Docker image (installs TensorFlow — takes 5–10 min)
3. Start the container on port 7860
4. Load your model into memory

Your API will be live at:
```
https://YOUR_HF_USERNAME-fruitcheck-api.hf.space
```

Test it in your browser:
```
https://YOUR_HF_USERNAME-fruitcheck-api.hf.space/health
→ {"status":"ok"}

https://YOUR_HF_USERNAME-fruitcheck-api.hf.space/ready
→ {"ready":true,"model":"fruits_classification.keras"}

https://YOUR_HF_USERNAME-fruitcheck-api.hf.space/docs
→ Swagger UI (interactive API docs)
```

---

## STEP 7 — Push Frontend to GitHub

```powershell
cd C:\DL\CNN

git init
git lfs install
git lfs track "*.keras"
git lfs track "*.h5"
git add .gitattributes

# Create .gitignore
@"
__pycache__/
*.pyc
.env
node_modules/
frontend/dist/
backend/models/
"@ | Out-File -FilePath .gitignore -Encoding utf8

git add .
git commit -m "FruitCheck: full project"
```

Go to https://github.com/new → create repo named `fruitcheck` → then:

```powershell
git remote add origin https://github.com/YOUR_GH_USERNAME/fruitcheck.git
git branch -M main
git push -u origin main
```

---

## STEP 8 — Deploy Frontend to Netlify

1. Go to https://app.netlify.com
2. Click **Add new site** → **Import an existing project**
3. Click **Deploy with GitHub** → Select `fruitcheck` repo

4. Set build config:

| Field | Value |
|-------|-------|
| **Base directory** | `frontend` |
| **Build command** | `npm run build` |
| **Publish directory** | `frontend/dist` |

5. Click **Add environment variables** before deploying:

| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://YOUR_HF_USERNAME-fruitcheck-api.hf.space` |

6. Click **Deploy site**

Your frontend will be live at:
```
https://your-site-name.netlify.app
```

---

## STEP 9 — Test the Full App

Open your Netlify URL in the browser:

1. ✅ Check `● MODEL ONLINE` badge appears in the header
2. ✅ Select **Apple** from the fruit selector
3. ✅ Upload an apple image (JPG/PNG)
4. ✅ Click **Analyze freshness**
5. ✅ See **FRESH / ROTTEN** result with confidence bar
6. ✅ Click **Other Fruit** → popup says "Training Phase Roadmap"
7. ✅ Click **Analyze another image** → resets the form

---

## STEP 10 — Local Development

### Backend locally:
```powershell
cd C:\DL\CNN\backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# API docs: http://localhost:8000/docs
```

### Frontend locally:
```powershell
cd C:\DL\CNN\frontend
Copy-Item .env.example .env
# Edit .env → VITE_API_URL=http://localhost:8000
npm install
npm run dev
# App: http://localhost:5173
```

---

## 📊 HF Spaces Free Tier Info

| Resource | HF Free Tier |
|----------|-------------|
| RAM | 16 GB |
| CPU | 2 vCPU |
| Storage | 50 GB |
| Cost | **$0 — completely free** |
| Sleep | Spaces sleep after inactivity (cold start ~30s) |
| Model size limit | Up to 50 GB via Git LFS (free) |

> HF Spaces free tier has **16 GB RAM** — more than enough for the ~700 MB–1 GB
> TensorFlow runtime. This is why HF is better than Render Free (512 MB).

---

## API Reference

### GET /health
```json
{"status": "ok"}
```

### GET /ready
```json
{"ready": true, "model": "fruits_classification.keras"}
```

### POST /predict
**Form fields:** `file` (image), `fruit` (apple/banana/orange)

```json
{
  "fruit": "Apple",
  "prediction": "Fresh",
  "confidence": 96.42,
  "raw_score": 0.0358,
  "is_supported_fruit": true,
  "disclaimer": "This is an image classification prediction, not a food-safety guarantee."
}
```

### Unsupported fruit (400 error):
```json
{
  "error": "Unsupported fruit",
  "message": "'mango' is not currently supported. FruitCheck is trained exclusively on Apple, Banana, and Orange. Other fruits are currently in the training phase.",
  "supported_fruits": ["Apple", "Banana", "Orange"]
}
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| HF Space shows "Building..." | Normal — first build takes 5–10 min (installing TensorFlow) |
| `/ready` returns false | Model still loading — wait 30–60s after cold start |
| CORS error in browser | `ALLOW_ALL_CORS=true` is already set in backend by default |
| Git push rejected (file too large) | Run `git lfs track "*.keras"` before adding files |
| HF asks for password | Use your HF Access Token (not your HF login password) |
| Netlify 404 on page refresh | Already handled by `netlify.toml` SPA redirect rule |
| Frontend shows "OFFLINE" | HF Space is sleeping — wait ~30s for cold start |

---

## Label Mapping (verified from CNN.ipynb)

| Dataset Classes | Binary Label | Sigmoid Output |
|----------------|-------------|----------------|
| freshapples, freshbanana, freshoranges | `0` → **Fresh** | `< 0.5` |
| rottenapples, rottenbanana, rottenoranges | `1` → **Rotten** | `≥ 0.5` |
