from flask import Flask, render_template, request
import re

app = Flask(__name__)

palabras_reservadas = ['for', 'while', 'if']
tokens_lista = []
# Nuevas listas para almacenar por separado
palabras_reservadas_encontradas = []
identificadores_encontrados = []
parentesis_encontrados = []
simbolos_encontrados = []
estadisticas = {}

@app.route('/')
def index():
    return render_template("index.html", tokens=tokens_lista,
                           palabras_reservadas_lista=palabras_reservadas_encontradas,
                           identificadores_lista=identificadores_encontrados,
                           parentesis_lista=parentesis_encontrados,
                           simbolos_lista=simbolos_encontrados,
                           estadisticas=estadisticas)

@app.route('/analizar', methods=['POST'])
def analizar():
    global tokens_lista, palabras_reservadas_encontradas, identificadores_encontrados, parentesis_encontrados, simbolos_encontrados, estadisticas
    texto = request.form['texto']
    tokens_lista = []
    palabras_reservadas_encontradas = []
    identificadores_encontrados = []
    parentesis_encontrados = []
    simbolos_encontrados = []
    patrones = [
        (r'<=', 'OPERADOR'),
        (r'>=', 'OPERADOR'), 
        (r'\+\+', 'OPERADOR'),
        (r'\(', 'P.I'), 
        (r'\)', 'P.D'), 
        (r'\{', 'LLAVE_I'),
        (r'\}', 'LLAVE_D'),
        (r'<', 'OPERADOR'),
        (r'>', 'OPERADOR'),
        (r'\+', 'OPERADOR'),
        (r'/', 'OPERADOR'),
        (r';', 'DELIMITADOR'),
        (r',', 'DELIMITADOR'),
        (r'\d+', 'NUMERO'),
        (r'[a-zA-Z_][a-zA-Z0-9_]*', 'PALABRA') 
    ]

    
    posicion = 0
    while posicion < len(texto):
        if texto[posicion].isspace():
            posicion += 1
            continue
        token_encontrado = False
        for patron, tipo in patrones:
            regex = re.compile(patron)
            match = regex.match(texto, posicion)
            if match:
                lexema = match.group(0)
                if tipo == 'PALABRA':
                    if lexema.lower() in palabras_reservadas:
                        tokens_lista.append([lexema, 'PALABRA RESERVADA'])
                        palabras_reservadas_encontradas.append(lexema)
                    else:
                        tokens_lista.append([lexema, 'IDENTIFICADOR'])
                        identificadores_encontrados.append(lexema)
                else:
                    tokens_lista.append([lexema, tipo])
                    if tipo in ['P.I', 'P.D']:
                        parentesis_encontrados.append(lexema)
                    elif tipo in ['OPERADOR', 'DELIMITADOR', 'LLAVE_I', 'LLAVE_D', 'NUMERO']:
                        simbolos_encontrados.append(lexema)
                posicion = match.end()
                token_encontrado = True
                break
        if not token_encontrado:
            tokens_lista.append([texto[posicion], 'DESCONOCIDO'])
            posicion += 1
    
    estadisticas = {
        'total_palabras_reservadas': len(palabras_reservadas_encontradas),
        'total_identificadores': len(identificadores_encontrados),
        'total_parentesis': len(parentesis_encontrados),
        'total_simbolos': len(simbolos_encontrados),
        'total_tokens': len(tokens_lista)
    }

    return render_template("index.html", 
                         tokens=tokens_lista, 
                         texto=texto,
                         palabras_reservadas_lista=palabras_reservadas_encontradas,
                         identificadores_lista=identificadores_encontrados,
                         parentesis_lista=parentesis_encontrados,
                         simbolos_lista=simbolos_encontrados,
                         estadisticas=estadisticas)

if __name__ == "__main__":
    app.run(debug=True)