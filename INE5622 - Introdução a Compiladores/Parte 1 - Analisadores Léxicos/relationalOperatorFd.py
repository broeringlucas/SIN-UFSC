from fd import fd

class RelationalOperatorFd(fd):
    def __init__(self):
        transitions = {
            0: {'REL_OP': 1},
            1: {'REL_OP': 2}
        }
        accepting_states = {
            1: 'RELATIONAL_OPERATOR',
            2: 'RELATIONAL_OPERATOR'
        }
        super().__init__(transitions, accepting_states)

    def get_input_type(self, char):
        if char in ['<', '>', '=', '!']:
            return 'REL_OP'
        else:
            return 'ERROR'