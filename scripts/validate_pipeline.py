#!/usr/bin/env python3
"""
Script de validación del pipeline de CI/CD
Verifica que todos los componentes necesarios estén presentes y configurados correctamente
"""

import os
import sys
import yaml
import subprocess
from pathlib import Path

def check_file_exists(file_path, description):
    """Verifica que un archivo exista"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NO ENCONTRADO")
        return False

def check_yaml_syntax(file_path):
    """Verifica la sintaxis YAML de un archivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        print(f"✅ Sintaxis YAML válida: {file_path}")
        return True
    except yaml.YAMLError as e:
        print(f"❌ Error de sintaxis YAML en {file_path}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error al leer {file_path}: {e}")
        return False

def check_python_syntax(file_path):
    """Verifica la sintaxis Python de un archivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            compile(f.read(), file_path, 'exec')
        print(f"✅ Sintaxis Python válida: {file_path}")
        return True
    except SyntaxError as e:
        print(f"❌ Error de sintaxis Python en {file_path}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error al leer {file_path}: {e}")
        return False

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    try:
        import pytest
        import requests
        import jsonschema
        print("✅ Dependencias principales instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        return False

def main():
    """Función principal de validación"""
    print("🔍 Validando configuración del pipeline...")
    print("=" * 50)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    all_checks_passed = True
    
    # Verificar archivos esenciales
    essential_files = [
        (".github/workflows/suit_tests.yml", "Pipeline de CI/CD"),
        ("requirements.tx", "Dependencias de Python"),
        ("pytest.ini", "Configuración de pytest"),
        ("conftest.py", "Configuración de pytest"),
        ("pyproject.toml", "Configuración del proyecto"),
        (".bandit", "Configuración de seguridad"),
        (".flake8", "Configuración de linting"),
    ]
    
    for file_path, description in essential_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    
    print("\n" + "=" * 50)
    print("🔍 Validando sintaxis de archivos...")
    
    # Verificar sintaxis YAML
    yaml_files = [
        ".github/workflows/suit_tests.yml",
        ".github/workflows/test-config.yml"
    ]
    
    for file_path in yaml_files:
        if os.path.exists(file_path):
            if not check_yaml_syntax(file_path):
                all_checks_passed = False
    
    # Verificar sintaxis Python
    python_files = [
        "conftest.py",
        "scripts/validate_pipeline.py"
    ]
    
    for file_path in python_files:
        if os.path.exists(file_path):
            if not check_python_syntax(file_path):
                all_checks_passed = False
    
    print("\n" + "=" * 50)
    print("🔍 Validando dependencias...")
    
    if not check_dependencies():
        all_checks_passed = False
    
    print("\n" + "=" * 50)
    print("📊 Resumen de validación:")
    
    if all_checks_passed:
        print("✅ ¡Todas las validaciones pasaron! El pipeline está listo.")
        return 0
    else:
        print("❌ Algunas validaciones fallaron. Revisa los errores arriba.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
