const bcrypt = require('bcryptjs');

async function generateHashes() {
    console.log('Generando hashes válidos...\n');
    
    // Generar hash para admin123
    const hash1 = await bcrypt.hash('admin123', 10);
    console.log('Hash para "admin123":');
    console.log(hash1);
    
    // Verificar que funciona
    const isValid1 = await bcrypt.compare('admin123', hash1);
    console.log(`Verificación admin123: ${isValid1 ? '✅ VÁLIDO' : '❌ INVÁLIDO'}\n`);
    
    // Generar hash para mod123
    const hash2 = await bcrypt.hash('mod123', 10);
    console.log('Hash para "mod123":');
    console.log(hash2);
    
    // Verificar que funciona
    const isValid2 = await bcrypt.compare('mod123', hash2);
    console.log(`Verificación mod123: ${isValid2 ? '✅ VÁLIDO' : '❌ INVÁLIDO'}\n`);
    
    console.log('Comandos SQL para actualizar:');
    console.log(`UPDATE users SET password_hash = '${hash1}' WHERE username = 'admin';`);
    console.log(`UPDATE users SET password_hash = '${hash2}' WHERE username = 'moderator';`);
}

generateHashes(); 