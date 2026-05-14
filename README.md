# AI-ErgoCheck: Intelligent HMI Readability Audit System

AI-ErgoCheck is an automated tool designed to verify the readability of Human-Machine Interface (HMI) designs based on international ergonomic standards like **ISO 15008**.

---

## 1. Problem Statement

### Limitations of Traditional Methods
- **Subjective Evaluation:** HMI readability is often judged subjectively by designers, leading to inconsistent quality.
- **Complexity of Standards:** Manually calculating ergonomic values (contrast ratios, visual angles) from ISO 15008 is time-consuming and prone to human error.
- **Delayed Feedback:** Issues are often discovered late in the production phase, making them expensive to fix.

### Our Solution
- **AI-Powered Automation:** Combines OCR and Computer Vision to quantitatively analyze text and graphical elements in design images.
- **Standard-as-Code:** Algorithms based on ISO 15008 provide instant 'Pass/Fail' feedback and actionable insights.

---

## 2. Development Process

### Step 1: Technical Stack & Architecture
- **OCR Engine:** `EasyOCR` for high-accuracy multi-language text extraction.
- **Image Processing:** `OpenCV` for ROI analysis and min-max luminance detection.
- **UI Framework:** `Streamlit` for an interactive, web-based audit dashboard.
- **Ergonomics Logic:** Custom Python modules implementing physical dimension to visual angle (Arcminute) conversions.

### Step 2: Core AI Integration
1. **Text Localization:** Detects and extracts text bounding boxes.
2. **Min-Max Contrast Analysis:** Analyzes the luminance difference between text and background within the ROI to ensure readability.
3. **Visual Angle Calculation:** Maps pixel height to physical size and calculates the visual angle (Arcmin) based on viewing distance presets.

### Step 3: Human-Centered UX
- Integrated environmental presets (Automotive, Mobile, Marine, etc.) to simplify complex ergonomic parameters for users without domain expertise.

---

## 3. Results & Portfolio Impact

### Key Achievements
- **Quantitative Data:** Provides objective metrics (e.g., "Contrast Ratio 5.2:1") instead of vague "looks good" judgments.
- **Real-time Feedback:** Instantly identifies non-compliant elements with red bounding box overlays.

### Professional Highlights (For Recruiters)
- **Expertise in CV:** Demonstrated advanced use of Computer Vision beyond simple library calls (e.g., handling relative sizing via DPI/Distance mapping).
- **Human-AI Collaboration:** Showcased the ability to use AI as a co-pilot to solve professional-grade ergonomic problems.
- **Global Standard Compliance:** Focused on international industry standards (ISO 15008), proving industry readiness.

---

## 4. How to Run

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application:**
   ```bash
   streamlit run app.py
   ```
