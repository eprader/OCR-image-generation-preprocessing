import image_generator
from image_metadata_generator import MetaDataGenerator
import preprocess
import text_generator
import numpy as np
import cv2 as cv
import string

FONT_PATH = preprocess.FONT_PATH

if __name__ == "__main__":
    image_generator = image_generator.ImageGenerator(FONT_PATH, 40)
    character_string = string.ascii_lowercase + " \n"
    meta_generator = MetaDataGenerator([*character_string], 50, 42)
    data_list = meta_generator.generate_random_image_data(10)
    for data in data_list:
        image = image_generator.createimage(data.text, data.rotation_angle_degrees)
        cv.imwrite(f"{data.text}_render.png", image)
