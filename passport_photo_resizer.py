from PIL import Image, ImageFilter
import cv2
import os

def resize_and_crop_to_passport_size(input_image_path, output_image_path):
    # Check if the input image exists
    if not os.path.exists(input_image_path):
        print(f"Error: {input_image_path} does not exist!")
        return

    # Load the image with OpenCV
    print(f"Opening image: {input_image_path}")  # Debugging line
    img = cv2.imread(input_image_path)
    
    # Load the pre-trained face detection model (Haar cascade)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert the image to grayscale for face detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        print("No faces detected!")
        return

    # Get the coordinates of the first detected face
    (x, y, w, h) = faces[0]

    # Crop the image to include the head, shoulders, and ears (expand the crop region)
    margin_top = int(h * 0.5)  # Add more margin on top for headroom and ears
    margin_bottom = int(h * 0.55)  # Add more margin on the bottom to include shoulders and ears
    cropped_img = img[y - margin_top:y + h + margin_bottom, x - int(w * 0.25):x + w + int(w * 0.25)]

    # Convert the cropped image back to RGB (for Pillow compatibility)
    cropped_img_pil = Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))

    # Get the current size of the cropped image
    width, height = cropped_img_pil.size
    print(f"Original Cropped Size: {width}x{height}")

    # Resize to passport photo size (600x600 pixels) while maintaining the aspect ratio
    passport_size = (600, 600)

    # Calculate the aspect ratio of the cropped image
    aspect_ratio = width / height

    if aspect_ratio > 1:  # Image is wide
        new_width = passport_size[0]
        new_height = int(new_width / aspect_ratio)
    else:  # Image is tall or square
        new_height = passport_size[1]
        new_width = int(new_height * aspect_ratio)

    # Resize the cropped image while maintaining the aspect ratio using Lanczos (high-quality filter)
    resized_img = cropped_img_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Apply sharpening filter to improve sharpness
    sharpened_img = resized_img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    # Create a new square image with a white background
    final_image = Image.new("RGB", passport_size, (255, 255, 255))  # White background

    # Paste the sharpened image onto the center of the white background
    final_image.paste(sharpened_img, ((passport_size[0] - new_width) // 2, (passport_size[1] - new_height) // 2))

    # Save the resized and sharpened image
    print(f"Saving image as: {output_image_path}")  # Debugging line
    final_image.save(output_image_path)

    # Verify if the image was saved
    if os.path.exists(output_image_path):
        print(f"Passport-sized image saved as {output_image_path}")
    else:
        print(f"Error: {output_image_path} was not saved!")

if __name__ == "__main__":
    # Example usage:
    input_image_path = "casual_photo.jpg"  # Replace with your casual photo file path
    output_image_path = "passport_photo.jpg"  # This will be the output file path
    print("Starting the script...")  # Added message to confirm the script starts
    resize_and_crop_to_passport_size(input_image_path, output_image_path)
    print("Script execution finished.")  # Added message after script finishes
