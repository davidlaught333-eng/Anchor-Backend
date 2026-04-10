Anchor App Backend API (v1.4)

API backend para la aplicación Anchor, encargada de la gestión de usuarios, autenticación y control de acceso basado en roles (RBAC).

Por: David Felipe Rodríguez Sierra
Curso: PRI1 - ICIB

Descripción

Esta versión introduce un sistema de roles de usuario, permitiendo restringir el acceso a endpoints según permisos.

Roles disponibles:

user (por defecto)
admin
Tecnologías utilizadas
Python 3.x
FastAPI – Framework para construir la API
SQLite – Base de datos ligera local
Pydantic – Validación de datos de entrada
bcrypt – Hash de contraseñas
JWT (JSON Web Tokens) – Autenticación segura
Funcionalidades
Registro de usuario (POST /register)

Crea un nuevo usuario con:

username (único)
password (segura)

Todos los usuarios se registran con rol user.

Validación de contraseña:
Al menos 8 caracteres
Al menos una letra mayúscula
Al menos una letra minúscula
Al menos un número
Respuesta exitosa:
{"message": "Usuario registrado exitosamente"}
Errores posibles:
Usuario ya existe
Contraseña débil
Inicio de sesión (POST /login)

Permite autenticación de usuarios registrados.

Input:
username
password
Respuesta:
{
  "access_token": "<token_jwt>",
  "token_type": "bearer"
}

El token incluye:

sub (username)
role (rol del usuario)
Listar usuarios (GET /users)

Protegido. Solo accesible por usuarios con rol admin.

Respuesta:
{
  "users": ["usuario1", "usuario2"]
}
Cambiar rol de usuario (PUT /users/role)

Protegido. Solo accesible por usuarios con rol admin.

Input:
{
  "username": "user1",
  "role": "admin"
}
Respuesta:
{
  "message": "Rol de user1 actualizado a admin"
}
Errores posibles:
Rol inválido
Usuario no existe
Intento de modificar el propio rol (opcional)
Home (GET /)

Verifica que la API está activa:

{"message": "Anchor API en ejecucion..."}
Setup inicial (POST /setup-admin)

Crea el primer usuario administrador.

{"message": "Admin creado"}

Importante: este endpoint debe eliminarse después del primer uso.

Base de datos

Archivo: users.db

Tabla users:

id – INTEGER PRIMARY KEY AUTOINCREMENT
username – TEXT único, obligatorio
password – TEXT, almacenado con hash bcrypt
role – TEXT (user o admin)
Funciones principales
init_db() – Inicializa la base de datos
get_user(username) – Obtiene usuario
add_user(username, password, role) – Crea usuario
update_user_role(username, role) – Cambia rol
list_all_users() – Lista usuarios
Autenticación y autorización
Tokens JWT firmados con SECRET_KEY y algoritmo HS256
Expiración configurable (ACCESS_TOKEN_EXPIRE_MINUTES)
Middleware verify_token valida el token
Control de acceso basado en roles mediante require_role
Testing

Accede a la documentación interactiva:

http://localhost:8000/docs

Flujo recomendado:

Crear administrador (/setup-admin)
Iniciar sesión (/login)
Autorizar usando el token
Probar endpoints protegidos
Instalación
git clone https://github.com/davidlaught333-eng/Anchor-Backend.git
cd anchor-app-backend

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install fastapi uvicorn bcrypt python-jose pydantic
Configuración

Archivo .env (opcional):

SECRET_KEY=supersecretkey
ACCESS_TOKEN_EXPIRE_MINUTES=60
DB_FILE=users.db
Ejecución
uvicorn app.main:app --reload

Disponible en:
http://localhost:8000

Modelos de datos
UserRegister
username: str
password: str
UserLogin
username: str
password: str
UpdateRole
username: str
role: str
Consideraciones de seguridad
No permitir selección de rol en /register
Eliminar /setup-admin en producción
Usar un SECRET_KEY seguro
Los tokens JWT son stateless (requieren re-login tras cambios de rol)
Roadmap futuro
Refresh tokens
Sistema de permisos granular
Migración a PostgreSQL
Dockerización
Logs y auditoría
Versión

v1.4 – Role-Based Access Control (RBAC)