# Aluno: Lucas Broering dos Santos

import io

# Implementei os AFD direto na classe Lexer, para cada tipo de token. Cada um é uma função que implementa o AFD para identificar o token correspondente.
# Cada AFD tem uma tabela de transição. A variável self.words é a minha tabela de símbolos, onde eu guardo as palavras reservadas e os identificadores.
# É tratado para que id não seja repetido na tabela.

class Token:
    def __init__(self, tipo, lexema):
        self.tipo = tipo
        self.lexema = lexema

    # Representação do token na hora do print
    def __repr__(self):
        return f"{self.lexema}" 

class Word(Token):
    def __init__(self, tipo, lexema):
        super().__init__(tipo, lexema)

class Num(Token):
    def __init__(self, valor):
        super().__init__('NUM', valor)

class Relop(Token):
    def __init__(self, lexema):
        super().__init__('RELOP', lexema)

class PartialLexer:
    def __init__(self, input_data):
        if isinstance(input_data, str):
            if input_data.endswith('.lsi'): 
                with open(input_data, 'r') as file:
                    self.stream = io.StringIO(file.read()) 
            else:
                self.stream = io.StringIO(input_data)  # Fluxo de entrada de string
        else:
            raise ValueError("O input deve ser uma string ou um caminho para um arquivo.")

        self.nlin = 1 
        self.ncol = 1  
        self.words = {} 
        self.tokens = []  
        self.p = self._peek()  

        # Coloquei algumas palavras reservadas para testar
        self.reserve(Word('IF', 'if'))
        self.reserve(Word('WHILE', 'while'))
        self.reserve(Word('ELSE', 'else'))
        self.reserve(Word('BREAK', 'break'))
        self.reserve(Word('CONTINUE', 'continue'))
        self.reserve(Word('RETURN', 'return'))
        self.reserve(Word('INT', 'int'))
        self.reserve(Word('FLOAT', 'float'))
        self.reserve(Word('VOID', 'void'))
        self.reserve(Word('DEF', 'def'))
        self.reserve(Word('FUNC', 'func'))
        self.reserve(Word('MAIN', 'main'))
        self.reserve(Word('FOR', 'for'))

    def _peek(self):
        pos = self.stream.tell()  # Salva posição atual
        char = self.stream.read(1)  # Lê um caractere
        self.stream.seek(pos)  # Volta para posição original
        return char

    def _advance(self):
        char = self.stream.read(1)  # Lê e consome o caractere
        self.ncol += 1  # Incrementa a coluna
        if char == '\n':  # Se for nova linha, reseta a coluna
            self.nlin += 1
            self.ncol = 1
        self.p = self._peek()  # Faz peek do próximo caractere
        return char

    def reserve(self, word):
        self.words[word.lexema] = word

    def scan(self):
        # Ignorar espaços em branco e novas linhas
        while self.p.isspace():
            self._advance()

        # Relational Operators
        if self.p in {'<', '=', '>'}:
            return self.AFD_RELOPS()
        elif self.p.isdigit():
            return self.AFD_NUMS()
        elif self.p.isalpha():
            return self.AFD_IDS()
        elif self.p:  # Caractere desconhecido
            return self.OUTRO()
        return None  # Fim do input

    def AFD_RELOPS(self):
        # Definindo os estados e símbolos
        # q0, q1, q2 (LE), q3 (NE), q4 (LT), q5 (EQ), q6, q7 (GE), q8 (GT) 
        # 0: '<', 1: '=', 2: '>', 3: EOF
        
        # Tabela de transição
        tab_transicao = [
            [1, 5, 6, -1],  # Estado 0
            [1, 2, 3, -1],  # Estado 1
            [1, 0, -1, -1],  # Estado 2 (aceitação: LE)
            [1, 0, -1, -1],  # Estado 3 (aceitação: NE)
            [1, 0, -1, -1],  # Estado 4 (aceitação: LT)
            [0, 0, 0, -1],  # Estado 5 (aceitação: EQ)
            [0, 7, 0, -1],  # Estado 6
            [1, 0, -1, -1],  # Estado 7 (aceitação: GE)
            [1, 0, -1, -1]   # Estado 8 (aceitação: GT)
        ]
        
        # Estados de aceitação
        aceita = [False, False, True, True, True, True, False, True, True]
        
        q = 0
        
        while True:
            if self.p == '<':
                simbolo = 0
            elif self.p == '=':
                simbolo = 1
            elif self.p == '>':
                simbolo = 2
            else:
                simbolo = 3 
            
            # Mover para o próximo estado
            q = tab_transicao[q][simbolo]
            if q == -1:
                break
            
            if simbolo != 3:
                self._advance()
            
            if aceita[q]:
                break

        # Criação do token baseado no estado final
        if q == 2:
            token = Relop('LE')  # Operador <=
        elif q == 3:
            token = Relop('NE')  # Operador <>
        elif q == 4:
            token = Relop('LT')  # Operador <
        elif q == 5:
            token = Relop('EQ')  # Operador =
        elif q == 7:
            token = Relop('GE')  # Operador >=
        elif q == 8:
            token = Relop('GT')  # Operador >
        else:
            token = Word('UNK', 'DESCONHECIDO')  # Caso de erro

        self.tokens.append(token)
        return token
    
    def AFD_NUMS(self):
        # Definindo os estados e símbolos
        # q0, q1, q2 
        # 0: dígito, 1: EOF ou caractere não dígito

        # Tabela de transição
        tab_transicao = [
            [1, 2],  # Estado 0: dígito -> Estado 1; não dígito -> Estado 2 (rejeição)
            [1, 2],  # Estado 1: dígito -> Estado 1; não dígito -> Estado 2 (rejeição)
            [2, 2]   # Estado 2: qualquer entrada leva a Estado 2 (rejeição)
        ]
        
        # Estados de aceitação
        aceita = [False, True, False] 

        q = 0
        value = 0 

        while True:
            if self.p.isdigit():  # Se o caractere é um dígito
                simbolo = 0
                value = value * 10 + int(self.p)  # Atualiza o valor acumulado
                self._advance()  # Avança para o próximo caractere
            else:
                simbolo = 1  # EOF ou caractere não válido
                # Se ainda estamos em um estado de aceitação, paramos aqui
                if aceita[q]:  
                    break
                else:
                    # Se não aceitamos o estado, quebramos
                    q = 2  # Força um estado de rejeição
                    break

            # Mover para o próximo estado
            q = tab_transicao[q][simbolo]

        # Criação do token baseado no estado final
        token = Num(value) if q == 1 else Word('UNK', 'DESCONHECIDO')
        
        self.tokens.append(token)
        return token

    def AFD_IDS(self):
        # Definindo os estados e símbolos
        # q0, q1, q2
        # 0: alfanumérico, 1: inválido

        # Tabela de transição
        tab_transicao = [
            [1, 2],  # Estado 0: alfanumérico -> Estado 1; inválido -> Estado 2
            [1, 2],  # Estado 1: alfanumérico -> Estado 1; inválido -> Estado 2
            [2, 2]   # Estado 2: qualquer entrada leva a Estado 2 (rejeição)
        ]

        # Estados de aceitação
        aceita = [False, True, False]  # Aceita apenas o estado 1

        q = 0
        buf = io.StringIO()  # Buffer para armazenar o lexema

        while True:
            if self.p.isalnum():  # Se o caractere é alfanumérico
                simbolo = 0
                buf.write(self.p)  # Adiciona o caractere ao buffer
                self._advance()  # Avança para o próximo caractere
            else:
                simbolo = 1  # Caractere inválido
                break

            # Mover para o próximo estado
            q = tab_transicao[q][simbolo]

            # Se chegamos a um estado de rejeição
            if q == 2:
                break

        # Extrai o lexema do buffer
        lexeme = buf.getvalue()

        # Verifica se já é uma palavra reservada
        if lexeme in self.words:
            self.tokens.append(self.words[lexeme])
            return self.words[lexeme]

        # Se for um novo identificador, cria um novo token
        new_token = Word('ID', lexeme)
        self.words[lexeme] = new_token
        self.tokens.append(new_token)
        return new_token

    def OUTRO(self):
        char = self._advance()
        print(f"Token desconhecido '{char}' na linha {self.nlin}, coluna {self.ncol}")
        return Word('UNK', 'DESCONHECIDO')

    def print_symbol_table(self):
        print("Tabela de Símbolos:")
        print(f"{'Lexema':<15} {'Tipo':<10}")
        print("-" * 25)
        for lexeme, token in self.words.items():
            print(f"{lexeme:<15} {token.tipo:<10}")
        print("-" * 25)

    def format_tokens(self):
        print(f"[{', '.join(repr(token.tipo) for token in self.tokens)}]") 

    def print_tokens(self):
        print("Lista de Tokens:")
        for token in self.tokens:
            print(token.tipo, token.lexema)
