import pytesseract
from PIL import Image, ImageEnhance
import numpy as np
import cv2

def enhance_image(image):
    """
    Enhance image for better text detection by adjusting contrast and sharpness.
    """
    # Convert PIL Image to numpy array for OpenCV processing
    img_array = np.array(image)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # Apply adaptive thresholding
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    # Convert back to PIL Image
    enhanced = Image.fromarray(binary)
    
    # Increase contrast
    enhancer = ImageEnhance.Contrast(enhanced)
    enhanced = enhancer.enhance(2.0)
    
    # Increase sharpness
    enhancer = ImageEnhance.Sharpness(enhanced)
    enhanced = enhancer.enhance(2.0)
    
    return enhanced

def find_text_boundaries(image, top_marker="Theoretical Questions", 
                        bottom_marker="Unlock 3877 Answers"):
    """
    Find the y-coordinates of the top and bottom markers using OCR.
    Returns tuple of (top_y, bottom_y) coordinates.
    Raises ValueError with specific details if markers aren't found.
    """
    # Get OCR data with bounding boxes
    ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    top_y = None
    bottom_y = None
    
    # Debug information
    detected_texts = []
    
    # Process each detected text element
    for i, text in enumerate(ocr_data['text']):
        # Clean up the detected text
        text = text.strip()
        if text:  # Only store non-empty text
            detected_texts.append(text)
            
        # Check for markers
        if top_marker.lower() in text.lower():
            top_y = ocr_data['top'][i] + ocr_data['height'][i]
            
        if bottom_marker.lower() in text.lower():
            bottom_y = ocr_data['top'][i]
    
    # Prepare detailed error message if needed
    error_messages = []
    if top_y is None:
        error_messages.append(f"Could not find top marker: '{top_marker}'")
    if bottom_y is None:
        error_messages.append(f"Could not find bottom marker: '{bottom_marker}'")
        
    if error_messages:
        error_detail = " AND ".join(error_messages)
        error_detail += "\nDetected text elements were: " + ", ".join(f"'{text}'" for text in detected_texts)
        raise ValueError(error_detail)
        
    return top_y, bottom_y

def process_image(input_path, output_path):
    """
    Main function to process the image and save the cropped output.
    """
    try:
        # Open and enhance the image
        original = Image.open(input_path)
        enhanced = enhance_image(original)
        
        # Find crop boundaries
        top_y, bottom_y = find_text_boundaries(enhanced)
        
        # Add small padding to the crop
        padding = 10
        top_y = max(0, top_y - padding)
        bottom_y = min(original.height, bottom_y + padding)
        
        # Crop the original image
        cropped = original.crop((0, top_y, original.width, bottom_y))
        
        # Save the cropped image
        cropped.save(output_path, 'PNG')
        
        print(f"Successfully processed image and saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return False

if __name__ == "__main__":
    # Example usage
    input_image =  r'.\screenshots\android.png'
    output_image = "cropped_image.png"
    process_image(input_image, output_image)