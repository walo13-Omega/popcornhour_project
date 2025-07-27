const bcrypt = require('bcryptjs');

// Hash de la contraseña '123456' que estamos usando
const hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2.';

// Probar diferentes contraseñas
const passwords = ['123456', 'password123', 'admin', 'test', 'password'];

console.log('Verificando hash de contraseña...\n');

passwords.forEach(password => {
    bcrypt.compare(password, hash).then(isValid => {
        console.log(`Contraseña "${password}": ${isValid ? '✅ VÁLIDA' : '❌ INVÁLIDA'}`);
    });
});

// Generar un nuevo hash para '123456'
bcrypt.hash('123456', 12).then(newHash => {
    console.log(`\nNuevo hash para '123456': ${newHash}`);
}); 