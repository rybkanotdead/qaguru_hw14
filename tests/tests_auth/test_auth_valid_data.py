import os
import allure
from allure_commons.types import Severity
from selene import browser

from Litres_tests.auth_litres import AuthorisationLitres


authorisation_litres = AuthorisationLitres()


@allure.tag("web")
@allure.severity(Severity.MINOR)
@allure.label("owner", "Rybka")
@allure.feature("Авторизация пользователя")
@allure.story("Пользователь может авторизоваться с валидными данными")
@allure.description("Простые тесты на проверку авторизации пользователя")
@allure.suite("UI-Тесты")
@allure.link("https://www.litres.ru/", name="Testing")
@allure.title("Авторизация с валидными данными")
def test_checking_authorisation_valid_data():
    litres_login = os.getenv("LITRES_LOGIN")
    litres_password = os.getenv("LITRES_PASSWORD")

    # GIVEN
    authorisation_litres.open()

    # WHEN
    authorisation_litres.press_tab_login()
    authorisation_litres.fill_login(litres_login)
    authorisation_litres.press_continue()
    authorisation_litres.fill_password(litres_password)
    authorisation_litres.press_enter()
    authorisation_litres.personal_account_entrance()

    # THEN
    authorisation_litres.should_have_authorized(litres_login, "Выход")