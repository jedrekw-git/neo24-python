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

class CategoryPage(BasePage):
    _title = "Category Page"

    _sort_dropdown = (By.XPATH, "//form/div[2]/div/span[3]")
    _sort_price_ascending_option = (By.XPATH, "//form/div[2]/div[2]/ul/li[3]/span")
    _sort_price_descending_option = (By.XPATH, "//form/div[2]/div[2]/ul/li[4]/span")
    _sort_alphabetically_ascending_option = (By.XPATH, "//form/div[2]/div[2]/ul/li/span")
    _sort_alphabetically_descending_option = (By.XPATH, "//form/div[2]/div[2]/ul/li[2]/span")
    _first_product_price_field = (By.XPATH, "//span/span/span")
    _second_product_price_field = (By.XPATH, "//article[2]/form/div[2]/div[2]/span/span/span")
    _third_product_price_field = (By.XPATH, "//article[3]/form/div[2]/div[2]/span/span/span")
    _fourth_product_price_field = (By.XPATH, "//article[4]/form/div[2]/div[2]/span/span/span")
    _first_product_name_field = (By.XPATH, "//form/div/h3/a")
    _second_product_name_field = (By.XPATH, "//article[2]/form/div/h3/a")
    _third_product_name_field = (By.XPATH, "//article[3]/form/div/h3/a")
    _fourth_product_name_field = (By.XPATH, "//article[4]/form/div/h3/a")
    _first_product_screen_size_field = (By.XPATH, "//li[2]/strong")
    _first_product_hdmi_field = (By.XPATH, "//li/strong")
    _first_product_HD_standard_field = (By.XPATH, '//li[3]/strong')
    _filter_price_menu = (By.XPATH, "//h5/span[3]")
    _filter_price_first_field = (By.NAME, "left_slider_545_1")
    _filter_price_first_value = randint(1000, 2500)
    _filter_price_second_field = (By.NAME, "right_slider_545_1")
    _filter_price_second_value = randint(2501, 5000)
    _filter_submit = (By.XPATH, "//div[16]/a")
    _processing_info = (By.XPATH, "/html/body/div[1]/div[3]/div")
    _filter_producer_menu = (By.XPATH, "//div[2]/h5/span[3]")
    _filter_producer_random_producer_index = randint(1, 14)
    _filter_producer_random_producer_checkbox = (By.XPATH, "(//input[@name='flt[]'])[%s]" %_filter_producer_random_producer_index)
    _filter_producer_random_producer_field = (By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div[2]/div/div/menu/div/div[2]/div/ul/li/ul/li[%s]/span[1]" %_filter_producer_random_producer_index)
    _filter_TV_screen_size_menu = (By.XPATH, "//div[4]/h5/span[3]")
    _filter_TV_screen_size_from_dropdown = (By.XPATH, "//div/span[3]")
    _filter_TV_screen_size_from_option = (By.XPATH, "//div[2]/ul/li[%s]" % randint(1,8))
    _filter_TV_screen_size_to_dropdown = (By.XPATH, "//label[2]/div[2]/div/span[3]")
    _filter_TV_screen_size_to_option = (By.XPATH, "//label[2]/div[2]/div[2]/ul/li[%s]" % randint(9,18))
    _filter_TV_hz_menu = (By.XPATH, "//div[15]/h5/span[3]")
    _filter_TV_hz_from_dropdown = (By.XPATH, "//div[15]/div/div/label/div[2]/div/span[3]")
    _filter_TV_hz_from_option = (By.XPATH, "//div[15]/div/div/label/div[2]/div[2]/ul/li[%s]" % randint(1,5))
    _filter_TV_hz_to_dropdown = (By.XPATH, "//div[15]/div/div/label[2]/div[2]/div/span[3]")
    _filter_TV_hz_to_option = (By.XPATH, "//div[15]/div/div/label[2]/div[2]/div[2]/ul/li[%s]" % randint(6,10))
    _compare_first_product_checkbox = (By.XPATH, "//div[3]/div/label/span")
    _compare_second_product_checkbox = (By.XPATH, "//article[2]/form/div[2]/div/div[3]/div/label/span")
    _compare_third_product_checkbox = (By.XPATH, "//article[3]/form/div[2]/div/div[3]/div/label/span")
    _compare_fourth_product_checkbox = (By.XPATH, "//article[4]/form/div[2]/div/div[3]/div/label/span")
    _compare_continue_shopping_button = (By.XPATH, "//div/span/span/a")
    _compare_submit_button = (By.XPATH, "//div[2]/span/span/a")
    _compare_first_product_name_field = (By.XPATH, "//td[5]/div[2]/form/a")
    _compare_second_product_name_field = (By.XPATH, "//td[4]/div[2]/form/a")
    _compare_third_product_name_field = (By.XPATH, "//td[3]/div[2]/form/a")
    _compare_fourth_product_name_field = (By.XPATH, "//td[2]/div[2]/form/a")
    _compare_first_product_price_field = (By.XPATH, "//td[5]/div[2]/form/div/div/p[2]")
    _compare_second_product_price_field = (By.XPATH, "//td[4]/div[2]/form/div/div/p[2]")
    _compare_third_product_price_field = (By.XPATH, "//td[3]/div[2]/form/div/div/p[2]")
    _compare_fourth_product_price_field = (By.XPATH, "//td[2]/div[2]/form/div/div/p[2]")
    _details_first_product_name_field = (By.XPATH, "//header/h1")
    _details_first_product_price_field = (By.XPATH, "//section[3]/div/div")
    _details_first_product_screen_size_field = (By.XPATH, "//article/div[2]/div")
    _details_first_product_hdmi_field = (By.XPATH, "//div[10]/div")
    _details_first_product_HD_standard_field = (By.XPATH, '//div[5]/div')
    _details_first_product_hz_field = (By.XPATH, "//div[7]/div")
    _first_product_add_to_basket_button = (By.XPATH, "//div[2]/div[2]/div/div/div/a")
    _product_added_to_basket_field = (By.XPATH, "//header/strong")
    _product_added_to_basket_product_name_field = (By.XPATH, "//h4")
    _product_added_to_basket_price_field = (By.XPATH, "//section[2]/section/section/article/div")
    _product_added_to_basket_summary_price_field = (By.XPATH, "//section[3]/span[2]")
    _go_to_basket_button = (By.XPATH, "//div/a/span")
    _product_in_basket_product_name_field = (By.XPATH, "//h3")
    _product_in_basket_price_field = (By.XPATH, "//td[3]")
    _product_in_basket_summary_price_field = (By.XPATH, "//td[2]")
    _remove_first_product_from_basket_button = (By.XPATH, "//td[6]/a")
    _basket_empty_text_field = (By.XPATH, "//main/div[2]")
    _go_back_to_shopping_button = (By.XPATH, "//p/a")

    def __init__(self, driver):
        super(CategoryPage, self).__init__(driver, self._title)

    def sort_by_price_ascending(self):
        self.click(self._sort_dropdown)
        self.click(self._sort_price_ascending_option)

    def sort_by_price_descending(self):
        self.click(self._sort_dropdown)
        self.click(self._sort_price_descending_option)

    def text_price_first_product(self):
        return self.get_text(self._first_product_price_field)[:-3]

    def text_price_second_product(self):
        return self.get_text(self._second_product_price_field)[:-3]

    def filter_price(self):
        self.click(self. _filter_price_menu)
        self.clear_field_and_send_keys(self._filter_price_first_value, self._filter_price_first_field)
        self.clear_field_and_send_keys(self._filter_price_second_value, self._filter_price_second_field)
        self.click(self._filter_submit)

    def filter_producer(self):
        self.click(self._filter_producer_menu)
        self._producer_text = self.get_text(self._filter_producer_random_producer_field)
        self.click(self._filter_producer_random_producer_checkbox)
        self.click(self._filter_submit)

    def text_name_first_product(self):
        return self.get_text(self._first_product_name_field)

    def text_name_second_product(self):
        return self.get_text(self._second_product_name_field)

    def filter_TV_screen_size(self):
        self.get_driver().execute_script("window.scrollTo(0, 0);")
        self.click(self._filter_TV_screen_size_menu)
        self.get_driver().execute_script("window.scrollTo(0, 0);")
        self.click(self._filter_TV_screen_size_from_dropdown)
        self._screen_size_from_text = self.get_text(self._filter_TV_screen_size_from_option)
        self.click(self._filter_TV_screen_size_from_option)
        self.get_driver().execute_script("window.scrollTo(0, 0);")
        self.click(self._filter_TV_screen_size_to_dropdown)
        self.click(self._filter_TV_screen_size_to_option)
        self._screen_size_to_text = self.get_text(self._filter_TV_screen_size_to_dropdown)
        self.click(self._filter_submit)

    def text_screen_size_first_product(self):
        return self.get_text(self._first_product_screen_size_field)

    def filter_TV_hz(self):
        self.get_driver().execute_script("window.scrollTo(0, 0);")
        self.click(self._filter_TV_hz_menu)
        self.click(self._filter_TV_hz_from_dropdown)
        self._hz_from_text = self.get_text(self._filter_TV_hz_from_option)
        self.click(self._filter_TV_hz_from_option)
        self.click(self._filter_TV_hz_to_dropdown)
        self.click(self._filter_TV_hz_to_option)
        self._hz_to_text = self.get_text(self._filter_TV_hz_to_dropdown)
        self.click(self._filter_submit)

    def open_first_product(self):
        self.get_driver().execute_script("window.scrollTo(0, 0);")
        self.click(self._first_product_name_field)

    def text_hz_first_product(self):
        return self.get_text(self._details_first_product_hz_field)

    def sort_alphabetically_ascending(self):
        self.click(self._sort_dropdown)
        self.click(self._sort_alphabetically_ascending_option)

    def sort_alphabetically_descending(self):
        self.click(self._sort_dropdown)
        self.click(self._sort_alphabetically_descending_option)

    def get_product_name_table(self):
        self.product_name_table = []
        self.product_name_table.append(self.text_name_first_product())
        self.product_name_table.append(self.text_name_second_product())

    def get_first_product_to_compare(self):
        self.get_driver().execute_script("window.scrollTo(0, 0);")
        self.click(self._compare_first_product_checkbox)

    def compare_continue_shopping(self):
        self.click(self._compare_continue_shopping_button)

    def get_second_product_to_compare(self):
        self.get_driver().execute_script("window.scrollTo(0, 0);")
        self.click(self._compare_second_product_checkbox)

    def get_third_product_to_compare(self):
        self.get_driver().execute_script("window.scrollTo(0, 0);")
        self.click(self._compare_third_product_checkbox)

    def get_fourth_product_to_compare(self):
        self.get_driver().execute_script("window.scrollTo(0, 0);")
        self.click(self._compare_fourth_product_checkbox)

    def compare_submit(self):
        self.click(self._compare_submit_button)

    def text_name_and_price_four_first_products(self):
        self.first_product_name = self.get_text(self._first_product_name_field)
        self.second_product_name = self.get_text(self._second_product_name_field)
        self.third_product_name = self.get_text(self._third_product_name_field)
        self.fourth_product_name = self.get_text(self._fourth_product_name_field)
        self.first_product_price = self.get_text(self._first_product_price_field)
        self.second_product_price = self.get_text(self._second_product_price_field)
        self.third_product_price = self.get_text(self._third_product_price_field)
        self.fourth_product_price = self.get_text(self._fourth_product_price_field)

    def text_compared_products_name_and_price(self):
        self.compare_first_product_name = self.get_text(self._compare_first_product_name_field)
        self.compare_second_product_name = self.get_text(self._compare_second_product_name_field)
        self.compare_third_product_name = self.get_text(self._compare_third_product_name_field)
        self.compare_fourth_product_name = self.get_text(self._compare_fourth_product_name_field)
        self.compare_first_product_price = self.get_text(self._compare_first_product_price_field)
        self.compare_second_product_price = self.get_text(self._compare_second_product_price_field)
        self.compare_third_product_price = self.get_text(self._compare_third_product_price_field)
        self.compare_fourth_product_price = self.get_text(self._compare_fourth_product_price_field)


    def get_first_product_values(self):
        self.first_product_name = self.get_text(self._first_product_name_field)
        self.first_product_price = self.get_text(self._first_product_price_field)
        self.first_product_hdmi_number = self.get_text(self._first_product_hdmi_field)
        self.first_product_screen_size = self.get_text(self._first_product_screen_size_field)
        self.first_product_HD_standard = self.get_text(self._first_product_HD_standard_field)

    def get_first_product_values_details(self):
        self.details_first_product_name = self.get_text(self._details_first_product_name_field)
        self.details_first_product_price = self.get_text(self._details_first_product_price_field)[:-3]
        # self.details_first_product_hdmi_number = self.get_text(self._details_first_product_hdmi_field)
        # self.details_first_product_screen_size = self.get_text(self._details_first_product_screen_size_field)
        # self.details_first_product_HD_standard = self.get_text(self._details_first_product_HD_standard_field)

    def get_first_product_name_and_price(self):
        self.first_product_name = self.get_text(self._first_product_name_field)
        self.first_product_price = self.get_text(self._first_product_price_field)[:-3]

    def add_first_product_to_basket(self):
        self.get_driver().execute_script("arguments[0].click();", self.find_element(self._first_product_add_to_basket_button))
        # self.click(self._first_product_add_to_basket_button)

    def product_added_to_basket_text(self):
        self.product_added_to_basket_confirmation = self.get_text(self._product_added_to_basket_field)
        self.product_added_to_basket_product_name = self.get_text(self._product_added_to_basket_product_name_field)
        self.product_added_to_basket_price = self.get_text(self._product_added_to_basket_price_field)[:-6]
        self.product_added_to_basket_summary_price = self.get_text(self._product_added_to_basket_summary_price_field)[:-6]

    def go_to_basket(self):
        self.click(self._go_to_basket_button)

    def product_in_basket_text(self):
        self.product_in_basket_product_name = self.get_text(self._product_in_basket_product_name_field)
        self.product_in_basket_price = self.get_text(self._product_in_basket_price_field)[:-3]
        self.product_in_basket_summary_price = self.get_text(self._product_in_basket_summary_price_field)[:-3]

    def remove_first_product_from_basket(self):
        self.click(self._remove_first_product_from_basket_button)

    def go_back_to_shopping(self):
        self.click(self._go_back_to_shopping_button)