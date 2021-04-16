import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys # need if global id provide
from fake_useragent import UserAgent
import time
import sys


class TestAplazame(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cli_argv = ""
        if len(sys.argv) > 1:
            cli_argv = str(sys.argv[1])
        cls.chrome_options = webdriver.ChromeOptions()
        if cli_argv == "--headless":
            cls.chrome_options.headless = True
        else:
            cls.chrome_options.headless = False
        ua = UserAgent()
        userAgent = ua.random
        cls.chrome_options.add_argument(f'user-agent={userAgent}')
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
        time.sleep(3)
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn"))).click()
        self.wait.until(EC.element_to_be_clickable((By.NAME, "document_id"))).send_keys("12345678 Z")
        self.wait.until(EC.element_to_be_clickable((By.NAME, "birthday"))).send_keys("22121995")
        time.sleep(0.2)

        self.wait.until(EC.element_to_be_clickable((By.NAME, "checkout_checkboxes[aplazame_conditions]"))).click()
        time.sleep(.5)

        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn"))).click()

        ## codes for global ID.
        # self.driver.find_element_by_name("job_status").click()  # profession selector
        # self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "apz_typeahead__prediction_content"))).click()
        # time.sleep(0.5)
        #
        # job = self.driver.find_element_by_name("job_sector")
        # job.send_keys(Keys.ARROW_DOWN)
        # job.send_keys(Keys.ENTER)
        #
        # nation = self.driver.find_element_by_name("nationality")
        # nation.send_keys(Keys.ARROW_DOWN)
        # nation.send_keys(Keys.ENTER)

        iframes = self.driver.find_elements_by_xpath("//iframe[contains(@name,'__privateStripeFrame')]")

        self.driver.switch_to.frame(iframes[0])
        self.wait.until(EC.visibility_of_element_located((By.NAME, "cardnumber")))
        card_number = self.driver.find_element_by_name("cardnumber")
        card_number.send_keys("4074 6552 3718 4431")
        time.sleep(1)

        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "aplazame-checkout-iframe")))
        iframes = self.driver.find_elements_by_xpath("//iframe[contains(@name,'__privateStripeFrame')]")
        self.driver.switch_to.frame(iframes[1])
        self.wait.until(EC.visibility_of_element_located((By.NAME, "exp-date")))
        exp_field = self.driver.find_element_by_name("exp-date")
        exp_field.send_keys(1023)
        time.sleep(1)

        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "aplazame-checkout-iframe")))
        iframes = self.driver.find_elements_by_xpath("//iframe[contains(@name,'__privateStripeFrame')]")
        self.driver.switch_to.frame(iframes[2])
        self.wait.until(EC.visibility_of_element_located((By.NAME, "cvc")))
        exp_field = self.driver.find_element_by_name("cvc")
        exp_field.send_keys(657)
        time.sleep(0.3)

        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "aplazame-checkout-iframe")))
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn"))).click()
        time.sleep(6)
        pin = self.driver.find_element_by_xpath('//*[@id="sandbox"]/span[2]'). \
            get_attribute("innerHTML")

        self.wait.until(EC.visibility_of_element_located((By.ID, "OtpSecureInput"))). \
            send_keys(pin)
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "-result-content")))
        result = self.driver.find_element_by_class_name("-result-description").text

        assert "Tu banco ha denegado el cobro del pago inicial en tu tarjeta. Si quieres" in result

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.close()
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]])
