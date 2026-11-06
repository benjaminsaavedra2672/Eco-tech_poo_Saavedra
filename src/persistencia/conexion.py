
"""Conexión configurable a SQLite o MariaDB/MySQL usando PyMySQL."""

import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _cargar_env():
    """Carga las variables del archivo .env."""
    env_path = ROOT / ".env"

    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()

            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)

                os.environ.setdefault(
                    key.strip(),
                    value.strip().strip('"').strip("'")
                )


_cargar_env()


def motor_actual():
    return os.getenv("DB_ENGINE", "sqlite").strip().lower()


# ==================================================
# ADAPTADOR DE CURSOR PARA PYMYSQL
# ==================================================

class CursorMySQL:
    """Adapta las consultas SQLite al formato de PyMySQL."""

    def __init__(self, cursor):
        self._cursor = cursor

    def execute(self, sql, parametros=()):
        sql = ConexionMySQL._sql(sql)
        self._cursor.execute(sql, parametros)
        return self

    def executemany(self, sql, parametros):
        sql = ConexionMySQL._sql(sql)
        self._cursor.executemany(sql, parametros)
        return self

    def __getattr__(self, nombre):
        return getattr(self._cursor, nombre)


# ==================================================
# CONEXION MYSQL / MARIADB
# ==================================================

class ConexionMySQL:
    """Adaptador de conexión compatible con los DAO existentes."""

    def __init__(self, conexion):
        self._conexion = conexion

    @staticmethod
    def _sql(sql):
        """Convierte los parámetros ? a %s."""
        return sql.replace("?", "%s")

    def execute(self, sql, parametros=()):
        cursor = self._conexion.cursor()
        cursor.execute(self._sql(sql), parametros)
        return cursor

    def cursor(self):
        return CursorMySQL(self._conexion.cursor())

    def executescript(self, script):
        """Ejecuta varias sentencias SQL."""

        cursor = self._conexion.cursor()

        try:
            for sentencia in script.split(";"):
                sentencia = sentencia.strip()

                if sentencia:
                    cursor.execute(sentencia)

        finally:
            cursor.close()

    def commit(self):
        self._conexion.commit()

    def rollback(self):
        self._conexion.rollback()

    def close(self):
        self._conexion.close()


# ==================================================
# ABRIR CONEXION
# ==================================================

def abrir_conexion():
    """Abre una conexión SQLite o MariaDB/MySQL."""

    motor = motor_actual()

    # ---------------- SQLITE ----------------

    if motor == "sqlite":

        db_name = os.getenv("DB_NAME", "ecotech.db")
        path = (ROOT / db_name).resolve()

        if ROOT.resolve() not in path.parents and path != ROOT.resolve():
            raise ValueError(
                "La ruta de la base de datos no es válida."
            )

        conn = sqlite3.connect(path, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")

        return conn

    # ------------- MARIADB / MYSQL -------------

    if motor in ("mysql", "mariadb"):

        try:
            import pymysql
            import pymysql.cursors

        except ImportError as exc:
            raise RuntimeError(
                "Falta PyMySQL. Instálalo con: "
                "py -m pip install PyMySQL"
            ) from exc

        # Comprobar variables necesarias.

        requeridas = ("DB_HOST", "DB_NAME", "DB_USER")

        faltantes = [
            nombre
            for nombre in requeridas
            if not os.getenv(nombre, "").strip()
        ]

        if os.getenv("DB_PASSWORD") is None:
            faltantes.append("DB_PASSWORD")

        if faltantes:
            raise ValueError(
                "Faltan variables en .env: "
                + ", ".join(faltantes)
            )

        try:

            conexion = pymysql.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=int(os.getenv("DB_PORT", "3306")),
                database=os.getenv("DB_NAME", "ecotech"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", ""),
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=10,
                autocommit=False
            )

            return ConexionMySQL(conexion)

        except pymysql.MySQLError as exc:

            raise RuntimeError(
                "No se pudo conectar a MariaDB/MySQL. "
                "Comprueba que WampServer esté iniciado, "
                "que el puerto sea correcto, que la base de datos "
                "exista y que el usuario y la contraseña sean válidos. "
                f"Detalle: {exc}"
            ) from exc

    raise ValueError(
        "DB_ENGINE debe ser 'sqlite', 'mysql' o 'mariadb'."
    )