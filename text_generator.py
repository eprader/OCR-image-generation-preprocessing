import numpy as np

class TextGenerator:
    def __init__(self, character_list, random_seed):
        self.character_list = character_list
        self.random_seed = random_seed
        np.random.seed(random_seed)

    def generate_random_sequence(self):

        sequence = ""
        previous_char = None

        length = np.random.choice(range(1, 50))

        for _ in range(length):
            char = np.random.choice(self.character_list)
            if char == ' ' or char == '\n':
                if previous_char != ' ' or None or '\n':
                    sequence += '\n'
            else:
                sequence += char

            previous_char = char

        return sequence
