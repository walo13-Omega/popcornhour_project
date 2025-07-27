#!/usr/bin/env python3
"""
Script para automatizar capturas de pantalla de PopcornHour
"""

import requests
import time
import os
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5000"
SCREENSHOTS_DIR = "Entregables/Checkpoint3-Capturas"

def create_directories():
    """Crear directorios necesarios"""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs("Entregables/Checkpoint4-Videos", exist_ok=True)
    os.makedirs("Entregables/Checkpoint5-Videos", exist_ok=True)

def test_page_accessibility():
    """Probar que las páginas son accesibles"""
    print("🔍 Probando accesibilidad de páginas...")
    
    pages = [
        ("/", "Página de inicio sin sesión"),
        ("/login", "Formulario de login"),
        ("/register", "Formulario de registro"),
        ("/movies", "Página de películas"),
        ("/series", "Página de series"),
        ("/foro", "Página del foro")
    ]
    
    accessible_pages = []
    
    for route, description in pages:
        try:
            response = requests.get(f"{BASE_URL}{route}")
            if response.status_code == 200:
                print(f"  ✅ {description}: {route}")
                accessible_pages.append((route, description))
            else:
                print(f"  ❌ {description}: {route} (Status: {response.status_code})")
        except Exception as e:
            print(f"  ❌ {description}: {route} (Error: {e})")
    
    return accessible_pages

def generate_screenshot_instructions():
    """Generar instrucciones para capturas de pantalla"""
    print("\n📸 INSTRUCCIONES PARA CAPTURAS DE PANTALLA")
    print("=" * 60)
    
    print("\n🎯 CHECKPOINT 3 - Capturas Requeridas:")
    print("1. Página de inicio sin sesión")
    print("   - URL: http://localhost:5000")
    print("   - Guardar como: 01-home-sin-sesion.png")
    
    print("\n2. Página de inicio con sesión (usuario estándar)")
    print("   - Login con: testuser / 123456")
    print("   - Guardar como: 02-home-con-sesion-usuario.png")
    
    print("\n3. Página de inicio con sesión (moderador)")
    print("   - Login con: superadmin / 123456")
    print("   - Guardar como: 03-home-con-sesion-moderador.png")
    
    print("\n4. Formulario de login")
    print("   - URL: http://localhost:5000/login")
    print("   - Guardar como: 04-formulario-login.png")
    
    print("\n5. Formulario de registro")
    print("   - URL: http://localhost:5000/register")
    print("   - Guardar como: 05-formulario-registro.png")

def generate_video_instructions():
    """Generar instrucciones para videos"""
    print("\n🎬 INSTRUCCIONES PARA VIDEOS")
    print("=" * 60)
    
    print("\n🎯 CHECKPOINT 3 - Video de Flujo Completo:")
    print("1. Abrir http://localhost:5000")
    print("2. Mostrar página principal")
    print("3. Hacer clic en 'Registrarse'")
    print("4. Llenar formulario de registro")
    print("5. Mostrar registro exitoso")
    print("6. Hacer clic en 'Iniciar Sesión'")
    print("7. Llenar formulario de login")
    print("8. Mostrar login exitoso")
    print("9. Guardar como: Checkpoint3-flujo-completo.mp4")
    
    print("\n🎯 CHECKPOINT 4 - Videos de Autenticación:")
    print("\nVideo 1 - Registro:")
    print("1. Ir a /register")
    print("2. Crear nuevo usuario")
    print("3. Mostrar mensaje de éxito")
    print("4. Guardar como: Checkpoint4-01-registro.mp4")
    
    print("\nVideo 2 - Login:")
    print("1. Ir a /login")
    print("2. Login con usuario existente")
    print("3. Mostrar acceso al perfil")
    print("4. Guardar como: Checkpoint4-02-login.mp4")
    
    print("\nVideo 3 - Persistencia de Sesión:")
    print("1. Estar logueado")
    print("2. Recargar página")
    print("3. Ir a /profile")
    print("4. Mostrar que la sesión persiste")
    print("5. Guardar como: Checkpoint4-03-persistencia.mp4")
    
    print("\n🎯 CHECKPOINT 5 - Video de Página Dinámica:")
    print("1. Mostrar página sin sesión")
    print("2. Hacer login")
    print("3. Mostrar cambios en la interfaz")
    print("4. Navegar por películas/series")
    print("5. Mostrar interacciones (reseñas, foro)")
    print("6. Guardar como: Checkpoint5-pagina-dinamica.mp4")

def generate_test_scenarios():
    """Generar escenarios de prueba"""
    print("\n🧪 ESCENARIOS DE PRUEBA")
    print("=" * 60)
    
    print("\n👤 Usuario Estándar (testuser / 123456):")
    print("- ✅ Navegar por películas y series")
    print("- ✅ Hacer reseñas")
    print("- ✅ Participar en foro")
    print("- ✅ Ver perfil personal")
    print("- ❌ Acceder a funciones de moderador")
    
    print("\n👑 Moderador (superadmin / 123456):")
    print("- ✅ Todas las funciones de usuario estándar")
    print("- ✅ Panel de moderador visible")
    print("- ✅ Agregar películas y series")
    print("- ✅ Editar contenido existente")
    print("- ✅ Eliminar contenido")
    print("- ✅ Moderar foro")

def main():
    print("🍿 GENERADOR DE INSTRUCCIONES PARA CAPTURAS Y VIDEOS")
    print("=" * 60)
    
    # Crear directorios
    create_directories()
    
    # Probar accesibilidad
    accessible_pages = test_page_accessibility()
    
    # Generar instrucciones
    generate_screenshot_instructions()
    generate_video_instructions()
    generate_test_scenarios()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE ENTREGABLES")
    print("=" * 60)
    
    print(f"\n✅ Páginas accesibles: {len(accessible_pages)}/6")
    print("✅ Estructura de directorios creada")
    print("✅ Instrucciones generadas")
    
    print("\n📁 Archivos a crear:")
    print("- Entregables/Checkpoint3-Capturas/ (5 capturas)")
    print("- Entregables/Checkpoint3-Video/ (1 video)")
    print("- Entregables/Checkpoint4-Videos/ (3 videos)")
    print("- Entregables/Checkpoint5-Videos/ (1 video)")

if __name__ == "__main__":
    main() 