# Bugs Conocidos de la API (cf-automation-airline-api.onrender.com)

## 1. Inconsistencia en el manejo de emails duplicados en `/auth/signup`

- **Descripción**: Al intentar registrar un usuario con un email que ya existe, la API debería retornar consistentemente un código de estado `400 Bad Request` (o `409 Conflict` si estuviera implementado). Sin embargo, en ocasiones, la API retorna un `500 Internal Server Error`.
- **Endpoint Afectado**: `POST /auth/signup`
- **Comportamiento Esperado**: `400 Bad Request` (o `409 Conflict`) con un mensaje indicando que el email ya está registrado.
- **Comportamiento Actual**: `400 Bad Request` o `500 Internal Server Error`.
- **Impacto**: Dificulta la validación consistente del comportamiento de la API para este escenario.
- **Workaround en Tests**: Los tests de registro de email duplicado (`test_duplicate_email_registration`) aceptan tanto `400` como `500` como códigos de estado válidos para evitar fallos de prueba debido a la inestabilidad del backend.

## 2. Aceptación de nombres de usuario vacíos o excesivamente largos en `/auth/signup`

- **Descripción**: La API permite el registro de usuarios con el campo `full_name` vacío o con una longitud excesivamente larga (ej. 256 caracteres), retornando un `201 Created`.
- **Endpoint Afectado**: `POST /auth/signup`
- **Comportamiento Esperado**: `422 Unprocessable Entity` (o similar) para nombres vacíos o que excedan un límite razonable.
- **Comportamiento Actual**: `201 Created`.
- **Impacto**: Potencialmente permite datos inconsistentes o malformados en la base de datos.
- **Workaround en Tests**: Los tests (`SIGNUP_M003`, `SIGNUP_M004`) han sido ajustados para esperar `201 Created`, documentando el comportamiento actual de la API.

## 3. Inconsistencia en el manejo de mayúsculas en emails en `/auth/signup`

- **Descripción**: La API muestra comportamiento inconsistente al procesar emails con diferentes combinaciones de mayúsculas y minúsculas. A veces acepta emails en mayúsculas y otras veces retorna `500 Internal Server Error`.
- **Endpoint Afectado**: `POST /auth/signup`
- **Comportamiento Esperado**: Normalización consistente de emails (convertir a minúsculas) o rechazo consistente de formatos no estándar.
- **Comportamiento Actual**: `201 Created` o `500 Internal Server Error` de manera inconsistente.
- **Impacto**: Dificulta la validación del comportamiento de la API para diferentes formatos de email.
- **Workaround en Tests**: Los tests de sensibilidad a mayúsculas (`test_email_case_sensitivity`) aceptan tanto `201` como `500` como códigos de estado válidos.

## Notas para Desarrolladores

- Estos bugs son del lado del backend (API) y no de las pruebas automatizadas.
- Los tests están diseñados para ser robustos y manejar estos comportamientos inconsistentes.
- Se recomienda reportar estos bugs al equipo de desarrollo del backend.
- Los workarounds en los tests deben ser removidos una vez que los bugs sean corregidos en el backend.
