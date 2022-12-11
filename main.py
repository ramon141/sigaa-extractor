from selenium import webdriver
# import chromedriver_autoinstaller
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from constants import *
from xpaths import *
import re


def get_main_info(driver: webdriver.Chrome, username, password, institution='ufopa'):
    infos = {
        'name': '',
        'picture': '',
        'description': '',
        'matriculationNumber': '',
        'course': '',
        'indices': {
            'MC': '', 'MCN': '', 'IEPL': '', 'IEAN': '', 'IECHP': '',
            'IRA': '', 'IECH': '', 'IEA': '', 'ISPL': ''
        },
        'first_year': '',
        'percentage_completed': ''
    }

    base_path = 'https://sigaa.' + institution + '.edu.br'
    login(driver, base_path, username, password)

    infos['name'] = driver.find_element(By.XPATH, MAIN_SPAN_NAME).text

    infos['picture'] = driver.find_element(
        By.XPATH, MAIN_IMG_USER).screenshot_as_base64

    infos['description'] = driver.find_element(
        By.XPATH, MAIN_SPAN_DESCRIPTION).text

    infos['matriculationNumber'] = driver.find_element(
        By.XPATH, MAIN_SPAN_MATRICULATION_NUMBER).text

    infos['course'] = driver.find_element(By.XPATH, MAIN_SPAN_COURSE).text

    infos['first_year'] = driver.find_element(
        By.XPATH, MAIN_SPAN_FIRST_YEAR).text

    percentage_completed = driver.find_element(
        By.XPATH, MAIN_SPAN_PERCENTAGE_COMPLETED).text
    infos['percentage_completed'] = re.findall(
        r'\b\d+\b', percentage_completed)[0]

    return infos


def login(driver: webdriver.Chrome, base_path, user, password):
    driver.get(base_path + PAGE_LOGIN)
    driver.find_element(By.XPATH, LOGIN_INPUT_USER).send_keys(user)
    driver.find_element(By.XPATH, LOGIN_INPUT_PASSWORD).send_keys(password)
    driver.find_element(By.XPATH, LOGIN_BUTTON_SUBMIT).click()
    WebDriverWait(driver, 10).until(
        # Espera até o nome aparecer
        EC.presence_of_element_located((By.XPATH, MAIN_SPAN_NAME))
    )


def click_btn_restaurant(driver: webdriver.Chrome):
    btn_restaurant = driver.find_element(By.XPATH, MAIN_BUTTON_OTHERS)
    actions.move_to_element(btn_restaurant).perform()

    btn_restaurant = driver.find_element(By.XPATH, MAIN_BUTTON_RESTAURANT)
    actions.move_to_element(btn_restaurant).perform()

    actions.click(on_element=btn_restaurant).perform()


def get_restaurant_info(driver: webdriver.Chrome, username, password, institution='ufopa'):
    infos = {
        'credits_available': '',
        'qr_code_picture': '',
        'code': '',
        'situation': ''
    }

    base_path_sigaa = 'https://sigaa.' + institution + '.edu.br/'
    login(driver, base_path_sigaa, username, password)
    click_btn_restaurant(driver)

    WebDriverWait(driver, 10).until(
        # Espera os créditos aparecerem
        EC.presence_of_element_located((By.XPATH, RESTAURANT_SPAN_CREDITS))
    )

    infos['credits_available'] = driver.find_element(
        By.XPATH, RESTAURANT_SPAN_CREDITS).text

    infos['code'] = driver.find_element(
        By.XPATH, RESTAURANT_SPAN_CODE).text

    infos['situation'] = driver.find_element(
        By.XPATH, RESTAURANT_SPAN_SITUATION).text

    infos['qr_code_picture'] = driver.find_element(
        By.XPATH, RESTAURANT_IMG_QR_CODE).screenshot_as_base64

    return infos


# Local
# chromedriver_autoinstaller.install()
# driver = webdriver.Chrome()
# actions = ActionChains(driver)


# Heroku
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get(
    "CHROMEDRIVER_PATH"), options=chrome_options)
actions = ActionChains(driver)
