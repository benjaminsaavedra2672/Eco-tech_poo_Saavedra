"""Operaciones administrativas: autorización obligatoria antes de cualquier DAO."""
from servicios.permisos import exigir_admin, exigir_empleado
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO

class OperacionesAdmin:
    def __init__(self, sesion, dao):
        exigir_admin(sesion)
        self.sesion, self.dao = sesion, dao

    def __getattr__(self, nombre):
        # Solo se exponen métodos conocidos de cada DAO, sin atributos privados.
        permitidos = {
            DepartamentoDAO: {'insertar','listar','buscar_por_id','actualizar','eliminar'},
            ProyectoDAO: {'insertar','listar','buscar_por_id','actualizar','eliminar','asignar_empleado'},
            RegistroTiempoDAO: {'insertar','listar','buscar_por_id','actualizar','eliminar'},
        }
        if nombre not in permitidos.get(self.dao, set()):
            raise AttributeError(nombre)
        metodo = getattr(self.dao, nombre)
        def autorizado(*args, **kwargs):
            exigir_admin(self.sesion)
            return metodo(*args, **kwargs)
        return autorizado

def mis_proyectos(sesion):
    return ProyectoDAO.listar_por_empleado(exigir_empleado(sesion))

def registrar_mis_horas(sesion, proyecto_id, fecha, horas, descripcion):
    empleado_id = exigir_empleado(sesion)
    asignados = {int(p['id_proyecto']) for p in ProyectoDAO.listar_por_empleado(empleado_id)}
    if type(proyecto_id) is not int or proyecto_id not in asignados:
        raise PermissionError('El proyecto no está asignado al empleado autenticado.')
    return RegistroTiempoDAO.insertar(empleado_id, proyecto_id, fecha, horas, descripcion)
