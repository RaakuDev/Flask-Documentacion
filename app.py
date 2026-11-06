
from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/hello")
def hello():
    """
    Endpoint para saludar al usuario.

    Parámetros:
        name (str): Nombre del usuario recibido por URL.

    Retorna:
        str: Mensaje de saludo.
    """
    name = request.args.get("name", "Usuario")
    return f"Hello, {escape(name)}!"


if __name__ == "__main__":
    app.run(debug=False)
