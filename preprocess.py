import numpy as np
import cv2 as cv
import string
import image_create

MIN_SOLIDITY = 0.6

BG_COLOR = (0, 0, 0) # black
FG_COLOR = (255, 255, 255) # white

FONT_PATH = "./fonts/EnvoyScript.ttf"

def convert_image_black_white(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    mean_intensity = np.mean(gray)

    if mean_intensity < 128:
        # Dark text on a light background
        _, im_bw = cv.threshold(gray, 90, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    else:
        # Light text on a dark background
        _, im_bw = cv.threshold(gray, 90, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    return im_bw

def find_bboxes(im_bw):
    kernal = cv.getStructuringElement(cv.MORPH_RECT, (15, 45))
    dilate = cv.dilate(im_bw, kernal, iterations=1)

    contours = cv.findContours(dilate, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    contours = sorted(contours, key=lambda x: cv.boundingRect(x)[0])

    image_height, image_width = im_bw.shape[:2]
    min_width = int(0.1 * image_width)
    min_height = int(0.1 * image_height)

    for contour in contours:
        # Get the rotated bounding box for the contour
        rect = cv.minAreaRect(contour)
        box = cv.boxPoints(rect)
        box = np.intp(box)

        # Calculate the width and height of the rotated bounding box
        width = np.linalg.norm(box[0] - box[1])
        height = np.linalg.norm(box[1] - box[2])

        # Adjust the minimum width and height based on the image size
        min_width = int(0.1 * min(im_bw.shape[1], im_bw.shape[0]))
        min_height = int(0.1 * min(im_bw.shape[1], im_bw.shape[0]))

        if width > min_width and height > min_height:
            # Calculate the solidity of the rotated bounding box
            solidity = cv.contourArea(contour) / (width * height)
            if solidity > MIN_SOLIDITY:
                # Draw the rotated bounding box on the image
                cv.drawContours(im_bw, [box], 0, (36, 255, 12), 2) 

    return im_bw

def find_orientation_with_sift(image, template):
    sift = cv.SIFT_create()

    keypoints1, descriptors1 = sift.detectAndCompute(image, None)
    keypoints2, descriptors2 = sift.detectAndCompute(template, None)

    bf = cv.BFMatcher()

    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # NOTE: Estimate homography matrix
    if len(good_matches) >= 4:
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)

        if M is not None:
            angle = np.arctan2(M[1, 0], M[0, 0]) * 180 / np.pi
            return angle

    return None

def average_rotation_angle_over_alphabet(image, alphabet):
    alphabet_angles = {}

    for char in alphabet:
        template = np.array(image_create.createimage(char, FONT_PATH))

        angle = find_orientation_with_sift(image, template)
        if angle is not None:
            alphabet_angles[char] = angle

    if not alphabet_angles:
        return None

    mean =  np.mean(list(alphabet_angles.values()))

    return mean

def preprocess(name):
    image = cv.imread(f"./{name}.png")
    im_bw = convert_image_black_white(image)
    template = np.array(image_create.createimage("t", FONT_PATH))
    cv.imwrite("template.png",template)
    template = np.array(convert_image_black_white(template))
    cv.imwrite("template_bw.png",template)
    angle = average_rotation_angle_over_alphabet(im_bw, string.ascii_lowercase)
    result = str(angle) if angle != None else "FAILED"
    print(result)
    bbox_image = find_bboxes(im_bw)

    cv.imwrite(f"{name}_bbox.png", bbox_image)
