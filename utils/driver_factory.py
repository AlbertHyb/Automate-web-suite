# utils/driver_factory.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

def create_driver(browser: str = "chrome"):
    browser = browser.lower()

    if browser == "chrome":
        options = ChromeOptions()
        # Descomenta esta línea si quieres sin ventana (headless)
        # options.add_argument("--headless=new")
        options.add_argument("--window-size=1366,768")
        return webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        # options.add_argument("--headless")
        options.add_argument("--width=1366")
        options.add_argument("--height=768")
        return webdriver.Firefox(options=options)

    else:
        raise ValueError(f"Navegador no soportado: {browser}")
