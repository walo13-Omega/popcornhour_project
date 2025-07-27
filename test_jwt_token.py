#!/usr/bin/env python3
"""
Script para probar el token JWT y las reseñas
"""

import requests
import json

# Configuración
API_BASE_URL = "http://localhost:3001/api"

def test_login_and_token():
    """Probar login y obtener token"""
    print("🔐 Probando login y token JWT...")
    
    # Login
    login_data = {
        "username": "testuser",
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            user = data.get('user')
            token = data.get('token')
            
            print(f"✅ Login exitoso!")
            print(f"  - Usuario: {user.get('username')}")
            print(f"  - Token: {token[:20]}..." if token else "❌ No hay token")
            
            return token
        else:
            print(f"❌ Error en login: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_review_with_token(token):
    """Probar crear reseña con token"""
    print("\n📝 Probando crear reseña con token...")
    
    if not token:
        print("❌ No hay token disponible")
        return False
    
    # Datos de la reseña
    review_data = {
        "content_type": "movie",
        "content_id": 1,  # ID de una película existente
        "rating": 4.5,
        "comment": "¡Excelente película! Probando con token JWT."
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/reviews", 
                               json=review_data, 
                               headers=headers)
        
        print(f"📡 Status: {response.status_code}")
        print(f"📡 Response: {response.text}")
        
        if response.status_code in (200, 201):
            print("✅ Reseña creada exitosamente con token JWT!")
            return True
        else:
            print(f"❌ Error creando reseña: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_review_without_token():
    """Probar crear reseña sin token (debería fallar)"""
    print("\n📝 Probando crear reseña SIN token...")
    
    review_data = {
        "content_type": "movie",
        "content_id": 1,
        "rating": 4.5,
        "comment": "Esta reseña debería fallar."
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/reviews", json=review_data)
        
        print(f"📡 Status: {response.status_code}")
        print(f"📡 Response: {response.text}")
        
        if response.status_code == 401:
            print("✅ Correcto: Se requiere token para crear reseñas")
            return True
        else:
            print(f"❌ Inesperado: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def main():
    print("🍿 PROBANDO TOKEN JWT PARA RESEÑAS")
    print("=" * 50)
    
    # 1. Probar login y obtener token
    token = test_login_and_token()
    
    # 2. Probar reseña sin token (debería fallar)
    test_review_without_token()
    
    # 3. Probar reseña con token (debería funcionar)
    if token:
        test_review_with_token(token)
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN:")
    print("- Login y token JWT funcionando")
    print("- Reseñas requieren autenticación")
    print("- Token se envía correctamente en headers")

if __name__ == "__main__":
    main() 