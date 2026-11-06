"""Observación validada de un tipo de cambio externo."""
from datetime import datetime, timezone, date
from email.utils import parsedate_to_datetime
from math import isfinite

class Indicador:
    def __init__(self, fecha, valor, codigo="CLP", fuente="open.er-api.com", verificado_en=None):
        if not isinstance(fecha, str) or not fecha.strip():
            raise ValueError("La fecha del indicador es obligatoria.")
        if not isinstance(codigo, str) or not codigo.isalpha() or len(codigo) != 3:
            raise ValueError("El código debe tener tres letras.")
        if type(valor) not in (float, int) or not isfinite(valor) or valor <= 0:
            raise ValueError("El valor debe ser un número positivo y finito.")
        fecha = fecha.strip()
        try:
            # El proveedor original entrega RFC 2822; también aceptamos ISO 8601.
            if len(fecha) == 10:
                dia = date.fromisoformat(fecha)
            else:
                try:
                    dia = datetime.fromisoformat(fecha.replace('Z', '+00:00')).date()
                except ValueError:
                    dia = parsedate_to_datetime(fecha).date()
            self.fecha = dia.isoformat()
        except (ValueError, TypeError, IndexError, OverflowError) as exc:
            raise ValueError('Fecha de indicador inválida; use ISO o fecha HTTP válida.') from exc
        self.valor = float(valor)
        self.codigo = codigo.upper()
        if not isinstance(fuente, str) or not fuente.strip():
            raise ValueError('La fuente es obligatoria.')
        self.fuente = fuente.strip()
        self.unidad = f"{self.codigo}/USD"
        self.verificado_en = verificado_en or datetime.now(timezone.utc).isoformat()
