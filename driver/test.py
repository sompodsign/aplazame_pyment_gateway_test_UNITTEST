import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time

driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
driver.maximize_window()
driver.implicitly_wait(10)

driver.get("https://cdn.aplazame.com/widgets/demo/")
time.sleep(10)
driver.find_element_by_class_name("pay-with-aplazame").click()

wait=WebDriverWait(driver,20)
wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "aplazame-checkout-iframe")))
wait.until(EC.element_to_be_clickable((By.NAME, "accepts_gdpr"))).click()

driver.find_element_by_class_name("btn").click()
time.sleep(5)

driver.find_element_by_class_name("btn").click()
