class fd: 
    def __init__(self, transitions, accepting_states):
        self.current_state = 0
        self.transitions = transitions
        self.accepting_states = accepting_states

    def reset(self):
        self.current_state = 0

    def is_accept(self):
        return self.current_state in self.accepting_states
    
    def process(self, char):
        input_type = self.get_input_type(char)
        if input_type in self.transitions[self.current_state]:
            self.current_state = self.transitions[self.current_state][input_type]
        else:
            self.current_state = -1

    def get_token(self):
        return self.accepting_states.get(self.current_state, "INVALID_TOKEN")
    