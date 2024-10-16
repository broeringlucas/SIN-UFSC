from fd import fd 
from identifierFd import IdentifierFd
from numberFd import NumberFd
from relationalOperatorFd import RelationalOperatorFd

def identify_token(automaton, string):
    automaton.reset()  
    for char in string:
        automaton.process(char)  
        if automaton.current_state == -1:
            return "INVALID_TOKEN"
    return automaton.get_token()  

identifier_automaton = IdentifierFd()  
number_automaton = NumberFd() 
relational_operator_automaton = RelationalOperatorFd()  

test_strings = ["var123", "123", "12.34", "<=", "!=", "==", "123var", "var_123", "var!"]

for string in test_strings:
    if string[0].isalpha():  
        token_type = identify_token(identifier_automaton, string)
    elif string[0].isdigit(): 
        token_type = identify_token(number_automaton, string)
    elif string[0] in ['<', '>', '=', '!']:  
        token_type = identify_token(relational_operator_automaton, string)
    else:
        token_type = "INVALID_TOKEN"  
    
    print(f"'{string}' é um {token_type}")
