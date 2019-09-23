from Version02.element import BasePageElement
from Version02.locators import MainPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import urllib.request  # the lib that handles the url stuff
import requests
from oauth2client import file, client, tools
from httplib2 import Http
from googleapiclient.discovery import build
import re
import random

# Scopes is only reading file
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class SearchTextElement(BasePageElement):
    """This class gets the search text from the specified locator"""

    # The locator for search box where search string is entered
    locator = 'q'


class SignInDomainTextElement(BasePageElement):
    # The locator for domain box where search string is entered
    locator = 'domain'


class InputEmail(BasePageElement):
    # The locator for email box where search string is entered
    locator = 'email'


class InputPassword(BasePageElement):
    # The locator for password box where search string is entered
    locator = 'password'


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver


class MainPage(BasePage):
    """Home page action methods come here. I.e. Python.org"""

    # Declares a variable that will contain the retrieved text
    search_text_element = SearchTextElement()

    signin_domain_text_element = SignInDomainTextElement()

    input_email_text_element = InputEmail()
    input_password_text_element = InputPassword()

    def is_title_matches(self):
        """Verifies that the hardcoded text "Python" appears in page title"""
        return "Python" in self.driver.title

    def click_go_button(self):
        """Triggers the search"""
        element = self.driver.find_element(*MainPageLocators.GO_BUTTON)
        element.click()

    def click_paperclip_button(self):
        element = self.driver.find_element(*MainPageLocators.PAPERCLIP_BUTTON)
        element.click()

    def click_yourcomputer_button(self):
        element = self.driver.find_element(*MainPageLocators.YOURCOMPUTER_BUTTON)
        element.click()

    def click_submit_button(self):
        element = self.driver.find_element(*MainPageLocators.SUBMIT_BUTTON)
        element.click()

    def click_next_button(self):
        element = self.driver.find_element(*MainPageLocators.NEXT_BUTTON)
        element.click()


    def get_elements_scroll_list(self):
        element = self.driver.find_elements(*MainPageLocators.SCROLL_LIST)
        return element

    def get_elements_messages_list(self):
        elm = self.driver.find_elements(*MainPageLocators.MESSAGES_LIST)
        # elm = WebDriverWait(self.driver,5).until(EC.presence_of_all_elements_located(*MainPageLocators.MESSAGES_LIST))
        # elm = WebDriverWait(self.driver,5).until(EC.presence_of_element_located(*MainPageLocators.MESSAGES_LIST))
        return elm

    def get_elements_scroll_list(self):
        element = self.driver.find_elements(*MainPageLocators.SCROLL_LIST)
        return element

    # Clicking descendant button with specific title/label/text
    def text_descend_button_click(self, text):
        elm = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button//descendant::*[contains(text(), \'" + text + "\')]")))
        # elm = self.driver.find_element_by_xpath("//button//descendant::*[contains(text(), \'" + title + "\')]")
        elm.click()

    # Clicking ancestor button with specific title/label/text
    def text_ancestor_button_click(self, text):
        elm = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), \'" + text + "\')]/ancestor::button")))
        elm.click()

    # Clicking button with specific title/label/text
    def text_button_click(self, text):
        elm = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), \'" + text + "\')]")))
        elm.click()

    def choosing_child(self, father, child):
        elm = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//button[text() = \'" + father + "\']//following::span[text() = \'" + child + "\']")))
        elm.click()

    def register_team(self, email):
        elm = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//input[@id='signup_email']")))
        elm.send_keys(email)

    def getting_confimration_code(self, data_folder, file_to_open):
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(file_to_open, SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('gmail', 'v1', http=creds.authorize(Http()))

        # Call the Gmail API to fetch INBOX
        results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
        messages = results.get('messages', [])
        messages = messages[0]

        if not messages:
            print("No messages found.")
        else:
            print("Message snippets:")
            msg = service.users().messages().get(userId='me', id=messages['id']).execute()
            # print('msg:', msg)
            str1 = msg['snippet']
            # print(str1)
            print(re.findall('\d+', str1))
            int_a = re.findall('\d+', str1)
            int_b = int_a[-2:]
            digit_confirmation_code = int_b[0] + int_b[1]
            # digit_confirmation_code = int(digit_confirmation_code)
            print("digit_confirmation_code:", digit_confirmation_code)
        return digit_confirmation_code

    def send_confirm_code(self, text, code):
        elm = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), \'" + text + "\')]/ancestor::form/descendant::input[1]")))
        elm.send_keys(code)

    def create_new_team(self):
        # Create a new team name and input
        elm = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='signup_team_name']")))
        team_name = "Team" + str(random.randint(1, 101))
        print(team_name)
        elm.send_keys(team_name)
        self.click_next_button()

    def create_new_project(self):
        # Create a new project name and input
        elm = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='channel_name']")))
        project_name = "Project" + str(random.randint(102, 201))
        print(project_name)
        elm.send_keys(project_name)
        self.click_next_button()

    # Sending only one line to webhook
    def send_one_line_message(self, webhook, line):
        response = requests.post(
            webhook, json={"text": line},
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )

    # Sending multiple lines to webhook
    def send_multiple_line_message(self, target_url, webhook):
        # Get large message from the book online
        data = urllib.request.urlopen(target_url)  # it's a file like object and works just like a file
        for i, line in enumerate(data):  # files are iterable
            str_line = str(line)
            str_line = str_line[2:-3]  # remove first and 2 last characters, which are break and linefeeds.
            if line.strip():
                self.send_one_line_message(webhook, str_line)
            if i > 36:
                break

class SearchResultsPage(BasePage):
    """Search results page action methods come here"""

    def is_results_found(self):
        # Probably should search for this text in the specific page
        # element, but as for now it works fine
        return "No results found." not in self.driver.page_source
