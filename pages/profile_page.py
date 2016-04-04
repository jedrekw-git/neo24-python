# coding=utf-8
from selenium.webdriver.common.by import By
from pages.base import BasePage
from utils.utils import *
from random import randint
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from change_password import *

class ProfilePage(BasePage):
    _title = "Profile Page"

    _name_field = (By.XPATH, "//div[2]/div/input")
    _name_value = get_random_string(7)
    _surname_field = (By.XPATH, "//div[2]/div[2]/input")
    _surname_value = get_random_string(8)
    _company_name_field = (By.XPATH, "//div[2]/div[3]/input")
    _company_name_value = get_random_string(8)
    _NIP_field = (By.XPATH, "//div[4]/input")
    _NIP_value = get_random_integer(3)+"-"+get_random_integer(3)+"-"+get_random_integer(2)+"-"+get_random_integer(2)
    _phone_field = (By.XPATH, "//div[5]/input")
    _phone_value = get_random_integer(9)
    _invoice_name_field = (By.XPATH, "//div[3]/div/input")
    _invoice_name_value = get_random_string(7)
    _invoice_surname_field = (By.XPATH, "//div[3]/div[2]/input")
    _invoice_surname_value = get_random_string(8)
    _invoice_street_field = (By.XPATH, "//div[3]/div[3]/input")
    _invoice_street_value = get_random_string(8)
    _invoice_house_nr_field = (By.XPATH, "//div[3]/div[4]/input")
    _invoice_house_nr_value = get_random_integer(2)
    _invoice_apartment_nr_field = (By.XPATH, "//div[3]/div[5]/input")
    _invoice_apartment_nr_value = get_random_integer(2)
    _invoice_postal_code_field = (By.XPATH, "//div[6]/input")
    _invoice_postal_code_value = get_random_integer(2)+"-"+get_random_integer(3)
    _invoice_city_field = (By.XPATH, "//div[7]/input")
    _invoice_city_value = get_random_string(7)
    _my_data_save_button = (By.ID, "save_profile_but")
    _change_password_menu = (By.XPATH, "//section/div/ul/li[2]/a")
    _change_password_new_field = (By.XPATH, "//form/fieldset/div[2]/input")
    _change_password_new2_field = (By.XPATH, "//form/fieldset/div[3]/input")
    _change_password_submit = (By.XPATH, "//div[4]/span/span/input")

    def __init__(self, driver):
        super(ProfilePage, self).__init__(driver, self._title)

    def change_user_data(self):
        self.clear_field_and_send_keys(self._name_value, self._name_field)
        self.clear_field_and_send_keys(self._surname_value, self._surname_field)
        self.clear_field_and_send_keys(self._company_name_value, self._company_name_field)
        self.clear_field_and_send_keys(self._NIP_value, self._NIP_field)
        self.clear_field_and_send_keys(self._phone_value, self._phone_field)
        self.clear_field_and_send_keys(self._invoice_name_value, self._invoice_name_field)
        self.clear_field_and_send_keys(self._invoice_surname_value, self._invoice_surname_field)
        self.clear_field_and_send_keys(self._invoice_street_value, self._invoice_street_field)
        self.clear_field_and_send_keys(self._invoice_house_nr_value, self._invoice_house_nr_field)
        self.clear_field_and_send_keys(self._invoice_apartment_nr_value, self._invoice_apartment_nr_field)
        self.clear_field_and_send_keys(self._invoice_postal_code_value, self._invoice_postal_code_field)
        self.clear_field_and_send_keys(self._invoice_city_value, self._invoice_city_field)
        self.get_driver().execute_script("arguments[0].click();", self.find_element(self._my_data_save_button))
        # self.click(self._my_data_save_button)

    def get_value_name(self):
        return self.get_value(self._name_field)

    def get_value_surname(self):
        return self.get_value(self._surname_field)

    def get_value_company_name(self):
        return self.get_value(self._company_name_field)

    def get_value_NIP(self):
        return self.get_value(self._NIP_field)

    def get_value_phone(self):
        return self.get_value(self._phone_field)

    def get_value_invoice_name(self):
        return self.get_value(self._invoice_name_field)

    def get_value_invoice_surname(self):
        return self.get_value(self._invoice_surname_field)

    def get_value_invoice_street(self):
        return self.get_value(self._invoice_street_field)

    def get_value_invoice_house_nr(self):
        return self.get_value(self._invoice_house_nr_field)

    def get_value_invoice_apartment_nr(self):
        return self.get_value(self._invoice_apartment_nr_field)

    def get_value_invoice_postal_code(self):
        return self.get_value(self._invoice_postal_code_field)

    def get_value_invoice_city(self):
        return self.get_value(self._invoice_city_field)

    def change_password(self):
        self.get_driver().execute_script("arguments[0].click();", self.find_element(self._change_password_menu))
        # self.click(self._change_password_menu)
        change_password_value('change_pass2.txt')
        self.clear_field_and_send_keys(get_password('change_pass2.txt'), self._change_password_new_field)
        self.clear_field_and_send_keys(get_password('change_pass2.txt'), self._change_password_new2_field)
        self.click(self._change_password_submit)