# ARCHIVO: app.py - MEJORAS MÍNIMAS SIN CAMBIAR ESTRUCTURA

from flask import Flask, render_template, request
from analizador import analizar_lexico, analizar_sintactico # Importamos las funciones
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analizar_lexico', methods=['POST'])
def ejecutar_analisis_lexico():
    texto = request.form['texto']
    tokens_lista = analizar_lexico(texto)

    # Procesar para estadísticas
    palabras_reservadas_encontradas = [t.value for t in tokens_lista if t.type in ['IF', 'FOR', 'WHILE']]
    identificadores_encontrados = [t.value for t in tokens_lista if t.type == 'ID']
    simbolos_encontrados = [t.value for t in tokens_lista if t.type in ['OPERADOR', 'PI', 'PD', 'LLAVEI', 'LLAVED', 'DELIMITADOR', 'NUMERO']]
    estadisticas = {
        'total_palabras_reservadas': len(palabras_reservadas_encontradas),
        'total_identificadores': len(identificadores_encontrados),
        'total_simbolos': len(simbolos_encontrados),
        'total_tokens': len(tokens_lista)
    }

    # ÚNICA MEJORA: Convertir tokens para la tabla con información de línea
    tokens_tabla = [[t.value, t.type, getattr(t, 'lineno', 'N/A')] for t in tokens_lista]
    return render_template("index.html",
                           texto=texto,
                           tokens=tokens_tabla,
                           estadisticas=estadisticas)


@app.route('/analizar_sintactico', methods=['POST'])
def ejecutar_analisis_sintactico():
    texto = request.form['texto']
    
    # Ejecutamos ambos análisis para mostrar toda la información
    tokens_lista_obj = analizar_lexico(texto)
    resultado_sintactico = analizar_sintactico(texto)

    # ÚNICA MEJORA: Tokens con información de línea
    tokens_tabla = [[t.value, t.type, getattr(t, 'lineno', 'N/A')] for t in tokens_lista_obj]

    palabras_reservadas_encontradas = [t.value for t in tokens_lista_obj if t.type in ['IF', 'FOR', 'WHILE']]
    identificadores_encontrados = [t.value for t in tokens_lista_obj if t.type == 'ID']
    simbolos_encontrados = [t.value for t in tokens_lista_obj if t.type in ['OPERADOR', 'PI', 'PD', 'LLAVEI', 'LLAVED', 'DELIMITADOR', 'NUMERO']]

    estadisticas = {
        'total_palabras_reservadas': len(palabras_reservadas_encontradas),
        'total_identificadores': len(identificadores_encontrados),
        'total_simbolos': len(simbolos_encontrados),
        'total_tokens': len(tokens_tabla)
    }

    return render_template("index.html",
                           texto=texto,
                           tokens=tokens_tabla,
                           estadisticas=estadisticas,
                           resultado_sintactico=resultado_sintactico)


if __name__ == "__main__":
    app.run(debug=True)