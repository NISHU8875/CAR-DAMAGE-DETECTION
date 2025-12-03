import os
import streamlit as st
from prediction import predict
import time

# 1. Configure the page (Must be the first Streamlit command)
st.set_page_config(
    page_title="AI Vehicle Damage Assessment",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS to give it that "Rich" look
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Title Styling */
    .title-text {
        color: #1E3D59;
        font-family: 'Helvetica', sans-serif;
        text-align: center;
        font-weight: 800;
        padding-bottom: 20px;
    }
    
    /* Subtitle/Caption */
    .caption-text {
        text-align: center;
        color: #666;
        font-size: 18px;
    }

    /* File Uploader Customization */
    .stFileUploader {
        border: 2px dashed #1E3D59;
        border-radius: 10px;
        padding: 20px;
        background-color: white;
    }

    /* Prediction Card Styling */
    .prediction-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 5px solid #ff4b4b;
    }
    
    .result-text {
        font-size: 24px;
        font-weight: bold;
        color: #1E3D59;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar for Context
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3209/3209995.png", width=100)
    st.title("AI Inspector")
    st.write("This application uses **ResNet50**, a powerful Deep Learning model, to analyze vehicle images and detect damage types.")
    st.markdown("---")
    st.write("### 🛠 How to use:")
    st.write("1. Upload an image (JPG/PNG)")
    st.write("2. AI scans the damage")
    st.write("3. Get instant classification")
    st.markdown("---")
    st.caption("Developed by Nishu")

# 4. Main Interface
st.markdown('<h1 class="title-text">🚗 Vehicle Damage Detection</h1>', unsafe_allow_html=True)
st.markdown('<p class="caption-text">Upload a photo of the vehicle to analyze the damage severity and location.</p>', unsafe_allow_html=True)

# Use Streamlit's temp directory
UPLOAD_DIR = "/tmp/Uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# File Uploader
uploaded_files = st.file_uploader(
    "Drag and drop vehicle images here...", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.markdown("---")
    
    for image_file in uploaded_files:
        # Create a clean layout with 2 columns: Image (Left) vs Result (Right)
        col1, col2 = st.columns([1, 1], gap="large")
        
        image_path = os.path.join(UPLOAD_DIR, image_file.name)
        
        # Save file
        with open(image_path, "wb") as file:
            file.write(image_file.getbuffer())

        # Column 1: Display Image
        with col1:
            st.image(image_file, caption=f"Source: {image_file.name}", use_container_width=True, output_format="JPEG")

        # Column 2: Display Prediction with "Liveliness"
        with col2:
            st.markdown("### 🔍 Analysis Report")
            
            # Add a spinner to simulate "AI Thinking" (makes it feel responsive)
            with st.spinner(f"Analyzing {image_file.name}..."):
                time.sleep(1) # Optional: purely for visual effect
                try:
                    prediction = predict(image_path)
                    
                    # Display the result in a nice card
                    st.markdown(f"""
                    <div class="prediction-card">
                        <p style="color:grey; margin-bottom:5px;">Detected Damage Type</p>
                        <p class="result-text">{prediction}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add a visual success indicator
                    st.success("Analysis Complete")
                    
                except Exception as e:
                    st.error(f"Prediction error: {e}")
        
        st.markdown("---")

else:
    # Show a placeholder when no image is uploaded to keep the UI looking full
    st.info("👋 Waiting for image upload...")








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




