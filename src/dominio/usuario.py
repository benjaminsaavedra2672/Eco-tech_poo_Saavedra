import hashlib
import hmac
import os


class Usuario:
    """Cuenta de acceso con permisos separados del cargo del empleado."""
    ROLES = ("admin", "empleado")

    def __init__(self, username: str, password: str, empleado_id: int | None = None, rol: str = "empleado"):
        username = username.strip()
        if not username:
            raise ValueError("El nombre de usuario es obligatorio.")
        if not password:
            raise ValueError("La contraseña es obligatoria.")
        self.username = username
        self.empleado_id = empleado_id
        self.rol = self.validar_rol(rol)
        self._password_hash = self._crear_hash(password)

    @classmethod
    def validar_rol(cls, rol):
        if not isinstance(rol, str) or rol.strip().lower() not in cls.ROLES:
            raise ValueError("El rol debe ser admin o empleado.")
        return rol.strip().lower()

    @staticmethod
    def _crear_hash(password: str, salt: bytes | None = None) -> str:
        salt = salt or os.urandom(16)
        derived = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, 200_000
        )
        return f"{salt.hex()}${derived.hex()}"

    @classmethod
    def desde_hash(cls, username: str, password_hash: str, rol: str = "empleado"):
        """Reconstruye el objeto desde la base sin tratar el hash como contraseña."""
        obj = cls.__new__(cls)
        obj.username = username
        obj.empleado_id = None
        obj.rol = cls.validar_rol(rol)
        obj._password_hash = password_hash
        return obj

    def autenticar(self, password: str) -> bool:
        try:
            salt_hex, expected_hex = self._password_hash.split("$", 1)
            candidate = self._crear_hash(password, bytes.fromhex(salt_hex))
            _, candidate_hex = candidate.split("$", 1)
            return hmac.compare_digest(expected_hex, candidate_hex)
        except (ValueError, TypeError):
            return False

    def encriptarPassword(self, password: str) -> bool:
        if not password:
            return False
        self._password_hash = self._crear_hash(password)
        return True

    def _hash_para_persistencia(self) -> str:
        """Uso interno de persistencia; no imprime ni expone el hash en el menú."""
        return self._password_hash

    def exportarReporte(self, tipo: str, formato: str) -> bool:
        return bool(tipo.strip() and formato.strip())

