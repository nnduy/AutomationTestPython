from selenium.webdriver.common.by import By


class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    GO_BUTTON = (By.ID, 'submit')
    PAPERCLIP_BUTTON = (By.XPATH, "//*[@type='paperclip']")
    YOURCOMPUTER_BUTTON = (By.XPATH, "//div[contains(text(),'Your computer')]")
    SCROLL_LIST = (By.XPATH, "(//div[@role='presentation' and @class='c-scrollbar__child'])[2]")
    MESSAGES_LIST = (By.XPATH, "//span[@class='c-message__body']")


class SearchResultsPageLocators(object):
    """A class for search results locators. All search results locators should come here"""
    pass
