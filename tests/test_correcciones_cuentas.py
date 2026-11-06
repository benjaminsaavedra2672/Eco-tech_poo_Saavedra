import unittest
from unittest.mock import patch
from types import SimpleNamespace
from servicios.mi_cuenta import actualizar_mi_usuario, actualizar_mi_clave
from dominio.usuario import Usuario

class TestCuentas(unittest.TestCase):
    def test_nombre_duplicado(self):
        sesion = SimpleNamespace(id=1, username='otro')
        with patch('persistencia.usuario_dao.UsuarioDAO.buscar_por_username', return_value=SimpleNamespace(id=2)):
            with self.assertRaisesRegex(ValueError, 'registrado'):
                actualizar_mi_usuario(sesion, 'ocupado')

    def test_cambiar_nombre(self):
        sesion = SimpleNamespace(id=3, username='administrador2')
        with patch('persistencia.usuario_dao.UsuarioDAO.buscar_por_username', return_value=None), patch('persistencia.usuario_dao.UsuarioDAO.actualizar_username', return_value=True) as actualizar:
            self.assertTrue(actualizar_mi_usuario(sesion, 'Nuevo_Admin'))
            actualizar.assert_called_once_with(3, 'nuevo_admin')
            self.assertEqual(sesion.username, 'nuevo_admin')

    def test_clave_actual_incorrecta(self):
        sesion = SimpleNamespace(id=3, username='administrador2')
        cuenta = SimpleNamespace(id=3, autenticar=lambda clave: False)
        with patch('persistencia.usuario_dao.UsuarioDAO.buscar_por_username', return_value=cuenta):
            with self.assertRaisesRegex(ValueError, 'incorrecta'):
                actualizar_mi_clave(sesion, 'mal', 'NuevaClave123')

    def test_cambio_clave(self):
        sesion = SimpleNamespace(id=3, username='administrador2')
        cuenta = SimpleNamespace(id=3, autenticar=lambda clave: clave == 'Actual123')
        with patch('persistencia.usuario_dao.UsuarioDAO.buscar_por_username', return_value=cuenta), patch('persistencia.usuario_dao.UsuarioDAO.actualizar_password', return_value=True) as actualizar:
            self.assertTrue(actualizar_mi_clave(sesion, 'Actual123', 'NuevaClave123'))
            self.assertTrue(Usuario.desde_hash('administrador2', actualizar.call_args.args[1]).autenticar('NuevaClave123'))

    def test_registros_no_sombra_dao(self):
        from menus.menu_registro_tiempo import menu_registros
        with patch('menus.menu_registro_tiempo.OperacionesAdmin') as proxy, patch('builtins.input', return_value='0'):
            menu_registros(SimpleNamespace(rol='admin'))
            proxy.assert_called_once()

if __name__ == '__main__':
    unittest.main()
