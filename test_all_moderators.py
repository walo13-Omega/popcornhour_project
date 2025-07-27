#!/usr/bin/env python3
"""
Script para probar todos los usuarios moderadores
"""

import requests
import json

# Configuración del backend
API_BASE_URL = "http://localhost:3001/api"

def test_moderator_login(username, password):
    """Probar login de un moderador específico"""
    print(f"🔍 Probando moderador: {username}")
    
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login", json={
            "username": username,
            "password": password
        })
        
        print(f"  📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            user = data.get('user', {})
            
            print(f"  ✅ Login exitoso!")
            print(f"  📋 Datos:")
            print(f"    - ID: {user.get('id')}")
            print(f"    - Username: {user.get('username')}")
            print(f"    - userType: {user.get('userType')}")
            
            # Verificar si es moderador
            user_type = user.get('userType')
            is_moderator = user_type == 'moderator'
            
            print(f"    - ¿Es moderador?: {is_moderator}")
            
            if is_moderator:
                print(f"  ✅ {username} SÍ es moderador")
            else:
                print(f"  ❌ {username} NO es moderador")
            
            return is_moderator
            
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
    print("🍿 PROBANDO TODOS LOS MODERADORES")
    print("=" * 50)
    
    # Lista de moderadores conocidos
    moderators = [
        ('admin', '123456'),
        ('moderator1', '123456'),
        ('moderator2', '123456'),
        ('superadmin', '123456')
    ]
    
    working_moderators = []
    
    for username, password in moderators:
        is_moderator = test_moderator_login(username, password)
        if is_moderator:
            working_moderators.append((username, password))
        print()
    
    print("=" * 50)
    print("📊 RESUMEN:")
    print(f"✅ Moderadores que funcionan: {len(working_moderators)}/{len(moderators)}")
    
    if working_moderators:
        print("\n🎯 Moderadores disponibles:")
        for username, password in working_moderators:
            print(f"  - {username} / {password}")
    
    print("\n🔧 Si todos los moderadores funcionan en el backend pero no en Flask:")
    print("  - El problema está en la sesión de Flask")
    print("  - Necesitas cerrar sesión y volver a iniciar")
    print("  - O reiniciar Flask para limpiar la sesión")

if __name__ == "__main__":
    main() 