-- Script final para limpiar y recrear usuarios con hashes válidos
-- Ejecutar: psql -U popcornhour_user -d popcornhour_db -f final_reset.sql

-- Limpiar TODAS las tablas
TRUNCATE TABLE forum_replies, forum_discussions, reviews, series, movies, users RESTART IDENTITY CASCADE;

-- Crear usuarios con hashes válidos pre-generados
-- admin / admin123
-- moderator / mod123
INSERT INTO users (username, email, password_hash, user_type) VALUES
('admin', 'admin@popcornhour.com', '$2b$10$rQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2.', 'moderator'),
('moderator', 'moderator@popcornhour.com', '$2b$10$sPw4d2zrCXWIyld1MIBkDPz7UuyNRrl9/MeweCQj5K5gKoIHjL3f.', 'moderator');

-- Insertar contenido de ejemplo
INSERT INTO movies (title, description, release_year, duration_minutes, genre, imdb_rating, created_by) VALUES
('Dune: Parte Dos', 'Paul Atreides se une a Chani y los Fremen.', 2024, 166, 'Sci-Fi', 4.8, 1),
('Oppenheimer', 'La historia de J. Robert Oppenheimer.', 2023, 181, 'Drama', 4.4, 1);

INSERT INTO series (title, description, release_year, seasons, genre, imdb_rating, created_by) VALUES
('House of the Dragon', 'Precuela de Game of Thrones.', 2022, 2, 'Drama', 4.4, 1),
('The Bear', 'Un chef regresa a Chicago.', 2022, 3, 'Comedia', 4.7, 1);

-- Verificar
SELECT username, email, user_type FROM users; 