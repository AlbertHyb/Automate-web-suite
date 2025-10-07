import os
import sys


def main():
    try:
        name = os.getenv("USERNAME", "Usuario")
        print(f"Hello, {name}! Estoy en GitHub Actions")
        print("Script ejecutado correctamente")
        return 0
    except Exception as e:
        print(f"Error en el script: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())