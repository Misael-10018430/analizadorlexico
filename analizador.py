import ply.lex as lex
import ply.yacc as yacc
reserved = {
    'if': 'IF','for': 'FOR','while': 'WHILE'
}
tokens = [
    'ID','NUMERO', 'OPERADOR','PI',  'PD', 'LLAVEI','LLAVED','DELIMITADOR'
] + list(reserved.values())
t_OPERADOR = r'<=|>=|\+\+|--|\*|/|[<>=+\-]'
t_PI = r'\('
t_PD = r'\)'
t_LLAVEI = r'\{'
t_LLAVED = r'\}'
t_DELIMITADOR = r'[;,]'
def t_NUMERO(t):
    r'\d+[a-zA-Z_][a-zA-Z0-9_]*|\d+'
    if any(c.isalpha() or c == '_' for c in t.value):
        print(f"ERROR LÉXICO: Identificador inválido '{t.value}' en línea {t.lineno}. Los identificadores no pueden empezar con números.")
        t.lexer.skip(len(t.value))
        return None
    else:
        t.value = int(t.value)
        return t
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
t_ignore = ' \t'
def t_error(t):
    print(f"ERROR LÉXICO: Carácter ilegal '{t.value[0]}' en línea {t.lineno}, posición {t.lexpos}. Este carácter no es válido en el lenguaje.")
    t.lexer.skip(1)
lexer = lex.lex()
error_sintactico = None
def p_programa(p):
    '''
    programa : sentencias
    '''
    p[0] = "Programa válido"
def p_sentencias(p):
    '''
    sentencias : sentencia sentencias | sentencia
    '''
    pass
def p_sentencia(p):
    '''
    sentencia : if_sentencia| for_sentencia| while_sentencia| asignacion DELIMITADOR
    '''
    pass
def p_if_sentencia(p):
    '''
    if_sentencia : IF PI expresion PD LLAVEI sentencias LLAVED
    '''
    pass
def p_sentencia_error(p):
    '''
    sentencia : NUMERO ID OPERADOR expresion DELIMITADOR
    '''
    global error_sintactico
    error_sintactico = f"ERROR SINTÁCTICO - Token: '{p[2]}' | Tipo: ID | Línea: {p.lineno(2)}\nIdentificador '{p[2]}' inesperado después de número '{p[1]}'. Los identificadores no pueden empezar con números."
def p_for_sentencia(p):
    '''
    for_sentencia : FOR PI asignacion DELIMITADOR expresion DELIMITADOR expresion_incremento PD LLAVEI sentencias LLAVED
    '''
    pass
def p_while_sentencia(p):
    '''
    while_sentencia : WHILE PI expresion PD LLAVEI sentencias LLAVED
    '''
    pass
def p_asignacion(p):
    '''
    asignacion : ID OPERADOR expresion| ID OPERADOR ID| ID OPERADOR NUMERO
    '''
    pass
def p_asignacion_error(p):
    '''
    asignacion : NUMERO ID| OPERADOR expresion| ID ID
    '''
    global error_sintactico
    if p[1].isdigit() if hasattr(p[1], 'isdigit') else str(p[1]).isdigit():
        error_sintactico = f"ERROR SINTÁCTICO - Token: '{p[2]}' | Tipo: ID | Línea: {p.lineno(2)}\nIdentificador '{p[2]}' inesperado después de número. Los identificadores no pueden empezar con números."
    elif p[1] in ['=', '+', '-', '*', '/', '<', '>', '<=', '>=']:
        error_sintactico = f"ERROR SINTÁCTICO - Token: '{p[1]}' | Tipo: OPERADOR | Línea: {p.lineno(1)}\nOperador '{p[1]}' inesperado al inicio. Falta identificador antes del operador."
def p_expresion_error(p):
    '''
    expresion : OPERADOR NUMERO| OPERADOR ID
    '''
    global error_sintactico
    error_sintactico = f"ERROR SINTÁCTICO - Token: '{p[1]}' | Tipo: OPERADOR | Línea: {p.lineno(1)}\nOperador '{p[1]}' inesperado. Falta identificador o número antes del operador."
def p_expresion(p):
    '''
    expresion : ID OPERADOR NUMERO| ID OPERADOR ID| NUMERO OPERADOR NUMERO| NUMERO OPERADOR ID| ID| NUMERO
    '''
    pass
def p_sentencias_vacia(p):
    '''
    sentencias : 
    '''
    pass
def p_expresion_incremento(p):
    '''
    expresion_incremento : ID OPERADOR| ID OPERADOR NUMERO| ID OPERADOR ID| asignacion
    '''
    pass
def p_error(p):
    global error_sintactico
    if p:
        token_actual = p.value
        tipo_token = p.type
        linea = p.lineno
        info_basica = f"ERROR SINTÁCTICO - Token: '{token_actual}' | Tipo: {tipo_token} | Línea: {linea}"       
        if tipo_token == 'LLAVED':
            descripcion = "Llave de cierre '}}' inesperada. Posible problema: falta delimitador ';' en la línea anterior o estructura incompleta."        
        elif tipo_token == 'LLAVEI':
            descripcion = "Llave de apertura '{{' inesperada. Posible problema: falta paréntesis de cierre ')' antes de la llave."        
        elif tipo_token == 'PD':
            descripcion = "Paréntesis de cierre ')' inesperado. Posible problema: paréntesis desbalanceados o expresión incompleta."       
        elif tipo_token == 'PI':
            descripcion = "Paréntesis de apertura '(' inesperado. Posible problema: falta palabra reservada (if, for, while) antes del paréntesis."        
        elif tipo_token == 'ID':
            descripcion = f"Identificador '{token_actual}' inesperado. Posible problema: falta operador, delimitador ';' o estructura de control incompleta."        
        elif tipo_token == 'OPERADOR':
            descripcion = f"Operador '{token_actual}' inesperado. Posible problema: falta identificador o número antes/después del operador."       
        elif tipo_token == 'NUMERO':
            descripcion = f"Número '{token_actual}' inesperado. Posible problema: falta operador antes del número."        
        elif tipo_token == 'DELIMITADOR':
            descripcion = f"Delimitador '{token_actual}' inesperado. Posible problema: expresión incompleta antes del delimitador."       
        elif tipo_token in ['IF', 'FOR', 'WHILE']:
            descripcion = f"Palabra reservada '{token_actual}' inesperada. Posible problema: estructura de control anterior incompleta o falta delimitador ';'."        
        else:
            descripcion = f"Token '{token_actual}' no válido en esta posición."        
        error_sintactico = f"{info_basica}\n{descripcion}"    
    else:
        error_sintactico = "Error sintactico - Token: N/A | Tipo: N/A | Línea: N/A\nFin de entrada inesperado. El código parece incompleto - posible problema: falta llave de cierre '}}' o delimitador ';'."
parser = yacc.yacc()
def analizar_lexico(texto):
    lexer.input(texto)
    tokens_encontrados = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_encontrados.append(tok)
    return tokens_encontrados
def analizar_sintactico(texto):
    global error_sintactico
    error_sintactico = None
    lexer.lineno = 1 
    parser.parse(texto, lexer=lexer)
    if error_sintactico:
        return error_sintactico
    return "Análisis sintáctico exitoso. La estructura es correcta."