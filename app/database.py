import sqlite3
from datetime import date
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "bd" / "hotel_pacific_reef.db"


def get_db_connection():
    """
    Crea una conexión a la base de datos SQLite del proyecto Hotel Pacific Reef.
    La conexión devuelve filas como diccionarios para facilitar el uso en las vistas.
    """
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró la base de datos en la ruta esperada: {DB_PATH}"
        )

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def test_db_connection():
    """
    Verifica que la base de datos exista y que se pueda consultar correctamente.
    Retorna un diccionario simple con el estado de la conexión.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row["name"] for row in cursor.fetchall()]

        connection.close()

        return {
            "ok": True,
            "database": str(DB_PATH),
            "tables": tables,
            "message": "Conexión correcta a la base de datos.",
        }

    except Exception as error:
        return {
            "ok": False,
            "database": str(DB_PATH),
            "tables": [],
            "message": f"Error de conexión: {error}",
        }


def buscar_habitaciones_disponibles(
    fecha_check_in,
    fecha_check_out,
    cantidad_huespedes,
):
    """
    Busca habitaciones disponibles para un rango de fechas y cantidad de huéspedes.

    Criterio de disponibilidad:
    - La habitación debe estar en estado Disponible.
    - La capacidad debe ser mayor o igual a la cantidad de huéspedes.
    - No debe existir una reserva Confirmada o Pendiente que se cruce con el rango consultado.
    - Las reservas Canceladas no bloquean disponibilidad.
    """
    connection = get_db_connection()

    query = """
        SELECT
            h.id_habitacion,
            h.numero,
            h.piso,
            h.capacidad,
            h.descripcion AS descripcion_habitacion,
            h.estado AS estado_habitacion,
            th.nombre AS tipo_habitacion,
            th.descripcion AS descripcion_tipo,
            th.cantidad_camas,
            COALESCE(t.precio_noche, th.precio_base) AS precio_noche
        FROM habitacion h
        INNER JOIN tipo_habitacion th
            ON h.id_tipo_habitacion = th.id_tipo_habitacion
        LEFT JOIN tarifa t
            ON t.id_tipo_habitacion = th.id_tipo_habitacion
            AND LOWER(TRIM(t.estado)) = 'activa'
            AND DATE(?) >= DATE(t.fecha_inicio)
            AND (
                t.fecha_termino IS NULL
                OR DATE(?) <= DATE(t.fecha_termino)
            )
        WHERE
            LOWER(TRIM(h.estado)) = 'disponible'
            AND h.capacidad >= ?
            AND NOT EXISTS (
                SELECT 1
                FROM reserva r
                WHERE
                    r.id_habitacion = h.id_habitacion
                    AND LOWER(TRIM(r.estado_reserva)) IN ('confirmada', 'pendiente')
                    AND DATE(r.fecha_check_in) < DATE(?)
                    AND DATE(r.fecha_check_out) > DATE(?)
            )
        ORDER BY
            precio_noche ASC,
            h.numero ASC;
    """

    rows = connection.execute(
        query,
        (
            fecha_check_in,
            fecha_check_in,
            cantidad_huespedes,
            fecha_check_out,
            fecha_check_in,
        ),
    ).fetchall()

    connection.close()
    return rows


def obtener_habitacion_por_id(id_habitacion, fecha_referencia=None):
    """
    Obtiene los datos de una habitación específica, incluyendo su tipo y precio.
    """
    fecha_referencia = fecha_referencia or date.today().isoformat()

    connection = get_db_connection()

    query = """
        SELECT
            h.id_habitacion,
            h.numero,
            h.piso,
            h.capacidad,
            h.descripcion AS descripcion_habitacion,
            h.estado AS estado_habitacion,
            th.nombre AS tipo_habitacion,
            th.descripcion AS descripcion_tipo,
            th.cantidad_camas,
            COALESCE(t.precio_noche, th.precio_base) AS precio_noche
        FROM habitacion h
        INNER JOIN tipo_habitacion th
            ON h.id_tipo_habitacion = th.id_tipo_habitacion
        LEFT JOIN tarifa t
            ON t.id_tipo_habitacion = th.id_tipo_habitacion
            AND LOWER(TRIM(t.estado)) = 'activa'
            AND DATE(?) >= DATE(t.fecha_inicio)
            AND (
                t.fecha_termino IS NULL
                OR DATE(?) <= DATE(t.fecha_termino)
            )
        WHERE h.id_habitacion = ?;
    """

    habitacion = connection.execute(
        query,
        (
            fecha_referencia,
            fecha_referencia,
            id_habitacion,
        ),
    ).fetchone()

    connection.close()
    return habitacion


def crear_reserva(
    id_cliente,
    id_habitacion,
    fecha_check_in,
    fecha_check_out,
    cantidad_huespedes,
    total_reserva,
    abono_requerido,
    saldo_pendiente,
    codigo_reserva,
):
    """
    Registra una nueva reserva en la base de datos SQLite.
    Para el MVP se utiliza un cliente de prueba previamente existente.
    """
    connection = get_db_connection()

    query = """
        INSERT INTO reserva (
            id_cliente,
            id_habitacion,
            fecha_reserva,
            fecha_check_in,
            fecha_check_out,
            cantidad_huespedes,
            estado_reserva,
            total_reserva,
            abono_requerido,
            saldo_pendiente,
            codigo_reserva
        )
        VALUES (
            ?,
            ?,
            DATE('now'),
            ?,
            ?,
            ?,
            'Pendiente',
            ?,
            ?,
            ?,
            ?
        );
    """

    cursor = connection.execute(
        query,
        (
            id_cliente,
            id_habitacion,
            fecha_check_in,
            fecha_check_out,
            cantidad_huespedes,
            total_reserva,
            abono_requerido,
            saldo_pendiente,
            codigo_reserva,
        ),
    )

    connection.commit()
    id_reserva = cursor.lastrowid
    connection.close()

    return id_reserva


def obtener_reserva_por_id(id_reserva):
    """
    Obtiene una reserva registrada, junto con la habitación y tipo asociado.
    """
    connection = get_db_connection()

    query = """
        SELECT
            r.id_reserva,
            r.id_cliente,
            r.id_habitacion,
            r.fecha_reserva,
            r.fecha_check_in,
            r.fecha_check_out,
            r.cantidad_huespedes,
            r.estado_reserva,
            r.total_reserva,
            r.abono_requerido,
            r.saldo_pendiente,
            r.codigo_reserva,
            h.numero AS numero_habitacion,
            h.piso,
            th.nombre AS tipo_habitacion
        FROM reserva r
        INNER JOIN habitacion h
            ON r.id_habitacion = h.id_habitacion
        INNER JOIN tipo_habitacion th
            ON h.id_tipo_habitacion = th.id_tipo_habitacion
        WHERE r.id_reserva = ?;
    """

    reserva = connection.execute(query, (id_reserva,)).fetchone()
    connection.close()

    return reserva