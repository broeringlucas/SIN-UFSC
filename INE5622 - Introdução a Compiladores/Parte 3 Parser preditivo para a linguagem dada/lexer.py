# Lucas Broering - 22100909
from ply.lex import lex

class LexicalAnalyzer:
    def __init__(self):
        # Palavras reservadas
        self.reserved = {
            'int': 'INT',
            'if': 'IF',
            'else': 'ELSE',
            'def': 'DEF',
            'print': 'PRINT',
            'return': 'RETURN',
        }

        # Tokens
        self.tokens = [
            'ID',
            'IDF',
            'NUM',
            'MENOR',
            'MAIOR',
            'MENORIGUAL',
            'MAIORIGUAL',
            'DIFERENTE',
            'IGUAL',
            'SOMA',
            'SUBTRACAO',
            'MULTIPLICACAO',
            'DIVISAO',
            'ATRIBUICAO',
            'LPAREN',
            'RPAREN',
            'LCHAVES',
            'RCHAVES',
            'VIRGULA',
            'PONTO_VIRGULA',
        ] + list(self.reserved.values())

        # Mapear tokens para seus símbolos
        self.symbol_map = {
            'MENOR': '<',
            'MAIOR': '>',
            'MENORIGUAL': '<=',
            'MAIORIGUAL': '>=',
            'DIFERENTE': '<>',
            'IGUAL': '=',
            'SOMA': '+',
            'SUBTRACAO': '-',
            'MULTIPLICACAO': '*',
            'DIVISAO': '/',
            'ATRIBUICAO': ':=',
            'LPAREN': '(',
            'RPAREN': ')',
            'LCHAVES': '{',
            'RCHAVES': '}',
            'VIRGULA': ',',
            'PONTO_VIRGULA': ';',
        }

        self.lexer = lex(module=self)

    # Definição de tokens
    t_ignore = ' \t'
    t_MENOR = r'<'
    t_MAIOR = r'>'
    t_MENORIGUAL = r'<='
    t_MAIORIGUAL = r'>='
    t_DIFERENTE = r'<>'
    t_IGUAL = r'='
    t_SOMA = r'\+'
    t_SUBTRACAO = r'-'
    t_MULTIPLICACAO = r'\*'
    t_DIVISAO = r'/'
    t_ATRIBUICAO = r':='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LCHAVES = r'\{'
    t_RCHAVES = r'\}'
    t_VIRGULA = r','
    t_PONTO_VIRGULA = r';'

    # Token para identificadores (ID)
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')  # Se for palavra reservada, atribui tipo correspondente
        return t

    def t_NUM(self, t):
        r'\d+'
        t.value = int(t.value)  # Converte o valor para inteiro
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Tratamento de erros
    def t_error(self, t):
        print(f'Caractere inválido {t.value[0]!r} na linha {t.lineno}, posição {t.lexpos}.')
        t.lexer.skip(1)

    # Método para analisar o código fonte
    def generate_tokens(self, data):
        self.lexer.input(data)
        token_list = []

        for tok in self.lexer:
            token_list.append(tok)

        # Processar os tokens para identificar IDF
        for i in range(len(token_list)):
            previous_token = token_list[i - 1] if i > 0 else None  # Token anterior
            next_token = token_list[i + 1] if i + 1 < len(token_list) else None  # Token seguinte

            # Verifica se o token atual é ID e se o anterior é ATRIBUICAO e o próximo é LPAREN
            if token_list[i].type == 'ID' and previous_token and next_token:
                if previous_token.type == 'ATRIBUICAO' and next_token.type == 'LPAREN':
                    # Substitui o ID por IDF
                    token_list[i].type = 'IDF'

        # Converter os tipos dos tokens para seus símbolos
        return [self.symbol_map.get(tok.type, tok.type.lower()) for tok in token_list]

    # Método para ler o arquivo de teste
    @staticmethod
    def read_data():
        arquivo_test = input("Digite o caminho do arquivo de teste (com extensão): ")
        with open(arquivo_test, mode="r", encoding="utf-8") as file:
            return file.read()

if __name__ == "__main__":
    analyzer = LexicalAnalyzer()
    data = analyzer.read_data()
    tokens = analyzer.generate_tokens(data)

