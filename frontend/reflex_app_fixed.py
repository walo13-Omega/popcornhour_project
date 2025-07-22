"""
PopcornHour - Aplicación Frontend con Reflex
Portal web para recomendar, calificar y discutir películas y series
"""

import reflex as rx
import httpx
import asyncio
from typing import List, Dict, Optional
import json

# Configuración de la API backend
API_BASE_URL = "http://localhost:3001/api"

class State(rx.State):
    """Estado global de la aplicación."""
    
    # Estado de autenticación
    is_authenticated: bool = False
    current_user: Dict = {}
    auth_token: str = ""
    
    # Estado de contenido
    movies: List[Dict] = []
    series: List[Dict] = []
    reviews: List[Dict] = []
    forum_discussions: List[Dict] = []
    
    # Estado de UI
    current_page: str = "home"
    loading: bool = False
    error_message: str = ""
    success_message: str = ""
    
    # Formularios
    login_username: str = ""
    login_password: str = ""
    register_username: str = ""
    register_email: str = ""
    register_password: str = ""
    search_query: str = ""
    
    async def check_auth_status(self):
        """Verificar el estado de autenticación del usuario."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE_URL}/auth/me")
                if response.status_code == 200:
                    data = response.json()
                    self.is_authenticated = True
                    self.current_user = data["user"]
                else:
                    self.is_authenticated = False
                    self.current_user = {}
        except Exception as e:
            print(f"Error checking auth status: {e}")
            self.is_authenticated = False
    
    async def login(self):
        """Iniciar sesión del usuario."""
        self.loading = True
        self.error_message = ""
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_BASE_URL}/auth/login",
                    json={
                        "username": self.login_username,
                        "password": self.login_password
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.is_authenticated = True
                    self.current_user = data["user"]
                    self.success_message = "Inicio de sesión exitoso"
                    self.current_page = "home"
                    # Limpiar formulario
                    self.login_username = ""
                    self.login_password = ""
                else:
                    error_data = response.json()
                    self.error_message = error_data.get("error", "Error en el inicio de sesión")
                    
        except Exception as e:
            self.error_message = f"Error de conexión: {str(e)}"
        
        self.loading = False
    
    async def register(self):
        """Registrar nuevo usuario."""
        self.loading = True
        self.error_message = ""
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_BASE_URL}/auth/register",
                    json={
                        "username": self.register_username,
                        "email": self.register_email,
                        "password": self.register_password
                    }
                )
                
                if response.status_code == 201:
                    data = response.json()
                    self.is_authenticated = True
                    self.current_user = data["user"]
                    self.success_message = "Registro exitoso"
                    self.current_page = "home"
                    # Limpiar formulario
                    self.register_username = ""
                    self.register_email = ""
                    self.register_password = ""
                else:
                    error_data = response.json()
                    self.error_message = error_data.get("error", "Error en el registro")
                    
        except Exception as e:
            self.error_message = f"Error de conexión: {str(e)}"
        
        self.loading = False
    
    async def logout(self):
        """Cerrar sesión del usuario."""
        try:
            async with httpx.AsyncClient() as client:
                await client.post(f"{API_BASE_URL}/auth/logout")
        except Exception as e:
            print(f"Error during logout: {e}")
        
        self.is_authenticated = False
        self.current_user = {}
        self.current_page = "home"
        self.success_message = "Sesión cerrada exitosamente"
    
    async def load_movies(self):
        """Cargar películas desde la API."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE_URL}/movies")
                if response.status_code == 200:
                    self.movies = response.json()
        except Exception as e:
            print(f"Error loading movies: {e}")
    
    async def load_series(self):
        """Cargar series desde la API."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE_URL}/series")
                if response.status_code == 200:
                    self.series = response.json()
        except Exception as e:
            print(f"Error loading series: {e}")
    
    async def load_reviews(self):
        """Cargar reseñas desde la API."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE_URL}/reviews")
                if response.status_code == 200:
                    self.reviews = response.json()
        except Exception as e:
            print(f"Error loading reviews: {e}")
    
    async def load_forum_discussions(self):
        """Cargar discusiones del foro desde la API."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE_URL}/forum/discussions")
                if response.status_code == 200:
                    self.forum_discussions = response.json()
        except Exception as e:
            print(f"Error loading forum discussions: {e}")
    
    def set_page(self, page: str):
        """Cambiar la página actual."""
        self.current_page = page
        self.error_message = ""
        self.success_message = ""
    
    def clear_messages(self):
        """Limpiar mensajes de error y éxito."""
        self.error_message = ""
        self.success_message = ""


def navbar() -> rx.Component:
    """Componente de navegación."""
    return rx.hstack(
        # Logo
        rx.hstack(
            rx.text("🍿", font_size="2em"),
            rx.heading("PopcornHour", size="lg", color="orange"),
            spacing="2",
        ),
        
        # Enlaces de navegación
        rx.hstack(
            rx.button("Inicio", on_click=State.set_page("home"), color="white", variant="ghost"),
            rx.button("Películas", on_click=State.set_page("movies"), color="white", variant="ghost"),
            rx.button("Series", on_click=State.set_page("series"), color="white", variant="ghost"),
            rx.button("Novedades", on_click=State.set_page("news"), color="white", variant="ghost"),
            rx.button("Foro", on_click=State.set_page("forum"), color="white", variant="ghost"),
            rx.button("Top 10", on_click=State.set_page("top10"), color="white", variant="ghost"),
            spacing="4",
        ),
        
        # Buscador y usuario
        rx.hstack(
            rx.input(
                placeholder="Buscar...",
                value=State.search_query,
                on_change=State.set_search_query,
                bg="gray.700",
                border="none",
                color="white",
                width="200px",
            ),
            rx.cond(
                State.is_authenticated,
                rx.hstack(
                    rx.text(f"Hola, {State.current_user.get('username', '')}", color="white"),
                    rx.button("Cerrar Sesión", on_click=State.logout, bg="red.500"),
                    spacing="2",
                ),
                rx.hstack(
                    rx.button("Iniciar Sesión", on_click=State.set_page("login"), bg="orange.500"),
                    rx.button("Registrarse", on_click=State.set_page("register"), bg="green.500"),
                    spacing="2",
                ),
            ),
            spacing="4",
        ),
        
        justify="between",
        align="center",
        width="100%",
        padding="4",
        bg="gray.900",
        position="sticky",
        top="0",
        z_index="1000",
    )


def error_message_component() -> rx.Component:
    """Componente para mostrar mensajes de error."""
    return rx.cond(
        State.error_message != "",
        rx.box(
            rx.text(State.error_message, color="red.400"),
            bg="red.100",
            border="1px solid red",
            border_radius="md",
            padding="3",
            margin_bottom="4",
        ),
    )


def success_message_component() -> rx.Component:
    """Componente para mostrar mensajes de éxito."""
    return rx.cond(
        State.success_message != "",
        rx.box(
            rx.text(State.success_message, color="green.400"),
            bg="green.100",
            border="1px solid green",
            border_radius="md",
            padding="3",
            margin_bottom="4",
        ),
    )


def login_page() -> rx.Component:
    """Página de inicio de sesión."""
    return rx.center(
        rx.vstack(
            rx.heading("Iniciar Sesión", size="xl", color="white", margin_bottom="6"),
            
            error_message_component(),
            
            rx.vstack(
                rx.input(
                    placeholder="Usuario o Email",
                    value=State.login_username,
                    on_change=State.set_login_username,
                    bg="gray.700",
                    border="none",
                    color="white",
                    width="300px",
                ),
                rx.input(
                    placeholder="Contraseña",
                    type="password",
                    value=State.login_password,
                    on_change=State.set_login_password,
                    bg="gray.700",
                    border="none",
                    color="white",
                    width="300px",
                ),
                rx.button(
                    "Iniciar Sesión",
                    on_click=State.login,
                    bg="orange.500",
                    color="white",
                    width="300px",
                    loading=State.loading,
                ),
                spacing="4",
            ),
            
            rx.text(
                "¿No tienes cuenta? ",
                rx.button("Regístrate aquí", on_click=State.set_page("register"), color="orange.400", variant="ghost"),
                color="gray.400",
                margin_top="4",
            ),
            
            spacing="6",
            align="center",
        ),
        height="80vh",
    )


def register_page() -> rx.Component:
    """Página de registro."""
    return rx.center(
        rx.vstack(
            rx.heading("Registrarse", size="xl", color="white", margin_bottom="6"),
            
            error_message_component(),
            
            rx.vstack(
                rx.input(
                    placeholder="Nombre de Usuario",
                    value=State.register_username,
                    on_change=State.set_register_username,
                    bg="gray.700",
                    border="none",
                    color="white",
                    width="300px",
                ),
                rx.input(
                    placeholder="Email",
                    type="email",
                    value=State.register_email,
                    on_change=State.set_register_email,
                    bg="gray.700",
                    border="none",
                    color="white",
                    width="300px",
                ),
                rx.input(
                    placeholder="Contraseña",
                    type="password",
                    value=State.register_password,
                    on_change=State.set_register_password,
                    bg="gray.700",
                    border="none",
                    color="white",
                    width="300px",
                ),
                rx.button(
                    "Registrarse",
                    on_click=State.register,
                    bg="green.500",
                    color="white",
                    width="300px",
                    loading=State.loading,
                ),
                spacing="4",
            ),
            
            rx.text(
                "¿Ya tienes cuenta? ",
                rx.button("Inicia sesión aquí", on_click=State.set_page("login"), color="orange.400", variant="ghost"),
                color="gray.400",
                margin_top="4",
            ),
            
            spacing="6",
            align="center",
        ),
        height="80vh",
    )


def movie_card(movie: Dict) -> rx.Component:
    """Componente de tarjeta de película."""
    return rx.box(
        rx.vstack(
            rx.image(
                src=movie.get("poster_url", "/placeholder.jpg"),
                alt=movie.get("title", ""),
                width="200px",
                height="300px",
                object_fit="cover",
                border_radius="lg",
            ),
            rx.vstack(
                rx.heading(movie.get("title", ""), size="sm", color="white"),
                rx.text(f"{movie.get('release_year', '')} • {movie.get('duration_minutes', 0)}min", color="gray.400", font_size="sm"),
                rx.hstack(
                    rx.text("⭐", font_size="16px"),
                    rx.text(str(movie.get("imdb_rating", "N/A")), color="orange", font_weight="bold"),
                    spacing="1",
                ),
                spacing="1",
                align="start",
            ),
            spacing="3",
            align="start",
        ),
        bg="gray.800",
        border_radius="lg",
        padding="4",
        _hover={"transform": "translateY(-5px)", "box_shadow": "lg"},
        transition="all 0.3s",
        cursor="pointer",
    )


def home_page() -> rx.Component:
    """Página principal."""
    return rx.vstack(
        # Hero Section
        rx.box(
            rx.vstack(
                rx.badge("ESTRENO", bg="orange.500", color="black", font_weight="bold"),
                rx.heading("Dune: Parte Dos", size="2xl", color="white"),
                rx.hstack(
                    rx.text("⭐⭐⭐⭐⭐", color="orange"),
                    rx.text("4.5/5 (1,234 votos)", color="gray.300"),
                    spacing="3",
                ),
                rx.text(
                    "Paul Atreides se une a los Fremen y comienza un viaje de venganza contra los conspiradores que destruyeron su familia.",
                    color="gray.300",
                    max_width="600px",
                    text_align="center",
                ),
                rx.hstack(
                    rx.button(
                        "▶️ Ver trailer",
                        bg="orange.500",
                        color="black",
                        font_weight="bold",
                    ),
                    rx.button(
                        "➕ Mi lista",
                        bg="gray.700",
                        color="white",
                        font_weight="bold",
                    ),
                    spacing="4",
                ),
                spacing="4",
                align="center",
            ),
            bg="linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7))",
            height="400px",
            display="flex",
            align_items="center",
            justify_content="center",
            width="100%",
        ),
        
        # Panel de Moderador (solo si es moderador)
        rx.cond(
            State.current_user.get("userType") == "moderator",
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text("👑", font_size="24px"),
                        rx.heading("Panel de Moderador", size="lg", color="white"),
                        rx.spacer(),
                        rx.button("Añadir Contenido", bg="orange.500", color="black"),
                        justify="between",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.box(
                            rx.vstack(
                                rx.heading("Subir Nueva Película", size="md", color="white"),
                                rx.text("Completa los detalles de la película para añadirla al catálogo.", color="gray.400", font_size="sm"),
                                rx.button("Comenzar", color="orange.400", variant="ghost"),
                                spacing="2",
                                align="start",
                            ),
                            bg="gray.700",
                            padding="4",
                            border_radius="lg",
                            flex="1",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.heading("Subir Nueva Serie", size="md", color="white"),
                                rx.text("Añade una nueva serie con temporadas y episodios.", color="gray.400", font_size="sm"),
                                rx.button("Comenzar", color="orange.400", variant="ghost"),
                                spacing="2",
                                align="start",
                            ),
                            bg="gray.700",
                            padding="4",
                            border_radius="lg",
                            flex="1",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.heading("Moderar Contenido", size="md", color="white"),
                                rx.text("Revisa y edita el contenido existente en la plataforma.", color="gray.400", font_size="sm"),
                                rx.button("Revisar", color="orange.400", variant="ghost"),
                                spacing="2",
                                align="start",
                            ),
                            bg="gray.700",
                            padding="4",
                            border_radius="lg",
                            flex="1",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    spacing="4",
                ),
                bg="gray.800",
                padding="6",
                border_radius="lg",
                border_left="4px solid orange",
                margin="6",
            ),
        ),
        
        # Tendencias Ahora
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.heading("Tendencias Ahora", size="lg", color="white"),
                    rx.spacer(),
                    rx.button("Ver todo", color="orange.400", font_weight="semibold", variant="ghost"),
                    justify="between",
                    width="100%",
                ),
                rx.hstack(
                    *[movie_card(movie) for movie in State.movies[:5]] if State.movies else [rx.text("Cargando películas...", color="gray.400")],
                    spacing="4",
                    overflow_x="auto",
                    width="100%",
                ),
                spacing="4",
            ),
            padding="6",
        ),
        
        # Reseñas Recientes
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.heading("Reseñas Recientes", size="lg", color="white"),
                    rx.spacer(),
                    rx.button("Ver todo", color="orange.400", font_weight="semibold", variant="ghost"),
                    justify="between",
                    width="100%",
                ),
                rx.vstack(
                    *[
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("👤", font_size="32px"),
                                    rx.vstack(
                                        rx.text(review.get("username", ""), font_weight="bold", color="white"),
                                        rx.text(f"Hace 2 horas • {review.get('content_title', '')}", color="gray.400", font_size="sm"),
                                        spacing="0",
                                        align="start",
                                    ),
                                    spacing="3",
                                    align="start",
                                ),
                                rx.text(review.get("content", ""), color="gray.300"),
                                rx.hstack(
                                    rx.button(
                                        "👍 124",
                                        variant="ghost",
                                        color="gray.400",
                                        size="sm",
                                    ),
                                    rx.button(
                                        "💬 Responder",
                                        variant="ghost",
                                        color="gray.400",
                                        size="sm",
                                    ),
                                    spacing="4",
                                ),
                                spacing="3",
                                align="start",
                            ),
                            bg="gray.800",
                            padding="4",
                            border_radius="lg",
                            _hover={"bg": "gray.750"},
                            transition="all 0.3s",
                        )
                        for review in State.reviews[:3]
                    ] if State.reviews else [rx.text("No hay reseñas disponibles", color="gray.400")],
                    spacing="4",
                    width="100%",
                ),
                spacing="4",
            ),
            padding="6",
        ),
        
        spacing="0",
        width="100%",
        on_mount=State.load_movies,
    )


def movies_page() -> rx.Component:
    """Página de películas."""
    return rx.vstack(
        rx.heading("Películas", size="xl", color="white", padding="6"),
        
        # Filtros
        rx.hstack(
            rx.input(
                placeholder="Buscar películas...",
                bg="gray.700",
                border="none",
                color="white",
                flex="1",
            ),
            rx.select(
                ["Género", "Acción", "Comedia", "Drama", "Ciencia Ficción", "Terror"],
                placeholder="Género",
                bg="gray.700",
                color="white",
            ),
            rx.select(
                ["Año", "2024", "2023", "2022", "2021"],
                placeholder="Año",
                bg="gray.700",
                color="white",
            ),
            spacing="4",
            padding="6",
            width="100%",
        ),
        
        # Grid de películas
        rx.box(
            rx.grid(
                *[movie_card(movie) for movie in State.movies] if State.movies else [rx.text("No hay películas disponibles", color="gray.400")],
                columns="5",
                spacing="4",
                width="100%",
            ),
            padding="6",
        ),
        
        width="100%",
        on_mount=State.load_movies,
    )


def main_content() -> rx.Component:
    """Contenido principal basado en la página actual."""
    return rx.cond(
        State.current_page == "login",
        login_page(),
        rx.cond(
            State.current_page == "register",
            register_page(),
            rx.cond(
                State.current_page == "movies",
                movies_page(),
                home_page(),  # Página por defecto
            ),
        ),
    )


def index() -> rx.Component:
    """Página principal de la aplicación."""
    return rx.vstack(
        # Mensajes de éxito/error
        success_message_component(),
        
        navbar(),
        main_content(),
        
        spacing="0",
        min_height="100vh",
        bg="linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
        width="100%",
        on_mount=State.check_auth_status,
    )


# Configuración de la aplicación
app = rx.App(
    style={
        "font_family": "Inter, sans-serif",
    }
)

app.add_page(index, route="/")

