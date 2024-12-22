# Parte 3 - Parser preditivo para a linguagem dada

## Estrutura

```
Parte 3 - Parser preditivo para a linguagem dada/

/── tests
    /── test_correto1.lsi
    /── test_correto2.lsi
    /── test_errado1.lsi
    /── test_errado2.lsi
/──lexer.py
/──main.py
/──parser_preditivo.py
```

## Observaçöes

O output gerado são os matchs e as produções utilizadas em ordem de execução dos tokens gerados pelo lexer. Por fim há um print se a cadeia foi aceita. Quando ocorre algum erro, o output é onde aconteceu o erro, se foi em algum terminal ou não terminal que não constava na tabela.

A tabela foi feita da seguinte forma, primeiro declarei os terminais e não terminais e depois fiz uma matriz, a lista de
terminais e não terminais serve para me localizar na matriz. Os demais espaços foram preenchidos com None.

## Como rodar o projeto

Na root, rodar o main.py
Tomar cuidado com o input, precisa ser um arquivo válido de test .lsi, no input ele deve ser digitado com a extensão

Ex: Se estiver na root o caminho para o diretório fica o seguinte: tests/test_errado2.lsi
