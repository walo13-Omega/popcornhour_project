#!/usr/bin/env python3
"""
Script para crear usuarios de prueba usando la API del backend
"""

import requests
import json

# Configuración del backend
API_BASE_URL = "http://localhost:3001/api"

def create_user(username, email, password):
    """Crear usuario usando la API"""
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register", json={
            "username": username,
            "email": email,
            "password": password
        })
        
        print(f"📝 Creando usuario {username}:")
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"  ✅ Usuario creado exitosamente!")
            print(f"  ID: {data['user']['id']}")
            print(f"  Tipo: {data['user']['userType']}")
            return True
        else:
            error = response.json().get('error', 'Error desconocido')
            print(f"  ❌ Error: {error}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error de conexión: {e}")
        return False

def test_login(username, password):
    """Probar login"""
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login", json={
            "username": username,
            "password": password
        })
        
        print(f"🔐 Probando login con {username}:")
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

def main():
    print("🍿 Creando usuarios de prueba para PopcornHour...")
    print("=" * 60)
    
    # Usuarios a crear
    test_users = [
        ('admin', 'admin@popcornhour.com', '123456'),
        ('moderator1', 'mod1@popcornhour.com', '123456'),
        ('user1', 'user1@popcornhour.com', '123456'),
        ('user2', 'user2@popcornhour.com', '123456')
    ]
    
    created_users = []
    
    # Crear usuarios
    for username, email, password in test_users:
        if create_user(username, email, password):
            created_users.append((username, password))
        print()
    
    # Probar login con todos los usuarios creados
    print("=" * 60)
    print("🧪 Probando login con usuarios creados...")
    
    for username, password in created_users:
        test_login(username, password)
        print()
    
    print("=" * 60)
    print("✅ Proceso completado!")
    print("\n🎯 Usuarios disponibles para login:")
    for username, password in created_users:
        print(f"  - {username} / {password}")
    print(f"  - testuser / 123456 (ya existía)")
    
    print("\n🌐 Ahora puedes ir a http://localhost:5000 y probar el login/registro!")

if __name__ == "__main__":
    main() 