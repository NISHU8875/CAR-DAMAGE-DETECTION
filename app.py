import os
import streamlit as st
from prediction import predict

# Page configuration
st.set_page_config(
    page_title="Vehicle Damage Detection",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for stunning design
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
        background-attachment: fixed;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Container styling */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    /* Hero Header */
    .hero-header {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 24px;
        padding: 3rem 2.5rem;
        margin-bottom: 3rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        border: 2px solid rgba(126, 34, 206, 0.2);
        text-align: center;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #1e3c72 0%, #7e22ce 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.75rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #64748b;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    /* Upload Section */
    .upload-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 24px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.12);
        border: 2px solid rgba(126, 34, 206, 0.15);
        animation: fadeInUp 0.8s ease-out;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    /* File Uploader Styling */
    div[data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 3px dashed #94a3b8;
        border-radius: 20px;
        padding: 2.5rem 2rem;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stFileUploader"]:hover {
        border-color: #7e22ce;
        background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(126, 34, 206, 0.15);
    }
    
    div[data-testid="stFileUploader"] label {
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        color: #1e293b !important;
    }
    
    div[data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #1e3c72 0%, #7e22ce 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.85rem 2rem !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 20px rgba(126, 34, 206, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stFileUploader"] button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 30px rgba(126, 34, 206, 0.4) !important;
    }
    
    /* Image Card Container */
    .image-card {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
        border: 2px solid rgba(126, 34, 206, 0.12);
        animation: fadeInScale 0.6s ease-out;
        transition: all 0.3s ease;
    }
    
    .image-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 60px rgba(126, 34, 206, 0.2);
    }
    
    /* Image container */
    div[data-testid="stImage"] {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        border: 2px solid #e2e8f0;
    }
    
    div[data-testid="stImage"] img {
        transition: transform 0.3s ease;
    }
    
    div[data-testid="stImage"]:hover img {
        transform: scale(1.02);
    }
    
    /* Info/Alert boxes */
    .stAlert {
        border-radius: 16px !important;
        border: none !important;
        padding: 1.5rem 1.75rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08) !important;
        animation: slideInUp 0.5s ease-out !important;
    }
    
    /* Info box (prediction result) */
    div[data-baseweb="notification"] {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        border-left: 5px solid #3b82f6 !important;
    }
    
    /* Error box */
    .stAlert[data-baseweb="notification"][kind="error"] {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%) !important;
        border-left: 5px solid #ef4444 !important;
    }
    
    /* Caption/Footer */
    .caption-box {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-top: 3rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 2px solid rgba(126, 34, 206, 0.12);
        animation: fadeIn 1s ease-out;
    }
    
    .caption-text {
        color: #64748b;
        font-size: 0.95rem;
        font-weight: 500;
        margin: 0;
    }
    
    /* Custom badge */
    .damage-badge {
        display: inline-block;
        padding: 0.5rem 1.25rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.95rem;
        margin-top: 1rem;
        animation: pulse 2s infinite;
    }
    
    .damage-detected {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        border: 2px solid #fbbf24;
    }
    
    .no-damage {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        border: 2px solid #10b981;
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 2px solid rgba(126, 34, 206, 0.1);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(126, 34, 206, 0.15);
        border-color: rgba(126, 34, 206, 0.3);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
    }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 500;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInScale {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.8;
        }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem !important;
        }
        
        .hero-subtitle {
            font-size: 1rem !important;
        }
        
        .section-title {
            font-size: 1.3rem !important;
        }
        
        .hero-header {
            padding: 2rem 1.5rem !important;
        }
        
        .upload-container,
        .image-card {
            padding: 1.5rem !important;
        }
        
        div[data-testid="stFileUploader"] {
            padding: 2rem 1.5rem !important;
        }
    }
    
    @media (max-width: 480px) {
        .hero-title {
            font-size: 1.75rem !important;
        }
        
        .block-container {
            padding-top: 2rem !important;
        }
        
        .feature-card {
            padding: 1.25rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Hero Header
st.markdown("""
    <div class="hero-header">
        <div class="hero-title">🚗 Vehicle Damage Detection</div>
        <div class="hero-subtitle">AI-Powered Damage Analysis • Upload Images for Instant Assessment</div>
    </div>
""", unsafe_allow_html=True)

# Feature Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Instant Analysis</div>
            <div class="feature-desc">Fast AI processing</div>
        </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">High Accuracy</div>
            <div class="feature-desc">Advanced detection</div>
        </div>
    """, unsafe_allow_html=True)
    
with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📸</div>
            <div class="feature-title">Multi-Image</div>
            <div class="feature-desc">Batch processing</div>
        </div>
    """, unsafe_allow_html=True)

# Upload Section
st.markdown('<div class="upload-container">', unsafe_allow_html=True)
st.markdown('<p class="section-title">📤 Upload Vehicle Images</p>', unsafe_allow_html=True)

# Use Streamlit's temp directory (safe in cloud)
UPLOAD_DIR = "/tmp/Uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

uploaded_files = st.file_uploader(
    "Drag and drop images here or click to browse",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

st.markdown('</div>', unsafe_allow_html=True)

# Process uploaded images
if uploaded_files:
    st.markdown(f'<p class="section-title">🔍 Analysis Results ({len(uploaded_files)} image{"s" if len(uploaded_files) > 1 else ""})</p>', unsafe_allow_html=True)
    
    for idx, image_file in enumerate(uploaded_files):
        st.markdown('<div class="image-card">', unsafe_allow_html=True)
        
        # Save image
        image_path = os.path.join(UPLOAD_DIR, image_file.name)
        with open(image_path, "wb") as file:
            file.write(image_file.getbuffer())
        
        # Create columns for image and result
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"**Image {idx + 1}:** {image_file.name}")
            st.image(image_file, use_container_width=True)
        
        with col2:
            st.markdown("**Detection Result:**")
            try:
                with st.spinner("🔄 Analyzing damage..."):
                    prediction = predict(image_path)
                    st.info(f"🎯 **Result:** {prediction}")
                    
                    # Add damage badge based on prediction
                    if "damage" in prediction.lower() and "no" not in prediction.lower():
                        st.markdown('<span class="damage-badge damage-detected">⚠️ Damage Detected</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="damage-badge no-damage">✓ No Damage</span>', unsafe_allow_html=True)
                        
            except Exception as e:
                st.error(f"❌ Prediction error: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="caption-box">
        <p class="caption-text">
            ⚠️ <strong>Disclaimer:</strong> AI predictions are for reference only. Model accuracy may vary. 
            Always verify with professional inspection for critical assessments.
        </p>
    </div>
""", unsafe_allow_html=True)








# import os
# import streamlit as st
# from prediction import predict

# st.title("Vehicle Damage Detection")

# # Use Streamlit's temp directory (safe in cloud)
# UPLOAD_DIR = "/tmp/Uploaded_images"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# uploaded_files = st.file_uploader(
#     "Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True
# )

# if uploaded_files:
#     for image_file in uploaded_files:
#         image_path = os.path.join(UPLOAD_DIR, image_file.name)
#         with open(image_path, "wb") as file:
#             file.write(image_file.getbuffer())

#         with st.container():
#             st.image(image_file, use_container_width=True)
#             try:
#                 prediction = predict(image_path)
#                 st.info(prediction)
#             except Exception as e:
#                 st.error(f"Prediction error: {e}")

# st.caption("Model can make Mistake")




