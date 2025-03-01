from PIL import Image

def load_image(filepath):
    try: 
        return Image.open(filepath)
    except IOError:
        return None

print(load_image("IMG_2099.jpg"))