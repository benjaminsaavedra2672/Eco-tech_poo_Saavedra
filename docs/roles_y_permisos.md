# Roles y permisos EcoTech

## Administrador (`admin`)
- Crear, listar, buscar, actualizar y eliminar empleados.
- Administrar departamentos.
- Crear, modificar, eliminar y asignar proyectos.
- Consultar y administrar registros de tiempo.
- Listar cuentas, cambiar roles y restablecer contraseñas.
- Crear otras cuentas administradoras.
- Consultar las API de tiempo y conversión de monedas.

## Empleado (`empleado`)
- Consultar sus propios datos.
- Consultar solamente los proyectos que tiene asignados.
- Registrar horas únicamente en proyectos que tiene asignados.
- Consultar solamente sus propios registros de tiempo.
- Consultar las API de tiempo y conversión de monedas.

## Modelo de cuenta
El rol de acceso se guarda en `usuario.rol` y solo admite `admin` o `empleado`. El campo `empleado.rol` conserva el cargo laboral (por ejemplo, Gerente o Analista), que no concede permisos administrativos. La cuenta del empleado se vincula con su ficha mediante `empleado.usuario_id`; `usuario.empleado_id` mantiene la referencia inversa para localizar su ficha. Las cuentas administradoras pueden existir sin una ficha de empleado.

## Cuenta inicial
En la primera ejecución se crea `admin` con contraseña temporal `Admin123!`. Se puede definir `ECOTECH_ADMIN_PASSWORD` en `.env` antes de la primera ejecución para establecer otra contraseña. Cambia la contraseña inicial y no uses credenciales de demostración en producción.
