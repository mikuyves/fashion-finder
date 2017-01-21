import time

from selenium import webdriver

from eshop.data.rules import website_rules


def get_screenshot(url, filepath, website):
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(url)

    # Execute different script in differnt site, to delete the discount price.
    browser.execute_script(website_rules[website]['screenshot_js'])
    # Need some time to render the modified page.
    time.sleep(2)

    browser.save_screenshot('%s_screenshot.png' % filepath)
    browser.close()
