import os

# Puedes cambiarlo por variables de entorno si quieres
BASE_URL = os.getenv("BASE_URL", "https://fake-cinema.vercel.app/")
BROWSER = os.getenv("BROWSER", "chrome")
IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "5"))