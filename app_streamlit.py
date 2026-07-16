import streamlit as st
import cv2
import numpy as np
from PIL import Image
from engine.ocr_engine import HMIOcrEngine
from engine.contrast_analyzer import ContrastAnalyzer
from engine.ergonomics import ErgonomicCalculator

# Initialize session state (to prevent reloading models)
if 'ocr_engine' not in st.session_state:
    st.session_state.ocr_engine = HMIOcrEngine()
if 'contrast_analyzer' not in st.session_state:
    st.session_state.contrast_analyzer = ContrastAnalyzer()

st.set_page_config(page_title="AI-ErgoCheck: HMI Readability Tool", layout="wide")

st.title("🛡️ AI-ErgoCheck")
st.markdown(
    "### Intelligent HMI Readability Audit System based on [ISO 15008](https://www.iso.org/standard/62784.html)"
)

# Main Configuration Area (Integrated into main screen)
st.divider()
st.subheader("⚙️ Analysis Configuration")
col_conf1, col_conf2 = st.columns([2, 1])

with col_conf1:
    env_preset = st.selectbox(
        "Select HMI Environment",
        ["Automotive", "Mobile", "Tablet", "Monitor", "Marine Dashboard"],
        help="Standard readability specifications (ISO 15008, etc.) will be applied automatically."
    )

# Internal parameter mapping
params = {
    "Automotive": {"dist": 70, "dpi": 120, "threshold": 4.5, "min_arcmin": 20},
    "Mobile": {"dist": 30, "dpi": 460, "threshold": 3.0, "min_arcmin": 16},
    "Tablet": {"dist": 40, "dpi": 264, "threshold": 3.0, "min_arcmin": 16},
    "Monitor": {"dist": 60, "dpi": 109, "threshold": 4.5, "min_arcmin": 16},
    "Marine Dashboard": {"dist": 80, "dpi": 96, "threshold": 5.0, "min_arcmin": 22}
}

current_params = params[env_preset]

uploaded_file = st.file_uploader("Upload HMI Design Image", type=["png", "jpg", "jpeg"])

# Start Analysis Button
analyze_button = st.button("🔍 Run Readability Audit", type="primary", use_container_width=True)

if uploaded_file is not None and analyze_button:
    # Load Image
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    # Convert to OpenCV format (RGB -> BGR)
    cv_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Original Design")
        st.image(image, use_container_width=True)

    with st.spinner(f'AI Analysis in progress ({env_preset} standards)...'):
        # 1. OCR Extraction
        temp_path = "temp_hmi.png"
        cv2.imwrite(temp_path, cv_img)
        ocr_results = st.session_state.ocr_engine.extract_text_data(temp_path)

        # 2. Result Visualization
        output_img = img_array.copy()
        analysis_data = []

        for item in ocr_results:
            bbox = item['bbox']
            text_pixel_height = item['height']
            
            # --- Contrast Analysis ---
            ratio = st.session_state.contrast_analyzer.analyze_text_contrast(cv_img, bbox)
            contrast_pass = ratio >= current_params['threshold']
            
            # --- Size (Arcmin) Analysis ---
            physical_height_mm = ErgonomicCalculator.pixel_to_mm(text_pixel_height, current_params['dpi'])
            arcmin = ErgonomicCalculator.calculate_visual_angle(physical_height_mm, current_params['dist'] * 10)
            size_pass = arcmin >= current_params['min_arcmin']
            
            # Combined Judgment
            is_pass = contrast_pass and size_pass
            
            # Color Coding (BGR)
            color = (0, 255, 0) if is_pass else (0, 0, 255) # Green / Red
            
            # Failure Reason
            fail_reasons = []
            if not contrast_pass: fail_reasons.append("Low Contrast")
            if not size_pass: fail_reasons.append("Small Font")
            status_text = "✅ Pass" if is_pass else f"❌ Fail ({', '.join(fail_reasons)})"
            
            # Draw Bounding Box
            pts = np.array(bbox, np.int32)
            cv2.polylines(output_img, [pts], True, color, 2)
            
            analysis_data.append({
                "Text": item['text'],
                "Contrast": f"{ratio:.2f}:1",
                "Size (Arcmin)": f"{arcmin:.1f}'",
                "Status": status_text
            })

    with col2:
        st.subheader("AI Audit Result (Overlay)")
        # BGR -> RGB for display
        display_output = cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)
        st.image(display_output, use_container_width=True)

    st.divider()
    st.subheader("📊 Detailed Audit Report")
    st.dataframe(analysis_data, use_container_width=True)

else:
    if uploaded_file is None:
        st.info("Please upload a design image to start.")
    elif not analyze_button:
        st.info("Click the 'Run Readability Audit' button to begin analysis.")
