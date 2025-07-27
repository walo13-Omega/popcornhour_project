#!/usr/bin/env python3
"""
Script para verificar los datos de sesión del usuario
"""

import requests
import json

# Configuración del backend
API_BASE_URL = "http://localhost:3001/api"

def test_login_and_check_session():
    """Probar login y verificar datos de sesión"""
    print("🔍 Probando login y verificando datos de sesión...")
    
    # Probar login con moderador
    login_data = {
        "username": "superadmin",
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)
        
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            user = data.get('user', {})
            
            print("✅ Login exitoso!")
            print("📋 Datos del usuario recibidos:")
            print(f"  - ID: {user.get('id')}")
            print(f"  - Username: {user.get('username')}")
            print(f"  - Email: {user.get('email')}")
            print(f"  - userType: {user.get('userType')}")
            print(f"  - user_type: {user.get('user_type')}")
            print(f"  - createdAt: {user.get('createdAt')}")
            
            # Verificar si es moderador
            user_type = user.get('userType') or user.get('user_type')
            is_moderator = user_type == 'moderator'
            
            print(f"\n🔐 Verificación de moderador:")
            print(f"  - userType encontrado: '{user_type}'")
            print(f"  - ¿Es moderador?: {is_moderator}")
            
            if is_moderator:
                print("  ✅ El usuario SÍ es moderador")
            else:
                print("  ❌ El usuario NO es moderador")
                print("  🔍 Posibles problemas:")
                print("    - Campo 'userType' no existe")
                print("    - Valor no es 'moderator'")
                print("    - Campo se llama 'user_type' en lugar de 'userType'")
            
            return user
            
        else:
            print(f"❌ Error en login: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def check_backend_user_data():
    """Verificar datos del usuario en el backend"""
    print("\n🔍 Verificando datos del usuario en el backend...")
    
    try:
        # Obtener información del usuario actual
        response = requests.get(f"{API_BASE_URL}/auth/me")
        
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            user = data.get('user', {})
            
            print("✅ Datos del usuario en backend:")
            print(f"  - ID: {user.get('id')}")
            print(f"  - Username: {user.get('username')}")
            print(f"  - Email: {user.get('email')}")
            print(f"  - userType: {user.get('userType')}")
            print(f"  - user_type: {user.get('user_type')}")
            
        else:
            print(f"❌ Error obteniendo datos: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def main():
    print("🍿 DIAGNÓSTICO DE SESIÓN DE USUARIO")
    print("=" * 50)
    
    # Probar login y verificar datos
    user_data = test_login_and_check_session()
    
    if user_data:
        # Verificar datos en backend
        check_backend_user_data()
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN:")
    print("Si el usuario NO aparece como moderador, el problema puede ser:")
    print("1. Campo 'userType' no se está enviando desde el backend")
    print("2. Campo se llama 'user_type' en lugar de 'userType'")
    print("3. Valor no es exactamente 'moderator'")
    print("\n🔧 Solución: Verificar el backend para asegurar que envía 'userType': 'moderator'")

if __name__ == "__main__":
    main() 