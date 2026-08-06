import time

from selenium.common.exceptions import ElementClickInterceptedException
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
    try:
        el.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        time.sleep(0.5)
        try:
            el.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", el)
    return el


def send_keys_when_visible(driver, xpath, text, timeout=None):
    el = wait_visible_xpath(driver, xpath, timeout)
    try:
        el.clear()
    except Exception:
        pass
    el.send_keys(text)
    return el


def wait_text_in_element(driver, xpath, text, timeout=None):
    t = timeout or TIMEOUT
    return WebDriverWait(driver, t).until(
        EC.text_to_be_present_in_element((By.XPATH, xpath), text)
    )


def wait_text_present(driver, text, timeout=None):
    t = timeout or TIMEOUT
    xpath = f"//*[contains(normalize-space(.), '{text}') ]"
    # Permite buscar cualquier elemento cuyo texto contenga la cadena dada
    return WebDriverWait(driver, t).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )


def wait_text_in_page(driver, text, timeout=None):
    t = timeout or TIMEOUT
    return WebDriverWait(driver, t).until(
        lambda d: text in d.page_source
    )
