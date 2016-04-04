# coding=utf-8
from selenium.webdriver.common.by import By
from pages.base import BasePage
from utils.utils import *
from random import randint
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.profile_page import ProfilePage


class HomePage(BasePage):
    _title = "neo24.pl"
    _url = "http://www.neo24.pl/"
    _close_privacy_policy_bar_button = (By.XPATH, "//body/div[2]/div[2]/a[2]")

    def __init__(self, driver):
        super(HomePage, self).__init__(driver, self._title, self._url)

    def open_home_page(self):
        self.get(self._url)
        self.is_the_current_page()
        self.click(self._close_privacy_policy_bar_button)
        return self
