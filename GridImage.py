import cv2
import math

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

    def __display_square(self, square):
        self.__display_cropped_image(square[0], square[1], square[2], square[3])

    def __display_cropped_image(self, x, y, w, h, title="dontcare", image=None):
        if not image:
            image = self.__image
        cv2.imshow(title, image[y:y+h, x:x+w])
        cv2.waitKey(0)

    def __crop_image(self, image, x, y, w, h):
        return image[y:y+h, x:x+w]

    def mask_image(self, thresh=100):
        test =  cv2.threshold(self.__image, thresh, 255, cv2.THRESH_BINARY_INV)[1]
        # self.__display_img(test)
        return test

    def find_squares(self):
        top_left = [math.inf, math.inf]
        top_right = [0, math.inf]
        bot_left = [math.inf, 0]
        bot_right = [0, 0]

        thresh = self.mask_image(thresh=60) # Adjust threshold value as needed
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        print(self.__width, self.__height)

        min_width = self.__width / 30
        min_height = self.__height / 40

        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                
                if w > min_width and h > min_height:
                    if y > 0 and y < top_left[1] and x < self.__width / 2:
                        top_left = [x, y, w, h]
                    if y > 0 and y < top_left[1] and x > self.__width / 2:
                        top_right = [x, y, w, h]
                    if y < self.__height - 1 and y > bot_left[1] and x < self.__width / 2:
                        bot_left = [x, y, w, h]
                    if y < self.__height - 1 and y > bot_right[1] and x > self.__width / 2:
                        bot_right = [x, y, w, h] 
        # for square in [top_left, top_right, bot_left, bot_right]:
        #     self.__display_square(square)

        print(top_left, top_right, bot_left, bot_right)
        self.__top_left = top_left
        self.__top_right = top_right
        self.__bot_left = bot_left
        self.__bot_right = bot_right

        self.__box_width = int((top_left[2] + top_right[2] + bot_left[2]) / 3)
        self.__box_height = int((top_left[3] + top_right[3] + bot_left[3]) / 3)

    def find_top_left_cell(self):        
        top_left = int(self.__top_left[1] + (1.5 * self.__box_height))

        search_x = self.__top_left[0]
        search_y = top_left

        img = self.__crop_image(self.__image, search_x, search_y, self.__box_width, int(1.5 * self.__box_height))

        thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)[1]
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            perimeter = cv2.arcLength(contour, False)
            approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
            x, y, w, h = cv2.boundingRect(approx)

            if w > self.__box_width / 2 and h > self.__box_height / 2:
                self.__display_cropped_image(search_x+x, search_y+y, int(self.__box_width*0.7), int(self.__box_height*1.1))

        self.__display_cropped_image(self.__top_left[0], top_left, self.__box_width, self.__box_height)

        return self.__top_left[0], top_left, self.__box_width, self.__box_height

    def test_find_top_left_cell(self):
        gridImage.find_top_left_cell()       
        #self.__display_cropped_image(x, y, 300, 300)
        
        

gridImage = GridImage("test_grids/grid_image_2.jpg")
gridImage.find_squares()
print(gridImage.test_find_top_left_cell())
