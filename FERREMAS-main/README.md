# FERREMAS - E-Commerce para Ferretería

Un proyecto universitario de e-commerce para una ferretería desarrollado con Flask, implementando las mejores prácticas de desarrollo web y seguridad.

## 🚀 Características Principales

### Gestión de Usuarios
- Registro de usuarios con validación de datos
- Inicio de sesión seguro con hash de contraseñas
- Gestión de sesiones con Flask-Session
- Protección de rutas para usuarios autenticados

### Catálogo y Productos
- Catálogo completo de productos con imágenes
- Categorización de productos
- Productos destacados y en promoción
- Búsqueda y filtrado por categorías
- Detalles completos de productos con imágenes y descripciones

### Carrito de Compras
- Gestión completa del carrito de compras
- Actualización en tiempo real de cantidades
- Cálculo automático de subtotales y totales
- Persistencia del carrito en la base de datos
- Validación de stock disponible

### Sistema de Pagos
- Integración con Webpay Plus
- Proceso de pago seguro
- Generación de comprobantes de pago
- Envío de comprobantes por correo electrónico
- Gestión de transacciones y estados de pago

### Características Adicionales
- Conversor de monedas integrado
- Sistema de contacto con envío de correos
- Interfaz responsiva y moderna
- Documentación API con Swagger
- Sistema de logging para debugging

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.x, Flask
- **Base de Datos**: PostgreSQL con SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **Autenticación**: Flask-Login, JWT, OAuth2
- **Email**: Flask-Mail
- **Documentación**: Flasgger (Swagger)
- **Pagos**: Webpay Plus
- **Migraciones**: Flask-Migrate (Alembic)

## 📁 Estructura del Proyecto

```
flask-app/
├── app.py              # Aplicación principal
├── auth.py             # Módulo de autenticación
├── models.py           # Modelos de base de datos
├── extensions.py       # Extensiones de Flask
├── webpay_plus.py      # Integración con Webpay
├── currency_converter.py # Conversor de monedas
├── migrations/         # Migraciones de base de datos
├── static/            # Archivos estáticos
│   ├── css/          # Estilos
│   ├── js/           # Scripts
│   └── images/       # Imágenes
├── templates/         # Plantillas HTML
│   ├── email/        # Plantillas de correo
│   └── ...
└── instance/         # Configuración local
```

## ⚙️ Configuración del Entorno

1. **Requisitos Previos**
   - Python 3.x
   - PostgreSQL
   - Git

2. **Clonar el Repositorio**
   ```bash
   git clone https://github.com/maricons/ferremas.git
   cd ferremas/flask-app
   ```

3. **Configurar Entorno Virtual**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Instalar Dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar Variables de Entorno**
   Crear archivo `.env` con:
   ```
   SECRET_KEY=tu_clave_google
   GOOGLE_CLIENT_ID=tu_clave_google
   GOOGLE_CLIENT_SECRET=tu_clave_google
   DB_USER=tu_usuario_db
   DB_PASSWORD=tu_password_db
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=ferremas
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=tu_email
   MAIL_PASSWORD=tu_password_email
   MAIL_DEFAULT_SENDER=tu_email
   BASE_URL=http://localhost:5000
   WEBPAY_COMMERCE_CODE=cod_webpay
   WEBPAY_API_KEY=api_webpay
   WEBPAY_INTEGRATION_TYPE=TEST
   BDE_EMAIL=cuenta_banco_central
   BDE_PASSWORD=cuenta_banco_central
   ```

6. **Inicializar Base de Datos**
   ```bash
   flask db upgrade
   python init_db.py
   python init_categories.py
   python init_products.py
   ```

## 🚀 Ejecución del Proyecto

1. **Iniciar la Aplicación**
   ```bash
   python app.py
   ```

2. **Acceder a la Aplicación**
   - URL: `http://localhost:5000`
   - Documentación API: `http://localhost:5000/apidocs`

## 📝 Documentación de la API

La API está documentada con Swagger y puede accederse en `/apidocs`. Incluye:

- Gestión de productos
- Gestión del carrito
- Autenticación de usuarios
- Conversión de monedas
- Sistema de contacto

## 🔒 Seguridad Implementada

- Hash seguro de contraseñas con PBKDF2
- Protección CSRF en formularios
- Validación de datos de entrada
- Sanitización de archivos subidos
- Manejo seguro de sesiones
- Protección de rutas sensibles

## 📧 Sistema de Correos

- Comprobantes de pago automáticos
- Notificaciones de contacto
- Plantillas HTML responsivas
- Configuración SMTP segura

## 💱 Conversor de Monedas

- Soporte para múltiples monedas
- Actualización en tiempo real
- API REST para conversiones
- Interfaz intuitiva

## 🛍️ Proceso de Compra

1. Selección de productos
2. Gestión del carrito
3. Inicio de sesión/registro
4. Integración con Webpay
5. Confirmación de pago
6. Generación de comprobante
7. Envío de correo de confirmación

## 🐛 Debugging y Logging

- Sistema de logging configurado
- Archivo de log en `app.log`
- Mensajes detallados de error
- Trazas de depuración

## 📊 Base de Datos

- Modelos relacionales
- Migraciones automáticas
- Índices optimizados
- Relaciones bien definidas

## 🎨 Frontend

- Diseño responsivo
- CSS moderno
- JavaScript interactivo
- Optimización de imágenes
- Experiencia de usuario mejorada

## 📱 Características Móviles

- Diseño adaptativo
- Menú hamburguesa
- Imágenes optimizadas
- Touch-friendly

## 📈 Optimizaciones

- Caché de consultas
- Compresión de assets
- Lazy loading de imágenes
- Minificación de CSS/JS

## 🔍 Monitoreo

- Logging de errores
- Tracking de transacciones
- Monitoreo de rendimiento
- Alertas de sistema

## 📚 Recursos Adicionales

- [Documentación de Flask](https://flask.palletsprojects.com/)
- [Documentación de SQLAlchemy](https://docs.sqlalchemy.org/)
- [Documentación de Webpay](https://www.transbankdevelopers.cl/)
- [Guía de Estilo Python](https://www.python.org/dev/peps/pep-0008/)

## 👥 Contribución

1. Fork el proyecto
2. Crear rama feature
3. Commit cambios
4. Push a la rama
5. Crear Pull Request

## 📄 Licencia

Este proyecto es para fines educativos y de evaluación.

## 👨‍🏫 Notas

Este proyecto demuestra la implementación de un e-commerce completo con las siguientes consideraciones técnicas:

1. **Arquitectura**
   - Patrón MVC
   - Separación de responsabilidades
   - Código modular y reutilizable

2. **Seguridad**
   - Implementación de mejores prácticas
   - Manejo seguro de datos sensibles
   - Protección contra vulnerabilidades comunes

3. **Base de Datos**
   - Diseño relacional optimizado
   - Migraciones automatizadas
   - Consultas eficientes

4. **Frontend**
   - Diseño responsivo
   - Experiencia de usuario intuitiva
   - Optimización de rendimiento

5. **Integración de Pagos**
   - Implementación segura de Webpay
   - Manejo de transacciones
   - Generación de comprobantes

6. **Características Adicionales**
   - Conversor de monedas
   - Sistema de correos
   - Logging y debugging

El código está documentado y sigue las mejores prácticas de desarrollo en Python y Flask. 