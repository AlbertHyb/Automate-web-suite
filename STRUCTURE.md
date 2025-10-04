# Estructura del proyecto API Testing

```
Automate-web-suite/
├── api/                    # Pruebas y lógica de API
│   ├── api_helper.py       # Helper para requests HTTP
│   ├── schemas/            # Esquemas para validación de respuestas
│   │   ├── login_schemas.py
│   │   ├── signup_schemas.py
│   │   ├── user_schemas.py
│   │   └── ...
│   └── tests/              # Tests de API organizados por funcionalidad
│       ├── conftest.py     # Fixtures principales para API
│       ├── auth/           # Tests de autenticación
│       │   ├── auth_login.py
│       │   └── auth_signup.py
│       ├── users/          # Tests de usuarios
│       │   ├── user_create.py
│       │   ├── user_delete.py
│       │   └── user_update.py
│       └── airports/       # Tests de aeropuertos
├── config/                 # Configuración centralizada
│   ├── settings.py         # Variables de entorno y configuración
│   ├── constants.py        # Constantes del proyecto
│   └── config.py          # Configuración adicional
├── features/               # Tests BDD con Behave
│   ├── environment.py      # Configuración de Behave
│   ├── *.feature          # Archivos Gherkin
│   └── steps/             # Implementación de steps
├── reports/                # Reportes generados
├── utils/                  # Utilidades compartidas
│   └── driver_factory.py  # Solo si usas UI testing
├── .env                    # Variables de entorno (no versionar)
├── pytest.ini             # Configuración de pytest
├── requirements.txt        # Dependencias
└── README.md              # Documentación
```

## Principios de esta estructura:

1. **Separación clara**: API tests, BDD tests, y configuración separados
2. **No duplicación**: Una sola ubicación para cada tipo de archivo
3. **Escalabilidad**: Fácil agregar nuevos tests por módulos
4. **Mantenibilidad**: Configuración centralizada en `config/`