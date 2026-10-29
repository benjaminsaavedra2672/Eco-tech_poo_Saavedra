# EcoTech Solutions — 

Este es mi proyecto de programación orientada a objetos para administrar información de EcoTech Solutions el programa está hecho en Python y permite trabajar con empleados, departamentos, proyectos y registros de tiempo también incluye inicio de sesión y persistencia de datos con SQLite o MySQL/MariaDB

## ¿Qué incluye?

- **Empleados:** registrar, consultar, modificar y eliminar empleados.
- **Departamentos:** administrar los departamentos de la empresa.
- **Proyectos:** crear y mantener la información de los proyectos.
- **Registros de tiempo:** guardar las horas trabajadas asociadas a empleados y proyectos.
- **Usuarios e inicio de sesión:** validar las credenciales usando contraseñas almacenadas como hash, no como texto plano.
- **Relación usuario-empleado:** cada empleado se vincula con su cuenta de usuario en la base de datos.
- **Persistencia:** se puede ejecutar con SQLite para probarlo localmente o configurar MySQL/MariaDB.
- **Pruebas:** incluye pruebas automatizadas básicas y archivos de apoyo del proyecto.

## Requisitos

- Para usar MySQL/MariaDB, tener el servidor iniciado y una base de datos creada.
- Las dependencias indicadas en `requirements.txt`.

## Cómo instalar y ejecutar en Windows

Abre PowerShell en la carpeta principal del proyecto y ejecuta:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Por defecto, el archivo `.env.example` deja configurado SQLite 

Para comprobar la sintaxis, ejecutar las pruebas y abrir el sistema:

```powershell
python -m compileall src
python -m unittest discover -s tests -v
python src\main.py
```

Al iniciar, el sistema prepara las tablas y carga datos de demostración que no estén registrados todavía después mostrara la pantalla de inicio de sesión.

## Inicio de sesión de prueba

| Usuario | Contraseña |
|---|---|
| `semilla.ana` | `EcoTechDemo2026!` |
| `semilla.carlos` | `EcoTechDemo2026!` |
| `semilla.valentina` | `EcoTechDemo2026!` |
| `semilla.diego` | `EcoTechDemo2026!` |

Son credenciales de demostración para el entorno 
## Usar MySQL o MariaDB

1. Inicia MySQL/MariaDB y crea la base de datos. Puedes revisar el archivo `sql/mysql_crear_base.sql`.
2. En el archivo `.env`, configura los datos de conexión. Por ejemplo:

```dotenv
DB_ENGINE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ecotech
DB_USER=tu_usuario
DB_PASSWORD=tu_clave
```

3. Ejecuta el programa desde la carpeta principal:

```powershell
python src\main.py
```

Para volver a SQLite, configura `DB_ENGINE=sqlite` y `DB_NAME=ecotech.db` en `.env`.

No subas el archivo `.env` con contraseñas reales al repositorio. El archivo `.env.example` sirve como referencia de configuración.

## Organización del código

```text
src/
  dominio/       Clases y reglas principales del sistema
  menus/         Menús e interacción por consola
  persistencia/  Conexión, creación de tablas y DAO
  servicios/     Funciones de apoyo
  main.py        Punto de entrada del programa
tests/           Pruebas automatizadas
sql/             Script de apoyo para MySQL
 docs/           Diagrama y documentos de revisión
```

Los DAO se encargan de las operaciones con la base de datos, mientras que las clases del dominio representan los datos y comportamientos del sistema.

## Archivos de apoyo

- `docs/diagrama de ecotech BJ.png`: diagrama del proyecto.
- `docs/validacion_ia.md`: explicación del uso de IA como apoyo.
- `docs/revision_critica_semilla.md`: revisión de la carga de datos de demostración.

## Uso de inteligencia artificial

La IA se utilizó como apoyo para revisar ideas, detectar errores y mejorar algunas partes de la documentación y del código. La revisión, adaptación y ejecución del proyecto forman parte del trabajo realizado; los detalles están en `docs/validacion_ia.md`.
