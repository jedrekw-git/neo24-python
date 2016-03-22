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

class RegisterUserPage(BasePage):
    _title = "Register User Page"

    _name_field = (By.XPATH, "//div/input")
    _name_value = get_random_string(7)
    _surname_field = (By.XPATH, "//div[2]/input")
    _surname_value = get_random_string(8)
    _company_name_field = (By.XPATH, "//div[3]/input")
    _company_name_value = get_random_string(8)
    _NIP_field = (By.XPATH, "//div[4]/input")
    _NIP_value = get_random_integer(3)+"-"+get_random_integer(3)+"-"+get_random_integer(2)+"-"+get_random_integer(2)
    _phone_field = (By.XPATH, "//div[5]/input")
    _phone_value = get_random_integer(9)
    _email_field = (By.XPATH, "//form/div[2]/input")
    _email_value = get_random_string(7)+"@"+get_random_string(5)+".pl"
    _password1_field = (By.XPATH, "//form/div[3]/input")
    _password2_field = (By.XPATH, "//form/div[4]/input")
    _password_value = get_random_uuid(8)
    _accept1_checkbox = (By.XPATH, "//form/div[5]/label")
    _accept2_checkbox = (By.XPATH, "//div[6]/label")
    _accept3_checkbox = (By.XPATH, "//div[2]/span/strong")
    _register_account_submit_button = (By.XPATH, "//span/input")

    def __init__(self, driver):
        super(RegisterUserPage, self).__init__(driver, self._title)

    def register_user(self):
        self.clear_field_and_send_keys(self._name_value, self._name_field)
        self.clear_field_and_send_keys(self._surname_value, self._surname_field)
        self.clear_field_and_send_keys(self._company_name_value, self._company_name_field)
        self.clear_field_and_send_keys(self._NIP_value, self._NIP_field)
        self.clear_field_and_send_keys(self._phone_value, self._phone_field)
        self.clear_field_and_send_keys(self._email_value, self._email_field)
        self.clear_field_and_send_keys(self._password_value, self._password1_field)
        self.clear_field_and_send_keys(self._password_value, self._password2_field)
        self.click(self._accept1_checkbox)
        self.click(self._accept2_checkbox)
        self.click(self._accept3_checkbox)
        self.click(self._register_account_submit_button)
        return ProfilePage(self.get_driver())

