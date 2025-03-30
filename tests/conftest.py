import pytest
import os
import logging
import time
import requests
from dotenv import load_dotenv
from selene.support.shared import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import attach

logger = logging.getLogger((__name__))
DEFAULT_BROWSER_VERSION = "128.0"
DEFAULT_WINDOW_WIDTH = int(os.getenv("BROWSER_WINDOW_WIDTH", 1700))
DEFAULT_WINDOW_HEIGHT = int(os.getenv("BROWSER_WINDOW_HEIGHT", 1080))


def pytest_addoption(parser):
    parser.addoption("--browser_version", default=DEFAULT_BROWSER_VERSION)


def is_selenoid_available(url):
    try:
        response = requests.get(f"http://{url}/status", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function", autouse=True)
def setup_browser(request):
    browser_version = request.config.getoption("--browser_version")
    browser.config.base_url = "https://www.litres.ru/"
    browser.config.timeout = 10
    browser.config.window_width = DEFAULT_WINDOW_WIDTH
    browser.config.window_height = DEFAULT_WINDOW_HEIGHT

    driver_options = webdriver.ChromeOptions()
    driver_options.page_load_strategy = "eager"

    # Получаем данные Selenoid
    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    selenoid_url = os.getenv("SELENOID_URL")

    if selenoid_url:
        if not selenoid_login or not selenoid_pass:
            pytest.exit("Для запуска в Selenoid необходимо задать SELENOID_LOGIN и SELENOID_PASS", returncode=1)

        if not is_selenoid_available(selenoid_url):
            pytest.exit(f"Selenoid недоступен по адресу {selenoid_url}", returncode=1)

        print(f"Запуск через Selenoid: {selenoid_url}")
        options = Options()
        selenoid_capabilities = {
            "browserName": "chrome",
            "browserVersion": browser_version,
            "selenoid:options": {"enableVNC": True, "enableVideo": True},
        }
        options.capabilities.update(selenoid_capabilities)

        browser.config.driver = webdriver.Remote(
            command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
            options=options,
        )
    else:
        print("SELENOID_URL не задан! Запуск локального Chrome.")
        browser.config.driver = webdriver.Chrome(options=driver_options)
    time.sleep(5)
    browser.open("/")

    yield

    # Завершение теста и добавление аттачей
    try:
        if browser.driver.session_id:
            attach.add_html(browser)
            attach.add_screenshot(browser)
            attach.add_logs(browser)
            attach.add_video(browser)
    finally:
        browser.quit()