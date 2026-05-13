# MANUAL TÉCNICO
## Servicio Técnico y Tecnología S.A. - Sistema de Gestión de Inventario y Reservas

---

## PORTADA

**SERVICIO TÉCNICO Y TECNOLOGÍA S.A.**

**Sistema de Gestión de Productos Tecnológicos y Reservas**

**MANUAL TÉCNICO PARA ADMINISTRADORES**

Versión: 1.0  
Fecha: Mayo 2026  
Autor: CAMILO ANDRES PARRA CUENCA
Clasificación: Documentación Técnica Interna

---

## TABLA DE CONTENIDO

1. [Introducción](#introducción)
2. [Descripción General del Sistema](#descripción-general-del-sistema)
3. [Características de los Usuarios del Sistema](#características-de-los-usuarios-del-sistema)
4. [Requisitos de Hardware y Software](#requisitos-de-hardware-y-software)
5. [Instalación y Configuración](#instalación-y-configuración)
6. [Gestión de Usuarios](#gestión-de-usuarios)
7. [Ejecución del Sistema](#ejecución-del-sistema)
8. [Copias de Seguridad y Recuperación](#copias-de-seguridad-y-recuperación)
9. [Desinstalación del Sistema](#desinstalación-del-sistema)
10. [Solución de Problemas](#solución-de-problemas)
11. [Mantenimiento Preventivo](#mantenimiento-preventivo)
12. [Contacto y Soporte](#contacto-y-soporte)

---

## INTRODUCCIÓN

### Propósito del Manual

Este Manual Técnico está dirigido al personal de Tecnologías de Información (TI) y administradores del sistema responsables de:

- Instalar y configurar la aplicación en entornos de producción, desarrollo y pruebas
- Administrar usuarios, permisos y roles del sistema
- Realizar tareas de mantenimiento, backup y recuperación de datos
- Diagnosticar y resolver problemas técnicos
- Optimizar el rendimiento de la aplicación
- Implementar políticas de seguridad

### Alcance

Este documento cubre:

- Arquitectura técnica de la aplicación
- Procedimientos de instalación en diferentes entornos
- Configuración de variables de entorno críticas
- Administración de la base de datos
- Políticas de respaldo y recuperación
- Procedimientos de diagnóstico y troubleshooting

### Audiencia

- Administradores de sistemas
- Ingenieros de infraestructura
- Personal de soporte técnico nivel 2
- Desarrolladores responsables del mantenimiento

---

## DESCRIPCIÓN GENERAL DEL SISTEMA

### Visión General

El sistema **Servicio Técnico y Tecnología S.A.** es una aplicación web desarrollada en Django para gestionar inventario de productos tecnológicos y permitir que clientes realicen reservas con control automático de stock.

### Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    NAVEGADOR DEL USUARIO                 │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS
                     ▼
┌─────────────────────────────────────────────────────────┐
│              SERVIDOR WEB (Gunicorn + Django)            │
│  - Runtime: Python 3.11                                  │
│  - Framework: Django 5.2                                 │
│  - Servidor App: Gunicorn (2 workers, 2 threads)        │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌─────────┐ ┌──────────┐ ┌──────────────┐
   │ BD Prod │ │  BD Dev  │ │ DB SQLite    │
   │(Postgre │ │(Postgre  │ │ (Local)      │
   │  SQL)   │ │  SQL)    │ │              │
   └─────────┘ └──────────┘ └──────────────┘
        │            │            │
        └────────────┼────────────┘
                     ▼
        ┌──────────────────────────┐
        │  Cloudinary (Almacenaje  │
        │  de Imágenes en Nube)    │
        └──────────────────────────┘
```

### Stack Tecnológico

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| **Backend** | Django | 5.2.11 |
| **Lenguaje** | Python | 3.11 |
| **Servidor Web** | Gunicorn | 25.1.0 |
| **BD Producción** | PostgreSQL | 12+ |
| **BD Desarrollo** | SQLite 3 | Incluida |
| **Almacenaje Imágenes** | Cloudinary | API REST |
| **Frontend** | Bootstrap 5 | HTML5/CSS |
| **Admin UI** | Django Jazzmin | 3.0.4 |

### Flujo de Datos Principal

1. Cliente accede a `/` (landing)
2. Visualiza productos y categorías desde BD
3. Registra cuenta o inicia sesión
4. Realiza reserva (apartado) de producto
5. Sistema descuenta stock automáticamente
6. Admin revisa y confirma/cancela apartado
7. Stock se repone automáticamente si expira

---

## CARACTERÍSTICAS DE LOS USUARIOS DEL SISTEMA

### Roles y Permisos

#### 1. Cliente (Usuario Regular)

**Permisos:**
- Ver catálogo de productos
- Registrarse en la plataforma
- Iniciar/cerrar sesión
- Realizar reservas (máx. 5 unidades por artículo, 3 tipos diferentes activos)
- Ver historial de sus reservas
- Actualizar perfil personal
- Cambiar contraseña

**Restricciones:**
- No puede acceder al panel administrativo
- No puede editar productos
- No puede confirmar reservas propias
- Sesión expira por inactividad (30 minutos)

#### 2. Administrador (Staff/Superusuario)

**Permisos:**
- Acceso completo al panel administrativo
- Crear, editar, eliminar productos y categorías
- Confirmar, cancelar o rechazar reservas
- Visualizar reporte de reservas pendientes
- Generar códigos de verificación
- Administrar usuarios
- Ver logs del sistema
- Cambiar configuración de políticas

**Restricciones:**
- Debe usar contraseña fuerte
- Acceso limitado a IP permitidas (en producción)
- Auditoría de cambios registrada

### Ciclo de Vida de Usuario

```
Registro → Email Verificación → Activo → Inactividad → Bloqueado → Reactivación
                                  ↓                          ↓
                              Suspendido             Reinicio de Sesión
```

### Políticas de Sesión

- **Timeout por inactividad**: 30 minutos (configurable)
- **Max. intentos fallidos de login**: 5
- **Duración del bloqueo**: 15 minutos tras 5 fallos
- **Ciclo de vida de cookie**: 30 minutos

---

## REQUISITOS DE HARDWARE Y SOFTWARE

### Requisitos de Hardware

#### Entorno de Desarrollo Local

| Recurso | Mínimo | Recomendado |
|---------|--------|------------|
| **Procesador** | 2 cores | 4 cores |
| **Memoria RAM** | 4 GB | 8 GB |
| **Disco Duro** | 2 GB libres | 10 GB libres |
| **Conexión** | 1 Mbps | 10 Mbps |

#### Entorno de Producción (Render)

| Recurso | Especificación |
|---------|---|
| **Tipo Instancia** | Web Service (Paid) |
| **CPU** | 0.5 vCPU (mínimo) |
| **Memoria** | 1 GB |
| **Almacenaje BD** | PostgreSQL 12 GB |
| **Bandwidth** | Sin límite |

### Requisitos de Software

#### Sistema Operativo

| Sistema | Versión | Soporte |
|---------|---------|--------|
| **Windows** | 10 / 11 / Server 2019+ | Completo |
| **macOS** | 10.14+ | Completo |
| **Linux** | Ubuntu 20.04+ / CentOS 7+ | Completo |

#### Dependencias Obligatorias

```
Python                      3.10+
Git                         2.25+
pip (Python Package Manager) 21+
PostgreSQL (Producción)     12+
```

#### Dependencias del Proyecto (Python)

Ver archivo `requirements.txt`:
- Django 5.2.11
- Gunicorn 25.1.0
- Pillow 12.1.1 (Procesamiento de imágenes)
- django-cloudinary-storage 0.3.0
- psycopg2-binary 2.9.10 (Driver PostgreSQL)
- django-jazzmin 3.0.4
- whitenoise 6.11.0 (Servir static files)

#### Software Recomendado para Administración

| Tool | Propósito | Descargar |
|------|-----------|-----------|
| **pgAdmin 4** | Administración PostgreSQL | https://www.pgadmin.org |
| **VS Code** | Editor de código | https://code.visualstudio.com |
| **Git Bash** | Control de versiones | https://git-scm.com |
| **Postman** | Pruebas de API | https://www.postman.com |

---

## INSTALACIÓN Y CONFIGURACIÓN

### 1. Instalación en Entorno Local (Desarrollo)

#### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/camilouan/servicio-tecnico-web.git
cd servicio-tecnico-web
```

#### Paso 2: Crear Entorno Virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Salida esperada:**
```
Successfully installed Django-5.2.11 gunicorn-25.1.0 ...
```

#### Paso 4: Configurar Variables de Entorno

Crear archivo `.env` en raíz del proyecto:

```bash
# .env (NUNCA SUBIR A GIT)
DEBUG=True
SECRET_KEY=tu-clave-secreta-superamegamuylargarandomizada-aqui
ALLOWED_HOSTS=localhost,127.0.0.1
LANGUAGE_CODE=es-co
TIME_ZONE=America/Bogota
SESSION_INACTIVITY_TIMEOUT=1800
LOGIN_MAX_FAILED_ATTEMPTS=5
LOGIN_LOCKOUT_SECONDS=900
```

#### Paso 5: Ejecutar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

**Salida esperada:**
```
Operations to perform:
  Apply all migrations: inventario, auth, ...
Running migrations:
  Applying inventario.0001_initial ... OK
```

#### Paso 6: Crear Superusuario

```bash
python manage.py createsuperuser
```

**Ejemplo:**
```
Username: admin
Email: admin@ejemplo.com
Password: MiContraseñaSegura123!
Password (again): MiContraseñaSegura123!
Superuser created successfully.
```

#### Paso 7: Cargar Datos Iniciales (Opcional)

```bash
# Solo cargar estructura (sin imágenes)
python manage.py seed

# Con imágenes de ejemplo en Cloudinary
SEED_UPLOAD_REMOTE_IMAGES=True python manage.py seed
```

#### Paso 8: Ejecutar Servidor Local

```bash
python manage.py runserver
```

**Salida esperada:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Acceder a: `http://localhost:8000/`  
Panel Admin: `http://localhost:8000/admin/`

---

### 2. Instalación en Render (Producción)

#### Paso 1: Crear Repositorio en GitHub

```bash
git remote add origin https://github.com/tu-usuario/repo.git
git push -u origin main
```

#### Paso 2: Crear Servicio en Render

1. Acceder a https://render.com
2. Conectar cuenta GitHub
3. Crear nuevo **Web Service**
4. Seleccionar repositorio
5. Configurar:
   - **Name**: `servicio-tecnico`
   - **Environment**: `Python 3.11`
   - **Build Command**: `chmod +x build.sh ; ./build.sh`
   - **Start Command**: Se lee de `render.yaml`
   - **Plan**: Starter (Free) o Superior

#### Paso 3: Configurar Variables de Entorno en Render

Panel → Environment → Agregar variables:

```
DEBUG=False
SECRET_KEY=[generar con: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"]
ALLOWED_HOSTS=.onrender.com
CLOUDINARY_CLOUD_NAME=tu-cloud
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
WEB_CONCURRENCY=2
GUNICORN_THREADS=2
DB_CONN_MAX_AGE=60
DB_CONNECT_TIMEOUT=5
DB_STATEMENT_TIMEOUT_MS=20000
RUN_SEED_ON_BUILD=False
RUN_CREATESU_ON_BUILD=False
```

#### Paso 4: Crear Base de Datos PostgreSQL en Render

1. En Render → Crear **PostgreSQL**
2. Seleccionar plan (Free para pruebas)
3. Copiar **Internal Database URL**
4. En el Web Service, agregar variable:
   ```
   DATABASE_URL=[url copiada]
   ```

#### Paso 5: Deploy Inicial

1. Hacer push a GitHub:
   ```bash
   git add .
   git commit -m "Initial Render deployment"
   git push origin main
   ```

2. Render detecta cambio y comienza build automático
3. Ver progreso en Render Dashboard → Build & Deployment Logs

**Logs esperados:**
```
Installing dependencies...
Running migrations...
Collecting static files...
Build completed successfully!
Service started on https://servicio-tecnico.onrender.com
```

#### Paso 6: Verificar Salud del Servicio

```bash
curl https://servicio-tecnico.onrender.com/healthz/
# Respuesta esperada: {"status": "ok"}

curl https://servicio-tecnico.onrender.com/readyz/
# Respuesta esperada: {"status": "ready"}
```

#### Paso 7: Crear Primer Superusuario en Producción

Una sola vez después del primer deploy:

1. En plan gratuito de Render no se dispone de shell interactivo. Para crear el
primer superusuario en producción, use una ejecución puntual del build con la
variable de entorno habilitada:

2. En Render Dashboard → Web Service → Environment
3. Definir temporalmente:
  ```bash
  RUN_CREATESU_ON_BUILD=True
  ```
4. Hacer deploy
5. Verificar que el usuario admin fue creado
6. Volver a dejar la variable en `False` para los siguientes despliegues

Si el usuario ya existe, el comando no lo duplica.

---

## GESTIÓN DE USUARIOS

### Crear Usuario Administrador

#### Desde CLI (Línea de Comandos)

```bash
python manage.py createsuperuser
# Ingresar datos solicitados
```

#### Desde Panel Administrativo Django

1. Acceder a `/admin/`
2. Ir a **Authentication and Authorization** → **Users**
3. Click en **Add User**
4. Ingresar:
   - **Username**: único
   - **Password**: mínimo 8 caracteres
   - **Confirm password**: repetir
5. Guardar y editar:
   - **Staff status**: ✓ Marcar
   - **Superuser status**: ✓ Marcar
   - **Permissions**: Seleccionar permisos específicos

### Crear Usuario Regular (Cliente)

#### Automático (Desde Aplicación)

1. Acceder a `/registro/`
2. Completar formulario con:
   - Username, Email, Nombres, Apellidos
   - Teléfono, Documento, Dirección, Ciudad
   - Contraseña (validación: mín. 8 caracteres)
3. Aceptar políticas de privacidad
4. Enviar

#### Manual (Desde Admin)

1. Panel Admin → Usuarios → Agregar Usuario
2. Establecer rol: **Cliente** (por defecto)
3. Marcar **Activo**: ✓
4. Guardar

### Cambiar Contraseña de Usuario

#### Usuario Modifica su Propia Contraseña

1. Login en `/login/`
2. Ir a **Mi Perfil** (esquina superior)
3. Sección "Cambiar Contraseña"
4. Ingresar contraseña actual
5. Nueva contraseña (mín. 8 caracteres)
6. Confirmar

#### Administrador Resetea Contraseña

1. Panel Admin → Usuarios
2. Click en usuario
3. Scroll a sección **Password**
4. Click en **Change password**
5. Ingresar nueva contraseña
6. Guardar

### Bloquear/Desbloquear Usuario

#### Bloquear Usuario

En Panel Admin:
1. Usuarios → Seleccionar usuario
2. Desmarcar: **Activo** ☐
3. Guardar

El usuario ya no podrá iniciar sesión.

#### Desbloquear Usuario

1. Usuarios → Seleccionar usuario
2. Marcar: **Activo** ✓
3. Guardar

### Ver Intentos de Login Fallidos

```bash
# Desde una terminal local con acceso al proyecto
python manage.py shell
>>> from django.core.cache import cache
>>> cache.get('login_security:username:ip:lock')
```

### Asignar Roles y Permisos

#### Permisos Granulares

1. Panel Admin → Usuarios → Seleccionar usuario
2. Scroll a **Groups** y **User Permissions**
3. Agregar permisos individuales:
   - `inventario.add_producto` (Crear productos)
   - `inventario.change_producto` (Editar)
   - `inventario.delete_producto` (Eliminar)
   - Etc.
4. Guardar

---

## EJECUCIÓN DEL SISTEMA

### Iniciar en Desarrollo

```bash
# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Ejecutar servidor
python manage.py runserver
```

Disponible en: `http://localhost:8000/`

### Iniciar en Producción (Render)

**Automático**: Render redeploy al hacer push a GitHub

**Manual**: En Render Dashboard → Deploy

### Verificar Estado del Servicio

#### Health Check Liviano (Responde rápido)
```bash
curl https://tudominio.onrender.com/healthz/
# {"status": "ok"}
```

#### Readiness Check (Verifica BD)
```bash
curl https://tudominio.onrender.com/readyz/
# {"status": "ready"} o {"status": "error", "detail": "..."}
```

#### Revisar Logs en Vivo

**Render Dashboard**:
1. Web Service → Logs
2. Filtrar por fecha/hora
3. Buscar términos: `ERROR`, `WARN`, `request timeout`

**Local**:
```bash
# Ver logs de Django en terminal donde ejecutas runserver
```

### Reiniciar Servicio

**Desarrollo:**
```bash
# Presionar CTRL+C en terminal
# Ejecutar: python manage.py runserver
```

**Producción (Render)**:
1. Dashboard → Web Service → Settings
2. Click en **Restart service**
3. O: Hacer nuevo push a GitHub

---

## COPIAS DE SEGURIDAD Y RECUPERACIÓN

### 1. Backup de Base de Datos PostgreSQL

#### Backup Manual Local (Durante Desarrollo)

```bash
# Exportar datos de todos los modelos
python manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json
```

**Resultado**:
```json
[
# Desde una terminal local con acceso al proyecto
    "model": "inventario.usuario",
    "pk": 1,
    "fields": {"username": "admin", ...}
  },
  ...
]
```

#### Backup Automático en Render

Render PostgreSQL mantiene **backups automáticos** cada 24 horas.

**Acceder a backups**:
1. Render Dashboard → PostgreSQL instance
2. Tab **Backups**
3. Seleccionar fecha
4. Click **Restore** (restaura a nueva instancia temporal)

#### Backup Manual en Producción (PostgreSQL)

```bash
# Desde terminal en servidor Render o local
pg_dump -h [HOST] -U [USER] -d [DBNAME] > backup_prod_$(date +%Y%m%d).sql

# Ejemplo:
pg_dump -h postgres-db.render.internal \
  -U servicio_tecnico_user \
  -d servicio_tecnico_db > backup_prod_20260502.sql
```

**Credenciales están en**:
- Render Dashboard → PostgreSQL → Connection info

### 2. Backup de Archivos de Media (Imágenes)

#### Si usa Cloudinary (Recomendado)

Cloudinary mantiene backup automático en nube. Sin acción requerida.

#### Si usa almacenaje local

```bash
# Comprimir carpeta /media/
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/

# O en Windows:
Compress-Archive -Path media/ -DestinationPath media_backup_$(Get-Date -Format 'yyyyMMdd').zip
```

### 3. Backup de Configuración y Código

```bash
# Respaldar .env y settings
cp .env .env.backup_$(date +%Y%m%d)
cp servicio_tecnico/settings.py settings.py.backup

# Código siempre está en Git (usar git tags para versiones)
git tag -a v1.0.0 -m "Versión estable para presentación"
git push origin v1.0.0
```

### 4. Recuperar desde Backup

#### Restaurar Base de Datos JSON

```bash
python manage.py loaddata backup_20260501_120000.json
```

#### Restaurar PostgreSQL SQL

```bash
# Crear BD vacía
createdb -h [HOST] -U [USER] servicio_tecnico_restored

# Restaurar dump
psql -h [HOST] -U [USER] -d servicio_tecnico_restored < backup_prod_20260502.sql
```

#### Restaurar Media (Si aplica)

```bash
# Descomprimir
tar -xzf media_backup_20260502.tar.gz
```

### 5. Plan de Backup Recomendado

| Elemento | Frecuencia | Retención | Método |
|----------|-----------|-----------|--------|
| **BD Producción** | Diaria | 30 días | Render automático |
| **Código** | Por commit | Indefinido | Git tags mensuales |
| **Media (si local)** | Semanal | 12 semanas | Descarga manual |
| **Configuración** | Por cambio | 3 meses | Backup manual |

---

## DESINSTALACIÓN DEL SISTEMA

### Desinstalación en Desarrollo Local

#### Opción 1: Limpiar Todo

```bash
# 1. Desactivar entorno
deactivate

# 2. Eliminar carpeta del proyecto
rmdir /s /q C:\ruta\a\servicio_tecnico
# macOS/Linux: rm -rf ~/servicio_tecnico
```

#### Opción 2: Mantener Código, Eliminar Entorno

```bash
# 1. Desactivar entorno
deactivate

# 2. Eliminar entorno virtual
rmdir /s /q venv
# macOS/Linux: rm -rf venv
```

#### Opción 3: Limpiar Base de Datos Local

```bash
# Solo eliminar datos sin afectar código
rm db.sqlite3

# O resetear desde cero
python manage.py migrate --fake-initial zero
python manage.py migrate
```

### Desinstalación en Render (Producción)

#### Eliminar Servicio Web

1. Render Dashboard → Web Service
2. Settings → Danger Zone
3. Click **Delete Service**
4. Confirmar nombre

**Impacto**: La aplicación ya no está disponible. Clientes no pueden acceder.

#### Mantener Base de Datos (Para Análisis Posterior)

1. **NO** eliminar PostgreSQL instance
2. Descarga backup: PostgreSQL → Backups → Restore (a archivo SQL)
3. Luego sí eliminar PostgreSQL instance

#### Recuperar Código

```bash
# El código siempre está en GitHub, puede clonar nuevamente
git clone https://github.com/usuario/servicio-tecnico-web.git
```

---

## SOLUCIÓN DE PROBLEMAS

### Problema 1: "La aplicación se queda cargando"

#### Síntomas
- Páginas tardan más de 10 segundos
- Algunas vistas responden, otras cuelgan
- Problema se resuelve si se redeploy

#### Causas Posibles
1. **Cold start en Render Free** (instancia dormida)
2. **Consultas pesadas a BD sin optimizar**
3. **Timeout de conexión a PostgreSQL**
4. **Escasos workers de Gunicorn**

#### Solución

**Paso 1**: Verificar salud rápida
```bash
curl https://tudominio.onrender.com/healthz/
```

Si responde rápido → No es un problema de arranque.

**Paso 2**: Aumentar workers/threads en Render
- Variables de entorno:
  - `WEB_CONCURRENCY=4` (aumentar de 2)
  - `GUNICORN_THREADS=4` (aumentar de 2)
- Redeploy

**Paso 3**: Ajustar timeout de BD
- Variable: `DB_STATEMENT_TIMEOUT_MS=30000` (aumentar de 20000)
- Variable: `DB_CONNECT_TIMEOUT=10` (aumentar de 5)

**Paso 4**: Revisar logs
```
Render Dashboard → Logs → Filtrar "slow query" o "timeout"
```

#### Prevención

- Usar índices en consultas frecuentes (ya implementados)
- Usar `.select_related()` y `.prefetch_related()`
- Cachear resultados que no cambian frecuentemente

---

### Problema 2: "Error: Módulo importa no encontrado"

#### Síntomas
```
ModuleNotFoundError: No module named 'django'
ImportError: cannot import name 'CLOUDINARY_STORAGE'
```

#### Causas Posibles
1. Entorno virtual no activado
2. `requirements.txt` no instalado
3. Versión incompatible de paquete

#### Solución

```bash
# 1. Verificar entorno virtual activo
# Windows: Should show (venv) in prompt
# macOS/Linux: source venv/bin/activate

# 2. Reinstalar dependencias
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# 3. Limpiar caché
pip cache purge

# 4. Verificar instalación
python -c "import django; print(django.VERSION)"
# Debe mostrar: (5, 2, ...)
```

---

### Problema 3: "Error de migración: Tabla ya existe"

#### Síntomas
```
django.db.utils.OperationalError: relation "inventario_apartado" already exists
```

#### Causas Posibles
1. Corriste `migrate` dos veces
2. Base de datos parcialmente inicializada
3. Conflicto en cambios de esquema

#### Solución

```bash
# Opción 1: Forzar estado conocido (desarrollo)
python manage.py migrate --fake inventario zero
python manage.py migrate

# Opción 2: Crear BD nueva (cuidado: perdés datos)
# Eliminar db.sqlite3 y correr:
python manage.py migrate

# Opción 3: En PostgreSQL producción
# Contactar con Render support si es crítico
```

---

### Problema 4: "Usuario bloqueado tras intentos fallidos"

#### Síntomas
- "Acceso bloqueado temporalmente. Intenta en X minuto(s)"
- Aunque contraseña es correcta

#### Causas Posibles
1. 5 intentos de login fallidos (normal, por seguridad)
2. IP fue bloqueada temporalmente

#### Solución

**Esperar**: Bloqueo expira automáticamente en **15 minutos**

**O resetear manualmente**:
```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.delete('login_security:admin:192.168.1.1:lock')
>>> exit()
```

**Prevención**: Tomar nota de contraseña, usar gestor de contraseñas

---

### Problema 5: "Error de conexión a PostgreSQL"

#### Síntomas
```
django.db.utils.OperationalError: could not connect to server
FATAL: database "servicio_tecnico_db" does not exist
```

#### Causas Posibles
1. Variable `DATABASE_URL` no configurada
2. Credenciales incorrectas
3. BD PostgreSQL no está corriendo
4. Firewall bloquea conexión

#### Solución

**Paso 1**: Verificar variable `DATABASE_URL`

```bash
# En Render Dashboard → Environment
# Debe existir: DATABASE_URL=postgresql://...

# Localmente en .env:
# DATABASE_URL=postgresql://usuario:password@localhost:5432/servicio_tecnico
```

**Paso 2**: Probar conexión

```bash
# Instalar herramienta psql
pip install psycopg2-binary

# Conectar
psql postgresql://usuario:password@hostname:5432/dbname

# O en Python:
python manage.py dbshell
```

**Paso 3**: Verificar BD existe

```bash
# Si no existe, Render la crea automáticamente
# O manualmente:
createdb -h hostname -U usuario servicio_tecnico_db
```

---

### Problema 6: "Error al subir imágenes a Cloudinary"

#### Síntomas
```
cloudinary.exceptions.Error: Invalid credentials
Error uploading to Cloudinary: Invalid API Key
```

#### Causas Posibles
1. Variables Cloudinary no configuradas
2. Credenciales expiradas o incorrectas
3. Límite de almacenaje excedido

#### Solución

**Paso 1**: Verificar credenciales en Render

```
Render Dashboard → Environment → Buscar:
- CLOUDINARY_CLOUD_NAME
- CLOUDINARY_API_KEY
- CLOUDINARY_API_SECRET
```

**Paso 2**: Regenerar credenciales

1. Acceder a Cloudinary Dashboard
2. Settings → API Keys
3. Regenerar si es necesario
4. Copiar nuevos valores a Render

**Paso 3**: Reiniciar servicio en Render

```
Render Dashboard → Web Service → Restart
```

---

### Problema 7: "Static files no se cargan en producción"

#### Síntomas
- CSS y JavaScript no funcionan en `onrender.com`
- Funciona en desarrollo
- Console browser muestra 404 para `/static/`

#### Causas Posibles
1. No corriste `collectstatic`
2. WhiteNoise no configurado
3. DEBUG=True en producción

#### Solución

**Paso 1**: Ejecutar collectstatic

```bash
python manage.py collectstatic --noinput
```

**Paso 2**: Verificar settings.py

```python
WHITENOISE_USE_FINDERS = True
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

**Paso 3**: En Render, incluir en `build.sh`

```bash
echo "Collecting static files..."
python manage.py collectstatic --noinput
```

(Ya está incluido en tu build.sh)

---

### Problema 8: "Productos no aparecen en catálogo"

#### Síntomas
- Página `/productos/` carga pero sin artículos
- Admin muestra productos pero no aparecen en vista pública

#### Causas Posibles
1. No correr comando `seed`
2. Productos creados con `activo=False`
3. BD vacía

#### Solución

```bash
# Cargar datos iniciales
python manage.py seed

# O con imágenes de Cloudinary:
SEED_UPLOAD_REMOTE_IMAGES=True python manage.py seed

# Verificar desde shell
python manage.py shell
>>> from inventario.models import Producto
>>> Producto.objects.count()
20  # Debe mostrar cantidad

>>> Producto.objects.filter(activo=True).count()
20  # Verificar que están activos
```

---

### Problema 9: "Error: `DEBUG` debe estar en False en producción"

#### Síntomas
```
DEBUG=True detectado en entorno de producción.
Por seguridad, cambiar a False.
```

#### Causas Posibles
1. Variable `DEBUG` no está configurada en Render
2. `.env` subido accidentalmente a producción

#### Solución

**Render Dashboard → Environment**:
```
DEBUG=False
```

**Verificar que no existe en código**:
```bash
git rm --cached .env  # Si lo subiste por error
echo ".env" >> .gitignore
git push
```

---

### Problema 10: "Apartados no expiran automáticamente"

#### Síntomas
- Apartados con `estado='pendiente'` caducos no cambian a `expirado`
- Stock no se repone tras expiración

#### Causas Posibles
1. Nadie ha accedido a vistas que llaman `actualizar_apartados_vencidos`
2. Throttle de expiración aún activo (espera 60 segundos)

#### Solución

```bash
# Ejecutar manualmente
python manage.py shell
>>> from inventario.models import Apartado
>>> Apartado.actualizar_apartados_vencidos()
3  # Retorna cantidad actualizada

# Verificar
>>> Apartado.objects.filter(estado='expirado').count()
3
```

**Prevención**: Implementar tarea programada (Celery/APScheduler)

```bash
# En roadmap futuro: agregar task scheduler para expiraciones automáticas
```

---

## MANTENIMIENTO PREVENTIVO

### Tareas Semanales

- [ ] Verificar logs en Render por errores
- [ ] Revisar alertas de rendimiento
- [ ] Comprobar que health check responde

### Tareas Mensuales

- [ ] Revisar conteo de usuarios activos
- [ ] Auditoría de permisos y roles
- [ ] Descargar backup manual de BD
- [ ] Revisar uso de Cloudinary (almacenaje)
- [ ] Actualizar dependencias menores de Python
  ```bash
  pip list --outdated
  pip install --upgrade [paquete]
  ```

### Tareas Trimestrales

- [ ] Limpieza de datos obsoletos:
  ```bash
  # Eliminar apartados expirados muy antiguos
  python manage.py shell
  >>> from inventario.models import Apartado
  >>> from django.utils import timezone
  >>> from datetime import timedelta
  >>> hace_3_meses = timezone.now() - timedelta(days=90)
  >>> Apartado.objects.filter(estado='expirado', fecha_apartado__lt=hace_3_meses).delete()
  ```
- [ ] Revisar y optimizar queries lentas
- [ ] Incremento de capacidad si aplica

### Tareas Anuales

- [ ] Auditoría de seguridad completa
- [ ] Renovación de certificados SSL (Render lo maneja)
- [ ] Revisión de políticas de contraseña
- [ ] Plan de upgrade de versión Django (evaluar)
- [ ] Renovación de credenciales sensibles

### Verificar Salud de la Aplicación

#### Script de Health Check (bash)

```bash
#!/bin/bash
# health_check.sh

URL="https://tudominio.onrender.com"
HEALTH_URL="$URL/healthz/"
READINESS_URL="$URL/readyz/"

echo "Verificando salud de $URL..."

# Health check
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)
if [ $HTTP_CODE -eq 200 ]; then
    echo "✓ Health check: OK"
else
    echo "✗ Health check: FALLÓ (Código: $HTTP_CODE)"
fi

# Readiness check
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" $READINESS_URL)
if [ $HTTP_CODE -eq 200 ]; then
    echo "✓ Readiness check: OK"
else
    echo "✗ Readiness check: FALLÓ (Código: $HTTP_CODE)"
fi
```

Ejecutar:
```bash
bash health_check.sh
```

---

## CONTACTO Y SOPORTE

### Recursos de Documentación

- **Documentación Django**: https://docs.djangoproject.com/
- **Documentación Render**: https://render.com/docs
- **Documentación PostgreSQL**: https://www.postgresql.org/docs/
- **Documentación Cloudinary**: https://cloudinary.com/documentation

### Contacto de Soporte

| Área | Contacto | Disponibilidad |
|------|----------|---|
| **Errores de Aplicación** | [Email Dev Team] | Horas de oficina |
| **Infraestructura (Render)** | support@render.com | 24/7 |
| **Base de Datos** | Render Support | 24/7 |
| **Almacenaje (Cloudinary)** | support@cloudinary.com | 24/7 |

### Escalación de Problemas

1. **Nivel 1 (TI Local)**: Verificar logs, health checks
2. **Nivel 2 (Dev Team)**: Revisar código, queries
3. **Nivel 3 (Providers)**: Contactar Render/Cloudinary

---

## ANEXOS

### Anexo A: Variables de Entorno Completas

```bash
# Seguridad
DEBUG=False
SECRET_KEY=valor-aleatorio-super-largo-seguro
ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1

# Base de Datos
DATABASE_URL=postgresql://user:pass@host:5432/dbname
DB_CONN_MAX_AGE=60
DB_CONNECT_TIMEOUT=5
DB_STATEMENT_TIMEOUT_MS=20000

# Cloudinary (Imágenes)
CLOUDINARY_CLOUD_NAME=cloud-name
CLOUDINARY_API_KEY=api-key
CLOUDINARY_API_SECRET=api-secret

# Gunicorn (Performance)
WEB_CONCURRENCY=2
GUNICORN_THREADS=2

# Sesión
SESSION_INACTIVITY_TIMEOUT=1800
LOGIN_MAX_FAILED_ATTEMPTS=5
LOGIN_LOCKOUT_SECONDS=900

# Seed (Datos iniciales)
RUN_SEED_ON_BUILD=False
RUN_CREATESU_ON_BUILD=False
SEED_UPLOAD_REMOTE_IMAGES=False

# Localización
LANGUAGE_CODE=es-co
TIME_ZONE=America/Bogota
```

### Anexo B: Comandos Management Útiles

```bash
# Ver todos los comandos disponibles
python manage.py help

# Crear backup de datos
python manage.py dumpdata > backup.json

# Restaurar desde backup
python manage.py loaddata backup.json

# Limpiar cache
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()

# Ver estado de migraciones
python manage.py showmigrations

# Crear nueva migración tras cambio en models.py
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear datos iniciales
python manage.py seed

# Crear superusuario
python manage.py createsuperuser

# Ejecutar tests
python manage.py test inventario

# Generar reporte de cobertura
coverage run --source='.' manage.py test
coverage report
```

### Anexo C: Estructura de Directorios

```
servicio-tecnico-web/
├── build.sh                    # Script de build para Render
├── manage.py                   # CLI de Django
├── requirements.txt            # Dependencias Python
├── README.md                   # Documentación principal
├── MANUAL_TECNICO.md          # Este archivo
├── db.sqlite3                  # BD SQLite (desarrollo)
├── .env                        # Variables de entorno (NO subir a Git)
├── .gitignore                  # Archivos ignorados en Git
│
├── servicio_tecnico/           # Proyecto Django (configuración)
│   ├── settings.py             # Configuración principal
│   ├── urls.py                 # Rutas principales
│   ├── wsgi.py                 # WSGI para producción
│   └── asgi.py                 # ASGI para async
│
├── inventario/                 # App principal
│   ├── models.py               # Modelos de BD
│   ├── views.py                # Vistas (lógica)
│   ├── urls.py                 # Rutas de app
│   ├── forms.py                # Formularios
│   ├── middleware.py           # Middleware custom
│   ├── context_processors.py   # Contexto para templates
│   ├── admin.py                # Configuración admin
│   │
│   ├── migrations/             # Cambios de BD
│   │   ├── 0001_initial.py
│   │   ├── ...
│   │   └── 0009_apartado_query_indexes.py
│   │
│   ├── templates/              # HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── landing.html
│   │   ├── login.html
│   │   ├── productos.html
│   │   ├── mis_apartados.html
│   │   ├── mi_perfil.html
│   │   └── ...
│   │
│   ├── static/                 # CSS, JS, imágenes
│   │   └── inventario/
│   │       ├── css/
│   │       │   └── styles.css
│   │       └── images/
│   │
│   ├── tests.py                # Pruebas unitarias
│   ├── test_landing.py         # Pruebas específicas
│   ├── management/             # Comandos custom
│   │   └── commands/
│   │       ├── seed.py         # Cargar datos
│   │       └── createsu.py     # Crear superusuario
│
├── media/                      # Archivos subidos (local)
│   └── productos/
│
├── staticfiles/                # Archivos compilados (producción)
│
└── render.yaml                 # Configuración Render
```

---

**Documento preparado por**: CAMILO ANDRES PARRA CUENCA
**Versión**: 1.0  
**Fecha última actualización**: Mayo 2026  
**Estado**: Aprobado para uso administrativo

---

*Confidencial - Uso Interno Only*
