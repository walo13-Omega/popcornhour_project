-- Script para limpiar y recrear usuarios con contraseñas válidas
-- Ejecutar: psql -U popcornhour_user -d popcornhour_db -f reset_users.sql

-- Limpiar todos los usuarios existentes
TRUNCATE TABLE forum_replies, forum_discussions, reviews, series, movies, users RESTART IDENTITY CASCADE;

-- Insertar usuarios con contraseñas válidas
-- Contraseña: 123456 (hash generado con bcrypt)
INSERT INTO users (username, email, password_hash, user_type) VALUES
('admin', 'admin@popcornhour.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2.', 'moderator'),
('moderator', 'moderator@popcornhour.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2.', 'moderator'),
('user', 'user@popcornhour.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2.', 'standard'),
('test', 'test@popcornhour.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2.', 'moderator');

-- Insertar películas de ejemplo
INSERT INTO movies (title, description, release_year, duration_minutes, genre, imdb_rating, created_by) VALUES
('Dune: Parte Dos', 'Paul Atreides se une a Chani y los Fremen mientras busca venganza.', 2024, 166, 'Sci-Fi', 4.8, 1),
('Oppenheimer', 'La historia de J. Robert Oppenheimer y la bomba atómica.', 2023, 181, 'Drama', 4.4, 1),
('The Batman', 'Batman investiga una serie de asesinatos en Gotham City.', 2022, 176, 'Acción', 4.2, 1),
('Spider-Man: No Way Home', 'Peter Parker debe enfrentar villanos de universos alternativos.', 2021, 148, 'Acción', 4.5, 1),
('Top Gun: Maverick', 'Maverick regresa como instructor de pilotos de élite.', 2022, 131, 'Acción', 4.3, 1),
('Avatar: El Camino del Agua', 'Jake Sully y su familia enfrentan nuevos desafíos en Pandora.', 2022, 192, 'Sci-Fi', 3.6, 1),
('Black Panther: Wakanda Forever', 'Wakanda lucha por proteger su nación tras la muerte del Rey T''Challa.', 2022, 161, 'Acción', 3.7, 1),
('Doctor Strange 2', 'Strange viaja por el multiverso para enfrentar una nueva amenaza.', 2022, 126, 'Acción', 3.9, 1),
('Jurassic World: Dominion', 'Los dinosaurios ahora viven y cazan junto a los humanos.', 2022, 147, 'Acción', 2.6, 1),
('Minions: El Origen de Gru', 'La historia de cómo Gru se convirtió en el villano más despreciable.', 2022, 87, 'Animación', 3.5, 1);

-- Insertar series de ejemplo
INSERT INTO series (title, description, release_year, seasons, genre, imdb_rating, created_by) VALUES
('House of the Dragon', 'Precuela de Game of Thrones sobre la casa Targaryen.', 2022, 2, 'Drama', 4.4, 1),
('The Bear', 'Un chef de alta cocina regresa a Chicago para dirigir un restaurante.', 2022, 3, 'Comedia', 4.7, 1),
('Stranger Things', 'Niños enfrentan fuerzas sobrenaturales en los años 80.', 2016, 4, 'Sci-Fi', 4.7, 1),
('The Boys', 'Un grupo lucha contra superhéroes corruptos.', 2019, 4, 'Acción', 4.7, 1),
('Euphoria', 'Adolescentes navegan por drogas, sexo y violencia.', 2019, 2, 'Drama', 4.4, 1);

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

-- Verificar que los datos se insertaron correctamente
SELECT 'Usuarios insertados:' as info, COUNT(*) as count FROM users
UNION ALL
SELECT 'Películas insertadas:', COUNT(*) FROM movies
UNION ALL
SELECT 'Series insertadas:', COUNT(*) FROM series
UNION ALL
SELECT 'Reseñas insertadas:', COUNT(*) FROM reviews
UNION ALL
SELECT 'Discusiones del foro:', COUNT(*) FROM forum_discussions
UNION ALL
SELECT 'Respuestas del foro:', COUNT(*) FROM forum_replies; 