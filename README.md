---
title: AI-ErgoCheck
emoji: 🛡️
colorFrom: blue
colorTo: indigo
sdk: gradio
app_file: app.py
pinned: false
---

# AI-ErgoCheck: Intelligent HMI Readability Audit System


AI-ErgoCheck is an automated tool designed to verify the readability of Human-Machine Interface (HMI) designs based on the **ISO 15008** international ergonomic standard. It utilizes AI and Computer Vision to provide quantitative assessments of text size and contrast.

---

## Key Features

- **Automated Text Audit:** Uses `EasyOCR` to detect and extract text from design images.
- **Min-Max Contrast Analysis:** Calculates the luminance contrast ratio between text and background within the ROI.
- **Ergonomic Size Validation:** Converts pixel dimensions into visual angles (Arcminutes) based on display DPI and viewing distance.
- **Environment Presets:** Optimized presets for Automotive, Mobile, Tablet, Monitor, and Marine environments.
- **Visual Feedback:** Provides an annotated overlay with color-coded bounding boxes (Green: Pass / Red: Fail).

## Technical Implementation

### 1. Contrast Analysis
The system identifies the darkest and brightest pixels within each text bounding box to calculate a true luminance ratio, preventing color dilution common in simple mean-average methods.

### 2. Physical Scale Mapping
To solve the problem of relative pixel sizing, the tool maps image resolution to physical dimensions using DPI settings and calculates the actual visual angle subtended at the observer's eye.

### 3. Compliance Checking
Results are compared against ISO 15008 benchmarks:
- **Minimum Contrast:** 3:1 or 4.5:1 depending on the environment.
- **Minimum Character Height:** Typically 16' to 22' arcminutes based on usage context.

---

## How to Run

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

## Requirements
- Python 3.8+
- EasyOCR
- OpenCV
- Streamlit
- NumPy

---

## 🚀 Deploying to Hugging Face Spaces (One-Click Web App)

You can host this tool online for free on Hugging Face Spaces so anyone can test it via a web browser without installing anything locally:

1. **Sign Up/Log In** to [Hugging Face](https://huggingface.co/).
2. Go to **Spaces** and click **Create new Space**.
3. Configure the Space:
   - **Space Name:** Choose any name (e.g., `ai-ergocheck`).
   - **SDK:** Select **Gradio**.
   - **Space Hardware:** Select **CPU Basic (Free)** (or `ZeroGPU` if you want GPU acceleration, but CPU Basic is unlimited).
   - **Repository Type:** Public (recommended for sharing).
4. Either clone the Hugging Face Space repository locally and push these files to it, or import this GitHub repository directly under the Space creation settings.
5. Once pushed, Hugging Face will automatically install the requirements and launch the Gradio app. It will be live at `https://huggingface.co/spaces/<your-username>/<your-space-name>`.

