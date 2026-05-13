# Servicio Técnico y Tecnología S.A.

Plataforma web desarrollada con Django para administrar inventario de productos tecnológicos, gestionar usuarios y controlar reservas con descuento automático de stock.

---

## Contenido

1. [Descripción general](#descripción-general)
2. [Objetivos del sistema](#objetivos-del-sistema)
3. [Funciones principales](#funciones-principales)
4. [Arquitectura y tecnologías](#arquitectura-y-tecnologías)
5. [Modelo funcional](#modelo-funcional)
6. [Requisitos](#requisitos)
7. [Instalación local](#instalación-local)
8. [Ejecución del sistema](#ejecución-del-sistema)
9. [Despliegue en Render](#despliegue-en-render)
10. [Variables de entorno](#variables-de-entorno)
11. [Gestión de datos y usuarios](#gestión-de-datos-y-usuarios)
12. [Pruebas](#pruebas)
13. [Copias de seguridad](#copias-de-seguridad)
14. [Solución de problemas](#solución-de-problemas)
15. [Estructura del proyecto](#estructura-del-proyecto)
16. [Autor y licencia](#autor-y-licencia)

---

## Descripción general

**Servicio Técnico y Tecnología S.A.** es una aplicación web pensada para la administración de productos tecnológicos y la gestión de reservas o apartados. El sistema permite que los usuarios consulten un catálogo público, se registren, inicien sesión y realicen reservas bajo reglas de negocio definidas. Desde el panel administrativo se pueden administrar productos, categorías, usuarios y apartados.

La aplicación fue construida con un enfoque práctico para uso académico y demostración institucional, con controles de stock dinámicos, expiración automática de reservas y documentación técnica para soporte y mantenimiento.

---

## Objetivos del sistema

- Centralizar la administración del inventario en una sola aplicación web.
- Permitir reservas de productos con límites por usuario y por producto.
- Mantener el stock actualizado de forma automática cuando un apartado expira, se cancela o se confirma.
- Proteger el acceso mediante autenticación, roles y sesiones con expiración por inactividad.
- Facilitar el mantenimiento técnico con comandos de administración, pruebas y health checks.

---

## Funciones principales

### Usuarios

- Registro de nuevos clientes.
- Inicio y cierre de sesión.
- Perfil de usuario con actualización de datos personales.
- Cambio de contraseña.
- Control de sesiones por inactividad.

### Productos y categorías

- Registro y edición de productos desde el panel administrativo.
- Administración de categorías.
- Visualización pública del catálogo.
- Control de stock total y stock disponible.
- Soporte para imágenes locales o en Cloudinary.

### Reservas / apartados

- Creación de reservas desde el catálogo.
- Límite de 5 unidades por producto y hasta 3 tipos diferentes activos por usuario.
- Expiración automática de apartados pendientes.
- Repone stock cuando un apartado expira o se cancela.
- Panel administrativo con resumen de apartados.

### Seguridad y operación

- Bloqueo temporal por intentos fallidos de acceso.
- Timeouts de sesión configurables.
- Health check y readiness check para monitoreo de despliegue.

---

## Arquitectura y tecnologías

### Stack tecnológico

- Python 3.10+
- Django 5.2
- Gunicorn
- PostgreSQL en producción
- SQLite en desarrollo local
- Bootstrap 5
- WhiteNoise para archivos estáticos
- Cloudinary para almacenamiento de imágenes
- Django Jazzmin para el panel administrativo

### Componentes principales

- **Backend**: lógica de negocio, autenticación, reservas, validaciones y administración.
- **Frontend**: plantillas HTML con Bootstrap y estilos personalizados.
- **Base de datos**: persistencia de usuarios, productos, categorías y apartados.
- **Almacenamiento de imágenes**: Cloudinary o almacenamiento local en desarrollo.

### Salud del servicio

La aplicación expone dos rutas livianas para monitoreo:

- `/healthz/` devuelve un estado rápido de aplicación.
- `/readyz/` verifica conectividad básica con la base de datos.

Estas rutas ayudan a Render a comprobar el servicio sin cargar vistas pesadas.

---

## Modelo funcional

### Entidades principales

- **Usuario**: cliente o administrador.
- **Categoría**: agrupación de productos.
- **Producto**: artículo tecnológico con stock y precio.
- **Apartado**: reserva realizada por un usuario.
- **HeroBanner**: banner principal de la landing.

### Relaciones

- Un usuario puede crear múltiples apartados.
- Un producto puede estar asociado a múltiples apartados.
- Una categoría puede agrupar múltiples productos.

### Reglas de negocio

- Cada producto tiene stock total y stock disponible.
- Un usuario no puede superar 5 unidades activas por producto.
- Un usuario no puede mantener más de 3 productos distintos activos al mismo tiempo.
- Los apartados pendientes expiran automáticamente al superar el tiempo límite.

---

## Requisitos

### Requisitos de hardware

#### Desarrollo local

- Procesador: 2 núcleos o superior.
- Memoria RAM: 4 GB mínimo, 8 GB recomendado.
- Espacio en disco: 2 GB libres como mínimo.
- Conexión a internet para dependencias y servicios externos.

#### Producción en Render

- Servicio web con Python 3.11.
- PostgreSQL administrado por Render.
- Conexión estable a Cloudinary si se usan imágenes en nube.

### Requisitos de software

- Git.
- Python 3.10 o superior.
- pip.
- Navegador moderno.
- Opcional: pgAdmin o DBeaver para administrar PostgreSQL.

---

## Instalación local

### 1. Clonar el repositorio

```bash
git clone https://github.com/camilouan/servicio-tecnico-web.git
cd servicio-tecnico-web
```

### 2. Crear y activar entorno virtual

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

Si usas PowerShell y aparece un error al ejecutar `Activate.ps1` por la política de ejecución, usa una de estas opciones:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

O bien activa el entorno desde CMD, o ejecuta Python directamente sin activar el entorno:

```bash
venv\Scripts\python.exe manage.py runserver
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

En Windows, `psycopg2-binary` no se instala porque el proyecto usa SQLite por defecto en desarrollo local. En Render sí se instala normalmente, ya que el despliegue corre sobre Linux y usa PostgreSQL cuando `DATABASE_URL` está definida.

### 4. Configurar variables locales

Crear un archivo `.env` o definir variables en el sistema:

```bash
DEBUG=True
SECRET_KEY=clave-local-segura
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Cargar datos iniciales

```bash
python manage.py seed
```

Si deseas subir imágenes de ejemplo a Cloudinary durante la carga inicial:

```bash
SEED_UPLOAD_REMOTE_IMAGES=True python manage.py seed
```

---

## Ejecución del sistema

### Desarrollo local

```bash
python manage.py runserver
```

Abrir en navegador:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/admin/`

### Verificación rápida

```bash
curl http://127.0.0.1:8000/healthz/
curl http://127.0.0.1:8000/readyz/
```

---

## Despliegue en Render

Este proyecto está preparado para Render y funciona correctamente en un flujo compatible con plan gratuito.

### Build

El archivo `build.sh` ejecuta:

- instalación de dependencias
- migraciones
- collectstatic
- carga de datos opcional
- creación de superusuario opcional

### Start

Render usa Gunicorn con concurrencia configurable:

- `WEB_CONCURRENCY` por defecto: `2`
- `GUNICORN_THREADS` por defecto: `2`

### Health check

La ruta de monitoreo configurada es:

- `/healthz/`

### Importante para Render Free

- No existe shell interactivo en el plan gratuito.
- Los comandos `shell` y `dbshell` deben ejecutarse en una terminal local o en un entorno autorizado.
- Si necesitas crear el primer superusuario en producción, activa temporalmente `RUN_CREATESU_ON_BUILD=True`, realiza un deploy y luego vuelve a dejarlo en `False`.

### Recomendaciones de producción

- `DEBUG=False`
- `SECRET_KEY` definida desde Render
- `DATABASE_URL` apuntando a PostgreSQL administrado
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` si se usan imágenes en nube
- `DB_CONN_MAX_AGE=60`
- `DB_CONNECT_TIMEOUT=5`
- `DB_STATEMENT_TIMEOUT_MS=20000`

---

## Variables de entorno

### Básicas

```bash
DEBUG=False
SECRET_KEY=valor-seguro-y-unico
ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1
```

### Base de datos

```bash
DATABASE_URL=postgresql://usuario:clave@host:puerto/nombre_bd
DB_CONN_MAX_AGE=60
DB_CONNECT_TIMEOUT=5
DB_STATEMENT_TIMEOUT_MS=20000
```

### Cloudinary

```bash
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
```

### Rendimiento y despliegue

```bash
WEB_CONCURRENCY=2
GUNICORN_THREADS=2
RUN_SEED_ON_BUILD=False
RUN_CREATESU_ON_BUILD=False
SEED_UPLOAD_REMOTE_IMAGES=False
```

### Seguridad de sesión

```bash
LOGIN_MAX_FAILED_ATTEMPTS=5
LOGIN_LOCKOUT_SECONDS=900
SESSION_INACTIVITY_TIMEOUT=1800
```

---

## Gestión de datos y usuarios

### Crear superusuario

```bash
python manage.py createsuperuser
```

### Cargar datos de prueba

```bash
python manage.py seed
```

### Crear superusuario en producción sin shell de Render

1. Activar temporalmente `RUN_CREATESU_ON_BUILD=True`.
2. Hacer deploy.
3. Confirmar la creación del usuario administrador.
4. Volver a dejar la variable en `False`.

### Revisar usuarios desde una terminal local

```bash
python manage.py shell
>>> from inventario.models import Usuario
>>> Usuario.objects.all()
```

### Cambiar contraseña de un usuario

```bash
python manage.py shell
>>> from inventario.models import Usuario
>>> u = Usuario.objects.get(username='usuario')
>>> u.set_password('nueva_clave_segura')
>>> u.save()
```

### Bloquear o desbloquear usuario

```bash
python manage.py shell
>>> from inventario.models import Usuario
>>> u = Usuario.objects.get(username='usuario')
>>> u.activo = False
>>> u.save()
```

---

## Pruebas

### Ejecutar pruebas del proyecto

```bash
python manage.py test inventario
```

### Validación recomendada antes de desplegar

- Verificar que las migraciones estén aplicadas.
- Ejecutar pruebas automáticas.
- Confirmar que `/healthz/` responda 200.
- Confirmar que `/readyz/` responda 200.

---

## Copias de seguridad

### Base de datos

```bash
python manage.py dumpdata > backup.json
```

### Restaurar datos

```bash
python manage.py loaddata backup.json
```

### Media local

```bash
tar -czf media_backup.tar.gz media/
```

### Recomendación operativa

- Guardar un backup antes de migraciones grandes.
- Mantener una copia del archivo `.env` en un lugar seguro.
- Registrar cada cambio importante en Git.

---

## Solución de problemas

### La página se queda cargando

Posibles causas:

- La instancia está en cold start.
- Hay una consulta lenta a base de datos.
- El servicio requiere más workers o threads.

Acciones:

- Revisar `/healthz/`.
- Revisar logs del despliegue.
- Confirmar `DATABASE_URL` y timeouts.

### No cargan los estilos

Posibles causas:

- `collectstatic` no se ejecutó.
- `DEBUG=True` en producción.

### No suben imágenes

Posibles causas:

- Credenciales de Cloudinary faltantes.
- Variables de entorno mal configuradas.

### Login bloqueado

Posibles causas:

- Muchos intentos fallidos.
- Bloqueo temporal por seguridad.

### PowerShell bloquea la activación del entorno virtual

Si al activar el entorno virtual en Windows aparece un error relacionado con `Activate.ps1` o con la política de ejecución de PowerShell, prueba lo siguiente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Ese cambio solo aplica a la sesión actual. Si prefieres no tocar la política, también puedes ejecutar los comandos con el intérprete del entorno virtual directamente:

```bash
venv\Scripts\python.exe manage.py runserver
```

### Productos vacíos

Posibles causas:

- Falta ejecutar `python manage.py seed`.
- La base de datos no contiene registros iniciales.

---

## Estructura del proyecto

```text
servicio_tecnico/
├── build.sh
├── manage.py
├── requirements.txt
├── render.yaml
├── README.md
├── MANUAL_TECNICO.md
├── GUIA_RAPIDA_ADMIN.md
├── inventario/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── middleware.py
│   ├── context_processors.py
│   ├── tests.py
│   ├── test_landing.py
│   ├── management/commands/
│   └── templates/
├── servicio_tecnico/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── static/
├── staticfiles/
└── media/
```

---

## Estado del proyecto

- Sistema funcional.
- Base de datos estructurada.
- Control de stock dinámico.
- Sistema de reservas operativo.
- Interfaz responsive con Bootstrap.
- Health checks y despliegue preparados para Render.

---

## Autor y licencia

**Autor:** Camilo Andrés Parra Cuenca  
**Programa:** Tecnología en Construcción de Software  
**Institución:** Universidad Antonio Nariño  

**Licencia:** Proyecto académico de uso educativo.
