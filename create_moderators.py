#!/usr/bin/env python3
"""
Script para crear usuarios moderadores en PopcornHour
"""

import requests
import json

# Configuración del backend
API_BASE_URL = "http://localhost:3001/api"

def create_moderator(username, email, password):
    """Crear usuario moderador usando la API"""
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register", json={
            "username": username,
            "email": email,
            "password": password,
            "userType": "moderator"  # Especificar tipo moderador
        })
        
        print(f"📝 Creando moderador {username}:")
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"  ✅ Moderador creado exitosamente!")
            print(f"  ID: {data['user']['id']}")
            print(f"  Tipo: {data['user']['userType']}")
            print(f"  Email: {data['user']['email']}")
            return True
        else:
            try:
                error = response.json().get('error', 'Error desconocido')
                print(f"  ❌ Error: {error}")
            except:
                print(f"  ❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error de conexión: {e}")
        return False

def test_moderator_login(username, password):
    """Probar login del moderador"""
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login", json={
            "username": username,
            "password": password
        })
        
        print(f"🔐 Probando login con moderador {username}:")
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Login exitoso!")
            print(f"  Usuario: {data['user']['username']}")
            print(f"  Tipo: {data['user']['userType']}")
            print(f"  Privilegios: {'Moderador' if data['user']['userType'] == 'moderator' else 'Usuario estándar'}")
            return True
        else:
            try:
                error = response.json().get('error', 'Error desconocido')
                print(f"  ❌ Error: {error}")
            except:
                print(f"  ❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error de conexión: {e}")
        return False

def main():
    print("🍿 Creando usuarios moderadores para PopcornHour...")
    print("=" * 60)
    
    # Moderadores a crear
    moderators = [
        ('admin', 'admin@popcornhour.com', '123456'),
        ('moderator1', 'mod1@popcornhour.com', '123456'),
        ('moderator2', 'mod2@popcornhour.com', '123456'),
        ('superadmin', 'superadmin@popcornhour.com', '123456')
    ]
    
    created_moderators = []
    
    # Crear moderadores
    for username, email, password in moderators:
        if create_moderator(username, email, password):
            created_moderators.append((username, password))
        print()
    
    # Probar login con todos los moderadores creados
    print("=" * 60)
    print("🧪 Probando login con moderadores creados...")
    
    for username, password in created_moderators:
        test_moderator_login(username, password)
        print()
    
    print("=" * 60)
    print("✅ Proceso completado!")
    print("\n🎯 Moderadores disponibles para login:")
    for username, password in created_moderators:
        print(f"  - {username} / {password} (Moderador)")
    
    print("\n👥 Usuarios estándar existentes:")
    print("  - testuser / 123456 (Usuario estándar)")
    print("  - testuser2 / 123456 (Usuario estándar)")
    
    print("\n🔐 Funcionalidades de moderador:")
    print("  - Agregar películas y series")
    print("  - Editar contenido existente")
    print("  - Eliminar contenido")
    print("  - Moderar foro")
    print("  - Acceso al panel de administración")
    
    print("\n🌐 Ve a http://localhost:5000 y prueba con los moderadores!")

if __name__ == "__main__":
    main() 