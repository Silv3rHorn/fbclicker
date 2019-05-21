from selenium.common.exceptions import NoSuchElementException

import time


def login(driver, username, password):
    print("Logging in...")
    # search for login textbox
    try:
        e_username = driver.find_element_by_id('email')
        e_username.send_keys(username)
    except NoSuchElementException:
        print("Cannot find Email or Phone textbox!")
        exit()
    # search for password textbox
    try:
        e_password = driver.find_element_by_id('pass')
        e_password.send_keys(password)
    except NoSuchElementException:
        print("Cannot find Password textbox!")
        exit()
    # search for login button
    try:
        e_login = driver.find_element_by_class_name("uiButtonConfirm")
        e_login.click()
    except NoSuchElementException:
        print("Cannot find Log In button")
        exit()


def scroll_to_bottom(driver, pause_time):
    # get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # wait to load page
        time.sleep(pause_time)

        # calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def navigation_panel(driver):
    # search for logout navigation panel
    try:
        e_navigation_panel = driver.find_element_by_id('userNavigationLabel')
        e_navigation_panel.click()
    except NoSuchElementException:
        print("Cannot find Navigation Panel button")
        exit()

    time.sleep(1)


def logout(driver):
    print("Logging out...")
    navigation_panel(driver)

    try:
        e_logout = driver.find_element_by_partial_link_text('Log Out')
        e_logout.click()
    except NoSuchElementException:
        print("Cannot find Log Out selection")
        exit()
