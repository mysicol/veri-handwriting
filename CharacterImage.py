import cv2
import os
import uuid

class CharacterImage():
    def __init__(self, image, x, y, w, h, save_directory="characters-sample", id=str(uuid.uuid4()), character_type="none", character_neatness="none"):
        self.__image = image[y:y+h, x:x+w]
        self.__image_name = "Character"
        self.__title = character_type + "_" + character_neatness + "_" + id
        self.__save_directory = save_directory
        self.__resize()

    def display(self):
        self.__display_img(self.__image)

    def save(self):
        if not os.path.exists(self.__save_directory):
            os.makedirs(self.__save_directory)
        print(self.__save_directory + "/" + self.__title)
        cv2.imwrite(self.__save_directory + "/" + self.__title + ".png", self.__image)

    def __display_img(self, image):
        cv2.imshow(self.__image_name, cv2.resize(image, (300, 500)))
        cv2.waitKey(0)

    def mask_image(self):
        masked_image = cv2.threshold(self.__image, 100, 255, cv2.THRESH_BINARY_INV)[1]
        self.__display_img(masked_image)