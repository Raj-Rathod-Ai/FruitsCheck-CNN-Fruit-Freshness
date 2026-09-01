import streamlit as st
import numpy as np
from PIL import Image
import io
import os
import time

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="FruitCheck — AI Fruit Freshness Detector",
    page_icon="🍎",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": "https://github.com/Raj-Rathod-Ai/FruitsCheck-CNN-Fruit-Freshness",
        "About": "FruitCheck — CNN-based fruit freshness classifier. Supports Apple, Banana, and Orange."
    }
)

# ─── Custom CSS Design System ─────────────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<style>
/* === GLOBAL RESET === */
* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #F9F8F5 !important;
    color: #1A1C1A !important;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
.stDeployButton { display: none !important; }

/* Remove default padding */
[data-testid="stAppViewContainer"] > .main { padding-top: 0 !important; }
.block-container { padding: 0 1rem 4rem 1rem !important; max-width: 820px !important; }

/* Remove scrollbar flicker */
body { overflow-y: scroll; }

/* === TYPOGRAPHY === */
h1, h2, h3, h4, h5, h6, p, span, div, label {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* === BACKGROUND GRID PATTERN === */
[data-testid="stAppViewContainer"] {
    background-image: radial-gradient(#E6E4DC 1px, transparent 1px) !important;
    background-size: 24px 24px !important;
}

/* === NAVBAR === */
.fc-navbar {
    position: sticky;
    top: 0;
    z-index: 999;
    background: rgba(255,255,255,0.90);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-bottom: 1px solid #E6E4DC;
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 0 -1rem 2rem -1rem;
}
.fc-brand { display: flex; align-items: center; gap: 0.6rem; }
.fc-brand-icon { font-size: 1.5rem; }
.fc-brand-name {
    font-size: 1.2rem; font-weight: 800;
    letter-spacing: -0.02em; color: #1A1C1A;
}
.fc-brand-sub {
    font-size: 0.78rem; color: #585F59;
    padding-left: 0.75rem; border-left: 1px solid #E6E4DC;
}
.fc-status-online {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: #ECFDF5; color: #065F46;
    border: 1px solid #A7F3D0;
    padding: 0.25rem 0.75rem; border-radius: 9999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.05em;
}
.fc-status-offline {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: #F3F4F6; color: #6B7280;
    border: 1px solid #E5E7EB;
    padding: 0.25rem 0.75rem; border-radius: 9999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.05em;
}
.fc-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: currentColor; display: inline-block;
    animation: pulse-dot 2s ease-in-out infinite;
}

/* === HERO === */
.fc-hero { text-align: center; padding: 2rem 0 2.5rem 0; }
.fc-pill {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; font-weight: 600;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: #585F59; background: #F3F2EC;
    border: 1px solid #E6E4DC;
    padding: 0.2rem 0.75rem; border-radius: 9999px;
    margin-bottom: 0.85rem;
}
.fc-title {
    font-size: 2.4rem; font-weight: 800;
    letter-spacing: -0.03em; color: #1A1C1A;
    line-height: 1.1; margin-bottom: 0.75rem;
}
.fc-desc {
    font-size: 1rem; color: #585F59;
    line-height: 1.55; max-width: 560px; margin: 0 auto;
}

/* === CARD === */
.fc-card {
    background: #FFFFFF;
    border: 1px solid #E6E4DC;
    border-radius: 18px;
    padding: 1.75rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    animation: fadeIn 0.35s ease-out;
}
.fc-card-title {
    font-size: 1.05rem; font-weight: 700;
    color: #1A1C1A; margin-bottom: 0.2rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.fc-card-sub { font-size: 0.82rem; color: #8B948C; margin-bottom: 1.25rem; }
.fc-step {
    width: 1.6rem; height: 1.6rem; border-radius: 50%;
    background: #1A1C1A; color: #fff;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 700; flex-shrink: 0;
}
.fc-step-done {
    background: #059669 !important;
}

/* === FRUIT CARDS === */
.fruit-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.65rem;
    margin-bottom: 0.85rem;
}
.fruit-btn {
    background: #F9F8F5;
    border: 1.5px solid #E6E4DC;
    border-radius: 12px;
    padding: 0.75rem 0.5rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.15s ease;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.fruit-btn:hover { border-color: #1A1C1A; background: #F3F2EC; transform: translateY(-1px); }
.fruit-btn.selected {
    border-color: #1A1C1A !important;
    background: #F3F2EC !important;
    box-shadow: 0 0 0 1.5px #1A1C1A;
}
.fruit-btn-other { border-style: dashed !important; }
.fruit-btn-other:hover { border-color: #D97706 !important; border-style: solid !important; }
.fruit-emoji { font-size: 1.75rem; display: block; margin-bottom: 0.25rem; }
.fruit-name { font-size: 0.8rem; font-weight: 700; color: #1A1C1A; display: block; }
.fruit-tag { font-size: 0.62rem; color: #8B948C; font-family: 'JetBrains Mono', monospace; }
.fruit-tag-road { color: #D97706 !important; font-weight: 600; }

/* === NOTICE BOX === */
.fc-notice {
    background: #F3F2EC; border-left: 3px solid #8B948C;
    border-radius: 0 8px 8px 0;
    padding: 0.6rem 0.85rem;
    font-size: 0.8rem; color: #585F59;
    margin-top: 0.5rem;
}

/* === ROADMAP MODAL === */
.fc-modal-overlay {
    position: fixed; inset: 0; z-index: 9999;
    background: rgba(0,0,0,0.45);
    backdrop-filter: blur(5px);
    display: flex; align-items: center; justify-content: center;
    animation: fadeIn 0.2s ease-out;
}
.fc-modal {
    background: #FFFFFF; border-radius: 18px;
    border: 1px solid #E6E4DC;
    box-shadow: 0 24px 60px rgba(0,0,0,0.15);
    padding: 2rem; max-width: 440px; width: 90%;
    animation: scaleUp 0.25s cubic-bezier(0.16,1,0.3,1);
}
.fc-modal-title { font-size: 1.2rem; font-weight: 800; margin-bottom: 0.75rem; }
.fc-modal-text { font-size: 0.88rem; color: #585F59; line-height: 1.55; margin-bottom: 0.85rem; }
.fc-callout {
    background: #FEF3C7; border: 1px solid #FDE68A;
    border-radius: 10px; padding: 0.85rem;
    font-size: 0.83rem; color: #92400E;
    line-height: 1.5; margin-bottom: 0.85rem;
}
.fc-modal-sub { font-size: 0.75rem; color: #8B948C; line-height: 1.4; }

/* === IMAGE PREVIEW === */
.fc-img-wrapper {
    border-radius: 12px; overflow: hidden;
    background: #0B0F0D;
    position: relative;
    border: 1px solid #2D2D2D;
    margin-bottom: 0.75rem;
}
.fc-scanner {
    position: relative;
    overflow: hidden;
}
.fc-scanner::after {
    content: '';
    position: absolute; left: 0; right: 0; top: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, #10B981, #34D399, transparent);
    box-shadow: 0 0 12px #10B981;
    animation: scan-move 1.5s ease-in-out infinite;
}

/* === ANALYZE BUTTON === */
.stButton > button {
    width: 100% !important;
    background: #1A1C1A !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 1.5rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    letter-spacing: -0.01em !important;
}
.stButton > button:hover {
    background: #000000 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.2) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Secondary button style */
.fc-btn-secondary > button {
    background: #FFFFFF !important;
    color: #1A1C1A !important;
    border: 1px solid #E6E4DC !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
}
.fc-btn-secondary > button:hover {
    background: #F9F8F5 !important;
    border-color: #D0CEBE !important;
    transform: none !important;
    box-shadow: none !important;
}

/* === RESULT CARDS === */
.fc-result-fresh {
    background: #ECFDF5; border: 1px solid #A7F3D0;
    border-radius: 14px; padding: 1.5rem;
    animation: fadeIn 0.4s ease-out;
}
.fc-result-rotten {
    background: #FEF2F2; border: 1px solid #FECACA;
    border-radius: 14px; padding: 1.5rem;
    animation: fadeIn 0.4s ease-out;
}
.fc-result-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem; font-weight: 800;
    letter-spacing: 0.08em;
    padding: 0.3rem 0.75rem; border-radius: 9999px;
    background: #FFFFFF; border: 1px solid currentColor;
    display: inline-block; margin-bottom: 0.85rem;
}
.fresh-label { color: #059669; }
.rotten-label { color: #DC2626; }
.fc-confidence-num {
    font-size: 2.5rem; font-weight: 800;
    letter-spacing: -0.03em; color: #1A1C1A;
    line-height: 1;
}
.fc-confidence-sub { font-size: 0.82rem; color: #585F59; margin-bottom: 0.75rem; }
.fc-bar-track {
    height: 8px; border-radius: 9999px;
    background: rgba(0,0,0,0.08); overflow: hidden;
    margin-bottom: 1rem;
}
.fc-bar-fresh {
    height: 100%; border-radius: 9999px;
    background: #059669;
    transition: width 1s cubic-bezier(0.16,1,0.3,1);
}
.fc-bar-rotten {
    height: 100%; border-radius: 9999px;
    background: #DC2626;
    transition: width 1s cubic-bezier(0.16,1,0.3,1);
}
.fc-explanation {
    background: #FFFFFF; border-radius: 8px;
    padding: 0.85rem 1rem; border: 1px solid rgba(0,0,0,0.06);
    font-size: 0.85rem; color: #1A1C1A; line-height: 1.5;
    margin-bottom: 0.75rem;
}
.fc-disclaimer {
    font-size: 0.75rem; color: #8B948C;
    border-top: 1px solid rgba(0,0,0,0.06); padding-top: 0.5rem;
}
.fc-user-note {
    font-size: 0.82rem; color: #585F59;
    margin-bottom: 0.5rem;
}

/* === TECH SECTION === */
.fc-tech {
    background: #FFFFFF; border: 1px solid #E6E4DC;
    border-radius: 18px; padding: 1.5rem;
    margin-bottom: 1.25rem;
}
.fc-tech-head {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 1.1rem;
}
.fc-tech-title { font-size: 0.95rem; font-weight: 700; color: #1A1C1A; }
.fc-tech-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; color: #585F59;
    background: #F3F2EC; border: 1px solid #E6E4DC;
    padding: 0.15rem 0.5rem; border-radius: 6px;
}
.fc-tech-grid {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
}
.fc-tech-cell {
    background: #F9F8F5; border: 1px solid #E6E4DC;
    border-radius: 10px; padding: 0.75rem;
}
.fc-tech-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.63rem; font-weight: 600;
    color: #8B948C; text-transform: uppercase;
    letter-spacing: 0.04em; display: block; margin-bottom: 0.2rem;
}
.fc-tech-val { font-size: 0.85rem; font-weight: 700; color: #1A1C1A; display: block; }
.fc-tech-sub { font-size: 0.7rem; color: #585F59; display: block; }

/* === FOOTER === */
.fc-footer {
    text-align: center; font-size: 0.73rem;
    color: #8B948C; padding: 0 1rem 1rem 1rem;
    line-height: 1.5;
}

/* === DIVIDER === */
.fc-divider { height: 1px; background: #E6E4DC; margin: 1.5rem 0; }

/* === SCANNING LOADING === */
.fc-scanning-wrap {
    border-radius: 12px; overflow: hidden;
    position: relative; background: #0B0F0D;
}
.fc-scan-img { width: 100%; display: block; opacity: 0.75; }
.fc-scan-overlay {
    position: absolute; inset: 0;
    background: rgba(0,0,0,0.35);
    display: flex; flex-direction: column;
    align-items: center; justify-content: flex-end;
    padding-bottom: 1rem;
}
.fc-scan-bar {
    position: absolute; left: 0; right: 0; top: 0; height: 3px;
    background: linear-gradient(90deg, transparent 0%, #10B981 50%, transparent 100%);
    box-shadow: 0 0 14px #10B981;
    animation: scan-move 1.5s ease-in-out infinite;
}
.fc-scan-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.08em; color: #FFFFFF;
    background: rgba(0,0,0,0.75);
    border: 1px solid #10B981;
    padding: 0.3rem 0.75rem; border-radius: 9999px;
}

/* Hide Streamlit file uploader default label */
[data-testid="stFileUploader"] label { display: none !important; }
[data-testid="stFileUploader"] section {
    background: #F9F8F5 !important;
    border: 2px dashed #E6E4DC !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    transition: border-color 0.15s !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: #1A1C1A !important;
}
[data-testid="stFileUploader"] section > div {
    color: #585F59 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #059669, #10B981) !important;
    border-radius: 9999px !important;
}
.stProgress > div > div { border-radius: 9999px !important; background: rgba(0,0,0,0.08) !important; }

/* Spinner */
.stSpinner > div { border-color: #1A1C1A transparent transparent transparent !important; }

/* === KEYFRAMES === */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes scaleUp {
    from { opacity: 0; transform: scale(0.94); }
    to { opacity: 1; transform: scale(1); }
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.75); }
}
@keyframes scan-move {
    0% { top: 0%; opacity: 0.9; }
    50% { top: calc(100% - 3px); opacity: 1; }
    100% { top: 0%; opacity: 0.9; }
}
@media (prefers-reduced-motion: reduce) {
    * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
@media (max-width: 600px) {
    .fc-title { font-size: 1.75rem; }
    .fruit-grid { grid-template-columns: repeat(2, 1fr); }
    .fc-tech-grid { grid-template-columns: 1fr; }
    .fc-brand-sub { display: none; }
}
</style>
""", unsafe_allow_html=True)


# ─── Session State Init ────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "selected_fruit": None,
        "result": None,
        "show_other_modal": False,
        "analyzed": False,
        "reset": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─── Model Loading (Singleton — loads ONCE) ────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    """Load the CNN model once and cache it for all sessions."""
    import tensorflow as tf

    # Search paths: local first, then HF Hub
    search_paths = [
        os.path.join(os.path.dirname(__file__), "fruits_classification.keras"),
        os.path.join(os.path.dirname(__file__), "models", "fruits_classification.keras"),
        "fruits_classification.keras",
        os.path.join(os.path.dirname(__file__), "fruits_classification.h5"),
        "fruits_classification.h5",
    ]

    for path in search_paths:
        if os.path.exists(path):
            try:
                model = tf.keras.models.load_model(path)
                return model, "loaded", os.path.basename(path)
            except Exception as e:
                continue

    # Try Hugging Face Hub as fallback (for Streamlit Cloud)
    try:
        from huggingface_hub import hf_hub_download
        hf_model_repo = os.getenv("HF_MODEL_REPO", "Raj1908/fruitcheck-model")
        path = hf_hub_download(repo_id=hf_model_repo, filename="fruits_classification.keras")
        model = tf.keras.models.load_model(path)
        return model, "loaded", "fruits_classification.keras (HF Hub)"
    except Exception:
        pass

    return None, "unavailable", None


def preprocess_image(image_bytes: bytes):
    """Preprocess image: RGB → resize 224×224 → normalize [0,1] → batch."""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))
    arr = np.array(image).astype("float32") / 255.0
    return np.expand_dims(arr, axis=0)


def run_inference(model, image_bytes: bytes):
    """Run CNN inference and return (label, confidence, raw_score)."""
    arr = preprocess_image(image_bytes)
    prob = float(model.predict(arr, verbose=0)[0][0])
    # Verified label mapping from CNN.ipynb:
    # sigmoid < 0.5  → Fresh (classes 0-2)
    # sigmoid ≥ 0.5  → Rotten (classes 3-5)
    if prob >= 0.5:
        return "Rotten", round(prob * 100, 2), prob
    else:
        return "Fresh", round((1.0 - prob) * 100, 2), prob


# ─── Load Model ───────────────────────────────────────────────────────────────
model, model_status, model_name = load_model()
model_online = model is not None

# ─── NAVBAR ───────────────────────────────────────────────────────────────────
if model_online:
    status_html = '<span class="fc-status-online"><span class="fc-dot"></span>MODEL ONLINE</span>'
else:
    status_html = '<span class="fc-status-offline"><span class="fc-dot"></span>MODEL OFFLINE</span>'

st.markdown(f"""
<div class="fc-navbar">
  <div class="fc-brand">
    <span class="fc-brand-icon">🍏</span>
    <span class="fc-brand-name">FruitCheck</span>
    <span class="fc-brand-sub">AI-Powered Freshness Detection</span>
  </div>
  {status_html}
</div>
""", unsafe_allow_html=True)

# ─── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="fc-hero">
  <div class="fc-pill">COMPUTER VISION &bull; FRUIT QUALITY</div>
  <div class="fc-title">Freshness, detected.</div>
  <div class="fc-desc">
    Upload an image of an apple, banana, or orange and let the trained
    CNN analyze its visual freshness characteristics.
  </div>
</div>
""", unsafe_allow_html=True)

# ─── MODEL OFFLINE BANNER ─────────────────────────────────────────────────────
if not model_online:
    st.error(
        "⚠️ **Model unavailable.** Place `fruits_classification.keras` in the project root "
        "and restart the app, or set the `HF_MODEL_REPO` environment variable.",
        icon=None
    )
    st.stop()

# ─── OTHER FRUIT MODAL ────────────────────────────────────────────────────────
if st.session_state.show_other_modal:
    st.markdown("""
<div class="fc-modal-overlay">
  <div class="fc-modal">
    <div style="font-size:1.75rem;margin-bottom:0.5rem;">🍈</div>
    <div class="fc-modal-title">Training Phase Notice</div>
    <div class="fc-modal-text">
      The FruitCheck CNN is <strong>trained exclusively on Apple, Banana, and
      Orange</strong> — 6 classes total (3 fruits × Fresh/Rotten).
    </div>
    <div class="fc-callout">
      📌 Other fruit categories — <strong>Mango, Strawberry, Grapes, Watermelon,
      Pineapple, Papaya</strong> — are in the <strong>training phase roadmap</strong>.
      The current model has no feature embeddings for these fruits and will
      produce unreliable predictions for them.
    </div>
    <div class="fc-modal-sub">
      Please select Apple, Banana, or Orange for a valid classification.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
    if st.button("✕  Got it — Close", key="close_modal"):
        st.session_state.show_other_modal = False
        st.rerun()

# ─── STEP 1: FRUIT SELECTOR ───────────────────────────────────────────────────
sf = st.session_state.selected_fruit

apple_cls  = "fruit-btn selected" if sf == "apple"  else "fruit-btn"
banana_cls = "fruit-btn selected" if sf == "banana" else "fruit-btn"
orange_cls = "fruit-btn selected" if sf == "orange" else "fruit-btn"

st.markdown(f"""
<div class="fc-card">
  <div class="fc-card-title">
    <span class="fc-step">1</span> Select fruit
  </div>
  <div class="fc-card-sub">Choose the target fruit type before uploading your image</div>
  <div class="fruit-grid">
    <div class="{apple_cls}" id="btn-apple">
      <span class="fruit-emoji">🍎</span>
      <span class="fruit-name">Apple</span>
      <span class="fruit-tag">Trained Dataset</span>
    </div>
    <div class="{banana_cls}" id="btn-banana">
      <span class="fruit-emoji">🍌</span>
      <span class="fruit-name">Banana</span>
      <span class="fruit-tag">Trained Dataset</span>
    </div>
    <div class="{orange_cls}" id="btn-orange">
      <span class="fruit-emoji">🍊</span>
      <span class="fruit-name">Orange</span>
      <span class="fruit-tag">Trained Dataset</span>
    </div>
    <div class="fruit-btn fruit-btn-other" id="btn-other">
      <span class="fruit-emoji">🍉</span>
      <span class="fruit-name">Other</span>
      <span class="fruit-tag fruit-tag-road">Roadmap ↗</span>
    </div>
  </div>
  <div class="fc-notice">
    ℹ️ Currently supports <strong>Apple</strong>, <strong>Banana</strong>,
    and <strong>Orange</strong>. Other fruits are not yet trained.
  </div>
</div>
""", unsafe_allow_html=True)

# Fruit selection buttons (invisible Streamlit buttons driving the HTML above)
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🍎 Apple", key="sel_apple", use_container_width=True):
        st.session_state.selected_fruit = "apple"
        st.session_state.result = None
        st.rerun()
with col2:
    if st.button("🍌 Banana", key="sel_banana", use_container_width=True):
        st.session_state.selected_fruit = "banana"
        st.session_state.result = None
        st.rerun()
with col3:
    if st.button("🍊 Orange", key="sel_orange", use_container_width=True):
        st.session_state.selected_fruit = "orange"
        st.session_state.result = None
        st.rerun()
with col4:
    if st.button("🍉 Other", key="sel_other", use_container_width=True):
        st.session_state.show_other_modal = True
        st.rerun()

st.markdown('<div class="fc-divider"></div>', unsafe_allow_html=True)

# ─── STEP 2: IMAGE UPLOAD ─────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:0.5rem;">
  <div class="fc-card-title">
    <span class="fc-step">2</span> Upload fruit image
  </div>
  <div class="fc-card-sub" style="margin-left:2.1rem;">
    Upload a clear single-fruit photograph — JPG, JPEG, PNG (max 15 MB)
  </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    label="Upload fruit image",
    type=["jpg", "jpeg", "png", "webp"],
    key="img_upload",
    label_visibility="collapsed"
)

# ─── MAIN ANALYSIS FLOW ───────────────────────────────────────────────────────
if uploaded_file is not None:
    img_bytes = uploaded_file.getvalue()
    img_pil = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    st.markdown('<div class="fc-divider"></div>', unsafe_allow_html=True)

    # Image preview + meta
    col_img, col_meta = st.columns([1.2, 1])
    with col_img:
        if st.session_state.result is None and not st.session_state.analyzed:
            st.image(img_pil, use_container_width=True, caption="")
        else:
            # Show scanning animation while analyzing, plain image otherwise
            st.image(img_pil, use_container_width=True, caption="")

    with col_meta:
        size_kb = len(img_bytes) / 1024
        fruit_display = st.session_state.selected_fruit.capitalize() if st.session_state.selected_fruit else "None selected"
        st.markdown(f"""
<div style="padding:0.5rem 0;">
  <div style="font-size:0.82rem;color:#8B948C;font-family:'JetBrains Mono',monospace;margin-bottom:0.3rem;">FILE INFO</div>
  <div style="font-size:0.9rem;font-weight:700;color:#1A1C1A;margin-bottom:0.15rem;word-break:break-all;">{uploaded_file.name}</div>
  <div style="font-size:0.75rem;color:#8B948C;margin-bottom:1rem;">{size_kb:.1f} KB</div>
  <div style="font-size:0.82rem;color:#8B948C;font-family:'JetBrains Mono',monospace;margin-bottom:0.2rem;">SELECTED FRUIT</div>
  <div style="font-size:1rem;font-weight:800;color:#1A1C1A;">{fruit_display if st.session_state.selected_fruit else '⚠️ Not selected'}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="fc-divider"></div>', unsafe_allow_html=True)

    # ── Analyze Button ─────────────────────────────────────────────────────────
    if st.session_state.result is None:
        if not st.session_state.selected_fruit:
            st.warning("⚠️ Please select **Apple**, **Banana**, or **Orange** above before analyzing.")
        else:
            if st.button("Analyze freshness →", key="btn_analyze", use_container_width=True):
                # Scanning animation placeholder
                scan_ph = st.empty()
                scan_ph.markdown(f"""
<div class="fc-scanning-wrap" style="margin-bottom:0.75rem;">
  <div style="position:relative;overflow:hidden;border-radius:12px;">
    <div class="fc-scan-bar"></div>
    <div style="padding:2rem;text-align:center;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;font-weight:700;
                  letter-spacing:0.08em;color:#10B981;margin-bottom:0.5rem;">
        CNN INFERENCE RUNNING
      </div>
      <div style="font-size:0.8rem;color:#8B948C;">Preprocessing → Normalizing → Forward pass</div>
    </div>
    <div class="fc-scan-bar"></div>
  </div>
</div>
""", unsafe_allow_html=True)
                prog_ph = st.empty()

                # Progress bar animation
                prog = prog_ph.progress(0, text="Loading image...")
                time.sleep(0.3)
                prog.progress(25, text="Preprocessing (224×224 RGB)...")
                time.sleep(0.3)
                prog.progress(50, text="Normalizing pixel values...")
                time.sleep(0.3)
                prog.progress(75, text="Running CNN forward pass...")

                # Actual inference
                try:
                    label, confidence, raw_score = run_inference(model, img_bytes)
                    time.sleep(0.2)
                    prog.progress(100, text="Complete!")
                    time.sleep(0.3)
                    st.session_state.result = {
                        "label": label,
                        "confidence": confidence,
                        "raw_score": raw_score,
                        "fruit": st.session_state.selected_fruit.capitalize()
                    }
                except Exception as e:
                    st.error(f"Inference error: {e}")
                finally:
                    scan_ph.empty()
                    prog_ph.empty()

                st.rerun()

    # ── Result Card ────────────────────────────────────────────────────────────
    if st.session_state.result:
        r = st.session_state.result
        is_fresh = r["label"] == "Fresh"
        card_cls = "fc-result-fresh" if is_fresh else "fc-result-rotten"
        label_cls = "fresh-label" if is_fresh else "rotten-label"
        bar_cls   = "fc-bar-fresh" if is_fresh else "fc-bar-rotten"
        icon      = "🟢" if is_fresh else "🔴"
        bar_pct   = r["confidence"]
        explanation = (
            "The CNN classified this image as <strong>fresh</strong> based on visual "
            "texture and color patterns learned during training on 8,000+ fruit images."
            if is_fresh else
            "The CNN classified this image as <strong>rotten</strong> based on "
            "discoloration and surface degradation patterns learned during training."
        )

        st.markdown(f"""
<div class="{card_cls}">
  <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;margin-bottom:0.85rem;">
    <span class="fc-result-label {label_cls}">{icon} {r['label'].upper()}</span>
    <span class="fc-user-note">Analyzed fruit: <strong>{r['fruit']}</strong></span>
  </div>
  <div class="fc-confidence-num">{r['confidence']}%</div>
  <div class="fc-confidence-sub">Model confidence</div>
  <div class="fc-bar-track">
    <div class="{bar_cls}" style="width:{bar_pct}%"></div>
  </div>
  <div class="fc-explanation">
    {explanation}
    <div class="fc-disclaimer">
      ⚠️ <strong>Notice:</strong> This prediction is based on image appearance and
      is <em>not</em> a food-safety guarantee.
    </div>
  </div>
  <div style="font-size:0.75rem;color:#8B948C;">
    Raw sigmoid score: <code style="font-family:'JetBrains Mono',monospace;">{r['raw_score']:.4f}</code>
    &nbsp;·&nbsp; Threshold: 0.5 &nbsp;·&nbsp; Framework: TensorFlow / Keras
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("<div style='height:0.85rem'></div>", unsafe_allow_html=True)

        # Reset button
        st.markdown('<div class="fc-btn-secondary">', unsafe_allow_html=True)
        if st.button("🔄  Analyze another image", key="btn_reset", use_container_width=True):
            st.session_state.result = None
            st.session_state.analyzed = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ─── TECHNICAL DETAILS ────────────────────────────────────────────────────────
st.markdown("""
<div class="fc-divider"></div>
<div class="fc-tech">
  <div class="fc-tech-head">
    <span class="fc-tech-title">Technical Specifications</span>
    <span class="fc-tech-badge">TensorFlow / Keras</span>
  </div>
  <div class="fc-tech-grid">
    <div class="fc-tech-cell">
      <span class="fc-tech-label">Model Architecture</span>
      <span class="fc-tech-val">3-Stage CNN</span>
      <span class="fc-tech-sub">Conv2D × 3 → Dense(512) → Sigmoid(1)</span>
    </div>
    <div class="fc-tech-cell">
      <span class="fc-tech-label">Input Resolution</span>
      <span class="fc-tech-val">224 × 224 RGB</span>
      <span class="fc-tech-sub">Normalized to [0.0, 1.0]</span>
    </div>
    <div class="fc-tech-cell">
      <span class="fc-tech-label">Supported Classes</span>
      <span class="fc-tech-val">Apple · Banana · Orange</span>
      <span class="fc-tech-sub">Binary: Fresh vs Rotten</span>
    </div>
    <div class="fc-tech-cell">
      <span class="fc-tech-label">Model Evaluation</span>
      <span class="fc-tech-val">96.33% Test Accuracy</span>
      <span class="fc-tech-sub">Loss: 0.0917 · 2,698 test images</span>
    </div>
    <div class="fc-tech-cell">
      <span class="fc-tech-label">Training Details</span>
      <span class="fc-tech-val">13 Epochs (Early Stopped)</span>
      <span class="fc-tech-sub">Best at Epoch 10 · 96.79% val acc</span>
    </div>
    <div class="fc-tech-cell">
      <span class="fc-tech-label">Data Augmentation</span>
      <span class="fc-tech-val">Flip · Rotation · Zoom</span>
      <span class="fc-tech-sub">RandomContrast · Applied on train set</span>
    </div>
  </div>
</div>

<div class="fc-footer">
  <strong>Model Limitation:</strong> FruitCheck is trained exclusively on apples, bananas,
  and oranges. This tool performs visual image classification and should not replace
  empirical food-safety assessments.<br>
  <span style="opacity:0.6;">FruitCheck v1.0 · Built by Raj Rathod · TensorFlow 2.x</span>
</div>
""", unsafe_allow_html=True)
