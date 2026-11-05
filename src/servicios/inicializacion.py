"""Inicializa una cuenta administradora si aún no existe."""
import os
from dominio.usuario import Usuario
from persistencia.usuario_dao import UsuarioDAO


def asegurar_administrador():
    existente = UsuarioDAO.buscar_por_username("admin")
    if existente:
        if existente.rol != "admin":
            UsuarioDAO.cambiar_rol(existente.id, "admin")
        return

    password = os.getenv("ECOTECH_ADMIN_PASSWORD", "Admin123!")
    admin = Usuario("admin", password, rol="admin")
    UsuarioDAO.insertar(admin)
    print("Cuenta inicial creada: usuario admin.")
    if os.getenv("ECOTECH_ADMIN_PASSWORD"):
        print("Se utilizó la contraseña definida en ECOTECH_ADMIN_PASSWORD.")
    else:
        print("Contraseña temporal: Admin123!")
    print("Cambia esta contraseña antes de usar el sistema en un entorno real.")
