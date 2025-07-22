"""
PopcornHour - Aplicación Frontend con Reflex
Portal web para recomendar, calificar y discutir películas y series
"""

import reflex as rx
import httpx
import asyncio
from typing import List, Dict, Optional
import json

# Configuración de la API
API_BASE_URL = "http://localhost:3001"

class State(rx.State):
    # Estado de autenticación
    is_authenticated: bool = False
    current_user: Dict = {}
    user_type: str = "standard"  # "standard" o "moderator"
    
    # Estado de navegación
    current_page: str = "inicio"
    
    # Estado de datos
    movies: List[Dict] = []
    series: List[Dict] = []
    reviews: List[Dict] = []
    forum_posts: List[Dict] = []
    
    # Estado de formularios
    login_username: str = ""
    login_password: str = ""
    register_username: str = ""
    register_email: str = ""
    register_password: str = ""
    register_user_type: str = "standard"
    
    # Estado de mensajes
    message: str = ""
    message_type: str = ""  # "success" o "error"
    
    # Estado de modales
    show_add_movie_modal: bool = False
    show_add_series_modal: bool = False
    
    # Formularios para agregar contenido
    new_movie_title: str = ""
    new_movie_year: str = ""
    new_movie_genre: str = ""
    new_movie_duration: str = ""
    new_movie_rating: str = ""
    new_movie_description: str = ""
    
    new_series_title: str = ""
    new_series_year: str = ""
    new_series_genre: str = ""
    new_series_seasons: str = ""
    new_series_rating: str = ""
    new_series_description: str = ""

    def set_page(self, page: str):
        """Cambiar página con verificación de autenticación"""
        # Páginas que requieren autenticación
        protected_pages = ["perfil", "mi_lista"]
        
        if page in protected_pages and not self.is_authenticated:
            self.current_page = "login"
            self.message = "Debes iniciar sesión para acceder a esta página"
            self.message_type = "error"
        else:
            self.current_page = page
            self.message = ""

    async def login(self):
        """Iniciar sesión"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_BASE_URL}/api/auth/login",
                    json={
                        "username": self.login_username,
                        "password": self.login_password
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.is_authenticated = True
                    self.current_user = data.get("user", {})
                    self.user_type = data.get("user", {}).get("user_type", "standard")
                    self.current_page = "inicio"
                    self.message = f"¡Bienvenido, {self.current_user.get('username', 'Usuario')}!"
                    self.message_type = "success"
                    
                    # Limpiar formulario
                    self.login_username = ""
                    self.login_password = ""
                    
                    # Cargar datos
                    await self.load_movies()
                    await self.load_series()
                else:
                    self.message = "Credenciales incorrectas"
                    self.message_type = "error"
                    
        except Exception as e:
            self.message = "Error de conexión con el servidor"
            self.message_type = "error"

    async def register(self):
        """Registrar nuevo usuario"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_BASE_URL}/api/auth/register",
                    json={
                        "username": self.register_username,
                        "email": self.register_email,
                        "password": self.register_password,
                        "user_type": self.register_user_type
                    }
                )
                
                if response.status_code == 201:
                    self.message = "Usuario registrado exitosamente. Puedes iniciar sesión."
                    self.message_type = "success"
                    self.current_page = "login"
                    
                    # Limpiar formulario
                    self.register_username = ""
                    self.register_email = ""
                    self.register_password = ""
                    self.register_user_type = "standard"
                else:
                    data = response.json()
                    self.message = data.get("message", "Error al registrar usuario")
                    self.message_type = "error"
                    
        except Exception as e:
            self.message = "Error de conexión con el servidor"
            self.message_type = "error"

    def logout(self):
        """Cerrar sesión"""
        self.is_authenticated = False
        self.current_user = {}
        self.user_type = "standard"
        self.current_page = "inicio"
        self.message = "Sesión cerrada exitosamente"
        self.message_type = "success"
        
        # Limpiar datos
        self.movies = []
        self.series = []
        self.reviews = []

    async def load_movies(self):
        """Cargar películas desde la API o datos de ejemplo"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE_URL}/api/movies")
                if response.status_code == 200:
                    self.movies = response.json()
                    return
        except:
            pass
        
        # Datos de ejemplo si la API no está disponible
        self.movies = [
            {"id": 1, "title": "Dune: Parte Dos", "year": 2024, "genre": "Sci-Fi", "duration": "166min", "imdb_rating": 8.8, "description": "Paul Atreides se une a Chani y los Fremen mientras busca venganza."},
            {"id": 2, "title": "Oppenheimer", "year": 2023, "genre": "Drama", "duration": "181min", "imdb_rating": 8.4, "description": "La historia de J. Robert Oppenheimer y la bomba atómica."},
            {"id": 3, "title": "The Batman", "year": 2022, "genre": "Acción", "duration": "176min", "imdb_rating": 7.8, "description": "Batman investiga una serie de asesinatos en Gotham City."},
            {"id": 4, "title": "Spider-Man: No Way Home", "year": 2021, "genre": "Acción", "duration": "148min", "imdb_rating": 8.2, "description": "Peter Parker debe enfrentar villanos de universos alternativos."},
            {"id": 5, "title": "Top Gun: Maverick", "year": 2022, "genre": "Acción", "duration": "131min", "imdb_rating": 8.3, "description": "Maverick regresa como instructor de pilotos de élite."},
            {"id": 6, "title": "Avatar: El Camino del Agua", "year": 2022, "genre": "Sci-Fi", "duration": "192min", "imdb_rating": 7.6, "description": "Jake Sully y su familia enfrentan nuevos desafíos en Pandora."},
            {"id": 7, "title": "Black Panther: Wakanda Forever", "year": 2022, "genre": "Acción", "duration": "161min", "imdb_rating": 6.7, "description": "Wakanda lucha por proteger su nación tras la muerte del Rey T'Challa."},
            {"id": 8, "title": "Doctor Strange 2", "year": 2022, "genre": "Acción", "duration": "126min", "imdb_rating": 6.9, "description": "Strange viaja por el multiverso para enfrentar una nueva amenaza."},
            {"id": 9, "title": "Jurassic World: Dominion", "year": 2022, "genre": "Acción", "duration": "147min", "imdb_rating": 5.6, "description": "Los dinosaurios ahora viven y cazan junto a los humanos."},
            {"id": 10, "title": "Minions: El Origen de Gru", "year": 2022, "genre": "Animación", "duration": "87min", "imdb_rating": 6.5, "description": "La historia de cómo Gru se convirtió en el villano más despreciable."},
            {"id": 11, "title": "Thor: Love and Thunder", "year": 2022, "genre": "Acción", "duration": "119min", "imdb_rating": 6.2, "description": "Thor busca la paz interior pero debe luchar contra Gorr."},
            {"id": 12, "title": "Lightyear", "year": 2022, "genre": "Animación", "duration": "105min", "imdb_rating": 6.1, "description": "La historia del origen del Space Ranger Buzz Lightyear."},
            {"id": 13, "title": "Sonic 2", "year": 2022, "genre": "Aventura", "duration": "122min", "imdb_rating": 6.5, "description": "Sonic y Tails enfrentan al Dr. Robotnik y Knuckles."},
            {"id": 14, "title": "Morbius", "year": 2022, "genre": "Acción", "duration": "104min", "imdb_rating": 5.1, "description": "Un científico se convierte en vampiro viviente."},
            {"id": 15, "title": "The Northman", "year": 2022, "genre": "Drama", "duration": "137min", "imdb_rating": 7.0, "description": "Un príncipe vikingo busca vengar la muerte de su padre."},
            {"id": 16, "title": "Everything Everywhere All at Once", "year": 2022, "genre": "Sci-Fi", "duration": "139min", "imdb_rating": 7.8, "description": "Una mujer debe conectar con versiones paralelas de sí misma."},
            {"id": 17, "title": "The Menu", "year": 2022, "genre": "Thriller", "duration": "107min", "imdb_rating": 7.2, "description": "Una pareja viaja a una isla para una experiencia culinaria exclusiva."},
            {"id": 18, "title": "Nope", "year": 2022, "genre": "Horror", "duration": "130min", "imdb_rating": 6.8, "description": "Hermanos intentan capturar evidencia de un OVNI."},
            {"id": 19, "title": "Bullet Train", "year": 2022, "genre": "Acción", "duration": "127min", "imdb_rating": 7.3, "description": "Asesinos rivales se encuentran en un tren bala japonés."},
            {"id": 20, "title": "Elvis", "year": 2022, "genre": "Drama", "duration": "159min", "imdb_rating": 7.3, "description": "La vida y carrera musical de Elvis Presley."},
            {"id": 21, "title": "Turning Red", "year": 2022, "genre": "Animación", "duration": "100min", "imdb_rating": 7.0, "description": "Una adolescente se convierte en un panda rojo gigante."},
            {"id": 22, "title": "The Lost City", "year": 2022, "genre": "Comedia", "duration": "112min", "imdb_rating": 6.1, "description": "Una novelista romántica es secuestrada por un excéntrico millonario."},
            {"id": 23, "title": "Scream", "year": 2022, "genre": "Horror", "duration": "114min", "imdb_rating": 6.3, "description": "Una nueva serie de asesinatos de Ghostface aterroriza Woodsboro."},
            {"id": 24, "title": "Uncharted", "year": 2022, "genre": "Aventura", "duration": "116min", "imdb_rating": 6.3, "description": "Nathan Drake busca el tesoro perdido de Magallanes."},
            {"id": 25, "title": "The Batman", "year": 2022, "genre": "Acción", "duration": "176min", "imdb_rating": 7.8, "description": "Una nueva versión del Caballero de la Noche."}
        ]

    async def load_series(self):
        """Cargar series desde la API o datos de ejemplo"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE_URL}/api/series")
                if response.status_code == 200:
                    self.series = response.json()
                    return
        except:
            pass
        
        # Datos de ejemplo si la API no está disponible
        self.series = [
            {"id": 1, "title": "House of the Dragon", "year": 2022, "genre": "Drama", "seasons": 2, "imdb_rating": 8.4, "description": "Precuela de Game of Thrones sobre la casa Targaryen."},
            {"id": 2, "title": "The Bear", "year": 2022, "genre": "Comedia", "seasons": 3, "imdb_rating": 8.7, "description": "Un chef de alta cocina regresa a Chicago para dirigir un restaurante."},
            {"id": 3, "title": "Stranger Things", "year": 2016, "genre": "Sci-Fi", "seasons": 4, "imdb_rating": 8.7, "description": "Niños enfrentan fuerzas sobrenaturales en los años 80."},
            {"id": 4, "title": "The Boys", "year": 2019, "genre": "Acción", "seasons": 4, "imdb_rating": 8.7, "description": "Un grupo lucha contra superhéroes corruptos."},
            {"id": 5, "title": "Euphoria", "year": 2019, "genre": "Drama", "seasons": 2, "imdb_rating": 8.4, "description": "Adolescentes navegan por drogas, sexo y violencia."},
            {"id": 6, "title": "The Mandalorian", "year": 2019, "genre": "Sci-Fi", "seasons": 3, "imdb_rating": 8.7, "description": "Un cazarrecompensas mandaloriano en el universo Star Wars."},
            {"id": 7, "title": "Wednesday", "year": 2022, "genre": "Comedia", "seasons": 1, "imdb_rating": 8.1, "description": "Wednesday Addams en la Academia Nevermore."},
            {"id": 8, "title": "The Last of Us", "year": 2023, "genre": "Drama", "seasons": 1, "imdb_rating": 8.8, "description": "Supervivientes en un mundo post-apocalíptico zombie."},
            {"id": 9, "title": "Succession", "year": 2018, "genre": "Drama", "seasons": 4, "imdb_rating": 8.8, "description": "Una familia disfuncional lucha por el control de un imperio mediático."},
            {"id": 10, "title": "The White Lotus", "year": 2021, "genre": "Drama", "seasons": 2, "imdb_rating": 7.6, "description": "Huéspedes y empleados en un resort de lujo."},
            {"id": 11, "title": "Ozark", "year": 2017, "genre": "Drama", "seasons": 4, "imdb_rating": 8.4, "description": "Una familia se muda a Ozarks para lavar dinero del cartel."},
            {"id": 12, "title": "Better Call Saul", "year": 2015, "genre": "Drama", "seasons": 6, "imdb_rating": 8.8, "description": "Precuela de Breaking Bad sobre el abogado Saul Goodman."},
            {"id": 13, "title": "The Crown", "year": 2016, "genre": "Drama", "seasons": 6, "imdb_rating": 8.6, "description": "La vida de la Reina Isabel II y la familia real británica."},
            {"id": 14, "title": "Squid Game", "year": 2021, "genre": "Thriller", "seasons": 1, "imdb_rating": 8.0, "description": "Personas desesperadas compiten en juegos infantiles mortales."},
            {"id": 15, "title": "Mare of Easttown", "year": 2021, "genre": "Drama", "seasons": 1, "imdb_rating": 8.4, "description": "Una detective investiga un asesinato en su ciudad natal."},
            {"id": 16, "title": "Ted Lasso", "year": 2020, "genre": "Comedia", "seasons": 3, "imdb_rating": 8.8, "description": "Un entrenador de fútbol americano entrena un equipo de fútbol inglés."},
            {"id": 17, "title": "The Queen's Gambit", "year": 2020, "genre": "Drama", "seasons": 1, "imdb_rating": 8.5, "description": "Una joven prodigio del ajedrez lucha contra la adicción."},
            {"id": 18, "title": "Bridgerton", "year": 2020, "genre": "Romance", "seasons": 2, "imdb_rating": 7.3, "description": "Romance y escándalo en la alta sociedad londinense del siglo XIX."},
            {"id": 19, "title": "The Witcher", "year": 2019, "genre": "Fantasía", "seasons": 3, "imdb_rating": 8.2, "description": "Geralt de Rivia, un cazador de monstruos en un mundo de magia."},
            {"id": 20, "title": "Money Heist", "year": 2017, "genre": "Thriller", "seasons": 5, "imdb_rating": 8.2, "description": "Un grupo de ladrones ejecuta el atraco perfecto en España."}
        ]

    async def load_reviews(self):
        """Cargar reseñas desde la API o datos de ejemplo"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE_URL}/api/reviews")
                if response.status_code == 200:
                    self.reviews = response.json()
                    return
        except:
            pass
        
        # Datos de ejemplo
        self.reviews = [
            {"id": 1, "movie_title": "Dune: Parte Dos", "user": "CineFan2024", "rating": 9, "comment": "Espectacular continuación. Villeneuve lo ha vuelto a hacer."},
            {"id": 2, "movie_title": "Oppenheimer", "user": "HistoryBuff", "rating": 8, "comment": "Nolan en su máximo esplendor. Actuaciones increíbles."},
            {"id": 3, "movie_title": "The Batman", "user": "ComicLover", "rating": 8, "comment": "La mejor versión de Batman en años. Muy noir."}
        ]

    # Funciones para modales
    def toggle_add_movie_modal(self):
        self.show_add_movie_modal = not self.show_add_movie_modal

    def toggle_add_series_modal(self):
        self.show_add_series_modal = not self.show_add_series_modal

    async def add_movie(self):
        """Agregar nueva película"""
        if not self.user_type == "moderator":
            self.message = "Solo los moderadores pueden agregar películas"
            self.message_type = "error"
            return
        
        try:
            new_movie = {
                "id": len(self.movies) + 1,
                "title": self.new_movie_title,
                "year": int(self.new_movie_year) if self.new_movie_year else 2024,
                "genre": self.new_movie_genre,
                "duration": self.new_movie_duration,
                "imdb_rating": float(self.new_movie_rating) if self.new_movie_rating else 7.0,
                "description": self.new_movie_description
            }
            
            self.movies.append(new_movie)
            self.message = f"Película '{self.new_movie_title}' agregada exitosamente"
            self.message_type = "success"
            
            # Limpiar formulario
            self.new_movie_title = ""
            self.new_movie_year = ""
            self.new_movie_genre = ""
            self.new_movie_duration = ""
            self.new_movie_rating = ""
            self.new_movie_description = ""
            self.show_add_movie_modal = False
            
        except Exception as e:
            self.message = "Error al agregar película"
            self.message_type = "error"

    async def add_series(self):
        """Agregar nueva serie"""
        if not self.user_type == "moderator":
            self.message = "Solo los moderadores pueden agregar series"
            self.message_type = "error"
            return
        
        try:
            new_series = {
                "id": len(self.series) + 1,
                "title": self.new_series_title,
                "year": int(self.new_series_year) if self.new_series_year else 2024,
                "genre": self.new_series_genre,
                "seasons": int(self.new_series_seasons) if self.new_series_seasons else 1,
                "imdb_rating": float(self.new_series_rating) if self.new_series_rating else 7.0,
                "description": self.new_series_description
            }
            
            self.series.append(new_series)
            self.message = f"Serie '{self.new_series_title}' agregada exitosamente"
            self.message_type = "success"
            
            # Limpiar formulario
            self.new_series_title = ""
            self.new_series_year = ""
            self.new_series_genre = ""
            self.new_series_seasons = ""
            self.new_series_rating = ""
            self.new_series_description = ""
            self.show_add_series_modal = False
            
        except Exception as e:
            self.message = "Error al agregar serie"
            self.message_type = "error"

    def on_load(self):
        """Cargar datos al iniciar la aplicación"""
        return [
            State.load_movies,
            State.load_series,
            State.load_reviews
        ]

# Componentes de UI

def message_component() -> rx.Component:
    """Componente para mostrar mensajes"""
    return rx.cond(
        State.message != "",
        rx.box(
            rx.text(State.message),
            background_color=rx.cond(
                State.message_type == "success",
                "green",
                "red"
            ),
            color="white",
            padding="10px",
            border_radius="5px",
            margin_bottom="20px"
        )
    )

def star_rating(rating: float) -> rx.Component:
    """Componente para mostrar calificación con estrellas"""
    stars = []
    for i in range(5):
        if i < int(rating / 2):
            stars.append("⭐")
        else:
            stars.append("☆")
    
    return rx.hstack(
        rx.text("".join(stars), color="gold", font_size="16px"),
        rx.text(f"{rating}/10", color="white", font_size="14px", margin_left="10px"),
        align_items="center"
    )

def movie_card(movie: Dict) -> rx.Component:
    """Tarjeta de película mejorada"""
    return rx.box(
        rx.vstack(
            # Imagen placeholder
            rx.box(
                rx.text("🎬", font_size="60px"),
                width="100%",
                height="240px",
                background_color="rgba(255, 255, 255, 0.1)",
                border_radius="8px",
                display="flex",
                align_items="center",
                justify_content="center"
            ),
            # Información
            rx.vstack(
                rx.text(
                    movie["title"],
                    font_size="16px",
                    font_weight="bold",
                    color="white",
                    text_align="center"
                ),
                rx.text(
                    f"{movie['year']} • {movie['duration']}",
                    font_size="12px",
                    color="gray",
                    text_align="center"
                ),
                star_rating(movie["imdb_rating"]),
                spacing="5px",
                width="100%"
            ),
            spacing="10px",
            width="100%"
        ),
        width="200px",
        padding="15px",
        background_color="rgba(255, 255, 255, 0.05)",
        border_radius="10px",
        border="1px solid rgba(255, 255, 255, 0.1)",
        _hover={
            "transform": "translateY(-5px)",
            "box_shadow": "0 10px 25px rgba(0, 0, 0, 0.3)"
        },
        transition="all 0.3s ease"
    )

def series_card(series: Dict) -> rx.Component:
    """Tarjeta de serie mejorada"""
    return rx.box(
        rx.vstack(
            # Imagen placeholder
            rx.box(
                rx.text("📺", font_size="60px"),
                width="100%",
                height="240px",
                background_color="rgba(255, 255, 255, 0.1)",
                border_radius="8px",
                display="flex",
                align_items="center",
                justify_content="center"
            ),
            # Información
            rx.vstack(
                rx.text(
                    series["title"],
                    font_size="16px",
                    font_weight="bold",
                    color="white",
                    text_align="center"
                ),
                rx.text(
                    f"{series['year']} • {series['seasons']} temporadas",
                    font_size="12px",
                    color="gray",
                    text_align="center"
                ),
                star_rating(series["imdb_rating"]),
                spacing="5px",
                width="100%"
            ),
            spacing="10px",
            width="100%"
        ),
        width="200px",
        padding="15px",
        background_color="rgba(255, 255, 255, 0.05)",
        border_radius="10px",
        border="1px solid rgba(255, 255, 255, 0.1)",
        _hover={
            "transform": "translateY(-5px)",
            "box_shadow": "0 10px 25px rgba(0, 0, 0, 0.3)"
        },
        transition="all 0.3s ease"
    )

def review_card(review: Dict) -> rx.Component:
    """Tarjeta de reseña"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("👤", font_size="20px"),
                rx.text(review["user"], font_weight="bold", color="white"),
                star_rating(review["rating"]),
                justify_content="space_between",
                width="100%"
            ),
            rx.text(review["movie_title"], font_size="14px", color="orange"),
            rx.text(review["comment"], color="gray"),
            spacing="10px",
            align_items="start"
        ),
        padding="20px",
        background_color="rgba(255, 255, 255, 0.05)",
        border_radius="10px",
        border="1px solid rgba(255, 255, 255, 0.1)",
        width="100%"
    )

def navbar() -> rx.Component:
    """Barra de navegación mejorada"""
    return rx.box(
        rx.hstack(
            # Logo
            rx.hstack(
                rx.text("🍿", font_size="30px"),
                rx.text("PopcornHour", font_size="24px", font_weight="bold", color="orange"),
                spacing="10px"
            ),
            
            # Navegación central
            rx.hstack(
                rx.button("Inicio", on_click=State.set_page("inicio"), variant="ghost", color="white", padding="15px"),
                rx.button("Películas", on_click=State.set_page("peliculas"), variant="ghost", color="white", padding="15px"),
                rx.button("Series", on_click=State.set_page("series"), variant="ghost", color="white", padding="15px"),
                rx.button("Novedades", on_click=State.set_page("novedades"), variant="ghost", color="white", padding="15px"),
                rx.button("Foro", on_click=State.set_page("foro"), variant="ghost", color="white", padding="15px"),
                rx.button("Top 10", on_click=State.set_page("top10"), variant="ghost", color="white", padding="15px"),
                spacing="20px"
            ),
            
            # Buscador
            rx.input(
                placeholder="Buscar...",
                width="300px",
                background_color="rgba(255, 255, 255, 0.1)",
                border="1px solid rgba(255, 255, 255, 0.2)",
                color="white"
            ),
            
            # Usuario
            rx.cond(
                State.is_authenticated,
                rx.hstack(
                    rx.text(f"Usuario", color="white"),
                    rx.button("Salir", on_click=State.logout, background_color="red", color="white"),
                    spacing="15px"
                ),
                rx.hstack(
                    rx.button("Iniciar Sesión", on_click=State.set_page("login"), variant="outline", color="white"),
                    rx.button("Registrarse", on_click=State.set_page("register"), background_color="orange", color="white"),
                    spacing="15px"
                )
            ),
            
            justify_content="space_between",
            align_items="center",
            width="100%",
            padding="20px"
        ),
        background_color="rgba(0, 0, 0, 0.9)",
        border_bottom="1px solid rgba(255, 255, 255, 0.1)",
        position="sticky",
        top="0",
        z_index="1000"
    )

def add_movie_modal() -> rx.Component:
    """Modal para agregar película"""
    return rx.cond(
        State.show_add_movie_modal,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text("Agregar Nueva Película", font_size="20px", font_weight="bold", color="white"),
                        rx.button("✕", on_click=State.toggle_add_movie_modal, variant="ghost", color="white"),
                        justify_content="space_between",
                        width="100%"
                    ),
                    rx.input(
                        placeholder="Título",
                        value=State.new_movie_title,
                        on_change=State.set_new_movie_title,
                        width="100%"
                    ),
                    rx.input(
                        placeholder="Año",
                        value=State.new_movie_year,
                        on_change=State.set_new_movie_year,
                        width="100%"
                    ),
                    rx.input(
                        placeholder="Género",
                        value=State.new_movie_genre,
                        on_change=State.set_new_movie_genre,
                        width="100%"
                    ),
                    rx.input(
                        placeholder="Duración (ej: 120min)",
                        value=State.new_movie_duration,
                        on_change=State.set_new_movie_duration,
                        width="100%"
                    ),
                    rx.input(
                        placeholder="Calificación (1-10)",
                        value=State.new_movie_rating,
                        on_change=State.set_new_movie_rating,
                        width="100%"
                    ),
                    rx.text_area(
                        placeholder="Descripción",
                        value=State.new_movie_description,
                        on_change=State.set_new_movie_description,
                        width="100%",
                        height="100px"
                    ),
                    rx.button(
                        "Agregar Película",
                        on_click=State.add_movie,
                        background_color="orange",
                        color="white",
                        width="100%"
                    ),
                    spacing="15px",
                    width="100%"
                ),
                background_color="rgba(20, 20, 20, 0.95)",
                padding="30px",
                border_radius="10px",
                border="1px solid rgba(255, 255, 255, 0.2)",
                width="500px",
                max_height="80vh",
                overflow_y="auto"
            ),
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            background_color="rgba(0, 0, 0, 0.8)",
            display="flex",
            align_items="center",
            justify_content="center",
            z_index="2000"
        )
    )

def add_series_modal() -> rx.Component:
    """Modal para agregar serie"""
    return rx.cond(
        State.show_add_series_modal,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text("Agregar Nueva Serie", font_size="20px", font_weight="bold", color="white"),
                        rx.button("✕", on_click=State.toggle_add_series_modal, variant="ghost", color="white"),
                        justify_content="space_between",
                        width="100%"
                    ),
                    rx.input(
                        placeholder="Título",
                        value=State.new_series_title,
                        on_change=State.set_new_series_title,
                        width="100%"
                    ),
                    rx.input(
                        placeholder="Año",
                        value=State.new_series_year,
                        on_change=State.set_new_series_year,
                        width="100%"
                    ),
                    rx.input(
                        placeholder="Género",
                        value=State.new_series_genre,
                        on_change=State.set_new_series_genre,
                        width="100%"
                    ),
                    rx.input(
                        placeholder="Número de temporadas",
                        value=State.new_series_seasons,
                        on_change=State.set_new_series_seasons,
                        width="100%"
                    ),
                    rx.input(
                        placeholder="Calificación (1-10)",
                        value=State.new_series_rating,
                        on_change=State.set_new_series_rating,
                        width="100%"
                    ),
                    rx.text_area(
                        placeholder="Descripción",
                        value=State.new_series_description,
                        on_change=State.set_new_series_description,
                        width="100%",
                        height="100px"
                    ),
                    rx.button(
                        "Agregar Serie",
                        on_click=State.add_series,
                        background_color="orange",
                        color="white",
                        width="100%"
                    ),
                    spacing="15px",
                    width="100%"
                ),
                background_color="rgba(20, 20, 20, 0.95)",
                padding="30px",
                border_radius="10px",
                border="1px solid rgba(255, 255, 255, 0.2)",
                width="500px",
                max_height="80vh",
                overflow_y="auto"
            ),
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            background_color="rgba(0, 0, 0, 0.8)",
            display="flex",
            align_items="center",
            justify_content="center",
            z_index="2000"
        )
    )

# Páginas

def login_page() -> rx.Component:
    """Página de inicio de sesión"""
    return rx.container(
        rx.vstack(
            rx.text("Iniciar Sesión", font_size="32px", font_weight="bold", color="white", text_align="center"),
            message_component(),
            rx.vstack(
                rx.input(
                    placeholder="Usuario",
                    value=State.login_username,
                    on_change=State.set_login_username,
                    width="100%",
                    padding="15px"
                ),
                rx.input(
                    placeholder="Contraseña",
                    type_="password",
                    value=State.login_password,
                    on_change=State.set_login_password,
                    width="100%",
                    padding="15px"
                ),
                rx.button(
                    "Iniciar Sesión",
                    on_click=State.login,
                    background_color="orange",
                    color="white",
                    width="100%",
                    padding="15px"
                ),
                spacing="20px",
                width="400px"
            ),
            rx.text(
                "¿No tienes cuenta? ",
                rx.link("Regístrate aquí", on_click=State.set_page("register"), color="orange"),
                color="gray",
                text_align="center"
            ),
            spacing="30px",
            align_items="center",
            min_height="80vh",
            justify_content="center"
        ),
        max_width="500px",
        margin="0 auto",
        padding="20px"
    )

def register_page() -> rx.Component:
    """Página de registro"""
    return rx.container(
        rx.vstack(
            rx.text("Registrarse", font_size="32px", font_weight="bold", color="white", text_align="center"),
            message_component(),
            rx.vstack(
                rx.input(
                    placeholder="Usuario",
                    value=State.register_username,
                    on_change=State.set_register_username,
                    width="100%",
                    padding="15px"
                ),
                rx.input(
                    placeholder="Email",
                    value=State.register_email,
                    on_change=State.set_register_email,
                    width="100%",
                    padding="15px"
                ),
                rx.input(
                    placeholder="Contraseña",
                    type_="password",
                    value=State.register_password,
                    on_change=State.set_register_password,
                    width="100%",
                    padding="15px"
                ),
                rx.select(
                    ["standard", "moderator"],
                    value=State.register_user_type,
                    on_change=State.set_register_user_type,
                    width="100%",
                    padding="15px"
                ),
                rx.button(
                    "Registrarse",
                    on_click=State.register,
                    background_color="orange",
                    color="white",
                    width="100%",
                    padding="15px"
                ),
                spacing="20px",
                width="400px"
            ),
            rx.text(
                "¿Ya tienes cuenta? ",
                rx.link("Inicia sesión aquí", on_click=State.set_page("login"), color="orange"),
                color="gray",
                text_align="center"
            ),
            spacing="30px",
            align_items="center",
            min_height="80vh",
            justify_content="center"
        ),
        max_width="500px",
        margin="0 auto",
        padding="20px"
    )

def movies_page() -> rx.Component:
    """Página de películas"""
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.text("Películas", font_size="32px", font_weight="bold", color="white"),
                rx.cond(
                    State.user_type == "moderator",
                    rx.button(
                        "Agregar Película",
                        on_click=State.toggle_add_movie_modal,
                        background_color="orange",
                        color="white"
                    )
                ),
                justify_content="space_between",
                width="100%"
            ),
            
            # Filtros
            rx.hstack(
                rx.input(placeholder="Buscar películas...", width="300px"),
                rx.select(["Todos", "Acción", "Drama", "Comedia", "Sci-Fi"], placeholder="Género", width="150px"),
                rx.select(["Todos", "2024", "2023", "2022", "2021"], placeholder="Año", width="150px"),
                spacing="15px"
            ),
            
            message_component(),
            
            # Grid de películas
            rx.box(
                rx.foreach(State.movies, movie_card),
                display="grid",
                grid_template_columns="repeat(auto-fill, minmax(200px, 1fr))",
                gap="20px",
                width="100%"
            ),
            
            spacing="30px",
            width="100%"
        ),
        max_width="1200px",
        margin="0 auto",
        padding="20px"
    )

def series_page() -> rx.Component:
    """Página de series"""
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.text("Series", font_size="32px", font_weight="bold", color="white"),
                rx.cond(
                    State.user_type == "moderator",
                    rx.button(
                        "Agregar Serie",
                        on_click=State.toggle_add_series_modal,
                        background_color="orange",
                        color="white"
                    )
                ),
                justify_content="space_between",
                width="100%"
            ),
            
            # Filtros
            rx.hstack(
                rx.input(placeholder="Buscar series...", width="300px"),
                rx.select(["Todos", "Drama", "Comedia", "Sci-Fi", "Thriller"], placeholder="Género", width="150px"),
                rx.select(["Todas", "En emisión", "Finalizada"], placeholder="Estado", width="150px"),
                spacing="15px"
            ),
            
            message_component(),
            
            # Grid de series
            rx.box(
                rx.foreach(State.series, series_card),
                display="grid",
                grid_template_columns="repeat(auto-fill, minmax(200px, 1fr))",
                gap="20px",
                width="100%"
            ),
            
            spacing="30px",
            width="100%"
        ),
        max_width="1200px",
        margin="0 auto",
        padding="20px"
    )

def novedades_page() -> rx.Component:
    """Página de novedades"""
    return rx.container(
        rx.vstack(
            rx.text("Novedades", font_size="32px", font_weight="bold", color="white"),
            
            rx.vstack(
                rx.box(
                    rx.vstack(
                        rx.text("🎬 Dune: Parte Dos arrasa en taquilla", font_size="20px", font_weight="bold", color="white"),
                        rx.text("La secuela de Denis Villeneuve supera todas las expectativas...", color="gray"),
                        rx.text("Hace 2 horas", font_size="12px", color="orange"),
                        spacing="10px",
                        align_items="start"
                    ),
                    padding="20px",
                    background_color="rgba(255, 255, 255, 0.05)",
                    border_radius="10px",
                    width="100%"
                ),
                
                rx.box(
                    rx.vstack(
                        rx.text("📺 House of the Dragon renovada para tercera temporada", font_size="20px", font_weight="bold", color="white"),
                        rx.text("HBO confirma la continuación de la exitosa serie...", color="gray"),
                        rx.text("Hace 5 horas", font_size="12px", color="orange"),
                        spacing="10px",
                        align_items="start"
                    ),
                    padding="20px",
                    background_color="rgba(255, 255, 255, 0.05)",
                    border_radius="10px",
                    width="100%"
                ),
                
                rx.box(
                    rx.vstack(
                        rx.text("🏆 Nominaciones a los Oscar 2024", font_size="20px", font_weight="bold", color="white"),
                        rx.text("Oppenheimer lidera las nominaciones con 13 categorías...", color="gray"),
                        rx.text("Hace 1 día", font_size="12px", color="orange"),
                        spacing="10px",
                        align_items="start"
                    ),
                    padding="20px",
                    background_color="rgba(255, 255, 255, 0.05)",
                    border_radius="10px",
                    width="100%"
                ),
                
                spacing="20px",
                width="100%"
            ),
            
            spacing="30px",
            width="100%"
        ),
        max_width="800px",
        margin="0 auto",
        padding="20px"
    )

def foro_page() -> rx.Component:
    """Página del foro"""
    return rx.container(
        rx.vstack(
            rx.text("Foro de Discusión", font_size="32px", font_weight="bold", color="white"),
            
            # Categorías
            rx.hstack(
                rx.box(
                    rx.vstack(
                        rx.text("🎬 Películas", font_size="18px", font_weight="bold", color="white"),
                        rx.text("1,234 discusiones", color="gray"),
                        spacing="5px"
                    ),
                    padding="20px",
                    background_color="rgba(255, 255, 255, 0.05)",
                    border_radius="10px",
                    width="200px",
                    cursor="pointer"
                ),
                
                rx.box(
                    rx.vstack(
                        rx.text("📺 Series", font_size="18px", font_weight="bold", color="white"),
                        rx.text("856 discusiones", color="gray"),
                        spacing="5px"
                    ),
                    padding="20px",
                    background_color="rgba(255, 255, 255, 0.05)",
                    border_radius="10px",
                    width="200px",
                    cursor="pointer"
                ),
                
                rx.box(
                    rx.vstack(
                        rx.text("🎭 General", font_size="18px", font_weight="bold", color="white"),
                        rx.text("432 discusiones", color="gray"),
                        spacing="5px"
                    ),
                    padding="20px",
                    background_color="rgba(255, 255, 255, 0.05)",
                    border_radius="10px",
                    width="200px",
                    cursor="pointer"
                ),
                
                spacing="20px"
            ),
            
            # Discusiones recientes
            rx.text("Discusiones Recientes", font_size="24px", font_weight="bold", color="white"),
            
            rx.vstack(
                rx.box(
                    rx.hstack(
                        rx.vstack(
                            rx.text("¿Qué opinan de Dune: Parte Dos?", font_size="16px", font_weight="bold", color="white"),
                            rx.text("Por CineFan2024 • Hace 2 horas", font_size="12px", color="gray"),
                            spacing="5px",
                            align_items="start"
                        ),
                        rx.vstack(
                            rx.text("45", font_size="16px", font_weight="bold", color="orange"),
                            rx.text("respuestas", font_size="12px", color="gray"),
                            spacing="2px",
                            align_items="center"
                        ),
                        justify_content="space_between",
                        width="100%"
                    ),
                    padding="20px",
                    background_color="rgba(255, 255, 255, 0.05)",
                    border_radius="10px",
                    width="100%"
                ),
                
                rx.box(
                    rx.hstack(
                        rx.vstack(
                            rx.text("Mejores series de 2024", font_size="16px", font_weight="bold", color="white"),
                            rx.text("Por SerieAdicto • Hace 4 horas", font_size="12px", color="gray"),
                            spacing="5px",
                            align_items="start"
                        ),
                        rx.vstack(
                            rx.text("23", font_size="16px", font_weight="bold", color="orange"),
                            rx.text("respuestas", font_size="12px", color="gray"),
                            spacing="2px",
                            align_items="center"
                        ),
                        justify_content="space_between",
                        width="100%"
                    ),
                    padding="20px",
                    background_color="rgba(255, 255, 255, 0.05)",
                    border_radius="10px",
                    width="100%"
                ),
                
                spacing="15px",
                width="100%"
            ),
            
            spacing="30px",
            width="100%"
        ),
        max_width="800px",
        margin="0 auto",
        padding="20px"
    )

def top10_page() -> rx.Component:
    """Página de Top 10"""
    return rx.container(
        rx.vstack(
            rx.text("Top 10", font_size="32px", font_weight="bold", color="white"),
            
            rx.hstack(
                rx.button("Películas", background_color="orange", color="white"),
                rx.button("Series", variant="outline", color="white"),
                spacing="10px"
            ),
            
            rx.vstack(
                *[
                    rx.box(
                        rx.hstack(
                            rx.text(f"{i+1}", font_size="24px", font_weight="bold", color="orange", width="40px"),
                            rx.box(
                                rx.text("🎬", font_size="30px"),
                                width="50px",
                                height="50px",
                                background_color="rgba(255, 255, 255, 0.1)",
                                border_radius="5px",
                                display="flex",
                                align_items="center",
                                justify_content="center"
                            ),
                            rx.vstack(
                                rx.text(movie["title"], font_size="16px", font_weight="bold", color="white"),
                                rx.text(f"{movie['year']} • {movie['genre']}", font_size="12px", color="gray"),
                                spacing="2px",
                                align_items="start"
                            ),
                            star_rating(movie["imdb_rating"]),
                            justify_content="space_between",
                            align_items="center",
                            width="100%"
                        ),
                        padding="20px",
                        background_color="rgba(255, 255, 255, 0.05)",
                        border_radius="10px",
                        width="100%"
                    )
                    for i, movie in enumerate([
                        {"title": "Dune: Parte Dos", "year": 2024, "genre": "Sci-Fi", "imdb_rating": 8.8},
                        {"title": "Oppenheimer", "year": 2023, "genre": "Drama", "imdb_rating": 8.4},
                        {"title": "Spider-Man: No Way Home", "year": 2021, "genre": "Acción", "imdb_rating": 8.2},
                        {"title": "Top Gun: Maverick", "year": 2022, "genre": "Acción", "imdb_rating": 8.3},
                        {"title": "The Batman", "year": 2022, "genre": "Acción", "imdb_rating": 7.8},
                        {"title": "Avatar: El Camino del Agua", "year": 2022, "genre": "Sci-Fi", "imdb_rating": 7.6},
                        {"title": "Everything Everywhere All at Once", "year": 2022, "genre": "Sci-Fi", "imdb_rating": 7.8},
                        {"title": "Bullet Train", "year": 2022, "genre": "Acción", "imdb_rating": 7.3},
                        {"title": "Elvis", "year": 2022, "genre": "Drama", "imdb_rating": 7.3},
                        {"title": "The Northman", "year": 2022, "genre": "Drama", "imdb_rating": 7.0}
                    ][:10])
                ],
                spacing="10px",
                width="100%"
            ),
            
            spacing="30px",
            width="100%"
        ),
        max_width="800px",
        margin="0 auto",
        padding="20px"
    )

def inicio_page() -> rx.Component:
    """Página de inicio"""
    return rx.container(
        rx.vstack(
            # Hero section
            rx.box(
                rx.vstack(
                    rx.text("🍿 PopcornHour", font_size="48px", font_weight="bold", color="orange", text_align="center"),
                    rx.text("Tu portal para descubrir, calificar y discutir películas y series", font_size="20px", color="gray", text_align="center"),
                    
                    rx.cond(
                        State.is_authenticated,
                        rx.vstack(
                            rx.text(f"¡Bienvenido de vuelta!", font_size="24px", color="white", text_align="center"),
                            
                            # Panel de moderador
                            rx.cond(
                                State.user_type == "moderator",
                                rx.box(
                                    rx.vstack(
                                        rx.text("👑 Panel de Moderador", font_size="20px", font_weight="bold", color="orange"),
                                        rx.hstack(
                                            rx.button("Agregar Película", on_click=State.toggle_add_movie_modal, background_color="orange", color="white"),
                                            rx.button("Agregar Serie", on_click=State.toggle_add_series_modal, background_color="orange", color="white"),
                                            rx.button("Moderar Contenido", background_color="orange", color="white"),
                                            spacing="15px"
                                        ),
                                        spacing="15px"
                                    ),
                                    padding="20px",
                                    background_color="rgba(255, 165, 0, 0.1)",
                                    border_radius="10px",
                                    border="1px solid orange",
                                    width="100%"
                                )
                            ),
                            spacing="20px"
                        ),
                        rx.hstack(
                            rx.button("Explorar Películas", on_click=State.set_page("peliculas"), background_color="orange", color="white", padding="15px 30px"),
                            rx.button("Ver Series", on_click=State.set_page("series"), variant="outline", color="white", padding="15px 30px"),
                            spacing="20px"
                        )
                    ),
                    
                    spacing="20px",
                    align_items="center"
                ),
                padding="60px 20px",
                text_align="center"
            ),
            
            message_component(),
            
            # Películas destacadas
            rx.vstack(
                rx.text("🎬 Películas Destacadas", font_size="28px", font_weight="bold", color="white"),
                rx.box(
                    rx.foreach(State.movies.slice(0, 6), movie_card),
                    display="grid",
                    grid_template_columns="repeat(auto-fit, minmax(200px, 1fr))",
                    gap="20px",
                    width="100%"
                ),
                spacing="20px",
                width="100%"
            ),
            
            # Series destacadas
            rx.vstack(
                rx.text("📺 Series Destacadas", font_size="28px", font_weight="bold", color="white"),
                rx.box(
                    rx.foreach(State.series.slice(0, 6), series_card),
                    display="grid",
                    grid_template_columns="repeat(auto-fit, minmax(200px, 1fr))",
                    gap="20px",
                    width="100%"
                ),
                spacing="20px",
                width="100%"
            ),
            
            # Reseñas recientes
            rx.vstack(
                rx.text("💬 Reseñas Recientes", font_size="28px", font_weight="bold", color="white"),
                rx.foreach(State.reviews, review_card),
                spacing="20px",
                width="100%"
            ),
            
            spacing="40px",
            width="100%"
        ),
        max_width="1200px",
        margin="0 auto",
        padding="20px"
    )

def main_content() -> rx.Component:
    """Contenido principal basado en la página actual"""
    return rx.cond(
        State.current_page == "login",
        login_page(),
        rx.cond(
            State.current_page == "register",
            register_page(),
            rx.cond(
                State.current_page == "peliculas",
                movies_page(),
                rx.cond(
                    State.current_page == "series",
                    series_page(),
                    rx.cond(
                        State.current_page == "novedades",
                        novedades_page(),
                        rx.cond(
                            State.current_page == "foro",
                            foro_page(),
                            rx.cond(
                                State.current_page == "top10",
                                top10_page(),
                                inicio_page()
                            )
                        )
                    )
                )
            )
        )
    )

def index() -> rx.Component:
    """Página principal de la aplicación"""
    return rx.box(
        navbar(),
        main_content(),
        add_movie_modal(),
        add_series_modal(),
        background="linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
        min_height="100vh",
        color="white"
    )

# Configuración de la aplicación
app = rx.App(
    state=State,
    style={
        "font_family": "Inter, sans-serif",
        "background_color": "#1a1a2e"
    }
)

app.add_page(index, route="/", on_load=State.on_load)