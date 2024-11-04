import cv2
import numpy as np

class ColorKeyer:
    def __init__(self, color_lower=(139, 65, 36), color_upper=(255, 144, 94)):
        """
        Initialize the ColorKeyer class
        Default values are set for orangez color keying
        """
        self.color_lower = np.array([5, 100, 100])
        self.color_upper = np.array([15, 255, 255])
        self.cap = cv2.VideoCapture(0)
        
    def run(self):
        while True:
            # Read frame from camera
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
            
            # Invert mask to key out the color
            mask_inv = cv2.bitwise_not(mask)
            
            # Apply the mask to the original frame
            result = cv2.bitwise_and(frame, frame, mask=mask_inv)
            
            # Display the result
            cv2.imshow('Color Keyed', result)
            
            # Break loop with 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    def __del__(self):
        """Cleanup when the object is destroyed"""
        self.cap.release()
        cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    # Create keyer with default green values
    keyer = ColorKeyer()
    # Or specify custom HSV color range
    # keyer = ColorKeyer(color_lower=(100, 50, 50), color_upper=(140, 255, 255))  # Blue
    keyer.run()
