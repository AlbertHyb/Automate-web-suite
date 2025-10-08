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


## Recursos Adicionales

- **Pytest Documentation**: https://docs.pytest.org/
- **Behave Documentation**: https://behave.readthedocs.io/
- **Selenium Documentation**: https://selenium-python.readthedocs.io/
- **Gherkin Syntax**: https://cucumber.io/docs/gherkin/
