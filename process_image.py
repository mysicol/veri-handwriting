from PIL import Image

class GridImage:
    def __init__(self, filepath):
        self.__filepath = filepath

        if not self.__open_image():
            return None

        self.__grayscale_convert()
        self.__load_image_pixels()

    def __open_image(self):
        try: 
            self.__image_file = Image.open(self.__filepath)
            return True
        except IOError:
            return False

    def __grayscale_convert(self):
        self.__image_file = self.__image_file.convert("L")

    def __load_image_pixels(self):
        self.__image_pixels = self.__image_file.load()

    def find_top_square(image_pixels):
        print(image_pixels)

gridImage = GridImage("grid_image.jpg")