# 🍿 PopcornHour - Tu Portal de Cine

## 📖 Descripción del Proyecto

PopcornHour es una plataforma web completa para explorar, calificar y discutir películas y series. Los usuarios pueden registrarse, hacer reseñas, participar en foros y los moderadores pueden gestionar el contenido de la plataforma.

### ✨ Características Principales

- **🎬 Catálogo de Películas y Series** con información detallada
- **⭐ Sistema de Reseñas** con calificaciones personalizadas
- **💬 Foro de Discusión** para compartir opiniones
- **👑 Panel de Moderadores** para gestión de contenido
- **🔍 Búsqueda Avanzada** por género, año y título
- **📱 Interfaz Responsiva** con diseño moderno
- **🔐 Sistema de Autenticación** seguro con JWT

### 🏗️ Arquitectura del Sistema

- **Frontend:** Flask (Python) con Jinja2 templates
- **Backend:** Node.js con Express.js
- **Base de Datos:** PostgreSQL
- **Autenticación:** JWT + bcrypt
- **APIs Externas:** TMDb para información de películas

## 📦 Paquetes Necesarios

### Frontend (Flask)
```
Flask==2.3.3
requests==2.31.0
psycopg2-binary==2.9.10
```

### Backend (Node.js)
```
express==5.1.0
bcryptjs==3.0.2
jsonwebtoken==9.0.2
pg==8.16.3
cors==2.8.5
dotenv==17.2.0
cookie-parser==1.4.7
```

### Base de Datos
```
PostgreSQL 12+
```

## 🚀 Instrucciones de Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/popcornhour.git
cd popcornhour
```

### 2. Configurar Base de Datos PostgreSQL
```bash
# Crear base de datos
createdb popcornhour_db

# Crear usuario
createuser popcornhour_user

# Configurar contraseña
psql -d popcornhour_db -c "ALTER USER popcornhour_user PASSWORD 'tu_nueva_password_segura';"

# Ejecutar esquema
psql -U popcornhour_user -d popcornhour_db -f database/database_schema.sql

# Poblar con datos de ejemplo
psql -U popcornhour_user -d popcornhour_db -f database/database_seed.sql
```

### 3. Configurar Backend (Node.js)
```bash
cd backend
npm install

# Crear archivo .env
echo "DB_USER=popcornhour_user
DB_HOST=localhost
DB_NAME=popcornhour_db
DB_PASSWORD=tu_nueva_password_segura
DB_PORT=5432
JWT_SECRET=tu_clave_jwt_super_secreta_aqui_2024
JWT_EXPIRES_IN=7d
PORT=3001" > .env

# Iniciar backend
node server.js
```

### 4. Configurar Frontend (Flask)
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar frontend
python app.py
```

### 5. Acceder a la Aplicación
- **Frontend:** http://localhost:5000
- **Backend API:** http://localhost:3001/api

## 👥 Usuarios de Prueba

### Moderadores
- `superadmin` / `123456`
- `moderator2` / `123456`

### Usuarios Estándar
- `testuser` / `123456`
- `testuser2` / `123456`

## 🔧 Scripts Útiles

### Crear Usuarios de Prueba
```bash
python create_moderators.py
python create_test_users.py
```

### Diagnosticar Sistema
```bash
python test_communication.py
python debug_session.py
```

## 📁 Estructura del Proyecto

```
popcornhour/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias Python
├── backend/
│   ├── server.js         # Servidor Node.js
│   ├── package.json      # Dependencias Node.js
│   └── .env             # Variables de entorno
├── database/
│   ├── database_schema.sql  # Esquema de BD
│   └── database_seed.sql    # Datos de ejemplo
├── templates/            # Plantillas HTML
├── documentation/        # Documentación del proyecto
└── scripts/             # Scripts de utilidad
```

## 🔐 Funcionalidades de Moderador

- ✅ Agregar películas y series
- ✅ Editar contenido existente
- ✅ Eliminar contenido
- ✅ Moderar foro
- ✅ Acceso al panel de administración

## 🌐 APIs Integradas

- **TMDb API:** Información de películas y series
- **Poster automático:** Imágenes de alta calidad
- **Metadatos:** Géneros, fechas, calificaciones

## 🛠️ Tecnologías Utilizadas

- **Frontend:** Flask, Jinja2, Bootstrap 5
- **Backend:** Node.js, Express.js
- **Base de Datos:** PostgreSQL
- **Autenticación:** JWT, bcrypt
- **APIs:** TMDb, requests
- **Estilos:** CSS3, Font Awesome

## 📝 Licencia

Este proyecto es de uso educativo y demostrativo.

## 📝 Licencia

Este proyecto es de uso educativo y demostrativo.

---

**🍿 ¡Disfruta explorando el mundo del cine con PopcornHour!** 