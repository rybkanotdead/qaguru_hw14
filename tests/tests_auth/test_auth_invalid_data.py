import allure
from allure_commons.types import Severity

from Litres_tests.auth_litres import AuthorisationLitres

@allure.tag("web")
@allure.severity(Severity.MINOR)
@allure.label("owner", "Rybka")
@allure.feature("Авторизация пользователя")
@allure.story("Пользователь не может авторизоваться с невалидными данными")
@allure.description("Простые тесты на проверку авторизации пользователя")
@allure.suite("UI-Тесты")
@allure.link("https://www.litres.ru/", name="Testing")
@allure.title("Невозможность авторизации с невалидными данными")
def test_checking_authorisation_invalid_data():
    authorisation_litres = AuthorisationLitres()
    #GIVEN
    authorisation_litres.open()

    #WHEN
    authorisation_litres.press_tab_login()
    authorisation_litres.fill_login('qweasdzxc')
    authorisation_litres.press_continue()
    authorisation_litres.fill_password('qweasdzxc')
    authorisation_litres.press_enter()

    #THEN
    authorisation_litres.should_not_have_authorized('Ввести пароль', 'Неверное сочетание логина и пароля', 'Войти')
