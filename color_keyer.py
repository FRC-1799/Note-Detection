import cv2
import numpy as np

class ColorKeyer:
    def __init__(self):
        """
        Initialize the ColorKeyer class
        Values set for orange color keying with oval detection
        """
        # Orange HSV range
        self.color_lower = np.array([5, 100, 100])
        self.color_upper = np.array([15, 255, 255])
        self.cap = cv2.VideoCapture(0)
        
    def is_orange_oval(self, contour, mask):
        """
        Check if the contour contains enough orange pixels
        """
        # Create a blank mask for this contour
        contour_mask = np.zeros_like(mask)
        cv2.drawContours(contour_mask, [contour], -1, 255, -1)
        
        # Count orange pixels within the contour
        orange_pixels = cv2.countNonZero(cv2.bitwise_and(mask, contour_mask))
        total_pixels = cv2.countNonZero(contour_mask)
        
        # Calculate percentage of orange pixels
        if total_pixels > 0:
            orange_ratio = orange_pixels / total_pixels
            return orange_ratio > 0.6  # Adjust this threshold (60% orange)
        return False

    def detect_ovals(self, mask):
        """
        Detect orange ovals in the masked image
        Returns only the ellipses that are predominantly orange
        """
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        ellipses = []
        for contour in contours:
            if len(contour) >= 5:
                area = cv2.contourArea(contour)
                if area > 500 and self.is_orange_oval(contour, mask):
                    ellipse = cv2.fitEllipse(contour)
                    ellipses.append(ellipse)
        
        return ellipses

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Convert frame to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Create mask for specified color range
            mask = cv2.inRange(hsv, self.color_lower, self.color_upper)
            
            # Refine the mask
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            
            # Detect orange ovals in the mask
            ellipses = self.detect_ovals(mask)
            
            # Draw detected orange ovals
            for ellipse in ellipses:
                cv2.ellipse(frame, ellipse, (0, 255, 0), 2)
                center = (int(ellipse[0][0]), int(ellipse[0][1]))
                cv2.circle(frame, center, 2, (0, 0, 255), 3)
                
                # Print oval info
                print(f"Orange oval detected - Center: {center}, "
                      f"Axes: {ellipse[1]}, "
                      f"Angle: {ellipse[2]:.1f}°")
            
            # Show both the mask and the final frame
            cv2.imshow('Orange Mask', mask)
            cv2.imshow('Orange Ovals Only', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    keyer = ColorKeyer()
    keyer.run()