-- Actualizar contraseñas de usuarios con hash válido
-- Contraseña: 123456
-- Hash generado con bcrypt

UPDATE users SET password_hash = '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi.' WHERE username = 'admin';
UPDATE users SET password_hash = '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi.' WHERE username = 'moderator';
UPDATE users SET password_hash = '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi.' WHERE username = 'user';
UPDATE users SET password_hash = '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi.' WHERE username = 'test';

-- Verificar que se actualizaron
SELECT username, password_hash FROM users; 