import React, { useState, useEffect, useRef } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const SUPPORTED_FRUITS = [
  { id: 'apple', name: 'Apple', icon: '🍎', desc: 'Trained Dataset' },
  { id: 'banana', name: 'Banana', icon: '🍌', desc: 'Trained Dataset' },
  { id: 'orange', name: 'Orange', icon: '🍊', desc: 'Trained Dataset' },
];

export default function App() {
  const [selectedFruit, setSelectedFruit] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [apiStatus, setApiStatus] = useState({ online: false, modelReady: false, checking: true });
  const [errorMessage, setErrorMessage] = useState('');
  const [showRoadmapModal, setShowRoadmapModal] = useState(false);
  const [pendingOtherSelection, setPendingOtherSelection] = useState(false);

  const fileInputRef = useRef(null);

  // Check backend health & readiness
  useEffect(() => {
    let isMounted = true;

    async function checkBackend() {
      try {
        const healthRes = await fetch(`${API_BASE_URL}/health`, { signal: AbortSignal.timeout(4000) });
        if (healthRes.ok) {
          const readyRes = await fetch(`${API_BASE_URL}/ready`, { signal: AbortSignal.timeout(4000) });
          const readyData = readyRes.ok ? await readyRes.json() : null;
          if (isMounted) {
            setApiStatus({
              online: true,
              modelReady: Boolean(readyData?.ready),
              checking: false
            });
          }
          return;
        }
      } catch (err) {
        // Backend not reachable
      }
      if (isMounted) {
        setApiStatus({ online: false, modelReady: false, checking: false });
      }
    }

    checkBackend();
    const interval = setInterval(checkBackend, 15000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  const handleFruitSelect = (fruitId) => {
    setSelectedFruit(fruitId);
    setErrorMessage('');
  };

  const handleOtherFruitClick = () => {
    setShowRoadmapModal(true);
  };

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      validateAndSetImage(file);
    }
  };

  const validateAndSetImage = (file) => {
    setErrorMessage('');
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      setErrorMessage('Unsupported file format. Please upload a JPG, JPEG, PNG, or WebP image.');
      return;
    }
    if (file.size > 15 * 1024 * 1024) {
      setErrorMessage('File size exceeds 15 MB limit. Please choose a smaller image.');
      return;
    }

    setImageFile(file);
    const previewUrl = URL.createObjectURL(file);
    setImagePreview(previewUrl);
    setAnalysisResult(null);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) {
      validateAndSetImage(file);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFruit) {
      setErrorMessage('Please select a fruit type (Apple, Banana, or Orange) first.');
      return;
    }
    if (!imageFile) {
      setErrorMessage('Please upload a fruit image to continue.');
      return;
    }

    setErrorMessage('');
    setIsAnalyzing(true);
    setAnalysisResult(null);

    const formData = new FormData();
    formData.append('file', imageFile);
    formData.append('fruit', selectedFruit);

    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || data.detail || 'Unable to analyze image. Please try again.');
      }

      // Smooth delay for CV scan animation effect
      setTimeout(() => {
        setAnalysisResult(data);
        setIsAnalyzing(false);
      }, 1000);

    } catch (err) {
      setIsAnalyzing(false);
      setErrorMessage(err.message || 'Connection to inference server failed. Ensure the backend is active.');
    }
  };

  const handleReset = () => {
    setImageFile(null);
    if (imagePreview) {
      URL.revokeObjectURL(imagePreview);
    }
    setImagePreview(null);
    setAnalysisResult(null);
    setErrorMessage('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="app-container">
      {/* Background Decorative Pattern */}
      <div className="bg-grid-pattern" aria-hidden="true" />

      {/* Navigation Header */}
      <header className="navbar">
        <div className="nav-brand">
          <div className="brand-badge">
            <span className="brand-logo-icon">🍏</span>
            <span className="brand-name">FruitCheck</span>
          </div>
          <span className="brand-tagline">AI-Powered Freshness Detection</span>
        </div>

        <div className="nav-status">
          <div className={`status-pill ${apiStatus.online && apiStatus.modelReady ? 'status-online' : 'status-offline'}`}>
            <span className="status-dot"></span>
            <span className="status-label">
              {apiStatus.checking ? 'CHECKING BACKEND' : (apiStatus.online && apiStatus.modelReady ? 'MODEL ONLINE' : 'OFFLINE / STANDBY')}
            </span>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="main-content">
        {/* Hero Section */}
        <section className="hero-section">
          <div className="hero-pill">COMPUTER VISION • FRUIT QUALITY</div>
          <h1 className="hero-title">Freshness, detected.</h1>
          <p className="hero-description">
            Upload an image of an apple, banana, or orange and let the trained CNN model analyze its visual freshness characteristics.
          </p>
        </section>

        {/* Global Error Banner */}
        {errorMessage && (
          <div className="alert-banner alert-error" role="alert">
            <svg className="alert-icon" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <div className="alert-text">{errorMessage}</div>
            <button className="alert-close" onClick={() => setErrorMessage('')} aria-label="Dismiss alert">✕</button>
          </div>
        )}

        {/* Core Analysis Container */}
        <div className="card-container">
          {/* Step 1: Select Fruit */}
          <div className="section-block">
            <div className="section-header">
              <div className="step-number">1</div>
              <div>
                <h2 className="section-title">Select fruit</h2>
                <p className="section-subtitle">Choose the target fruit type before uploading</p>
              </div>
            </div>

            <div className="fruit-selector-grid">
              {SUPPORTED_FRUITS.map((fruit) => {
                const isSelected = selectedFruit === fruit.id;
                return (
                  <button
                    key={fruit.id}
                    type="button"
                    className={`fruit-card ${isSelected ? 'fruit-card-selected' : ''}`}
                    onClick={() => handleFruitSelect(fruit.id)}
                  >
                    <span className="fruit-card-icon">{fruit.icon}</span>
                    <div className="fruit-card-info">
                      <span className="fruit-card-name">{fruit.name}</span>
                      <span className="fruit-card-tag">{fruit.desc}</span>
                    </div>
                    {isSelected && <span className="fruit-card-check">✓</span>}
                  </button>
                );
              })}

              {/* Other Fruits Button with Informative Popup Notice */}
              <button
                type="button"
                className={`fruit-card fruit-card-other ${selectedFruit === 'other' ? 'fruit-card-selected' : ''}`}
                onClick={handleOtherFruitClick}
                title="View unlisted fruit roadmap notice"
              >
                <span className="fruit-card-icon">🍉</span>
                <div className="fruit-card-info">
                  <span className="fruit-card-name">Other Fruit</span>
                  <span className="fruit-card-tag tag-roadmap">Training Roadmap ↗</span>
                </div>
              </button>
            </div>

            <div className="fruit-constraint-notice">
              <span className="info-icon">ℹ️</span>
              <span>Currently supports <strong>Apple</strong>, <strong>Banana</strong>, and <strong>Orange</strong>. User fruit selection provides essential context for evaluation.</span>
            </div>
          </div>

          <div className="divider" />

          {/* Step 2: Upload Area */}
          <div className="section-block">
            <div className="section-header">
              <div className="step-number">2</div>
              <div>
                <h2 className="section-title">Upload fruit image</h2>
                <p className="section-subtitle">Provide a clear single-fruit photograph</p>
              </div>
            </div>

            {!imagePreview ? (
              <div
                className={`dropzone ${isDragging ? 'dropzone-active' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                tabIndex={0}
                role="button"
                aria-label="Upload fruit image"
              >
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileChange}
                  accept=".jpg,.jpeg,.png,.webp"
                  className="hidden-input"
                />
                <div className="dropzone-icon">📷</div>
                <div className="dropzone-title">Drop your image here</div>
                <div className="dropzone-subtitle">or <span className="browse-link">browse files</span> from your computer</div>
                <div className="dropzone-formats">JPG · JPEG · PNG · WEBP (Max 15MB)</div>
              </div>
            ) : (
              <div className="preview-container">
                <div className="preview-media-wrapper">
                  <img src={imagePreview} alt="Uploaded fruit preview" className="preview-image" />
                  
                  {/* Computer Vision Scanning Line Animation */}
                  {isAnalyzing && (
                    <div className="scanner-overlay">
                      <div className="scanner-line"></div>
                      <div className="scanner-grid"></div>
                      <div className="scanner-label">CNN INFERENCE RUNNING</div>
                    </div>
                  )}
                </div>

                <div className="preview-meta">
                  <div className="preview-info-row">
                    <span className="preview-filename">{imageFile?.name}</span>
                    <span className="preview-filesize">{(imageFile?.size ? (imageFile.size / 1024).toFixed(1) : 0)} KB</span>
                  </div>

                  <div className="preview-constraint-badge">
                    Selected Fruit: <strong>{selectedFruit ? selectedFruit.toUpperCase() : 'None selected'}</strong>
                  </div>

                  {!analysisResult && !isAnalyzing && (
                    <button
                      type="button"
                      className="btn-change-image"
                      onClick={handleReset}
                    >
                      Remove / Change Image
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Action Trigger */}
          {imagePreview && !analysisResult && (
            <div className="action-footer">
              <button
                type="button"
                className="btn-analyze"
                disabled={isAnalyzing}
                onClick={handleAnalyze}
              >
                {isAnalyzing ? (
                  <>
                    <span className="spinner"></span>
                    <span>Analyzing image...</span>
                  </>
                ) : (
                  <>
                    <span>Analyze freshness</span>
                    <span className="btn-arrow">→</span>
                  </>
                )}
              </button>
            </div>
          )}

          {/* Step 3: Analysis Result */}
          {analysisResult && (
            <div className="result-section">
              <div className="divider" />

              <div className="section-header">
                <div className="step-number step-done">✓</div>
                <div>
                  <h2 className="section-title">Classification Result</h2>
                  <p className="section-subtitle">Visual pattern prediction generated by Convolutional Neural Network</p>
                </div>
              </div>

              <div className={`result-card ${analysisResult.prediction === 'Fresh' ? 'result-fresh' : 'result-rotten'}`}>
                <div className="result-badge-row">
                  <span className="result-status-pill">
                    {analysisResult.prediction === 'Fresh' ? '🟢 FRESH' : '🔴 ROTTEN'}
                  </span>
                  <span className="result-user-fruit">
                    Analyzed Fruit: <strong>{analysisResult.fruit}</strong>
                  </span>
                </div>

                <div className="result-metric-display">
                  <div className="metric-value-wrap">
                    <span className="confidence-number">{analysisResult.confidence}%</span>
                    <span className="confidence-label">Model confidence</span>
                  </div>

                  <div className="confidence-bar-track">
                    <div
                      className="confidence-bar-fill"
                      style={{ width: `${analysisResult.confidence}%` }}
                    ></div>
                  </div>
                </div>

                <div className="result-explanation">
                  <p className="explanation-text">
                    {analysisResult.prediction === 'Fresh'
                      ? 'The CNN classified this image as fresh based on visual patterns and texture features learned during training.'
                      : 'The CNN classified this image as rotten based on discoloration and surface degradation patterns learned during training.'}
                  </p>
                  <p className="safety-disclaimer">
                    ⚠️ <strong>Notice:</strong> {analysisResult.disclaimer || 'This prediction is based on image appearance and is not a food-safety assessment.'}
                  </p>
                </div>

                <div className="result-footer-actions">
                  <button
                    type="button"
                    className="btn-secondary"
                    onClick={handleReset}
                  >
                    🔄 Analyze another image
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Technical Architecture Overview Card */}
        <section className="tech-section">
          <div className="tech-header">
            <h3 className="tech-heading">Technical Specifications</h3>
            <span className="tech-badge">TensorFlow / Keras</span>
          </div>

          <div className="tech-grid">
            <div className="tech-card">
              <span className="tech-label">MODEL ARCHITECTURE</span>
              <span className="tech-value">3-Stage CNN (Conv2D + MaxPool)</span>
              <span className="tech-sub">Dense(512) → Sigmoid(1)</span>
            </div>

            <div className="tech-card">
              <span className="tech-label">INPUT RESOLUTION</span>
              <span className="tech-value">224 × 224 RGB</span>
              <span className="tech-sub">Normalized [0.0, 1.0]</span>
            </div>

            <div className="tech-card">
              <span className="tech-label">SUPPORTED CLASSES</span>
              <span className="tech-value">Apple · Banana · Orange</span>
              <span className="tech-sub">Binary (Fresh vs Rotten)</span>
            </div>

            <div className="tech-card">
              <span className="tech-label">MODEL EVALUATION</span>
              <span className="tech-value">96.33% Test Accuracy</span>
              <span className="tech-sub">Loss: 0.0917 on 2,698 test images</span>
            </div>
          </div>
        </section>

        {/* Important Limitations Footer Note */}
        <footer className="footer-disclaimer">
          <p>
            <strong>Model Limitation Statement:</strong> FruitCheck is trained specifically on apples, bananas, and oranges. Predictions for unlisted fruits are unsupported.
            This tool is built for visual classification demonstration and should not replace empirical food-safety assessments.
          </p>
        </footer>
      </main>

      {/* Informative Popup / Modal for Unsupported / Roadmap Fruits */}
      {showRoadmapModal && (
        <div className="modal-backdrop" onClick={() => setShowRoadmapModal(false)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div className="modal-icon-wrap">🍈</div>
              <h3 className="modal-title">Training Phase Notice</h3>
            </div>

            <div className="modal-body">
              <p className="modal-text">
                Currently, the FruitCheck CNN model is <strong>trained exclusively on Apple, Banana, and Orange</strong> datasets (6 classes).
              </p>
              <div className="modal-callout">
                <span className="callout-icon">📌</span>
                <p>
                  Other fruit categories such as <strong>Mango, Strawberry, Grapes, Watermelon, Pineapple, and Papaya</strong> are currently in the <strong>training phase roadmap</strong>.
                </p>
              </div>
              <p className="modal-subtext">
                Analyzing an unlisted fruit with the current model will yield unpredictable results because the neural network lacks feature embeddings for those fruits.
              </p>
            </div>

            <div className="modal-actions">
              <button
                type="button"
                className="btn-modal-primary"
                onClick={() => {
                  setShowRoadmapModal(false);
                }}
              >
                Got It, Choose Supported Fruit
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
