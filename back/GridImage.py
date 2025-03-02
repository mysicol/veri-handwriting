import cv2
import math

class GridImage:
    def __init__(self, filepath):
        self.__filepath = filepath
    
        self.__load_image()
        self.__grayscale_convert()

        self.__height, self.__width = self.__image.shape[:2]
        self.__rotated = False

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
    
    def __rotate_image(self, angle):
        M = cv2.getRotationMatrix2D((self.__height / 2, self.__width / 2), angle, 1)
        self.__image = cv2.warpAffine(self.__image, M, (self.__width, self.__height))

    def mask_image(self, thresh=100):
        test = cv2.threshold(self.__image, thresh, 255, cv2.THRESH_BINARY_INV)[1]
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

        self.__w_approx = int(self.__box_width*0.8)
        self.__h_approx = int(self.__box_height)

        if not self.__rotated:
            self.display()

            self.__rotate_image(math.degrees(math.atan((self.__top_right[1] - self.__top_left[1])/(self.__top_right[0] - self.__top_left[0]))))
            print("inner", self.__top_left[1], self.__top_right[1])

            self.display()

            self.__rotated = True

            self.find_squares()
        
        print("outer", self.__top_left[1], self.__top_right[1])

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
                self.__display_cropped_image(search_x+x, search_y+y, self.__w_approx, self.__h_approx)
                return search_x+x, search_y+y
            
    def find_top_right_cell(self):        
        top_right = int(self.__top_right[1] + (1.5 * self.__box_height))

        search_x = self.__top_right[0]
        search_y = top_right

        img = self.__crop_image(self.__image, search_x, search_y, int(self.__box_width * 1.1), int(1.5 * self.__box_height))

        self.__display_img(img)

        thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)[1]
        self.__display_img(thresh)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
            x, y, w, h = cv2.boundingRect(approx)

            if w > self.__box_width / 2 and h > self.__box_height / 2:
                self.__display_cropped_image(search_x+x, search_y+y, self.__w_approx, self.__h_approx)
                # return search_x+x, search_y+y

    def export_squares(self):
        x, y = self.find_top_left_cell()

        horizontal = 14
        vertical = 11

        approx_cell_width = int(((self.__top_right[0] + self.__top_right[2]) - self.__top_left[0]) / horizontal)
        approx_cell_height = int((((self.__bot_right[1] + self.__bot_right[3]) - self.__top_right[1]) * 0.75) / vertical)

        for h in range(horizontal-1):
            for v in range(vertical-1):
                self.__display_cropped_image(x + approx_cell_width * h, y + approx_cell_height * v, self.__w_approx, self.__h_approx) 

    def __how_crooked(self):
        return self.__top_right[1]  - self.__top_left[1]

gridImage = GridImage("test_grids/grid_image_4.jpg")
gridImage.find_squares()
gridImage.find_top_right_cell()
# print(gridImage.export_squares())
