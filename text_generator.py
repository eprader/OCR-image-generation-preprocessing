import numpy as np

class TextGenerator:
    """
    This class allows  you to generate a random string based on a custom character_list.

    Attributes:
        character_list (char): A list of characters to be contained in the generated string. 
        max_string_length (int): The maximum length the generated strnig is allowed to have.
        random_seed (int): The seed for the random generator for reproducability.
    """
    def __init__(self, character_list, max_string_length, random_seed):
        self.character_list = character_list
        self.max_string_length = max_string_length
        self.random_seed = random_seed
        np.random.seed(random_seed)

    def generate_random_sequence(self):
        """
        Generates a random string sequence.
        """
        sequence = ""
        previous_char = None

        length = np.random.choice(range(1, self.max_string_length))

        for _ in range(length):
            char = np.random.choice(self.character_list)
            if char == ' ' or char == '\n':
                if previous_char != ' ' or None or '\n':
                    sequence += '\n'
            else:
                sequence += char

            previous_char = char

        return sequence
