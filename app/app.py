from flask import Flask, render_template
from database import test_db_connection


app = Flask(__name__)
app.secret_key = "hotel-pacific-reef-dev"


@app.route("/")
def index():
    """
    Página principal del MVP funcional.
    """
    return render_template("index.html")


@app.route("/disponibilidad", methods=["GET"])
def disponibilidad():
    """
    Vista inicial del formulario de consulta de disponibilidad.
    En el siguiente hito se agregará el procesamiento POST.
    """
    return render_template("disponibilidad.html")


@app.route("/health-db")
def health_db():
    """
    Ruta técnica para verificar que Flask se conecta correctamente a SQLite.
    Esta ruta sirve como evidencia inicial de integración back-end/base de datos.
    """
    status = test_db_connection()
    return render_template("index.html", db_status=status)


if __name__ == "__main__":
    app.run(debug=True)