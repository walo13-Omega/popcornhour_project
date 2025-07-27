#!/usr/bin/env python3
"""
Script para arreglar la autenticación de PopcornHour
"""

import psycopg2
import requests
import json

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'popcornhour_db',
    'user': 'popcornhour_user',
    'password': 'tu_nueva_password_segura',
    'port': 5432
}

# Configuración del backend
API_BASE_URL = "http://localhost:3001/api"

def fix_database():
    """Arreglar usuarios en la base de datos"""
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Hash válido para contraseña "123456"
        valid_hash = '$2b$12$LrSzZt.ywKxag0aulFA1yuOxunDGQYvLxzbEpKGNoS9dcjdL8u56C'
        
        # Insertar/actualizar usuarios
        users = [
            ('admin', 'admin@popcornhour.com', valid_hash, 'moderator'),
            ('user1', 'user1@popcornhour.com', valid_hash, 'standard'),
            ('user2', 'user2@popcornhour.com', valid_hash, 'standard'),
            ('modnuevo1', 'modnuevo1@popcornhour.com', valid_hash, 'moderator'),
            ('modnuevo2', 'modnuevo2@popcornhour.com', valid_hash, 'moderator')
        ]
        
        for username, email, password_hash, user_type in users:
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, user_type) 
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (username) DO UPDATE SET 
                    password_hash = EXCLUDED.password_hash,
                    email = EXCLUDED.email,
                    user_type = EXCLUDED.user_type
            """, (username, email, password_hash, user_type))
        
        conn.commit()
        print("✅ Usuarios actualizados en la base de datos")
        
        # Verificar usuarios
        cursor.execute("SELECT username, email, user_type FROM users ORDER BY username")
        users = cursor.fetchall()
        print("\n📋 Usuarios en la base de datos:")
        for user in users:
            print(f"  - {user[0]} ({user[1]}) - {user[2]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error en la base de datos: {e}")

def test_login(username, password):
    """Probar login con el backend"""
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login", json={
            "username": username,
            "password": password
        })
        
        print(f"\n🔐 Probando login con {username}:")
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Login exitoso!")
            print(f"  Usuario: {data['user']['username']}")
            print(f"  Tipo: {data['user']['userType']}")
            return True
        else:
            error = response.json().get('error', 'Error desconocido')
            print(f"  ❌ Error: {error}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error de conexión: {e}")
        return False

def test_register(username, email, password):
    """Probar registro con el backend"""
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register", json={
            "username": username,
            "email": email,
            "password": password
        })
        
        print(f"\n📝 Probando registro con {username}:")
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"  ✅ Registro exitoso!")
            print(f"  Usuario: {data['user']['username']}")
            return True
        else:
            error = response.json().get('error', 'Error desconocido')
            print(f"  ❌ Error: {error}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error de conexión: {e}")
        return False

def main():
    print("🍿 Arreglando autenticación de PopcornHour...")
    print("=" * 50)
    
    # 1. Arreglar base de datos
    fix_database()
    
    # 2. Probar login con usuarios existentes
    print("\n" + "=" * 50)
    print("🧪 Probando autenticación...")
    
    test_users = [
        ('admin', '123456'),
        ('user1', '123456'),
        ('user2', '123456'),
        ('modnuevo1', '123456'),
        ('modnuevo2', '123456')
    ]
    
    for username, password in test_users:
        test_login(username, password)
    
    # 3. Probar registro de nuevo usuario
    print("\n" + "=" * 50)
    print("📝 Probando registro...")
    
    test_register('testuser', 'test@test.com', '123456')
    
    print("\n" + "=" * 50)
    print("✅ Proceso completado!")
    print("\n🎯 Ahora puedes usar estos usuarios para login:")
    print("  - admin / 123456 (moderador)")
    print("  - user1 / 123456 (usuario estándar)")
    print("  - user2 / 123456 (usuario estándar)")
    print("  - modnuevo1 / 123456 (moderador)")
    print("  - modnuevo2 / 123456 (moderador)")
    print("  - testuser / 123456 (nuevo usuario)")

if __name__ == "__main__":
    main() 