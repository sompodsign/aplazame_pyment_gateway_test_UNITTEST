import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class TestAplazame(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.chrome_options = webdriver.ChromeOptions()

        cls.chrome_options.add_argument("--headless")
        cls.chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")
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
        self.wait.until(EC.element_to_be_clickable((By.NAME, "document_id"))).send_keys("X0345345 T")
        self.wait.until(EC.element_to_be_clickable((By.NAME, "birthday"))).send_keys("22121995")
        time.sleep(0.2)

        self.driver.find_element_by_name("job_status").click()  # profession selector
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "apz_typeahead__prediction_content"))).click()
        time.sleep(0.5)

        job = self.driver.find_element_by_name("job_sector")
        job.send_keys(Keys.ARROW_DOWN)
        job.send_keys(Keys.ENTER)

        nation = self.driver.find_element_by_name("nationality")
        nation.send_keys(Keys.ARROW_DOWN)
        nation.send_keys(Keys.ENTER)

        self.driver.find_element_by_name("checkout_checkboxes[aplazame_conditions]").click()  # checkbox check
        time.sleep(0.2)
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn"))).click()

        iframes = self.driver.find_elements_by_xpath("//iframe[contains(@name,'__privateStripeFrame')]")
        self.driver.switch_to.frame(iframes[0])
        self.wait.until(EC.element_to_be_clickable((By.NAME, "cardnumber")))
        card_number = self.driver.find_element_by_name("cardnumber")
        card_number.send_keys("4074655237184431")
        self.driver.execute_script("window.stop();");

        self.driver.switch_to.frame(iframes[1])  # frame switch to exp date
        self.wait.until(EC.element_to_be_clickable((By.NAME, "exp-date")))
        exp_field = self.driver.find_element_by_name("exp-date")
        exp_field.send_keys(1023)
        # self.driver.execute_script("window.stop();");
                # break

            # except:
            #     print("no such element")

        # self.driver.switch_to.frame(iframes[2])
        # self.wait.until(EC.element_to_be_clickable((By.NAME, "cvc")))
        # exp_field = self.driver.find_element_by_name("cvc")
        # exp_field.send_keys(657)

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     cls.driver.close()
    #     cls.driver.quit()
