"""Transforma una respuesta JSON ya interpretada a una entidad."""
from dominio.indicador import Indicador
from servicios.consulta_moneda import extraer_primero

class DeserializadorIndicador:
    @staticmethod
    def desde_api(datos, codigo="CLP"):
        fecha, valor = extraer_primero(datos, codigo)
        return Indicador(fecha=fecha, valor=valor, codigo=codigo)
