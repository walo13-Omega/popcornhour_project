#!/usr/bin/env python3
"""
Script para verificar las contraseñas en la base de datos
"""

import psycopg2
import bcrypt

def check_password_hashes():
    """Verificar las contraseñas en la base de datos"""
    print("🔍 VERIFICANDO CONTRASEÑAS EN LA BASE DE DATOS")
    print("=" * 50)
    
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            dbname="popcornhour_db",
            user="popcornhour_user",
            password="tu_nueva_password_segura",
            host="localhost",
            port="5432"
        )
        
        cursor = conn.cursor()
        
        # Obtener todos los usuarios
        cursor.execute("SELECT username, password_hash, user_type FROM users")
        users = cursor.fetchall()
        
        print(f"📊 Total de usuarios: {len(users)}")
        print("\n🔐 VERIFICACIÓN DE CONTRASEÑAS:")
        print("-" * 40)
        
        expected_password = "123456"
        working_users = []
        broken_users = []
        
        for username, password_hash, user_type in users:
            print(f"\n👤 Usuario: {username}")
            print(f"   Tipo: {user_type}")
            print(f"   Hash: {password_hash[:20]}...")
            
            try:
                # Verificar si la contraseña "123456" coincide con el hash
                is_valid = bcrypt.checkpw(expected_password.encode('utf-8'), password_hash.encode('utf-8'))
                
                if is_valid:
                    print(f"   ✅ Contraseña válida")
                    working_users.append(username)
                else:
                    print(f"   ❌ Contraseña inválida")
                    broken_users.append(username)
                    
            except Exception as e:
                print(f"   ❌ Error verificando: {e}")
                broken_users.append(username)
        
        print("\n" + "=" * 50)
        print("📋 RESUMEN:")
        print(f"✅ Usuarios con contraseña correcta: {len(working_users)}")
        print(f"❌ Usuarios con contraseña incorrecta: {len(broken_users)}")
        
        if working_users:
            print(f"\n🎯 Usuarios que deberían funcionar:")
            for user in working_users:
                print(f"   - {user}")
        
        if broken_users:
            print(f"\n🔧 Usuarios que necesitan arreglo:")
            for user in broken_users:
                print(f"   - {user}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")

def test_bcrypt_hash():
    """Probar la generación de hash bcrypt"""
    print("\n🧪 PROBANDO GENERACIÓN DE HASH")
    print("=" * 35)
    
    password = "123456"
    hash_generated = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
    
    print(f"Contraseña: {password}")
    print(f"Hash generado: {hash_generated.decode('utf-8')}")
    
    # Verificar que funciona
    is_valid = bcrypt.checkpw(password.encode('utf-8'), hash_generated)
    print(f"Verificación: {'✅ Válido' if is_valid else '❌ Inválido'}")

def main():
    print("🍿 VERIFICACIÓN DE CONTRASEÑAS")
    print("=" * 50)
    
    # 1. Verificar hashes en la base de datos
    check_password_hashes()
    
    # 2. Probar generación de hash
    test_bcrypt_hash()
    
    print("\n" + "=" * 50)
    print("💡 RECOMENDACIONES:")
    print("1. Si hay usuarios con contraseñas incorrectas, actualízalos")
    print("2. Usa el hash generado para actualizar la base de datos")
    print("3. Prueba login con usuarios que tengan contraseñas correctas")

if __name__ == "__main__":
    main() 