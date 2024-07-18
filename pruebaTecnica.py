from flask import Flask
from datetime import datetime

app = Flask(__name__)
print(app)

# Asocimos la URL '/' (la raíz del sitio web) con la función home.
@app.route('/')
def home():
    # Obtenemos la fecha y hora actuales, luego las formateamos como una cadena en el formato YYYY-MM-DD HH:MM:SS.
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    # return f """ ... """: Es una cadena de texto multilínea formateada (f-string), que permite incluir variables dentro de la cadena usando llaves {}.
    return f"""
    <html>
        <head>
            <title>Bienvenida</title>
        </head>
        <body>
            <h1>¡Bienvenido NEXOS!</h1>
            <p>La fecha y hora actuales son: {current_time}</p>
        </body>
    </html>
    """
# verifica si el archivo está siendo ejecutado directamente (no importado como un módulo). Si es así, el código dentro de este bloque se ejecuta.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
# app.run(): Inicia el servidor de desarrollo de Flask, que escucha peticiones HTTP.
# debug=True: Habilita el modo de depuración, que reinicia automáticamente el servidor cuando se detectan cambios en el código y proporciona un depurador interactivo en caso de errores.
