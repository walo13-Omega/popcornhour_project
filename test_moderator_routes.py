#!/usr/bin/env python3
"""
Script para probar las rutas de moderador
"""

import requests
import json

# Configuración
FLASK_URL = "http://localhost:5000"
NODE_URL = "http://localhost:3001/api"

def test_moderator_login():
    """Probar login de moderador"""
    print("🔐 Probando login de moderador...")
    
    try:
        response = requests.post(f"{NODE_URL}/auth/login", json={
            "username": "superadmin",
            "password": "123456"
        })
        
        if response.status_code == 200:
            data = response.json()
            user = data.get('user', {})
            print(f"✅ Login exitoso: {user.get('username')}")
            print(f"📋 userType: {user.get('userType')}")
            return True
        else:
            print(f"❌ Error en login: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_moderator_routes():
    """Probar rutas de moderador"""
    print("\n🔍 Probando rutas de moderador...")
    
    routes = [
        "/add_movie",
        "/add_series", 
        "/admin_content"
    ]
    
    for route in routes:
        print(f"\n📡 Probando: {route}")
        try:
            response = requests.get(f"{FLASK_URL}{route}")
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ Ruta accesible")
            elif response.status_code == 302:
                print(f"  🔄 Redirección (posible problema de autenticación)")
            else:
                print(f"  ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error de conexión: {e}")

def main():
    print("🍿 PROBANDO RUTAS DE MODERADOR")
    print("=" * 50)
    
    # Probar login
    login_success = test_moderator_login()
    
    if login_success:
        # Probar rutas
        test_moderator_routes()
    
    print("\n" + "=" * 50)
    print("📋 INSTRUCCIONES PARA PROBAR:")
    print("1. Ve a: http://localhost:5000")
    print("2. Inicia sesión con: superadmin / 123456")
    print("3. Haz clic en los botones del panel de moderador")
    print("4. Mira la consola de Flask para ver los logs de debug")
    
    print("\n🔧 Si las rutas no funcionan:")
    print("- Verifica que Flask esté ejecutándose con los cambios de debug")
    print("- Asegúrate de estar logueado como moderador")
    print("- Revisa los logs de Flask para ver qué está pasando")

if __name__ == "__main__":
    main() 