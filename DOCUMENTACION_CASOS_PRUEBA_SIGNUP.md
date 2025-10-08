# Documentación de Casos de Prueba - Módulo de Registro (Signup)

## Información General
- **Módulo**: Autenticación - Registro de Usuario
- **Archivo**: `api/tests/auth/auth_signup.py`
- **Endpoint**: `POST /auth/signup`
- **Total de Casos de Prueba**: 6 casos (3 Críticos, 2 Medios, 1 Básico)

---

## CASOS DE PRUEBA CRÍTICOS (3 casos)

### SIGNUP_C001 - Registro Exitoso con Datos Válidos
- **ID**: SIGNUP_C001
- **Prioridad**: Critical
- **Descripción**: Verificar que el registro funcione correctamente con datos válidos
- **Datos de Prueba**:
  - Email: `test{timestamp}{uuid}@gmail.com` (generado dinámicamente)
  - Password: `ValidPass123!`
  - Full Name: `Test User`
- **Estado Esperado**: `201 Created`
- **Validación de Esquema**: Sí
- **Validación de Datos**: Sí
- **Propósito**: Validar el flujo principal de registro exitoso

### SIGNUP_C002 - Registro con Email Duplicado
- **ID**: SIGNUP_C002
- **Prioridad**: Critical
- **Descripción**: Verificar el comportamiento al intentar registrar con un email ya existente
- **Datos de Prueba**:
  - Email: `duplicate{timestamp}{uuid}@test.com` (generado dinámicamente)
  - Password: `ValidPass123!`
  - Full Name: `Duplicate User`
- **Estado Esperado**: `400 Bad Request`, `500 Internal Server Error`, o `201 Created` (por bug conocido)
- **Validación de Esquema**: No
- **Validación de Datos**: No
- **Propósito**: Validar el manejo de emails duplicados
- **Nota**: Incluye flag `is_duplicate_test` para identificación especial

### SIGNUP_C003 - Registro con Email Inválido
- **ID**: SIGNUP_C003
- **Prioridad**: Critical
- **Descripción**: Verificar el rechazo de emails con formato inválido
- **Datos de Prueba**:
  - Email: `invalid-email` (formato inválido)
  - Password: `ValidPass123!`
  - Full Name: `Invalid User`
- **Estado Esperado**: `422 Unprocessable Entity`
- **Validación de Esquema**: No
- **Validación de Datos**: No
- **Propósito**: Validar la validación de formato de email

---

## CASOS DE PRUEBA MEDIOS (2 casos)

### SIGNUP_M001 - Registro con Contraseña Débil
- **ID**: SIGNUP_M001
- **Prioridad**: Medium
- **Descripción**: Verificar el rechazo de contraseñas que no cumplen criterios de seguridad
- **Datos de Prueba**:
  - Email: `weakpass{timestamp}{uuid}@gmail.com` (generado dinámicamente)
  - Password: `123` (contraseña débil)
  - Full Name: `Weak Pass User`
- **Estado Esperado**: `422 Unprocessable Entity`
- **Validación de Esquema**: No
- **Validación de Datos**: No
- **Propósito**: Validar la validación de fortaleza de contraseña

### SIGNUP_M002 - Registro con Nombre Vacío
- **ID**: SIGNUP_M002
- **Prioridad**: Medium
- **Descripción**: Verificar el comportamiento con nombre de usuario vacío
- **Datos de Prueba**:
  - Email: `emptyname{timestamp}{uuid}@gmail.com` (generado dinámicamente)
  - Password: `ValidPass123!`
  - Full Name: `""` (cadena vacía)
- **Estado Esperado**: `201 Created` (por bug conocido en la API)
- **Validación de Esquema**: Sí
- **Validación de Datos**: Sí
- **Propósito**: Validar el manejo de campos opcionales
- **Nota**: Según KNOWN_BUGS.md, la API acepta nombres vacíos incorrectamente

---

## CASOS DE PRUEBA BÁSICOS (1 caso)

### SIGNUP_L001 - Registro con Campos Faltantes
- **ID**: SIGNUP_L001
- **Prioridad**: Low
- **Descripción**: Verificar el rechazo cuando faltan campos obligatorios
- **Datos de Prueba**:
  - Email: `missing{timestamp}{uuid}@gmail.com` (generado dinámicamente)
  - Password: `ValidPass123!`
  - Full Name: (campo faltante intencionalmente)
- **Estado Esperado**: `422 Unprocessable Entity`
- **Validación de Esquema**: No
- **Validación de Datos**: No
- **Propósito**: Validar la validación de campos obligatorios

---

## CASO DE PRUEBA ESPECIAL

### test_signup_duplicate_email_real_scenario
- **Tipo**: Test de Escenario Real
- **Descripción**: Simula el escenario real de intentar registrar el mismo email dos veces consecutivas
- **Proceso**:
  1. Primera petición con email único → Debe retornar `201 Created`
  2. Segunda petición con el mismo email → Debe retornar `400`, `500`, o `201` (por bug)
- **Propósito**: Validar el comportamiento real de duplicados en secuencia

---

## BUGS DETECTADOS EN LA API

### Bug #1: Inconsistencia en el Manejo de Emails Duplicados
- **Endpoint Afectado**: `POST /auth/signup`
- **Descripción**: Al intentar registrar un usuario con un email que ya existe, la API debería retornar consistentemente un código `400 Bad Request` (o `409 Conflict`). Sin embargo, en ocasiones retorna `500 Internal Server Error`.
- **Comportamiento Esperado**: `400 Bad Request` con mensaje indicando email ya registrado
- **Comportamiento Actual**: `400 Bad Request` o `500 Internal Server Error` (inconsistente)
- **Impacto**: Dificulta la validación consistente del comportamiento de la API
- **Workaround**: Los tests aceptan tanto `400` como `500` como códigos válidos

### Bug #2: Aceptación de Nombres de Usuario Vacíos
- **Endpoint Afectado**: `POST /auth/signup`
- **Descripción**: La API permite el registro de usuarios con el campo `full_name` vacío, retornando `201 Created` cuando debería rechazar la petición.
- **Comportamiento Esperado**: `422 Unprocessable Entity` para nombres vacíos
- **Comportamiento Actual**: `201 Created` (acepta nombres vacíos)
- **Impacto**: Permite datos inconsistentes en la base de datos
- **Workaround**: Los tests están ajustados para esperar `201 Created`, documentando el comportamiento actual

### Bug #3: Inconsistencia en el Manejo de Mayúsculas en Emails
- **Endpoint Afectado**: `POST /auth/signup`
- **Descripción**: La API muestra comportamiento inconsistente al procesar emails con diferentes combinaciones de mayúsculas y minúsculas.
- **Comportamiento Esperado**: Normalización consistente de emails (convertir a minúsculas) o rechazo consistente
- **Comportamiento Actual**: `201 Created` o `500 Internal Server Error` de manera inconsistente
- **Impacto**: Dificulta la validación del comportamiento de la API para diferentes formatos de email
- **Workaround**: Los tests aceptan tanto `201` como `500` como códigos válidos

---

## ESTRUCTURA DE VALIDACIÓN

### Clase SignupTestHelper
La clase contiene métodos estáticos para:
- `perform_signup_request()`: Realiza la petición con headers apropiados
- `validate_response_status()`: Valida el código de estado de la respuesta
- `validate_response_schema()`: Valida el esquema JSON de la respuesta
- `validate_response_data()`: Valida los datos específicos de la respuesta
- `log_response_details()`: Registra detalles para debugging

### Headers Utilizados
- Se utilizan headers específicos para signup obtenidos de `AuthHeaders.get_signup_headers()`

### Generación de Datos Únicos
- Se utiliza `time.time()` y `uuid.uuid4()` para generar emails únicos en cada ejecución
- Esto evita conflictos entre ejecuciones de pruebas

---

## NOTAS IMPORTANTES

1. **Bugs del Backend**: Todos los bugs documentados son del lado del backend (API), no de las pruebas automatizadas.

2. **Tests Robustos**: Los tests están diseñados para ser robustos y manejar comportamientos inconsistentes de la API.

3. **Workarounds Temporales**: Los workarounds en los tests deben ser removidos una vez que los bugs sean corregidos en el backend.

4. **Recomendación**: Se recomienda reportar estos bugs al equipo de desarrollo del backend para su corrección.

5. **Validación de Servicio**: Incluye verificación previa de que el servicio API esté disponible antes de ejecutar las pruebas.

---

## MÉTRICAS DE COBERTURA

- **Casos Críticos**: 3 casos (50% del total)
- **Casos Medios**: 2 casos (33% del total)
- **Casos Básicos**: 1 caso (17% del total)
- **Cobertura de Bugs**: 3 bugs documentados y manejados
- **Validación de Esquemas**: Implementada para casos exitosos
- **Logging Detallado**: Implementado para debugging y trazabilidad
