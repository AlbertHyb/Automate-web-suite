# Automated Testing Suite

## Descripción
Suite de pruebas automatizadas para validar la funcionalidad de la API de autenticación y aeropuertos. Incluye pruebas de:
- Autenticación (login/signup)
- Gestión de aeropuertos
- Validaciones de esquemas JSON

## Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Acceso a la API (cf-automation-airline-api.onrender.com)

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tuusuario/automated-testing-suite.git
cd automated-testing-suite
```

2. Crea y activa un entorno virtual:
```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno:
- Copia el archivo `.env.example` a `.env` (si existe) o crea uno nuevo.
- Agrega las siguientes variables mínimas:

```
ADMIN_USER=admin@demo.com
ADMIN_PASS=admin123
API_PROTOCOL=https
API_HOST=cf-automation-airline-api.onrender.com
API_BASE_PATH=/
API_VERSION=v1
SIGNUP_STATUS_EMAIL=test_status_check@gmail.com
SIGNUP_STATUS_PASS=Test1234!
SIGNUP_STATUS_NAME=Status Check
```

> **Nota:** El archivo `.env` está en `.gitignore` y no debe subirse al repositorio.

## Estructura del Proyecto
```
Automate-web-suite/
├── api/
│   ├── api_helper.py
│   ├── schemas/
│   └── tests/
│       ├── auth_login.py
│       ├── auth_signup.py
│       ├── conftest.py
│       └── ...
├── config/
│   ├── settings.py
│   └── ...
├── utils/
├── pages/
├── features/
├── requirements.txt
├── .env (no subir)
└── README.md
```

## Ejecución de Pruebas

### Todas las pruebas:
```bash
pytest
```

### Pruebas específicas:
```bash
pytest api/tests/auth_login.py -v
pytest api/tests/auth_signup.py -v
pytest api/tests/test_airports.py -v
```

### Generar reporte HTML:
```bash
pytest --html=reports/report.html
```

## Configuración Centralizada
Toda la configuración y las variables sensibles se gestionan desde `config/settings.py`, que carga automáticamente las variables del archivo `.env` usando `python-dotenv`. No es necesario modificar los tests para cambiar credenciales o endpoints, solo actualiza el `.env`.

## Escenarios Cubiertos

### Autenticación
- Login exitoso
- Credenciales inválidas
- Campos faltantes
- Formatos inválidos

### Aeropuertos
- Creación exitosa
- Validación de códigos IATA
- Manejo de duplicados
- Actualizaciones y eliminaciones

## Contribución
1. Haz fork del repositorio
2. Crea una rama feature: `git checkout -b feature/nueva-caracteristica`
3. Agrega tus cambios: `git add .`
4. Haz commit de tus cambios: `git commit -m 'Añadir nueva característica'`
5. Haz push a la rama: `git push origin feature/nueva-caracteristica`
6. Crea un Pull Request

## Licencia
MIT
