import sqlite3
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