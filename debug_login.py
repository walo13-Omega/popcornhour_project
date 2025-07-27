#!/usr/bin/env python3
"""
Script para diagnosticar el error 500 en login
"""

import requests
import json

# Configuración
API_BASE_URL = "http://localhost:3001/api"

def test_login_with_debug():
    """Probar login con información detallada"""
    print("🔍 DIAGNÓSTICO DEL ERROR 500 EN LOGIN")
    print("=" * 50)
    
    # Datos de login
    login_data = {
        "username": "testuser",
        "password": "123456"
    }
    
    print(f"📡 Enviando datos: {json.dumps(login_data, indent=2)}")
    
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📡 Headers: {dict(response.headers)}")
        print(f"📡 Response: {response.text}")
        
        if response.status_code == 500:
            print("\n❌ ERROR 500 DETECTADO")
            print("🔧 Posibles causas:")
            print("1. Error en la base de datos")
            print("2. Error en la validación de contraseña")
            print("3. Error en la generación del JWT")
            print("4. Error en la configuración del servidor")
            
        elif response.status_code == 200:
            data = response.json()
            print(f"\n✅ LOGIN EXITOSO!")
            print(f"Usuario: {data.get('user', {}).get('username')}")
            print(f"Token: {data.get('token', 'No disponible')[:20]}...")
            
        else:
            print(f"\n⚠️ Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_different_users():
    """Probar con diferentes usuarios"""
    print("\n🧪 PROBANDO DIFERENTES USUARIOS")
    print("=" * 30)
    
    users_to_test = [
        ("testuser", "123456"),
        ("superadmin", "123456"),
        ("admin", "123456"),
        ("moderator2", "123456")
    ]
    
    for username, password in users_to_test:
        print(f"\n🔐 Probando: {username}")
        
        login_data = {
            "username": username,
            "password": password
        }
        
        try:
            response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                user_type = data.get('user', {}).get('userType', 'unknown')
                print(f"  ✅ Éxito - Tipo: {user_type}")
            elif response.status_code == 500:
                print(f"  ❌ Error 500")
            else:
                print(f"  ⚠️ {response.text}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")

def test_backend_health():
    """Verificar que el backend está funcionando"""
    print("\n🏥 VERIFICANDO SALUD DEL BACKEND")
    print("=" * 35)
    
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Backend funcionando correctamente")
        else:
            print("❌ Backend con problemas")
            
    except Exception as e:
        print(f"❌ Error conectando al backend: {e}")

def main():
    print("🍿 DIAGNÓSTICO COMPLETO DEL LOGIN")
    print("=" * 50)
    
    # 1. Verificar salud del backend
    test_backend_health()
    
    # 2. Probar login con debug
    test_login_with_debug()
    
    # 3. Probar diferentes usuarios
    test_different_users()
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN:")
    print("- Si todos dan error 500: problema en el backend")
    print("- Si algunos funcionan: problema específico de usuario")
    print("- Si backend no responde: problema de conexión")

if __name__ == "__main__":
    main() 