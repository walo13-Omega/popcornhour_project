from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'popcornhour_secret')

# Configuración de la API backend
API_BASE_URL = "http://localhost:3001/api"

TMDB_API_KEY = "61c4a7408b169f7b383096a78a0cd7a6"
TMDB_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2MWM0YTc0MDhiMTY5ZjdiMzgzMDk2YTc4YTBjZDdhNiIsIm5iZiI6MTc1MzQ3NDQ4Ni40ODUsInN1YiI6IjY4ODNlNWI2MmQ5MDU1MjU2ZGQ5YTVmOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.jxMwRlz5M5XQbzWrboFu8ElXh2kqyQfChYiJIz7AsKI"

def get_tmdb_poster(title, content_type="movie"):
    base_url = "https://api.themoviedb.org/3/search/"
    url = f"{base_url}{content_type}"
    headers = {"Authorization": f"Bearer {TMDB_TOKEN}"}
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": "es-ES"
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            poster_path = results[0].get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/180x270?text=No+Image"

def get_tmdb_info(title, content_type="movie"):
    base_url = "https://api.themoviedb.org/3/search/"
    url = f"{base_url}{content_type}"
    headers = {"Authorization": f"Bearer {TMDB_TOKEN}"}
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": "es-ES"
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            data = results[0]
            poster_path = data.get("poster_path")
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/180x270?text=No+Image"
            overview = data.get("overview", "")
            release_date = data.get("release_date") or data.get("first_air_date")
            genres = data.get("genre_ids", [])
            vote_average = data.get("vote_average")
            return {
                "poster_url": poster_url,
                "overview": overview,
                "release_date": release_date,
                "genres": genres,
                "vote_average": vote_average
            }
    return {
        "poster_url": "https://via.placeholder.com/180x270?text=No+Image",
        "overview": "",
        "release_date": "",
        "genres": [],
        "vote_average": None
    }

def enrich_movies(movies):
    for m in movies:
        info = get_tmdb_info(m['title'], "movie")
        m['poster_url'] = info['poster_url']
        m['overview'] = info['overview'] or m.get('description', '')
        m['release_date'] = info['release_date']
        m['genres_tmdb'] = info['genres']
        m['vote_average'] = info['vote_average']
    return movies

def enrich_series(series):
    for s in series:
        info = get_tmdb_info(s['title'], "tv")
        s['poster_url'] = info['poster_url']
        s['overview'] = info['overview'] or s.get('description', '')
        s['release_date'] = info['release_date']
        s['genres_tmdb'] = info['genres']
        s['vote_average'] = info['vote_average']
    return series

# Modificar home, movies y series para incluir poster_url
def add_posters_to_movies(movies):
    for m in movies:
        m['poster_url'] = get_tmdb_poster(m['title'], "movie")
    return movies

def add_posters_to_series(series):
    for s in series:
        s['poster_url'] = get_tmdb_poster(s['title'], "tv")
    return series

def moderator_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get('user')
        
        # Debug: Imprimir datos de sesión en rutas protegidas
        print(f"🔍 DEBUG - Ruta protegida por moderador:")
        print(f"  - Usuario en sesión: {user}")
        if user:
            print(f"  - userType: {user.get('userType')}")
            print(f"  - user_type: {user.get('user_type')}")
        
        # Verificar si es moderador (probar ambos campos)
        if not user:
            flash('Debes iniciar sesión para acceder a esta función.', 'danger')
            return redirect(url_for('login'))
        
        user_type = user.get('userType') or user.get('user_type')
        if user_type != 'moderator':
            flash('Acceso solo para moderadores.', 'danger')
            return redirect(url_for('home'))
        
        print(f"  ✅ Acceso permitido para moderador: {user.get('username')}")
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            flash('Debes iniciar sesión para acceder a tu perfil.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Home
@app.route('/')
def home():
    try:
        response = requests.get(f"{API_BASE_URL}/movies")
        if response.status_code == 200:
            movies = response.json()
            movies = enrich_movies(movies[:6])
        else:
            movies = []
    except Exception as e:
        movies = []
        flash(f"Error al cargar películas: {e}", "danger")
    
    user = session.get('user')
    
    # Debug: Imprimir datos de sesión
    print(f"🔍 DEBUG - Datos de sesión:")
    print(f"  - Usuario en sesión: {user}")
    if user:
        print(f"  - user_type: {user.get('user_type')}")
        print(f"  - userType: {user.get('userType')}")
    
    # Verificar si es moderador (probar ambos campos)
    is_moderator = False
    if user:
        user_type = user.get('userType') or user.get('user_type')
        is_moderator = user_type == 'moderator'
        print(f"  - user_type encontrado: '{user_type}'")
        print(f"  - ¿Es moderador?: {is_moderator}")
    
    return render_template('home.html', movies=movies, is_moderator=is_moderator)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Debug: Imprimir la URL que se está intentando acceder
        login_url = f"{API_BASE_URL}/auth/login"
        print(f"🔍 Intentando acceder a: {login_url}")
        print(f"📝 Datos enviados: username={username}, password={'*' * len(password) if password else 'None'}")
        
        try:
            response = requests.post(login_url, json={
                "username": username,
                "password": password
            })
            
            # Debug: Imprimir la respuesta del backend
            print(f"📡 Status Code: {response.status_code}")
            print(f"📡 Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                user_data = data.get('user')
                token = data.get('token')
                
                # Debug: Imprimir datos del usuario
                print(f"🔍 DEBUG - Datos del usuario recibidos:")
                print(f"  - Usuario completo: {user_data}")
                if user_data:
                    print(f"  - userType: {user_data.get('userType')}")
                    print(f"  - user_type: {user_data.get('user_type')}")
                
                session['user'] = user_data
                session['token'] = token  # Guardar el token JWT
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('home'))
            else:
                error = response.json().get('error', 'Error en el inicio de sesión')
                flash(error, 'danger')
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            flash(f"Error de conexión: {e}", 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Debug: Imprimir la URL que se está intentando acceder
        register_url = f"{API_BASE_URL}/auth/register"
        print(f"🔍 Intentando acceder a: {register_url}")
        print(f"📝 Datos enviados: username={username}, email={email}, password={'*' * len(password) if password else 'None'}")
        
        try:
            response = requests.post(register_url, json={
                "username": username,
                "email": email,
                "password": password
            })
            
            # Debug: Imprimir la respuesta del backend
            print(f"📡 Status Code: {response.status_code}")
            print(f"📡 Response: {response.text}")
            
            if response.status_code == 201:
                data = response.json()
                user_data = data.get('user')
                token = data.get('token')
                session['user'] = user_data
                session['token'] = token  # Guardar el token JWT
                flash('Registro exitoso', 'success')
                return redirect(url_for('home'))
            else:
                error = response.json().get('error', 'Error en el registro')
                flash(error, 'danger')
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            flash(f"Error de conexión: {e}", 'danger')
    return render_template('register.html')

# Movies
@app.route('/movies')
def movies():
    search = request.args.get('search', '').strip()
    genre = request.args.get('genre', '').strip()
    year = request.args.get('year', '').strip()
    try:
        response = requests.get(f"{API_BASE_URL}/movies")
        if response.status_code == 200:
            movies = response.json()
        else:
            movies = []
    except Exception as e:
        movies = []
        flash(f"Error al cargar películas: {e}", "danger")
    filtered = []
    for m in movies:
        if search and search.lower() not in m.get('title', '').lower():
            continue
        if genre and genre != 'Todos' and genre.lower() not in m.get('genre', '').lower():
            continue
        if year and year != 'Todos' and str(m.get('release_year', '')) != year:
            continue
        filtered.append(m)
    genres = sorted({m.get('genre', '') for m in movies if m.get('genre', '')})
    years = sorted({str(m.get('release_year', '')) for m in movies if m.get('release_year', '')})
    filtered = enrich_movies(filtered)
    return render_template('movies.html', movies=filtered, search=search, genre=genre, year=year, genres=genres, years=years)

# Series
@app.route('/series')
def series():
    search = request.args.get('search', '').strip()
    genre = request.args.get('genre', '').strip()
    year = request.args.get('year', '').strip()
    try:
        response = requests.get(f"{API_BASE_URL}/series")
        if response.status_code == 200:
            series = response.json()
        else:
            series = []
    except Exception as e:
        series = []
        flash(f"Error al cargar series: {e}", "danger")
    filtered = []
    for s in series:
        if search and search.lower() not in s.get('title', '').lower():
            continue
        if genre and genre != 'Todos' and genre.lower() not in s.get('genre', '').lower():
            continue
        if year and year != 'Todos' and str(s.get('release_year', '')) != year:
            continue
        filtered.append(s)
    genres = sorted({s.get('genre', '') for s in series if s.get('genre', '')})
    years = sorted({str(s.get('release_year', '')) for s in series if s.get('release_year', '')})
    filtered = enrich_series(filtered)
    return render_template('series.html', series=filtered, search=search, genre=genre, year=year, genres=genres, years=years)

@app.route('/foro')
def foro():
    try:
        response = requests.get(f"{API_BASE_URL}/forum/discussions")
        if response.status_code == 200:
            discussions = response.json()
            # Buscar poster para cada discusión según categoría
            for d in discussions:
                if d.get('category') == 'movies':
                    d['poster_url'] = get_tmdb_poster(d.get('title', ''), 'movie')
                elif d.get('category') == 'series':
                    d['poster_url'] = get_tmdb_poster(d.get('title', ''), 'tv')
                else:
                    d['poster_url'] = None
        else:
            discussions = []
    except Exception as e:
        discussions = []
        flash(f"Error al cargar discusiones: {e}", "danger")
    return render_template('foro.html', discussions=discussions)

# Top 10
@app.route('/top10')
def top10():
    try:
        response = requests.get(f"{API_BASE_URL}/movies")
        if response.status_code == 200:
            movies = response.json()
            top_movies = sorted(movies, key=lambda m: m.get('imdb_rating', 0), reverse=True)[:10]
            top_movies = add_posters_to_movies(top_movies)
        else:
            top_movies = []
    except Exception as e:
        top_movies = []
        flash(f"Error al cargar top 10: {e}", "danger")
    return render_template('top10.html', movies=top_movies)

@app.route('/novedades')
def novedades():
    return render_template('novedades.html')

@app.route('/add_movie', methods=['GET', 'POST'])
@moderator_required
def add_movie():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        imdb_rating = request.form.get('imdb_rating')
        genres = request.form.get('genres')
        release_year = request.form.get('release_year')
        data = {
            "title": title,
            "description": description,
            "imdb_rating": imdb_rating,
            "genres": genres,
            "release_year": int(release_year),
            "created_by": session['user']['id']
        }
        token = session.get('token')
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        try:
            resp = requests.post(f"{API_BASE_URL}/movies", json=data, headers=headers)
            print("DEBUG add_movie:", resp.status_code, resp.text)  # Debug
            if resp.status_code == 201:
                flash('Película agregada exitosamente.', 'success')
                return redirect(url_for('movies'))
            else:
                flash(resp.json().get('error', 'Error al agregar la película.'), 'danger')
        except Exception as e:
            flash(f"Error de conexión: {e}", 'danger')
    return render_template('add_movie.html')

@app.route('/add_series', methods=['GET', 'POST'])
@moderator_required
def add_series():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        imdb_rating = request.form.get('imdb_rating')
        genres = request.form.get('genres')
        release_year = request.form.get('release_year')
        data = {
            "title": title,
            "description": description,
            "imdb_rating": imdb_rating,
            "genres": genres,
            "release_year": int(release_year),
            "created_by": session['user']['id']
        }
        token = session.get('token')
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        try:
            resp = requests.post(f"{API_BASE_URL}/series", json=data, headers=headers)
            print("DEBUG add_series:", resp.status_code, resp.text)  # Debug
            if resp.status_code == 201:
                flash('Serie agregada exitosamente.', 'success')
                return redirect(url_for('series'))
            else:
                flash(resp.json().get('error', 'Error al agregar la serie.'), 'danger')
        except Exception as e:
            flash(f"Error de conexión: {e}", 'danger')
    return render_template('add_series.html')

@app.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    # Obtener detalles de la película
    try:
        response = requests.get(f"{API_BASE_URL}/movies/{movie_id}")
        if response.status_code == 200:
            movie = response.json()
            # Enriquecer con datos de TMDb
            if movie:
                tmdb_info = get_tmdb_info(movie['title'], 'movie')
                if tmdb_info:
                    movie.update(tmdb_info)
        else:
            movie = None
    except Exception as e:
        movie = None
        flash(f"Error al cargar película: {e}", "danger")
    # Obtener reseñas
    reviews = []
    try:
        r = requests.get(f"{API_BASE_URL}/reviews?content_type=movie&content_id={movie_id}")
        if r.status_code == 200:
            reviews = r.json()
    except Exception:
        pass
    # Agregar reseña
    if request.method == 'POST' and session.get('user'):
        content = request.form.get('content')
        rating = request.form.get('rating')
        try:
            # Obtener token de la sesión
            token = session.get('token')
            headers = {}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            
            resp = requests.post(f"{API_BASE_URL}/reviews", 
                json={
                    "content_type": "movie",
                    "content_id": movie_id,
                    "rating": float(rating),
                    "comment": content
                },
                headers=headers
            )
            if resp.status_code in (200, 201):
                flash('Reseña agregada exitosamente.', 'success')
                return redirect(url_for('movie_detail', movie_id=movie_id))
            else:
                error = resp.json().get('error', 'Error al agregar reseña')
                flash(error, 'danger')
        except Exception as e:
            flash(f"Error de conexión: {e}", 'danger')
    return render_template('movie_detail.html', movie=movie, reviews=reviews)

@app.route('/series/<int:series_id>', methods=['GET', 'POST'])
def series_detail(series_id):
    # Obtener detalles de la serie
    try:
        response = requests.get(f"{API_BASE_URL}/series/{series_id}")
        if response.status_code == 200:
            series = response.json()
            # Enriquecer con datos de TMDb
            if series:
                tmdb_info = get_tmdb_info(series['title'], 'tv')
                if tmdb_info:
                    series.update(tmdb_info)
        else:
            series = None
    except Exception as e:
        series = None
        flash(f"Error al cargar serie: {e}", "danger")
    # Obtener reseñas
    reviews = []
    try:
        r = requests.get(f"{API_BASE_URL}/reviews?content_type=series&content_id={series_id}")
        if r.status_code == 200:
            reviews = r.json()
    except Exception:
        pass
    # Agregar reseña
    if request.method == 'POST' and session.get('user'):
        content = request.form.get('content')
        rating = request.form.get('rating')
        try:
            # Obtener token de la sesión
            token = session.get('token')
            headers = {}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            
            resp = requests.post(f"{API_BASE_URL}/reviews", 
                json={
                    "content_type": "series",
                    "content_id": series_id,
                    "rating": float(rating),
                    "comment": content
                },
                headers=headers
            )
            if resp.status_code in (200, 201):
                flash('Reseña agregada exitosamente.', 'success')
                return redirect(url_for('series_detail', series_id=series_id))
            else:
                error = resp.json().get('error', 'Error al agregar reseña')
                flash(error, 'danger')
        except Exception as e:
            flash(f"Error de conexión: {e}", 'danger')
    return render_template('series_detail.html', series=series, reviews=reviews)

@app.route('/admin_content')
@moderator_required
def admin_content():
    # Obtener películas
    try:
        movies_resp = requests.get(f"{API_BASE_URL}/movies")
        movies = movies_resp.json() if movies_resp.status_code == 200 else []
    except Exception:
        movies = []
    # Obtener series
    try:
        series_resp = requests.get(f"{API_BASE_URL}/series")
        series = series_resp.json() if series_resp.status_code == 200 else []
    except Exception:
        series = []
    return render_template('admin_content.html', movies=movies, series=series)

@app.route('/delete_movie/<int:movie_id>')
@moderator_required
def delete_movie(movie_id):
    token = session.get('token')
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    try:
        resp = requests.delete(f"{API_BASE_URL}/movies/{movie_id}", headers=headers)
        print("DEBUG delete_movie:", resp.status_code, resp.text)
        if resp.status_code == 200:
            flash('Película eliminada exitosamente.', 'success')
        else:
            flash(resp.json().get('error', 'Error al eliminar la película.'), 'danger')
    except Exception as e:
        flash(f"Error de conexión: {e}", 'danger')
    return redirect(url_for('admin_content'))

@app.route('/delete_series/<int:series_id>')
@moderator_required
def delete_series(series_id):
    token = session.get('token')
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    try:
        resp = requests.delete(f"{API_BASE_URL}/series/{series_id}", headers=headers)
        print("DEBUG delete_series:", resp.status_code, resp.text)
        if resp.status_code == 200:
            flash('Serie eliminada exitosamente.', 'success')
        else:
            flash(resp.json().get('error', 'Error al eliminar la serie.'), 'danger')
    except Exception as e:
        flash(f"Error de conexión: {e}", 'danger')
    return redirect(url_for('admin_content'))

@app.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
@moderator_required
def edit_movie(movie_id):
    # Obtener datos actuales
    try:
        resp = requests.get(f"{API_BASE_URL}/movies/{movie_id}")
        if resp.status_code == 200:
            movie = resp.json()
        else:
            flash('Película no encontrada.', 'danger')
            return redirect(url_for('admin_content'))
    except Exception as e:
        flash(f"Error de conexión: {e}", 'danger')
        return redirect(url_for('admin_content'))
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        release_year = request.form.get('release_year')
        duration_minutes = request.form.get('duration_minutes')
        genre = request.form.get('genre')
        imdb_rating = request.form.get('imdb_rating')
        poster_url = request.form.get('poster_url')
        data = {
            "title": title,
            "description": description,
            "release_year": int(release_year) if release_year else None,
            "duration_minutes": int(duration_minutes) if duration_minutes else None,
            "genre": genre,
            "imdb_rating": imdb_rating,
            "poster_url": poster_url
        }
        token = session.get('token')
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        try:
            update_resp = requests.put(f"{API_BASE_URL}/movies/{movie_id}", json=data, headers=headers)
            print("DEBUG edit_movie:", update_resp.status_code, update_resp.text)
            if update_resp.status_code == 200:
                flash('Película actualizada exitosamente.', 'success')
                return redirect(url_for('admin_content'))
            else:
                flash(update_resp.json().get('error', 'Error al actualizar la película.'), 'danger')
        except Exception as e:
            flash(f"Error de conexión: {e}", 'danger')
    return render_template('edit_movie.html', movie=movie)

@app.route('/edit_series/<int:series_id>', methods=['GET', 'POST'])
@moderator_required
def edit_series(series_id):
    # Obtener datos actuales
    try:
        resp = requests.get(f"{API_BASE_URL}/series/{series_id}")
        if resp.status_code == 200:
            series = resp.json()
        else:
            flash('Serie no encontrada.', 'danger')
            return redirect(url_for('admin_content'))
    except Exception as e:
        flash(f"Error de conexión: {e}", 'danger')
        return redirect(url_for('admin_content'))
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        release_year = request.form.get('release_year')
        duration_minutes = request.form.get('duration_minutes')
        genre = request.form.get('genre')
        imdb_rating = request.form.get('imdb_rating')
        poster_url = request.form.get('poster_url')
        data = {
            "title": title,
            "description": description,
            "release_year": int(release_year) if release_year else None,
            "duration_minutes": int(duration_minutes) if duration_minutes else None,
            "genre": genre,
            "imdb_rating": imdb_rating,
            "poster_url": poster_url
        }
        token = session.get('token')
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        try:
            update_resp = requests.put(f"{API_BASE_URL}/series/{series_id}", json=data, headers=headers)
            print("DEBUG edit_series:", update_resp.status_code, update_resp.text)
            if update_resp.status_code == 200:
                flash('Serie actualizada exitosamente.', 'success')
                return redirect(url_for('admin_content'))
            else:
                flash(update_resp.json().get('error', 'Error al actualizar la serie.'), 'danger')
        except Exception as e:
            flash(f"Error de conexión: {e}", 'danger')
    return render_template('edit_series.html', series=series)

@app.route('/delete_review/<int:review_id>/<string:content_type>/<int:content_id>', methods=['POST'])
@login_required
def delete_review(review_id, content_type, content_id):
    user = session.get('user')
    token = session.get('token')
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    # Obtener la reseña para verificar permisos
    try:
        resp = requests.get(f"{API_BASE_URL}/reviews/{review_id}", headers=headers)
        if resp.status_code == 200:
            review = resp.json()
        else:
            flash('Reseña no encontrada.', 'danger')
            return redirect(url_for('home'))
    except Exception as e:
        flash(f"Error de conexión: {e}", 'danger')
        return redirect(url_for('home'))
    # Permiso: autor o moderador
    if not user or (user['id'] != review.get('user_id') and user.get('user_type') != 'moderator'):
        flash('No tienes permiso para eliminar esta reseña.', 'danger')
        return redirect(url_for('home'))
    # Eliminar
    try:
        del_resp = requests.delete(f"{API_BASE_URL}/reviews/{review_id}", headers=headers)
        if del_resp.status_code == 200:
            flash('Reseña eliminada exitosamente.', 'success')
        else:
            flash('Error al eliminar la reseña.', 'danger')
    except Exception as e:
        flash(f"Error de conexión: {e}", 'danger')
    # Redirigir a la página de detalles
    if content_type == 'movie':
        return redirect(url_for('movie_detail', movie_id=content_id))
    else:
        return redirect(url_for('series_detail', series_id=content_id))

@app.route('/edit_review/<int:review_id>/<string:content_type>/<int:content_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id, content_type, content_id):
    user = session.get('user')
    token = session.get('token')
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    # Obtener la reseña para verificar permisos
    try:
        resp = requests.get(f"{API_BASE_URL}/reviews/{review_id}", headers=headers)
        if resp.status_code == 200:
            review = resp.json()
        else:
            flash('Reseña no encontrada.', 'danger')
            return redirect(url_for('home'))
    except Exception as e:
        flash(f"Error de conexión: {e}", 'danger')
        return redirect(url_for('home'))
    # Permiso: autor o moderador
    if not user or (user['id'] != review.get('user_id') and user.get('user_type') != 'moderator'):
        flash('No tienes permiso para editar esta reseña.', 'danger')
        return redirect(url_for('home'))
    # Editar
    if request.method == 'POST':
        content = request.form.get('content')
        rating = request.form.get('rating')
        try:
            update_resp = requests.put(f"{API_BASE_URL}/reviews/{review_id}", json={
                "content": content,
                "rating": float(rating)
            }, headers=headers)
            if update_resp.status_code == 200:
                flash('Reseña actualizada exitosamente.', 'success')
            else:
                flash('Error al actualizar la reseña.', 'danger')
        except Exception as e:
            flash(f"Error de conexión: {e}", 'danger')
        # Redirigir a la página de detalles
        if content_type == 'movie':
            return redirect(url_for('movie_detail', movie_id=content_id))
        else:
            return redirect(url_for('series_detail', series_id=content_id))
    return render_template('edit_review.html', review=review, content_type=content_type, content_id=content_id)

# Perfil de usuario
@app.route('/profile')
@login_required
def profile():
    user = session['user']
    try:
        resp = requests.get(f"{API_BASE_URL}/reviews?user_id={user['id']}")
        reviews = resp.json() if resp.status_code == 200 else []
    except Exception:
        reviews = []
    movie_reviews = [r for r in reviews if r.get('content_type') == 'movie']
    series_reviews = [r for r in reviews if r.get('content_type') == 'series']
    # Agregar poster_url a cada reseña
    for r in movie_reviews:
        r['poster_url'] = get_tmdb_poster(r.get('content_title', ''), 'movie')
    for r in series_reviews:
        r['poster_url'] = get_tmdb_poster(r.get('content_title', ''), 'tv')
    return render_template('profile.html', user=user, movie_reviews=movie_reviews, series_reviews=series_reviews)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Sesión cerrada exitosamente.', 'success')
    return redirect(url_for('home'))

@app.route('/foro/new', methods=['GET', 'POST'])
@login_required
def foro_new():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        try:
            resp = requests.post(f"{API_BASE_URL}/forum/discussions", json={
                "title": title,
                "content": content,
                "user_id": session['user']['id'],
                "category": category
            })
            if resp.status_code in (200, 201):
                flash('Discusión creada exitosamente.', 'success')
                return redirect(url_for('foro'))
            else:
                flash('Error al crear la discusión.', 'danger')
        except Exception as e:
            flash(f"Error de conexión: {e}", 'danger')
    return render_template('foro_new.html')

@app.route('/foro/<int:discussion_id>', methods=['GET', 'POST'])
def foro_detail(discussion_id):
    # Obtener discusión
    try:
        resp = requests.get(f"{API_BASE_URL}/forum/discussions/{discussion_id}")
        if resp.status_code == 200:
            discussion = resp.json()
        else:
            flash('Discusión no encontrada.', 'danger')
            return redirect(url_for('foro'))
    except Exception as e:
        flash(f"Error de conexión: {e}", 'danger')
        return redirect(url_for('foro'))
    # Obtener respuestas
    try:
        replies_resp = requests.get(f"{API_BASE_URL}/forum/replies?discussion_id={discussion_id}")
        replies = replies_resp.json() if replies_resp.status_code == 200 else []
    except Exception:
        replies = []
    # Responder
    if request.method == 'POST' and session.get('user'):
        content = request.form.get('content')
        try:
            reply_resp = requests.post(f"{API_BASE_URL}/forum/replies", json={
                "discussion_id": discussion_id,
                "user_id": session['user']['id'],
                "content": content
            })
            if reply_resp.status_code in (200, 201):
                flash('Respuesta publicada.', 'success')
                return redirect(url_for('foro_detail', discussion_id=discussion_id))
            else:
                flash('Error al publicar la respuesta.', 'danger')
        except Exception as e:
            flash(f"Error de conexión: {e}", 'danger')
    return render_template('foro_detail.html', discussion=discussion, replies=replies)

@app.route('/delete_discussion/<int:discussion_id>')
@moderator_required
def delete_discussion(discussion_id):
    try:
        resp = requests.delete(f"{API_BASE_URL}/forum/discussions/{discussion_id}")
        if resp.status_code == 200:
            flash('Discusión eliminada exitosamente.', 'success')
        else:
            flash('Error al eliminar la discusión.', 'danger')
    except Exception as e:
        flash(f"Error de conexión: {e}", 'danger')
    return redirect(url_for('foro'))

@app.route('/delete_reply/<int:reply_id>/<int:discussion_id>')
@moderator_required
def delete_reply(reply_id, discussion_id):
    try:
        resp = requests.delete(f"{API_BASE_URL}/forum/replies/{reply_id}")
        if resp.status_code == 200:
            flash('Respuesta eliminada exitosamente.', 'success')
        else:
            flash('Error al eliminar la respuesta.', 'danger')
    except Exception as e:
        flash(f"Error de conexión: {e}", 'danger')
    return redirect(url_for('foro_detail', discussion_id=discussion_id))

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    local_results = []
    external_results = []
    if not query:
        return render_template('search_results.html', query=query, local_results=[], external_results=[])
    # Buscar en API local (películas)
    try:
        resp = requests.get(f"{API_BASE_URL}/movies")
        if resp.status_code == 200:
            movies = resp.json()
            for m in movies:
                if query.lower() in m.get('title', '').lower():
                    info = get_tmdb_info(m['title'], 'movie')
                    m['poster_url'] = info['poster_url']
                    m['overview'] = info['overview'] or m.get('description', '')
                    m['release_date'] = info['release_date']
                    m['genres_tmdb'] = info['genres']
                    m['vote_average'] = info['vote_average']
                    m['type'] = 'movie'
                    m['is_local'] = True
                    local_results.append(m)
    except Exception:
        pass
    # Buscar en API local (series)
    try:
        resp = requests.get(f"{API_BASE_URL}/series")
        if resp.status_code == 200:
            series = resp.json()
            for s in series:
                if query.lower() in s.get('title', '').lower():
                    info = get_tmdb_info(s['title'], 'tv')
                    s['poster_url'] = info['poster_url']
                    s['overview'] = info['overview'] or s.get('description', '')
                    s['release_date'] = info['release_date']
                    s['genres_tmdb'] = info['genres']
                    s['vote_average'] = info['vote_average']
                    s['type'] = 'series'
                    s['is_local'] = True
                    local_results.append(s)
    except Exception:
        pass
    # Si no hay resultados locales, buscar en TMDb
    if not local_results:
        # Buscar películas externas
        tmdb_movies = get_tmdb_info_tmdb_search(query, 'movie')
        for m in tmdb_movies:
            m['type'] = 'movie'
            m['is_local'] = False
            external_results.append(m)
        # Buscar series externas
        tmdb_series = get_tmdb_info_tmdb_search(query, 'tv')
        for s in tmdb_series:
            s['type'] = 'series'
            s['is_local'] = False
            external_results.append(s)
    return render_template('search_results.html', query=query, local_results=local_results, external_results=external_results)

def get_tmdb_info_tmdb_search(query, content_type="movie"):
    base_url = "https://api.themoviedb.org/3/search/"
    url = f"{base_url}{content_type}"
    headers = {"Authorization": f"Bearer {TMDB_TOKEN}"}
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "es-ES"
    }
    response = requests.get(url, params=params, headers=headers)
    results = []
    if response.status_code == 200:
        for data in response.json().get("results", [])[:10]:
            poster_path = data.get("poster_path")
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/180x270?text=No+Image"
            overview = data.get("overview", "")
            release_date = data.get("release_date") or data.get("first_air_date")
            genres = data.get("genre_ids", [])
            vote_average = data.get("vote_average")
            title = data.get("title") or data.get("name")
            tmdb_id = data.get("id")
            results.append({
                "title": title,
                "poster_url": poster_url,
                "overview": overview,
                "release_date": release_date,
                "genres_tmdb": genres,
                "vote_average": vote_average,
                "tmdb_id": tmdb_id
            })
    return results

def get_tmdb_details(tmdb_id, content_type="movie"):
    url = f"https://api.themoviedb.org/3/{'movie' if content_type == 'movie' else 'tv'}/{tmdb_id}"
    headers = {"Authorization": f"Bearer {TMDB_TOKEN}"}
    params = {"api_key": TMDB_API_KEY, "language": "es-ES"}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/180x270?text=No+Image"
        overview = data.get("overview", "")
        release_date = data.get("release_date") or data.get("first_air_date")
        genres = [g['name'] for g in data.get("genres", [])]
        vote_average = data.get("vote_average")
        title = data.get("title") or data.get("name")
        return {
            "tmdb_id": tmdb_id,
            "title": title,
            "poster_url": poster_url,
            "overview": overview,
            "release_date": release_date,
            "genres": genres,
            "vote_average": vote_average,
            "type": content_type
        }
    return None

@app.route('/tmdb/movie/<int:tmdb_id>', methods=['GET', 'POST'])
def tmdb_movie_detail(tmdb_id):
    movie = get_tmdb_details(tmdb_id, 'movie')
    if not movie:
        flash('Película no encontrada en TMDb.', 'danger')
        return redirect(url_for('search'))
    # Obtener reseñas locales asociadas a este tmdb_id
    try:
        resp = requests.get(f"{API_BASE_URL}/reviews?content_type=tmdb_movie&content_id={tmdb_id}")
        reviews = resp.json() if resp.status_code == 200 else []
    except Exception:
        reviews = []
    # Agregar reseña
    if request.method == 'POST' and session.get('user'):
        content = request.form.get('content')
        rating = request.form.get('rating')
        try:
            resp = requests.post(f"{API_BASE_URL}/reviews", json={
                "user_id": session['user']['id'],
                "content_type": "tmdb_movie",
                "content_id": tmdb_id,
                "content": content,
                "rating": float(rating)
            })
            if resp.status_code in (200, 201):
                flash('Reseña agregada exitosamente.', 'success')
                return redirect(url_for('tmdb_movie_detail', tmdb_id=tmdb_id))
            else:
                error = resp.json().get('error', 'Error al agregar reseña')
                flash(error, 'danger')
        except Exception as e:
            flash(f"Error de conexión: {e}", 'danger')
    return render_template('tmdb_detail.html', item=movie, reviews=reviews)

@app.route('/tmdb/series/<int:tmdb_id>', methods=['GET', 'POST'])
def tmdb_series_detail(tmdb_id):
    series = get_tmdb_details(tmdb_id, 'tv')
    if not series:
        flash('Serie no encontrada en TMDb.', 'danger')
        return redirect(url_for('search'))
    # Obtener reseñas locales asociadas a este tmdb_id
    try:
        resp = requests.get(f"{API_BASE_URL}/reviews?content_type=tmdb_series&content_id={tmdb_id}")
        reviews = resp.json() if resp.status_code == 200 else []
    except Exception:
        reviews = []
    # Agregar reseña
    if request.method == 'POST' and session.get('user'):
        content = request.form.get('content')
        rating = request.form.get('rating')
        try:
            resp = requests.post(f"{API_BASE_URL}/reviews", json={
                "user_id": session['user']['id'],
                "content_type": "tmdb_series",
                "content_id": tmdb_id,
                "content": content,
                "rating": float(rating)
            })
            if resp.status_code in (200, 201):
                flash('Reseña agregada exitosamente.', 'success')
                return redirect(url_for('tmdb_series_detail', tmdb_id=tmdb_id))
            else:
                error = resp.json().get('error', 'Error al agregar reseña')
                flash(error, 'danger')
        except Exception as e:
            flash(f"Error de conexión: {e}", 'danger')
    return render_template('tmdb_detail.html', item=series, reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True) 