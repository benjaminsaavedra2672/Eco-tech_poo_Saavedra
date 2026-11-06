"""Persistencia de observaciones económicas; clave: fuente+código+fecha."""
from persistencia.conexion import abrir_conexion, motor_actual
from dominio.indicador import Indicador

class IndicadorDAO:
    @staticmethod
    def guardar(indicador):
        conn = abrir_conexion()
        try:
            if motor_actual() == "sqlite":
                conn.execute("""INSERT INTO indicador (fuente,codigo,fecha,valor,unidad,verificado_en)
                    VALUES (?,?,?,?,?,?) ON CONFLICT(fuente,codigo,fecha)
                    DO UPDATE SET valor=excluded.valor, unidad=excluded.unidad,
                    verificado_en=excluded.verificado_en""", (
                    indicador.fuente,indicador.codigo,indicador.fecha,indicador.valor,
                    indicador.unidad,indicador.verificado_en))
            else:
                conn.execute("""INSERT INTO indicador (fuente,codigo,fecha,valor,unidad,verificado_en)
                    VALUES (?,?,?,?,?,?) ON DUPLICATE KEY UPDATE valor=VALUES(valor),
                    unidad=VALUES(unidad),verificado_en=VALUES(verificado_en)""", (
                    indicador.fuente,indicador.codigo,indicador.fecha,indicador.valor,
                    indicador.unidad,indicador.verificado_en))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def listar(codigo=None):
        conn = abrir_conexion()
        try:
            sql = "SELECT fuente,codigo,fecha,valor,unidad,verificado_en FROM indicador"
            params = ()
            if codigo:
                sql += " WHERE codigo=?"
                params = (codigo.upper(),)
            sql += " ORDER BY fecha DESC, verificado_en DESC"
            filas = conn.execute(sql, params).fetchall()
            return [dict(fila) for fila in filas]
        finally:
            conn.close()

    @staticmethod
    def ultimo(codigo):
        filas = IndicadorDAO.listar(codigo)
        return filas[0] if filas else None
