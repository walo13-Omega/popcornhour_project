-- Esquema de Base de Datos para PopcornHour
-- Proyecto de portal web para recomendar, calificar y discutir películas y series

-- Tabla de usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_type VARCHAR(20) DEFAULT 'standard' CHECK (user_type IN ('standard', 'moderator')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de películas
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    release_year INTEGER,
    duration_minutes INTEGER,
    genre VARCHAR(100),
    poster_url VARCHAR(500),
    trailer_url VARCHAR(500),
    imdb_rating DECIMAL(3,1),
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de series
CREATE TABLE series (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    release_year INTEGER,
    seasons INTEGER,
    episodes INTEGER,
    genre VARCHAR(100),
    poster_url VARCHAR(500),
    trailer_url VARCHAR(500),
    imdb_rating DECIMAL(3,1),
    status VARCHAR(20) DEFAULT 'ongoing' CHECK (status IN ('ongoing', 'completed', 'cancelled')),
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de calificaciones de usuarios
CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    content_type VARCHAR(10) CHECK (content_type IN ('movie', 'series')),
    content_id INTEGER,
    rating DECIMAL(2,1) CHECK (rating >= 1.0 AND rating <= 5.0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, content_type, content_id)
);

-- Tabla de reseñas
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    content_type VARCHAR(10) CHECK (content_type IN ('movie', 'series')),
    content_id INTEGER,
    title VARCHAR(255),
    content TEXT NOT NULL,
    rating DECIMAL(2,1) CHECK (rating >= 1.0 AND rating <= 5.0),
    likes_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de comentarios en reseñas
CREATE TABLE review_comments (
    id SERIAL PRIMARY KEY,
    review_id INTEGER REFERENCES reviews(id),
    user_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de discusiones del foro
CREATE TABLE forum_discussions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'general',
    is_spoiler BOOLEAN DEFAULT FALSE,
    replies_count INTEGER DEFAULT 0,
    last_reply_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de respuestas a discusiones
CREATE TABLE forum_replies (
    id SERIAL PRIMARY KEY,
    discussion_id INTEGER REFERENCES forum_discussions(id),
    user_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de listas personales de usuarios
CREATE TABLE user_lists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    content_type VARCHAR(10) CHECK (content_type IN ('movie', 'series')),
    content_id INTEGER,
    list_type VARCHAR(20) DEFAULT 'watchlist' CHECK (list_type IN ('watchlist', 'favorites', 'watched')),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, content_type, content_id, list_type)
);

-- Tabla de likes en reseñas
CREATE TABLE review_likes (
    id SERIAL PRIMARY KEY,
    review_id INTEGER REFERENCES reviews(id),
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(review_id, user_id)
);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_movies_genre ON movies(genre);
CREATE INDEX idx_movies_release_year ON movies(release_year);
CREATE INDEX idx_series_genre ON series(genre);
CREATE INDEX idx_series_release_year ON series(release_year);
CREATE INDEX idx_ratings_content ON ratings(content_type, content_id);
CREATE INDEX idx_reviews_content ON reviews(content_type, content_id);
CREATE INDEX idx_forum_discussions_category ON forum_discussions(category);
CREATE INDEX idx_user_lists_user ON user_lists(user_id);

-- Triggers para actualizar timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_movies_updated_at BEFORE UPDATE ON movies FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_series_updated_at BEFORE UPDATE ON series FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_reviews_updated_at BEFORE UPDATE ON reviews FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_forum_discussions_updated_at BEFORE UPDATE ON forum_discussions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insertar datos de ejemplo
INSERT INTO users (username, email, password_hash, user_type) VALUES
('admin', 'admin@popcornhour.com', '$2b$10$example_hash_here', 'moderator'),
('johndoe', 'john@example.com', '$2b$10$example_hash_here', 'standard'),
('moviefan', 'fan@example.com', '$2b$10$example_hash_here', 'standard');

INSERT INTO movies (title, description, release_year, duration_minutes, genre, poster_url, imdb_rating, created_by) VALUES
('Dune: Parte Dos', 'Paul Atreides se une a los Fremen y comienza un viaje de venganza contra los conspiradores que destruyeron su familia.', 2024, 166, 'Ciencia Ficción', 'https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg', 8.3, 1),
('Oppenheimer', 'La historia de J. Robert Oppenheimer y su papel en el desarrollo de la bomba atómica.', 2023, 181, 'Drama', 'https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQHlyCZ3N6xx.jpg', 8.7, 1),
('The Batman', 'Batman se aventura en los bajos fondos de Gotham City en la búsqueda de un asesino en serie.', 2022, 176, 'Acción', 'https://image.tmdb.org/t/p/w500/5mzr6JZbrqnqD8rCEvPhuCE5Fw2.jpg', 9.1, 1);

INSERT INTO series (title, description, release_year, seasons, episodes, genre, poster_url, imdb_rating, status, created_by) VALUES
('Breaking Bad', 'Un profesor de química se convierte en fabricante de metanfetaminas.', 2008, 5, 62, 'Drama', 'https://image.tmdb.org/t/p/w500/example.jpg', 9.0, 'completed', 1),
('The Shawshank Redemption', 'Dos hombres encarcelados se unen durante varios años.', 1994, 1, 1, 'Drama', 'https://image.tmdb.org/t/p/w500/example2.jpg', 9.3, 'completed', 1);

