import time

from selenium import webdriver


lc_js = '''
// Focus to the item.
window.scrollBy(0, 174);
// Set the price back to origin, and delete the elements about discount.
$(".sale-price").text($(".discounted-price").text());
$(".discounted-price").remove();
$(".save-percentage").remove();
'''

def get_screenshot(url, filepath):
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(url)

    # Execute different script in differnt site, to delete the discount price.
    browser.execute_script(lc_js)
    # Need some time to render the modified page.
    time.sleep(2)

    browser.save_screenshot('%s_screenshot.png' % filepath)
    browser.close()
