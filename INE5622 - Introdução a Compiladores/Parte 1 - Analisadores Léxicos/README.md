# Parte 1 - Analisadores Léxicos

## Estrutura

```
Parte 1 - Analisadores Léxicos/
/── Parte A/
    /── PartialLexer.py
    /── tests
        /── testA_1.lsi
        /── testA_2.lsi
/── Parte B/
    /── Lexer.py
    /── tests
        /── testB_1.lsi
        /── testB_2.lsi
```

## Observaçöes

Os outputs para a parte A e B são uma lista de tokens como abaixo além de uma mensagem de erro, apontando o char inválido e onde ocorreu.

[def, id, (, int, id, , , int, id, ), {, int, id, ..., return, ;, } ].

Na parte A a tabela de símbolos também é mostrada.

## Como rodar o projeto

Na root, rodar o main.py ou Lexer.py, para a parte A ou B, respectivamente.
Tomar cuidado com o input, precisa ser um arquivo válido de test .lsi, no input ele deve ser digitado com a extensão

Ex: Se estiver na root o caminho para o diretório fica o seguinte: Parte B/tests/testB_2.lsi
