# 📊 Diagramas - PopcornHour

Esta carpeta contiene los diagramas técnicos del proyecto PopcornHour.

## 📋 Contenido

### 1. ERD_Database.pdf
- **Diagrama Entidad-Relación** de la base de datos
- Muestra todas las tablas y sus relaciones
- Incluye tipos de datos y constraints
- Documenta el esquema completo de PostgreSQL

### 2. User_Flows.pdf
- **Diagramas de flujo** de casos de uso
- Flujos de autenticación (login/registro)
- Flujos de interacción (reseñas, foro)
- Flujos de moderación
- Estados del sistema

## 🛠️ Cómo Generar los PDFs

### Opción 1: Desde Markdown
```bash
# Instalar pandoc
sudo apt install pandoc  # Ubuntu/Debian
brew install pandoc      # macOS

# Convertir ERD
pandoc ../../documentation/database_erd.md -o ERD_Database.pdf

# Convertir User Flows
pandoc ../../documentation/user_flows.md -o User_Flows.pdf
```

### Opción 2: Desde Navegador
1. Abrir los archivos .md en el navegador
2. Usar Ctrl+P para imprimir
3. Guardar como PDF

### Opción 3: Herramientas Online
- **Markdown to PDF:** https://md-to-pdf.fly.dev/
- **Pandoc Online:** https://pandoc.org/try/

## 📊 Detalles de los Diagramas

### ERD (Entity Relationship Diagram)
- **6 entidades principales:** users, movies, series, reviews, forum_discussions, forum_replies
- **Relaciones 1:N** entre entidades
- **Sistema polimórfico** para reseñas
- **Constraints y validaciones** documentadas

### User Flows
- **7 flujos principales** de usuario
- **Flujo de autenticación** completo
- **Estados del sistema** definidos
- **Ciclos de vida** documentados

## ✅ Checklist

- [ ] ERD_Database.pdf generado
- [ ] User_Flows.pdf generado
- [ ] Diagramas son legibles y claros
- [ ] Incluyen toda la información necesaria
- [ ] Formato PDF correcto 