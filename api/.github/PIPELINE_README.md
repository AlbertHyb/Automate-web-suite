# Pipeline de CI/CD - Automate Web Suite

## Descripción
Este pipeline automatiza las pruebas, análisis de seguridad y calidad de código para el proyecto de automatización de pruebas de API.

## Estructura del Pipeline

### Jobs Principales

#### 1. **test** - Ejecución de Pruebas
- **Versiones de Python**: 3.11, 3.12
- **Estrategia**: Matrix para probar en múltiples versiones
- **Funcionalidades**:
  - Instalación de dependencias con cache
  - Ejecución de pruebas con pytest
  - Generación de reportes HTML y JUnit
  - Análisis de cobertura de código
  - Subida de artefactos

#### 2. **security-scan** - Análisis de Seguridad
- **Dependencia**: Ejecuta después de `test`
- **Herramientas**:
  - **Bandit**: Análisis estático de seguridad Python
  - **Safety**: Verificación de vulnerabilidades en dependencias
- **Reportes**: JSON y TXT para ambos análisis

#### 3. **lint** - Análisis de Calidad de Código
- **Herramientas**:
  - **Black**: Formateo de código
  - **isort**: Ordenamiento de imports
  - **Flake8**: Análisis de estilo y errores
- **Ejecución**: Paralela con otros jobs

### Triggers del Pipeline

```yaml
on:
  push:
    branches: ["main", "gha-prueba"]
  pull_request:
    branches: ["main"]
  workflow_dispatch:  # Ejecución manual
  schedule:
    - cron: "0 4 * * *"  # Diario a las 4:00 AM UTC
```

### Configuraciones

#### Variables de Entorno
- `BASE_URL`: https://cf-automation-airline-api.onrender.com
- `ENVIRONMENT`: test

#### Cache
- **Dependencias pip**: Cache automático para acelerar builds
- **Clave**: Basada en hash del archivo requirements.tx

### Reportes Generados

1. **Reportes de Pruebas**:
   - HTML: `reports/report_{run_number}.html`
   - JUnit: `reports/junit.xml`
   - Cobertura: `reports/coverage/`

2. **Reportes de Seguridad**:
   - Bandit: `reports/bandit-report.{json,txt}`
   - Safety: `reports/safety-report.{json,txt}`

3. **Artefactos**:
   - `test-results-{python-version}`
   - `coverage-reports-{python-version}`
   - `security-reports`

### Herramientas de Desarrollo

#### Scripts Incluidos
- `scripts/validate_pipeline.py`: Validación del pipeline

#### Archivos de Configuración
- `.bandit`: Configuración de análisis de seguridad
- `.flake8`: Configuración de linting
- `.safety`: Configuración de verificación de dependencias
- `pyproject.toml`: Configuración unificada del proyecto

### Manejo de Errores

- **Concurrency**: Cancela builds anteriores si hay nuevos commits
- **Artifacts**: Se suben siempre, incluso si las pruebas fallan
- **Security scans**: Continúan ejecutándose aunque fallen (`|| true`)

### Métricas y Monitoreo

- **Cobertura de código**: Reportes HTML y XML
- **Tiempo de ejecución**: Visible en GitHub Actions
- **Tasa de éxito**: Historial en la pestaña Actions

### Flujo de Trabajo Recomendado

1. **Desarrollo local**:
   ```bash
   # Validar pipeline localmente
   python scripts/validate_pipeline.py
   
   # Ejecutar pruebas
   pytest api/tests/
   
   # Verificar formato
   black --check api/
   flake8 api/
   ```

2. **Push a rama**:
   - Pipeline se ejecuta automáticamente
   - Revisar reportes en GitHub Actions

3. **Pull Request**:
   - Pipeline ejecuta todas las validaciones
   - Revisar cambios en la pestaña "Checks"

4. **Merge a main**:
   - Pipeline ejecuta y sube artefactos
   - Reportes disponibles para descarga

### Troubleshooting

#### Problemas Comunes

1. **Fallo en instalación de dependencias**:
   - Verificar que `requirements.tx` esté actualizado
   - Revisar cache de pip

2. **Fallo en pruebas**:
   - Revisar logs en GitHub Actions
   - Verificar conectividad con API externa

3. **Fallo en security scan**:
   - Revisar reportes de Bandit/Safety
   - Actualizar dependencias vulnerables

4. **Fallo en linting**:
   - Ejecutar `black api/` para formatear
   - Ejecutar `isort api/` para ordenar imports

### Recursos Adicionales

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Black Documentation](https://black.readthedocs.io/)
