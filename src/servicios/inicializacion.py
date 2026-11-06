"""Configuración explícita de la cuenta administradora inicial."""
import os
from dominio.usuario import Usuario
from persistencia.usuario_dao import UsuarioDAO

def asegurar_administrador():
    existente = UsuarioDAO.buscar_por_username("admin")
    if existente:
        if existente.rol != "admin":
            raise RuntimeError("La cuenta admin existe sin rol admin. Revise los permisos manualmente.")
        return
    clave = os.getenv("ECOTECH_ADMIN_PASSWORD")
    if not clave:
        raise RuntimeError("Defina ECOTECH_ADMIN_PASSWORD en el entorno o .env antes de crear la primera cuenta admin.")
    Usuario.validar_clave(clave)
    UsuarioDAO.insertar(Usuario("admin", clave, rol="admin"))
    print("Cuenta administradora inicial creada con contraseña configurada por el usuario.")
