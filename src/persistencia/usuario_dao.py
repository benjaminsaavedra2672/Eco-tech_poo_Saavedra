from .conexion import abrir_conexion


class UsuarioDAO:

    @staticmethod
    def insertar(usuario):
        conn = abrir_conexion()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO usuario(username, password_hash)
                VALUES (?, ?)
            """, (
                usuario.username,
                usuario._hash_para_persistencia()
            ))

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
        from dominio.usuario import Usuario

        obj = Usuario.__new__(Usuario)
        obj.id = row["id"]
        obj.username = row["username"]
        obj.empleado_id = row["empleado_id"] if "empleado_id" in row.keys() else None
        obj.nombre_empleado = row["nombre_empleado"] if "nombre_empleado" in row.keys() else None
        obj.rol = row["rol"] if "rol" in row.keys() else None
        obj._password_hash = row["password_hash"]
        return obj

    @staticmethod
    def buscar_por_id(id_usuario):
        conn = abrir_conexion()
        try:
            row = conn.execute("""
                SELECT u.id, u.username, u.password_hash, e.id_empleado AS empleado_id, e.nombre AS nombre_empleado, e.rol
                FROM usuario u LEFT JOIN empleado e ON e.usuario_id = u.id
                WHERE u.id = ?
            """, (id_usuario,)).fetchone()

            return UsuarioDAO._desde_fila(row) if row else None

        finally:
            conn.close()

    @staticmethod
    def buscar_por_username(username):
        conn = abrir_conexion()
        try:
            row = conn.execute("""
                SELECT u.id, u.username, u.password_hash, e.id_empleado AS empleado_id, e.nombre AS nombre_empleado, e.rol
                FROM usuario u LEFT JOIN empleado e ON e.usuario_id = u.id
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
                SELECT u.id, u.username, u.password_hash, e.id_empleado AS empleado_id, e.nombre AS nombre_empleado, e.rol
                FROM usuario u LEFT JOIN empleado e ON e.usuario_id = u.id
                ORDER BY u.id
            """).fetchall()

            return [
                UsuarioDAO._desde_fila(row)
                for row in rows
            ]

        finally:
            conn.close()

    @staticmethod
    def actualizar(usuario):
        conn = abrir_conexion()
        try:
            cur = conn.execute("""
                UPDATE usuario
                SET username = ?, password_hash = ?
                WHERE id = ?
            """, (
                usuario.username,
                usuario._hash_para_persistencia(),
                usuario.id
            ))

            conn.commit()
            return cur.rowcount > 0

        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_usuario):
        conn = abrir_conexion()
        try:
            cur = conn.execute("""
                DELETE FROM usuario
                WHERE id = ?
            """, (id_usuario,))

            conn.commit()
            return cur.rowcount > 0

        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()