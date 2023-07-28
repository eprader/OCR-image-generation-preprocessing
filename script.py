from PIL import Image, ImageDraw, ImageFont
import cv2 as cv
import numpy as np

MIN_SOLIDITY = 0.6

BG_COLOR = (0, 0, 0) # black
FG_COLOR = (255, 255, 255) # white

def get_font_text_size(font, text):
    image = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(image)

    width, height = draw.textsize(text, font=font)

    return width, height

def draw_text_image(text, font, text_padding, background_color=BG_COLOR, font_color=FG_COLOR):
    width, height = get_font_text_size(font, text)
    image = Image.new("RGB", (width + 2 * text_padding, height + 2 * text_padding), background_color)
    draw = ImageDraw.Draw(image) 
    text_x_y = (text_padding, text_padding)

    draw.text(text_x_y, text, font=font, fill=font_color)

    return image

def rotate_image(image, angle_degrees, fillcolor=BG_COLOR):
    rotated_text = image.rotate(angle_degrees, resample=Image.BICUBIC, expand=True, fillcolor=fillcolor)

    return rotated_text

def createimage(text, font_path, font_size=40, text_padding=10, angle_degrees = 0):
    font = ImageFont.truetype(font_path, font_size)
    image = draw_text_image(text, font, text_padding=text_padding)
    image.save(f"{text}_render.png")

    rotated = rotate_image(image, angle_degrees)
    rotated.save(f"{text}_render_rotate.png")

    return rotated

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

def find_orientation_with_template_matching(image, template):
    result = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)

    # Find the location of the best match
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    # Get the top-left and bottom-right corners of the matched region
    h, w = template.shape[:2]
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    center_x = (top_left[0] + bottom_right[0]) // 2
    center_y = (top_left[1] + bottom_right[1]) // 2

    angle = np.arctan2(center_y - image.shape[0] // 2, center_x - image.shape[1] // 2) * 180 / np.pi

    return angle

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
    # Initialize SIFT detector
    sift = cv.SIFT_create()

    # Detect keypoints and compute descriptors for both the image and the template
    keypoints1, descriptors1 = sift.detectAndCompute(image, None)
    keypoints2, descriptors2 = sift.detectAndCompute(template, None)

    # Initialize a Brute-Force Matcher
    bf = cv.BFMatcher()

    # Find matches between the descriptors of the image and the template
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # Apply ratio test to filter good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    if len(good_matches) >= 4:
        # Estimate the homography matrix using RANSAC
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)

        if M is not None:
            # Calculate the angle from the homography matrix
            angle = np.arctan2(M[1, 0], M[0, 0]) * 180 / np.pi
            return angle

    return None

def preprocess(name):
    image = cv.imread(f"./{name}.png")
    im_bw = convert_image_black_white(image)
    template = np.array(createimage("t", "./fonts/EnvoyScript.ttf"))
    cv.imwrite(f"template.png",template)
    template = np.array(convert_image_black_white(template))
    cv.imwrite(f"template_bw.png",template)
    angle = find_orientation_with_sift(im_bw, template)
    result = str(angle) if angle != None else "FAILED"
    print(result)
    bbox_image = find_bboxes(im_bw)
    cv.imwrite(f"{name}_bbox.png", bbox_image)


if __name__ == "__main__":
    text = "tester\n\nsecond line\nthird line\n\n top"
    font_path = "./fonts/EnvoyScript.ttf"  # specify the path to your font file
    createimage(text, font_path, angle_degrees=180)
    preprocess(text + "_render_rotate")

