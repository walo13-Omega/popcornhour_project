# 🗄️ Esquema de Base de Datos - PopcornHour

## 📊 Diagrama Entidad-Relación (ERD)

### Entidades Principales

#### 👥 USERS (Usuarios)
```
users {
  id: SERIAL PRIMARY KEY
  username: VARCHAR(50) UNIQUE NOT NULL
  email: VARCHAR(100) UNIQUE NOT NULL
  password_hash: VARCHAR(255) NOT NULL
  user_type: VARCHAR(20) DEFAULT 'standard'
  created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  last_login: TIMESTAMP
}
```

#### 🎬 MOVIES (Películas)
```
movies {
  id: SERIAL PRIMARY KEY
  title: VARCHAR(200) NOT NULL
  description: TEXT
  release_year: INTEGER
  duration_minutes: INTEGER
  genre: VARCHAR(100)
  director: VARCHAR(100)
  imdb_rating: DECIMAL(3,1)
  poster_url: VARCHAR(500)
  created_by: INTEGER REFERENCES users(id)
  created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
}
```

#### 📺 SERIES (Series)
```
series {
  id: SERIAL PRIMARY KEY
  title: VARCHAR(200) NOT NULL
  description: TEXT
  release_year: INTEGER
  seasons: INTEGER
  genre: VARCHAR(100)
  imdb_rating: DECIMAL(3,1)
  poster_url: VARCHAR(500)
  created_by: INTEGER REFERENCES users(id)
  created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
}
```

#### ⭐ REVIEWS (Reseñas)
```
reviews {
  id: SERIAL PRIMARY KEY
  user_id: INTEGER REFERENCES users(id)
  content_type: VARCHAR(20) NOT NULL -- 'movie', 'series', 'tmdb_movie', 'tmdb_series'
  content_id: INTEGER NOT NULL
  content: TEXT NOT NULL
  rating: DECIMAL(3,1) CHECK (rating >= 0 AND rating <= 5)
  created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
}
```

#### 💬 FORUM_DISCUSSIONS (Discusiones del Foro)
```
forum_discussions {
  id: SERIAL PRIMARY KEY
  title: VARCHAR(200) NOT NULL
  content: TEXT NOT NULL
  user_id: INTEGER REFERENCES users(id)
  category: VARCHAR(50) -- 'movies', 'series', 'general'
  created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
}
```

#### 💭 FORUM_REPLIES (Respuestas del Foro)
```
forum_replies {
  id: SERIAL PRIMARY KEY
  discussion_id: INTEGER REFERENCES forum_discussions(id)
  user_id: INTEGER REFERENCES users(id)
  content: TEXT NOT NULL
  created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
}
```

## 🔗 Relaciones

### Relaciones 1:N (Uno a Muchos)

1. **USERS → MOVIES**
   - Un usuario puede crear muchas películas
   - `movies.created_by` → `users.id`

2. **USERS → SERIES**
   - Un usuario puede crear muchas series
   - `series.created_by` → `users.id`

3. **USERS → REVIEWS**
   - Un usuario puede hacer muchas reseñas
   - `reviews.user_id` → `users.id`

4. **USERS → FORUM_DISCUSSIONS**
   - Un usuario puede crear muchas discusiones
   - `forum_discussions.user_id` → `users.id`

5. **USERS → FORUM_REPLIES**
   - Un usuario puede hacer muchas respuestas
   - `forum_replies.user_id` → `users.id`

6. **FORUM_DISCUSSIONS → FORUM_REPLIES**
   - Una discusión puede tener muchas respuestas
   - `forum_replies.discussion_id` → `forum_discussions.id`

### Relaciones Polimórficas

7. **REVIEWS → CONTENT**
   - Las reseñas pueden referenciar películas, series o contenido TMDb
   - `reviews.content_type` + `reviews.content_id` → contenido específico

## 📋 Tipos de Usuario

### User Types
- `standard`: Usuario normal (puede hacer reseñas, participar en foro)
- `moderator`: Moderador (puede gestionar contenido, moderar foro)

### Content Types (Reviews)
- `movie`: Reseña de película local
- `series`: Reseña de serie local
- `tmdb_movie`: Reseña de película de TMDb
- `tmdb_series`: Reseña de serie de TMDb

## 🔐 Restricciones y Validaciones

### Constraints
- `users.username`: UNIQUE
- `users.email`: UNIQUE
- `reviews.rating`: CHECK (0 <= rating <= 5)
- `movies.imdb_rating`: CHECK (0 <= rating <= 10)
- `series.imdb_rating`: CHECK (0 <= rating <= 10)

### Índices Recomendados
```sql
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_content ON reviews(content_type, content_id);
CREATE INDEX idx_forum_discussions_category ON forum_discussions(category);
CREATE INDEX idx_forum_replies_discussion ON forum_replies(discussion_id);
CREATE INDEX idx_movies_genre ON movies(genre);
CREATE INDEX idx_series_genre ON series(genre);
```

## 📊 Estadísticas de la Base de Datos

### Datos de Ejemplo Incluidos
- **10 películas** con información completa
- **15 series** con información completa
- **5 usuarios** (2 moderadores, 3 estándar)
- **Múltiples reseñas** de ejemplo
- **Discusiones del foro** de ejemplo

### Capacidades del Sistema
- **Escalabilidad**: Diseño normalizado para grandes volúmenes
- **Integridad**: Constraints y foreign keys
- **Rendimiento**: Índices optimizados
- **Flexibilidad**: Sistema polimórfico para reseñas

## 🛠️ Scripts de Mantenimiento

### Limpiar Base de Datos
```sql
TRUNCATE TABLE forum_replies, forum_discussions, reviews, series, movies, users RESTART IDENTITY CASCADE;
```

### Resetear Usuarios
```sql
UPDATE users SET password_hash = '$2b$12$LrSzZt.ywKxag0aulFA1yuOxunDGQYvLxzbEpKGNoS9dcjdL8u56C';
```

### Estadísticas
```sql
SELECT 
  (SELECT COUNT(*) FROM users) as total_users,
  (SELECT COUNT(*) FROM movies) as total_movies,
  (SELECT COUNT(*) FROM series) as total_series,
  (SELECT COUNT(*) FROM reviews) as total_reviews,
  (SELECT COUNT(*) FROM forum_discussions) as total_discussions;
``` 