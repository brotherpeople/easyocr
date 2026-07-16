import gradio as gr
import cv2
import numpy as np
from PIL import Image
from engine.ocr_engine import HMIOcrEngine
from engine.contrast_analyzer import ContrastAnalyzer
from engine.ergonomics import ErgonomicCalculator

# Try importing spaces for Hugging Face ZeroGPU support
try:
    import spaces
except ImportError:
    # Fallback dummy class for local CPU execution
    class spaces:
        @staticmethod
        def GPU(func):
            return func

# Initialize engines lazily to prevent Hugging Face startup timeout during model download
ocr_engine = None
contrast_analyzer = ContrastAnalyzer()

def get_ocr_engine():
    global ocr_engine
    if ocr_engine is None:
        ocr_engine = HMIOcrEngine()
    return ocr_engine

# Parameter mapping based on ISO 15008 presets
params = {
    "Automotive": {"dist": 70, "dpi": 120, "threshold": 4.5, "min_arcmin": 20},
    "Mobile": {"dist": 30, "dpi": 460, "threshold": 3.0, "min_arcmin": 16},
    "Tablet": {"dist": 40, "dpi": 264, "threshold": 3.0, "min_arcmin": 16},
    "Monitor": {"dist": 60, "dpi": 109, "threshold": 4.5, "min_arcmin": 16},
    "Marine Dashboard": {"dist": 80, "dpi": 96, "threshold": 5.0, "min_arcmin": 22}
}

@spaces.GPU
def analyze_hmi(image, env_preset):
    if image is None:
        return None, []
    
    # Gradio provides the image as a NumPy array (RGB)
    img_array = np.array(image)
        
    # Convert to OpenCV format (RGB -> BGR)
    cv_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    current_params = params[env_preset]
    
    # Run OCR (requires a file path, so write to a temp file)
    temp_path = "temp_hmi.png"
    cv2.imwrite(temp_path, cv_img)
    engine = get_ocr_engine()
    ocr_results = engine.extract_text_data(temp_path)
    
    output_img = img_array.copy()
    analysis_data = []
    
    for item in ocr_results:
        bbox = item['bbox']
        text_pixel_height = item['height']
        
        # --- Contrast Analysis ---
        ratio = contrast_analyzer.analyze_text_contrast(cv_img, bbox)
        contrast_pass = ratio >= current_params['threshold']
        
        # --- Size (Arcmin) Analysis ---
        physical_height_mm = ErgonomicCalculator.pixel_to_mm(text_pixel_height, current_params['dpi'])
        arcmin = ErgonomicCalculator.calculate_visual_angle(physical_height_mm, current_params['dist'] * 10)
        size_pass = arcmin >= current_params['min_arcmin']
        
        is_pass = contrast_pass and size_pass
        
        # Color Coding in RGB (Green for pass, Red for fail)
        color = (0, 255, 0) if is_pass else (255, 0, 0)
        
        # Failure Reason
        fail_reasons = []
        if not contrast_pass: fail_reasons.append("Low Contrast")
        if not size_pass: fail_reasons.append("Small Font")
        status_text = "✅ Pass" if is_pass else f"❌ Fail ({', '.join(fail_reasons)})"
        
        # Draw Bounding Box
        pts = np.array(bbox, np.int32)
        cv2.polylines(output_img, [pts], True, color, 2)
        
        analysis_data.append([
            item['text'],
            f"{ratio:.2f}:1",
            f"{arcmin:.1f}'",
            status_text
        ])
        
    return output_img, analysis_data

# Gradio Interface Custom CSS
css = """
/* Target only the source select buttons in the bottom bar, not the main upload button */
#hmi-image-input div[class*="select"] button:nth-of-type(1)::after,
#hmi-image-input div[class*="source"] button:nth-of-type(1)::after {
    content: " Upload" !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    margin-left: 6px !important;
}
#hmi-image-input div[class*="select"] button:nth-of-type(2)::after,
#hmi-image-input div[class*="source"] button:nth-of-type(2)::after {
    content: " Paste" !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    margin-left: 6px !important;
}
#hmi-image-input div[class*="select"] button,
#hmi-image-input div[class*="source"] button {
    display: inline-flex !important;
    align-items: center !important;
    padding: 6px 12px !important;
    margin: 0 8px !important; /* Add margin between Upload and Paste */
    width: auto !important; /* Auto width to prevent text overflow/overlap */
    min-width: 90px !important; /* Ensure enough room for text */
}

/* Add indent and spacing for the Detailed Audit Report section */
.report-section {
    margin-top: 35px !important;
    padding-left: 20px !important;
    border-left: 3px solid #3b82f6 !important;
}
"""

with gr.Blocks(title="AI-ErgoCheck: HMI Readability Tool") as demo:
    gr.Markdown("# 🛡️ AI-ErgoCheck")
    gr.Markdown("### Intelligent HMI Readability Audit System based on [ISO 15008](https://www.iso.org/standard/62784.html)")
    
    with gr.Row():
        with gr.Column():
            env_preset = gr.Dropdown(
                choices=["Automotive", "Mobile", "Tablet", "Monitor", "Marine Dashboard"],
                value="Automotive",
                label="Select HMI Environment",
                info="Standard readability specifications (ISO 15008, etc.) will be applied automatically."
            )
            image_input = gr.Image(
                type="numpy", 
                label="Upload HMI Design Image",
                sources=["upload", "clipboard"],
                elem_id="hmi-image-input"
            )
            analyze_btn = gr.Button("🔍 Run Readability Audit", variant="primary")
            
        with gr.Column():
            image_output = gr.Image(label="AI Audit Result (Overlay)")
            
    with gr.Column(elem_classes="report-section"):
        gr.Markdown("### 📊 Detailed Audit Report")
        table_output = gr.Dataframe(
            headers=["Text", "Contrast", "Size (Arcmin)", "Status"],
            datatype=["str", "str", "str", "str"],
            label="Audit Report"
        )
    
    analyze_btn.click(
        fn=analyze_hmi,
        inputs=[image_input, env_preset],
        outputs=[image_output, table_output]
    )

if __name__ == "__main__":
    demo.launch(css=css, ssr_mode=False)
