# from PIL import Image, ImageEnhance, ImageFilter
# import pytesseract
# # Reload the newly uploaded image for analysis
# original_image_path = r'.\screenshots\android.png'
# original_image = Image.open(original_image_path)

# # Display the dimensions of the image for reference
# original_image_dimensions = original_image.size  # (width, height)
# print(original_image_dimensions)

# # Step 2: Define cropping coordinates
# # Coordinates need to be manually set based on visual analysis of the image
# # These values assume a vertical crop and leave horizontal dimensions intact

# # Top boundary: Location of "Theoretical Questions"
# top_crop_y = 850  # Adjust this based on your image dimensions

# # Bottom boundary: Location of the orange "Unlock 3877 Answers" button
# bottom_crop_y = 2200  # Adjust this based on your image dimensions

# # Crop the image
# cropped_image = original_image.crop((0, top_crop_y, original_image.width, bottom_crop_y))

# # Step 3: Enhance the cropped image for better OCR results
# enhanced_image = cropped_image.filter(ImageFilter.SHARPEN)  # Sharpen the image
# enhancer = ImageEnhance.Contrast(enhanced_image)
# enhanced_image = enhancer.enhance(2)  # Increase contrast

# # Optional: Save the cropped image for verification
# cropped_image.save("cropped_image.png")  # Check this file to ensure the crop is correct

# # Step 4: Perform OCR on the cropped section
# extracted_text = pytesseract.image_to_string(enhanced_image)

# # Step 5: Output the extracted text
# print("Extracted Text:\n")
# print(extracted_text)

# # Save the text to a file
# with open("extracted_text.txt", "w", encoding="utf-8") as text_file:
#     text_file.write(extracted_text)
from PIL import Image, ImageEnhance, ImageDraw
import pytesseract

# Load the image
image_path = r'.\screenshots\android.png'  # Replace with your image file path
original_image = Image.open(image_path)

# Enhance image for better text recognition
enhancer = ImageEnhance.Contrast(original_image)
enhanced_image = enhancer.enhance(2)  # Increase contrast for better OCR

# Use pytesseract to get bounding boxes of all detected text
text_boxes = pytesseract.image_to_boxes(enhanced_image)

# Initialize top and bottom boundaries
top_boundary = None
bottom_boundary = None

# Parse the detected text boxes to find the coordinates
for line in text_boxes.splitlines():
    parts = line.split()
    if len(parts) < 6:
        continue
    char, x1, y1, x2, y2, page = parts  # Extract bounding box info
    text = pytesseract.image_to_string(enhanced_image)  # Extract text
    
    # Check for "Theoretical Questions"
    if "Theoretical Questions" in text:
        top_boundary = int(original_image.height) - int(y2)  # Get the top boundary (adjusted for inverted y-coordinates)
    
    # Check for "Unlock 3877 Answers"
    if "Unlock 3877 Answers" in text:
        bottom_boundary = int(original_image.height) - int(y1)  # Get the bottom boundary (adjusted for inverted y-coordinates)

# Ensure boundaries are found
if top_boundary is None or bottom_boundary is None:
    raise ValueError("Could not find required text in the image.")

# Crop the image using the detected boundaries
cropped_image = original_image.crop((0, top_boundary, original_image.width, bottom_boundary))

# Save the cropped image for verification
cropped_image_path = "dynamic_cropped_image.png"
cropped_image.save(cropped_image_path)

# Create a new image with the same dimensions as the original
new_image = Image.new("RGB", original_image.size, (255, 255, 255))  # White background
new_image.paste(cropped_image, (0, top_boundary))  # Place the cropped image in its original position

# Save the new image
new_image_path = "new_image_with_cropped_dimensions.png"
new_image.save(new_image_path)

# Perform OCR on the cropped section
extracted_text = pytesseract.image_to_string(cropped_image)

# Output the extracted text
print("Extracted Text:\n")
print(extracted_text)

# Save the text to a file
with open("dynamic_extracted_text.txt", "w", encoding="utf-8") as text_file:
    text_file.write(extracted_text)

# Save paths for reference
print(f"Cropped Image Path: {cropped_image_path}")
print(f"New Image Path: {new_image_path}")
