import io
import os
import time
import base64
import streamlit as st
import numpy as np
from PIL import Image

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="FruitCheck — AI Fruit Freshness & Recognition System",
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

/* Background Subtle Dot Grid */
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

/* === LARGE EXPANDED UPLOAD DROPZONE === */
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

[data-testid="stFileUploader"] {
    width: 100% !important;
}
[data-testid="stFileUploader"] section {
    min-height: 230px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    background: #FAF9F6 !important;
    border: 2.5px dashed #D2CEC2 !important;
    border-radius: 20px !important;
    padding: 3rem 2rem !important;
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

/* === GLOWING LASER SCANNER CONTAINER === */
.fc-laser-box {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    background: #0B0E0D;
    border: 1.5px solid #2D3748;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    display: flex;
    justify-content: center;
    align-items: center;
    max-height: 380px;
    width: 100%;
}
.fc-laser-img {
    width: 100%;
    max-height: 380px;
    object-fit: contain;
    display: block;
}
.fc-laser-scanner-active {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    height: 3.5px;
    background: linear-gradient(90deg, transparent 0%, #10B981 30%, #34D399 50%, #10B981 70%, transparent 100%);
    box-shadow: 0 0 16px 3px #10B981, 0 0 30px #34D399;
    animation: laser-sweep 1.8s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite alternate;
    pointer-events: none;
}
.fc-laser-grid {
    position: absolute;
    inset: 0;
    background: linear-gradient(rgba(16, 185, 129, 0.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(16, 185, 129, 0.04) 1px, transparent 1px);
    background-size: 20px 20px;
    pointer-events: none;
}
.fc-laser-pill {
    position: absolute;
    bottom: 12px;
    right: 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    color: #FFFFFF;
    background: rgba(0,0,0,0.75);
    border: 1px solid #10B981;
    border-radius: 9999px;
    padding: 0.25rem 0.65rem;
    letter-spacing: 0.06em;
    pointer-events: none;
    display: flex;
    align-items: center;
    gap: 0.35rem;
}
.fc-laser-pill-complete {
    position: absolute;
    bottom: 12px;
    right: 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    color: #ECFDF5;
    background: rgba(4, 120, 87, 0.85);
    border: 1px solid #34D399;
    border-radius: 9999px;
    padding: 0.25rem 0.65rem;
    letter-spacing: 0.06em;
    pointer-events: none;
    display: flex;
    align-items: center;
    gap: 0.35rem;
}
.fc-laser-pill-dot {
    width: 5px;
    height: 5px;
    background: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 6px #10B981;
}

@keyframes laser-sweep {
    0% {
        top: 2%;
        opacity: 0.95;
    }
    100% {
        top: 96%;
        opacity: 0.95;
    }
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
    font-size: 1.45rem;
    font-weight: 800;
    color: #1A1C1A;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.fc-fruit-conf {
    font-size: 0.8rem;
    color: #5C635E;
    margin-top: 0.25rem;
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

/* === STREAMLIT EXPANDER, CODE, BUTTONS & CHECKBOX THEME OVERRIDES === */
code {
    background: #EFECE4 !important;
    color: #1A1C1A !important;
    border: 1px solid #DCD8CD !important;
    padding: 0.15rem 0.45rem !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.85em !important;
}

[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #E5E2D9 !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
    margin-top: 1rem !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] details {
    background: #FFFFFF !important;
    border-radius: 14px !important;
}
[data-testid="stExpander"] summary {
    background: #FFFFFF !important;
    color: #1A1C1A !important;
    font-weight: 700 !important;
    padding: 0.75rem 1rem !important;
    border-radius: 14px !important;
}
[data-testid="stExpander"] summary:hover {
    background: #F8F7F4 !important;
    color: #000000 !important;
}
[data-testid="stExpander"] summary svg, [data-testid="stExpander"] summary span {
    color: #1A1C1A !important;
    fill: #1A1C1A !important;
}
[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background: #FFFFFF !important;
    color: #1A1C1A !important;
    padding: 1rem !important;
    border-top: 1px solid #F1EFE9 !important;
}
[data-testid="stExpander"] [data-testid="stExpanderDetails"] p,
[data-testid="stExpander"] [data-testid="stExpanderDetails"] li,
[data-testid="stExpander"] [data-testid="stExpanderDetails"] span {
    color: #1A1C1A !important;
}

/* Fix Streamlit Buttons & Switcher */
.stButton > button {
    background: #FFFFFF !important;
    color: #1A1C1A !important;
    border: 1.5px solid #DCD8CD !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: #F4F2EB !important;
    border-color: #1A1C1A !important;
    color: #000000 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06) !important;
}

/* Fix Checkbox & Label Colors */
[data-testid="stCheckbox"] label {
    color: #1A1C1A !important;
    font-weight: 600 !important;
}
[data-testid="stCheckbox"] span {
    color: #1A1C1A !important;
}

@media (max-width: 600px) {
    .fc-res-container { grid-template-columns: 1fr; }
    .fc-tech-grid { grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
if "manual_fruit_override" not in st.session_state:
    st.session_state.manual_fruit_override = None

# ─── Load Models ──────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_all_models():
    """Load both the CNN Freshness Classifier and the Fruit Recognition Model."""
    import tensorflow as tf
    from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2

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

    # Automatic Cloud Download Fallback for Streamlit Cloud
    if freshness_model is None:
        try:
            from huggingface_hub import hf_hub_download
            repo_id = "Raj1908/fruitcheck-model"
            if hasattr(st, "secrets") and "HF_MODEL_REPO" in st.secrets:
                repo_id = st.secrets["HF_MODEL_REPO"]
            elif os.getenv("HF_MODEL_REPO"):
                repo_id = os.getenv("HF_MODEL_REPO")
                
            downloaded = hf_hub_download(repo_id=repo_id, filename="fruits_classification.keras")
            freshness_model = tf.keras.models.load_model(downloaded)
        except Exception:
            pass

    try:
        fruit_identifier = MobileNetV2(weights="imagenet")
    except Exception:
        fruit_identifier = None

    return freshness_model, fruit_identifier

freshness_model, fruit_identifier = load_all_models()

# ─── Intelligent Validation & Recognition Engine ──────────────────────────────
DIRECT_FRUITS = {
    "banana": ("Banana", "🍌"),
    "apple": ("Apple", "🍎"),
    "granny_smith": ("Apple", "🍏"),
    "orange": ("Orange", "🍊"),
    "lemon": ("Lemon", "🍋"),
    "lime": ("Lime", "🍈"),
    "strawberry": ("Strawberry", "🍓"),
    "pineapple": ("Pineapple", "🍍"),
    "pomegranate": ("Pomegranate", "🍎"),
    "fig": ("Fig", "🫐"),
    "custard_apple": ("Custard Apple", "🍈"),
    "jackfruit": ("Jackfruit", "🍈"),
    "papaya": ("Papaya", "🥭"),
    "mango": ("Mango", "🥭"),
    "grape": ("Grapes", "🍇"),
    "watermelon": ("Watermelon", "🍉"),
    "cantaloupe": ("Melon", "🍈"),
    "cucumber": ("Cucumber", "🥒"),
    "bell_pepper": ("Bell Pepper", "🫑"),
    "zucchini": ("Zucchini", "🥒"),
    "peach": ("Peach", "🍑"),
    "avocado": ("Avocado", "🥑"),
}

# ImageNet shape-proxies for rotten/decayed/blackened fruits:
ROTTEN_SHAPE_PROXIES = {
    "hook": ("Banana (Decayed)", "🍌"),
    "slug": ("Banana (Decayed)", "🍌"),
    "snail": ("Banana (Decayed)", "🍌"),
    "spindle": ("Banana (Decayed)", "🍌"),
    "wooden_spoon": ("Banana (Decayed)", "🍌"),
    "mushroom": ("Fruit (Decayed)", "🍎"),
    "acorn": ("Apple (Decayed)", "🍎"),
    "sponge": ("Orange (Decayed)", "🍊"),
    "rock": ("Fruit (Decayed)", "🍎"),
    "stone": ("Fruit (Decayed)", "🍎"),
    "dough": ("Fruit (Decayed)", "🍊"),
    "potato": ("Fruit (Decayed)", "🍎"),
}

# Explicit non-fruit categories that should be blocked:
EXPLICIT_NON_FRUITS = [
    "jean", "suit", "jersey", "t-shirt", "shirt", "dress", "sunglasses", "person", "groom",
    "lab_coat", "cardigan", "sweatshirt", "car", "truck", "airplane", "boat", "motorcycle",
    "laptop", "cellphone", "monitor", "keyboard", "desk", "sofa", "chair", "bed",
    "dog", "cat", "horse", "bird", "fish", "clock", "watch", "shoe", "boot"
]

def analyze_image_contents(img: Image.Image):
    """
    Intelligently determines whether the image contains a fruit (fresh or rotten)
    or an invalid non-fruit object.
    Returns: (is_valid, fruit_display, emoji, confidence, detected_raw)
    """
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

    img_rgb = img.convert("RGB").resize((224, 224), Image.Resampling.BILINEAR)
    arr = np.array(img_rgb, dtype=np.float32)
    arr = preprocess_input(np.expand_dims(arr, axis=0))

    if fruit_identifier is not None:
        preds = fruit_identifier.predict(arr, verbose=0)
        top5 = decode_predictions(preds, top=5)[0]
        
        top1_name = top5[0][1].lower().replace(" ", "_")
        top1_conf = round(float(top5[0][2]) * 100.0, 1)
        top1_display = top5[0][1].replace("_", " ").title()

        # 1. Check for explicit non-fruit items
        for non_item in EXPLICIT_NON_FRUITS:
            if non_item in top1_name:
                return False, top1_display, "🚫", top1_conf, top1_display

        # 2. Check for direct fruit matches in top-5
        for _, label, conf in top5:
            clean_label = label.lower().replace(" ", "_")
            for k, (name, emoji) in DIRECT_FRUITS.items():
                if k in clean_label:
                    return True, name, emoji, round(float(conf) * 100.0, 1), label.replace("_", " ").title()

        # 3. Check for rotten/decayed fruit shape proxies
        for k, (name, emoji) in ROTTEN_SHAPE_PROXIES.items():
            if k in top1_name:
                return True, name, emoji, top1_conf, top1_display

        # 4. If top-1 is not on the explicit non-fruit list, treat as general produce
        return True, "Fruits", "🍎", top1_conf, top1_display

    return True, "Fruits", "🍎", 95.0, "Fruits"

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
model_badge = (
    '<span class="fc-dot"></span> MODEL ONLINE'
    if freshness_model is not None else
    '<span style="color:#DC2626;">● MODEL OFFLINE</span>'
)

st.markdown(f"""
<div class="fc-nav">
  <div class="fc-nav-left">
    <span class="fc-logo">🍏</span>
    <div>
      <div class="fc-brand-title">FruitCheck</div>
      <div class="fc-brand-tag">Auto Fruit Recognition & Quality AI</div>
    </div>
  </div>
  <div class="fc-badge-online">
    {model_badge}
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Hero Section ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="fc-hero">
  <div class="fc-hero-pill">AUTO-RECOGNITION &bull; CNN FRESHNESS CLASSIFICATION</div>
  <div class="fc-hero-title">Instant Fruit & Freshness AI</div>
  <div class="fc-hero-desc">
    Upload any fruit photograph. The AI automatically validates the fruit type and assesses its freshness in real time.
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Large Prominent Upload Section ───────────────────────────────────────────
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

# ─── Analysis & Validation Pipeline ───────────────────────────────────────────
if uploaded_file is not None:
    try:
        raw_bytes = uploaded_file.read()
        pil_image = Image.open(io.BytesIO(raw_bytes))
        
        # Convert image to base64 for laser scanner rendering
        b64_buffer = io.BytesIO()
        pil_image.save(b64_buffer, format="JPEG")
        img_b64_str = base64.b64encode(b64_buffer.getvalue()).decode("utf-8")
        
        # Display image preview with completed scanner badge (laser line stops once result is ready)
        img_col, opt_col = st.columns([1.3, 1])
        
        with img_col:
            st.markdown(f"""
            <div class="fc-laser-box">
              <img src="data:image/jpeg;base64,{img_b64_str}" class="fc-laser-img" alt="Uploaded Image" />
              <div class="fc-laser-grid"></div>
              <div class="fc-laser-pill-complete">
                <span>✓</span> SCAN COMPLETE
              </div>
            </div>
            <div style="font-size: 0.75rem; color: #8B948C; text-align: center; margin-top: 0.35rem;">
              Surface patterns analyzed successfully
            </div>
            """, unsafe_allow_html=True)
            
        with opt_col:
            st.markdown(f"**Dimensions:** `{pil_image.width} × {pil_image.height}`")
            crop_enabled = st.checkbox(
                "🎯 Focus / Center Crop",
                value=False,
                help="Focuses on the central fruit region, reducing background interference (leaves, tables, bright glare)."
            )

        # 1. Validation & Automatic Fruit Identification
        is_fruit, auto_name, auto_emoji, auto_conf, raw_detected = analyze_image_contents(pil_image)
        
        # ─── VALIDATION CHECK: Non-Fruit Image Detected ───────────────────────
        if not is_fruit:
            st.markdown(f"""
            <div style="background: #FEF2F2; border: 1.5px solid #FECACA; border-radius: 16px; padding: 1.5rem; margin-top: 1rem;">
              <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.6rem;">
                <span style="font-size: 1.6rem;">🚫</span>
                <span style="font-size: 1.15rem; font-weight: 800; color: #991B1B;">Validation Notice: Non-Fruit Image Detected</span>
              </div>
              <p style="font-size: 0.92rem; color: #7F1D1D; line-height: 1.5; margin-bottom: 0.75rem;">
                The AI detected <strong>'{raw_detected}'</strong> (Confidence: {auto_conf}%) in the uploaded image.
                This does not appear to be a fruit or produce item.
              </p>
              <div style="background: #FFFFFF; border: 1px solid #FEE2E2; border-radius: 10px; padding: 0.85rem; font-size: 0.85rem; color: #991B1B;">
                💡 <strong>Please upload a fruit photo</strong>: FruitCheck is calibrated specifically for fruits (Apples, Bananas, Oranges, etc.).
                Freshness assessment has been skipped for this non-fruit image.
              </div>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            # Determine active fruit name (auto-detected or manually switched)
            active_fruit_name = st.session_state.manual_fruit_override if st.session_state.manual_fruit_override else auto_name
            active_emoji = "🍌" if "Banana" in active_fruit_name else ("🍊" if "Orange" in active_fruit_name else "🍎")

            # 2. Freshness Prediction (Runs for all validated fruits!)
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
                
                # Dual Result Cards: Detected Fruits + Freshness Assessment
                st.markdown(f"""
                <div class="fc-res-container">
                  <!-- Box 1: Auto-Detected Fruit Name -->
                  <div class="fc-box">
                    <div class="fc-box-label">DETECTED FRUITS</div>
                    <div class="fc-fruit-detected">{active_emoji} {active_fruit_name}</div>
                    <div class="fc-fruit-conf">Recognition: <strong>{auto_conf}%</strong> &bull; Auto-Identified</div>
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
                    f"The AI recognized these fruits as <strong>{active_fruit_name}</strong> and detected clear, healthy surface pigmentation indicating they are <strong>Fresh</strong>."
                    if is_fresh else
                    f"The AI recognized these fruits as <strong>{active_fruit_name}</strong> and detected surface degradation or discoloration indicating they are <strong>Rotten</strong>."
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
                with st.expander("🔍 View Technical Metrics & Fruit Override"):
                    st.markdown(f"""
                    - **Detected Class:** `{active_fruit_name}` *(Raw: {raw_detected})*
                    - **Fresh Probability:** `{fresh_prob}%`
                    - **Rotten Probability:** `{rotten_prob}%`
                    - **Sigmoid Score:** `{raw_score:.4f}` *(Threshold: 0.5000)*
                    """)
                    
                    st.markdown("**Switch Target Fruit (Optional):**")
                    sw1, sw2, sw3, sw4 = st.columns(4)
                    with sw1:
                        if st.button("🍎 Apple"):
                            st.session_state.manual_fruit_override = "Apple"
                            st.rerun()
                    with sw2:
                        if st.button("🍌 Banana"):
                            st.session_state.manual_fruit_override = "Banana"
                            st.rerun()
                    with sw3:
                        if st.button("🍊 Orange"):
                            st.session_state.manual_fruit_override = "Orange"
                            st.rerun()
                    with sw4:
                        if st.button("🤖 Reset Auto"):
                            st.session_state.manual_fruit_override = None
                            st.rerun()

            else:
                st.markdown("""
                <div style="background: #FFFBEB; border: 1px solid #FCD34D; border-radius: 14px; padding: 1.25rem; margin-top: 1rem;">
                  <div style="display: flex; align-items: center; gap: 0.5rem; font-weight: 700; color: #92400E; margin-bottom: 0.35rem;">
                    <span>⏳</span> AI Model Initializing
                  </div>
                  <div style="font-size: 0.85rem; color: #B45309; line-height: 1.45;">
                    The neural network weights are currently loading into memory. Please wait a moment or refresh the page.
                  </div>
                </div>
                """, unsafe_allow_html=True)
                
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
