"""Coordina autorización, API, deserialización, guardado y respaldo."""
import requests
from servicios.consulta_moneda import obtener_datos
from servicios.deserializador_indicador import DeserializadorIndicador
from persistencia.indicador_dao import IndicadorDAO
from servicios.permisos import exigir_sesion as verificar_sesion

def exigir_sesion(sesion):
    verificar_sesion(sesion)

def consultar_indicador(sesion, codigo="CLP"):
    exigir_sesion(sesion)
    codigo = codigo.strip().upper()
    if codigo not in ("CLP", "EUR", "GBP", "BRL", "ARS", "PEN", "MXN"):
        raise ValueError("Moneda no admitida.")
    try:
        datos = obtener_datos()
        indicador = DeserializadorIndicador.desde_api(datos, codigo)
    except (requests.RequestException, ValueError, KeyError, TypeError) as error:
        respaldo = IndicadorDAO.ultimo(codigo)
        if respaldo is None:
            return {"dato": None, "origen": "SIN DATOS", "mensaje": f"API no disponible y sin respaldo: {error}"}
        return {"dato": respaldo, "origen": "BD local (respaldo)", "mensaje": "API no disponible; se muestra la última observación guardada, no una cotización actual."}
    dato = vars(indicador).copy()
    try:
        IndicadorDAO.guardar(indicador)
        mensaje = "Observación guardada o actualizada correctamente."
    except Exception as error:
        mensaje = f"Consulta válida, pero no fue posible guardar en BD: {error}"
    return {"dato": dato, "origen": "API", "mensaje": mensaje}

def obtener_historial(sesion, codigo=None):
    exigir_sesion(sesion)
    if codigo is not None:
        if not isinstance(codigo, str) or codigo.upper() not in ('CLP','EUR','GBP','BRL','ARS','PEN','MXN'):
            raise ValueError('Moneda no admitida.')
    return IndicadorDAO.listar(codigo)
