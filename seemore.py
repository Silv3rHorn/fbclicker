#!/usr/bin/python

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import argparse
import helpers
import platform
import sys
import time

SHORT_PAUSE_TIME = 1
LONG_PAUSE_TIME = 3
FACEBOOK_HOME = 'https://www.facebook.com/'


def go_to_activity_log(driver):
    # search for profile button
    try:
        e_profile = driver.find_element_by_xpath('//*[@title="Profile"]')
        e_profile.click()
    except NoSuchElementException:
        print("Cannot find Profile button")
        exit()

    time.sleep(SHORT_PAUSE_TIME)

    # extract fb username from url to access user's activity log page
    url = driver.current_url
    fb_username = url.split('/')[-1]
    dest_url = FACEBOOK_HOME + fb_username + '/' + 'allactivity?privacy_source=activity_log_top_menu'
    driver.get(dest_url)

    time.sleep(LONG_PAUSE_TIME)


def see_more(driver):
    print("seeing more...")
    helpers.navigation_panel(driver)

    # search for Activity log selection in logout panel
    try:
        e_activity_log = driver.find_element_by_partial_link_text('Activity log')
        e_activity_log.click()
        # go_to_activity_log(driver)
    except NoSuchElementException:
        print("Cannot find Activity log selection")
        print("Going to Activity log page via profile page instead")
        go_to_activity_log(driver)

    time.sleep(SHORT_PAUSE_TIME)

    # search for Posts selection in sidebar
    try:
        e_posts = driver.find_element_by_xpath('//*[@title="Posts"]')
        e_posts.click()
    except NoSuchElementException:
        print("Cannot find Posts button")
        exit()

    time.sleep(LONG_PAUSE_TIME)
    helpers.scroll_to_bottom(driver, LONG_PAUSE_TIME)
    time.sleep(SHORT_PAUSE_TIME)

    # search for all 'See more's in the page
    try:
        e_see_more = driver.find_elements_by_xpath(".//span[@class='see_more_link_inner']")
        e_see_more.reverse()
        print("Total see mores: ", len(e_see_more))
        for element in e_see_more:
            driver.execute_script("arguments[0].click();", element)
            time.sleep(SHORT_PAUSE_TIME)
    except NoSuchElementException:
        print("Cannot find See more button")
        exit()


def main():
    global SHORT_PAUSE_TIME, LONG_PAUSE_TIME

    argument_parser = argparse.ArgumentParser(description=(
        "logs in to user's facebook account, and click See more for all his/her posts"
    ))

    argument_parser.add_argument('-u', '--username', default=None, help="username of user")
    argument_parser.add_argument('-p', '--password', default=None, help="password of user")
    argument_parser.add_argument('-s', '--sp', type=int, default=SHORT_PAUSE_TIME, help="short pause duration")
    argument_parser.add_argument('-l', '--lp', type=int, default=LONG_PAUSE_TIME, help="long pause duration")

    arguments = argument_parser.parse_args()
    if arguments.username is None or arguments.password is None:
        print("Missing username or password of account!")
        exit()
    if arguments.sp != SHORT_PAUSE_TIME:
        SHORT_PAUSE_TIME = arguments.sp
    if arguments.lp != LONG_PAUSE_TIME:
        LONG_PAUSE_TIME = arguments.lp

    # configure ChromeDriver
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--test-type')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-extensions')
    options.add_experimental_option("detach", True)
    options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile': {
            'password_manager_enabled': False
        }
    })

    # point to Google Chrome executable location, default location is used
    if platform.system() == 'Windows':
        options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    else:
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    driver = webdriver.Chrome(options=options)
    driver.get(FACEBOOK_HOME)
    helpers.login(driver, arguments.username, arguments.password)
    time.sleep(SHORT_PAUSE_TIME)
    see_more(driver)
    # helpers.logout(driver)


if __name__ == '__main__':
    if not main():
        sys.exit(1)
    else:
        sys.exit(0)
