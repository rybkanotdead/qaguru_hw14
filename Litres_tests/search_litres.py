from selene import browser, have
import allure



class SearchLitres:

    @allure.step("Открывается сайт 'Литрес'")
    def open(self):
        browser.open('/')

    @allure.step("Вводится в поле поиска значение")
    def fill_search(self, value1):
        browser.element('[data-testid="search__input"]').type(value1)

    @allure.step("Нажимается кнопка 'Поиск'")
    def click_button_search(self):
        browser.element('[data-testid="search__button"]').click()

    @allure.step("Нажимается 'PressEnter' на клавиатуре")
    def press_enter_search(self):
        browser.element('[data-testid="search__input"]').press_enter()

    @allure.step("Проверяются результаты поиска")
    def checking_search_results(self, value1, value2):
        browser.element('[id="pageTitle"]').should(have.text(value1))
        browser.element('[data-testid="art__title"][href="/book/lev-tolstoy/voyna-i-mir-66691848/"]').should(
            have.text(value2))