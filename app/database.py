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


def normalizar_correo(correo):
    """
    Normaliza correos para búsquedas consistentes.
    """
    return correo.strip().lower()


def separar_nombre_apellido(nombre_contacto):
    """
    Separa un nombre completo en nombres y apellidos.
    Si el usuario ingresa solo una palabra, se asigna apellido 'Sin apellido'.
    """
    partes = nombre_contacto.strip().split()

    if not partes:
        return "Cliente", "Sin apellido"

    if len(partes) == 1:
        return partes[0], "Sin apellido"

    nombres = partes[0]
    apellidos = " ".join(partes[1:])

    return nombres, apellidos


def generar_rut_temporal_cliente():
    """
    Genera un RUT temporal para usuarios creados desde el formulario del MVP.

    La tabla usuario exige RUT como dato obligatorio. Como el formulario de reserva
    no solicita RUT, se genera un valor temporal controlado para mantener la
    integridad de la base de datos en ambiente de pruebas.
    """
    connection = get_db_connection()

    row = connection.execute(
        """
        SELECT COALESCE(MAX(id_usuario), 0) + 1 AS siguiente_id
        FROM usuario;
        """
    ).fetchone()

    connection.close()

    siguiente_id = int(row["siguiente_id"])
    return f"9000{siguiente_id:04d}-{siguiente_id % 10}"


def obtener_id_rol_cliente(connection):
    """
    Obtiene el id_rol correspondiente a cliente.

    En los datos actuales del proyecto, los clientes usan id_rol = 1.
    Se intenta confirmar por nombre de rol si la tabla lo permite; si no,
    se usa 1 como valor por defecto controlado.
    """
    try:
        columnas_rol = connection.execute("PRAGMA table_info(rol);").fetchall()
        nombres_columnas = [columna["name"] for columna in columnas_rol]

        columna_nombre = None
        for candidata in ["nombre", "nombre_rol", "descripcion"]:
            if candidata in nombres_columnas:
                columna_nombre = candidata
                break

        if columna_nombre:
            row = connection.execute(
                f"""
                SELECT id_rol
                FROM rol
                WHERE LOWER(TRIM({columna_nombre})) LIKE '%cliente%'
                   OR LOWER(TRIM({columna_nombre})) LIKE '%turista%'
                LIMIT 1;
                """
            ).fetchone()

            if row:
                return row["id_rol"]

    except Exception:
        pass

    return 1


def buscar_usuario_por_correo(connection, correo_contacto):
    """
    Busca un usuario activo o existente por correo electrónico.
    """
    correo = normalizar_correo(correo_contacto)

    return connection.execute(
        """
        SELECT *
        FROM usuario
        WHERE LOWER(TRIM(correo)) = ?
        LIMIT 1;
        """,
        (correo,),
    ).fetchone()


def crear_usuario_cliente(connection, nombre_contacto, correo_contacto, telefono_contacto):
    """
    Crea un usuario con rol cliente usando los datos ingresados en el formulario.
    """
    nombres, apellidos = separar_nombre_apellido(nombre_contacto)
    correo = normalizar_correo(correo_contacto)
    rut_temporal = generar_rut_temporal_cliente()
    id_rol_cliente = obtener_id_rol_cliente(connection)

    cursor = connection.execute(
        """
        INSERT INTO usuario (
            id_rol,
            rut,
            nombres,
            apellidos,
            correo,
            contrasena,
            telefono,
            idioma,
            estado
        )
        VALUES (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            'ES',
            'Activo'
        );
        """,
        (
            id_rol_cliente,
            rut_temporal,
            nombres,
            apellidos,
            correo,
            "Cliente1234",
            telefono_contacto,
        ),
    )

    return cursor.lastrowid


def buscar_cliente_por_id_usuario(connection, id_usuario):
    """
    Busca un cliente asociado a un usuario.
    """
    return connection.execute(
        """
        SELECT *
        FROM cliente
        WHERE id_usuario = ?
        LIMIT 1;
        """,
        (id_usuario,),
    ).fetchone()


def crear_cliente_para_usuario(connection, id_usuario):
    """
    Crea un cliente asociado a un usuario existente.
    """
    cursor = connection.execute(
        """
        INSERT INTO cliente (
            id_usuario,
            fecha_registro,
            estado_cliente
        )
        VALUES (
            ?,
            DATE('now'),
            'Activo'
        );
        """,
        (id_usuario,),
    )

    return cursor.lastrowid


def buscar_o_crear_cliente(nombre_contacto, correo_contacto, telefono_contacto):
    """
    Busca o crea un cliente a partir de los datos ingresados en el formulario.

    Flujo:
    - Busca usuario por correo.
    - Si no existe, crea usuario con rol cliente.
    - Busca cliente asociado al usuario.
    - Si no existe cliente, crea registro en tabla cliente.
    - Retorna id_cliente para asociarlo a la reserva.
    """
    connection = get_db_connection()

    try:
        usuario = buscar_usuario_por_correo(connection, correo_contacto)

        if usuario:
            id_usuario = usuario["id_usuario"]
        else:
            id_usuario = crear_usuario_cliente(
                connection,
                nombre_contacto,
                correo_contacto,
                telefono_contacto,
            )

        cliente = buscar_cliente_por_id_usuario(connection, id_usuario)

        if cliente:
            id_cliente = cliente["id_cliente"]
        else:
            id_cliente = crear_cliente_para_usuario(connection, id_usuario)

        connection.commit()
        return id_cliente

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


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
    Registra una nueva reserva en la base de datos SQLite,
    asociándola al cliente recibido como parámetro.
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
    Obtiene una reserva registrada, junto con la habitación, tipo y cliente asociado.
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
            th.nombre AS tipo_habitacion,
            u.nombres AS nombres_cliente,
            u.apellidos AS apellidos_cliente,
            u.correo AS correo_cliente,
            u.telefono AS telefono_cliente
        FROM reserva r
        INNER JOIN habitacion h
            ON r.id_habitacion = h.id_habitacion
        INNER JOIN tipo_habitacion th
            ON h.id_tipo_habitacion = th.id_tipo_habitacion
        INNER JOIN cliente c
            ON r.id_cliente = c.id_cliente
        INNER JOIN usuario u
            ON c.id_usuario = u.id_usuario
        WHERE r.id_reserva = ?;
    """

    reserva = connection.execute(query, (id_reserva,)).fetchone()
    connection.close()

    return reserva


def listar_reservas_admin():
    """
    Lista las reservas registradas para la vista administrativa del release Semana 8.
    Se muestran datos principales de la reserva, habitación, tipo de habitación y cliente.
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
            th.nombre AS tipo_habitacion,
            u.nombres AS nombres_cliente,
            u.apellidos AS apellidos_cliente,
            u.correo AS correo_cliente,
            u.telefono AS telefono_cliente
        FROM reserva r
        INNER JOIN habitacion h
            ON r.id_habitacion = h.id_habitacion
        INNER JOIN tipo_habitacion th
            ON h.id_tipo_habitacion = th.id_tipo_habitacion
        INNER JOIN cliente c
            ON r.id_cliente = c.id_cliente
        INNER JOIN usuario u
            ON c.id_usuario = u.id_usuario
        ORDER BY
            r.id_reserva DESC;
    """

    reservas = connection.execute(query).fetchall()
    connection.close()

    return reservas


def obtener_resumen_reservas_admin():
    """
    Obtiene indicadores básicos para la vista administrativa.
    """
    connection = get_db_connection()

    query = """
        SELECT
            COUNT(*) AS total_reservas,
            SUM(CASE WHEN LOWER(TRIM(estado_reserva)) = 'confirmada' THEN 1 ELSE 0 END) AS confirmadas,
            SUM(CASE WHEN LOWER(TRIM(estado_reserva)) = 'pendiente' THEN 1 ELSE 0 END) AS pendientes,
            SUM(CASE WHEN LOWER(TRIM(estado_reserva)) = 'cancelada' THEN 1 ELSE 0 END) AS canceladas,
            COALESCE(SUM(total_reserva), 0) AS monto_total_reservas
        FROM reserva;
    """

    resumen = connection.execute(query).fetchone()
    connection.close()

    return resumen