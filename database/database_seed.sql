-- Script para poblar la base de datos PopcornHour con contenido de ejemplo
-- Ejecutar después de crear el esquema inicial

-- Insertar usuarios de ejemplo
INSERT INTO users (username, email, password_hash, user_type) VALUES
('admin', 'admin@popcornhour.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdXzogKLzPdAa', 'moderator'), -- password: admin123
('moderador1', 'mod1@popcornhour.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdXzogKLzPdAa', 'moderator'), -- password: admin123
('usuario1', 'user1@popcornhour.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdXzogKLzPdAa', 'standard'), -- password: admin123
('cinefan2024', 'cinefan@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdXzogKLzPdAa', 'standard'), -- password: admin123
('serieadicto', 'series@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdXzogKLzPdAa', 'standard'); -- password: admin123

-- Insertar películas de ejemplo
INSERT INTO movies (title, year, genre, duration, imdb_rating, description, created_by) VALUES
('Dune: Parte Dos', 2024, 'Sci-Fi', '166min', 8.8, 'Paul Atreides se une a Chani y los Fremen mientras busca venganza.', 1),
('Oppenheimer', 2023, 'Drama', '181min', 8.4, 'La historia de J. Robert Oppenheimer y la bomba atómica.', 1),
('The Batman', 2022, 'Acción', '176min', 7.8, 'Batman investiga una serie de asesinatos en Gotham City.', 1),
('Spider-Man: No Way Home', 2021, 'Acción', '148min', 8.2, 'Peter Parker debe enfrentar villanos de universos alternativos.', 1),
('Top Gun: Maverick', 2022, 'Acción', '131min', 8.3, 'Maverick regresa como instructor de pilotos de élite.', 1),
('Avatar: El Camino del Agua', 2022, 'Sci-Fi', '192min', 7.6, 'Jake Sully y su familia enfrentan nuevos desafíos en Pandora.', 1),
('Black Panther: Wakanda Forever', 2022, 'Acción', '161min', 6.7, 'Wakanda lucha por proteger su nación tras la muerte del Rey T''Challa.', 1),
('Doctor Strange 2', 2022, 'Acción', '126min', 6.9, 'Strange viaja por el multiverso para enfrentar una nueva amenaza.', 1),
('Jurassic World: Dominion', 2022, 'Acción', '147min', 5.6, 'Los dinosaurios ahora viven y cazan junto a los humanos.', 1),
('Minions: El Origen de Gru', 2022, 'Animación', '87min', 6.5, 'La historia de cómo Gru se convirtió en el villano más despreciable.', 1),
('Thor: Love and Thunder', 2022, 'Acción', '119min', 6.2, 'Thor busca la paz interior pero debe luchar contra Gorr.', 1),
('Lightyear', 2022, 'Animación', '105min', 6.1, 'La historia del origen del Space Ranger Buzz Lightyear.', 1),
('Sonic 2', 2022, 'Aventura', '122min', 6.5, 'Sonic y Tails enfrentan al Dr. Robotnik y Knuckles.', 1),
('Morbius', 2022, 'Acción', '104min', 5.1, 'Un científico se convierte en vampiro viviente.', 1),
('The Northman', 2022, 'Drama', '137min', 7.0, 'Un príncipe vikingo busca vengar la muerte de su padre.', 1),
('Everything Everywhere All at Once', 2022, 'Sci-Fi', '139min', 7.8, 'Una mujer debe conectar con versiones paralelas de sí misma.', 1),
('The Menu', 2022, 'Thriller', '107min', 7.2, 'Una pareja viaja a una isla para una experiencia culinaria exclusiva.', 1),
('Nope', 2022, 'Horror', '130min', 6.8, 'Hermanos intentan capturar evidencia de un OVNI.', 1),
('Bullet Train', 2022, 'Acción', '127min', 7.3, 'Asesinos rivales se encuentran en un tren bala japonés.', 1),
('Elvis', 2022, 'Drama', '159min', 7.3, 'La vida y carrera musical de Elvis Presley.', 1),
('Turning Red', 2022, 'Animación', '100min', 7.0, 'Una adolescente se convierte en un panda rojo gigante.', 1),
('The Lost City', 2022, 'Comedia', '112min', 6.1, 'Una novelista romántica es secuestrada por un excéntrico millonario.', 1),
('Scream', 2022, 'Horror', '114min', 6.3, 'Una nueva serie de asesinatos de Ghostface aterroriza Woodsboro.', 1),
('Uncharted', 2022, 'Aventura', '116min', 6.3, 'Nathan Drake busca el tesoro perdido de Magallanes.', 1),
('The Adam Project', 2022, 'Sci-Fi', '106min', 6.7, 'Un piloto viaja en el tiempo para salvar el futuro.', 1);

-- Insertar series de ejemplo
INSERT INTO series (title, year, genre, seasons, imdb_rating, description, created_by) VALUES
('House of the Dragon', 2022, 'Drama', 2, 8.4, 'Precuela de Game of Thrones sobre la casa Targaryen.', 1),
('The Bear', 2022, 'Comedia', 3, 8.7, 'Un chef de alta cocina regresa a Chicago para dirigir un restaurante.', 1),
('Stranger Things', 2016, 'Sci-Fi', 4, 8.7, 'Niños enfrentan fuerzas sobrenaturales en los años 80.', 1),
('The Boys', 2019, 'Acción', 4, 8.7, 'Un grupo lucha contra superhéroes corruptos.', 1),
('Euphoria', 2019, 'Drama', 2, 8.4, 'Adolescentes navegan por drogas, sexo y violencia.', 1),
('The Mandalorian', 2019, 'Sci-Fi', 3, 8.7, 'Un cazarrecompensas mandaloriano en el universo Star Wars.', 1),
('Wednesday', 2022, 'Comedia', 1, 8.1, 'Wednesday Addams en la Academia Nevermore.', 1),
('The Last of Us', 2023, 'Drama', 1, 8.8, 'Supervivientes en un mundo post-apocalíptico zombie.', 1),
('Succession', 2018, 'Drama', 4, 8.8, 'Una familia disfuncional lucha por el control de un imperio mediático.', 1),
('The White Lotus', 2021, 'Drama', 2, 7.6, 'Huéspedes y empleados en un resort de lujo.', 1),
('Ozark', 2017, 'Drama', 4, 8.4, 'Una familia se muda a Ozarks para lavar dinero del cartel.', 1),
('Better Call Saul', 2015, 'Drama', 6, 8.8, 'Precuela de Breaking Bad sobre el abogado Saul Goodman.', 1),
('The Crown', 2016, 'Drama', 6, 8.6, 'La vida de la Reina Isabel II y la familia real británica.', 1),
('Squid Game', 2021, 'Thriller', 1, 8.0, 'Personas desesperadas compiten en juegos infantiles mortales.', 1),
('Mare of Easttown', 2021, 'Drama', 1, 8.4, 'Una detective investiga un asesinato en su ciudad natal.', 1),
('Ted Lasso', 2020, 'Comedia', 3, 8.8, 'Un entrenador de fútbol americano entrena un equipo de fútbol inglés.', 1),
('The Queen''s Gambit', 2020, 'Drama', 1, 8.5, 'Una joven prodigio del ajedrez lucha contra la adicción.', 1),
('Bridgerton', 2020, 'Romance', 2, 7.3, 'Romance y escándalo en la alta sociedad londinense del siglo XIX.', 1),
('The Witcher', 2019, 'Fantasía', 3, 8.2, 'Geralt de Rivia, un cazador de monstruos en un mundo de magia.', 1),
('Money Heist', 2017, 'Thriller', 5, 8.2, 'Un grupo de ladrones ejecuta el atraco perfecto en España.', 1);

-- Insertar reseñas de ejemplo
INSERT INTO reviews (movie_id, user_id, rating, comment) VALUES
(1, 4, 9, 'Espectacular continuación. Villeneuve lo ha vuelto a hacer.'),
(2, 4, 8, 'Nolan en su máximo esplendor. Actuaciones increíbles.'),
(3, 5, 8, 'La mejor versión de Batman en años. Muy noir.'),
(4, 3, 9, 'No Way Home es puro fan service, pero funciona perfectamente.'),
(5, 4, 8, 'Maverick vuela alto una vez más. Cruise sigue siendo increíble.'),
(1, 3, 9, 'Dune Parte Dos supera a la primera en todos los aspectos.'),
(2, 5, 9, 'Oppenheimer es una obra maestra del cine biográfico.'),
(6, 4, 7, 'Avatar 2 es visualmente impresionante pero la historia es predecible.'),
(16, 3, 8, 'Everything Everywhere es una locura creativa que funciona.'),
(19, 5, 7, 'Bullet Train es entretenida pero no memorable.');

-- Insertar posts del foro de ejemplo
INSERT INTO forum_posts (title, content, user_id, category) VALUES
('¿Qué opinan de Dune: Parte Dos?', 'Acabo de ver la película y me parece que supera a la primera en todos los aspectos. ¿Qué piensan ustedes?', 4, 'movies'),
('Mejores series de 2024', 'Hagamos una lista de las mejores series que han salido este año. Yo empiezo con The Bear temporada 3.', 5, 'series'),
('Teorías sobre House of the Dragon', 'Después del final de la temporada 2, ¿qué creen que pasará con los Targaryen?', 3, 'series'),
('Películas más esperadas de 2025', 'Ya estoy emocionado por las películas que vienen el próximo año. ¿Cuáles esperan más?', 4, 'movies'),
('¿Vale la pena ver The Last of Us?', 'He escuchado cosas buenas pero no sé si empezarla. ¿Recomendaciones?', 3, 'series');

-- Insertar respuestas del foro de ejemplo
INSERT INTO forum_replies (post_id, user_id, content) VALUES
(1, 3, 'Totalmente de acuerdo. La cinematografía es impresionante.'),
(1, 5, 'A mí me gustó pero siento que le faltó más acción.'),
(2, 4, 'The Bear es increíble. También recomiendo Wednesday.'),
(3, 4, 'Creo que veremos más dragones en la próxima temporada.'),
(5, 4, 'Definitivamente vale la pena. Es una adaptación muy fiel al juego.');

-- Verificar que los datos se insertaron correctamente
SELECT 'Usuarios insertados:' as info, COUNT(*) as count FROM users
UNION ALL
SELECT 'Películas insertadas:', COUNT(*) FROM movies
UNION ALL
SELECT 'Series insertadas:', COUNT(*) FROM series
UNION ALL
SELECT 'Reseñas insertadas:', COUNT(*) FROM reviews
UNION ALL
SELECT 'Posts del foro:', COUNT(*) FROM forum_posts
UNION ALL
SELECT 'Respuestas del foro:', COUNT(*) FROM forum_replies;

