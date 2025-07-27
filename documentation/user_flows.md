# 🔄 Diagramas de Flujo - PopcornHour

## 📋 Casos de Uso Principales

### 1. 🔐 Registro de Usuario

```mermaid
flowchart TD
    A[Usuario accede a /register] --> B[Llena formulario]
    B --> C{Validar datos}
    C -->|Datos inválidos| D[Mostrar errores]
    D --> B
    C -->|Datos válidos| E[Enviar a API /auth/register]
    E --> F{Usuario existe?}
    F -->|Sí| G[Error: Usuario ya existe]
    G --> B
    F -->|No| H[Crear usuario en BD]
    H --> I[Generar JWT token]
    I --> J[Guardar en sesión]
    J --> K[Redirigir a /home]
    K --> L[Mostrar panel de moderador si aplica]
```

### 2. 🔑 Inicio de Sesión

```mermaid
flowchart TD
    A[Usuario accede a /login] --> B[Ingresa credenciales]
    B --> C[Enviar a API /auth/login]
    C --> D{Validar credenciales}
    D -->|Inválidas| E[Error: Credenciales incorrectas]
    E --> B
    D -->|Válidas| F[Generar JWT token]
    F --> G[Guardar usuario en sesión]
    G --> H[Redirigir a /home]
    H --> I{¿Es moderador?}
    I -->|Sí| J[Mostrar panel de moderador]
    I -->|No| K[Mostrar interfaz estándar]
```

### 3. ⭐ Calificar Película

```mermaid
flowchart TD
    A[Usuario navega a película] --> B[Ver detalles de película]
    B --> C{¿Está logueado?}
    C -->|No| D[Redirigir a /login]
    C -->|Sí| E[Ver formulario de reseña]
    E --> F[Escribir reseña y calificación]
    F --> G[Enviar a API /reviews]
    G --> H{Validar datos}
    H -->|Inválidos| I[Mostrar errores]
    I --> F
    H -->|Válidos| J[Guardar reseña en BD]
    J --> K[Actualizar página]
    K --> L[Mostrar reseña agregada]
```

### 4. 💬 Participar en Foro

```mermaid
flowchart TD
    A[Usuario accede a /foro] --> B[Ver lista de discusiones]
    B --> C[Seleccionar discusión]
    C --> D[Ver discusión y respuestas]
    D --> E{¿Quiere responder?}
    E -->|No| F[Leer más respuestas]
    E -->|Sí| G{¿Está logueado?}
    G -->|No| H[Redirigir a /login]
    G -->|Sí| I[Escribir respuesta]
    I --> J[Enviar a API /forum/replies]
    J --> K[Guardar respuesta]
    K --> L[Actualizar página]
    L --> M[Mostrar respuesta agregada]
```

### 5. 👑 Funciones de Moderador

```mermaid
flowchart TD
    A[Moderador inicia sesión] --> B[Ver panel de moderador]
    B --> C[Seleccionar función]
    C --> D{¿Qué función?}
    D -->|Agregar Película| E[Formulario nueva película]
    D -->|Agregar Serie| F[Formulario nueva serie]
    D -->|Moderar Contenido| G[Panel de administración]
    D -->|Eliminar Contenido| H[Seleccionar contenido]
    
    E --> I[Llenar datos película]
    I --> J[Enviar a API /movies]
    J --> K[Guardar en BD]
    
    F --> L[Llenar datos serie]
    L --> M[Enviar a API /series]
    M --> N[Guardar en BD]
    
    G --> O[Ver lista de contenido]
    O --> P[Seleccionar para editar/eliminar]
    
    H --> Q[Confirmar eliminación]
    Q --> R[Eliminar de BD]
    
    K --> S[Redirigir a /admin_content]
    N --> S
    P --> T[Editar contenido]
    R --> S
    T --> S
```

### 6. 🔍 Búsqueda de Contenido

```mermaid
flowchart TD
    A[Usuario en página principal] --> B[Usar barra de búsqueda]
    B --> C[Enviar query a /search]
    C --> D[Buscar en películas]
    D --> E[Buscar en series]
    E --> F[Combinar resultados]
    F --> G[Filtrar por género/año]
    G --> H[Mostrar resultados]
    H --> I[Usuario selecciona resultado]
    I --> J[Navegar a detalles]
```

### 7. 📱 Navegación General

```mermaid
flowchart TD
    A[Usuario accede a /] --> B[Página principal]
    B --> C{¿Está logueado?}
    C -->|No| D[Mostrar botones login/registro]
    C -->|Sí| E[Mostrar perfil y logout]
    
    D --> F[Usuario puede navegar libremente]
    E --> G[Usuario tiene acceso completo]
    
    F --> H[Navegar a /movies]
    F --> I[Navegar a /series]
    F --> J[Navegar a /foro]
    
    G --> K[Acceso a funciones de usuario]
    G --> L{¿Es moderador?}
    L -->|Sí| M[Acceso a funciones de moderador]
    L -->|No| N[Acceso estándar]
```

## 🔐 Flujo de Autenticación

### Middleware de Autenticación

```mermaid
flowchart TD
    A[Usuario accede a ruta protegida] --> B[Verificar sesión]
    B --> C{¿Hay usuario en sesión?}
    C -->|No| D[Redirigir a /login]
    C -->|Sí| E{¿Ruta requiere moderador?}
    E -->|No| F[Permitir acceso]
    E -->|Sí| G{¿Es moderador?}
    G -->|No| H[Error: Acceso denegado]
    G -->|Sí| F
    H --> I[Redirigir a /home]
    F --> J[Ejecutar función]
```

## 📊 Estados del Sistema

### Estados de Usuario
- **No autenticado**: Solo navegación básica
- **Usuario estándar**: Reseñas, foro, perfil
- **Moderador**: Todas las funciones + gestión de contenido

### Estados de Contenido
- **Película/Serie**: Activa, editable, eliminable
- **Reseña**: Creada, editable por autor, eliminable por moderador
- **Discusión**: Activa, con respuestas, moderable

## 🔄 Ciclos de Vida

### Ciclo de Vida de Usuario
1. **Registro** → Crear cuenta
2. **Login** → Autenticación
3. **Navegación** → Uso de funciones
4. **Logout** → Cerrar sesión

### Ciclo de Vida de Contenido
1. **Creación** → Por moderador/usuario
2. **Visualización** → Por todos los usuarios
3. **Interacción** → Reseñas, comentarios
4. **Moderación** → Edición/eliminación
5. **Archivado** → Eliminación lógica 