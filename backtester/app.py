from flask import Flask

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Ruta de ejemplo
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Punto de entrada para la aplicación WSGI
if __name__ == '__main__':
    app.run()
