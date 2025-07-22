const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cookieParser = require('cookie-parser');
const { Pool } = require('pg');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// Configuración de la base de datos
const pool = new Pool({
    user: process.env.DB_USER || 'popcornhour_user',
    host: process.env.DB_HOST || 'localhost',
    database: process.env.DB_NAME || 'popcornhour_db',
    password: process.env.DB_PASSWORD || 'tu_nueva_password_segura',
    port: process.env.DB_PORT || 5432,
});

// Configuración de JWT
const JWT_SECRET = process.env.JWT_SECRET || 'tu_clave_jwt_super_secreta_aqui_2024';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '7d';

// Middleware
app.use(cors({
    origin: ['http://localhost:3000', 'http://127.0.0.1:3000'],
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'Cookie']
}));

app.use(express.json());
app.use(cookieParser());

// Middleware de autenticación
const authenticateToken = async (req, res, next) => {
    try {
        // Buscar token en cookies o header Authorization
        let token = req.cookies.auth_token;
        
        if (!token) {
            const authHeader = req.headers['authorization'];
            token = authHeader && authHeader.split(' ')[1];
        }

        if (!token) {
            return res.status(401).json({ error: 'Token de acceso requerido' });
        }

        // Verificar token
        const decoded = jwt.verify(token, JWT_SECRET);
        
        // Obtener información del usuario de la base de datos
        const userResult = await pool.query(
            'SELECT id, username, email, user_type, created_at FROM users WHERE id = $1',
            [decoded.userId]
        );

        if (userResult.rows.length === 0) {
            return res.status(401).json({ error: 'Usuario no encontrado' });
        }

        req.user = userResult.rows[0];
        next();
    } catch (error) {
        console.error('Error en autenticación:', error);
        return res.status(403).json({ error: 'Token inválido' });
    }
};

// Middleware para verificar rol de moderador
const requireModerator = (req, res, next) => {
    if (req.user.user_type !== 'moderator') {
        return res.status(403).json({ error: 'Acceso denegado. Se requieren permisos de moderador.' });
    }
    next();
};

// Función para generar token JWT
const generateToken = (userId) => {
    return jwt.sign({ userId }, JWT_SECRET, { expiresIn: JWT_EXPIRES_IN });
};

// Función para establecer cookie segura
const setAuthCookie = (res, token) => {
    res.cookie('auth_token', token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax',
        maxAge: 7 * 24 * 60 * 60 * 1000 // 7 días
    });
};

// Rutas de autenticación

// Registro de usuario
app.post('/api/auth/register', async (req, res) => {
    try {
        const { username, email, password, userType = 'standard' } = req.body;

        // Validaciones básicas
        if (!username || !email || !password) {
            return res.status(400).json({ error: 'Todos los campos son requeridos' });
        }

        if (password.length < 6) {
            return res.status(400).json({ error: 'La contraseña debe tener al menos 6 caracteres' });
        }

        // Verificar si el usuario ya existe
        const existingUser = await pool.query(
            'SELECT id FROM users WHERE username = $1 OR email = $2',
            [username, email]
        );

        if (existingUser.rows.length > 0) {
            return res.status(400).json({ error: 'El usuario o email ya existe' });
        }

        // Encriptar contraseña
        const saltRounds = 12;
        const hashedPassword = await bcrypt.hash(password, saltRounds);

        // Crear usuario
        const newUser = await pool.query(
            'INSERT INTO users (username, email, password_hash, user_type) VALUES ($1, $2, $3, $4) RETURNING id, username, email, user_type, created_at',
            [username, email, hashedPassword, userType]
        );

        const user = newUser.rows[0];

        // Generar token
        const token = generateToken(user.id);

        // Establecer cookie
        setAuthCookie(res, token);

        res.status(201).json({
            message: 'Usuario registrado exitosamente',
            user: {
                id: user.id,
                username: user.username,
                email: user.email,
                userType: user.user_type,
                createdAt: user.created_at
            },
            token
        });

    } catch (error) {
        console.error('Error en registro:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// Inicio de sesión
app.post('/api/auth/login', async (req, res) => {
    try {
        const { username, password } = req.body;

        if (!username || !password) {
            return res.status(400).json({ error: 'Usuario y contraseña son requeridos' });
        }

        // Buscar usuario por username o email
        const userResult = await pool.query(
            'SELECT id, username, email, password_hash, user_type, created_at FROM users WHERE username = $1 OR email = $1',
            [username]
        );

        if (userResult.rows.length === 0) {
            return res.status(401).json({ error: 'Credenciales inválidas' });
        }

        const user = userResult.rows[0];

        // Verificar contraseña
        const isValidPassword = await bcrypt.compare(password, user.password_hash);

        if (!isValidPassword) {
            return res.status(401).json({ error: 'Credenciales inválidas' });
        }

        // Actualizar último acceso
        await pool.query(
            'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = $1',
            [user.id]
        );

        // Generar token
        const token = generateToken(user.id);

        // Establecer cookie
        setAuthCookie(res, token);

        res.json({
            message: 'Inicio de sesión exitoso',
            user: {
                id: user.id,
                username: user.username,
                email: user.email,
                userType: user.user_type,
                createdAt: user.created_at
            },
            token
        });

    } catch (error) {
        console.error('Error en login:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// Verificar estado de autenticación
app.get('/api/auth/me', authenticateToken, (req, res) => {
    res.json({
        user: {
            id: req.user.id,
            username: req.user.username,
            email: req.user.email,
            userType: req.user.user_type,
            createdAt: req.user.created_at
        }
    });
});

// Cerrar sesión
app.post('/api/auth/logout', (req, res) => {
    res.clearCookie('auth_token');
    res.json({ message: 'Sesión cerrada exitosamente' });
});

// Rutas de contenido

// Obtener películas
app.get('/api/movies', async (req, res) => {
    try {
        const { genre, year, search } = req.query;
        let query = 'SELECT * FROM movies WHERE 1=1';
        const params = [];

        if (genre) {
            params.push(`%${genre}%`);
            query += ` AND genre ILIKE $${params.length}`;
        }

        if (year) {
            params.push(year);
            query += ` AND release_year = $${params.length}`;
        }

        if (search) {
            params.push(`%${search}%`);
            query += ` AND title ILIKE $${params.length}`;
        }

        query += ' ORDER BY created_at DESC';

        const result = await pool.query(query, params);
        res.json(result.rows);

    } catch (error) {
        console.error('Error obteniendo películas:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// Crear película (solo moderadores)
app.post('/api/movies', authenticateToken, requireModerator, async (req, res) => {
    try {
        const { title, description, release_year, duration_minutes, genre, director, imdb_rating, poster_url } = req.body;

        if (!title || !release_year) {
            return res.status(400).json({ error: 'Título y año de lanzamiento son requeridos' });
        }

        const newMovie = await pool.query(
            'INSERT INTO movies (title, description, release_year, duration_minutes, genre, director, imdb_rating, poster_url, created_by) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING *',
            [title, description, release_year, duration_minutes, genre, director, imdb_rating, poster_url, req.user.id]
        );

        res.status(201).json({
            message: 'Película creada exitosamente',
            movie: newMovie.rows[0]
        });

    } catch (error) {
        console.error('Error creando película:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// Obtener reseñas
app.get('/api/reviews', async (req, res) => {
    try {
        const { content_id, content_type } = req.query;
        let query = `
            SELECT r.*, u.username, 
                   CASE 
                       WHEN r.content_type = 'movie' THEN m.title
                       WHEN r.content_type = 'series' THEN s.title
                   END as content_title
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            LEFT JOIN movies m ON r.content_id = m.id AND r.content_type = 'movie'
            LEFT JOIN series s ON r.content_id = s.id AND r.content_type = 'series'
            WHERE 1=1
        `;
        const params = [];

        if (content_id) {
            params.push(content_id);
            query += ` AND r.content_id = $${params.length}`;
        }

        if (content_type) {
            params.push(content_type);
            query += ` AND r.content_type = $${params.length}`;
        }

        query += ' ORDER BY r.created_at DESC LIMIT 20';

        const result = await pool.query(query, params);
        res.json(result.rows);

    } catch (error) {
        console.error('Error obteniendo reseñas:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// Crear reseña (usuarios autenticados)
app.post('/api/reviews', authenticateToken, async (req, res) => {
    try {
        const { content_id, content_type, rating, comment } = req.body;

        if (!content_id || !content_type || !rating) {
            return res.status(400).json({ error: 'ID de contenido, tipo y calificación son requeridos' });
        }

        if (rating < 1 || rating > 5) {
            return res.status(400).json({ error: 'La calificación debe estar entre 1 y 5' });
        }

        // Verificar si el usuario ya reseñó este contenido
        const existingReview = await pool.query(
            'SELECT id FROM reviews WHERE user_id = $1 AND content_id = $2 AND content_type = $3',
            [req.user.id, content_id, content_type]
        );

        if (existingReview.rows.length > 0) {
            return res.status(400).json({ error: 'Ya has reseñado este contenido' });
        }

        const newReview = await pool.query(
            'INSERT INTO reviews (user_id, content_id, content_type, rating, comment) VALUES ($1, $2, $3, $4, $5) RETURNING *',
            [req.user.id, content_id, content_type, rating, comment]
        );

        res.status(201).json({
            message: 'Reseña creada exitosamente',
            review: newReview.rows[0]
        });

    } catch (error) {
        console.error('Error creando reseña:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// Obtener series
app.get('/api/series', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM series ORDER BY created_at DESC');
        res.json(result.rows);
    } catch (error) {
        console.error('Error obteniendo series:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// Obtener discusiones del foro
app.get('/api/forum/discussions', async (req, res) => {
    try {
        const result = await pool.query(`
            SELECT fd.*, u.username as author_username,
                   COUNT(fc.id) as comment_count
            FROM forum_discussions fd
            JOIN users u ON fd.user_id = u.id
            LEFT JOIN forum_comments fc ON fd.id = fc.discussion_id
            GROUP BY fd.id, u.username
            ORDER BY fd.created_at DESC
        `);
        res.json(result.rows);
    } catch (error) {
        console.error('Error obteniendo discusiones:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// Crear discusión en el foro (usuarios autenticados)
app.post('/api/forum/discussions', authenticateToken, async (req, res) => {
    try {
        const { title, content, category } = req.body;

        if (!title || !content) {
            return res.status(400).json({ error: 'Título y contenido son requeridos' });
        }

        const newDiscussion = await pool.query(
            'INSERT INTO forum_discussions (user_id, title, content, category) VALUES ($1, $2, $3, $4) RETURNING *',
            [req.user.id, title, content, category || 'general']
        );

        res.status(201).json({
            message: 'Discusión creada exitosamente',
            discussion: newDiscussion.rows[0]
        });

    } catch (error) {
        console.error('Error creando discusión:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// Ruta de salud del servidor
app.get('/api/health', (req, res) => {
    res.json({
        message: 'Backend de PopcornHour funcionando correctamente',
        timestamp: new Date().toISOString(),
        version: '2.0.0'
    });
});

// Manejo de errores global
app.use((error, req, res, next) => {
    console.error('Error no manejado:', error);
    res.status(500).json({ error: 'Error interno del servidor' });
});

// Manejo de rutas no encontradas
app.use('*', (req, res) => {
    res.status(404).json({ error: 'Ruta no encontrada' });
});

// Iniciar servidor
app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Servidor backend ejecutándose en http://localhost:${PORT}`);
    console.log(`📊 Base de datos: ${process.env.DB_NAME || 'popcornhour_db'}`);
    console.log(`🔐 JWT configurado correctamente`);
    console.log(`🍪 Cookies seguras habilitadas`);
});

// Manejo de cierre graceful
process.on('SIGINT', async () => {
    console.log('🛑 Cerrando servidor...');
    await pool.end();
    process.exit(0);
});

process.on('SIGTERM', async () => {
    console.log('🛑 Cerrando servidor...');
    await pool.end();
    process.exit(0);
});

