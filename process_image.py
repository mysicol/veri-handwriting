from PIL import Image

class GridImage:
    def __init__(self, filepath):
        self.__filepath = filepath

        if not self.__open_image():
            return None

        self.__grayscale_convert()
        self.__load_image_pixels()

        self.__width, self.__height = self.__image.size

    def __open_image(self):
        try: 
            self.__image = Image.open(self.__filepath)
            return True
        except IOError:
            return False

    def __grayscale_convert(self):
        self.__image = self.__image.convert("L")

    def __load_image_pixels(self):
        self.__image_pixels = self.__image.load()

    def find_top_square(self):
        maxn = 0
        for i in range(int(self.__width / 6)):
            for j in range(int(self.__height / 6)):                    
                print(self.__image_pixels[i, j])

gridImage = GridImage("grid_image.jpg")
gridImage.find_top_square()