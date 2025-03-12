from PIL import Image

def resize_to_passport_size(input_image_path, output_image_path):
    # Open the image file
    img = Image.open(input_image_path)

    # Resize image to 600x600 pixels (passport photo size)
    passport_size = (600, 600)
    img = img.resize(passport_size, Image.ANTIALIAS)

    # Save the resized image
    img.save(output_image_path)
    print(f"Passport-sized image saved as {output_image_path}")

if __name__ == "__main__":
    # Example usage:
    input_image_path = "casual_photo.jpg"  # Replace with your casual photo file path
    output_image_path = "passport_photo.jpg"  # This will be the output file path
    resize_to_passport_size(input_image_path, output_image_path)

