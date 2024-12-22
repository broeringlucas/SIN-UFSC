# Lucas Broering - 22100909
class Parser:
    def __init__(self, parsing_table, start_symbol, terminals, non_terminals):
        self.parsing_table = parsing_table
        self.start_symbol = start_symbol
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.stack = []
        self.derivations = []
    
    def parse(self, w):
        # Adiciona o token "$" ao final
        w.append('$')
        
        # Inicializa a pilha com o símbolo inicial e o delimitador $.
        self.stack = ['$']
        self.stack.append(self.start_symbol)
        
        # Inicializa o símbolo de entrada (primeiro token da cadeia)
        a = w.pop(0)
        
        self.productions = [] 

        while self.stack: # Enquanto a pilha não estiver vazia
            # Símbolo no topo da pilha
            X = self.stack.pop()

            if X in self.terminals:  # Se X for terminal
                if X == a:
                    print(f"Match: {a}")
                    if w:  # Se ainda houver símbolos na entrada
                        a = w.pop(0)  # Consome o próximo símbolo
                else:
                    print(f"Erro: Terminal inesperado '{a}'. Esperado '{X}'.")
                    return False
            
            elif X in self.non_terminals:  # Se X for não-terminal
                # Busca a produção na tabela de parsing
                row = self.non_terminals.index(X)
                col = self.terminals.index(a)
                production = self.parsing_table[row][col]

                print(f"Analisando: {X} e {a}")

                if production == None:  # É uma entrada de erro
                    print(f"Erro: Produção inválida para '{X}' e '{a}'.")
                    return False
                else:
                    print(f"Produção usada: {X} -> {production}")
                    self.productions.append(f"{X} -> {production}")

                    # Empilha a produção na ordem correta
                    if production != 'ε':
                        for symbol in reversed(production.split()):
                            self.stack.append(symbol)
            else:
                print(f"Erro: Símbolo inesperado '{X}'.")
                return False
            
        # Verifica se toda a entrada foi consumida
        if a == '$':
            print("Sucesso: Cadeia aceita.")
            # print("Produções usadas:")
            # for derivation in self.derivations:
            #     print(derivation)
            return True
