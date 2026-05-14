import easyocr
import cv2
import numpy as np

class HMIOcrEngine:
    def __init__(self, languages=['ko', 'en']):
        """
        Initialize OCR engine for HMI readability analysis.
        :param languages: List of supported languages (Default: Korean, English).
        """
        self.reader = easyocr.Reader(languages)

    def extract_text_data(self, image_path):
        """
        Extract text information (content, bounding box, confidence) from an image.
        :param image_path: Path to the image to analyze.
        :return: List of formatted text data.
        """
        results = self.reader.readtext(image_path)
        formatted_results = []
        
        for (bbox, text, prob) in results:
            # bbox: [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
            formatted_results.append({
                'text': text,
                'bbox': bbox,
                'confidence': prob,
                'width': bbox[1][0] - bbox[0][0],
                'height': bbox[2][1] - bbox[0][1]
            })
            
        return formatted_results

if __name__ == "__main__":
    # Test code
    print("OCR Engine Initialized.")
