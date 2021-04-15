import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class TestAplazame(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        cls.chrome_options.add_argument('--disable-extensions')
        cls.chrome_options.add_argument('--no-sandbox')
        cls.chrome_options.add_experimental_option('excludeSwitches',
                                               ['enable-automation'])
        cls.driver = webdriver.Chrome(executable_path=r"driver/chromedriver.exe", options=cls.chrome_options)
        cls.driver.maximize_window()  # maximize window if headless is not running
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 20)

    def test_checkout(self):
        self.driver.get("https://cdn.aplazame.com/widgets/demo/")
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "pay-with-aplazame"))).click()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "aplazame-checkout-iframe")))
        self.wait.until(EC.element_to_be_clickable((By.NAME, "accepts_gdpr"))).click()
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn"))).click()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.close()
        cls.driver.quit()




# X0345345 T