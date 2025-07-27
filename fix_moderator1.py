#!/usr/bin/env python3
"""
Script para arreglar usuarios moderadores problemáticos
"""

import requests
import json

# Configuración del backend
API_BASE_URL = "http://localhost:3001/api"

def create_admin():
    """Crear usuario admin como moderador"""
    print("📝 Creando admin como moderador...")
    
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register", json={
            "username": "admin",
            "email": "admin@popcornhour.com",
            "password": "123456",
            "userType": "moderator"
        })
        
        print(f"  📡 Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"  ✅ Admin creado exitosamente!")
            print(f"  - ID: {data['user']['id']}")
            print(f"  - Tipo: {data['user']['userType']}")
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

def test_admin_login():
    """Probar login de admin"""
    print("\n🔐 Probando login de admin...")
    
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login", json={
            "username": "admin",
            "password": "123456"
        })
        
        print(f"  📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            user = data.get('user', {})
            print(f"  ✅ Login exitoso!")
            print(f"  - userType: {user.get('userType')}")
            print(f"  - ¿Es moderador?: {user.get('userType') == 'moderator'}")
            return True
        else:
            print(f"  ❌ Error en login")
            return False
            
    except Exception as e:
        print(f"  ❌ Error de conexión: {e}")
        return False

def main():
    print("🍿 ARREGLANDO USUARIOS MODERADORES")
    print("=" * 50)
    
    # Crear admin
    admin_created = create_admin()
    
    # Probar admin
    if admin_created:
        test_admin_login()
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN FINAL:")
    print("✅ Moderadores que funcionan:")
    print("  - moderator2 / 123456")
    print("  - superadmin / 123456")
    
    if admin_created:
        print("  - admin / 123456 (nuevo)")
    
    print("\n❌ Moderadores problemáticos:")
    print("  - moderator1 / 123456 (userType: standard - necesita arreglo manual)")
    
    print("\n🔧 Para arreglar moderator1 manualmente:")
    print("  - Conectar a PostgreSQL")
    print("  - UPDATE users SET user_type = 'moderator' WHERE username = 'moderator1';")
    
    print("\n🌐 Prueba con los moderadores que funcionan en: http://localhost:5000")

if __name__ == "__main__":
    main() 