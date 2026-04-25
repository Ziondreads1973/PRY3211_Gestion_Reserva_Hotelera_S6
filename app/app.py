from datetime import datetime

from flask import Flask, render_template, request

from database import buscar_habitaciones_disponibles, test_db_connection


app = Flask(__name__)
app.secret_key = "hotel-pacific-reef-dev"


@app.template_filter("clp")
def clp(value):
    """
    Formatea valores numéricos como moneda chilena.
    Ejemplo: 120000 -> $120.000
    """
    try:
        number = int(round(float(value)))
        return f"${number:,}".replace(",", ".")
    except (TypeError, ValueError):
        return "$0"


def parse_date(value):
    """
    Convierte una fecha HTML yyyy-mm-dd a objeto date.
    """
    return datetime.strptime(value, "%Y-%m-%d").date()


def validar_datos_busqueda(fecha_check_in_raw, fecha_check_out_raw, cantidad_raw):
    """
    Valida los datos ingresados en el formulario de disponibilidad.
    """
    if not fecha_check_in_raw or not fecha_check_out_raw or not cantidad_raw:
        return None, None, None, "Debe completar todos los campos de búsqueda."

    try:
        fecha_check_in = parse_date(fecha_check_in_raw)
        fecha_check_out = parse_date(fecha_check_out_raw)
    except ValueError:
        return None, None, None, "Las fechas ingresadas no tienen un formato válido."

    try:
        cantidad_huespedes = int(cantidad_raw)
    except ValueError:
        return None, None, None, "La cantidad de huéspedes debe ser un número entero."

    if fecha_check_out <= fecha_check_in:
        return (
            None,
            None,
            None,
            "La fecha de salida debe ser posterior a la fecha de entrada.",
        )

    if cantidad_huespedes <= 0:
        return None, None, None, "La cantidad de huéspedes debe ser mayor que cero."

    return fecha_check_in, fecha_check_out, cantidad_huespedes, None


@app.route("/")
def index():
    """
    Página principal del MVP funcional.
    """
    return render_template("index.html")


@app.route("/disponibilidad", methods=["GET", "POST"])
def disponibilidad():
    """
    Vista y procesamiento de la consulta de disponibilidad.
    """
    if request.method == "POST":
        fecha_check_in_raw = request.form.get("fecha_check_in", "").strip()
        fecha_check_out_raw = request.form.get("fecha_check_out", "").strip()
        cantidad_raw = request.form.get("cantidad_huespedes", "").strip()

        values = {
            "fecha_check_in": fecha_check_in_raw,
            "fecha_check_out": fecha_check_out_raw,
            "cantidad_huespedes": cantidad_raw,
        }

        (
            fecha_check_in,
            fecha_check_out,
            cantidad_huespedes,
            error,
        ) = validar_datos_busqueda(
            fecha_check_in_raw,
            fecha_check_out_raw,
            cantidad_raw,
        )

        if error:
            return render_template(
                "disponibilidad.html",
                error=error,
                values=values,
            )

        habitaciones = buscar_habitaciones_disponibles(
            fecha_check_in.isoformat(),
            fecha_check_out.isoformat(),
            cantidad_huespedes,
        )

        cantidad_noches = (fecha_check_out - fecha_check_in).days

        return render_template(
            "resultados.html",
            habitaciones=habitaciones,
            fecha_check_in=fecha_check_in.isoformat(),
            fecha_check_out=fecha_check_out.isoformat(),
            cantidad_huespedes=cantidad_huespedes,
            cantidad_noches=cantidad_noches,
        )

    return render_template("disponibilidad.html", values={})


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