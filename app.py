import io
import os
import streamlit as st
import numpy as np
from PIL import Image

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="FruitCheck — AI Fruit Freshness Detector",
    page_icon="🍏",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Premium Modern CSS (Zero Layout Glitches, No Text Overlap) ───────────────
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

/* Remove default Streamlit chrome */
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
    max-width: 520px;
    margin: 0 auto;
}

/* === CARD CONTAINER === */
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
    width: 1.6rem;
    height: 1.6rem;
    border-radius: 50%;
    background: #1A1C1A;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    flex-shrink: 0;
}
.fc-step-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #1A1C1A;
}
.fc-step-sub {
    font-size: 0.8rem;
    color: #717871;
    margin-top: 0.1rem;
}

/* Streamlit Button Customization */
.stButton > button {
    border-radius: 12px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    transition: all 0.15s ease !important;
    border: 1px solid #E2DFD6 !important;
    padding: 0.6rem 1rem !important;
}

/* Primary Action Button */
.fc-btn-primary button {
    background: #1A1C1A !important;
    color: #FFFFFF !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.5rem !important;
    width: 100% !important;
    border: none !important;
}
.fc-btn-primary button:hover {
    background: #000000 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.15) !important;
}

/* Fruit Selector Button Styles */
.fc-fruit-active button {
    background: #1A1C1A !important;
    color: #FFFFFF !important;
    border-color: #1A1C1A !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
}
.fc-fruit-inactive button {
    background: #F8F7F4 !important;
    color: #1A1C1A !important;
    border-color: #E2DFD6 !important;
}
.fc-fruit-inactive button:hover {
    background: #EFECE4 !important;
    border-color: #CFCBC0 !important;
}
.fc-fruit-other button {
    background: #FFFBEB !important;
    color: #B45309 !important;
    border: 1px dashed #FCD34D !important;
}
.fc-fruit-other button:hover {
    background: #FEF3C7 !important;
    border-color: #F59E0B !important;
}

/* Result Cards */
.fc-result-card {
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1rem;
    border: 1px solid;
    animation: fadeIn 0.25s ease-out;
}
.fc-result-fresh {
    background: #F0FDF4;
    border-color: #BBF7D0;
}
.fc-result-rotten {
    background: #FEF2F2;
    border-color: #FECACA;
}
.fc-result-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.75rem;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.fc-pill-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    padding: 0.3rem 0.75rem;
    border-radius: 9999px;
    background: #FFFFFF;
    border: 1px solid currentColor;
}
.pill-fresh { color: #059669; border-color: #A7F3D0; }
.pill-rotten { color: #DC2626; border-color: #FECACA; }

.fc-big-score {
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #1A1C1A;
    line-height: 1;
    margin-bottom: 0.25rem;
}
.fc-score-desc {
    font-size: 0.82rem;
    color: #5C635E;
    font-weight: 500;
    margin-bottom: 0.85rem;
}

.fc-meter-bg {
    height: 10px;
    background: rgba(0,0,0,0.06);
    border-radius: 9999px;
    overflow: hidden;
    margin-bottom: 1rem;
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
    margin-bottom: 0.75rem;
}
.fc-disclaimer {
    font-size: 0.75rem;
    color: #717871;
    border-top: 1px solid rgba(0,0,0,0.06);
    padding-top: 0.5rem;
    margin-top: 0.5rem;
}

/* Callout Note */
.fc-notice-box {
    background: #F4F2EC;
    border-left: 3px solid #717871;
    border-radius: 0 8px 8px 0;
    padding: 0.55rem 0.8rem;
    font-size: 0.8rem;
    color: #5C635E;
    margin-top: 0.75rem;
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

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(4px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# ─── Session State Initialization ─────────────────────────────────────────────
if "fruit" not in st.session_state:
    st.session_state.fruit = "apple"
if "crop_mode" not in st.session_state:
    st.session_state.crop_mode = False
if "roadmap_popup" not in st.session_state:
    st.session_state.roadmap_popup = False

# ─── Model Loading (Cached Singleton) ──────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_model():
    """Load TensorFlow model once into memory."""
    import tensorflow as tf
    candidate_paths = [
        os.path.join(os.path.dirname(__file__), "fruits_classification.keras"),
        "fruits_classification.keras",
        os.path.join(os.path.dirname(__file__), "fruits_classification.h5"),
        "fruits_classification.h5",
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            try:
                m = tf.keras.models.load_model(path)
                return m, os.path.basename(path)
            except Exception:
                continue
    return None, None

model, model_filename = get_model()

# ─── Preprocessing & Inference (Fast & Clean) ───────────────────────────────────
def preprocess(img: Image.Image, auto_center_crop: bool = False) -> np.ndarray:
    """Prepare PIL image for 224x224x3 CNN."""
    img = img.convert("RGB")
    
    if auto_center_crop:
        # Crop square from center to focus on the fruit (removes wide background borders)
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) / 2
        top = (h - min_dim) / 2
        right = (w + min_dim) / 2
        bottom = (h + min_dim) / 2
        img = img.crop((left, top, right, bottom))
        
    img = img.resize((224, 224), Image.Resampling.BILINEAR)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)

def predict_freshness(img: Image.Image, auto_center_crop: bool = False):
    """Run model prediction with verified label threshold."""
    tensor = preprocess(img, auto_center_crop)
    raw = float(model.predict(tensor, verbose=0)[0][0])
    
    # Exact mapping from CNN.ipynb:
    # 0 -> Fresh (freshapples, freshbanana, freshoranges)
    # 1 -> Rotten (rottenapples, rottenbanana, rottenoranges)
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
st.markdown(f"""
<div class="fc-nav">
  <div class="fc-nav-left">
    <span class="fc-logo">🍏</span>
    <div>
      <div class="fc-brand-title">FruitCheck</div>
      <div class="fc-brand-tag">AI Fruit Quality Assessment</div>
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
  <div class="fc-hero-pill">COMPUTER VISION &bull; CONVOLUTIONAL NEURAL NET</div>
  <div class="fc-hero-title">Freshness, detected.</div>
  <div class="fc-hero-desc">
    Upload an image of an apple, banana, or orange to inspect visual surface features and classify freshness with high precision.
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Training Roadmap Modal / Notification ────────────────────────────────────
if st.session_state.roadmap_popup:
    st.warning("""
    **📌 Training Phase Notice: Unsupported Fruits**
    
    The FruitCheck CNN is **trained exclusively on Apple, Banana, and Orange** datasets.
    
    Other fruits such as **Mango, Strawberry, Grapes, Watermelon, Pineapple, and Papaya** are currently in the **training phase roadmap**. Analyzing unlisted fruits will yield inaccurate predictions because the model lacks their visual feature maps.
    """)
    if st.button("✕ Dismiss Notice"):
        st.session_state.roadmap_popup = False
        st.rerun()

# ─── Step 1: Fruit Selection ──────────────────────────────────────────────────
st.markdown("""
<div class="fc-card">
  <div class="fc-card-header">
    <div class="fc-step-badge">1</div>
    <div>
      <div class="fc-step-title">Select Target Fruit</div>
      <div class="fc-step-sub">Select the fruit category corresponding to your image</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

f_col1, f_col2, f_col3, f_col4 = st.columns(4)

with f_col1:
    apple_style = "fc-fruit-active" if st.session_state.fruit == "apple" else "fc-fruit-inactive"
    st.markdown(f'<div class="{apple_style}">', unsafe_allow_html=True)
    if st.button("🍎 Apple", use_container_width=True):
        st.session_state.fruit = "apple"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with f_col2:
    banana_style = "fc-fruit-active" if st.session_state.fruit == "banana" else "fc-fruit-inactive"
    st.markdown(f'<div class="{banana_style}">', unsafe_allow_html=True)
    if st.button("🍌 Banana", use_container_width=True):
        st.session_state.fruit = "banana"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with f_col3:
    orange_style = "fc-fruit-active" if st.session_state.fruit == "orange" else "fc-fruit-inactive"
    st.markdown(f'<div class="{orange_style}">', unsafe_allow_html=True)
    if st.button("🍊 Orange", use_container_width=True):
        st.session_state.fruit = "orange"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with f_col4:
    st.markdown('<div class="fc-fruit-other">', unsafe_allow_html=True)
    if st.button("🍉 Other ↗", use_container_width=True):
        st.session_state.roadmap_popup = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="fc-notice-box">
  Selected Fruit: <strong>{st.session_state.fruit.capitalize()}</strong> &bull; Supported dataset classes: Apple, Banana, Orange.
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

# ─── Step 2: Upload Image ─────────────────────────────────────────────────────
st.markdown("""
<div class="fc-card">
  <div class="fc-card-header">
    <div class="fc-step-badge">2</div>
    <div>
      <div class="fc-step-title">Upload Fruit Image</div>
      <div class="fc-step-sub">Select or drag-and-drop a JPG, JPEG, or PNG photograph</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload image",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed"
)

# ─── Live Analysis & Diagnostic Results ───────────────────────────────────────
if uploaded_file is not None:
    try:
        raw_bytes = uploaded_file.read()
        pil_image = Image.open(io.BytesIO(raw_bytes))
        
        # Image Display & Crop Setting
        img_col, opt_col = st.columns([1.4, 1])
        
        with img_col:
            st.image(pil_image, caption=f"Uploaded: {uploaded_file.name}", use_container_width=True)
            
        with opt_col:
            st.markdown(f"**Image Dimensions:** `{pil_image.width} × {pil_image.height}`")
            st.markdown(f"**Selected Fruit:** `{st.session_state.fruit.capitalize()}`")
            
            # Smart Center-Crop Option (helps remove wide background leaves/branches)
            crop_checked = st.checkbox(
                "🎯 Focus / Center Crop",
                value=st.session_state.crop_mode,
                help="Crops the center square of the image to focus on the fruit and reduce background influence (e.g., leaves, tables, sunlight)."
            )
            if crop_checked != st.session_state.crop_mode:
                st.session_state.crop_mode = crop_checked
                st.rerun()

        # Instant Inference (No Artificial Lag!)
        if model is not None:
            label, confidence, raw_score, fresh_prob, rotten_prob = predict_freshness(
                pil_image,
                auto_center_crop=st.session_state.crop_mode
            )
            
            is_fresh = label == "Fresh"
            card_class = "fc-result-fresh" if is_fresh else "fc-result-rotten"
            pill_class = "pill-fresh" if is_fresh else "pill-rotten"
            fill_class = "fc-meter-fill-fresh" if is_fresh else "fc-meter-fill-rotten"
            icon = "🟢" if is_fresh else "🔴"
            
            explanation = (
                f"The CNN model detected smooth surface textures and natural skin coloration characteristic of a <strong>fresh {st.session_state.fruit}</strong>."
                if is_fresh else
                f"The CNN model detected surface discoloration, spotting, or degradation patterns characteristic of a <strong>decayed/rotten {st.session_state.fruit}</strong>."
            )
            
            st.markdown(f"""
            <div class="fc-result-card {card_class}">
              <div class="fc-result-top">
                <span class="fc-pill-badge {pill_class}">{icon} {label.upper()}</span>
                <span style="font-size:0.85rem; color:#5C635E;">Target: <strong>{st.session_state.fruit.capitalize()}</strong></span>
              </div>
              
              <div class="fc-big-score">{confidence}%</div>
              <div class="fc-score-desc">Model Confidence Score</div>
              
              <div class="fc-meter-bg">
                <div class="{fill_class}" style="width: {confidence}%;"></div>
              </div>
              
              <div class="fc-info-bubble">
                {explanation}
                <div class="fc-disclaimer">
                  ⚠️ <strong>Disclaimer:</strong> This is a visual pattern classification prediction and should not be used as an empirical food safety guarantee.
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Diagnostic Probability Breakdown
            with st.expander("🔍 View Detailed Probability Breakdown & Sigmoid Metrics"):
                st.markdown(f"""
                - **Fresh Probability:** `{fresh_prob}%`
                - **Rotten Probability:** `{rotten_prob}%`
                - **Raw Sigmoid Activation:** `{raw_score:.4f}` *(Threshold: 0.5000)*
                - **Interpretation:** Scores `< 0.50` indicate Fresh; scores `≥ 0.50` indicate Rotten.
                - **Tip:** If your fruit image contains prominent non-fruit objects (such as tree branches or thick green leaves), enable the **Focus / Center Crop** option above to concentrate the CNN receptive field on the fruit body.
                """)

        else:
            st.error("⚠️ Model file could not be loaded into memory.")
            
    except Exception as err:
        st.error(f"Unable to process image: {err}")

# ─── Technical Specifications ─────────────────────────────────────────────────
st.markdown("""
<div class="fc-tech-wrap">
  <div style="font-size: 0.9rem; font-weight: 700; color: #1A1C1A;">Technical Architecture</div>
  <div class="fc-tech-grid">
    <div class="fc-tech-item">
      <div class="fc-tech-k">Architecture</div>
      <div class="fc-tech-v">3-Stage CNN + Dense(512)</div>
    </div>
    <div class="fc-tech-item">
      <div class="fc-tech-k">Input Resolution</div>
      <div class="fc-tech-v">224 × 224 RGB (Normalized)</div>
    </div>
    <div class="fc-tech-item">
      <div class="fc-tech-k">Validation Accuracy</div>
      <div class="fc-tech-v">96.79% (Best Checkpoint)</div>
    </div>
    <div class="fc-tech-item">
      <div class="fc-tech-k">Test Accuracy</div>
      <div class="fc-tech-v">96.33% (2,698 Images)</div>
    </div>
  </div>
</div>
<div style="text-align: center; font-size: 0.72rem; color: #8B948C; margin-top: 1.5rem;">
  FruitCheck AI &bull; Powered by TensorFlow & Keras &bull; Built by Raj Rathod
</div>
""", unsafe_allow_html=True)
