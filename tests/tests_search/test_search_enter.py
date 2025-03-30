import allure
from allure_commons.types import Severity
from Litres_tests.search_litres import SearchLitres

@allure.tag("web")
@allure.severity(Severity.MINOR)
@allure.label("owner", "Rybka")
@allure.feature("Проверка поиска")
@allure.story("Пользователь может подтвердить результаты ввода кнопкой 'Поиск'")
@allure.description("Простые тесты на проверку поиска")
@allure.suite("UI-Тесты")
@allure.link("https://www.litres.ru/", name="Testing")
@allure.title("Проверка поиска через кнопку 'Поиск'")
def test_search_press_enter_audio_author():
    search_litres = SearchLitres()
    # GIVEN
    search_litres.open()

    # WHEN
    search_litres.fill_search("Война и мир")
    search_litres.press_enter_search()

    # THEN
    search_litres.checking_search_results('Результаты поиска «Война и мир»', 'Война и мир')
