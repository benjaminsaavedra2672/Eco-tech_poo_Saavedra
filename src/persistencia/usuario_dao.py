from .conexion import abrir_conexion
from dominio.usuario import Usuario


class UsuarioDAO:
    @staticmethod
    def insertar(usuario):
        conn = abrir_conexion()
        try:
            cur = conn.execute(
                "INSERT INTO usuario(username, password_hash, rol, empleado_id) VALUES (?, ?, ?, ?)",
                (usuario.username, usuario._hash_para_persistencia(), usuario.rol, usuario.empleado_id)
            )
            usuario.id = cur.lastrowid
            conn.commit()
            return usuario
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def _desde_fila(row):
        obj = Usuario.__new__(Usuario)
        obj.id = row["id"]
        obj.username = row["username"]
        obj.empleado_id = row["empleado_id"]
        obj.nombre_empleado = row["nombre_empleado"]
        obj.rol = row["rol"]
        obj._password_hash = row["password_hash"]
        return obj

    @staticmethod
    def buscar_por_username(username):
        username = Usuario.normalizar_usuario(username)
        conn = abrir_conexion()
        try:
            row = conn.execute("""
                SELECT u.id, u.username, u.password_hash, u.rol,
                       COALESCE(u.empleado_id, e.id_empleado) AS empleado_id, e.nombre AS nombre_empleado
                FROM usuario u LEFT JOIN empleado e ON e.id_empleado = COALESCE(u.empleado_id, (SELECT id_empleado FROM empleado WHERE usuario_id=u.id LIMIT 1))
                WHERE u.username = ?
            """, (username,)).fetchone()
            return UsuarioDAO._desde_fila(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def listar():
        conn = abrir_conexion()
        try:
            rows = conn.execute("""
                SELECT u.id, u.username, u.password_hash, u.rol,
                       COALESCE(u.empleado_id, e.id_empleado) AS empleado_id, e.nombre AS nombre_empleado
                FROM usuario u LEFT JOIN empleado e ON e.id_empleado = COALESCE(u.empleado_id, (SELECT id_empleado FROM empleado WHERE usuario_id=u.id LIMIT 1))
                ORDER BY u.id
            """).fetchall()
            return [UsuarioDAO._desde_fila(row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def cambiar_rol(id_usuario, rol):
        rol = Usuario.validar_rol(rol)
        conn = abrir_conexion()
        try:
            cur = conn.execute("UPDATE usuario SET rol=? WHERE id=?", (rol, id_usuario))
            conn.commit()
            return cur.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def actualizar_password(id_usuario, password_hash):
        conn = abrir_conexion()
        try:
            cur = conn.execute(
                "UPDATE usuario SET password_hash=? WHERE id=?",
                (password_hash, id_usuario)
            )
            conn.commit()
            return cur.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
