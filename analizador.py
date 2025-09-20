# analizador.py
import ply.lex as lex
import ply.yacc as yacc

# --- DEFINICIÓN DEL ANALIZADOR LÉXICO (LEXER) ---

# Lista de palabras reservadas
reserved = {
    'if': 'IF',
    'for': 'FOR',
    'while': 'WHILE'
}

# Lista de nombres de tokens. Siempre es requerida.
tokens = [
    'ID',
    'NUMERO',
    'OPERADOR',
    'PI',  # Paréntesis Izquierdo
    'PD',  # Paréntesis Derecho
    'LLAVEI',
    'LLAVED',
    'DELIMITADOR'
] + list(reserved.values())

# Expresiones regulares para tokens simples
t_OPERADOR = r'<=|>=|\+\+|[<>/+]'
t_PI = r'\('
t_PD = r'\)'
t_LLAVEI = r'\{'
t_LLAVED = r'\}'
t_DELIMITADOR = r'[;,]'

# Regla para números
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regla para identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID')  # Revisa si es una palabra reservada
    return t

# Regla para contar números de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espacios y tabs
t_ignore = ' \t'

# Regla para manejar errores léxicos
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# --- DEFINICIÓN DEL ANALIZADOR SINTÁCTICO (PARSER) ---

# Variable para almacenar el resultado del análisis
error_sintactico = None

def p_programa(p):
    '''
    programa : sentencias
    '''
    p[0] = "Programa válido"

def p_sentencias(p):
    '''
    sentencias : sentencia sentencias
               | sentencia
    '''
    pass

def p_sentencia(p):
    '''
    sentencia : if_sentencia
              | for_sentencia
              | while_sentencia
              | asignacion DELIMITADOR
    '''
    pass

def p_if_sentencia(p):
    '''
    if_sentencia : IF PI expresion PD LLAVEI sentencias LLAVED
    '''
    pass

def p_for_sentencia(p):
    '''
    for_sentencia : FOR PI asignacion DELIMITADOR expresion DELIMITADOR asignacion PD LLAVEI sentencias LLAVED
    '''
    pass

def p_while_sentencia(p):
    '''
    while_sentencia : WHILE PI expresion PD LLAVEI sentencias LLAVED
    '''
    pass

def p_asignacion(p):
    '''
    asignacion : ID OPERADOR expresion
               | ID OPERADOR ID
    '''
    pass

def p_expresion(p):
    '''
    expresion : ID OPERADOR NUMERO
              | ID OPERADOR ID
              | NUMERO
              | ID
    '''
    pass

# Regla para manejar errores de sintaxis
def p_error(p):
    global error_sintactico
    if p:
        error_sintactico = f"Error de sintaxis en el token '{p.value}' (tipo: {p.type}) en la línea {p.lineno}"
    else:
        error_sintactico = "Error de sintaxis: fin de entrada inesperado."

# Construir el parser
parser = yacc.yacc()

# --- FUNCIONES DE INTERFAZ ---

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
    error_sintactico = None # Reiniciar el error en cada análisis
    lexer.lineno = 1 # Reiniciar el contador de líneas del lexer
    parser.parse(texto, lexer=lexer)
    if error_sintactico:
        return error_sintactico
    return "Análisis sintáctico exitoso. La estructura es correcta."