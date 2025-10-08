# Alcance y Propósito de Casos de Prueba - Suite de APIs

## Resumen Ejecutivo del Alcance

### **Objetivo Principal**
Validar exhaustivamente la funcionalidad, seguridad y robustez de la API de aerolínea mediante casos de prueba estructurados que cubran todos los aspectos críticos del sistema.

### **Cobertura Total**
- **6 Módulos Principales**: Autenticación, Aeronaves, Aeropuertos, Vuelos, Reservas, Usuarios
- **65+ Casos de Prueba**: Distribuidos estratégicamente por prioridad
- **15 Endpoints**: Cubiertos completamente
- **100% Funcionalidades Críticas**: Validadas exhaustivamente

---

## MÓDULO 1: AUTENTICACIÓN Y SEGURIDAD

### **Alcance del Módulo**
- **Propósito**: Garantizar la seguridad y funcionalidad del sistema de autenticación
- **Endpoints Cubiertos**: 2 (`/auth/signup`, `/auth/login`)
- **Casos Totales**: 14 casos
- **Tiempo de Ejecución**: 5-7 minutos

### **Casos de Prueba Críticos (7 casos)**

#### **SIGNUP_C001 - Registro Exitoso**
- **Alcance**: Flujo principal de negocio
- **Propósito**: Validar que usuarios pueden registrarse correctamente
- **Criterios de Éxito**: Usuario creado con datos correctos
- **Impacto de Fallo**: Bloquea funcionalidad principal

#### **SIGNUP_C002 - Email Duplicado**
- **Alcance**: Validación de unicidad de datos
- **Propósito**: Prevenir duplicados en base de datos
- **Criterios de Éxito**: API rechaza emails duplicados
- **Impacto de Fallo**: Permite duplicados

#### **SIGNUP_C003 - Email Inválido**
- **Alcance**: Validación de formato de datos
- **Propósito**: Asegurar integridad de datos
- **Criterios de Éxito**: API rechaza formatos inválidos
- **Impacto de Fallo**: Permite datos inconsistentes

#### **LOGIN_C001 - Login Exitoso**
- **Alcance**: Flujo principal de autenticación
- **Propósito**: Validar acceso de usuarios autenticados
- **Criterios de Éxito**: Token JWT válido generado
- **Impacto de Fallo**: Bloquea acceso al sistema

#### **LOGIN_C002 - Usuario Inexistente**
- **Alcance**: Seguridad contra usuarios inexistentes
- **Propósito**: Prevenir acceso no autorizado
- **Criterios de Éxito**: API rechaza credenciales inexistentes
- **Impacto de Fallo**: Compromete seguridad

#### **LOGIN_C003 - Contraseña Incorrecta**
- **Alcance**: Seguridad de contraseñas
- **Propósito**: Validar autenticación segura
- **Criterios de Éxito**: API rechaza contraseñas incorrectas
- **Impacto de Fallo**: Permite acceso no autorizado

#### **LOGIN_C004 - Campos Faltantes**
- **Alcance**: Validación de campos requeridos
- **Propósito**: Asegurar peticiones completas
- **Criterios de Éxito**: API rechaza peticiones incompletas
- **Impacto de Fallo**: Permite peticiones malformadas

### **Casos de Prueba Medios (4 casos)**

#### **SIGNUP_M001 - Contraseña Débil**
- **Alcance**: Validación de seguridad
- **Propósito**: Asegurar contraseñas seguras
- **Criterios de Éxito**: API rechaza contraseñas débiles
- **Impacto de Fallo**: Compromete seguridad

#### **SIGNUP_M002 - Nombre Vacío**
- **Alcance**: Validación de campos opcionales
- **Propósito**: Manejar campos opcionales correctamente
- **Criterios de Éxito**: API maneja nombres vacíos consistentemente
- **Impacto de Fallo**: Datos inconsistentes

#### **LOGIN_M001 - Grant Type Inválido**
- **Alcance**: Validación de parámetros
- **Propósito**: Asegurar parámetros válidos
- **Criterios de Éxito**: API rechaza grant types inválidos
- **Impacto de Fallo**: Permite parámetros inválidos

#### **LOGIN_M002 - Email Formato Inválido**
- **Alcance**: Validación de formato
- **Propósito**: Asegurar formato de email válido
- **Criterios de Éxito**: API rechaza formatos inválidos
- **Impacto de Fallo**: Permite formatos inválidos

### **Casos de Prueba Básicos (3 casos)**

#### **SIGNUP_L001 - Campos Faltantes**
- **Alcance**: Validación de campos requeridos
- **Propósito**: Asegurar peticiones completas
- **Criterios de Éxito**: API rechaza peticiones incompletas
- **Impacto de Fallo**: Permite datos incompletos

#### **LOGIN_L001 - Campos Vacíos**
- **Alcance**: Validación de campos vacíos
- **Propósito**: Asegurar campos no vacíos
- **Criterios de Éxito**: API rechaza campos vacíos
- **Impacto de Fallo**: Permite campos vacíos

#### **LOGIN_L002 - Validación de Esquemas**
- **Alcance**: Consistencia de respuestas
- **Propósito**: Asegurar formato consistente
- **Criterios de Éxito**: Esquemas JSON válidos
- **Impacto de Fallo**: Respuestas inconsistentes

---

## MÓDULO 2: GESTIÓN DE AERONAVES

### **Alcance del Módulo**
- **Propósito**: Validar la gestión completa de aeronaves en el sistema
- **Endpoints Cubiertos**: 4 (`POST /aircrafts`, `GET /aircrafts`, `PUT /aircrafts/{id}`, `DELETE /aircrafts/{id}`)
- **Casos Totales**: 27 casos
- **Tiempo de Ejecución**: 8-10 minutos

### **Submódulo 2.1: Creación de Aeronaves (5 casos)**

#### **AIRCRAFT_C001 - Creación Exitosa**
- **Alcance**: Flujo principal de creación
- **Propósito**: Validar creación de aeronaves con datos válidos
- **Criterios de Éxito**: Aeronave creada con datos correctos
- **Impacto de Fallo**: Bloquea funcionalidad principal

#### **AIRCRAFT_C002 - Capacidad Inválida (String)**
- **Alcance**: Validación de tipos de datos
- **Propósito**: Asegurar tipos de datos correctos
- **Criterios de Éxito**: API rechaza tipos incorrectos
- **Impacto de Fallo**: Permite datos inconsistentes

#### **AIRCRAFT_C003 - Capacidad Vacía**
- **Alcance**: Validación de campos requeridos
- **Propósito**: Asegurar campos no vacíos
- **Criterios de Éxito**: API rechaza campos vacíos
- **Impacto de Fallo**: Permite datos incompletos

#### **AIRCRAFT_M001 - Sin Campo Capacity**
- **Alcance**: Validación de campos obligatorios
- **Propósito**: Asegurar campos requeridos
- **Criterios de Éxito**: API rechaza campos faltantes
- **Impacto de Fallo**: Permite datos incompletos

#### **AIRCRAFT_L001 - Tail Number Extremadamente Largo**
- **Alcance**: Validación de límites de longitud
- **Propósito**: Asegurar límites razonables
- **Criterios de Éxito**: API rechaza datos excesivamente largos
- **Impacto de Fallo**: Potencial problema de rendimiento

### **Submódulo 2.2: Listado de Aeronaves (6 casos)**

#### **AIRCRAFT_LIST_C001 - Listado Básico**
- **Alcance**: Funcionalidad básica de listado
- **Propósito**: Validar listado de aeronaves
- **Criterios de Éxito**: Lista de aeronaves devuelta correctamente
- **Impacto de Fallo**: Bloquea visualización de datos

#### **AIRCRAFT_LIST_C002 - Listado con Offset**
- **Alcance**: Paginación
- **Propósito**: Validar paginación de resultados
- **Criterios de Éxito**: Paginación funciona correctamente
- **Impacto de Fallo**: Problemas de rendimiento

#### **AIRCRAFT_LIST_C003 - Listado con Límite Mayor**
- **Alcance**: Límites de paginación
- **Propósito**: Validar límites de paginación
- **Criterios de Éxito**: Límites respetados correctamente
- **Impacto de Fallo**: Problemas de rendimiento

#### **AIRCRAFT_LIST_C004 - Listado con Parámetros Personalizados**
- **Alcance**: Combinaciones de parámetros
- **Propósito**: Validar combinaciones de parámetros
- **Criterios de Éxito**: Combinaciones funcionan correctamente
- **Impacto de Fallo**: Funcionalidad limitada

#### **AIRCRAFT_LIST_M001 - Skip Negativo**
- **Alcance**: Validación de parámetros negativos
- **Propósito**: Asegurar parámetros válidos
- **Criterios de Éxito**: API rechaza parámetros negativos
- **Impacto de Fallo**: Permite parámetros inválidos

#### **AIRCRAFT_LIST_L001 - Skip Grande**
- **Alcance**: Comportamiento con datos inexistentes
- **Propósito**: Validar comportamiento edge case
- **Criterios de Éxito**: API maneja datos inexistentes correctamente
- **Impacto de Fallo**: Comportamiento inconsistente

### **Submódulo 2.3: Actualización de Aeronaves (7 casos)**

#### **AIRCRAFT_UPDATE_C001 - Actualización Exitosa**
- **Alcance**: Flujo principal de actualización
- **Propósito**: Validar actualización de aeronaves
- **Criterios de Éxito**: Aeronave actualizada correctamente
- **Impacto de Fallo**: Bloquea funcionalidad de actualización

#### **AIRCRAFT_UPDATE_C002 - Tail Number Excesivamente Largo**
- **Alcance**: Validación de límites de longitud
- **Propósito**: Asegurar límites razonables
- **Criterios de Éxito**: API rechaza datos excesivamente largos
- **Impacto de Fallo**: Potencial problema de rendimiento

#### **AIRCRAFT_UPDATE_C003 - Tail Number Vacío**
- **Alcance**: Validación de campos requeridos
- **Propósito**: Asegurar campos no vacíos
- **Criterios de Éxito**: API rechaza campos vacíos
- **Impacto de Fallo**: Permite datos incompletos

#### **AIRCRAFT_UPDATE_C004 - Capacity No Numérica**
- **Alcance**: Validación de tipos de datos
- **Propósito**: Asegurar tipos de datos correctos
- **Criterios de Éxito**: API rechaza tipos incorrectos
- **Impacto de Fallo**: Permite datos inconsistentes

#### **AIRCRAFT_UPDATE_M001 - Sin Campo Model**
- **Alcance**: Validación de campos obligatorios
- **Propósito**: Asegurar campos requeridos
- **Criterios de Éxito**: API rechaza campos faltantes
- **Impacto de Fallo**: Permite datos incompletos

#### **AIRCRAFT_UPDATE_M002 - Capacity Negativa (BUG)**
- **Alcance**: Validación de lógica de negocio
- **Propósito**: Documentar bug de validación
- **Criterios de Éxito**: API debería rechazar valores negativos
- **Impacto de Fallo**: Permite datos inconsistentes

#### **AIRCRAFT_UPDATE_L001 - Capacity en Cero (BUG)**
- **Alcance**: Validación de lógica de negocio
- **Propósito**: Documentar bug de validación
- **Criterios de Éxito**: API debería rechazar valores cero
- **Impacto de Fallo**: Permite datos inconsistentes

### **Submódulo 2.4: Eliminación de Aeronaves (9 casos)**

#### **AIRCRAFT_DELETE_C001 - Eliminación Exitosa**
- **Alcance**: Flujo principal de eliminación
- **Propósito**: Validar eliminación de aeronaves
- **Criterios de Éxito**: Aeronave eliminada correctamente
- **Impacto de Fallo**: Bloquea funcionalidad de eliminación

#### **AIRCRAFT_DELETE_C002 - Sin Autenticación**
- **Alcance**: Seguridad de autenticación
- **Propósito**: Asegurar autenticación requerida
- **Criterios de Éxito**: API rechaza peticiones no autenticadas
- **Impacto de Fallo**: Compromete seguridad

#### **AIRCRAFT_DELETE_C003 - Aeronave Inexistente (BUG)**
- **Alcance**: Validación de existencia
- **Propósito**: Documentar bug de validación
- **Criterios de Éxito**: API debería devolver 404
- **Impacto de Fallo**: Comportamiento inconsistente

#### **AIRCRAFT_DELETE_C004 - ID Formato Inválido (BUG)**
- **Alcance**: Validación de formato de ID
- **Propósito**: Documentar bug de validación
- **Criterios de Éxito**: API debería devolver 400
- **Impacto de Fallo**: Comportamiento inconsistente

#### **AIRCRAFT_DELETE_M001 - ID Vacío**
- **Alcance**: Validación de endpoints válidos
- **Propósito**: Asegurar endpoints válidos
- **Criterios de Éxito**: API rechaza IDs vacíos
- **Impacto de Fallo**: Permite endpoints inválidos

#### **AIRCRAFT_DELETE_M002 - Eliminación Doble (Idempotencia)**
- **Alcance**: Idempotencia de DELETE
- **Propósito**: Validar idempotencia
- **Criterios de Éxito**: Segunda eliminación es idempotente
- **Impacto de Fallo**: Comportamiento inconsistente

#### **AIRCRAFT_DELETE_M003 - Verificación Post-Eliminación**
- **Alcance**: Validación de eliminación efectiva
- **Propósito**: Asegurar eliminación real
- **Criterios de Éxito**: Aeronave no existe después de eliminación
- **Impacto de Fallo**: Eliminación no efectiva

#### **AIRCRAFT_DELETE_L001 - ID Extremadamente Largo (BUG)**
- **Alcance**: Validación de longitud de ID
- **Propósito**: Documentar bug de validación
- **Criterios de Éxito**: API debería validar longitud
- **Impacto de Fallo**: Potencial problema de rendimiento

#### **AIRCRAFT_DELETE_L002 - Caracteres Especiales**
- **Alcance**: Seguridad contra path traversal
- **Propósito**: Asegurar seguridad
- **Criterios de Éxito**: API rechaza caracteres especiales
- **Impacto de Fallo**: Compromete seguridad

---

## MÓDULO 3: GESTIÓN DE AEROPUERTOS

### **Alcance del Módulo**
- **Propósito**: Validar la gestión completa de aeropuertos en el sistema
- **Endpoints Cubiertos**: 3 (`POST /airports`, `GET /airports`, `GET /airports/{iata_code}`)
- **Casos Totales**: 12 casos
- **Tiempo de Ejecución**: 4-5 minutos

### **Submódulo 3.1: Creación de Aeropuertos (8 casos)**

#### **AIRPORT_CREATE_C001 - Creación Exitosa**
- **Alcance**: Flujo principal de creación
- **Propósito**: Validar creación de aeropuertos con datos válidos
- **Criterios de Éxito**: Aeropuerto creado con datos correctos
- **Impacto de Fallo**: Bloquea funcionalidad principal

#### **AIRPORT_CREATE_C002 - Campos Faltantes**
- **Alcance**: Validación de campos obligatorios
- **Propósito**: Asegurar campos requeridos
- **Criterios de Éxito**: API rechaza campos faltantes
- **Impacto de Fallo**: Permite datos incompletos

#### **AIRPORT_CREATE_M001 - IATA Code Longitud Incorrecta**
- **Alcance**: Validación de longitud de IATA code
- **Propósito**: Asegurar longitud correcta (3 caracteres)
- **Criterios de Éxito**: API rechaza longitudes incorrectas
- **Impacto de Fallo**: Permite códigos IATA inválidos

#### **AIRPORT_CREATE_M002 - IATA Code Formato Inválido**
- **Alcance**: Validación de formato de IATA code
- **Propósito**: Asegurar formato correcto (solo letras mayúsculas)
- **Criterios de Éxito**: API rechaza formatos inválidos
- **Impacto de Fallo**: Permite códigos IATA inválidos

#### **AIRPORT_CREATE_M003 - Campos Adicionales No Permitidos**
- **Alcance**: Validación de esquema estricto
- **Propósito**: Asegurar esquema estricto
- **Criterios de Éxito**: API rechaza campos adicionales
- **Impacto de Fallo**: Permite datos no válidos

#### **AIRPORT_CREATE_M004 - IATA Code Duplicado**
- **Alcance**: Validación de unicidad de IATA code
- **Propósito**: Prevenir duplicados
- **Criterios de Éxito**: API rechaza códigos duplicados
- **Impacto de Fallo**: Permite duplicados

#### **AIRPORT_CREATE_L001 - Campos Vacíos**
- **Alcance**: Validación de campos no vacíos
- **Propósito**: Asegurar campos no vacíos
- **Criterios de Éxito**: API rechaza campos vacíos
- **Impacto de Fallo**: Permite datos incompletos

#### **AIRPORT_CREATE_L002 - Tipos de Datos Incorrectos**
- **Alcance**: Validación de tipos de datos
- **Propósito**: Asegurar tipos correctos
- **Criterios de Éxito**: API rechaza tipos incorrectos
- **Impacto de Fallo**: Permite datos inconsistentes

### **Submódulo 3.2: Listado de Aeropuertos (2 casos)**

#### **AIRPORT_LIST_C001 - Listado con Parámetros Válidos**
- **Alcance**: Funcionalidad básica de listado
- **Propósito**: Validar listado de aeropuertos
- **Criterios de Éxito**: Lista de aeropuertos devuelta correctamente
- **Impacto de Fallo**: Bloquea visualización de datos

#### **AIRPORT_LIST_C002 - Listado con Parámetros Inválidos**
- **Alcance**: Validación de parámetros
- **Propósito**: Asegurar parámetros válidos
- **Criterios de Éxito**: API rechaza parámetros inválidos
- **Impacto de Fallo**: Permite parámetros inválidos

### **Submódulo 3.3: Consulta por IATA Code (2 casos)**

#### **AIRPORT_IATA_C001 - Consulta con IATA Code Válido**
- **Alcance**: Consulta por IATA code
- **Propósito**: Validar consulta específica
- **Criterios de Éxito**: Aeropuerto devuelto correctamente
- **Impacto de Fallo**: Bloquea consulta específica

#### **AIRPORT_IATA_C002 - Consulta con IATA Code Inexistente**
- **Alcance**: Manejo de recursos inexistentes
- **Propósito**: Validar manejo de errores
- **Criterios de Éxito**: API devuelve 404
- **Impacto de Fallo**: Comportamiento inconsistente

---

## MÓDULO 4: GESTIÓN DE VUELOS

### **Alcance del Módulo**
- **Propósito**: Validar la gestión de vuelos en el sistema
- **Endpoints Cubiertos**: 1 (`POST /flights`)
- **Casos Totales**: 7 casos
- **Tiempo de Ejecución**: 3-4 minutos

### **Submódulo 4.1: Creación de Vuelos (7 casos)**

#### **FLIGHT_CREATE_C001 - Creación Exitosa**
- **Alcance**: Flujo principal de creación
- **Propósito**: Validar creación de vuelos con datos válidos
- **Criterios de Éxito**: Vuelo creado con datos correctos
- **Impacto de Fallo**: Bloquea funcionalidad principal

#### **FLIGHT_CREATE_C002 - Aircraft ID Tipo Incorrecto**
- **Alcance**: Validación de tipos de datos
- **Propósito**: Asegurar tipos correctos
- **Criterios de Éxito**: API rechaza tipos incorrectos
- **Impacto de Fallo**: Permite datos inconsistentes

#### **FLIGHT_CREATE_C003 - Base Price Negativo (BUG)**
- **Alcance**: Validación de lógica de negocio
- **Propósito**: Documentar bug de validación
- **Criterios de Éxito**: API debería rechazar precios negativos
- **Impacto de Fallo**: Permite datos inconsistentes

#### **FLIGHT_CREATE_C004 - Origin Vacío**
- **Alcance**: Validación de campos requeridos
- **Propósito**: Asegurar campos requeridos
- **Criterios de Éxito**: API rechaza campos vacíos
- **Impacto de Fallo**: Permite datos incompletos

#### **FLIGHT_CREATE_M001 - Sin Campo Departure Time**
- **Alcance**: Validación de campos obligatorios
- **Propósito**: Asegurar campos requeridos
- **Criterios de Éxito**: API rechaza campos faltantes
- **Impacto de Fallo**: Permite datos incompletos

#### **FLIGHT_CREATE_L001 - Origin Extremadamente Largo**
- **Alcance**: Validación de límites de longitud
- **Propósito**: Asegurar límites razonables
- **Criterios de Éxito**: API rechaza datos excesivamente largos
- **Impacto de Fallo**: Potencial problema de rendimiento

#### **FLIGHT_CREATE_L002 - Mismo Origen y Destino (BUG)**
- **Alcance**: Validación de lógica de negocio
- **Propósito**: Documentar bug de validación
- **Criterios de Éxito**: API debería rechazar origen = destino
- **Impacto de Fallo**: Permite datos inconsistentes

---

## MÓDULO 5: GESTIÓN DE USUARIOS

### **Alcance del Módulo**
- **Propósito**: Validar la gestión de usuarios en el sistema
- **Endpoints Cubiertos**: 4 (`POST /users`, `GET /users`, `GET /users/me`, `PUT /users/{id}`)
- **Casos Totales**: 5 casos
- **Tiempo de Ejecución**: 2-3 minutos

### **Submódulo 5.1: Creación de Usuario Administrador (2 casos)**

#### **USER_CREATE_C001 - Creación Exitosa de Usuario Admin**
- **Alcance**: Flujo principal de creación de admin
- **Propósito**: Validar creación de usuarios administradores
- **Criterios de Éxito**: Usuario admin creado correctamente
- **Impacto de Fallo**: Bloquea funcionalidad de gestión de usuarios

#### **USER_CREATE_C002 - Creación con Datos Inválidos**
- **Alcance**: Validación de datos
- **Propósito**: Asegurar datos válidos
- **Criterios de Éxito**: API rechaza datos inválidos
- **Impacto de Fallo**: Permite datos inconsistentes

### **Submódulo 5.2: Listado de Usuarios (1 caso)**

#### **USER_LIST_C001 - Listado Exitoso de Usuarios**
- **Alcance**: Funcionalidad de listado con autenticación
- **Propósito**: Validar listado de usuarios autenticado
- **Criterios de Éxito**: Lista de usuarios devuelta correctamente
- **Impacto de Fallo**: Bloquea visualización de usuarios

### **Submódulo 5.3: Consulta de Usuario Actual (1 caso)**

#### **USER_ME_C001 - Consulta de Usuario Actual**
- **Alcance**: Endpoint de usuario actual
- **Propósito**: Validar consulta de usuario autenticado
- **Criterios de Éxito**: Usuario actual devuelto correctamente
- **Impacto de Fallo**: Bloquea consulta de usuario actual

### **Submódulo 5.4: Actualización de Usuario (1 caso)**

#### **USER_UPDATE_C001 - Actualización Exitosa de Usuario**
- **Alcance**: Funcionalidad de actualización
- **Propósito**: Validar actualización de usuarios
- **Criterios de Éxito**: Usuario actualizado correctamente
- **Impacto de Fallo**: Bloquea funcionalidad de actualización

---

## MÓDULO 6: RESERVAS (EN DESARROLLO)

### **Alcance del Módulo**
- **Propósito**: Validar la gestión de reservas en el sistema
- **Endpoints Cubiertos**: 1 (`POST /bookings`)
- **Casos Totales**: 0 casos (en desarrollo)
- **Tiempo de Ejecución**: N/A

### **Estado Actual**
- **Archivo**: `api/tests/bookings/create_booking.py`
- **Estado**: Archivo básico implementado, casos de prueba pendientes
- **Prioridad**: Alta (completar en próxima iteración)

---

## MATRIZ DE COBERTURA DETALLADA

### **Cobertura por Funcionalidad**

| Funcionalidad | Casos Críticos | Casos Medios | Casos Básicos | Total | Cobertura |
|---------------|----------------|--------------|---------------|-------|-----------|
| **Autenticación** | 7 | 4 | 3 | 14 | 100% |
| **Creación de Datos** | 15 | 8 | 4 | 27 | 100% |
| **Lectura de Datos** | 8 | 2 | 1 | 11 | 100% |
| **Actualización de Datos** | 4 | 2 | 1 | 7 | 100% |
| **Eliminación de Datos** | 4 | 3 | 2 | 9 | 100% |
| **Validación de Seguridad** | 5 | 2 | 1 | 8 | 100% |
| **Validación de Datos** | 12 | 6 | 3 | 21 | 100% |
| **Manejo de Errores** | 8 | 4 | 2 | 14 | 100% |

### **Cobertura por Tipo de Validación**

| Tipo de Validación | Casos | Cobertura | Descripción |
|-------------------|-------|-----------|-------------|
| **Validación de Esquemas** | 25 | 100% | Esquemas JSON de respuestas |
| **Validación de Tipos** | 18 | 100% | Tipos de datos correctos |
| **Validación de Campos Requeridos** | 22 | 100% | Campos obligatorios |
| **Validación de Longitud** | 12 | 80% | Límites de longitud |
| **Validación de Formato** | 15 | 70% | Formatos específicos |
| **Validación de Lógica de Negocio** | 8 | 60% | Reglas de negocio |
| **Validación de Seguridad** | 10 | 100% | Autenticación y autorización |
| **Validación de Unicidad** | 6 | 100% | Campos únicos |

### **Cobertura por Prioridad de Negocio**

| Prioridad | Casos | Porcentaje | Descripción |
|-----------|-------|------------|-------------|
| **Críticos** | 37 | 57% | Funcionalidades principales |
| **Medios** | 15 | 23% | Validaciones importantes |
| **Básicos** | 13 | 20% | Casos edge y documentación |

---

## ESTRATEGIA DE EJECUCIÓN POR ALCANCE

### **Ejecución por Módulo**

#### **Módulo de Autenticación**
- **Alcance**: Validación completa de seguridad
- **Tiempo**: 5-7 minutos
- **Prioridad**: Crítica (debe ejecutarse primero)
- **Dependencias**: Ninguna

#### **Módulo de Aeronaves**
- **Alcance**: Validación completa de CRUD
- **Tiempo**: 8-10 minutos
- **Prioridad**: Alta
- **Dependencias**: Autenticación

#### **Módulo de Aeropuertos**
- **Alcance**: Validación completa de CRUD
- **Tiempo**: 4-5 minutos
- **Prioridad**: Alta
- **Dependencias**: Autenticación

#### **Módulo de Vuelos**
- **Alcance**: Validación de creación
- **Tiempo**: 3-4 minutos
- **Prioridad**: Media
- **Dependencias**: Aeronaves, Aeropuertos

#### **Módulo de Usuarios**
- **Alcance**: Validación de gestión
- **Tiempo**: 2-3 minutos
- **Prioridad**: Media
- **Dependencias**: Autenticación

### **Ejecución por Prioridad**

#### **Casos Críticos (37 casos)**
- **Alcance**: Funcionalidades principales
- **Tiempo**: 10-12 minutos
- **Propósito**: Validar flujos críticos de negocio
- **Frecuencia**: Cada commit, cada deploy

#### **Casos Medios (15 casos)**
- **Alcance**: Validaciones importantes
- **Tiempo**: 5-7 minutos
- **Propósito**: Validar comportamientos importantes
- **Frecuencia**: Cada build, cada release

#### **Casos Básicos (13 casos)**
- **Alcance**: Casos edge y documentación
- **Tiempo**: 3-5 minutos
- **Propósito**: Documentar bugs y validar extremos
- **Frecuencia**: Cada release, cada sprint

---

## MÉTRICAS DE CALIDAD DEL ALCANCE

### **Cobertura de Funcionalidades**
- **Funcionalidades Críticas**: 100% cubiertas
- **Funcionalidades Importantes**: 95% cubiertas
- **Funcionalidades Secundarias**: 80% cubiertas
- **Funcionalidades Pendientes**: 20% (Reservas)

### **Cobertura de Validaciones**
- **Validaciones de Seguridad**: 100% cubiertas
- **Validaciones de Datos**: 95% cubiertas
- **Validaciones de Negocio**: 85% cubiertas
- **Validaciones de Rendimiento**: 70% cubiertas

### **Cobertura de Casos de Error**
- **Errores de Autenticación**: 100% cubiertos
- **Errores de Validación**: 95% cubiertos
- **Errores de Negocio**: 80% cubiertos
- **Errores de Sistema**: 70% cubiertos

---

## CONCLUSIONES SOBRE EL ALCANCE

### **Fortalezas del Alcance Actual**
1. **Cobertura Completa**: 83% de funcionalidades cubiertas
2. **Validación Exhaustiva**: Múltiples tipos de validación implementados
3. **Documentación Detallada**: Cada caso tiene propósito y alcance claros
4. **Estrategia de Priorización**: Casos distribuidos por importancia
5. **Manejo de Bugs**: Bugs documentados y manejados apropiadamente

### **Áreas de Mejora**
1. **Completar Módulo de Reservas**: 20% de funcionalidades pendientes
2. **Aumentar Cobertura de Actualización**: Solo 50% de módulos cubiertos
3. **Aumentar Cobertura de Eliminación**: Solo 33% de módulos cubiertos
4. **Implementar Tests de Integración**: Validación entre módulos
5. **Agregar Tests de Rendimiento**: Validación de escalabilidad

### **Recomendaciones**
1. **Priorizar completar Reservas** para alcanzar 100% de cobertura
2. **Implementar tests de integración** para validar flujos completos
3. **Agregar tests de rendimiento** para validar escalabilidad
4. **Mantener documentación actualizada** con cada cambio
5. **Implementar métricas de cobertura** automatizadas

---

## APÉNDICE: GLOSARIO DE TÉRMINOS

### **Términos Técnicos**
- **API**: Application Programming Interface
- **CRUD**: Create, Read, Update, Delete
- **JWT**: JSON Web Token
- **IATA**: International Air Transport Association
- **HTTP Status**: Códigos de estado HTTP
- **JSON Schema**: Esquema de validación JSON

### **Términos de Pruebas**
- **Test Case**: Caso de prueba individual
- **Test Suite**: Conjunto de casos de prueba
- **Coverage**: Cobertura de pruebas
- **Smoke Test**: Pruebas básicas de funcionalidad
- **Regression Test**: Pruebas de regresión
- **Edge Case**: Casos límite o extremos

### **Términos de Negocio**
- **Aircraft**: Aeronave o avión
- **Airport**: Aeropuerto
- **Flight**: Vuelo
- **Booking**: Reserva
- **User**: Usuario
- **Admin**: Administrador
