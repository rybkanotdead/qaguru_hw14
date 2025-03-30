import pytest
from selene.support.shared import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import attach
from dotenv import load_dotenv
import os
import time

DEFAULT_BROWSER_VERSION = "128.0"


def pytest_addoption(parser):
    parser.addoption("--browser_version", default=DEFAULT_BROWSER_VERSION)


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function", autouse=True)
def setup_browser(request):
    browser_version = request.config.getoption("--browser_version")
    browser.config.base_url = "https://www.litres.ru/"
    browser.config.timeout = 10

    driver_options = webdriver.ChromeOptions()
    driver_options.page_load_strategy = "eager"
    browser.config.window_width = 1700
    browser.config.window_height = 1080

    # Получаем данные Selenoid
    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    selenoid_url = os.getenv("SELENOID_URL")

    if selenoid_url:  # Если Selenoid URL задан, запускаем удалённо
        print(f"Запуск через Selenoid: {selenoid_url}")
        options = Options()
        selenoid_capabilities = {
            "browserName": "chrome",
            "browserVersion": browser_version,
            "selenoid:options": {"enableVNC": True, "enableVideo": True},
        }
        options.capabilities.update(selenoid_capabilities)

        browser.config.driver = webdriver.Remote(
            command_executor=f"http://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
            options=options,
        )
    else:  # Если нет Selenoid, запускаем локально
        print("SELENOID_URL не задан! Запуск локального Chrome.")
        browser.config.driver = webdriver.Chrome(options=driver_options)

    browser.wait_until(lambda: browser.driver.current_url.startswith("https://www.litres.ru/"))

    yield

    # Завершение теста и добавление аттачей
    if browser.driver.session_id:
        attach.add_html(browser)
        attach.add_screenshot(browser)
        attach.add_logs(browser)
        attach.add_video(browser)
        browser.quit()
