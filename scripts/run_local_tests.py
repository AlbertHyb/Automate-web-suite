#!/usr/bin/env python3
"""
Script para ejecutar las pruebas localmente de manera similar al pipeline
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"\n🔧 {description}")
    print(f"Comando: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Comando ejecutado exitosamente")
        if result.stdout:
            print("Salida:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en comando: {e}")
        if e.stdout:
            print("Salida:", e.stdout)
        if e.stderr:
            print("Error:", e.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Ejecutar pruebas localmente")
    parser.add_argument("--test-type", choices=["all", "api", "security", "lint"], 
                       default="all", help="Tipo de pruebas a ejecutar")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Ejecutar en modo verbose")
    
    args = parser.parse_args()
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("🚀 Ejecutando pruebas localmente...")
    print(f"Directorio de trabajo: {os.getcwd()}")
    print("=" * 60)
    
    # Crear directorios necesarios
    os.makedirs("reports", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    success = True
    
    if args.test_type in ["all", "api"]:
        # Instalar dependencias
        if not run_command("pip install -r requirements.tx", "Instalando dependencias"):
            success = False
        
        # Ejecutar pruebas
        pytest_cmd = "pytest api/tests/ -v --html=reports/local_report.html --self-contained-html"
        if args.verbose:
            pytest_cmd += " -s"
        
        if not run_command(pytest_cmd, "Ejecutando pruebas de API"):
            success = False
    
    if args.test_type in ["all", "security"] and success:
        # Instalar herramientas de seguridad
        if not run_command("pip install bandit safety", "Instalando herramientas de seguridad"):
            success = False
        
        # Ejecutar Bandit
        if not run_command("bandit -r api/ -f txt -o reports/bandit-local.txt", "Ejecutando análisis de seguridad (Bandit)"):
            success = False
        
        # Ejecutar Safety
        if not run_command("safety check --output reports/safety-local.txt", "Verificando dependencias (Safety)"):
            success = False
    
    if args.test_type in ["all", "lint"] and success:
        # Instalar herramientas de linting
        if not run_command("pip install black flake8 isort", "Instalando herramientas de linting"):
            success = False
        
        # Ejecutar Black
        if not run_command("black --check --diff api/", "Verificando formato de código (Black)"):
            print("💡 Ejecuta 'black api/' para formatear el código")
        
        # Ejecutar isort
        if not run_command("isort --check-only --diff api/", "Verificando orden de imports (isort)"):
            print("💡 Ejecuta 'isort api/' para ordenar los imports")
        
        # Ejecutar Flake8
        if not run_command("flake8 api/", "Ejecutando análisis de estilo (Flake8)"):
            success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ¡Todas las pruebas se ejecutaron exitosamente!")
        print("📊 Revisa los reportes en el directorio 'reports/'")
    else:
        print("❌ Algunas pruebas fallaron. Revisa los errores arriba.")
        sys.exit(1)

if __name__ == "__main__":
    main()
