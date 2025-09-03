# Estructura real del proyecto

Automate-web-suite/
├── api/                    # Lógica y helpers de API
│   ├── api_helper.py       # Helper para requests a la API
│   ├── schemas/            # Esquemas JSON para validación
│   └── tests/              # Pruebas automatizadas de API
│       ├── auth_login.py
│       ├── auth_signup.py
│       ├── conftest.py     # Fixtures y configuración de tests de API
│       └── ...
├── config/                 # Configuración centralizada
│   ├── settings.py         # Configuración y carga de variables de entorno
│   ├── config.py
│   ├── constants.py
│   └── settings.json
├── features/               # Pruebas BDD (Gherkin, Behave)
│   ├── environment.py
│   ├── login.feature
│   └── steps/
├── pages/                  # Page Objects para pruebas de UI
│   └── base_page.py
├── utils/                  # Utilidades generales (drivers, helpers)
│   └── driver_factory.py
├── reports/                # Reportes generados por pytest
├── Reportes/               # (Carpeta alternativa de reportes, revisar uso)
├── requirements.txt        # Dependencias del proyecto
├── README.md               # Documentación principal
├── STRUCTURE.md            # Estructura del proyecto (este archivo)
├── pytest.ini              # Configuración de pytest
├── .env                    # Variables de entorno (no subir)
└── ...otros archivos

> Nota: Esta estructura refleja el estado actual del proyecto y puede diferir de la sugerida inicialmente. Toda la configuración se centraliza en `config/settings.py` y las pruebas de API están en `api/tests/`.

