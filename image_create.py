from PIL import Image, ImageDraw, ImageFont

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

    rotated = rotate_image(image, angle_degrees)

    return rotated
