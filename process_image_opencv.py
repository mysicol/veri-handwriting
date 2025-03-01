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
        cv2.imshow("Image", self.__image)
        cv2.waitKey(0)

    def find_top_square(self):
        pass

gridImage = GridImage("grid_image.jpg")
gridImage.display()