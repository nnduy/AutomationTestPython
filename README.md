# Automation testing for web telecommunication application.

## Languages and Tools
Python 
Selenium

## Test case list:
1.	Create a new account on slack
1.	Create private channel “Channels”
1.	Insert large message to that private channel
1.	Using “Code or text snippet” with full detail information
1.	Upload some txt file with a certain content: "example content"
1.	Create another slack user for your team "tranvanba"
1.	Add that user to “Channels” channel
1.	Log in new user and check the previous long message sent

## Screenshot Videos
https://drive.google.com/open?id=1uY2VFR56Jzf9ZEFmjl38XkZpIcO-PTDM

## Overview of the tasks

| Num | Test cases                                                                                                                                                                                             | Steps                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Technologies or tools used                                                                                   |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| 1   | Create a team on slack                                                                                                                                                                                 | Step 01: Sign up for a new account by using email<br>Step 02: Waiting and Fetching confirmation code by using Google API to read the latest email.<br>In order to use Google API, I need to create credentials.json file to access the email address.<br>Step 03: Input confirmation code and proceed by input team name and project name                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Google API                                                                                                   |
| 2   | Create two private channels “simple”, “advanced”                                                                                                                                                       | Step 01: Sign in, input domain name, email and new password<br>Step 02: Click on "Channels" and create new "Channel"<br>Step 03: Input required information and click "Create"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | WebDriverWait<br>Generalize input name and input data function.                                              |
| 3   | Into “simple” inset The Complete Works of William Shakespeare<br>from https://raw.githubusercontent.com/bbejeck/hadoop-algorithms/master/src/shakespeare.txt<br>every line as a separate slack message | Step 01: Sign in, input domain name, email and new password<br>Step 02: Choosing "Channels" and the existence "simple" channel by function choosing\_child<br>Step 03: Find the input message field and send all lines of the book.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Generalize choosing channels section and channel name function.<br>Get large messages and send line by line. |
| 4   | Into “advanced” as “Code or text snippet”:<br>title: “Example title”<br>type: “Plain Text”<br>content: “snippet content snippet content”<br>comment: “firts”                                           | Step 01: Sign in, input domain name, email and new password<br>Step 02: Choosing "Channels" and the existence private "advanced37" channel by function choosing\_child<br>Step 03: Choose Paperclip, Create New, Code or text snippet<br>Step 04: Input required information and click "Create Snippet"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | driver.execute\_script                                                                                       |
| 5   | Into “advanced” upload some txt file with the content:<br>\---------------------<br>AAAAAAAAAAAAAAAAAAAAA<br>BBBBBBBBBBBBBBBBBBBBB<br>CCCCCCCCCCCCCCCCCCCCC<br>\---------------------                  | Step 01: Sign in, input domain name, email and new password<br>Step 02: Choosing "Channels" and the existence private "advanced37" channel by function choosing\_child<br>Step 03: Choose Paperclip, and "Your Computer"<br>Step 04: Choosing file from "Explorer window" using pywinauto<br>I connect to running window application and automate steps of choosing file from system to upload<br>Found dialog "Edit" and input file path, then click on "Open"<br>Step 05: Click on "Upload" to upload file                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Pywinauto to automate interaction with applications on Windows System.                                       |
| 6   | Create a new slack user for your team “second user”                                                                                                                                                    | Step 01: Sign in, input domain name, email and new password<br>Step 02: Open a new Chrome browser window to get confirmation code and close this new driver<br>Step 03: Input confirmation code, team, project, and proceed to 'See Your Channel in Slack'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Using multiple Chorme drivers.<br>Gmail reading.                                                             |
| 7   | Add a second user to “simple” channel                                                                                                                                                                  | Step 01: Sign in, input domain name, email and new password<br>Step 02: Open a new Chrome browser window to get confirmation code and close this new driver<br>Step 03: Input confirmation code, team, project, and proceed to 'See Your Channel in Slack'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Generalize button click by searching ancestor elements.                                                      |
| 8   | Log in as the second user and check that The Complete Works of William Shakespeare is added                                                                                                            | Step 01: Sign in the second user (tranvanba777), input domain name, email and new password<br>Step 02: Choosing Channels section and private channel "simple"<br>Step 03: Scroll up to the header of the chat pane. By this webdriver can see all possible messages<br>Step 04: Scrape all possible messages in the chat pane<br>Step 05: Get the book "The Complete Works of William Shakespeare"<br>Normally I get full book, but in order to speed up running, I only send 35 lines of the book.<br>So I get only first part of the book, which I sent by the first user in the previous test case<br>Number of lines of the book, which I sent is 35.<br>Step 06: Using set function to remove duplicate lines in messages list and book\_lines list.<br>Step 07: Compare the book (with 35 first lines) with all messages received from chat pane.<br>If percentage of book\_lines over messages is over 90 percent.<br>Then "The Complete Works of William Shakespeare" is added. | Scrolling up and get all messages from chating pane.<br>Compare intersection two lists.                      |                      |

## Techniques used:
1. Google API
1. Selenium Explicit waits (WebDriverWait)
1. driver.execute_script
1. Pywinauto to automate interaction with applications on Windows System.
1. Using multiple webdriver and multiple Chorme drivers.
1. Scrolling
1. Page Objects
1. PyUnit for Selenium Python Test Suite
1. pytest
1. Slack API: Webhook, Slack App, bot
1. Jenkins

## Future Improvements
1. Robot Framework
1. JMeter
