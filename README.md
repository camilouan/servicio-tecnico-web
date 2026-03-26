#  Servicio Técnico y Tecnología S.A.

Aplicación web desarrollada con Django para la gestión de productos tecnológicos y sistema de reservas con control de stock.

---

##  Descripción del Proyecto

Servicio Técnico y Tecnología S.A. es una plataforma web que permite:

- Gestionar productos tecnológicos
- Administrar categorías
- Controlar stock disponible
- Registrar usuarios
- Permitir reservas de productos
- Gestionar reservas desde el panel administrador

El sistema controla dinámicamente la disponibilidad de productos evitando sobreventa y permitiendo reservas múltiples con límite de unidades por usuario.

---

## Objetivo General

Desarrollar una aplicación web que permita gestionar inventario y reservas de productos tecnológicos, garantizando control de stock y administración eficiente mediante autenticación de usuarios.

---

##  Tecnologías Utilizadas

- Python 3.10
- Django 5
- SQLite (Base de datos)
- Bootstrap 5 (Frontend)
- HTML5
- Git & GitHub

---

---

##  Modelo de Datos

El sistema está compuesto por las siguientes entidades principales:

- Usuario
- Categoría
- Producto
- Apartado (Reserva)

### Relaciones principales

- Un Usuario puede realizar múltiples Apartados.
- Un Producto puede tener múltiples Apartados.
- Una Categoría puede tener múltiples Productos.

La disponibilidad del producto se calcula dinámicamente según el stock disponible.

---

##  Funcionalidades Implementadas

###  Usuarios
- Registro de usuarios
- Inicio y cierre de sesión
- Roles (administrador / cliente)

###  Productos
- Creación y edición desde panel administrador
- Control de stock total y stock disponible
- Visualización en catálogo público

###  Reservas
- Límite máximo de 5 unidades por reserva
- Descuento automático del stock
- Fecha de expiración automática
- Gestión desde el panel administrador

---

##  Instalación y Ejecución

1. Clonar repositorio:
   ```bash
   git clone https://github.com/camilouan/servicio-tecnico-web.git
   ```

2. Entrar al proyecto:
   ```bash
   cd servicio-tecnico-web
   ```

3. Crear entorno virtual:
   ```bash
   python -m venv venv
   ```

4. Activar entorno:
   ```bash
   # Windows
   venv\Scripts\activate
   ```

5. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

6. Ejecutar migraciones:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. Definir variable de entorno `DEBUG` para desarrollo:
   ```bash
   # Windows
   set DEBUG=True
   ```
   El valor por defecto es `False` (seguridad en producción), por lo que
   al omitirlo no se servirán los archivos de media desde Django.

8. Ejecutar servidor:
   ```bash
   python manage.py runserver
   ```

9. Acceder en navegador:
   ```
   http://127.0.0.1:8000/
   ```

###  Despliegue en Render

Este repositorio está preparado para funcionar en [Render](https://render.com).
Algunas notas importantes:

- Configure la variable de entorno `DEBUG` a `False`.
- El proyecto ahora soporta **Cloudinary** para almacenar los archivos de
  medios. Dé la URL completa en la variable `CLOUDINARY_URL` o bien configure
  las tres variables `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY` y
  `CLOUDINARY_API_SECRET`.
  Render permite agregar estas variables en el panel de "Environment Variables".
  Cuando se detecta esta configuración, Django usa `django-cloudinary-storage`
  como `DEFAULT_FILE_STORAGE` y las imágenes subidas desde el admin se
  guardarán en la nube.
- Si no usa Cloudinary, Render no sirve archivos de media por defecto, por
  lo que debe proporcionar un volumen persistente o un bucket y dejar el
  middleware de WhiteNoise para servir `/media/` (la aplicación crea las
  carpetas automáticamente al arrancar).
- Asegúrese de que el directorio `media/` se mantenga entre despliegues si
  aún depende de él.
- No olvide definir otras variables (`SECRET_KEY`, `ALLOWED_HOSTS`, etc.)
  mediante el panel de configuraciones.



---

##  Datos de Prueba

Los productos pueden cargarse desde el panel administrador o mediante el shell de Django usando el ORM.

---

##  Estado del Proyecto

 Sistema funcional  
 Base de datos estructurada  
 Control de stock dinámico  
 Sistema de reservas operativo  
  Diseño responsive con Bootstrap  

---

##  Autor

Camilo Andrés Parra Cuenca  
Tecnólogo en Construcción de Software  
Universidad Antonio Nariño  

---

##  Licencia

Proyecto académico – Uso educativo.
