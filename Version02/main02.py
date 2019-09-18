from pywinauto.application import Application
import unittest
import time
from selenium import webdriver
from Version02 import page
import urllib.request  # the lib that handles the url stuff

DOMAIN_NAME = ["teamacaisoft"]
EMAIL_ADDRESS = ["nguyenngocduy9@gmail.com"]
SLACK_PASSWORD = ["Lu@escape2"]

# Second user
SECOND_USER_EMAIL_ADDRESS = "tranvanba777@gmail.com"
SECOND_USER_PASSWORD = "M1nhbien@"

TARGET_URL = "https://raw.githubusercontent.com/bbejeck/hadoop-algorithms/master/src/shakespeare.txt"


class SlackQA(unittest.TestCase):
    """A sample test class to show how page object works"""

    @classmethod
    def setUpClass(class_SlackQA):
        print("setUpClass executed")

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://slack.com/signin")
        self.driver.maximize_window()

    # Function SignIn Slack:
    # Access website, input domain name, email, password, click Sign-in
    def sign_in_slack(self, domain, email, password):
        # Load the main page. In this case the home page of Slack Sign in.
        main_page = page.MainPage(self.driver)

        main_page.signin_domain_text_element = domain
        main_page.text_descend_button_click("Continue")

        main_page.input_email_text_element = email
        main_page.input_password_text_element = password
        main_page.text_descend_button_click("Sign in")
        return main_page

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
        main_page = self.sign_in_slack(DOMAIN_NAME, EMAIL_ADDRESS, SLACK_PASSWORD)

        # Choosing child node
        father_node_name = "Channels"
        child_node_name = "advanced37"
        main_page.choosing_child(father_node_name, child_node_name)

        main_page.click_paperclip_button()
        main_page.click_yourcomputer_button()

        # Connect to "Window Explorer" window with title as "Open"
        time.sleep(5)
        app = Application().connect(title_re='Open')
        main_dlg = app.window(title_re='Open')

        # Print all controls on the dialog for searching the right control to enter path of the file
        # main_dlg.print_control_identifiers()
        # dialogs = app.windows()
        # print(dialogs)

        # After found dialogs is "Edit". I slowly input input information and click on "Open"
        main_dlg.Edit.type_keys("C:\\Users\\Daniel\\Desktop\\05.txt",
                                with_spaces=True,
                                with_newlines=False,
                                pause=0.1,
                                with_tabs=False)
        main_dlg.Open.click()

        # Find button "Upload" and click using pre-defined function
        main_page.text_button_click("Upload")

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
        # Signin Slack as second user
        main_page = self.sign_in_slack(DOMAIN_NAME, SECOND_USER_EMAIL_ADDRESS, SECOND_USER_PASSWORD)

        # Choosing child node
        str_father_node_name = "Channels"
        str_child_node_name = "simple"
        main_page.choosing_child(str_father_node_name, str_child_node_name)

        # Scroll up
        # Iterate the list of web elements which contains messages in the chat pane
        # By this we scroll to the top of the pane and make visible to all chat messages
        # for further scraping messages
        recentList = main_page.get_elements_scroll_list()
        # recentList = driver.find_elements_by_xpath("(//div[@role='presentation' and @class='c-scrollbar__child'])[2]")
        for list in recentList:
            print(list)
            self.driver.execute_script("arguments[0].scrollIntoView();", list)

        # Get all messages from the visible view
        list_messages = []
        # message_elements = self.driver.find_elements_by_xpath("//span[@class='c-message__body']")
        message_elements = main_page.get_elements_messages_list()
        time.sleep(15)  # Waiting for retrieve all messages after scrolling up

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
        data = urllib.request.urlopen(TARGET_URL)  # it's a file like object and works just like a file
        for i, line in enumerate(data):  # files are iterable
            str_line = str(line)
            str_line = str_line[2:-3]  # Trimming first and 2 last charactesr of the line
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
        assert (percentage_of_lines_sent > 90)

    def tearDown(self):
        self.driver.close()

    @classmethod
    def tearDownClass(class_SlackQA):
        print("tearDownClass executed")


if __name__ == "__main__":
    unittest.main()
