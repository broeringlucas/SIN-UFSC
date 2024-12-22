# Lucas Broering - 22100909
from lexer import LexicalAnalyzer
from parser_preditivo import Parser

if __name__ == "__main__":
    lexer = LexicalAnalyzer()
    data = lexer.read_data()
    lexer.generate_tokens(data)

    print(lexer.generate_tokens(data))

    terminals = [
        '$', 'def', 'id', '(', ')', '{', '}', 'int', ',', ';', ':=', 'idf', 'print', 'return', 
        'if', 'else', '<', '<=', '>', '>=', '==', '<>', '+', '-', '*', '/', 'num'
    ]

    non_terminals = [
        "S", "MAIN", "FLIST", "FLIST'", "FDEF", "PARLIST", "PARLIST'", "VARLIST", "VARLIST'", "STMT",
        "ATRIBST", "ATREXPR", "FCALL", "PARLISTCALL", "PARLISTCALL'", "PRINTST", "RETURNST", "RETURNEXPR",
        "IFSTMT", "IFSTMT'", "STMTLIST", "STMTLIST'", "EXPR", "EXPR'", "NUMEXPR", "NUMEXPR'", "TERM", "TERM'", "FACTOR"
    ]

    parsing_table = [
        ["MAIN", "MAIN", "MAIN", None, None, "MAIN", None, "MAIN", None, "MAIN", None, None, "MAIN", "MAIN", "MAIN", None, None, None, None, None, None, None, None, None, None, None, None],
        ["ε", "FLIST", "STMT", None, None, "STMT", None, "STMT", None, "STMT", None, None, "STMT", "STMT", "STMT", None, None, None, None, None, None, None, None, None, None, None, None],
        [None, "FDEF FLIST'", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        ["ε", "FLIST", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, "def id ( PARLIST ) { STMTLIST }", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, "ε", None, None,"int id PARLIST'",None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, "ε", None, None, None,", int id PARLIST'", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, "id VARLIST'", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None,", VARLIST", "ε", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, "ATRIBST ;", None, None, "{ STMTLIST } ;", None, "int VARLIST ;", None, ";", None, None, "PRINTST ;", "RETURNST ;", "IFSTMT ;", None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, "id := ATREXPR", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, "EXPR", "EXPR", None, None, None, None, None, None, None, "FCALL", None, None, None, None, None, None, None, None, None, None, None, None, None, None, "EXPR"],
        [None, None, None, None, None, None, None, None, None, None, None, "idf ( PARLISTCALL )", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, "id PARLISTCALL'", None, "ε", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, "ε", None, None, None, ", PARLISTCALL", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, "print EXPR", None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, "return RETURNEXPR" , None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, "id", None, None, None, None, None, None, "ε", None, None, None, None , None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None , "if ( EXPR ) STMT IFSTMT'", None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, "ε", None, None, None, None , None, "else STMT", None, None, None, None, None, None, None, None, None, None, None],
        [None, None, "STMT STMTLIST'", None, None, "STMT STMTLIST'", None, "STMT STMTLIST'", None, "STMT STMTLIST'", None, None, "STMT STMTLIST'","STMT STMTLIST'","STMT STMTLIST'", None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, "STMT STMTLIST'", None, None, "STMT STMTLIST'", "ε", "STMT STMTLIST'", None, "STMT STMTLIST'", None, None, "STMT STMTLIST'","STMT STMTLIST'","STMT STMTLIST'",None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, "NUMEXPR EXPR'","NUMEXPR EXPR'",None, None, None, None, None, None, None, None, None, None , None, None, None, None, None, None, None, None, None, None, None, None,"NUMEXPR EXPR'"],
        [None, None, None, None, "ε", None, None, None, None, "ε", None, None, None, None , None, None, "< NUMEXPR", "<= NUMEXPR", "> NUMEXPR", ">= NUMEXPR", "== NUMEXPR", "<> NUMEXPR", None, None, None, None, None],
        [None, None, "TERM NUMEXPR'", "TERM NUMEXPR'", None, None, None, None, None, None, None, None, None, None , None, None, None, None, None, None, None, None, None, None, None, None, "TERM NUMEXPR'"],
        [None, None, None, None, "ε", None, None, None, None, "ε", None, None, None, None , None, None, "ε", "ε", "ε", "ε", "ε", "ε", "+ TERM NUMEXPR'", "- TERM NUMEXPR'", None, None, None],
        [None, None, "FACTOR TERM'", "FACTOR TERM'", None, None, None, None, None, None, None, None, None, None , None, None, None, None, None, None, None, None, None, None, None, None, "FACTOR TERM'"],
        [None, None, None, None, "ε", None, None, None, None, "ε", None, None, None, None , None, None, "ε", "ε", "ε", "ε", "ε", "ε", "ε", "ε", "* FACTOR TERM'", "/ FACTOR TERM'", None],
        [None, None, "id", "( NUMEXPR )", None, None, None, None, None, None, None, None, None, None , None, None, "else STMT", None, None, None, None, None, None, None, None, None, "num"],
    ]

    parser = Parser(parsing_table, 'S', terminals, non_terminals)
    result = parser.parse(lexer.generate_tokens(data))



