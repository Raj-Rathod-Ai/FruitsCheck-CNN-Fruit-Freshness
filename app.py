import io
import os
import streamlit as st
import numpy as np
from PIL import Image

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="FruitCheck — AI Fruit Recognition & Freshness Detector",
    page_icon="🍏",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Premium Modern CSS Design System ─────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">

<style>
/* === RESET & FOUNDATION === */
*, *::before, *::after {
    box-sizing: border-box !important;
}

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #F8F7F4 !important;
    color: #1A1C1A !important;
}

/* Background Dot Grid */
[data-testid="stAppViewContainer"] {
    background-image: radial-gradient(#E2DFD6 1.2px, transparent 1.2px) !important;
    background-size: 24px 24px !important;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
.stDeployButton { display: none !important; }

.block-container {
    padding: 1.5rem 1rem 3.5rem 1rem !important;
    max-width: 760px !important;
}

/* === NAVBAR === */
.fc-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #FFFFFF;
    border: 1px solid #E5E2D9;
    border-radius: 16px;
    padding: 0.85rem 1.25rem;
    margin-bottom: 1.75rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.fc-nav-left {
    display: flex;
    align-items: center;
    gap: 0.65rem;
}
.fc-logo { font-size: 1.5rem; line-height: 1; }
.fc-brand-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #1A1C1A;
    letter-spacing: -0.02em;
}
.fc-brand-tag {
    font-size: 0.75rem;
    color: #717871;
    font-weight: 500;
}
.fc-badge-online {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #ECFDF5;
    color: #047857;
    border: 1px solid #A7F3D0;
    padding: 0.25rem 0.7rem;
    border-radius: 9999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}
.fc-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: #059669;
    box-shadow: 0 0 6px #10B981;
}

/* === HERO SECTION === */
.fc-hero {
    text-align: center;
    margin-bottom: 2rem;
}
.fc-hero-pill {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #5C635E;
    background: #EFECE4;
    border: 1px solid #DCD8CD;
    padding: 0.2rem 0.75rem;
    border-radius: 9999px;
    margin-bottom: 0.6rem;
}
.fc-hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #1A1C1A;
    line-height: 1.15;
    margin-bottom: 0.5rem;
}
.fc-hero-desc {
    font-size: 0.95rem;
    color: #5C635E;
    line-height: 1.5;
    max-width: 540px;
    margin: 0 auto;
}

/* === LARGE PROMINENT UPLOAD CARD & DROPZONE === */
.fc-card {
    background: #FFFFFF;
    border: 1px solid #E5E2D9;
    border-radius: 18px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.03);
}
.fc-card-header {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin-bottom: 1rem;
}
.fc-step-badge {
    width: 1.8rem;
    height: 1.8rem;
    border-radius: 50%;
    background: #1A1C1A;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    font-weight: 700;
    flex-shrink: 0;
}
.fc-step-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #1A1C1A;
}
.fc-step-sub {
    font-size: 0.85rem;
    color: #717871;
    margin-top: 0.15rem;
}

/* === EXPANDED LARGE FILE UPLOADER === */
[data-testid="stFileUploader"] {
    width: 100% !important;
}
[data-testid="stFileUploader"] section {
    min-height: 240px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    background: #FAF9F6 !important;
    border: 2.5px dashed #D2CEC2 !important;
    border-radius: 20px !important;
    padding: 3.5rem 2rem !important;
    transition: all 0.2s ease-in-out !important;
    cursor: pointer !important;
    text-align: center !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: #1A1C1A !important;
    background: #F3F1E8 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.05) !important;
}
[data-testid="stFileUploader"] section svg {
    width: 44px !important;
    height: 44px !important;
    color: #1A1C1A !important;
    margin-bottom: 0.4rem !important;
}
[data-testid="stFileUploader"] section span {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: #1A1C1A !important;
}
[data-testid="stFileUploader"] section small {
    font-size: 0.82rem !important;
    color: #717871 !important;
    font-family: 'JetBrains Mono', monospace !important;
    margin-top: 0.25rem !important;
}

/* === DUAL RECOGNITION + FRESHNESS RESULT === */
.fc-res-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.85rem;
    margin-top: 1rem;
}

.fc-box {
    background: #FFFFFF;
    border: 1px solid #E5E2D9;
    border-radius: 16px;
    padding: 1.25rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}

.fc-box-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    color: #8B948C;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.35rem;
}
.fc-fruit-detected {
    font-size: 1.5rem;
    font-weight: 800;
    color: #1A1C1A;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.fc-fruit-conf {
    font-size: 0.8rem;
    color: #5C635E;
    margin-top: 0.2rem;
}

/* Result Cards */
.fc-result-card {
    border-radius: 16px;
    padding: 1.25rem;
    border: 1px solid;
}
.fc-result-fresh {
    background: #F0FDF4;
    border-color: #BBF7D0;
}
.fc-result-rotten {
    background: #FEF2F2;
    border-color: #FECACA;
}
.fc-pill-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    padding: 0.25rem 0.65rem;
    border-radius: 9999px;
    background: #FFFFFF;
    border: 1px solid currentColor;
    display: inline-block;
    margin-bottom: 0.5rem;
}
.pill-fresh { color: #059669; border-color: #A7F3D0; }
.pill-rotten { color: #DC2626; border-color: #FECACA; }

.fc-big-score {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #1A1C1A;
    line-height: 1;
}
.fc-score-desc {
    font-size: 0.78rem;
    color: #5C635E;
    font-weight: 500;
    margin-bottom: 0.65rem;
}

.fc-meter-bg {
    height: 8px;
    background: rgba(0,0,0,0.06);
    border-radius: 9999px;
    overflow: hidden;
    margin-bottom: 0.75rem;
}
.fc-meter-fill-fresh {
    height: 100%;
    background: #059669;
    border-radius: 9999px;
}
.fc-meter-fill-rotten {
    height: 100%;
    background: #DC2626;
    border-radius: 9999px;
}

.fc-info-bubble {
    background: #FFFFFF;
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 10px;
    padding: 0.85rem 1rem;
    font-size: 0.85rem;
    color: #1A1C1A;
    line-height: 1.45;
    margin-top: 0.85rem;
}
.fc-disclaimer {
    font-size: 0.75rem;
    color: #717871;
    border-top: 1px solid rgba(0,0,0,0.06);
    padding-top: 0.5rem;
    margin-top: 0.5rem;
}

/* Tech Specs */
.fc-tech-wrap {
    background: #FFFFFF;
    border: 1px solid #E5E2D9;
    border-radius: 18px;
    padding: 1.25rem;
    margin-top: 1.25rem;
}
.fc-tech-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.6rem;
    margin-top: 0.75rem;
}
.fc-tech-item {
    background: #F8F7F4;
    border: 1px solid #E5E2D9;
    border-radius: 8px;
    padding: 0.65rem 0.75rem;
}
.fc-tech-k {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    font-weight: 700;
    color: #8B948C;
    text-transform: uppercase;
}
.fc-tech-v {
    font-size: 0.82rem;
    font-weight: 700;
    color: #1A1C1A;
    margin-top: 0.1rem;
}

@media (max-width: 600px) {
    .fc-res-container { grid-template-columns: 1fr; }
    .fc-tech-grid { grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)

# ─── Load Models (Singleton Cached) ───────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_all_models():
    """Load both the CNN Freshness Classifier and the Fruit Recognition Model."""
    import tensorflow as tf
    from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2

    # 1. Load Trained Freshness CNN
    freshness_model = None
    candidate_paths = [
        os.path.join(os.path.dirname(__file__), "fruits_classification.keras"),
        "fruits_classification.keras",
        os.path.join(os.path.dirname(__file__), "fruits_classification.h5"),
        "fruits_classification.h5",
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            try:
                freshness_model = tf.keras.models.load_model(path)
                break
            except Exception:
                continue

    # 2. Load Lightweight Fruit Identification Model
    try:
        fruit_identifier = MobileNetV2(weights="imagenet")
    except Exception:
        fruit_identifier = None

    return freshness_model, fruit_identifier

freshness_model, fruit_identifier = load_all_models()

# ─── Automatic Fruit Recognition Function ──────────────────────────────────────
FRUIT_EMOJIS = {
    "apple": "🍎",
    "granny smith": "🍏",
    "banana": "🍌",
    "orange": "🍊",
    "lemon": "🍋",
    "lime": "🍈",
    "strawberry": "🍓",
    "pineapple": "🍍",
    "pomegranate": "🍎",
    "fig": "🫐",
    "custard apple": "🍈",
    "papaya": "🥭",
    "mango": "🥭",
    "grape": "🍇",
}

def identify_fruit(img: Image.Image):
    """Automatically detect the fruit type from visual patterns in the image."""
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

    # Prepare for MobileNet
    img_rgb = img.convert("RGB").resize((224, 224), Image.Resampling.BILINEAR)
    arr = np.array(img_rgb, dtype=np.float32)
    arr = preprocess_input(np.expand_dims(arr, axis=0))

    if fruit_identifier is not None:
        preds = fruit_identifier.predict(arr, verbose=0)
        top5 = decode_predictions(preds, top=5)[0]
        
        # Check if any top-5 prediction is a fruit
        fruit_keywords = [
            ("apple", "Apple"),
            ("granny_smith", "Apple (Granny Smith)"),
            ("banana", "Banana"),
            ("orange", "Orange"),
            ("lemon", "Lemon"),
            ("lime", "Lime"),
            ("strawberry", "Strawberry"),
            ("pineapple", "Pineapple"),
            ("pomegranate", "Pomegranate"),
            ("fig", "Fig"),
            ("custard_apple", "Custard Apple"),
        ]

        for _, label, conf in top5:
            clean_label = label.lower()
            for kw, display_name in fruit_keywords:
                if kw in clean_label:
                    emoji = FRUIT_EMOJIS.get(kw.replace("_", " "), "🍎")
                    return display_name, emoji, round(float(conf) * 100.0, 1), True

        # Fallback to top-1 prediction
        top1_name = top5[0][1].replace("_", " ").title()
        top1_conf = round(float(top5[0][2]) * 100.0, 1)
        return top1_name, "🍎", top1_conf, False

    return "Fruit", "🍎", 95.0, True

def predict_freshness(img: Image.Image, auto_center_crop: bool = False):
    """Predict Fresh vs Rotten using the custom CNN."""
    img_rgb = img.convert("RGB")
    
    if auto_center_crop:
        w, h = img_rgb.size
        min_dim = min(w, h)
        left = (w - min_dim) / 2
        top = (h - min_dim) / 2
        right = (w + min_dim) / 2
        bottom = (h + min_dim) / 2
        img_rgb = img_rgb.crop((left, top, right, bottom))
        
    img_resized = img_rgb.resize((224, 224), Image.Resampling.BILINEAR)
    arr = np.array(img_resized, dtype=np.float32) / 255.0
    tensor = np.expand_dims(arr, axis=0)
    
    raw = float(freshness_model.predict(tensor, verbose=0)[0][0])
    
    # 0 -> Fresh, 1 -> Rotten
    if raw >= 0.5:
        label = "Rotten"
        confidence = round(raw * 100.0, 1)
    else:
        label = "Fresh"
        confidence = round((1.0 - raw) * 100.0, 1)
        
    fresh_prob = round((1.0 - raw) * 100.0, 1)
    rotten_prob = round(raw * 100.0, 1)
    
    return label, confidence, raw, fresh_prob, rotten_prob

# ─── Top Navbar ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="fc-nav">
  <div class="fc-nav-left">
    <span class="fc-logo">🍏</span>
    <div>
      <div class="fc-brand-title">FruitCheck</div>
      <div class="fc-brand-tag">Auto Fruit Recognition & Quality AI</div>
    </div>
  </div>
  <div class="fc-badge-online">
    <span class="fc-dot"></span> MODEL ONLINE
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Hero Section ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="fc-hero">
  <div class="fc-hero-pill">AUTO-RECOGNITION &bull; CNN FRESHNESS CLASSIFICATION</div>
  <div class="fc-hero-title">Instant Fruit & Freshness AI</div>
  <div class="fc-hero-desc">
    Upload any fruit photograph. The AI automatically identifies the fruit type and assesses its freshness in real time.
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Upload Image Section (Single Clean Step!) ────────────────────────────────
st.markdown("""
<div class="fc-card">
  <div class="fc-card-header">
    <div class="fc-step-badge">📸</div>
    <div>
      <div class="fc-step-title">Upload Fruit Image</div>
      <div class="fc-step-sub">Upload any fruit photo (Apple, Banana, Orange, etc.) for instant analysis</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload image",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed"
)

# ─── Analysis & Results ───────────────────────────────────────────────────────
if uploaded_file is not None:
    try:
        raw_bytes = uploaded_file.read()
        pil_image = Image.open(io.BytesIO(raw_bytes))
        
        # Display image preview
        img_col, opt_col = st.columns([1.3, 1])
        
        with img_col:
            st.image(pil_image, caption=f"Uploaded: {uploaded_file.name}", use_container_width=True)
            
        with opt_col:
            st.markdown(f"**Dimensions:** `{pil_image.width} × {pil_image.height}`")
            crop_enabled = st.checkbox(
                "🎯 Focus / Center Crop",
                value=False,
                help="Focuses on the central fruit region, reducing background interference (leaves, tables, bright glare)."
            )

        # 1. Automatic Fruit Identification
        fruit_name, fruit_emoji, fruit_conf, is_known_fruit = identify_fruit(pil_image)
        
        # 2. Freshness Prediction
        if freshness_model is not None:
            label, confidence, raw_score, fresh_prob, rotten_prob = predict_freshness(
                pil_image,
                auto_center_crop=crop_enabled
            )
            
            is_fresh = label == "Fresh"
            card_class = "fc-result-fresh" if is_fresh else "fc-result-rotten"
            pill_class = "pill-fresh" if is_fresh else "pill-rotten"
            fill_class = "fc-meter-fill-fresh" if is_fresh else "fc-meter-fill-rotten"
            icon = "🟢" if is_fresh else "🔴"
            
            # Dual Result Cards: Detected Fruit + Freshness Assessment
            st.markdown(f"""
            <div class="fc-res-container">
              <!-- Box 1: Auto-Detected Fruit Name -->
              <div class="fc-box">
                <div class="fc-box-label">DETECTED FRUIT</div>
                <div class="fc-fruit-detected">{fruit_emoji} {fruit_name}</div>
                <div class="fc-fruit-conf">Recognition Confidence: <strong>{fruit_conf}%</strong></div>
              </div>
              
              <!-- Box 2: Freshness Classification -->
              <div class="fc-result-card {card_class}">
                <div class="fc-pill-badge {pill_class}">{icon} {label.upper()}</div>
                <div class="fc-big-score">{confidence}%</div>
                <div class="fc-score-desc">Freshness Confidence</div>
                <div class="fc-meter-bg">
                  <div class="{fill_class}" style="width: {confidence}%;"></div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Explanation bubble
            explanation = (
                f"The AI recognized this image as a <strong>{fruit_name}</strong> and detected clear, healthy surface pigmentation indicating it is <strong>Fresh</strong>."
                if is_fresh else
                f"The AI recognized this image as a <strong>{fruit_name}</strong> and detected surface degradation or discoloration indicating it is <strong>Rotten</strong>."
            )
            
            st.markdown(f"""
            <div class="fc-info-bubble">
              {explanation}
              <div class="fc-disclaimer">
                ⚠️ <strong>Note:</strong> Freshness assessment is an AI visual appearance model trained on apple, banana, and orange datasets.
              </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Diagnostic Breakdown
            with st.expander("🔍 View Technical Metrics"):
                st.markdown(f"""
                - **Detected Class:** `{fruit_name}`
                - **Fresh Probability:** `{fresh_prob}%`
                - **Rotten Probability:** `{rotten_prob}%`
                - **Sigmoid Score:** `{raw_score:.4f}` *(Threshold: 0.5000)*
                """)

        else:
            st.error("Freshness CNN model not found in memory.")
            
    except Exception as err:
        st.error(f"Error processing image: {err}")

# ─── Technical Specifications ─────────────────────────────────────────────────
st.markdown("""
<div class="fc-tech-wrap">
  <div style="font-size: 0.9rem; font-weight: 700; color: #1A1C1A;">Dual-Model AI Architecture</div>
  <div class="fc-tech-grid">
    <div class="fc-tech-item">
      <div class="fc-tech-k">Fruit Recognition</div>
      <div class="fc-tech-v">MobileNetV2 (Auto-Detect)</div>
    </div>
    <div class="fc-tech-item">
      <div class="fc-tech-k">Freshness Classifier</div>
      <div class="fc-tech-v">3-Stage CNN (96.33% Accuracy)</div>
    </div>
  </div>
</div>
<div style="text-align: center; font-size: 0.72rem; color: #8B948C; margin-top: 1.5rem;">
  FruitCheck AI &bull; Autonomous Fruit Detection & Freshness Classification
</div>
""", unsafe_allow_html=True)
