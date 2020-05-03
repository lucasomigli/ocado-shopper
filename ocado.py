import os
import time
import json
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from helper import exists, set_arguments

parser = argparse.ArgumentParser()

args = set_arguments(parser)
print(args)


# Main Function
def main():
    driver = session()
    login_ocado(driver)

    for arg in vars(args):
        quantity = getattr(args, arg)
        search(arg, quantity, driver)

    l.close()
    f.close()


# Open JSON formatted shopping list
f = open('grocery.json', )
grocery_list = json.load(f)
# Open JSON credentials file
l = open('login.json', )
login_details = json.load(l)


# Driver Setup
def session():
    options = webdriver.FirefoxOptions()
    profile = FirefoxProfile(
        r'/Users/Luca/Library/Application Support/Firefox/Profiles/s8i83kl9.default'
    )
    driver = webdriver.Firefox(
        firefox_profile=profile,
        options=options,
        executable_path="/Users/luca/Desktop/zoe-ocado/geckodriver")

    driver.get("https://accounts.ocado.com/auth-service/sso/login")

    return driver


# Search for items
def search(item, quantity, driver):
    print("Searching for item ---> ", item)

    button_xpath = '/html/body/div[1]/div[1]/div[3]/article/section[2]'

    # Check if out-of-stock element exists then opt for the next choice in line.
    choice = 0
    while True:
        driver.get('https://www.ocado.com/products/' +
                   grocery_list[item]['id'][choice])
        time.sleep(2)

        if exists(driver, validator='bop-outOfStock', type='class'):
            choice += 1
            if choice > len(grocery_list[item]['id']) - 1:
                return
        else:
            break

    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, button_xpath + "/ul/li/div[1]/input")))
        add_item = driver.find_element_by_xpath(button_xpath +
                                                "/ul/li/div[1]/input")
        add_item.click()
        add_item.send_keys(Keys.BACKSPACE)
        add_item.send_keys(str(grocery_list[item]['quantity']))
    except (NoSuchElementException, TimeoutException) as e:
        el = driver.find_element_by_xpath(button_xpath +
                                          "/ul/li/div[1]/button")
        el.click()

        time.sleep(2)
        add_item = driver.find_element_by_xpath(button_xpath +
                                                "/ul/li/div[1]/input")
        add_item.click()
        add_item.send_keys(Keys.BACKSPACE)
        add_item.send_keys(str(grocery_list[item]['quantity']))

    print('\tYou now have ' + str(grocery_list[item]['quantity']) + ' ' +
          item + ' in basket...')


# Login into Ocado
def login_ocado(driver):
    login = driver.find_element_by_id("login-input")
    login.clear()
    login.send_keys(login_details['email'])
    pword = driver.find_element_by_name("password")
    pword.clear()
    pword.send_keys(login_details['password'])

    time.sleep(7)  # Decrease chances of getting detected by Recaptcha v3
    button = driver.find_element_by_id("login-submit-button")
    button.click()

    # Allow time in case of Recaptcha v3
    time.sleep(6)


main()
