from datetime import datetime
from uuid import uuid4

from flask import Flask, redirect, render_template, request, url_for

from database import (
    buscar_habitaciones_disponibles,
    crear_reserva,
    listar_reservas_admin,
    obtener_habitacion_por_id,
    obtener_reserva_por_id,
    obtener_resumen_reservas_admin,
    test_db_connection,
)


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


def calcular_montos(precio_noche, cantidad_noches):
    """
    Calcula total de reserva, abono requerido del 30% y saldo pendiente.
    """
    total_reserva = int(round(float(precio_noche) * cantidad_noches))
    abono_requerido = int(round(total_reserva * 0.30))
    saldo_pendiente = total_reserva - abono_requerido

    return total_reserva, abono_requerido, saldo_pendiente


def generar_codigo_reserva():
    """
    Genera un código simple para identificar la reserva en el MVP.
    """
    fecha = datetime.now().strftime("%Y%m%d")
    sufijo = uuid4().hex[:6].upper()
    return f"HPR-{fecha}-{sufijo}"


def habitacion_sigue_disponible(
    id_habitacion,
    fecha_check_in,
    fecha_check_out,
    cantidad_huespedes,
):
    """
    Verifica nuevamente la disponibilidad antes de registrar la reserva.
    Evita registrar una habitación que ya no esté disponible.
    """
    disponibles = buscar_habitaciones_disponibles(
        fecha_check_in,
        fecha_check_out,
        cantidad_huespedes,
    )

    return any(
        int(habitacion["id_habitacion"]) == int(id_habitacion)
        for habitacion in disponibles
    )


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


@app.route("/reservar/<int:id_habitacion>", methods=["GET", "POST"])
def reservar(id_habitacion):
    """
    Muestra y procesa el formulario de reserva para una habitación disponible.
    """
    if request.method == "GET":
        fecha_check_in_raw = request.args.get("fecha_check_in", "").strip()
        fecha_check_out_raw = request.args.get("fecha_check_out", "").strip()
        cantidad_raw = request.args.get("cantidad_huespedes", "").strip()

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
                "reserva.html",
                error="Debe realizar una búsqueda válida antes de reservar.",
                habitacion=None,
            )

        habitacion = obtener_habitacion_por_id(
            id_habitacion,
            fecha_check_in.isoformat(),
        )

        if not habitacion:
            return render_template(
                "reserva.html",
                error="No se encontró la habitación seleccionada.",
                habitacion=None,
            )

        if not habitacion_sigue_disponible(
            id_habitacion,
            fecha_check_in.isoformat(),
            fecha_check_out.isoformat(),
            cantidad_huespedes,
        ):
            return render_template(
                "reserva.html",
                error="La habitación seleccionada ya no está disponible para ese rango.",
                habitacion=None,
            )

        cantidad_noches = (fecha_check_out - fecha_check_in).days
        total_reserva, abono_requerido, saldo_pendiente = calcular_montos(
            habitacion["precio_noche"],
            cantidad_noches,
        )

        return render_template(
            "reserva.html",
            habitacion=habitacion,
            fecha_check_in=fecha_check_in.isoformat(),
            fecha_check_out=fecha_check_out.isoformat(),
            cantidad_huespedes=cantidad_huespedes,
            cantidad_noches=cantidad_noches,
            total_reserva=total_reserva,
            abono_requerido=abono_requerido,
            saldo_pendiente=saldo_pendiente,
        )

    fecha_check_in_raw = request.form.get("fecha_check_in", "").strip()
    fecha_check_out_raw = request.form.get("fecha_check_out", "").strip()
    cantidad_raw = request.form.get("cantidad_huespedes", "").strip()

    nombre_contacto = request.form.get("nombre_contacto", "").strip()
    correo_contacto = request.form.get("correo_contacto", "").strip()
    telefono_contacto = request.form.get("telefono_contacto", "").strip()

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

    habitacion = obtener_habitacion_por_id(
        id_habitacion,
        fecha_check_in_raw,
    )

    if error or not habitacion:
        return render_template(
            "reserva.html",
            error="No fue posible procesar la reserva. Verifique los datos ingresados.",
            habitacion=None,
        )

    if not nombre_contacto or not correo_contacto or not telefono_contacto:
        cantidad_noches = (fecha_check_out - fecha_check_in).days
        total_reserva, abono_requerido, saldo_pendiente = calcular_montos(
            habitacion["precio_noche"],
            cantidad_noches,
        )

        return render_template(
            "reserva.html",
            error="Debe completar los datos de contacto para registrar la reserva.",
            habitacion=habitacion,
            fecha_check_in=fecha_check_in.isoformat(),
            fecha_check_out=fecha_check_out.isoformat(),
            cantidad_huespedes=cantidad_huespedes,
            cantidad_noches=cantidad_noches,
            total_reserva=total_reserva,
            abono_requerido=abono_requerido,
            saldo_pendiente=saldo_pendiente,
        )

    if not habitacion_sigue_disponible(
        id_habitacion,
        fecha_check_in.isoformat(),
        fecha_check_out.isoformat(),
        cantidad_huespedes,
    ):
        return render_template(
            "reserva.html",
            error="La habitación seleccionada ya no está disponible para ese rango.",
            habitacion=None,
        )

    cantidad_noches = (fecha_check_out - fecha_check_in).days
    total_reserva, abono_requerido, saldo_pendiente = calcular_montos(
        habitacion["precio_noche"],
        cantidad_noches,
    )

    codigo_reserva = generar_codigo_reserva()

    # Release Semana 8:
    # En esta versión se mantiene temporalmente un cliente de prueba para asociar la reserva.
    # Esta lógica será mejorada en el siguiente hito para registrar o reutilizar clientes reales.
    id_cliente_demo = 1

    id_reserva = crear_reserva(
        id_cliente=id_cliente_demo,
        id_habitacion=id_habitacion,
        fecha_check_in=fecha_check_in.isoformat(),
        fecha_check_out=fecha_check_out.isoformat(),
        cantidad_huespedes=cantidad_huespedes,
        total_reserva=total_reserva,
        abono_requerido=abono_requerido,
        saldo_pendiente=saldo_pendiente,
        codigo_reserva=codigo_reserva,
    )

    return redirect(url_for("confirmacion", id_reserva=id_reserva))


@app.route("/confirmacion/<int:id_reserva>")
def confirmacion(id_reserva):
    """
    Muestra la confirmación de una reserva registrada.
    """
    reserva = obtener_reserva_por_id(id_reserva)

    if not reserva:
        return render_template(
            "confirmacion.html",
            error="No se encontró la reserva solicitada.",
            reserva=None,
        )

    return render_template("confirmacion.html", reserva=reserva)

@app.route("/admin/reservas")
def admin_reservas():
    """
    Vista administrativa simple para consultar reservas registradas.
    Esta vista permite validar que las reservas creadas desde el flujo cliente
    quedan disponibles para revisión administrativa.
    """
    reservas = listar_reservas_admin()
    resumen = obtener_resumen_reservas_admin()

    return render_template(
        "admin_reservas.html",
        reservas=reservas,
        resumen=resumen,
    )

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