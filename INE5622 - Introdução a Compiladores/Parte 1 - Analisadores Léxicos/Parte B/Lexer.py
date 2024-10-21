# Aluno: Lucas Broering dos Santos

from ply.lex import lex

# Palavras reservadas
reserved = {
    'def': 'DEF',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'break': 'BREAK',
    'print': 'PRINT',
    'call': 'CALL',
    'read': 'READ',
    'return': 'RETURN',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'new': 'NEW',
    'null': 'NULL',
}

# Tokens
tokens = [
    'ID',
    'FLOAT_CONSTANT',
    'INT_CONSTANT',
    'STRING_CONSTANT',
    'MENOR',
    'MENORIGUAL',
    'IGUAL',
    'DIFERENTE',
    'MAIOR',
    'MAIORIGUAL',
    'LPAREN',
    'PONTO_VIRGULA',
    'LCOLCHETES',
    'RCOLCHETES',
    'ATRIBUICAO',
    'SOMA',
    'SUBTRACAO',
    'MULTIPLICACAO',
    'RPAREN',
    'LCHAVES',
    'RCHAVES',
    'VIRGULA',
    'DIVISAO',
    'RESTO',
    'IGUAL_IGUAL',
] + list(reserved.values())

# Mapear tokens para seus símbolos
symbol_map = {
    'LPAREN': '(',
    'RPAREN': ')',
    'LCHAVES': '{',
    'RCHAVES': '}',
    'VIRGULA': ',',
    'PONTO_VIRGULA': ';',
    'LCOLCHETES': '[',
    'RCOLCHETES': ']',
    'MENOR': '<',
    'MAIOR': '>',
    'MENORIGUAL': '<=',
    'MAIORIGUAL': '>=',
    'IGUAL': '==',
    'DIFERENTE': '!=',
    'SOMA': '+',
    'SUBTRACAO': '-',
    'MULTIPLICACAO': '*',
    'DIVISAO': '/',
    'RESTO': '%',
    'IGUAL_IGUAL': '==',
    'ATRIBUICAO': ':=',
}

# Definição de tokens
t_ignore = ' \t'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCHAVES = r'\{'
t_RCHAVES = r'\}'
t_VIRGULA = r','
t_PONTO_VIRGULA = r';'
t_LCOLCHETES = r'\['
t_RCOLCHETES = r'\]'
t_MENOR = r'<'
t_MAIOR = r'>'
t_MENORIGUAL = r'<='
t_IGUAL = r'=='
t_DIFERENTE = r'!='
t_MAIORIGUAL = r'>='
t_SOMA = r'\+'
t_SUBTRACAO = r'-'
t_MULTIPLICACAO = r'\*'
t_DIVISAO = r'/'
t_RESTO = r'%'
t_IGUAL_IGUAL = r'=='

# Funções para os tokens especiais
def t_ATRIBUICAO(t):
    r':=|='
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_FLOAT_CONSTANT(t):
    r'\d+\.\d*|\.\d+|\d+\.'
    t.value = float(t.value)
    return t

def t_INT_CONSTANT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_CONSTANT(t):
    r'\"([^\\\"]|\\.)*\"'
    t.value = t.value[1:-1]
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erros
def t_error(t):
    print(f'Caractere inválido {t.value[0]!r} na linha {t.lineno}, posição {t.lexpos}.')
    t.lexer.skip(1)

# Função para ler o arquivo de teste, pede um input do usuário
def read_data():
    arquivo_test = input("Digite o caminho do arquivo de teste(com extensão): ")
    with open(arquivo_test, mode="r", encoding="utf-8") as file:
        return file.read()

lexer = lex()

def analyse_lex(data):
    lexer.input(data)
    token_list = []

    for tok in lexer:
        token = symbol_map.get(tok.type, tok.type.lower())
        token_list.append(token)

    print(f"[{' , '.join(token_list)}]")

if __name__ == "__main__":
    data = read_data()
    analyse_lex(data)
