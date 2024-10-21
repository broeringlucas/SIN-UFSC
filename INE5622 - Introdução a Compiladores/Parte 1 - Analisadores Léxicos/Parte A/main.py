# Aluno: Lucas Broering dos Santos

from PartialLexer import PartialLexer

# Aqui quando rodar vai pedir para digitar um caminho de arquivo, no diretorio tests tem 2 arquivos de test
arquivo_test = input("Digite o caminho do arquivo de teste(com extensão): ")
lexer = PartialLexer(arquivo_test) 
while True:
    token = lexer.scan()
    if token is None:
        break

# Imprimindo a tabela de símbolos e a lista de tokens
lexer.print_symbol_table()
lexer.format_tokens()
lexer.print_tokens()