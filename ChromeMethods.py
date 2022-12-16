import os
import logging
from time import sleep
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver
from robot.api.deco import keyword


def match_by(stype):
    match stype:
        case 'XPATH':
            return By.XPATH
        case 'CSS_SELECTOR':
            return By.CSS_SELECTOR
        case 'PARTIAL_LINK_TEXT':
            return By.PARTIAL_LINK_TEXT
        case 'ID':
            return By.ID
        case 'LINK_TEXT':
            return By.LINK_TEXT
        case _:
            return


class ChromeMethods:
    def __init__(self):
        self.driver = webdriver.Chrome()
        super(ChromeMethods, self).__init__()

    @keyword('START CHROME BROWSER')
    def start_gchrome(self, url):
        """
        Start chrome in specific url
        :param url: The url
        :return: None
        """
        logging.info("Start google chrome browser")
        self.driver.maximize_window()
        self.driver.implicitly_wait(4)
        self.driver.get(url)

    @keyword("QUIT CHROME")
    def quit_chrome(self):
        logging.info("Exit google chrome.")
        self.driver.quit()

    @keyword("TAP ON ELEMENT BY")
    def tap_element(self, by_type, identifier):
        """
        Tap to a specific location given by identifier
        :param by_type: type of the search, could be any variant of By
        eg: XPATH, CSS_SELECTOR, PARTIAL_LINK_TEXT, ID, etc.
        :param identifier: element identifier
        :return: True if tap performed, false otherwise
        """
        try:
            by = match_by(by_type)
            element = self.driver.find_element(by, identifier)
            logging.info("Element = {}".format(element))
            if element:
                if not self.check_element_displayed_on_visible_screen(by_type, identifier):
                    logging.info("Scrolling to element")
                    self.scroll_to_element_using(by_type, identifier)
                element.click()
                return True
            logging.info("Element was not clicked")
            return False
        except Exception as message:
            return message

    @keyword('CHECK ELEMENT DISPLAYED ON VISIBLE SCREEN')
    def check_element_displayed_on_visible_screen(self, by_type, identifier):
        """
        Check if an element is displayed on the visible screen
        Used to check if elements are on visual field
        :param by_type: type of the search, could be any variant of By
        eg: XPATH, CSS_SELECTOR, PARTIAL_LINK_TEXT, ID, etc.
        :param identifier: element identifier
        :return: True if element is on the visible screen, false otherwise
        """
        try:
            by = match_by(by_type)
            element = self.driver.find_element(by, identifier)
            logging.info("Check if element is displayed on visual field")

            win_upper_bound = self.driver.execute_script('return window.pageYOffset')
            win_left_bound = self.driver.execute_script('return window.pageXOffset')
            win_width = self.driver.execute_script('return document.documentElement.clientWidth')
            win_height = self.driver.execute_script('return document.documentElement.clientHeight')

            logging.info("elem.location = {}".format(element.location))
            logging.info("win_upper_bound = {}".format(win_upper_bound))
            logging.info("win_left_bound = {}".format(win_left_bound))
            logging.info("win_width = {}".format(win_width))
            logging.info("win_height = {}".format(win_height))

            if win_upper_bound <= element.location["y"]:
                if win_upper_bound + win_height >= element.location["y"]:
                    logging.info("Element is ON visual field")
                    return True
                else:
                    logging.info("Element is NOT on visual field")
                    return False
            else:
                if win_upper_bound - win_height >= element.location["y"]:
                    logging.info("Element is ON visual field")
                else:
                    logging.info("Element is NOT on visual field")
                    return False
        except Exception as message:
            return message

    @keyword('SCROLL TO ELEMENT USING')
    def scroll_to_element_using(self, by_type, identifier):
        """
        Goal: Scroll to a specified element and performed the action
        :param by_type: type of the search, could be any variant of By
        eg: XPATH, CSS_SELECTOR, PARTIAL_LINK_TEXT, ID, etc.
        :param identifier: element identifier
        :return: True if action is performed, false otherwise
        """
        try:
            by = match_by(by_type)
            element = self.driver.find_element(by, identifier)
            y = element.location['y']
            logging.info("VAR = {}".format(y))
            self.driver.execute_script("window.scrollTo(0, {})".format(y * 0.90))
            logging.info("Scroll to y = {}".format(y * 0.90))
            sleep(0.8)
            return True
        except Exception as message:
            return message

    @keyword('GO BACK PAGE')
    def go_back_page(self):
        """
        Go back to the previous page
        :return: None
        """
        self.driver.back()
        sleep(1)

    @keyword('RETRIEVE TEXT USING')
    def retrieve_text_using(self, by_type, identifier, attr=None):
        """
        Retrieve the text located at a specific location
        :param by_type: type of the search, could be any variant of By
        eg: XPATH, CSS_SELECTOR, PARTIAL_LINK_TEXT, ID, etc.
        :param identifier: the location from where to retrieve the text from attribute
        :param attr: the attribute from which the withdrawal is made
        Could be None or other attribute
        :return: Text retrieved from xpath location
        """
        try:
            by = match_by(by_type)
            if attr is None:
                text = self.driver.find_element(by, identifier).text
                logging.info("Text retrieved = {}".format(text))
                return text
            else:
                text = self.driver.find_element(by, identifier).get_attribute(attr)
                logging.info("Text retrieved based on attr = {}".format(text))
                return text
        except Exception as message:
            return message
