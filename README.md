# EcoTech Solutions

Aplicación de consola en Python para administrar empleados, departamentos, proyectos y registros de tiempo. Incluye persistencia SQLite o MySQL/MariaDB, autenticación con hash PBKDF2 y control de acceso por roles.

## Funcionalidades

- **Administrador (`admin`)**: administra empleados, departamentos, proyectos, registros de tiempo, usuarios y roles.
- **Empleado (`empleado`)**: consulta su perfil, revisa sus proyectos asignados, registra horas en proyectos propios y consulta sus registros.
- **Servicios API**: ambos perfiles pueden consultar el tiempo actual de Santiago y las tasas de cambio/conversión de monedas.
- **Seguridad**: las contraseñas se guardan como hash; los menús se separan según el rol de la cuenta.
- **Persistencia**: SQLite por defecto; MySQL/MariaDB configurable mediante `.env`.

## Instalación y ejecución en Windows

Desde la carpeta principal:

```powershell
py -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python -m compileall src
python -m unittest discover -s tests -v
python src\\main.py
```

La aplicación crea las tablas y carga los datos de demostración al iniciar.

## Accesos iniciales

La primera ejecución crea la cuenta administradora:

| Rol | Usuario | Contraseña inicial |
|---|---|---|
| Administrador | `admin` | `Admin123!` |

También se cargan cuentas de empleados para pruebas:

| Usuario | Contraseña | Rol |
|---|---|---|
| `semilla_ana` | `EcoTechDemo2026!` | empleado |
| `semilla_carlos` | `EcoTechDemo2026!` | empleado |
| `semilla_valentina` | `EcoTechDemo2026!` | empleado |
| `semilla_diego` | `EcoTechDemo2026!` | empleado |

**Importante:** cambia la contraseña inicial del administrador antes de usar el programa con datos reales. Puedes definir `ECOTECH_ADMIN_PASSWORD` en `.env` antes del primer inicio. El cambio se aplica cuando se crea por primera vez la cuenta `admin`.

## Configurar MySQL/MariaDB

1. Inicia el servidor y crea la base de datos usando `sql/mysql_crear_base.sql`.
2. Configura `.env`:

```dotenv
DB_ENGINE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ecotech
DB_USER=tu_usuario
DB_PASSWORD=tu_clave
```

3. Ejecuta `python src\\main.py`.

Para usar SQLite, deja `DB_ENGINE=sqlite` y `DB_NAME=ecotech.db`.

## Estructura

```text
src/
  dominio/       Entidades y reglas de negocio
  menus/         Menú principal, menú admin, menú empleado y menú API
  persistencia/  Conexión, esquema y DAO
  servicios/     Autenticación, inicialización y consumo de API
  main.py        Punto de entrada
tests/           Pruebas automatizadas
sql/             Script de creación de base MySQL/MariaDB
docs/            Documentación del proyecto
```
