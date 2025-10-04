from flask import Flask, render_template, request
from analizador import analizar_lexico, analizar_sintactico
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/analizar_lexico', methods=['POST'])
def ejecutar_analisis_lexico():
    texto = request.form['texto']
    tokens_lista = analizar_lexico(texto)
    palabras_reservadas_encontradas = [t.value for t in tokens_lista if t.type in ['IF', 'FOR', 'WHILE', 'PROGRAMA', 'INT', 'READ', 'PRINT', 'PRINTF', 'END']]
    identificadores_encontrados = [t.value for t in tokens_lista if t.type == 'ID']
    simbolos_encontrados = [t.value for t in tokens_lista if t.type in ['OPERADOR', 'PI', 'PD', 'LLAVEI', 'LLAVED', 'DELIMITADOR', 'NUMERO']]
    estadisticas = {
        'total_palabras_reservadas': len(palabras_reservadas_encontradas),
        'total_identificadores': len(identificadores_encontrados),
        'total_simbolos': len(simbolos_encontrados),
        'total_tokens': len(tokens_lista)
    }
    tokens_tabla = [[t.value, t.type, getattr(t, 'lineno', 'N/A')] for t in tokens_lista]
    return render_template("index.html",
                           texto=texto,
                           tokens=tokens_tabla,
                           estadisticas=estadisticas)
@app.route('/analizar_sintactico', methods=['POST'])
def ejecutar_analisis_sintactico():
    texto = request.form['texto']
    tokens_lista_obj = analizar_lexico(texto)
    resultado_sintactico = analizar_sintactico(texto)
    tokens_tabla = [[t.value, t.type, getattr(t, 'lineno', 'N/A')] for t in tokens_lista_obj]
    palabras_reservadas_encontradas = [t.value for t in tokens_lista_obj if t.type in ['IF', 'FOR', 'WHILE', 'PROGRAMA', 'INT', 'READ', 'PRINT', 'PRINTF', 'END']]
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


#analizador lexico: usuario escribe codigo->flask recibe->analizadr lexico procesa->claisifica tokens->genera estadisticas->muestra resultados en web
#analizador sintactico: usuario escribe codigo-> flask recibe->analizador lexico->sintactico procesan->clasifica tokens + verifica gramatica->genera estadisticas + resultado sintactico->muestra eresultados completos en la web