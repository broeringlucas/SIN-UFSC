from fd import fd 

class NumberFd(fd):
    def __init__(self):
        transitions = {
            0: {'DIGIT': 1},
            1: {'DIGIT': 1, 'DOT': 2},
            2: {'DIGIT': 3},
            3: {'DIGIT': 3}
        }
        accepting_states = {
            1: 'NUMBER_INT',
            3: 'NUMBER_FLOAT'
        }
        super().__init__(transitions, accepting_states)

    def get_input_type(self, char):
        if char.isdigit():
            return 'DIGIT'
        elif char == '.':
            return 'DOT'
        else:
            return 'ERROR'