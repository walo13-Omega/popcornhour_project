-- Script para arreglar usuarios con contraseñas válidas
-- Primero limpiar usuarios existentes (opcional)
-- TRUNCATE TABLE users RESTART IDENTITY CASCADE;

-- Insertar usuarios con contraseña "123456" (hash generado con bcrypt)
INSERT INTO users (username, email, password_hash, user_type) VALUES
('admin', 'admin@popcornhour.com', '$2b$12$LrSzZt.ywKxag0aulFA1yuOxunDGQYvLxzbEpKGNoS9dcjdL8u56C', 'moderator'),
('user1', 'user1@popcornhour.com', '$2b$12$LrSzZt.ywKxag0aulFA1yuOxunDGQYvLxzbEpKGNoS9dcjdL8u56C', 'standard'),
('user2', 'user2@popcornhour.com', '$2b$12$LrSzZt.ywKxag0aulFA1yuOxunDGQYvLxzbEpKGNoS9dcjdL8u56C', 'standard'),
('modnuevo1', 'modnuevo1@popcornhour.com', '$2b$12$LrSzZt.ywKxag0aulFA1yuOxunDGQYvLxzbEpKGNoS9dcjdL8u56C', 'moderator'),
('modnuevo2', 'modnuevo2@popcornhour.com', '$2b$12$LrSzZt.ywKxag0aulFA1yuOxunDGQYvLxzbEpKGNoS9dcjdL8u56C', 'moderator')
ON CONFLICT (username) DO UPDATE SET 
    password_hash = EXCLUDED.password_hash,
    email = EXCLUDED.email,
    user_type = EXCLUDED.user_type;

-- Verificar que se insertaron correctamente
SELECT username, email, user_type FROM users ORDER BY username; 