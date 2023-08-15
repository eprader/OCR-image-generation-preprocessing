from PIL import Image, ImageDraw, ImageFont
import numpy as np

class ImageGenerator:
    def __init__(self, font_path, font_size, padding=10, bg_color=(0, 0, 0), fg_color=(255, 255, 255)):
        self.font = ImageFont.truetype(font_path, font_size)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.padding = padding

    def _get_font_text_size(self, text):
        """
        Returns the projected width and height of the text to be drawn.

        Parameters:
            text (str): The text to be measured in size.

        Returns:
            width (int): width of the text if rendered (in pixels).
            height (int): height of the text if rendered (in pixels).
        """

        image = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(image)

        width, height = draw.textsize(text, font=self.font)

        return width, height

    def _draw_text_image(self, text,):
        """
        Creates an image containing the given text.
        
        Parameters:
            text (str): The text to be contained in the image.

        Returns:
            
        """
        width, height = self._get_font_text_size(text)
        image = Image.new("RGB", (width + 2 * self.padding, height + 2 * self.padding), self.bg_color)
        draw = ImageDraw.Draw(image) 
        text_x_y = (self.padding, self.padding)

        draw.text(text_x_y, text, font=self.font, fill=self.fg_color)

        return image

    def _rotate_image(self, image, angle_degrees):
        """
        Rotates a given image by the given degrees.

        Parameters:
            image (Image): The image to be rotated.
            angle_degrees (int): the degrees the image will be rotated by. If negative the image will be rotated clockwise else counter clockwise
        """
        rotated_text = image.rotate(angle_degrees, resample=Image.BICUBIC, expand=True, fillcolor=self.bg_color)

        return rotated_text

    def createimage(self, text, rotation_angle_degrees = 0):
        """
        Generates the image containing the given text and rotated according to 'rotation_angle_degrees'.

        Parameters:
            text (str): The text to be contained in the image.
            rotation_angle_degrees (int): If negative the image will be rotated clockwise else counter clockwise.

        Returns:
            array () The final image as an np.array.
        """
        image = self._draw_text_image(text)

        rotated = self._rotate_image(image, rotation_angle_degrees)

        return np.array(rotated)
