import time
from time import sleep

from behave import when, given, then
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@given("El usuario accede a la URL del sitio web de cine")
def step_open_browser(context):
    context.page = BasePage(context.driver)
    context.page.open('https://fake-cinema.vercel.app/')  # usa la URL del config.py


@when('el usuario selecciona la pelicula "{name}"')
def step_impl(context, name):
    base = BasePage(context.driver)
    # selector dinámico basado en el alt del póster
    locator = (By.XPATH, f'//img[contains(@alt, "Poster de {name}")]')
    base.click(locator)

@when('el usuario selecciona la fecha actual')
def step_impl(context):
    from datetime import datetime
    base = BasePage(context.driver)
    hoy = datetime.now().day+1  # obtiene el día actual, por ejemplo 7

    # Busca el botón que contiene el número del día actual
    locator = (By.XPATH, f'//button[.//div[text()="{hoy}"]]')
    base.click(locator)


@when('el usuario selecciona un horario disponible')
def step_impl(context):
    # Encuentra todos los horarios (enlaces <a> con href que contiene "/book")
    horarios = context.driver.find_elements(By.XPATH, '//a[contains(@href, "/book")]')

    if not horarios:
        raise AssertionError("No se encontraron horarios disponibles")
    # Selecciona el primero (puedes hacerlo aleatorio si prefieres)
    horarios[0].click()
    sleep(2)  # espera a que cargue la página de selección de asientos


@when('el usuario selecciona los asientos de la fila "{fila}" con numeros {numeros}')
def step_impl(context, fila, numeros):

    print(f"\n Iniciando selección de asientos: Fila {fila}, Números {numeros}")

    wait = WebDriverWait(context.driver, 10)

    # Esperar que el contenedor principal esté presente
    print("⏳ Esperando que el contenedor de asientos esté visible...")
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class,'flex gap-1.5')]")
        )
    )
    print(" Contenedor principal detectado correctamente.")

    # Calcular el índice de la fila (A=1, B=2, ..., L=12)
    fila_index = ord(fila.upper()) - ord('A') + 1
    print(f" Fila {fila} → índice {fila_index}")

    # Convertir los números recibidos a lista
    asientos = [int(n.strip()) for n in numeros.split(',')]
    print(f" Asientos a seleccionar: {asientos}")

    for numero in asientos:
        # Generar el XPath dinámico basado en la fila y el asiento
        xpath = f"(//div[contains(@class,'flex gap-1.5')])[{fila_index}]/button[{numero}]"
        try:
            print(f"️ Intentando clic en asiento {fila}{numero} → {xpath}")
            asiento = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", asiento)
            time.sleep(0.5)
            asiento.click()
            print(f" Asiento {fila}{numero} seleccionado correctamente.")
        except Exception as e:
            print(f" Error al seleccionar el asiento {fila}{numero}: {e}")

    print(" Selección de asientos completada ")





@when('el usuario da clic en comprar boletos')
def step_impl(context):
    from selenium.webdriver.common.by import By
    base = BasePage(context.driver)
    locator = (By.XPATH, '//button[contains(., "Comprar boletos")]')
    base.click(locator)
    time.sleep(2)


@when('el usuario ingresa la cantidad de persona "{cantidadGente}"')
def step_impl(context, cantidadGente):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time

    print(f"\n🎟️ Iniciando selección de boletos con cantidades: {cantidadGente}")

    wait = WebDriverWait(context.driver, 10)

    # Esperar que aparezca el modal (role="dialog")
    print("⏳ Esperando que aparezca el modal de selección de boletos...")
    modal = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
    )
    print("✅ Modal detectado correctamente.")

    # Dividir las cantidades: niños, adultos, adultos mayores
    try:
        ninos, adultos, mayores = [int(x.strip()) for x in cantidadGente.split(',')]
    except Exception as e:
        raise AssertionError(f"❌ Error al interpretar las cantidades '{cantidadGente}': {e}")

    print(f"👶 Niños: {ninos}, 👨 Adultos: {adultos}, 👴 Adultos mayores: {mayores}")

    # Localizadores por ID
    campos = {
        "kids": ninos,
        "adults": adultos,
        "elderly": mayores,
    }

    # Llenar cada campo
    for campo_id, valor in campos.items():
        try:
            campo = wait.until(EC.presence_of_element_located((By.ID, campo_id)))
            context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo)
            campo.clear()
            campo.send_keys(str(valor))
            print(f"✅ Campo '{campo_id}' actualizado con valor {valor}.")
            time.sleep(0.3)
        except Exception as e:
            raise AssertionError(f"❌ No se pudo llenar el campo '{campo_id}': {e}")

    # Confirmar
    try:
        boton_confirmar = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Confirmar')]"))
        )
        boton_confirmar.click()
        print("🎯 Clic en 'Confirmar' realizado correctamente ✅")
    except Exception as e:
        raise AssertionError(f"❌ Error al hacer clic en Confirmar: {e}")



@when('el usuario procede al pago')
def step_impl(context):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time

    print("\n💳 Intentando proceder al pago...")

    wait = WebDriverWait(context.driver, 10)

    # --- Paso 1: Clic en “Proceder al pago” ---
    try:
        boton_pago = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Proceder al pago')]"))
        )
        context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_pago)
        time.sleep(0.5)
        boton_pago.click()
        print("✅ Se hizo clic en 'Proceder al pago'.")
    except Exception as e:
        raise AssertionError(f"❌ No se pudo hacer clic en 'Proceder al pago': {e}")

    # --- Paso 2: Esperar el formulario ---
    print("⏳ Esperando el formulario de pago...")
    wait.until(EC.presence_of_element_located((By.ID, "firstName")))
    print("✅ Formulario detectado.")

    # --- Paso 3: Completar el formulario ---
    campos = {
        "firstName": "karen",
        "lastName": "rojas",
        "email": "krojas.tester@fake.com",
        "cardName": "Karen Rojas",
        "cardNumber": "4111111111111111",  # número de prueba Visa
        "cvv": "123"
    }

    for campo_id, valor in campos.items():
        try:
            campo = wait.until(EC.presence_of_element_located((By.ID, campo_id)))
            campo.clear()
            campo.send_keys(valor)
            print(f"📝 Campo '{campo_id}' completado con '{valor}'.")
            time.sleep(0.3)
        except Exception as e:
            raise AssertionError(f"❌ No se pudo llenar el campo '{campo_id}': {e}")

    # --- Paso 4: Confirmar pago ---
    try:
        boton_confirmar = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Confirmar pago')]"))
        )
        context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_confirmar)
        time.sleep(0.5)
        boton_confirmar.click()
        print("🎯 Clic en 'Confirmar pago' realizado correctamente ✅")
    except Exception as e:
        raise AssertionError(f"❌ Error al confirmar el pago: {e}")

    # --- Paso 5: Confirmar que el pago fue exitoso ---
    try:
        time.sleep(2)
        mensaje = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Pago exitoso') or contains(text(),'Gracias')]"))
        )
        print(f"🎉 Pago completado: {mensaje.text}")
    except:
        print("⚠️ No se encontró mensaje de confirmación (puede no estar implementado aún).")


@then('el pago debe completarse exitosamente')
def step_impl(context):
    print("\n🧾 Validando mensaje de confirmación de pago...")

    wait = WebDriverWait(context.driver, 10)
    try:
        titulo = wait.until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'¡Pago completado!')]"))
        )
        assert titulo.is_displayed(), "El mensaje '¡Pago completado!' no está visible."
        print("✅ Validación exitosa: ¡Pago completado! está visible en la pantalla.")
    except Exception as e:
        raise AssertionError(f"❌ No se encontró el mensaje de '¡Pago completado!': {e}")