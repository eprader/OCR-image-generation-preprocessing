import image_create
import preprocess
import numpy as np
import cv2 as cv

FONT_PATH = preprocess.FONT_PATH

if __name__ == "__main__":
    text = "tester\n\nsecond line\nthird line\n\n top"
    image = np.array(image_create.createimage(text, FONT_PATH, angle_degrees=180))
    cv.imwrite(f"{text}_render.png", image)
    preprocess.preprocess(text + "_render")

