import re

token_specification = [
    ('NUMBER', r'\d+(\.\d*)?'),          # Números inteiros ou decimais
    ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),  # Identificadores
    ('REL_OP', r'<=|>=|==|!=|<|>'),      # Operadores relacionais
    ('ASSIGN', r'='),                    # Operador de atribuição
    ('PLUS', r'\+'),                     # Operador de soma
    ('MINUS', r'-'),                     # Operador de subtração
    ('MULTIPLY', r'\*'),                 # Operador de multiplicação
    ('DIVIDE', r'/'),                    # Operador de divisão
    ('LPAREN', r'\('),                   # Parêntese esquerdo
    ('RPAREN', r'\)'),                   # Parêntese direito
    ('SEMICOLON', r';'),                 # Ponto e vírgula
    ('LBRACE', r'\{'),                   # Chave esquerda
    ('RBRACE', r'\}'),                   # Chave direita
    ('SKIP', r'[ \t]+'),                 # Ignorar espaços em branco
    ('NEWLINE', r'\n'),                  # Quebra de linha
    ('MISMATCH', r'.'),                  # Qualquer outro caractere inválido
]

token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)


def tokenize(code):
    line_num = 1
    line_start = 0
    tokens = []

    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group(kind)
        column = match.start() - line_start
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'NEWLINE':
            line_start = match.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} inesperado na linha {line_num}')
        tokens.append((kind, value, line_num, column))
    return tokens

if __name__ == '__main__':
    test_input = '''
    var123 = 42;
    if (var123 >= 10) {
        var_name = 12.34 + 5;
    }
    '''

    tokens = tokenize(test_input)
    for token in tokens:
        print(token)
