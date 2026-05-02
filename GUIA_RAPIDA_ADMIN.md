# GUÍA RÁPIDA DE ADMINISTRACIÓN
## Servicio Técnico y Tecnología S.A.

**Versión**: 1.0 | **Fecha**: Mayo 2026

---

## 🚀 STARTUP RÁPIDO (5 minutos)

### Desarrollo Local

```bash
git clone https://github.com/camilouan/servicio-tecnico-web.git
cd servicio-tecnico-web
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed
python manage.py runserver
```

**→ Ir a**: `http://localhost:8000`

### Producción (Render)

```bash
git push origin main
# Render redeploy automático
# Monitorear en: Render Dashboard → Logs
```

---

## 🔑 CREDENCIALES DE ACCESO

| Sistema | URL | Usuario | Contraseña |
|---------|-----|---------|-----------|
| **Landing** | `https://servicio-tecnico.onrender.com/` | N/A | N/A |
| **Login Cliente** | `https://tudominio.com/login/` | Tu usuario | Tu contraseña |
| **Admin Panel** | `https://tudominio.com/admin/` | admin | (ver `.env`) |

---

## 👥 GESTIÓN DE USUARIOS - COMANDOS ESENCIALES

### Crear Superusuario

```bash
python manage.py createsuperuser
```

### Crear Datos de Prueba

```bash
python manage.py seed
```

### Ver Usuarios en BD

```bash
python manage.py shell
>>> from inventario.models import Usuario
>>> Usuario.objects.all()
>>> Usuario.objects.filter(rol='cliente').count()
```

### Resetear Contraseña de Usuario

```bash
python manage.py shell
>>> from inventario.models import Usuario
>>> u = Usuario.objects.get(username='usuario')
>>> u.set_password('nueva_contraseña')
>>> u.save()
```

### Bloquear/Desbloquear Usuario

```bash
python manage.py shell
>>> u = Usuario.objects.get(username='usuario')
>>> u.activo = False  # Bloquear
>>> u.save()
```

---

## 🗄️ BACKUP Y RECUPERACIÓN

### Backup de BD (Django)

```bash
python manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json
```

### Backup de BD (PostgreSQL)

```bash
pg_dump -h [HOST] -U [USER] -d [DB] > backup.sql
```

### Restaurar BD

```bash
# Desde JSON:
python manage.py loaddata backup_20260502_120000.json

# Desde SQL:
psql -h [HOST] -U [USER] -d [DB] < backup.sql
```

### Respaldar Media

```bash
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

---

## 🔍 DIAGNOSTICAR PROBLEMAS

### Health Check (¿Está vivo?)

```bash
curl https://tudominio.onrender.com/healthz/
# OK si responde: {"status": "ok"}
```

### Readiness Check (¿BD funciona?)

```bash
curl https://tudominio.onrender.com/readyz/
# OK si responde: {"status": "ready"}
```

### Ver Logs en Vivo

**Render Dashboard**:
1. Web Service → Logs
2. Buscar: `ERROR`, `timeout`, `WARN`

**Local**:
```bash
python manage.py runserver --verbosity 2
```

### Consultar BD Directamente

```bash
python manage.py dbshell
# Luego: SELECT COUNT(*) FROM inventario_producto;
```

---

## ⚙️ VARIABLES CRÍTICAS EN RENDER

```
DEBUG=False                           # SIEMPRE False en producción
SECRET_KEY=valor-generado-aleatorio
DATABASE_URL=postgresql://...        # Automática desde PostgreSQL
WEB_CONCURRENCY=2                    # Aumentar si muchos usuarios
GUNICORN_THREADS=2
DB_STATEMENT_TIMEOUT_MS=20000        # Si queries tardan
```

---

## 📊 OPERACIONES FRECUENTES

### Reiniciar Aplicación

```bash
# Render Dashboard → Web Service → Restart
# O: hacer push a GitHub (trigger redeploy)
```

### Ver Productos en BD

```bash
python manage.py shell
>>> from inventario.models import Producto
>>> Producto.objects.count()
>>> Producto.objects.filter(activo=True).values('nombre', 'precio')
```

### Forzar Expiración de Apartados Vencidos

```bash
python manage.py shell
>>> from inventario.models import Apartado
>>> Apartado.actualizar_apartados_vencidos()
>>> # Retorna cantidad actualizada
```

### Limpiar Cache

```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

---

## 🆘 PROBLEMAS COMUNES & SOLUCIONES

| Problema | Síntoma | Solución |
|----------|---------|----------|
| **Carga lenta** | >10s por página | Aumentar `WEB_CONCURRENCY=4` |
| **BD desconectada** | "OperationalError" | Verificar `DATABASE_URL` |
| **Módulo no encontrado** | `ModuleNotFoundError` | `pip install -r requirements.txt` |
| **Imágenes no cargan** | Error Cloudinary | Verificar credenciales env |
| **Usuario bloqueado** | "Bloqueado temporalmente" | Esperar 15 min o: `cache.clear()` |
| **Productos vacíos** | `/productos/` sin items | Correr: `python manage.py seed` |

---

## 📞 ESCALA DE CONTACTO

1. **Problema local**: Revisar logs + health checks
2. **Problema en Render**: Contactar support@render.com
3. **Problema BD**: Render dashboard PostgreSQL → Backups
4. **Problema Cloudinary**: support@cloudinary.com

---

## 📋 CHECKLIST PRE-PRESENTACIÓN

- [ ] Health check responde: `curl /healthz/` → 200
- [ ] Readiness check responde: `curl /readyz/` → 200
- [ ] BD PostgreSQL conectada
- [ ] Cloudinary (imágenes) funcionando
- [ ] Backup reciente disponible
- [ ] Documentación subida a repo
- [ ] Variables de entorno OK (DEBUG=False)
- [ ] No hay errores recientes en logs
- [ ] Admin panel accesible
- [ ] Página de inicio carga < 3 segundos

---

## 🔗 RUTAS IMPORTANTES

| Ruta | Propósito |
|------|-----------|
| `/` | Landing page |
| `/productos/` | Catálogo público |
| `/login/` | Iniciar sesión |
| `/registro/` | Registrarse |
| `/admin/` | Panel administrativo |
| `/healthz/` | Health check (respuesta rápida) |
| `/readyz/` | Readiness check (con BD) |
| `/mis-apartados/` | Historial de reservas (requiere login) |
| `/mi-perfil/` | Perfil de usuario (requiere login) |

---

## 📁 ARCHIVOS CLAVE

| Archivo | Propósito |
|---------|-----------|
| `.env` | Variables secretas (NO SUBIR) |
| `requirements.txt` | Dependencias Python |
| `manage.py` | CLI Django |
| `render.yaml` | Config Render |
| `build.sh` | Script de construcción |
| `MANUAL_TECNICO.md` | Documentación completa |
| `README.md` | Documentación general |

---

**Para más detalles, revisar**: `MANUAL_TECNICO.md`

*Confidencial - Uso Administrativo*
