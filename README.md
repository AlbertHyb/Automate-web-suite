# Automated Testing Suite

## Descripción
Suite de pruebas automatizadas completa que incluye:

### **Pruebas de API**
- Autenticación (login/signup)
- Gestión de usuarios (creación, actualización, listado)
- Gestión de aeropuertos
- Validaciones de esquemas JSON

### **Pruebas de UI (Interfaz Web)**
- Automatización con Selenium WebDriver
- Pruebas BDD con Behave (Behavior Driven Development)
- Validación de funcionalidades de interfaz web

## Tecnologías Utilizadas
- **Python 3.8+** - Lenguaje principal
- **Pytest** - Framework de pruebas para API
- **Behave** - Framework BDD para pruebas de UI
- **Selenium WebDriver** - Automatización de navegadores
- **Requests** - Cliente HTTP para pruebas de API
- **JSONSchema** - Validación de esquemas JSON

## Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web (Chrome, Firefox, Edge)
- WebDriver correspondiente al navegador
- Acceso a la API (cf-automation-airline-api.onrender.com)

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/AlbertHyb/Automate-web-suite.git
cd Automate-web-suite
```

2. Crea y activa un entorno virtual:
```bash
python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno:
- Crea un archivo `.env` en la raíz del proyecto
- Agrega las siguientes variables:

```
# Configuración de API
ADMIN_USER=admin@admin.com
ADMIN_PASS=admin
API_PROTOCOL=https
API_HOST=cf-automation-airline-api.onrender.com
API_BASE_PATH=/
API_VERSION=
SIGNUP_STATUS_EMAIL=test_status_check@gmail.com
SIGNUP_STATUS_PASS=Test1234!
SIGNUP_STATUS_NAME=Status Check

# Configuración de UI
BASE_URL=https://fake-cinema-v0.onrender.com
BROWSER=chrome
HEADLESS=false
```

> **Nota:** El archivo `.env` está en `.gitignore` y no debe subirse al repositorio.

## Estructura del Proyecto
```
Automate-web-suite/
├── api/                          # Pruebas de API
│   ├── api_helper.py            # Cliente HTTP helper
│   ├── schemas/                 # Esquemas de validación JSON
│   │   ├── login_schemas.py
│   │   ├── signup_schemas.py
│   │   ├── user_update_put_schema.py
│   │   └── airport_schemas.py
│   └── tests/                   # Tests de API con Pytest
│       ├── conftest.py         # Configuración de fixtures
│       ├── auth_login.py       # Tests de autenticación
│       ├── auth_signup.py      # Tests de registro
│       ├── user_update_put.py  # Tests de actualización de usuarios
│       ├── test_airports.py    # Tests de aeropuertos
│       └── ...
├── features/                    # Pruebas BDD con Behave
│   ├── login.feature           # Scenarios de login en Gherkin
│   ├── environment.py          # Configuración de Behave
│   └── steps/                  # Implementación de steps
│       └── test_login_steps.py
├── pages/                      # Page Object Model
│   └── base_page.py           # Clase base para páginas
├── utils/                      # Utilidades compartidas
│   ├── driver_factory.py      # Factory para WebDrivers
│   └── conftest.py
├── config/                     # Configuración centralizada
│   └── settings.py
├── debug_api_status.py         # Script de monitoreo de API
├── pytest.ini                 # Configuración de Pytest
├── requirements.txt
└── README.md
```

## Ejecución de Pruebas

Las pruebas se ejecutan automáticamente en GitHub Actions cuando se hace push a las ramas `main` o `gha-prueba`, o cuando se crea un Pull Request.

### **Pipeline de CI/CD**

El pipeline incluye:
- **Pruebas de API**: Ejecutadas con Pytest en Python 3.11 y 3.12
- **Análisis de seguridad**: Bandit y Safety
- **Análisis de calidad**: Black, isort y Flake8
- **Generación de reportes**: HTML, JUnit XML y cobertura de código

### **Monitoreo de Estado**

Para verificar el estado de las pruebas:
1. Ve a la pestaña "Actions" en GitHub
2. Revisa el estado del último workflow
3. Descarga los artefactos para ver reportes detallados

## Escenarios de Prueba

### **API Testing**

#### **Autenticación**
- Login exitoso con credenciales válidas
- Login con credenciales inválidas
- Login con campos faltantes
- Login con formatos incorrectos

#### **Registro de Usuarios**
- Registro exitoso con datos válidos
- Registro con email duplicado
- Registro con formato de email inválido
- Registro con contraseña débil

#### **Gestión de Usuarios**
- Actualización de perfil de usuario (PUT /users/{id})
- Obtener información del usuario actual (GET /users/me)
- Listar usuarios (GET /users)
- Creación de usuarios por admin

#### **Gestión de Aeropuertos**
- Creación de aeropuertos
- Validación de códigos IATA
- Manejo de duplicados
- Actualizaciones y eliminaciones

###  **UI Testing (BDD)**

#### **Navegación Web**
```gherkin
Feature: Acceso al sitio Fake Cinema

  Scenario: El usuario abre la página principal
    Given que el usuario abre el navegador
    When accede a la página de inicio
    Then la página debería cargar con el título correcto
```

#### **Características de los Tests BDD:**
- **Page Object Model** - Patrón de diseño para mantenibilidad
- **Driver Factory** - Soporte para múltiples navegadores (Chrome, Firefox, Edge)
- **Configuración flexible** - Modo headless y configuración por variables de entorno
- **Hooks de Behave** - Setup y teardown automático de navegadores

## Configuración Avanzada

### **Pytest Configuration**
```ini
[pytest]
pythonpath = .
testpaths = api/tests
python_files = test_*.py auth_*.py
markers =
    smoke: pruebas básicas de funcionalidad
    integration: pruebas de integración
    api: pruebas de API
    ui: pruebas de interfaz de usuario
```

### **Behave Configuration**
- **environment.py** - Configuración de hooks y setup
- **Driver Factory** - Creación automática de WebDrivers
- **Base Page** - Clase base con métodos comunes de UI

### **Variables de Entorno Soportadas**
```bash
# API
BASE_URL=https://cf-automation-airline-api.onrender.com
ADMIN_USER=admin@admin.com
ADMIN_PASS=admin

# UI
BROWSER=chrome|firefox|edge
HEADLESS=true|false
IMPLICIT_WAIT=10
PAGE_LOAD_TIMEOUT=30
```

## Debugging y Troubleshooting

### **Problemas Comunes**

1. **Fallo en el pipeline de GitHub Actions**:
   - Revisa los logs en la pestaña "Actions"
   - Verifica que la API esté disponible
   - Revisa los reportes de seguridad y linting

2. **Problemas de conectividad con la API**:
   - Verifica que `https://cf-automation-airline-api.onrender.com` esté disponible
   - Revisa los logs del workflow para errores de conexión

3. **Fallo en análisis de código**:
   - Revisa los reportes de Black, isort y Flake8
   - Corrige los problemas de formato y estilo

## Reportes

Los reportes se generan automáticamente en GitHub Actions y están disponibles como artefactos:

### **Reportes de Pruebas**
- **HTML**: `reports/report_{run_number}.html`
- **JUnit XML**: `reports/junit.xml`
- **Cobertura**: `reports/coverage/`

### **Reportes de Seguridad**
- **Bandit**: `reports/bandit-report.{json,txt}`
- **Safety**: `reports/safety-report.{json,txt}`

### **Acceso a Reportes**
1. Ve a la pestaña "Actions" en GitHub
2. Selecciona el workflow que deseas revisar
3. Descarga los artefactos correspondientes

## Integración Continua

### **Configuración del Pipeline**

El pipeline está configurado en `.github/workflows/suit_tests.yml` e incluye:

- **Triggers**: Push a `main`/`gha-prueba`, Pull Requests, ejecución manual y programada
- **Versiones de Python**: 3.11 y 3.12
- **Jobs**: Pruebas, análisis de seguridad y linting
- **Artefactos**: Reportes HTML, JUnit XML y cobertura de código

### **Configuración de Variables de Entorno**
```yaml
env:
  BASE_URL: https://cf-automation-airline-api.onrender.com
  ENVIRONMENT: test
```

## Contribución

### **Para Tests de API**
1. Crear tests en `api/tests/`
2. Definir schemas en `api/schemas/`
3. Usar fixtures de `conftest.py`
4. Seguir convenciones de naming: `test_*.py`

### **Para Tests de UI**
1. Crear features en `features/*.feature`
2. Implementar steps en `features/steps/`
3. Usar Page Object Model en `pages/`
4. Seguir sintaxis Gherkin para scenarios

### **Proceso de Contribución**
1. Fork del repositorio
2. Crear rama feature: `git checkout -b feature/nueva-caracteristica`
3. Agregar tests y documentación
4. Commit: `git commit -m 'feat: descripción de la característica'`
5. Push: `git push origin feature/nueva-caracteristica`
6. Crear Pull Request

## Licencia
MIT License - Ver archivo LICENSE para más detalles

---

## Recursos Adicionales

- **Pytest Documentation**: https://docs.pytest.org/
- **Behave Documentation**: https://behave.readthedocs.io/
- **Selenium Documentation**: https://selenium-python.readthedocs.io/
- **Gherkin Syntax**: https://cucumber.io/docs/gherkin/
