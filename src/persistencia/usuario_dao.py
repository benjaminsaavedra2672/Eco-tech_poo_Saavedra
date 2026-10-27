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
        obj._password_hash = row["password_hash"]
        return obj

    @staticmethod
    def buscar_por_id(id_usuario):
        conn = abrir_conexion()
        try:
            row = conn.execute("""
                SELECT id, username, password_hash
                FROM usuario
                WHERE id = ?
            """, (id_usuario,)).fetchone()

            return UsuarioDAO._desde_fila(row) if row else None

        finally:
            conn.close()

    @staticmethod
    def buscar_por_username(username):
        conn = abrir_conexion()
        try:
            row = conn.execute("""
                SELECT id, username, password_hash
                FROM usuario
                WHERE username = ?
            """, (username,)).fetchone()

            return UsuarioDAO._desde_fila(row) if row else None

        finally:
            conn.close()

    @staticmethod
    def listar():
        conn = abrir_conexion()
        try:
            rows = conn.execute("""
                SELECT id, username, password_hash
                FROM usuario
                ORDER BY id
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