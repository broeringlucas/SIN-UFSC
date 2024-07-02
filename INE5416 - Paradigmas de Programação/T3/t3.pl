/* swipl t3.pl */
/* [t3]. */
/* set_prolog_flag(answer_write_options, [max_depth(0)]).*/
/* solucao(Resultado). */

:- use_module(library(clpfd)).

/* Lógica principal */
resolver(Puzzle) :-
    /* Concatena todas as sublistas de Puzzle em uma única lista Lista */
    append(Puzzle, Lista), 
    /* Restringe os valores possíveis de cada célula com base no tamanho da região */
    maplist(valor_maximo_regiao, Lista),
    /* Garante que os valores das células vizinhas são diferentes, com as linhas */
    maplist(vizinhos_diferentes, Puzzle),
    /* Transpõe uma matriz (Puzzle) para obter suas colunas (Colunas) */
    transpose(Puzzle, Colunas),
    /* Garante que os valores das células vizinhas são diferentes, agora com as colunas */
    maplist(vizinhos_diferentes, Colunas),
    /* Garante que o valor de uma célula é maior que o valor da célula acima quando ambas pertencem à mesma região */
    maplist(superior_maior, Colunas),
    /* Agrupa os elementos de cada região */
    agrupar_elementos(0, Lista, Regiao0),
    agrupar_elementos(1, Lista, Regiao1),
    agrupar_elementos(2, Lista, Regiao2),
    agrupar_elementos(3, Lista, Regiao3),
    agrupar_elementos(4, Lista, Regiao4),
    agrupar_elementos(5, Lista, Regiao5),
    agrupar_elementos(6, Lista, Regiao6),
    agrupar_elementos(7, Lista, Regiao7),
    agrupar_elementos(8, Lista, Regiao8),
    agrupar_elementos(9, Lista, Regiao9),
    agrupar_elementos(10, Lista, Regiao10),
    Regioes = [Regiao0, Regiao1, Regiao2, Regiao3, Regiao4, Regiao5, 
              Regiao6, Regiao7, Regiao8, Regiao9, Regiao10], 
    todas_regioes_diferentes(Regioes), !.

/* Define o domínio dos valores que cada célula pode assumir com base no tamanho da região. */
valor_maximo_regiao([R,X]) :- tamanho_regiao(R,T), X in 1..T.

/* Garante que os vizinhos à direita sejam distintos */
vizinhos_diferentes([_]).
vizinhos_diferentes([[_,X1],[R2,X2]|T]) :-
    X1 #\= X2, append([[R2,X2]],T,L), vizinhos_diferentes(L).

/* Garante que o valor acima é maior quando fazem parte do mesmo grupo */
superior_maior([_]).
superior_maior([[R1,X1],[R2,X2]|T]) :-
    (R1 #\= R2 ; X1 #> X2), append([[R2,X2]],T,L), superior_maior(L).

/* Agrupa os elementos que pertencem a mesma regiao */
agrupar_elementos(_, [], []).
agrupar_elementos(R, [[R1, X1] | T], [X1 | L]) :- R #= R1, agrupar_elementos(R, T, L).
agrupar_elementos(R, [[R1, _] | T], L) :- R #\= R1, agrupar_elementos(R, T, L).

/* Verifica se todos os elementos de uma regiao são distintos */
todas_regioes_diferentes([H]) :-
    all_distinct(H).
todas_regioes_diferentes([H|T]) :-
    all_distinct(H),
    todas_regioes_diferentes(T).

/* Chama a função para solucionar o tabuleiro */
solucao(ResultadoTabuleiro) :-
    tabuleiro(ProblemaTabuleiro), 
    resolver(ProblemaTabuleiro),
    extrair_segundos_valores(ProblemaTabuleiro, ResultadoTabuleiro),
    imprimir_matriz(ResultadoTabuleiro).

/* Adquire a lista de cada linha da matriz */
extrair_segundos_valores([], []).
extrair_segundos_valores([Sublista | Resto], [SegundosValores | Resultado]) :-
    extrair_segundo(Sublista, SegundosValores),
    extrair_segundos_valores(Resto, Resultado).

/* Adquire o segundo elemento de cada lista adquirida */
extrair_segundo([], []).
extrair_segundo([[_, Segundo] | Resto], [Segundo | SegundosValores]) :-
    extrair_segundo(Resto, SegundosValores).

/* Imprime a matriz de forma legível */
imprimir_matriz([]).
imprimir_matriz([Linha|Resto]) :-
    writeln(Linha),
    imprimir_matriz(Resto).

/* Esta definição representa o tabuleiro como uma lista de listas, onde cada célula é uma sub-lista com dois elementos:
a região e o valor (ou variável se o valor não estiver definido). */
/* https://www.janko.at/Raetsel/Kojun/003.a.htm */

tabuleiro([[[1,_],[2,_],[3,_],[3,_],[4,_],[4,2]],
            [[1,2],[2,_],[5,_],[4,5],[4,_],[4,_]],
            [[1,_],[1,_],[5,_],[5,_],[5,_],[6,4]],
            [[8,_],[8,_],[7,_],[6,3],[6,_],[6,1]],
            [[8,_],[8,_],[7,_],[9,_],[0,_],[0,_]],
            [[10,_],[10,_],[9,3],[9,_],[9,2],[9,5]]]).

/* Define a quantidade de elementos em cada região, sendo o primeiro valor a região e o segundo a quantidade de elementos.*/
tamanho_regiao(0,2).
tamanho_regiao(1,4).
tamanho_regiao(2,2).
tamanho_regiao(3,2).
tamanho_regiao(4,5).
tamanho_regiao(5,4).
tamanho_regiao(6,4).
tamanho_regiao(7,2).
tamanho_regiao(8,4).
tamanho_regiao(9,5).
tamanho_regiao(10,2).

