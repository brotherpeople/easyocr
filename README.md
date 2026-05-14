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
