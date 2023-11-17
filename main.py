from selenium import webdriver
from selenium.common import WebDriverException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from time import time

from selenium.webdriver.support.wait import WebDriverWait

# Keep chrome opened
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("window-size=1400,1200")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/cookieclicker/")
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "langSelect-EN")))
driver.find_element(By.ID, value="langSelect-EN").click()

wait_time = 3


def get_power_ups():
    list_powers_cost = []
    click_upgrade()
    power_ups = driver.find_elements(By.CSS_SELECTOR, value="div.product.unlocked.enabled")

    if len(power_ups) > 0:
        for power_cost in power_ups:
            price_text = power_cost.find_element(By.CSS_SELECTOR, value="div > span.price").text.replace(",", "")
            if "," in price_text:
                price_text.replace(",", "")
            elif "." and " million" in price_text:
                price_text.replace(".", "")
                price_text.replace(" million", "000")
            price = int(price_text)
            list_powers_cost.append(price)
        power_ups[list_powers_cost.index(max(list_powers_cost))].click()


def click_upgrade():
    elements = driver.find_elements(By.CSS_SELECTOR, value="div.crate.upgrade.enabled")
    if len(elements) > 0:
        try:
            elements[0].click()
        except StaleElementReferenceException:
            click_upgrade()


start_time = time()
timeout = start_time + 300
power_up_time = start_time
big_cookie = driver.find_element(By.ID, value="bigCookie")
while time() < timeout:
    try:
        big_cookie.click()
    except StaleElementReferenceException:
        big_cookie = driver.find_element(By.ID, value="bigCookie")

    if start_time > start_time + 180:
        wait_time += 2
    if power_up_time + wait_time < time():
        get_power_ups()
        power_up_time = time()


print(driver.find_element(By.ID, value="cookies").text)

driver.quit()