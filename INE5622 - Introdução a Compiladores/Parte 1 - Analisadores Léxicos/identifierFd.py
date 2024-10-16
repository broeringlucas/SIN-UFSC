from fd import fd 


class IdentifierFd(fd):
    def __init__(self):
        transitions = {
            0: {'LETTER': 1},
            1: {'LETTER': 1, 'DIGIT': 1, 'UNDERSCORE': 1}
        }
        accepting_states = {
            1: 'IDENTIFIER'
        }
        super().__init__(transitions, accepting_states)

    def get_input_type(self, char):
        if char.isalpha():
            return 'LETTER'
        elif char.isdigit():
            return 'DIGIT'
        elif char == '_':
            return 'UNDERSCORE'
        else:
            return 'ERROR'
