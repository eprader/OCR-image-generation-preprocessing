import numpy as np
from collections import namedtuple
import text_generator

class ImageData(namedtuple('ImageData', ['text', 'rotation_angle_degrees'])):
    """
    Represents the data based on which a text image will be generated.

    Attributes:
        text (str): The string to be contained in the image.
        rotation_angle_degrees (int):
    """
    pass

class MetaDataGenerator:
    """
    Generates ImageData tuples.

    Attributes:
        character_list (char): List of characters to be contained in the ImageData text string.
        max_string_length (int): Maximum length a generated string is allowed to have.
        random_seed (int): Initial seed for reproducability.
    """
    def __init__(self, character_list, max_string_length, random_seed):
        self.random_seed = random_seed
        np.random.seed(random_seed)
        self.text_gen = text_generator.TextGenerator(character_list, max_string_length, random_seed)

    def generate_random_image_data(self, n):
        """
        Generates a list of ImageData tuples. 

        Parameters:
            n (int): number of image data tuples to be generated (positive integer).

        Returns:
            list (ImageData): The list of ImageData generated.
        """
        return [self._generate_image_data_tuple() for _ in range(n)]

    def _generate_image_data_tuple(self):
        """
        Generates an ImageData tuple.
        """
        rotation_angle_degrees = np.random.choice(range(-181,179))
        text = self.text_gen.generate_random_sequence()
        return ImageData(text, rotation_angle_degrees)
