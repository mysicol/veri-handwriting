import cv2

class GridImage:
    def __init__(self, filepath):
        self.__filepath = filepath
    
        self.__load_image()
        self.__grayscale_convert()

        self.__height, self.__width = self.__image.shape[:2]

    def __load_image(self):
        self.__image = cv2.imread(self.__filepath)

    def __grayscale_convert(self):
        self.__image = cv2.cvtColor(self.__image, cv2.COLOR_BGR2GRAY)

    def display(self):
        self.__display_img(self.__image)

    def __display_img(self, image):
        cv2.imshow(self.__filepath, cv2.resize(image, (500, 500)))
        cv2.waitKey(0)

    def mask_image(self):
        masked_image = cv2.threshold(self.__image, 100, 255, cv2.THRESH_BINARY_INV)[1]
        self.__display_img(masked_image)

gridImage = GridImage("grid_image.jpg")
# gridImage.display()
gridImage.mask_image()