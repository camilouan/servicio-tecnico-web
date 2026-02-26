# 🖥️ Servicio Técnico y Tecnología S.A.

Aplicación web desarrollada con Django para la gestión de productos tecnológicos y sistema de reservas con control de stock.

---

## 📌 Descripción del Proyecto

Servicio Técnico y Tecnología S.A. es una plataforma web que permite:

- Gestionar productos tecnológicos
- Administrar categorías
- Controlar stock disponible
- Registrar usuarios
- Permitir reservas de productos
- Gestionar reservas desde el panel administrador

El sistema controla dinámicamente la disponibilidad de productos evitando sobreventa y permitiendo reservas múltiples con límite de unidades por usuario.

---

## 🎯 Objetivo General

Desarrollar una aplicación web que permita gestionar inventario y reservas de productos tecnológicos, garantizando control de stock y administración eficiente mediante autenticación de usuarios.

---

## 🛠️ Tecnologías Utilizadas

- Python 3.10
- Django 5
- SQLite (Base de datos)
- Bootstrap 5 (Frontend)
- HTML5
- Git & GitHub

---

---

## 🧩 Modelo de Datos

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

## 🔐 Funcionalidades Implementadas

### 👤 Usuarios
- Registro de usuarios
- Inicio y cierre de sesión
- Roles (administrador / cliente)

### 📦 Productos
- Creación y edición desde panel administrador
- Control de stock total y stock disponible
- Visualización en catálogo público

### 🛒 Reservas
- Límite máximo de 5 unidades por reserva
- Descuento automático del stock
- Fecha de expiración automática
- Gestión desde el panel administrador

---

## 🚀 Instalación y Ejecución

1. Clonar repositorio:
git clone https://github.com/camilouan/servicio-tecnico-web.git

2. Entrar al proyecto:
cd servicio-tecnico-web


3. Crear entorno virtual:


python -m venv venv


4. Activar entorno:

Windows:

venv\Scripts\activate


5. Instalar dependencias:


pip install django


6. Ejecutar migraciones:


python manage.py makemigrations
python manage.py migrate


7. Ejecutar servidor:


python manage.py runserver


8. Acceder en navegador:


http://127.0.0.1:8000/


---

## 🧪 Datos de Prueba

Los productos pueden cargarse desde el panel administrador o mediante el shell de Django usando el ORM.

---

## 📊 Estado del Proyecto

✔ Sistema funcional  
✔ Base de datos estructurada  
✔ Control de stock dinámico  
✔ Sistema de reservas operativo  
✔ Diseño responsive con Bootstrap  

---

## 👨‍💻 Autor

Camilo Andrés Parra Cuenca  
Tecnólogo en Construcción de Software  
Universidad Antonio Nariño  

---

## 📄 Licencia

Proyecto académico – Uso educativo.
