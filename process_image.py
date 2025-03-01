from PIL import Image

def open_image(filepath):
    try: 
        return Image.open(filepath)
    except IOError:
        return None

def grayscale_convert(image_file):
    return image_file.convert("L")

def load_image(image_file):
    return image_file.load()

def find_top_square():
    print(len(image_pixels))

image_file = open_image("IMG_2099.jpg")
print(image_file)

gray_image_file = grayscale_convert(image_file)
print(gray_image_file)

image_pixels = load_image(gray_image_file)
print(image_pixels)

find_top_square(image_pixels)