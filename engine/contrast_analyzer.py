import cv2
import numpy as np

class ContrastAnalyzer:
    @staticmethod
    def calculate_luminance(rgb):
        """
        Calculate luminance based on RGB values.
        Formula: L = 0.2126R + 0.7152G + 0.0722B
        """
        r, g, b = rgb / 255.0
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    @staticmethod
    def get_contrast_ratio(l1, l2):
        """
        Calculate contrast ratio between two luminance values.
        Formula: (Lmax + 0.05) / (Lmin + 0.05)
        """
        l_max = max(l1, l2)
        l_min = min(l1, l2)
        return (l_max + 0.05) / (l_min + 0.05)

    def analyze_text_contrast(self, image, bbox):
        """
        Analyze contrast of text region (Min-Max Luminance method).
        :param image: Original image (OpenCV BGR format).
        :param bbox: Text bounding box.
        :return: Contrast ratio.
        """
        x1, y1 = int(bbox[0][0]), int(bbox[0][1])
        x2, y2 = int(bbox[2][0]), int(bbox[2][1])
        
        h, w = image.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)

        text_roi = image[y1:y2, x1:x2]
        if text_roi.size == 0:
            return 0.0

        # Convert ROI to grayscale for luminance analysis
        gray_roi = cv2.cvtColor(text_roi, cv2.COLOR_BGR2GRAY)
        
        # Use min and max luminance within ROI to measure actual contrast
        min_val, max_val, _, _ = cv2.minMaxLoc(gray_roi)
        
        # Calculate luminance (normalized to 0~1)
        l_min = min_val / 255.0
        l_max = max_val / 255.0
        
        ratio = self.get_contrast_ratio(l_min, l_max)
        
        return ratio

if __name__ == "__main__":
    print("Contrast Analyzer Initialized.")
