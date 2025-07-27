# 📸 Capturas de Pantalla - PopcornHour

Esta carpeta contiene las 5 capturas de pantalla requeridas para el Checkpoint 3.

## 📋 Capturas Requeridas

### 1. 01-home-sin-sesion.png
- **Descripción:** Página principal sin iniciar sesión
- **URL:** http://localhost:5000
- **Elementos a mostrar:**
  - Header con logo y navegación
  - Botones "Iniciar Sesión" y "Registrarse"
  - Lista de películas/series
  - Footer

### 2. 02-home-con-sesion-usuario.png
- **Descripción:** Página principal con usuario estándar logueado
- **Usuario:** testuser / 123456
- **Elementos a mostrar:**
  - Header con nombre de usuario
  - Botón "Cerrar Sesión"
  - Panel de usuario (sin funciones de moderador)
  - Lista de películas/series

### 3. 03-home-con-sesion-moderador.png
- **Descripción:** Página principal con moderador logueado
- **Usuario:** superadmin / 123456
- **Elementos a mostrar:**
  - Header con nombre de moderador
  - Panel de moderador visible
  - Opciones de administración
  - Funciones de gestión de contenido

### 4. 04-formulario-login.png
- **Descripción:** Formulario de inicio de sesión
- **URL:** http://localhost:5000/login
- **Elementos a mostrar:**
  - Formulario completo
  - Campos: Usuario/Email y Contraseña
  - Botón "Iniciar Sesión"
  - Enlace a registro

### 5. 05-formulario-registro.png
- **Descripción:** Formulario de registro
- **URL:** http://localhost:5000/register
- **Elementos a mostrar:**
  - Formulario completo
  - Campos: Usuario, Email y Contraseña
  - Botón "Registrarse"
  - Enlace a login

## 📱 Herramientas Recomendadas
- **Windows:** Snipping Tool, PrintScreen, Windows + Shift + S
- **macOS:** Screenshot, Cmd + Shift + 4
- **Linux:** Flameshot, Spectacle, gnome-screenshot

## 🎯 Consejos para las Capturas

### Antes de Capturar
1. **Asegúrate de que el servidor esté corriendo**
   ```bash
   python app.py  # Frontend en puerto 5000
   node server.js # Backend en puerto 3001
   ```

2. **Limpia el navegador**
   - Cierra sesiones anteriores
   - Limpia caché si es necesario

3. **Prepara la ventana**
   - Maximiza el navegador
   - Ajusta el zoom al 100%
   - Oculta barras de herramientas innecesarias

### Durante la Captura
1. **Captura toda la página** (no solo la parte visible)
2. **Incluye elementos interactivos** (botones, formularios)
3. **Asegúrate de que el texto sea legible**
4. **Evita información personal** en las capturas

### Después de Capturar
1. **Revisa que se vean todos los elementos** importantes
2. **Renombra** según la convención establecida
3. **Guarda** en la carpeta correcta

## ✅ Checklist de Capturas

- [ ] 01-home-sin-sesion.png - Página principal sin sesión
- [ ] 02-home-con-sesion-usuario.png - Usuario estándar logueado
- [ ] 03-home-con-sesion-moderador.png - Moderador logueado
- [ ] 04-formulario-login.png - Formulario de login
- [ ] 05-formulario-registro.png - Formulario de registro

## 🔧 Solución de Problemas

### Si las capturas no se ven bien:
1. **Verifica que el servidor esté corriendo**
2. **Comprueba que no haya errores** en la consola
3. **Asegúrate de usar los usuarios correctos**
4. **Revisa que la resolución sea adecuada**

### Si faltan elementos:
1. **Verifica que estés en la URL correcta**
2. **Comprueba que el usuario tenga los permisos adecuados**
3. **Asegúrate de que la sesión esté activa** 