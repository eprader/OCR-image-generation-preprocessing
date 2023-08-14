import image_generator
import preprocess
import text_generator
import numpy as np
import cv2 as cv
import string

FONT_PATH = preprocess.FONT_PATH

if __name__ == "__main__":
    text = "tester\n\nsecond line\nthird line\n\n top"
    image_generator = image_generator.ImageGenerator(FONT_PATH, 40)
    image = np.array(image_generator.createimage(text, 20))
    cv.imwrite(f"{text}_render.png", image)
    preprocess.preprocess(text + "_render")
    character_string = string.ascii_lowercase + " \n"
    generator = text_generator.TextGenerator([*character_string], 50, 42)
    print(generator.generate_random_sequence())
    print(generator.generate_random_sequence())
    print(generator.generate_random_sequence())
    print(generator.generate_random_sequence())
