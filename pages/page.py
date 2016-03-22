from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

class Page(object):
    def __init__(self, driver, title=None, url=None):
        self._driver = driver
        self._title = title
        self._url = url
        if self._url:
            self.get(url)
        # if self._title:
        #     self.is_the_current_page()

    def is_the_current_page(self):
        if self._title:
            WebDriverWait(self.get_driver(), 10).until(lambda s: self.get_driver().title)

        if self._title[len(self._title)-1] == ".":
            self._title = self._title[0:len(self._title)-1]
        # Assert.equal(self.get_driver().title, self._title,
        #             "Expected page title: %s. Actual page title: %s" % (self._title, self.get_driver().title))
        return True

    def wait_for_visibility(self, locator, timeout=10):
        return WebDriverWait(self.get_driver(), timeout).until(
            expected_conditions.visibility_of_element_located(locator)
        )

    def hit_enter(self, element):
        element.send_keys(Keys.RETURN)
        return self

    def find_element(self, locator):
        return self.get_driver().find_element(*locator)

    def send_keys(self, value_to_send, locator):
        self.find_element(locator).send_keys(value_to_send)
        return self

    def send_keys_to_element(self, element, value_to_send):
        element.send_keys(value_to_send)
        return self

    def clear_field_and_send_keys(self, value_to_send, locator):
        self.clear_field(locator)
        self.send_keys(value_to_send, locator)

    def clear_field(self, locator):
        self.find_element(locator).clear()

    def click(self, locator):
        element = self.wait_for_visibility(locator)
        # self.find_element(locator).click()
        # ycoord = element.location['y']
        # self.get_driver().execute_script("window.scrollTo(0, {0})".format(ycoord))
        # wait = WebDriverWait(self.get_driver(), 10, poll_frequency=.2)
        # wait.until(expected_conditions.element_to_be_clickable(locator))
        element.click()

    def click1(self, locator):
        ycoord = self.find_element(locator).location['y']
        self.get_driver().execute_script("window.scrollTo({0}, 0)".format(ycoord))
        wait = WebDriverWait(self.get_driver(), 10, poll_frequency=.2)
        wait.until(expected_conditions.element_to_be_clickable(locator)).click()

    def select_value_from_dropdown(self, value, locator):
        dropdown = Select(self.find_element(locator))
        dropdown.select_by_value(value)

    def select_value_from_dropdown_element(self, value, element):
        dropdown = Select(element)
        dropdown.select_by_value(value)

    def select_index_from_dropdown(self, index, locator):
        dropdown = Select(self.find_element(locator))
        dropdown.select_by_index(index)

    def select_text_from_dropdown(self, text, locator):
        dropdown = Select(self.find_element(locator))
        dropdown.select_by_visible_text(text)

    def accept_alert(self):
        return self.get_driver().switch_to_alert().accept()

    def refresh(self):
        self.get_driver().refresh()

    def get_page_title(self):
        return self.get_driver().title

    def get_text(self, locator):
        return self.find_element(locator).text

    def get_page_source(self):
        return self.get_driver().page_source

    def get_driver(self):
        return self._driver

    def get(self, url):
        return self.get_driver().get(url)

    def quit(self):
        self.get_driver().quit()

    def check(self, locator):
        if not self.wait_for_visibility(locator).is_selected():
            self.click(locator)

    def uncheck(self, locator):
        if self.wait_for_visibility(locator).is_selected():
            self.click(locator)

    def get_value(self, locator):
        return self.wait_for_visibility(locator).get_attribute("value")