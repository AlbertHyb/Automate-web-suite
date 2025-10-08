# Proyecto: Automatización de Pruebas BDD para Sitio de Cine

Este proyecto utiliza *Behave* (BDD), *Selenium* y *webdriver-manager* para automatizar pruebas sobre un sitio web de cine.

## Requisitos previos
- Python 3.7 o superior
- pip
- Google Chrome o Firefox instalado

## Instalación y configuración

1. *Crea y activa un entorno virtual:*
   bash
   python3 -m venv venv
   source venv/bin/activate
   

2. *Instala las dependencias:*
   bash
   pip install selenium behave webdriver-manager
   
   O si tienes un archivo requirements.txt:
   bash
   pip install -r requirements.txt
   

3. *(Opcional) Guarda las dependencias instaladas:*
   bash
   pip freeze > requirements.txt
   

## Ejecución de pruebas

- Para ejecutar todos los escenarios:
  bash
  behave
  
- Para ejecutar un feature específico (por ejemplo, cine):
  bash
  behave features/cine.feature
  
- Para ejecutar el feature de fallidos:
  bash
  behave features/cine-fallidos.feature
  

## Notas adicionales
- Puedes modificar la resolución de la ventana del navegador en la configuración del driver (por ejemplo, usando options.add_argument('--window-size=1920,1080') para Chrome).
- El proyecto usa webdriver-manager para gestionar automáticamente los drivers de navegador.

## Recursos útiles
- [Behave Documentation](https://behave.readthedocs.io/en/stable/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager)

---

Si tienes dudas, revisa los archivos de ejemplo en features/ y los pasos en features/steps/.