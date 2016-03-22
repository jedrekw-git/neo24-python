# coding=utf-8
from selenium.webdriver.common.by import By
from pages.page import Page
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from pages.register_user import RegisterUserPage


class HeaderRegion(Page):
    _my_account_button = (By.XPATH, "//a/span")
    _login_button = (By.LINK_TEXT, "Zaloguj się")
    _login_field = (By.NAME, "user_login")
    _password_field = (By.NAME, "password")
    _login_submit = (By.XPATH, "//input[@value='Zaloguj się']")
    _base_url = "http://www.neo24.pl/"
    _logout_button = (By.LINK_TEXT, u"Wyloguj się")

    def login(self, login, password):
        self.click(self._my_account_button)
        self.click(self._login_button)
        self.send_keys(login, self._login_field)
        self.send_keys(password, self._password_field)
        self.click(self._login_submit)

    def logout(self):
        self.click(self._my_account_button)
        self.click(self._logout_button)

    def open_register_user_page(self):
        self.get(self._base_url + "index.php?dispatch=profiles.add&user_type=C")
        return RegisterUserPage(self.get_driver())
