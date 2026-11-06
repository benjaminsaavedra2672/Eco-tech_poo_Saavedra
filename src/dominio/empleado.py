from datetime import date
from .usuario import Usuario


class Empleado(Usuario):
    MIN_NOMBRE = 2
    MAX_NOMBRE = 100
    MIN_CORREO = 6
    MAX_CORREO = 254

    @classmethod
    def validar_nombre(cls, nombre):
        if not isinstance(nombre, str):
            raise TypeError("El nombre debe ser texto.")
        nombre = nombre.strip()
        if not cls.MIN_NOMBRE <= len(nombre) <= cls.MAX_NOMBRE:
            raise ValueError("El nombre debe tener entre 2 y 100 caracteres.")
        return nombre

    @classmethod
    def validar_correo(cls, correo):
        if not isinstance(correo, str):
            raise TypeError("El correo debe ser texto.")
        correo = correo.strip().lower()
        if not cls.MIN_CORREO <= len(correo) <= cls.MAX_CORREO or correo.count("@") != 1 or "." not in correo.split("@",1)[1] or " " in correo:
            raise ValueError("Ingrese un correo válido (ejemplo: nombre@dominio.cl).")
        return correo

    def __init__(
        self, username: str, password: str, id_empleado: int | None = None,
        nombre: str = "", correo: str = "", direccion: str = "",
        telefono: str = "", fecha_contrato: str | None = None,
        salario: float = 0.0, rol: str = "Empleado",
        departamento_id: int | None = None,
    ):
        super().__init__(username, password)
        self.id_empleado = id_empleado
        self.nombre = nombre.strip()
        self.correo = correo.strip()
        self.direccion = direccion.strip()
        self.telefono = telefono.strip()
        self.fecha_contrato = fecha_contrato or date.today().isoformat()
        self.salario = float(salario)
        self.rol = rol.strip() or "Empleado"
        self.departamento_id = departamento_id
        self.validar()

    def validar(self):
        self.nombre = self.validar_nombre(self.nombre)
        self.correo = self.validar_correo(self.correo)
        if self.salario < 0:
            raise ValueError("El salario no puede ser negativo.")

    def obtenerSalario(self) -> float:
        return self.salario

    def actualizarPerfil(self, nombre, correo, direccion, telefono) -> bool:
        nombre, correo = nombre.strip(), correo.strip()
        if not nombre:
            return False
        if "@" not in correo or "." not in correo.rsplit("@", 1)[-1]:
            return False
        self.nombre, self.correo = nombre, correo
        self.direccion, self.telefono = direccion.strip(), telefono.strip()
        return True
