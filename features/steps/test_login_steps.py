from behave import given, when, then
from pages.base_page import BasePage
from utils.config import BASE_URL

@given("que el usuario abre el navegador")
def step_open_browser(context):
    context.page = BasePage(context.driver)

@when("accede a la página de inicio")
def step_go_to_home(context):
    context.page.open(BASE_URL)

@then("la página debería cargar con el título correcto")
def step_validate_title(context):
    title = context.driver.title.strip()
    assert title != "", "La página no tiene título"
    assert "Cinema" in title or "v0 App" in title, f"Título inesperado: {title}"
