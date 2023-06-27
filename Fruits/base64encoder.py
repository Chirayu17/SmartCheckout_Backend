import base64

def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')

# Set the image file name you want to convert
image_pathname = "/Users/cgupta/Documents/smartcheckoutv3/SmartCheckout_Backend/Fruits/Apple.jpeg"

# Convert the image to base64
base64_image = convert_image_to_base64(image_pathname)
print("Base64 encoded image:")
print(base64_image)


