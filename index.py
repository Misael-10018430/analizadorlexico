from flask import Flask, render_template, request
from analizador import analizar_lexico, analizar_sintactico # Importamos las funciones
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/analizar_lexico', methods=['POST'])
def ejecutar_analisis_lexico():
    texto = request.form['texto'] #obtiene el codigo fuente enviado desde el formulario web
    tokens_lista = analizar_lexico(texto)#llama a la funcion del analizador lexico, obtiene la lista de tokens encontrados
    #Procesar para estadísticas
    #clasifica tokens por categoria para conteo
    palabras_reservadas_encontradas = [t.value for t in tokens_lista if t.type in ['IF', 'FOR', 'WHILE']]
    identificadores_encontrados = [t.value for t in tokens_lista if t.type == 'ID']
    simbolos_encontrados = [t.value for t in tokens_lista if t.type in ['OPERADOR', 'PI', 'PD', 'LLAVEI', 'LLAVED', 'DELIMITADOR', 'NUMERO']]
    estadisticas = {
    #genera estadisticas, cuenta cuantos tokens de cada tipo se encontraron, proporciona metrica del codigo analizado
        'total_palabras_reservadas': len(palabras_reservadas_encontradas),
        'total_identificadores': len(identificadores_encontrados),
        'total_simbolos': len(simbolos_encontrados),
        'total_tokens': len(tokens_lista)
    }
   #Convertir tokens para la tabla con información de línea
   #prepara los datos para visualizacion, convierte tokens en formato tabla para mostrar en HTML
    tokens_tabla = [[t.value, t.type, getattr(t, 'lineno', 'N/A')] for t in tokens_lista]
    return render_template("index.html",
                           texto=texto,
                           tokens=tokens_tabla,
                           estadisticas=estadisticas)
@app.route('/analizar_sintactico', methods=['POST'])
#Obtiene el texto, del formulario web, ejecuta ambos analisis (lexico y sintactico), procesa resultados: igual que el analisis lexico + reusltado sintactico, retonro todo: tokens, estadisiticas y resultado del analisis sintactico
def ejecutar_analisis_sintactico():
    texto = request.form['texto']
    tokens_lista_obj = analizar_lexico(texto)
    resultado_sintactico = analizar_sintactico(texto)
    #incluye el resultado del analisis sintactico en la respuesta
    #puede ser: analisis exitoso o mensaje de error detallado
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


#analizador lexico: usuario escribe codigo->flask recibe->analizadr lexico procesa->claisifica tokens->genera estadisticas->muestra resultados en web
#analizador sintactico: usuario escribe codigo-> flask recibe->analizador lexico->sintactico procesan->clasifica tokens + verifica gramatica->genera estadisticas + resultado sintactico->muestra eresultados completos en la web