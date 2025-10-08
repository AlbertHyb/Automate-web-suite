import os

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@when('el usuario hace clic en el botón "Elige tu cine"')
def step_click_button(context):
    wait = WebDriverWait(context.driver, 10)
    boton = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button//span[text()='Elige tu cine']"))
    )
    boton.click()
    print("️ Clic realizado en el botón 'Elige tu cine'.")
    time.sleep(1)  # espera corta para permitir el despliegue


@then("debe mostrarse un menú desplegable")
def step_validate_dropdown(context):
    # Buscar elementos que representen el menú desplegable
    posibles_menus = context.driver.find_elements(
        By.XPATH,
        "//ul | //div[contains(@class, 'menu') or contains(@class, 'dropdown') or contains(text(),'Selecciona') or contains(text(),'Cine')]"
    )

    if len(posibles_menus) > 0:
        print(f" Se detectó un menú desplegable con {len(posibles_menus)} elemento(s).")
    else:
        raise AssertionError(" No se detectó ningún menú desplegable después de hacer clic en 'Elige tu cine'.")


@when("el usuario hace clic en el botón de búsqueda")
def step_click_search_button(context):
    wait = WebDriverWait(context.driver, 10)
    boton = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button//*[name()='svg' and contains(@class, 'lucide-search')]")
        )
    )
    boton.click()
    print("️ Clic realizado en el botón de búsqueda.")
    time.sleep(1.5)  # esperar un poco por animaciones o carga


@then("debe mostrarse el campo de búsqueda o resultados")
def step_validate_search_field(context):
    wait = WebDriverWait(context.driver, 5)
    posibles_campos = context.driver.find_elements(
        By.XPATH,
        "//input[contains(@type,'text')] | //div[contains(@class,'search')] | //form[contains(@class,'search')]"
    )

    if len(posibles_campos) > 0:
        print(f" Se detectó el campo o contenedor de búsqueda ({len(posibles_campos)} elemento/s).")
    else:
        print(" No se detectó ningún campo de búsqueda.")
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot_path = os.path.join(os.getcwd(), f"error_no_search_{timestamp}.png")
        context.driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot guardada en: {screenshot_path}")
        raise AssertionError(" No se mostró ningún campo de búsqueda después de hacer clic en el botón.")
