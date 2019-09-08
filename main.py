import unittest
import time
import smtplib
import time
import imaplib
import email
from googleapiclient.discovery import build
from pathlib import Path
from httplib2 import Http
from oauth2client import file, client, tools
import re
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pywinauto
from pywinauto import findwindows
from pywinauto import application
# Import pywinauto Application class
from pywinauto.application import Application
from pywinauto.application import WindowSpecification
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import urllib.request   # the lib that handles the url stuff
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support.events import AbstractEventListener

# Scopes is only reading file
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
DOMAIN_NAME = ["teamacaisoft"]
EMAIL_ADDRESS = ["nguyenngocduy9@gmail.com"]
SLACK_PASSWORD = ["Lu@escape2"]
TARGET_URL = "https://raw.githubusercontent.com/bbejeck/hadoop-algorithms/master/src/shakespeare.txt"

class ScreenshotListener(AbstractEventListener):
    def on_exception(self, exception, driver):
        screenshot_name = "exception.png"
        driver.get_screenshot_as_file(screenshot_name)
        print("Screenshot saved as '%s'" % screenshot_name)

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    # Entering data for input form with title
    def input_enter_data(self, driver, input_title, input_data):
        elm = driver.find_element_by_xpath("//*[text() = \'" + input_title + "\']//following::input")
        elm.send_keys(input_data)

    # Entering data for input form with title
    def input_following_title(self, driver, input_title, input_data):
        elm = driver.find_element_by_xpath("(//*[contains(text(), \'" + input_title + "\')]//following::input)[1]")
        elm.send_keys(input_data)

    # Check or uncheck checkbox as data
    def checkbox_choose(self, driver, checkbox_title, data):
        elm = driver.find_element_by_xpath("//*[text() = \'" + checkbox_title + "\']//following::input")
        if elm.is_selected():
            # print("is selected")
            if data == "unchecked":
                driver.execute_script("arguments[0].click();", elm)
        else:
            # print("not selected")
            if data == "checked":
                driver.execute_script("arguments[0].click();", elm)

    # Clicking button with specific title/label
    def button_click(self, driver, title):
        elm = driver.find_element_by_xpath("//*[@type='button' and contains(text(), \'" + title + "\')]")
        # elm = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@type='button' and contains(text(), \'" + title + "\')]")))
        elm.click()

    # Find title and ancestor button
    # This function will have a higher scope to cover multiple part of text,
    # and multiple different levels of tag of the page
    # by using ancestor keyword function.
    # Usage:
    # Input: Driver, title (label) of the button
    def ancestor_btn_click(self, driver, title):
        elm = driver.find_element_by_xpath("//*[contains(text(), \'" + title + "\')]//ancestor::button")
        elm.click()

    # Click to choose main section and it's child with specific name
    # This function help us to navigate to the right section [Channels, ...] then lower 1 level.
    # By this, we can easily and access the channel name or other sections and it's children.
    # This function can be reused many times.
    # Usage:
    # Input: driver, name of the father node, and name of the child node
    # Output: Access to the right channel or child node.
    def choosing_child(self, driver, father, child):
        elm = driver.find_element_by_xpath("//button[text() = \'" + father + "\']//following::span[text() = \'" + child + "\']")
        # print("//button[text() = \'" + father + "\']//following::span[text() = \'" + child + "\']")
        # elm = WebDriverWait(driver, 20).until(EC.element_to_be_clickable("//button[text() = \'" + father + "\']//following::span[text() = \'" + child + "\']"))
        elm.click()

    # TESTCASE 01: Create a new team on slack
    # Step 01: Sign up for a new account by using email
    # Step 02: Waiting and Fetching confirmation code by using Google API to read the latest email.
    #           In order to use Google API, I need to create credentials.json file to access the email address.
    # Step 03: Input confirmation code and proceed by input team name and project name
    def test_01_create_team_on_slack(self):
        driver = self.driver
        driver.get("https://slack.com/create#email")
        time.sleep(5)
        element = driver.find_element_by_xpath("//input[@id='signup_email']")
        element.send_keys("nguyenngocduy9@gmail.com")
        driver.find_element_by_id("submit_btn").click()
        time.sleep(10)


        # Waiting for confirmation code from Gmail
        data_folder = Path("readEmailPython/")
        file_to_open = data_folder / "credentials.json"

        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(file_to_open, SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('gmail', 'v1', http=creds.authorize(Http()))

        # Call the Gmail API to fetch INBOX
        results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
        messages = results.get('messages', [])
        messages = messages[0]

        if not messages:
            print("No messages found.")
        else:
            print("Message snippets:")
            msg = service.users().messages().get(userId='me', id=messages['id']).execute()
            str1 = msg['snippet']
            print(str1)
            print(re.findall('\d+', str1))
            int_a = re.findall('\d+', str1)
            int_b = int_a[-2:]
            digit_confirmation_code = int_b[0] + int_b[1]
            # digit_confirmation_code = int(digit_confirmation_code)
            # print(digit_confirmation_code)

        time.sleep(5)
        # Input confirmation code
        elm_confirm = driver.find_element_by_xpath("//*[@id='creation_card']/div[1]/div[1]/div[1]/input")
        elm_confirm.send_keys(digit_confirmation_code)
        print(digit_confirmation_code)
        time.sleep(5)

        # Create a new team name and input
        elm_team_name = driver.find_element_by_xpath("//*[@id='signup_team_name']")
        team_name = "Team" + str(random.randint(1,101))
        print(team_name)
        elm_team_name.send_keys(team_name)
        time.sleep(2)

        elm_next = driver.find_element_by_xpath("//*[text()='Next']")
        elm_next.click()
        time.sleep(5)

        # Create a new project name and input
        elm_project_name = driver.find_element_by_xpath("//*[@id='channel_name']")
        project_name = "Project" + str(random.randint(102,201))
        print(project_name)
        elm_project_name.send_keys(project_name)
        elm_next = driver.find_element_by_xpath("//*[text()='Next']")
        elm_next.click()
        time.sleep(5)

        # Bypass unnecessary information by clicking "skip for now"
        elm_next = driver.find_element_by_xpath("//*[text()='skip for now']")
        elm_next.click()
        time.sleep(5)

        # Click "See Your Channel in Slack" to proceed initiation step
        elm_next = driver.find_element_by_xpath("//*[text()='See Your Channel in Slack']")
        elm_next.click()
        time.sleep(5)

    # TESTCASE 02a: Create a private channel "simple"
    # Step 01: Sign in, input domain name, email and new password
    # Step 02: Click on "Channels" and create new "Channel"
    # Step 03: Input required information and click "Create"
    def test_02a_create_team_on_slack(self):
        self.create_team_on_slack("simple", "purpose", "invite_to", "private")

    # TESTCASE 02b: Create a private channel "advanced"
    # Step 01: Sign in, input domain name, email and new password
    # Step 02: Click on "Channels" and create new "Channel"
    # Step 03: Input required information and click "Create"
    def test_02b_create_team_on_slack(self):
        self.create_team_on_slack("advanced", "purpose", "invite_to", "private")

    # Function SignIn Slack:
    # Access website, input domain name, email, password, click Sign-in
    def sign_in_slack(self):
        driver = self.driver
        driver.maximize_window()
        wait = WebDriverWait(driver,40)

        driver.get("https://slack.com/signin")
        time.sleep(2)
        elm_domain = driver.find_element_by_xpath("//*[@id='domain']")
        elm_domain.send_keys(DOMAIN_NAME)
        time.sleep(2)
        driver.find_element_by_id("submit_team_domain").click()
        time.sleep(5)

        elm_email = driver.find_element_by_xpath("//*[@id='email']")
        elm_pass = driver.find_element_by_xpath("//*[@id='password']")
        elm_email.send_keys(EMAIL_ADDRESS)
        elm_pass.send_keys(SLACK_PASSWORD)
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='signin_btn']").click()
        time.sleep(6)
        return driver

    # Function Sign in extended:
    # Input: email, password
    # Output: Sign in page status
    def sign_in_slack_extended(self, email, password):
        driver = self.driver
        driver.maximize_window()
        wait = WebDriverWait(driver,40)

        driver.get("https://slack.com/signin")
        time.sleep(2)
        elm_domain = driver.find_element_by_xpath("//*[@id='domain']")
        elm_domain.send_keys(DOMAIN_NAME)
        time.sleep(2)
        self.ancestor_btn_click(driver, "Continue")
        time.sleep(5)

        elm_email = driver.find_element_by_xpath("//*[@id='email']")
        elm_pass = driver.find_element_by_xpath("//*[@id='password']")
        elm_email.send_keys(email)
        elm_pass.send_keys(password)
        time.sleep(2)
        self.ancestor_btn_click(driver, "Sign in")
        time.sleep(6)
        return driver

    # Create a channel with details
    # Input: name of the channel, purpose to create, invitation to someone, private or not
    # Output: new channel created
    # Tools used: WebDriverWait
    # Step 01: Sign in, input domain name, email and new password
    # Step 02: Click on "Channels" and create new "Channel"
    # Step 03: Input required information and click "Create"
    def create_team_on_slack(self, name, purpose, invite_to, isPrivate):
        driver = self.driver
        driver.maximize_window()
        wait = WebDriverWait(driver,40)

        driver.get("https://slack.com/signin")
        time.sleep(2)
        elm_domain = driver.find_element_by_xpath("//*[@id='domain']")
        elm_domain.send_keys(DOMAIN_NAME)
        time.sleep(2)
        driver.find_element_by_id("submit_team_domain").click()
        time.sleep(5)

        elm_email = driver.find_element_by_xpath("//*[@id='email']")
        elm_pass = driver.find_element_by_xpath("//*[@id='password']")
        elm_email.send_keys(EMAIL_ADDRESS)
        elm_pass.send_keys(SLACK_PASSWORD)
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='signin_btn']").click()
        time.sleep(6)

        btn_channel = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Channels']")))
        btn_channel.click()
        time.sleep(5)

        btn_create_channel = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Create Channel']")))
        btn_create_channel.click()
        time.sleep(5)

        simple_name = name + str(random.randint(1,101))
        self.input_enter_data(driver, "Name", simple_name)

        time.sleep(2)
        elm = driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div/div[1]/div[2]/div[1]/div[1]")
        purpose_name = purpose + str(random.randint(102,201))
        elm.send_keys(purpose_name)

        # self.input_enter_data(driver, "Purpose", "Purpose01")
        # self.input_enter_data(driver, "Send invites to", "")

        if isPrivate == "private":
            self.checkbox_choose(driver, "Make private", "checked")
        else:
            self.checkbox_choose(driver, "Make private", "unchecked")
        time.sleep(5)

        self.button_click(driver, "Create")
        time.sleep(10)

    # TESTCASE 03:  Into “simple” inset The Complete Works of William Shakespeare or Insert large message
    #   from https://raw.githubusercontent.com/bbejeck/hadoop-algorithms/master/src/shakespeare.txt
    #   every line as a separate slack message
    # Step 01: Sign in, input domain name, email and new password
    # Step 02: Choosing "Channels" and the existence "simple" channel by function choosing_child
    # Step 03: Find the input message field and send all lines of the book.
    def test_03_insert_large_message(self):
        # Signin Slack
        driver = self.sign_in_slack()

        # Choosing child node
        father_node_name = "Channels"
        child_node_name = "simple"
        time.sleep(5)
        self.choosing_child(driver, father_node_name, child_node_name)

        # Get input element for user to send messages
        elm = driver.find_element_by_xpath("//div[@role='textbox' and @aria-label='Message #" + child_node_name + "\' or @aria-label='Message " + child_node_name + "']")


        # Get large message from the book online
        data = urllib.request.urlopen(TARGET_URL) # it's a file like object and works just like a file
        for line in data: # files are iterable
            str_line = str(line)
            str_line = str_line[2:-3] # remove first and 2 last characters, which are break and linefeeds.
            elm.send_keys(str_line, Keys.ENTER) # Send message
        time.sleep(5)

    # TESTCASE 04:  Into “advanced” as “Code or text snippet”:
    # title: “Example title”
    # type: "Plain Text"
    # content: “snippet content snippet content”
    # comment: “firts”
    # Step 01: Sign in, input domain name, email and new password
    # Step 02: Choosing "Channels" and the existence private "advanced37" channel by function choosing_child
    # Step 03: Choose Paperclip, Create New, Code or text snippet
    # Step 04: Input required information and click "Create Snippet"
    def test_04_Add_code_text_snippet(self):
        # Signin Slack
        driver = self.sign_in_slack()

        # Choosing child node
        father_node_name = "Channels"
        child_node_name = "advanced37"
        time.sleep(3)
        self.choosing_child(driver, father_node_name, child_node_name)

        # Choosing "paperclip", "create new", "code or text snippet" items menu
        elm_paperclip = driver.find_element_by_xpath("//*[@type='paperclip']")
        elm_paperclip.click()
        elm_createnew = driver.find_element_by_xpath("//div[contains(text(),'Create new...')]")
        elm_createnew.click()
        elm_createnew = driver.find_element_by_xpath("//div[contains(text(),'Code or text snippet')]")
        elm_createnew.click()

        time.sleep(2)

        # elm_content = driver.find_element_by_xpath("//textarea")
        # driver.execute_script("arguments[0].click();", elm_content)
        # driver.execute_script("arguments[0].value = arguments[1]", elm_content, "snippet content snippet content!")

        actions = ActionChains(self.driver)
        actions.send_keys('snippet content snippet content!')
        actions.perform()

        # Find element with placeholder as "snippet.txt" and type in title field
        # elm_title = driver.find_element_by_xpath("//input[@placeholder='snippet.txt']")
        elm_title = driver.find_element_by_xpath("//*[text() = 'Title (optional)']//following::input[@placeholder='snippet.txt']")
        # elm_title = driver.find_element_by_xpath("//input[@id='snippet-name86']")
        # driver.find_element_by_id('snippet-name86').send_keys('Example title')
        elm_title.send_keys("Example title")
        time.sleep(2)

        # Find element with text as "Type" and type in type field
        elm_type = driver.find_element_by_xpath("//span[text() = 'Type']//following::input[1]")
        # elm_type.click()
        driver.execute_script("arguments[0].click();", elm_type)
        time.sleep(2)
        elm_plaintext = driver.find_element_by_xpath("//span[text() = 'Plain Text']")
        elm_plaintext.click()
        time.sleep(2)

        # Find textare element and type in content "snippet content snippet content!"
        elm_content = driver.find_element_by_xpath("//textarea")
        driver.execute_script("arguments[0].click();", elm_content)
        driver.execute_script("arguments[0].value = arguments[1]", elm_content, "snippet content snippet content!")
        # elm_content.click()
        # elm_content.send_keys("snippet content snippet content")
        time.sleep(2)

        # Find comment element and type in "firts"
        elm_comment = driver.find_element_by_xpath("//div[@role='textbox' and @aria-label='Add a message, if you’d like.']")
        elm_comment.send_keys("first")
        time.sleep(2)

        # Click button "Create Snippet" by the function button_click
        self.button_click(driver, "Create Snippet")
        time.sleep(2)

    # TESTCASE 05:  Into “advanced” upload some txt file (05.txt) with the content:
    # ---------------------
    # AAAAAAAAAAAAAAAAAAAAA
    # BBBBBBBBBBBBBBBBBBBBB
    # CCCCCCCCCCCCCCCCCCCCC
    # ---------------------
    # Step 01: Sign in, input domain name, email and new password
    # Step 02: Choosing "Channels" and the existence private "advanced37" channel by function choosing_child
    # Step 03: Choose Paperclip, and "Your Computer"
    # Step 04: Choosing file from "Explorer window" using pywinauto
    #           I connect to running window application and automate steps of choosing file from system to upload
    #           Found dialog "Edit" and input file path, then click on "Open"
    # Step 05: Click on "Upload" to upload file
    def test_05_UploadTxtFile(self):
        # Signin Slack
        driver = self.sign_in_slack()

        # Choosing child node
        father_node_name = "Channels"
        child_node_name = "advanced37"
        time.sleep(3)
        self.choosing_child(driver, father_node_name, child_node_name)
        time.sleep(3)

        elm_paperclip = driver.find_element_by_xpath("//*[@type='paperclip']")
        elm_paperclip.click()
        elm_yourcomputer = driver.find_element_by_xpath("//div[contains(text(),'Your computer')]")
        elm_yourcomputer.click()
        time.sleep(3)

        # Connect to "Window Explorer" window with title as "Open"
        app = Application().connect(title_re='Open')
        main_dlg = app.window(title_re='Open')

        # Print all controls on the dialog for searching the right control to enter path of the file
        main_dlg.print_control_identifiers()
        dialogs = app.windows()
        # print(dialogs)

        # After found dialogs is "Edit". I slowly input input information and click on "Open"
        main_dlg.Edit.type_keys("C:\\Users\\Daniel\\Desktop\\05.txt",
                        with_spaces=True,
                        with_newlines=False,
                        pause=0.2,
                        with_tabs=False)
        main_dlg.Open.click()
        time.sleep(3)

        # Find button "Upload" and click using pre-defined function
        self.button_click(driver, "Upload")
        time.sleep(3)

    # TESTCASE 06:  create a new slack user for your team “second user”
    #   (I change the name as "nguyendaniel777" in the video)
    #   Instead of the old technique in the TESTCASE 01, I used another Chrome window to get confirmation code
    # Step 01: Sign in, input domain name, email and new password
    # Step 02: Open a new Chrome browser window to get confirmation code and close this new driver
    # Step 03: Input confirmation code, team, project, and proceed to 'See Your Channel in Slack'
    def test_06_CreateNewSlackUser(self):
        # Open first web driver to input email
        driver = self.driver
        driver.get("https://slack.com/create#email")
        time.sleep(5)
        element = driver.find_element_by_xpath("//input[@id='signup_email']")
        element.send_keys("nguyendaniel777@gmail.com")
        driver.find_element_by_id("submit_btn").click()
        time.sleep(5)

        EMAIL_ADDRESS1 = "nguyendaniel777@gmail.com"
        # SLACK_PASSWORD1 = "------"
        driver1 = webdriver.Chrome()
        driver1.get("https://mail.google.com/mail/")
        elm_email = driver1.find_element_by_xpath("//*[@id='identifierId']")
        elm_email.send_keys(EMAIL_ADDRESS1)
        elm_button = driver1.find_element_by_xpath("//span[text() ='Dalej']")
        driver1.execute_script("arguments[0].click();", elm_button)
        time.sleep(5)

        elm_password = driver1.find_element_by_xpath("//*[@name='password']")
        elm_password.send_keys("M1nhbien@")
        # Finding the elment below is not optimize. Because it will fail for log in Gmail in another language
        # Need to improving codind here
        elm_button = driver1.find_element_by_xpath("//span[text() ='Dalej']")
        driver1.execute_script("arguments[0].click();", elm_button)
        time.sleep(10)

        # Choosing first email which includes confirmation code
        elm_email           = driver1.find_element_by_xpath("(//*//span[contains(text(), 'Slack confirmation code:')])[1]//ancestor::tr").click()
        time.sleep(3)

        # Choose email header and get confirmation code
        elm_email_header    = driver1.find_element_by_xpath("//*//h2[@class='hP']")
        str_text = elm_email_header.text
        print(str_text)
        int_a = re.findall('\d+', str_text)
        int_b = int_a[-2:]
        digit_confirmation_code = int_b[0] + int_b[1]
        print(digit_confirmation_code)
        time.sleep(2)
        driver1.close()

        # Input confirmation code for the first web driver
        elm_confirm = driver.find_element_by_xpath("//*[@id='creation_card']/div[1]/div[1]/div[1]/input")
        elm_confirm.send_keys(digit_confirmation_code)
        time.sleep(5)

        # Create new team for second user
        elm_team_name = driver.find_element_by_xpath("//*[@id='signup_team_name']")
        team_name = "Team" + str(random.randint(1,101))
        elm_team_name.send_keys(team_name)
        time.sleep(2)

        # self.button_click(driver, "Next")
        elm_next = driver.find_element_by_xpath("//*[text()='Next']")
        elm_next.click()
        time.sleep(5)

        # Create new project for second user
        elm_project_name = driver.find_element_by_xpath("//*[@id='channel_name']")
        project_name = "Project" + str(random.randint(102,201))
        elm_project_name.send_keys(project_name)
        # self.button_click(driver, "Next")
        elm_next = driver.find_element_by_xpath("//*[text()='Next']")
        elm_next.click()
        time.sleep(5)

        # Skip "Who else is working on this project?"
        # self.button_click(driver, "skip for now")
        elm_next = driver.find_element_by_xpath("//*[text()='skip for now']")
        elm_next.click()
        time.sleep(5)

        elm_next = driver.find_element_by_xpath("//*[text()='See Your Channel in Slack']")
        elm_next.click()
        # self.button_click(driver, "See Your Channel in Slack")
        time.sleep(5)

    # TESTCASE 07:  Add a "second user" to “simple” channel
    #   (I change the name as "tranvanba777" in the video)
    # Step 01: Sign in, input domain name, email and new password
    # Step 02: Open a new Chrome browser window to get confirmation code and close this new driver
    # Step 03: Input confirmation code, team, project, and proceed to 'See Your Channel in Slack'
    def test_07_AddSecondUserToSimpleChannel(self):
        # Signin Slack
        driver = self.sign_in_slack()

        # Choosing child node
        father_node_name = "Channels"
        child_node_name = "simple"
        time.sleep(3)
        self.choosing_child(driver, father_node_name, child_node_name)
        time.sleep(3)

        # elm_channel_info = driver.find_element_by_xpath("//i[@type='info-circle']")
        elm_channel_info = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//i[@type='info-circle']")))
        elm_channel_info.click()

        elm_channel_info = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//i[@type='info-circle']")))
        # Click on button with pre-defined ancestor_btn_click function
        self.ancestor_btn_click(driver, "Member")
        time.sleep(2)
        self.ancestor_btn_click(driver, "Add People")
        time.sleep(2)
        self.ancestor_btn_click(driver, "Continue")
        time.sleep(2)
        self.ancestor_btn_click(driver, "Invite people to")
        time.sleep(2)

        # elm_channel_button = driver.find_element_by_xpath("//span[contains(text(), 'Member')]//ancestor::button").click()
        # self.button_click(driver, "Add People")
        # self.button_click(driver, "Invite people to")

        # Input email address of the user and send invitation
        self.input_following_title(driver, "Email Address", "tranvanba777@gmail.com")
        time.sleep(2)
        self.ancestor_btn_click(driver, "Send Invitations")
        time.sleep(2)
        self.ancestor_btn_click(driver, "Done")
        time.sleep(5)

    # TESTCASE 08:  Log in as the second user and check that The Complete Works of William Shakespeare is added
    # Step 01: Sign in the second user (tranvanba777), input domain name, email and new password
    # Step 02: Choosing Channels section and private channel "simple"
    # Step 03: Scroll up to the header of the chat pane. By this webdriver can see all possible messages
    # Step 04: Scrape all possible messages in the chat pane
    # Step 05: Get the book "The Complete Works of William Shakespeare"
    #         Normally I get full book, but in order to speed up running, I only send 35 lines of the book.
    #         So I get only first part of the book, which I sent by the first user in the previous test case
    #         Number of lines of the book, which I sent is 35.
    # Step 06: Using set function to remove duplicate lines in messages list and book_lines list.
    # Step 07: Compare the book (with 35 first lines) with all messages received from chat pane.
    #     If percentage of book_lines over messages is over 90 percent.
    #       Then "The Complete Works of William Shakespeare" is added.
    def test_08_LoginAsSecondUserToCheckText(self):
        # Signin Slack
        str_email = "tranvanba777@gmail.com"
        str_password = "M1nhbien@"
        driver = self.sign_in_slack_extended(str_email, str_password)

        # Choosing child node
        str_father_node_name = "Channels"
        str_child_node_name = "simple"
        time.sleep(3)
        self.choosing_child(driver, str_father_node_name, str_child_node_name)
        time.sleep(7)

        # Scroll up
        # Iterate the list of web elements which contains messages in the chat pane
        # By this we scroll to the top of the pane and make visible to all chat messages
        # for further scraping messages
        recentList = driver.find_elements_by_xpath("(//div[@role='presentation' and @class='c-scrollbar__child'])[2]")
        for list in recentList:
            # print(list)
            driver.execute_script("arguments[0].scrollIntoView();", list)
        time.sleep(3)

        # Get all messages from the visible view
        list_messages = []
        message_elements = driver.find_elements_by_xpath("//span[@class='c-message__body']")
        for msg in message_elements:
            line = msg.text
            list_messages.append(line)
        # print("Messages received:", list_messages)
        print("Full of messages received length:", len(list_messages))

        # Get the book "The Complete Works of William Shakespeare"
        # Normally I get full book, but for this test case I get only first part of the book,
        # which I sent by the first user in the previous test case
        # Number of lines of the book, which I sent is 35
        list_book = []
        data = urllib.request.urlopen(TARGET_URL) # it's a file like object and works just like a file
        for i, line in enumerate(data): # files are iterable
            str_line = str(line)
            str_line = str_line[2:-3] # Trimming first and 2 last charactesr of the line
            list_book.append(str_line)
            if i > 36:
                break
        print("Full book:", list_book)
        print("Full book length:", len(list_book))
        data.close()

        # Use set fucntion to remove duplicate lines in the receives messages and book
        # For example: \n line
        size_messages = len(set(list_messages))
        size_book = len(set(list_book))
        print("Size in set of the messages:", size_messages)
        print("size in set of the book:", size_book)

        # Check intersection of the lines in book and lines in messages
        set_intersection = set(list_messages) & set(list_book)
        size_intersection = len(set_intersection)
        print("Length of set intersection between messages and the book: ", size_intersection)
        percentage_of_lines_sent = 100 * float(size_intersection) / float(size_book)
        print("Percentage of lines were sent: ", percentage_of_lines_sent)
        # "The Complete Works of William Shakespeare is added" with percentage of over 90 percent
        assert(percentage_of_lines_sent > 90)

        time.sleep(5)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()

