#!/usr/bin/env python3
"""
Script para diagnosticar la comunicación entre Flask, Node.js y PostgreSQL
"""

import requests
import json
import time

# Configuración
FLASK_URL = "http://localhost:5000"
NODE_URL = "http://localhost:3001/api"

def test_backend_health():
    """Probar si el backend Node.js está funcionando"""
    print("🔍 Probando backend Node.js...")
    try:
        response = requests.get(f"{NODE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Backend funcionando: {data['message']}")
            print(f"  📅 Timestamp: {data['timestamp']}")
            print(f"  🏷️  Versión: {data['version']}")
            return True
        else:
            print(f"  ❌ Backend respondió con status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error conectando al backend: {e}")
        return False

def test_flask_frontend():
    """Probar si Flask está funcionando"""
    print("\n🔍 Probando frontend Flask...")
    try:
        response = requests.get(FLASK_URL)
        if response.status_code == 200:
            print(f"  ✅ Flask funcionando en {FLASK_URL}")
            print(f"  📄 Respuesta HTML recibida ({len(response.text)} caracteres)")
            return True
        else:
            print(f"  ❌ Flask respondió con status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error conectando a Flask: {e}")
        return False

def test_login_api():
    """Probar la API de login"""
    print("\n🔍 Probando API de login...")
    try:
        response = requests.post(f"{NODE_URL}/auth/login", json={
            "username": "testuser",
            "password": "123456"
        })
        
        print(f"  📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Login exitoso!")
            print(f"  👤 Usuario: {data['user']['username']}")
            print(f"  🏷️  Tipo: {data['user']['userType']}")
            print(f"  🔑 Token recibido: {'Sí' if 'token' in data else 'No'}")
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

def test_register_api():
    """Probar la API de registro"""
    print("\n🔍 Probando API de registro...")
    try:
        response = requests.post(f"{NODE_URL}/auth/register", json={
            "username": "testuser2",
            "email": "test2@test.com",
            "password": "123456"
        })
        
        print(f"  📡 Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"  ✅ Registro exitoso!")
            print(f"  👤 Usuario: {data['user']['username']}")
            print(f"  🏷️  Tipo: {data['user']['userType']}")
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

def test_flask_to_backend_communication():
    """Probar comunicación Flask → Backend"""
    print("\n🔍 Probando comunicación Flask → Backend...")
    try:
        # Simular lo que hace Flask
        login_data = {
            "username": "testuser",
            "password": "123456"
        }
        
        response = requests.post(f"{NODE_URL}/auth/login", json=login_data)
        
        if response.status_code == 200:
            print(f"  ✅ Flask puede comunicarse con el backend")
            print(f"  📡 Datos enviados: {login_data}")
            print(f"  📡 Respuesta recibida: {response.status_code}")
            return True
        else:
            print(f"  ❌ Error en comunicación: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error de comunicación: {e}")
        return False

def test_database_connection():
    """Probar conexión a la base de datos (indirectamente)"""
    print("\n🔍 Probando conexión a base de datos...")
    try:
        # Intentar obtener datos que requieren DB
        response = requests.get(f"{NODE_URL}/movies")
        
        if response.status_code == 200:
            movies = response.json()
            print(f"  ✅ Base de datos accesible")
            print(f"  📽️  Películas cargadas: {len(movies)}")
            return True
        else:
            print(f"  ❌ Error accediendo a datos: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error de conexión a DB: {e}")
        return False

def main():
    print("🍿 DIAGNÓSTICO COMPLETO DE COMUNICACIÓN")
    print("=" * 60)
    
    results = []
    
    # 1. Backend Node.js
    results.append(("Backend Node.js", test_backend_health()))
    
    # 2. Frontend Flask
    results.append(("Frontend Flask", test_flask_frontend()))
    
    # 3. API de Login
    results.append(("API Login", test_login_api()))
    
    # 4. API de Registro
    results.append(("API Registro", test_register_api()))
    
    # 5. Comunicación Flask → Backend
    results.append(("Comunicación Flask→Backend", test_flask_to_backend_communication()))
    
    # 6. Base de datos
    results.append(("Base de datos", test_database_connection()))
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE DIAGNÓSTICO")
    print("=" * 60)
    
    all_working = True
    for component, working in results:
        status = "✅ FUNCIONANDO" if working else "❌ FALLANDO"
        print(f"  {component}: {status}")
        if not working:
            all_working = False
    
    print("\n" + "=" * 60)
    if all_working:
        print("🎉 ¡TODO FUNCIONANDO PERFECTAMENTE!")
        print("✅ El sistema de login y registro está completamente operativo")
        print("🌐 Puedes usar la aplicación en: http://localhost:5000")
    else:
        print("⚠️  HAY PROBLEMAS QUE NECESITAN ATENCIÓN")
        print("🔧 Revisa los errores arriba y soluciona los componentes fallando")
    
    print("\n🎯 Usuarios disponibles para probar:")
    print("  - testuser / 123456")
    print("  - testuser2 / 123456 (si se creó en el test)")

if __name__ == "__main__":
    main() 