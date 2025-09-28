import ply.lex as lex
import ply.yacc as yacc
# Lista de palabras reservadas
reserved = {
    'if': 'IF','for': 'FOR','while': 'WHILE','programa': 'PROGRAMA','int': 'INT','read': 'READ','print': 'PRINT','printf': 'PRINTF','end': 'END'
}
# Lista de nombres de tokens
tokens = [
    'ID','NUMERO', 'OPERADOR','PI',  'PD', 'LLAVEI','LLAVED','DELIMITADOR', 'PUNTO', 'CADENA'
] + list(reserved.values())
# CORREGIDO: Expresiones regulares para tokens simples - agregué más operadores
t_OPERADOR = r'<=|>=|\+\+|--|\*|/|[<>=+\-]'
t_PI = r'\('
t_PD = r'\)'
t_LLAVEI = r'\{'
t_LLAVED = r'\}'
t_DELIMITADOR = r'[;,]'
t_PUNTO = r'\.'
def t_CADENA(t): 
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t
# Regla para números (Reconoce numeros validos, "los identificasores por ejemplo no puede empezar con numeros")
def t_NUMERO(t):
    r'\d+[a-zA-Z_][a-zA-Z0-9_]*|\d+'
    if any(c.isalpha() or c == '_' for c in t.value):
        # Si hay letras después de números, es un error
        print(f"ERROR LÉXICO: Identificador inválido '{t.value}' en línea {t.lineno}. Los identificadores no pueden empezar con números.")
        t.lexer.skip(len(t.value))
        return None
    else:
        t.value = int(t.value)
        return t
# Regla para identificadores y palabras reservadas (identifca variables y funcionaes)
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
    print(f"ERROR LÉXICO: Carácter ilegal '{t.value[0]}' en línea {t.lineno}, posición {t.lexpos}. Este carácter no es válido en el lenguaje.")
    t.lexer.skip(1)
# Construir el lexer
lexer = lex.lex()
# Variable para almacenar el resultado del análisis
error_sintactico = None


def p_programa_completo(p):
    '''
    programa : PROGRAMA ID PI PD LLAVEI declaraciones sentencias LLAVED
    | PROGRAMA ID PI PD LLAVEI sentencias LLAVED
    '''
    p[0] = "Programa válido"
#un programa consiste en una sencuencia de sentencias
def p_programa(p):
    '''
    programa : sentencias
    '''
    p[0] = "Programa válido"
def p_declaraciones(p):
    '''
    declaraciones : declaracion declaraciones
    | declaracion
    '''
    pass
def p_declaracion(p):
    '''
    declaracion : tipo_dato lista_variables DELIMITADOR
    '''
    pass
def p_tipo_dato(p):
    '''
    tipo_dato : INT
    '''
    pass
def p_lista_variables(p):
    '''
    lista_variables : lista_variables DELIMITADOR ID
    | ID
    '''
    pass
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
    | llamada_sistema DELIMITADOR
    | entrada_datos DELIMITADOR
    | salida_datos DELIMITADOR
    | fin_programa DELIMITADOR
    '''
    pass
def p_entrada_datos(p):
    '''
    entrada_datos : READ ID
    '''
    pass
def p_salida_datos(p):
    '''
    salida_datos : PRINT PI argumentos PD
    | PRINT PI CADENA PD
    | PRINTF PI argumentos PD
    | PRINTF PI CADENA PD
    '''
    pass
def p_fin_programa(p):
    '''
    fin_programa : END
    '''
    pass
def p_llamada_sistema(p):
    '''
    llamada_sistema : ID PUNTO ID PI argumentos PD
    '''
    pass
def p_argumentos(p):
    '''
    argumentos : expresion DELIMITADOR argumentos
    | expresion
    | CADENA DELIMITADOR argumentos
    | CADENA
    |
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
def p_programa_error(p):
    '''
    programa : PROGRAMA error
    | ID error
    '''
    global error_sintactico
    error_sintactico = f"ERROR SINTÁCTICO- Estructura de programa incorrecta. Formato esperado: 'programa nombre() {{ ... }}'"
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
    asignacion : ID OPERADOR expresion
    | ID OPERADOR ID
    | ID OPERADOR NUMERO
    '''
    pass

def p_asignacion_error(p):
    '''
    asignacion : NUMERO ID
    | OPERADOR expresion
    | ID ID
    '''
    # Captura errores comunes en asignaciones
    global error_sintactico
    if p[1].isdigit() if hasattr(p[1], 'isdigit') else str(p[1]).isdigit():
        error_sintactico = f"ERROR SINTÁCTICO - Token: '{p[2]}' | Tipo: ID | Línea: {p.lineno(2)}\nIdentificador '{p[2]}' inesperado después de número. Los identificadores no pueden empezar con números."
    elif p[1] in ['=', '+', '-', '*', '/', '<', '>', '<=', '>=']:
        error_sintactico = f"ERROR SINTÁCTICO - Token: '{p[1]}' | Tipo: OPERADOR | Línea: {p.lineno(1)}\nOperador '{p[1]}' inesperado al inicio. Falta identificador antes del operador."
def p_declaracion_error(p):
    '''
    declaracion : INT error DELIMITADOR
    | error ID DELIMITADOR
    '''
    global error_sintactico
    error_sintactico = f"ERROR SINTÁCTICO - Error en declaración de variable. Formato correcto: 'int variable;'"
#Errores para entrada/salida de datos
def p_entrada_error(p):
    '''
    entrada_datos : READ error
    '''
    global error_sintactico
    error_sintactico = f"ERROR SINTÁCTICO - Instrucción READ incorrecta. Formato correcto: 'read variable;'"

def p_salida_error(p):
    '''
    salida_datos : PRINT error
    | PRINTF error
    '''
    global error_sintactico
    if len(p) > 1 and p[1] == 'printf':
        error_sintactico = f"ERROR SINTÁCTICO - Instrucción PRINTF incorrecta. Formato correcto: 'printf(expresion);' o 'printf(\"texto\");'"
    else:
        error_sintactico = f"ERROR SINTÁCTICO - Instrucción PRINT incorrecta. Formato correcto: 'print(expresion);' o 'print(\"texto\");'"
def p_expresion_error(p):
    '''
    expresion : OPERADOR NUMERO
    | OPERADOR ID
    '''
    global error_sintactico
    error_sintactico = f"ERROR SINTÁCTICO - Token: '{p[1]}' | Tipo: OPERADOR | Línea: {p.lineno(1)}\nOperador '{p[1]}' inesperado. Falta identificador o número antes del operador."

# MEJORADO: Expresiones más flexibles
def p_expresion(p):
    '''
    expresion : ID OPERADOR NUMERO
    | ID OPERADOR ID
    | NUMERO OPERADOR NUMERO
    | NUMERO OPERADOR ID
    | ID
    | NUMERO
    | cadena
    | CADENA
    '''
    pass
def p_cadena(p):
    '''
    cadena : ID
    '''
    pass
#Permitir sentencias vacías para manejar bloques correctamente
def p_sentencias_vacia(p):
    '''
    sentencias : 
    '''
    pass
# AGREGADO: Permitir declaraciones vacías
def p_declaraciones_vacia(p):
    '''
    declaraciones :
    '''
    pass
# Regla para incrementos en for que reconoce i++ correctamente
def p_expresion_incremento(p):
    '''
    expresion_incremento : ID OPERADOR
    | ID OPERADOR NUMERO
    | ID OPERADOR ID
    | asignacion
    '''
    pass
# Regla para manejar errores de sintaxis 
def p_error(p):
    global error_sintactico
    if p:
        token_actual = p.value
        tipo_token = p.type
        linea = p.lineno
        # INFORMACIÓN BÁSICA DEL ERROR
        info_basica = f"ERROR SINTÁCTICO - Token: '{token_actual}' | Tipo: {tipo_token} | Línea: {linea}"       
        # DESCRIPCIÓN ESPECÍFICA según el contexto - AMPLIADA
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
        # AGREGADO: Manejo de errores para nuevas palabras reservadas        
        elif tipo_token in ['PROGRAMA', 'INT', 'READ', 'PRINT', 'PRINTF', 'END']:
            descripcion = f"Palabra reservada '{token_actual}' inesperada en esta posición. Verifique la estructura del programa."
        elif tipo_token == 'CADENA':
            descripcion = f"Cadena '{token_actual}' inesperada. Posible problema: falta función print() o printf() o paréntesis."
        else:
            descripcion = f"Token '{token_actual}' no válido en esta posición."        
        
        # COMBINAR INFORMACIÓN BÁSICA + DESCRIPCIÓN
        error_sintactico = f"{info_basica}\n{descripcion}"    
    else:
        error_sintactico = f"Error sintactico - Token: N/A | Tipo: N/A | Línea: N/A\nFin de entrada inesperado. El código parece incompleto - posible problema: falta llave de cierre '}}', 'end;' o delimitador ';'."

# Construir el parser
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
    error_sintactico = None # Reiniciar el error en cada análisis
    lexer.lineno = 1 # Reiniciar el contador de líneas del lexer
    parser.parse(texto, lexer=lexer)
    if error_sintactico:
        return error_sintactico
    return "Análisis sintáctico dice que tiene estructura correcta."