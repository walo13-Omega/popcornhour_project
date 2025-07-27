# 🎬 Videos de Autenticación - PopcornHour

Esta carpeta contiene los 3 videos requeridos para el Checkpoint 4.

## 📋 Videos Requeridos

### 1. 01-registro.mp4
- **Descripción:** Proceso de registro de nuevo usuario
- **Contenido:**
  - Ir a /register
  - Llenar formulario completo
  - Mostrar mensaje de éxito
  - Verificar redirección

### 2. 02-login.mp4
- **Descripción:** Proceso de inicio de sesión
- **Contenido:**
  - Ir a /login
  - Login con usuario existente
  - Mostrar acceso al perfil
  - Verificar sesión activa

### 3. 03-persistencia.mp4
- **Descripción:** Demostración de persistencia de sesión
- **Contenido:**
  - Estar logueado
  - Recargar página
  - Ir a /profile
  - Mostrar que la sesión persiste

## 🎯 Detalles de Cada Video

### Video 1: Registro (01-registro.mp4)

#### Secuencia:
1. **Abrir página de registro** (10 segundos)
   - Ir a http://localhost:5000/register
   - Mostrar formulario completo

2. **Llenar formulario** (30 segundos)
   - Usuario: `usuario_prueba`
   - Email: `prueba@ejemplo.com`
   - Contraseña: `123456`
   - Mostrar cada campo mientras se llena

3. **Enviar formulario** (20 segundos)
   - Hacer clic en "Registrarse"
   - Mostrar mensaje de éxito
   - Verificar redirección a home

### Video 2: Login (02-login.mp4)

#### Secuencia:
1. **Abrir página de login** (10 segundos)
   - Ir a http://localhost:5000/login
   - Mostrar formulario completo

2. **Llenar credenciales** (20 segundos)
   - Usuario: `testuser`
   - Contraseña: `123456`
   - Mostrar campos mientras se llenan

3. **Iniciar sesión** (30 segundos)
   - Hacer clic en "Iniciar Sesión"
   - Mostrar login exitoso
   - Navegar a /profile
   - Mostrar información del usuario

### Video 3: Persistencia (03-persistencia.mp4)

#### Secuencia:
1. **Estado inicial** (15 segundos)
   - Mostrar que el usuario está logueado
   - Mostrar nombre en el header

2. **Recargar página** (15 segundos)
   - Presionar F5 o recargar
   - Mostrar que la sesión persiste
   - Verificar que sigue logueado

3. **Navegar a perfil** (30 segundos)
   - Ir a /profile
   - Mostrar información del usuario
   - Verificar que la sesión está activa

## 🛠️ Configuración de Grabación

### Software Recomendado:
- **Windows:** OBS Studio, Windows Game Bar
- **macOS:** QuickTime Player, OBS Studio
- **Linux:** OBS Studio, SimpleScreenRecorder

## 🎬 Consejos Específicos

### Para el Video de Registro:
- Usa un usuario que no exista
- Muestra claramente el mensaje de éxito
- Verifica que el usuario se creó correctamente

### Para el Video de Login:
- Usa un usuario que ya exista
- Muestra el acceso al perfil
- Verifica que la sesión se inició correctamente

### Para el Video de Persistencia:
- Asegúrate de estar logueado antes de empezar
- Muestra claramente que la sesión persiste
- Verifica que puedes acceder a funciones protegidas

## ✅ Checklist de Videos

### Video 1 - Registro:
- [ ] Muestra formulario completo
- [ ] Incluye mensaje de éxito
- [ ] Verifica redirección

### Video 2 - Login:
- [ ] Muestra formulario completo
- [ ] Incluye login exitoso
- [ ] Muestra acceso a perfil

### Video 3 - Persistencia:
- [ ] Muestra recarga de página
- [ ] Verifica persistencia de sesión
- [ ] Muestra acceso a funciones

## 🔧 Solución de Problemas

### Si el registro falla:
- Verifica que el usuario no exista
- Comprueba que el servidor esté corriendo
- Revisa que no haya errores en la consola

### Si el login falla:
- Verifica que el usuario exista
- Comprueba las credenciales
- Asegúrate de que la base de datos esté funcionando

### Si la persistencia no funciona:
- Verifica que las cookies estén habilitadas
- Comprueba que el JWT se esté guardando
- Revisa la configuración de sesión 