import image_create
import preprocess
import text_generator
import numpy as np
import cv2 as cv
import string

FONT_PATH = preprocess.FONT_PATH

if __name__ == "__main__":
    text = "tester\n\nsecond line\nthird line\n\n top"
    image = np.array(image_create.createimage(text, FONT_PATH, angle_degrees=180))
    cv.imwrite(f"{text}_render.png", image)
    preprocess.preprocess(text + "_render")
    character_string = string.ascii_lowercase + " \n"
    generator = text_generator.Generator([*character_string], 42)
    print(generator.generate_random_sequence())
    print(generator.generate_random_sequence())
    print(generator.generate_random_sequence())
    print(generator.generate_random_sequence())
