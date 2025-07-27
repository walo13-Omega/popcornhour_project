-- Limpiar todas las tablas antes de insertar datos de ejemplo
TRUNCATE TABLE forum_replies, forum_discussions, reviews, series, movies, users RESTART IDENTITY CASCADE;

-- Insertar usuarios de ejemplo
INSERT INTO users (username, email, password_hash, user_type) VALUES
('admin', 'admin@popcornhour.com', '$2b$12$LrSzZt.ywKxag0aulFA1yuOxunDGQYvLxzbEpKGNoS9dcjdL8u56C', 'moderator'),
('user1', 'user1@popcornhour.com', '$2b$12$LrSzZt.ywKxag0aulFA1yuOxunDGQYvLxzbEpKGNoS9dcjdL8u56C', 'standard'),
('user2', 'user2@popcornhour.com', '$2b$12$LrSzZt.ywKxag0aulFA1yuOxunDGQYvLxzbEpKGNoS9dcjdL8u56C', 'standard'),
('modnuevo1', 'modnuevo1@popcornhour.com', '$2b$12$LrSzZt.ywKxag0aulFA1yuOxunDGQYvLxzbEpKGNoS9dcjdL8u56C', 'moderator'),
('modnuevo2', 'modnuevo2@popcornhour.com', '$2b$12$LrSzZt.ywKxag0aulFA1yuOxunDGQYvLxzbEpKGNoS9dcjdL8u56C', 'moderator');
-- ... el resto igual ...
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
('La La Land', 'Una historia de amor entre un pianista de jazz y una aspirante a actriz en Los Ángeles.', 2016, 128, 'Musical', 4.4, 1),
('Whiplash', 'Un joven baterista ambicioso se enfrenta a un exigente instructor de música.', 2014, 107, 'Drama', 4.5, 1),
('Gladiator', 'Un general romano busca venganza tras ser traicionado.', 2000, 155, 'Acción', 4.6, 1),
('Forrest Gump', 'La vida de un hombre con un bajo coeficiente intelectual que presencia grandes eventos históricos.', 1994, 142, 'Drama', 4.8, 1),
('El Gran Hotel Budapest', 'Las aventuras de un conserje legendario en un famoso hotel europeo.', 2014, 99, 'Comedia', 4.3, 1),
('Coco', 'Un niño mexicano viaja a la Tierra de los Muertos para descubrir la historia de su familia.', 2017, 105, 'Animación', 4.7, 1),
('El Origen', 'Un ladrón roba secretos corporativos a través de la tecnología de sueños.', 2010, 148, 'Sci-Fi', 4.8, 1),
('El Padrino', 'La historia de la familia criminal Corleone.', 1972, 175, 'Crimen', 4.9, 1),
('Pulp Fiction', 'Historias entrelazadas de crimen en Los Ángeles.', 1994, 154, 'Crimen', 4.7, 1),
('Amélie', 'Una joven decide ayudar a los que la rodean en París.', 2001, 122, 'Romance', 4.5, 1)
-- Insertar series de ejemplo
INSERT INTO series (title, description, release_year, seasons, genre, imdb_rating, created_by) VALUES
('House of the Dragon', 'Precuela de Game of Thrones sobre la casa Targaryen.', 2022, 2, 'Drama', 4.4, 1),
('The Bear', 'Un chef de alta cocina regresa a Chicago para dirigir un restaurante.', 2022, 3, 'Comedia', 4.7, 1),
('Stranger Things', 'Niños enfrentan fuerzas sobrenaturales en los años 80.', 2016, 4, 'Sci-Fi', 4.7, 1),
('The Boys', 'Un grupo lucha contra superhéroes corruptos.', 2019, 4, 'Acción', 4.7, 1),
('Euphoria', 'Adolescentes navegan por drogas, sexo y violencia.', 2019, 2, 'Drama', 4.4, 1);
('Sherlock', 'Un detective moderno resuelve crímenes en Londres.', 2010, 4, 'Misterio', 4.7, 1),
('Fargo', 'Historias de crimen inspiradas en la película homónima.', 2014, 5, 'Crimen', 4.5, 1),
('Narcos', 'La historia de los cárteles de droga en Colombia.', 2015, 3, 'Crimen', 4.4, 1),
('Chernobyl', 'La historia del desastre nuclear de 1986.', 2019, 1, 'Drama', 4.8, 1),
('The Office', 'La vida diaria de los empleados de una oficina.', 2005, 9, 'Comedia', 4.6, 1),
('Friends', 'Seis amigos navegan la vida y el amor en Nueva York.', 1994, 10, 'Comedia', 4.7, 1),
('Black Mirror', 'Episodios independientes sobre tecnología y sociedad.', 2011, 6, 'Sci-Fi', 4.5, 1),
('Better Call Saul', 'La precuela de Breaking Bad sobre el abogado Saul Goodman.', 2015, 6, 'Drama', 4.6, 1),
('The Mandalorian', 'Un cazarrecompensas en el universo de Star Wars.', 2019, 3, 'Sci-Fi', 4.7, 1),
('The Crown', 'La vida de la Reina Isabel II y la familia real británica.', 2016, 6, 'Drama', 4.5, 1)
-- Insertar reseñas de ejemplo (solo user_id 1 y 2)
INSERT INTO reviews (user_id, content_type, content_id, content, rating) VALUES
(1, 'movie', 1, '¡Excelente película!', 4.5),
(2, 'movie', 2, 'Muy buena historia.', 4.0);

-- Insertar discusiones del foro de ejemplo (solo user_id 1 y 2)
INSERT INTO forum_discussions (title, content, user_id, category) VALUES
('¿Qué opinan de Dune: Parte Dos?', 'Me encantó la película.', 1, 'movies'),
('Mejores series de 2024', '¿Cuál es tu favorita?', 2, 'series');

-- Insertar respuestas del foro de ejemplo (discussion_id 1-2, user_id 1-2)
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

