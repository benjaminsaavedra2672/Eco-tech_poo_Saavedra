"""Pruebas U3; ejecutar: python -m unittest discover -s tests -v"""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from dominio.indicador import Indicador
from dominio.usuario import Usuario
from servicios.deserializador_indicador import DeserializadorIndicador
from servicios.gestion_operaciones import OperacionesAdmin, registrar_mis_horas
from servicios.indicadores import consultar_indicador, obtener_historial
from persistencia.crear_bd import crear_tablas
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.indicador_dao import IndicadorDAO

class Sesion:
    def __init__(self, rol, empleado_id=1):
        self.id = 1
        self.rol = rol
        self.empleado_id = empleado_id
        self.username = 'prueba'

class Unidad3(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.env = patch.dict(os.environ, {'DB_ENGINE':'sqlite','DB_NAME':self.tmp.name.split('/')[-1] + '.db'})
        self.env.start(); self.addCleanup(self.env.stop)
        # DB_NAME is relative to project root; isolate by random basename and delete at end
        from persistencia.conexion import ROOT
        self.db = ROOT / os.environ['DB_NAME']
        self.addCleanup(lambda: self.db.unlink(missing_ok=True))
        crear_tablas()
        self.admin, self.empleado = Sesion('admin'), Sesion('empleado')

    def test_roles_en_servicio(self):
        with self.assertRaises(PermissionError):
            OperacionesAdmin(self.empleado, DepartamentoDAO)
        admin_dao = OperacionesAdmin(self.admin, DepartamentoDAO)
        self.assertIsInstance(admin_dao.listar(), list)
        admin_dao.sesion = self.empleado
        with self.assertRaises(PermissionError):
            admin_dao.insertar('Prohibido')

    def test_empleado_no_registra_proyecto_ajeno(self):
        with self.assertRaises(PermissionError):
            registrar_mis_horas(self.empleado, 999, '2026-11-05', 2, 'Prueba')

    def test_usuario_validacion_y_hash(self):
        for invalido in ('', 'ab', 'nombre con espacios'):
            with self.assertRaises(ValueError): Usuario.normalizar_usuario(invalido)
        u = Usuario('ANA_1', 'ClaveSegura123')
        self.assertTrue(u.autenticar('ClaveSegura123'))
        self.assertFalse(u.autenticar('Incorrecta'))

    def test_fecha_y_valor(self):
        for fecha in ('no disponible', '2026-02-30', ''):
            with self.assertRaises(ValueError): Indicador(fecha, 950)
        with self.assertRaises(ValueError): Indicador('2026-11-05', -2)
        self.assertEqual(Indicador('Thu, 05 Nov 2026 00:00:01 +0000', 950).fecha, '2026-11-05')

    def test_deserializacion_upsert_historial(self):
        datos = {'result':'success','rates':{'CLP':950},'time_last_update_utc':'Thu, 05 Nov 2026 00:00:01 +0000'}
        a = DeserializadorIndicador.desde_api(datos, 'CLP')
        IndicadorDAO.guardar(a)
        IndicadorDAO.guardar(Indicador('2026-11-05', 951))
        filas = IndicadorDAO.listar('CLP')
        self.assertEqual(len(filas), 1)
        self.assertEqual(filas[0]['valor'], 951)
        self.assertEqual(obtener_historial(self.empleado,'CLP')[0]['fecha'],'2026-11-05')

    def test_api_y_respaldo(self):
        datos = {'result':'success','rates':{'CLP':900},'time_last_update_utc':'Thu, 05 Nov 2026 00:00:01 +0000'}
        with patch('servicios.indicadores.obtener_datos', return_value=datos):
            resultado = consultar_indicador(self.empleado,'CLP')
        self.assertEqual(resultado['origen'], 'API')
        with patch('servicios.indicadores.obtener_datos', side_effect=ValueError('sin red')):
            respaldo = consultar_indicador(self.empleado,'CLP')
        self.assertEqual(respaldo['origen'], 'BD local (respaldo)')
        with self.assertRaises(PermissionError):
            consultar_indicador(None,'CLP')

if __name__ == '__main__': unittest.main()
