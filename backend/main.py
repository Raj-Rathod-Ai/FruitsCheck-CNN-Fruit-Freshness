import io
import os
import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, File, Form, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
from PIL import Image, UnidentifiedImageError

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("fruitcheck-api")

# Model configuration
SUPPORTED_FRUITS = {"apple", "banana", "orange"}
IMAGE_SIZE = (224, 224)

def resolve_model_path() -> Optional[str]:
    """Search for .keras primary model with .h5 fallback."""
    candidate_paths = [
        os.path.join(os.path.dirname(__file__), "models", "fruits_classification.keras"),
        os.path.join(os.path.dirname(__file__), "fruits_classification.keras"),
        os.path.join(os.path.dirname(__file__), "..", "fruits_classification.keras"),
        "fruits_classification.keras",
        os.path.join(os.path.dirname(__file__), "models", "fruits_classification.h5"),
        os.path.join(os.path.dirname(__file__), "fruits_classification.h5"),
        os.path.join(os.path.dirname(__file__), "..", "fruits_classification.h5"),
        "fruits_classification.h5",
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            return os.path.abspath(path)
    return None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to load TensorFlow model once on startup."""
    model_path = resolve_model_path()
    app.state.model = None
    app.state.model_name = None

    if model_path:
        logger.info(f"Loading fruit freshness classification model from: {model_path}")
        try:
            import tensorflow as tf
            # Load model once as a singleton
            app.state.model = tf.keras.models.load_model(model_path)
            app.state.model_name = os.path.basename(model_path)
            logger.info("TensorFlow model loaded successfully into memory.")
        except Exception as e:
            logger.error(f"Failed to load model from {model_path}: {e}")
    else:
        logger.warning("No model file (fruits_classification.keras or .h5) found in search paths.")

    yield

    # Teardown logic
    if app.state.model is not None:
        logger.info("Cleaning up model references on application shutdown.")
        app.state.model = None

# Initialize FastAPI application
app = FastAPI(
    title="FruitCheck AI - Fruit Freshness Classification API",
    description="Production-grade AI inference API for Fresh vs Rotten classification of apples, bananas, and oranges.",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
# Hugging Face Spaces serves the API publicly — allow all origins by default
# (HF Spaces apps are public; restrict via FRONTEND_URL env var if needed)
allowed_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    # Netlify preview & production domains
    "https://*.netlify.app",
    # Hugging Face Spaces origin (when testing via HF UI)
    "https://*.hf.space",
    "https://huggingface.co",
]

frontend_env_url = os.getenv("FRONTEND_URL")
if frontend_env_url:
    for url in frontend_env_url.split(","):
        url = url.strip().rstrip("/")
        if url:
            allowed_origins.append(url)

# For public HF Spaces deployment, allow all origins so the Netlify frontend can call it
_allow_all = os.getenv("ALLOW_ALL_CORS", "true").lower() in ("1", "true", "yes")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if _allow_all else allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Decodes and normalizes image for the 224x224x3 CNN.
    Returns np.ndarray of shape (1, 224, 224, 3) with float32 values in [0, 1].
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
    except (UnidentifiedImageError, ValueError) as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is not a valid or readable image. Please upload a JPG, JPEG, or PNG."
        ) from err

    image = image.convert("RGB")
    image = image.resize(IMAGE_SIZE)

    image_array = np.array(image).astype("float32")
    image_array = image_array / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    return image_array

@app.get("/", tags=["General"])
async def root():
    return {
        "service": "Fruit Freshness Classification API",
        "status": "running"
    }

@app.get("/health", tags=["Monitoring"])
async def health_check():
    """
    Extremely lightweight health monitoring endpoint.
    Does NOT load the model or perform inference.
    """
    return {"status": "ok"}

@app.get("/ready", tags=["Monitoring"])
async def readiness_check():
    """Returns model readiness state for deployment orchestration."""
    if hasattr(app.state, "model") and app.state.model is not None:
        return {
            "ready": True,
            "model": app.state.model_name or "fruits_classification"
        }
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"ready": False, "message": "Model is not yet loaded into memory."}
    )

@app.post("/predict", tags=["Inference"])
async def predict_freshness(
    file: UploadFile = File(...),
    fruit: str = Form(...)
):
    """
    Inference endpoint for fruit freshness classification.
    Validates fruit selection and performs CNN inference on uploaded image.
    """
    # Verify model is available
    if not hasattr(app.state, "model") or app.state.model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is currently unavailable. Please try again shortly."
        )

    # Normalize fruit input
    fruit_cleaned = (fruit or "").strip().lower()
    is_supported = fruit_cleaned in SUPPORTED_FRUITS

    # If unsupported fruit is passed, return structured notice or validation error
    if not is_supported and fruit_cleaned not in ("other", "unspecified", "experimental"):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Unsupported fruit",
                "message": f"'{fruit}' is not currently supported. FruitCheck is trained exclusively on Apple, Banana, and Orange. Other fruits are currently in the training phase.",
                "supported_fruits": ["Apple", "Banana", "Orange"]
            }
        )

    # Validate uploaded file type
    if not file.content_type or not (
        file.content_type.startswith("image/") or
        file.filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Please upload a JPG, JPEG, PNG, or WebP image."
        )

    # Read image contents into memory
    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty."
            )
        if len(contents) > 15 * 1024 * 1024:  # 15MB safety limit
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image file size exceeds maximum limit of 15 MB."
            )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to read uploaded image stream."
        ) from e

    # Preprocess image
    image_tensor = preprocess_image(contents)

    # Perform inference using singleton model
    try:
        prediction = app.state.model.predict(image_tensor, verbose=0)
        probability = float(prediction[0][0])
    except Exception as e:
        logger.error(f"Inference execution error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error occurred while analyzing the image."
        ) from e

    # Exact label mapping verified from CNN.ipynb:
    # 0 = Fresh (freshapples, freshbanana, freshoranges)
    # 1 = Rotten (rottenapples, rottenbanana, rottenoranges)
    if probability >= 0.5:
        predicted_label = "Rotten"
        confidence_pct = round(probability * 100.0, 2)
    else:
        predicted_label = "Fresh"
        confidence_pct = round((1.0 - probability) * 100.0, 2)

    fruit_display_name = fruit_cleaned.capitalize() if fruit_cleaned in SUPPORTED_FRUITS else "Other / Unlisted Fruit"

    return {
        "fruit": fruit_display_name,
        "prediction": predicted_label,
        "confidence": confidence_pct,
        "raw_score": round(probability, 4),
        "is_supported_fruit": is_supported,
        "disclaimer": "This is an image classification prediction based on visual appearance, not a food-safety guarantee.",
        "model_notice": "This model is trained specifically on apples, bananas, and oranges. Predictions for other fruits are not guaranteed."
    }
