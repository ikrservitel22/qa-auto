from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utili.config import TIMEOUT


def wait_visible_xpath(driver, xpath, timeout=None):
    t = timeout or TIMEOUT
    return WebDriverWait(driver, t).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )


def wait_clickable_xpath(driver, xpath, timeout=None):
    t = timeout or TIMEOUT
    return WebDriverWait(driver, t).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )


def click_when_clickable(driver, xpath, timeout=None):
    el = wait_clickable_xpath(driver, xpath, timeout)
    el.click()
    return el


def send_keys_when_visible(driver, xpath, text, timeout=None):
    el = wait_visible_xpath(driver, xpath, timeout)
    try:
        el.clear()
    except Exception:
        pass
    el.send_keys(text)
    return el
