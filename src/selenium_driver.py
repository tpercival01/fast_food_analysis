from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def open_selenium(url):
    headless_option = webdriver.FirefoxOptions()
    headless_option.add_argument("--headless")
    driver = webdriver.Firefox(options=headless_option)
    driver.get(url)
    driver.set_window_size(1920,1080)
    return driver

def close_selenium(driver):
    driver.close()
    return