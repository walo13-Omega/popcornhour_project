-- Script para limpiar completamente la base de datos y crear usuarios nuevos
-- Ejecutar: psql -U popcornhour_user -d popcornhour_db -f clean_and_reset.sql

-- Limpiar TODAS las tablas en orden correcto para evitar restricciones de clave foránea
TRUNCATE TABLE forum_replies, forum_discussions, reviews, series, movies, users RESTART IDENTITY CASCADE;

-- Crear usuarios nuevos con hashes válidos generados con bcrypt
-- Usuario 1: admin / admin123
-- Usuario 2: moderator / mod123

INSERT INTO users (username, email, password_hash, user_type) VALUES
('admin', 'admin@popcornhour.com', '$2b$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'moderator'),
('moderator', 'moderator@popcornhour.com', '$2b$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'moderator');

-- Insertar películas de ejemplo
INSERT INTO movies (title, description, release_year, duration_minutes, genre, imdb_rating, created_by) VALUES
('Dune: Parte Dos', 'Paul Atreides se une a Chani y los Fremen mientras busca venganza.', 2024, 166, 'Sci-Fi', 4.8, 1),
('Oppenheimer', 'La historia de J. Robert Oppenheimer y la bomba atómica.', 2023, 181, 'Drama', 4.4, 1),
('The Batman', 'Batman investiga una serie de asesinatos en Gotham City.', 2022, 176, 'Acción', 4.2, 1),
('Spider-Man: No Way Home', 'Peter Parker debe enfrentar villanos de universos alternativos.', 2021, 148, 'Acción', 4.5, 1),
('Top Gun: Maverick', 'Maverick regresa como instructor de pilotos de élite.', 2022, 131, 'Acción', 4.3, 1);

-- Insertar series de ejemplo
INSERT INTO series (title, description, release_year, seasons, genre, imdb_rating, created_by) VALUES
('House of the Dragon', 'Precuela de Game of Thrones sobre la casa Targaryen.', 2022, 2, 'Drama', 4.4, 1),
('The Bear', 'Un chef de alta cocina regresa a Chicago para dirigir un restaurante.', 2022, 3, 'Comedia', 4.7, 1),
('Stranger Things', 'Niños enfrentan fuerzas sobrenaturales en los años 80.', 2016, 4, 'Sci-Fi', 4.7, 1);

-- Insertar reseñas de ejemplo
INSERT INTO reviews (user_id, content_type, content_id, content, rating) VALUES
(1, 'movie', 1, '¡Excelente película!', 4.5),
(2, 'movie', 2, 'Muy buena historia.', 4.0);

-- Insertar discusiones del foro de ejemplo
INSERT INTO forum_discussions (title, content, user_id, category) VALUES
('¿Qué opinan de Dune: Parte Dos?', 'Me encantó la película.', 1, 'movies'),
('Mejores series de 2024', '¿Cuál es tu favorita?', 2, 'series');

-- Insertar respuestas del foro de ejemplo
INSERT INTO forum_replies (discussion_id, user_id, content) VALUES
(1, 2, '¡Totalmente de acuerdo!'),
(2, 1, 'The Bear es mi favorita.');

-- Verificar que todo se insertó correctamente
SELECT 'Usuarios creados:' as info, COUNT(*) as count FROM users
UNION ALL
SELECT 'Películas creadas:', COUNT(*) FROM movies
UNION ALL
SELECT 'Series creadas:', COUNT(*) FROM series
UNION ALL
SELECT 'Reseñas creadas:', COUNT(*) FROM reviews
UNION ALL
SELECT 'Discusiones creadas:', COUNT(*) FROM forum_discussions
UNION ALL
SELECT 'Respuestas creadas:', COUNT(*) FROM forum_replies;

-- Mostrar los usuarios creados
SELECT username, email, user_type FROM users; 