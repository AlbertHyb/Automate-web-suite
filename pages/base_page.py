from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self, url: str):
        self.driver.get(url)

    def find(self, locator: tuple, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located(locator)
        )

    def click(self, locator: tuple, timeout: int = 10):
        el = WebDriverWait(self.driver, timeout).until(
            ec.element_to_be_clickable(locator)
        )
        el.click()

    def type(self, locator: tuple, text: str, clear: bool = True, timeout: int = 10):
        el = self.find(locator, timeout)
        if clear:
            el.clear()
        el.send_keys(text)

    def text_of(self, locator: tuple, timeout: int = 10) -> str:
        return self.find(locator, timeout).text

    def current_url(self) -> str:
        return self.driver.current_url
