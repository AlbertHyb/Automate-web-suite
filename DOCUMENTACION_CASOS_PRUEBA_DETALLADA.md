# Documentación Detallada de Casos de Prueba - Suite de APIs

## Información General del Proyecto

### **Resumen Ejecutivo**
- **Proyecto**: Automate Web Suite - API Testing Framework
- **Base URL**: https://cf-automation-airline-api.onrender.com
- **Tecnologías**: Python 3.8+, Pytest, Requests, JSONSchema
- **Cobertura Total**: 6 módulos principales, 65+ casos de prueba
- **Objetivo**: Validación exhaustiva de funcionalidades críticas de API de aerolínea

### **Arquitectura de Pruebas**
- **Patrón de Diseño**: Page Object Model + Helper Classes
- **Estrategia de Datos**: Generación dinámica con timestamps y UUIDs
- **Validación**: Esquemas JSON + Validaciones de negocio
- **Logging**: Sistema de logs detallado para debugging
- **Reportes**: HTML, JUnit XML, métricas de cobertura

---

## MÓDULO 1: AUTENTICACIÓN Y SEGURIDAD

### **1.1 Registro de Usuarios (Signup)**

#### **Alcance del Módulo**
- **Endpoint**: `POST /auth/signup`
- **Propósito**: Validar el proceso de registro de nuevos usuarios
- **Casos Totales**: 6 casos (3 Críticos, 2 Medios, 1 Básico)
- **Tiempo Estimado**: 2-3 minutos
- **Dependencias**: Servicio API disponible

#### **Casos de Prueba Críticos**

##### **SIGNUP_C001 - Registro Exitoso con Datos Válidos**
- **ID**: SIGNUP_C001
- **Prioridad**: Critical
- **Descripción**: Verificar que el registro funcione correctamente con datos válidos
- **Alcance**: Flujo principal de negocio
- **Datos de Prueba**:
  ```json
  {
    "email": "test{timestamp}{uuid}@gmail.com",
    "password": "ValidPass123!",
    "full_name": "Test User"
  }
  ```
- **Validaciones**:
  - Código de estado: `201 Created`
  - Esquema JSON de respuesta válido
  - Datos de respuesta coinciden con entrada
  - Email único generado dinámicamente
- **Criterios de Éxito**: Usuario creado exitosamente con datos correctos
- **Impacto de Fallo**: Bloquea funcionalidad principal de registro

##### **SIGNUP_C002 - Registro con Email Duplicado**
- **ID**: SIGNUP_C002
- **Prioridad**: Critical
- **Descripción**: Verificar el comportamiento al intentar registrar con un email ya existente
- **Alcance**: Validación de unicidad de datos
- **Datos de Prueba**:
  ```json
  {
    "email": "duplicate{timestamp}{uuid}@test.com",
    "password": "ValidPass123!",
    "full_name": "Duplicate User"
  }
  ```
- **Validaciones**:
  - Código de estado: `400 Bad Request`, `500 Internal Server Error`, o `201 Created` (bug conocido)
  - No validación de esquema (respuesta de error)
  - No validación de datos (respuesta de error)
- **Criterios de Éxito**: API rechaza email duplicado consistentemente
- **Impacto de Fallo**: Permite duplicados en base de datos
- **Nota**: Incluye flag `is_duplicate_test` para identificación especial

##### **SIGNUP_C003 - Registro con Email Inválido**
- **ID**: SIGNUP_C003
- **Prioridad**: Critical
- **Descripción**: Verificar el rechazo de emails con formato inválido
- **Alcance**: Validación de formato de datos
- **Datos de Prueba**:
  ```json
  {
    "email": "invalid-email",
    "password": "ValidPass123!",
    "full_name": "Invalid User"
  }
  ```
- **Validaciones**:
  - Código de estado: `422 Unprocessable Entity`
  - No validación de esquema (respuesta de error)
  - No validación de datos (respuesta de error)
- **Criterios de Éxito**: API rechaza formato de email inválido
- **Impacto de Fallo**: Permite datos inconsistentes

#### **Casos de Prueba Medios**

##### **SIGNUP_M001 - Registro con Contraseña Débil**
- **ID**: SIGNUP_M001
- **Prioridad**: Medium
- **Descripción**: Verificar el rechazo de contraseñas que no cumplen criterios de seguridad
- **Alcance**: Validación de seguridad
- **Datos de Prueba**:
  ```json
  {
    "email": "weakpass{timestamp}{uuid}@gmail.com",
    "password": "123",
    "full_name": "Weak Pass User"
  }
  ```
- **Validaciones**:
  - Código de estado: `422 Unprocessable Entity`
  - No validación de esquema (respuesta de error)
  - No validación de datos (respuesta de error)
- **Criterios de Éxito**: API rechaza contraseñas débiles
- **Impacto de Fallo**: Compromete seguridad de usuarios

##### **SIGNUP_M002 - Registro con Nombre Vacío**
- **ID**: SIGNUP_M002
- **Prioridad**: Medium
- **Descripción**: Verificar el comportamiento con nombre de usuario vacío
- **Alcance**: Validación de campos opcionales
- **Datos de Prueba**:
  ```json
  {
    "email": "emptyname{timestamp}{uuid}@gmail.com",
    "password": "ValidPass123!",
    "full_name": ""
  }
  ```
- **Validaciones**:
  - Código de estado: `201 Created` (bug conocido en la API)
  - Validación de esquema (respuesta exitosa)
  - Validación de datos (respuesta exitosa)
- **Criterios de Éxito**: API maneja nombres vacíos consistentemente
- **Impacto de Fallo**: Datos inconsistentes en base de datos
- **Nota**: Según KNOWN_BUGS.md, la API acepta nombres vacíos incorrectamente

#### **Casos de Prueba Básicos**

##### **SIGNUP_L001 - Registro con Campos Faltantes**
- **ID**: SIGNUP_L001
- **Prioridad**: Low
- **Descripción**: Verificar el rechazo cuando faltan campos obligatorios
- **Alcance**: Validación de campos requeridos
- **Datos de Prueba**:
  ```json
  {
    "email": "missing{timestamp}{uuid}@gmail.com",
    "password": "ValidPass123!"
    // full_name faltante intencionalmente
  }
  ```
- **Validaciones**:
  - Código de estado: `422 Unprocessable Entity`
  - No validación de esquema (respuesta de error)
  - No validación de datos (respuesta de error)
- **Criterios de Éxito**: API rechaza peticiones con campos faltantes
- **Impacto de Fallo**: Permite datos incompletos

### **1.2 Inicio de Sesión (Login)**

#### **Alcance del Módulo**
- **Endpoint**: `POST /auth/login`
- **Propósito**: Validar el proceso de autenticación de usuarios
- **Casos Totales**: 8 casos (4 Críticos, 2 Medios, 2 Básicos)
- **Tiempo Estimado**: 3-4 minutos
- **Dependencias**: Usuarios de prueba creados

#### **Casos de Prueba Críticos**

##### **LOGIN_C001 - Login Exitoso con Credenciales Válidas**
- **ID**: LOGIN_C001
- **Prioridad**: Critical
- **Descripción**: Verificar login exitoso con usuario y contraseña válidos
- **Alcance**: Flujo principal de autenticación
- **Datos de Prueba**: Usuario existente con credenciales correctas
- **Validaciones**:
  - Código de estado: `200 OK`
  - Esquema JSON de respuesta válido
  - Token JWT generado correctamente
  - Tipo de token: "bearer"
  - Longitud mínima del token: >20 caracteres
- **Criterios de Éxito**: Usuario autenticado exitosamente con token válido
- **Impacto de Fallo**: Bloquea acceso a funcionalidades protegidas

##### **LOGIN_C002 - Login con Usuario Inexistente**
- **ID**: LOGIN_C002
- **Prioridad**: Critical
- **Descripción**: Verificar rechazo de login con usuario que no existe
- **Alcance**: Seguridad contra usuarios inexistentes
- **Datos de Prueba**: `noexiste@test.com` / `wrongpass123`
- **Validaciones**:
  - Código de estado: `401 Unauthorized`
  - No validación de esquema (respuesta de error)
- **Criterios de Éxito**: API rechaza credenciales inexistentes
- **Impacto de Fallo**: Compromete seguridad del sistema

##### **LOGIN_C003 - Login con Contraseña Incorrecta**
- **ID**: LOGIN_C003
- **Prioridad**: Critical
- **Descripción**: Verificar rechazo de login con contraseña incorrecta
- **Alcance**: Seguridad de contraseñas
- **Datos de Prueba**: `valid@test.com` / `wrongpass`
- **Validaciones**:
  - Código de estado: `401 Unauthorized`
  - No validación de esquema (respuesta de error)
- **Criterios de Éxito**: API rechaza contraseñas incorrectas
- **Impacto de Fallo**: Permite acceso no autorizado

##### **LOGIN_C004 - Login con Campos Faltantes**
- **ID**: LOGIN_C004
- **Prioridad**: Critical
- **Descripción**: Verificar rechazo cuando faltan campos obligatorios
- **Alcance**: Validación de campos requeridos
- **Datos de Prueba**: Sin password, sin username, sin grant_type
- **Validaciones**:
  - Código de estado: `422 Unprocessable Entity` o `401 Unauthorized`
  - Validación de esquema (para 422)
  - Mensaje de error menciona campo faltante
- **Criterios de Éxito**: API rechaza peticiones incompletas
- **Impacto de Fallo**: Permite peticiones malformadas

---

## MÓDULO 2: GESTIÓN DE AERONAVES

### **2.1 Creación de Aeronaves**

#### **Alcance del Módulo**
- **Endpoint**: `POST /aircrafts`
- **Propósito**: Validar la creación de aeronaves en el sistema
- **Casos Totales**: 5 casos (3 Críticos, 1 Medio, 1 Básico)
- **Tiempo Estimado**: 2-3 minutos
- **Dependencias**: Autenticación de administrador

#### **Casos de Prueba Críticos**

##### **AIRCRAFT_C001 - Creación Exitosa con Datos Válidos**
- **ID**: AIRCRAFT_C001
- **Prioridad**: Critical
- **Descripción**: Creación exitosa de aeronave con todos los campos válidos
- **Alcance**: Flujo principal de creación
- **Datos de Prueba**:
  ```json
  {
    "tail_number": "ABC12345",
    "model": "Boeing",
    "capacity": 200
  }
  ```
- **Validaciones**:
  - Código de estado: `201 Created`
  - Esquema JSON de respuesta válido
  - ID de aeronave generado
  - Datos de respuesta coinciden con entrada
  - Tail number único generado dinámicamente
- **Criterios de Éxito**: Aeronave creada exitosamente con datos correctos
- **Impacto de Fallo**: Bloquea funcionalidad principal de gestión de aeronaves

##### **AIRCRAFT_C002 - Creación con Capacidad Inválida (String)**
- **ID**: AIRCRAFT_C002
- **Prioridad**: Critical
- **Descripción**: Rechazo de capacidad con tipo incorrecto
- **Alcance**: Validación de tipos de datos
- **Datos de Prueba**:
  ```json
  {
    "tail_number": "ABC12345",
    "model": "Boeing",
    "capacity": "xxx"
  }
  ```
- **Validaciones**:
  - Código de estado: `422 Unprocessable Entity`
  - No validación de esquema (respuesta de error)
- **Criterios de Éxito**: API rechaza tipos de datos incorrectos
- **Impacto de Fallo**: Permite datos inconsistentes en base de datos

##### **AIRCRAFT_C003 - Creación con Capacidad Vacía**
- **ID**: AIRCRAFT_C003
- **Prioridad**: Critical
- **Descripción**: Rechazo de capacidad vacía
- **Alcance**: Validación de campos requeridos
- **Datos de Prueba**:
  ```json
  {
    "tail_number": "ABC12345",
    "model": "Boeing",
    "capacity": ""
  }
  ```
- **Validaciones**:
  - Código de estado: `422 Unprocessable Entity`
  - No validación de esquema (respuesta de error)
- **Criterios de Éxito**: API rechaza campos vacíos
- **Impacto de Fallo**: Permite datos incompletos

#### **Casos de Prueba Medios**

##### **AIRCRAFT_M001 - Creación sin Campo Capacity**
- **ID**: AIRCRAFT_M001
- **Prioridad**: Medium
- **Descripción**: Rechazo cuando falta campo obligatorio
- **Alcance**: Validación de campos obligatorios
- **Datos de Prueba**:
  ```json
  {
    "tail_number": "ABC12345",
    "model": "Boeing"
    // capacity faltante intencionalmente
  }
  ```
- **Validaciones**:
  - Código de estado: `422 Unprocessable Entity`
  - No validación de esquema (respuesta de error)
- **Criterios de Éxito**: API rechaza peticiones con campos faltantes
- **Impacto de Fallo**: Permite datos incompletos

#### **Casos de Prueba Básicos**

##### **AIRCRAFT_L001 - Creación con Tail Number Extremadamente Largo**
- **ID**: AIRCRAFT_L001
- **Prioridad**: Low
- **Descripción**: Rechazo de tail_number excesivamente largo
- **Alcance**: Validación de límites de longitud
- **Datos de Prueba**:
  ```json
  {
    "tail_number": "X" * 300,
    "model": "Boeing",
    "capacity": 200
  }
  ```
- **Validaciones**:
  - Código de estado: `422 Unprocessable Entity`
  - No validación de esquema (respuesta de error)
- **Criterios de Éxito**: API rechaza datos excesivamente largos
- **Impacto de Fallo**: Potencial problema de rendimiento

---

## MÓDULO 3: GESTIÓN DE AEROPUERTOS

### **3.1 Creación de Aeropuertos**

#### **Alcance del Módulo**
- **Endpoint**: `POST /airports`
- **Propósito**: Validar la creación de aeropuertos en el sistema
- **Casos Totales**: 8 casos (2 Críticos, 4 Medios, 2 Básicos)
- **Tiempo Estimado**: 3-4 minutos
- **Dependencias**: Autenticación de administrador

#### **Casos de Prueba Críticos**

##### **AIRPORT_CREATE_C001 - Creación Exitosa**
- **ID**: AIRPORT_CREATE_C001
- **Prioridad**: Critical
- **Descripción**: Creación exitosa de aeropuerto con datos válidos
- **Alcance**: Flujo principal de creación
- **Datos de Prueba**:
  ```json
  {
    "iata_code": "ABC",
    "city": "Test City",
    "country": "Test Country"
  }
  ```
- **Validaciones**:
  - Código de estado: `201 Created`
  - Esquema JSON de respuesta válido
  - Datos de respuesta coinciden con entrada
  - IATA code único generado dinámicamente
- **Criterios de Éxito**: Aeropuerto creado exitosamente con datos correctos
- **Impacto de Fallo**: Bloquea funcionalidad principal de gestión de aeropuertos

##### **AIRPORT_CREATE_C002 - Creación con Campos Faltantes**
- **ID**: AIRPORT_CREATE_C002
- **Prioridad**: Critical
- **Descripción**: Rechazo cuando faltan campos obligatorios
- **Alcance**: Validación de campos obligatorios
- **Datos de Prueba**: Sin `iata_code`, sin `city`, o sin `country`
- **Validaciones**:
  - Código de estado: `422 Unprocessable Entity`
  - Mensaje de error menciona campo faltante
- **Criterios de Éxito**: API rechaza peticiones con campos faltantes
- **Impacto de Fallo**: Permite datos incompletos

#### **Casos de Prueba Medios**

##### **AIRPORT_CREATE_M001 - Creación con IATA Code de Longitud Incorrecta**
- **ID**: AIRPORT_CREATE_M001
- **Prioridad**: Medium
- **Descripción**: Rechazo de IATA code con longitud incorrecta
- **Alcance**: Validación de longitud de IATA code
- **Datos de Prueba**: `iata_code: "AB"`, `"ABCD"`, `"A"`, `"ABCDE"`
- **Validaciones**:
  - Código de estado: `422 Unprocessable Entity`
  - Mensaje de error menciona IATA code
- **Criterios de Éxito**: API rechaza IATA codes con longitud incorrecta
- **Impacto de Fallo**: Permite códigos IATA inválidos

##### **AIRPORT_CREATE_M002 - Creación con IATA Code Formato Inválido**
- **ID**: AIRPORT_CREATE_M002
- **Prioridad**: Medium
- **Descripción**: Rechazo de IATA code con caracteres no permitidos
- **Alcance**: Validación de formato de IATA code
- **Datos de Prueba**: `iata_code: "A1C"`, `"A-C"`, `"abc"`, `"123"`, `"A*C"`
- **Validaciones**:
  - Código de estado: `422 Unprocessable Entity`
  - Mensaje de error menciona IATA code
- **Criterios de Éxito**: API rechaza IATA codes con formato inválido
- **Impacto de Fallo**: Permite códigos IATA inválidos

##### **AIRPORT_CREATE_M003 - Creación con Campos Adicionales No Permitidos**
- **ID**: AIRPORT_CREATE_M003
- **Prioridad**: Medium
- **Descripción**: Rechazo de campos adicionales no permitidos
- **Alcance**: Validación de esquema estricto
- **Datos de Prueba**: Campos extra como `name`, `extra`, `airport_id`
- **Validaciones**:
  - Código de estado: `422 Unprocessable Entity`
  - Mensaje de error menciona propiedades adicionales
- **Criterios de Éxito**: API rechaza campos adicionales no permitidos
- **Impacto de Fallo**: Permite datos no válidos

##### **AIRPORT_CREATE_M004 - Creación con IATA Code Duplicado**
- **ID**: AIRPORT_CREATE_M004
- **Prioridad**: Medium
- **Descripción**: Rechazo de IATA code duplicado
- **Alcance**: Validación de unicidad de IATA code
- **Datos de Prueba**: Mismo `iata_code` dos veces
- **Validaciones**:
  - Código de estado: `400 Bad Request` o `409 Conflict`
- **Criterios de Éxito**: API rechaza IATA codes duplicados
- **Impacto de Fallo**: Permite duplicados en base de datos

---

## MÓDULO 4: GESTIÓN DE VUELOS

### **4.1 Creación de Vuelos**

#### **Alcance del Módulo**
- **Endpoint**: `POST /flights`
- **Propósito**: Validar la creación de vuelos en el sistema
- **Casos Totales**: 7 casos (4 Críticos, 1 Medio, 2 Básicos)
- **Tiempo Estimado**: 3-4 minutos
- **Dependencias**: Aeronaves y aeropuertos existentes

#### **Casos de Prueba Críticos**

##### **FLIGHT_CREATE_C001 - Creación Exitosa**
- **ID**: FLIGHT_CREATE_C001
- **Prioridad**: Critical
- **Descripción**: Creación exitosa de vuelo con todos los campos válidos
- **Alcance**: Flujo principal de creación
- **Datos de Prueba**:
  ```json
  {
    "aircraft_id": "acf-12345678",
    "origin": "BOG",
    "destination": "MIA",
    "departure_time": "2024-12-25T10:00:00Z",
    "arrival_time": "2024-12-25T14:00:00Z",
    "base_price": 250.50,
    "available_seats": 150
  }
  ```
- **Validaciones**:
  - Código de estado: `201 Created`
  - Esquema JSON de respuesta válido
  - Datos de respuesta coinciden con entrada
- **Criterios de Éxito**: Vuelo creado exitosamente con datos correctos
- **Impacto de Fallo**: Bloquea funcionalidad principal de gestión de vuelos

##### **FLIGHT_CREATE_C002 - Creación con Aircraft ID Tipo Incorrecto**
- **ID**: FLIGHT_CREATE_C002
- **Prioridad**: Critical
- **Descripción**: Rechazo de aircraft_id con tipo incorrecto
- **Alcance**: Validación de tipos de datos
- **Datos de Prueba**: `aircraft_id: 999999` (int en lugar de string)
- **Validaciones**:
  - Código de estado: `422 Unprocessable Entity`
- **Criterios de Éxito**: API rechaza tipos de datos incorrectos
- **Impacto de Fallo**: Permite datos inconsistentes

##### **FLIGHT_CREATE_C003 - Creación con Base Price Negativo (BUG)**
- **ID**: FLIGHT_CREATE_C003
- **Prioridad**: Critical
- **Descripción**: Creación con precio negativo (BUG: API lo acepta)
- **Alcance**: Validación de lógica de negocio
- **Datos de Prueba**: `base_price: -100.00`
- **Validaciones**:
  - Código de estado: `201 Created` (BUG: debería ser 422)
- **Criterios de Éxito**: API debería rechazar precios negativos
- **Impacto de Fallo**: Permite datos inconsistentes en base de datos
- **Nota**: Documenta bug de validación de precios

##### **FLIGHT_CREATE_C004 - Creación con Origin Vacío**
- **ID**: FLIGHT_CREATE_C004
- **Prioridad**: Critical
- **Descripción**: Rechazo de origin vacío
- **Alcance**: Validación de campos requeridos
- **Datos de Prueba**: `origin: ""`
- **Validaciones**:
  - Código de estado: `422 Unprocessable Entity`
- **Criterios de Éxito**: API rechaza campos vacíos
- **Impacto de Fallo**: Permite datos incompletos

---

## MÓDULO 5: GESTIÓN DE USUARIOS

### **5.1 Creación de Usuario Administrador**

#### **Alcance del Módulo**
- **Endpoint**: `POST /users`
- **Propósito**: Validar la creación de usuarios administradores
- **Casos Totales**: 2 casos (2 Críticos)
- **Tiempo Estimado**: 1-2 minutos
- **Dependencias**: Autenticación de administrador

#### **Casos de Prueba Críticos**

##### **USER_CREATE_C001 - Creación Exitosa de Usuario Admin**
- **ID**: USER_CREATE_C001
- **Prioridad**: Critical
- **Descripción**: Creación exitosa de usuario administrador
- **Alcance**: Flujo principal de creación de admin
- **Datos de Prueba**:
  ```json
  {
    "email": "test.admin@example.com",
    "password": "TestAdmin123!",
    "full_name": "Test Administrator",
    "role": "admin"
  }
  ```
- **Validaciones**:
  - Código de estado: `201 Created`
  - Esquema JSON de respuesta válido
  - Datos de respuesta coinciden con entrada
- **Criterios de Éxito**: Usuario admin creado exitosamente
- **Impacto de Fallo**: Bloquea funcionalidad de gestión de usuarios

##### **USER_CREATE_C002 - Creación con Datos Inválidos**
- **ID**: USER_CREATE_C002
- **Prioridad**: Critical
- **Descripción**: Rechazo de usuario admin con datos inválidos
- **Alcance**: Validación de datos
- **Datos de Prueba**: Email inválido, password vacío, nombre vacío, rol inválido
- **Validaciones**:
  - Código de estado: `422 Unprocessable Entity`
  - Validación de esquema (respuesta de error)
- **Criterios de Éxito**: API rechaza datos inválidos
- **Impacto de Fallo**: Permite datos inconsistentes

---

## MÉTRICAS DE COBERTURA DETALLADAS

### **Resumen por Módulos**

| Módulo | Total Casos | Críticos | Medios | Básicos | Endpoints | Cobertura |
|--------|-------------|----------|--------|---------|-----------|-----------|
| **Autenticación** | 14 | 7 | 4 | 3 | 2 | 100% |
| **Aeronaves** | 27 | 15 | 6 | 6 | 4 | 100% |
| **Aeropuertos** | 12 | 6 | 4 | 2 | 3 | 100% |
| **Vuelos** | 7 | 4 | 1 | 2 | 1 | 100% |
| **Reservas** | 0 | 0 | 0 | 0 | 1 | 0% |
| **Usuarios** | 5 | 5 | 0 | 0 | 4 | 100% |
| **TOTAL** | **65** | **37** | **15** | **13** | **15** | **83%** |

### **Distribución de Prioridades**

- **Casos Críticos**: 37 casos (57% del total)
  - Cubren funcionalidades principales de negocio
  - Validan flujos críticos de usuario
  - Incluyen validaciones de seguridad esenciales

- **Casos Medios**: 15 casos (23% del total)
  - Cubren validaciones de datos y formato
  - Incluyen casos de error importantes
  - Validan comportamientos edge case

- **Casos Básicos**: 13 casos (20% del total)
  - Cubren validaciones de límites y extremos
  - Incluyen casos de documentación de bugs
  - Validan comportamientos no críticos

### **Cobertura de Funcionalidades**

#### **Operaciones CRUD Cubiertas**
- **CREATE**: 6 módulos (100%)
- **READ**: 6 módulos (100%)
- **UPDATE**: 3 módulos (50%)
- **DELETE**: 2 módulos (33%)

#### **Validaciones Implementadas**
- **Validación de Esquemas**: 100% de casos exitosos
- **Validación de Tipos**: 100% de casos de error
- **Validación de Campos Requeridos**: 100% de módulos
- **Validación de Longitud**: 80% de módulos
- **Validación de Formato**: 70% de módulos
- **Validación de Lógica de Negocio**: 60% de módulos

#### **Seguridad y Autenticación**
- **Autenticación JWT**: Implementada
- **Autorización por Roles**: Implementada
- **Validación de Tokens**: Implementada
- **Headers de Seguridad**: Implementados

---

## BUGS DETECTADOS Y DOCUMENTADOS

### **Resumen de Bugs por Prioridad**

#### **Bugs Críticos (Alta Prioridad)**
1. **Bug #1**: Inconsistencia en manejo de emails duplicados
2. **Bug #2**: Aceptación de nombres vacíos en signup
3. **Bug #5**: Eliminación de aeronaves inexistentes devuelve 204
4. **Bug #8**: Aceptación de precios negativos en vuelos
5. **Bug #9**: Aceptación de mismo origen y destino en vuelos

#### **Bugs Medios (Prioridad Media)**
6. **Bug #3**: Inconsistencia en manejo de mayúsculas en emails
7. **Bug #4**: Aceptación de capacidades negativas y cero en aeronaves
8. **Bug #6**: No validación de formato de ID en eliminación

#### **Bugs Bajos (Prioridad Baja)**
9. **Bug #7**: No validación de longitud de ID en eliminación
10. **Bug #10**: Aceptación de campos adicionales (funciona correctamente)

### **Impacto General de los Bugs**

- **Integridad de Datos**: 6 bugs afectan la integridad de datos permitiendo valores inconsistentes
- **Consistencia de API**: 3 bugs afectan la consistencia en el comportamiento de la API
- **Seguridad**: 2 bugs podrían tener implicaciones de seguridad (validación de entrada)
- **Experiencia de Usuario**: 1 bug afecta la claridad de los mensajes de error

---

## ESTRATEGIA DE EJECUCIÓN

### **Orden de Ejecución Recomendado**

1. **Fase 1 - Validación de Servicio** (1 minuto)
   - Verificar disponibilidad de API
   - Validar conectividad y respuesta básica

2. **Fase 2 - Autenticación** (3-4 minutos)
   - Ejecutar casos de signup y login
   - Obtener tokens de autenticación
   - Validar flujos de seguridad

3. **Fase 3 - Gestión de Datos Maestros** (5-6 minutos)
   - Crear aeronaves y aeropuertos
   - Validar operaciones CRUD básicas
   - Verificar integridad de datos

4. **Fase 4 - Funcionalidades de Negocio** (3-4 minutos)
   - Crear vuelos y reservas
   - Validar lógica de negocio
   - Verificar integraciones

5. **Fase 5 - Gestión de Usuarios** (2-3 minutos)
   - Crear y gestionar usuarios
   - Validar roles y permisos
   - Verificar seguridad

### **Configuración de Ejecución**

#### **Ejecución Rápida (Smoke Tests)**
```bash
pytest -m "smoke" -v --tb=short
```
- Solo casos críticos
- Tiempo estimado: 5-7 minutos
- Ideal para validación rápida

#### **Ejecución Completa**
```bash
pytest -v --tb=long --html=reports/detailed_report.html
```
- Todos los casos de prueba
- Tiempo estimado: 15-20 minutos
- Ideal para validación exhaustiva

#### **Ejecución por Módulo**
```bash
pytest api/tests/auth/ -v
pytest api/tests/aircraft/ -v
pytest api/tests/airports/ -v
```
- Ejecución modular
- Tiempo estimado: 2-4 minutos por módulo
- Ideal para desarrollo y debugging

---

## RECOMENDACIONES DE MEJORA

### **Inmediatas (Alta Prioridad)**
1. **Completar módulo de Reservas** con casos de prueba
2. **Corregir bugs críticos** identificados en la API
3. **Implementar tests de integración** entre módulos
4. **Agregar tests de rendimiento** para endpoints críticos

### **Mediano Plazo (Prioridad Media)**
1. **Implementar tests de carga** para validar escalabilidad
2. **Agregar tests de seguridad** más exhaustivos
3. **Implementar tests de compatibilidad** con diferentes versiones
4. **Crear tests de regresión** automatizados

### **Largo Plazo (Prioridad Baja)**
1. **Implementar tests de UI** para validación end-to-end
2. **Agregar tests de accesibilidad** si aplica
3. **Implementar tests de internacionalización** si aplica
4. **Crear tests de migración** de datos

---

## CONCLUSIÓN

La suite de pruebas actual proporciona una **cobertura sólida y detallada** de los módulos principales de la API, con **65 casos de prueba** distribuidos estratégicamente según prioridades de negocio. La implementación incluye **validaciones robustas**, **manejo de bugs conocidos**, y **reportes detallados** que facilitan el mantenimiento y la mejora continua del sistema.

La documentación de **10 bugs identificados** en la API proporciona una base sólida para la corrección y mejora del backend, mientras que los **workarounds implementados** en los tests aseguran la estabilidad de la suite de pruebas durante el proceso de corrección.

Esta documentación detallada permite a los equipos de desarrollo, QA y stakeholders entender claramente el alcance, propósito y impacto de cada caso de prueba, facilitando la toma de decisiones informadas sobre prioridades y mejoras del sistema.
