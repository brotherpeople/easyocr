import math

class ErgonomicCalculator:
    @staticmethod
    def pixel_to_mm(pixels, dpi):
        """
        Convert pixels to physical size (mm).
        :param pixels: Number of pixels.
        :param dpi: Dots Per Inch of the display.
        :return: Physical size in mm.
        """
        # 1 inch = 25.4 mm
        return (pixels / dpi) * 25.4

    @staticmethod
    def calculate_visual_angle(height_mm, distance_mm):
        """
        Calculate visual angle (Arcminute) based on physical height and viewing distance.
        ISO 15008 minimum character height is typically 16-20 arcmin.
        :param height_mm: Physical height of the object (mm).
        :param distance_mm: Viewing distance (mm).
        :return: Visual angle in Arcminutes.
        """
        # arctan(height / distance) -> convert radians to degrees -> convert degrees to arcmin
        angle_rad = math.atan2(height_mm, distance_mm)
        angle_deg = math.degrees(angle_rad)
        arcmin = angle_deg * 60
        return arcmin
