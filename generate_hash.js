const bcrypt = require('bcryptjs');

async function generateHash() {
    const password = '123456';
    const hash = await bcrypt.hash(password, 12);
    console.log(`Hash para '${password}': ${hash}`);
    
    // Verificar que funciona
    const isValid = await bcrypt.compare(password, hash);
    console.log(`Verificación: ${isValid ? '✅ VÁLIDO' : '❌ INVÁLIDO'}`);
}

generateHash(); 