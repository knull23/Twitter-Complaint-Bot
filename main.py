from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

PROMISED_DOWN = 150
PROMISED_UP = 10
TWITTER_URL = "https://twitter.com/"
TWITTER_USERNAME = "YOUR_USERNAME"
TWITTER_EMAIL = "YOUR_EMAIL"
TWITTER_PASSWORD = "YOUR_PASSWORD"
SPEED_TEST_URL = "https://www.speedtest.net/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)


class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get(SPEED_TEST_URL)
        time.sleep(3)

        # Handle Privacy pop-up
        try:
            privacy_button = self.driver.find_element(By.ID, value="onetrust-accept-btn-handler")
            privacy_button.click()
            print("Accepted privacy policy.")
        except NoSuchElementException:
            print("No privacy policy pop-up found.")

        go_button = self.driver.find_element(By.CSS_SELECTOR, value=".start-button a")
        go_button.click()

        time.sleep(60)
        self.down = self.driver.find_element(By.CSS_SELECTOR, value=".download-speed").text
        self.up = self.driver.find_element(By.CSS_SELECTOR, value=".upload-speed").text
        print(f"Download speed: {self.down} Mbps")
        print(f"Upload speed: {self.up} Mbps")

    def tweet_at_provider(self):
        self.driver.get(f"{TWITTER_URL}login")

        time.sleep(3)
        try:
            # Find email/phone/username input field
            email = self.driver.find_element(By.NAME, value='text')
            email.send_keys(TWITTER_EMAIL)
            email.send_keys(Keys.ENTER)
            time.sleep(3)

            # Find password input field
            password = self.driver.find_element(By.NAME, value='password')
            password.send_keys(TWITTER_PASSWORD)
            password.send_keys(Keys.ENTER)
        except NoSuchElementException:
            print("Error: Login fields not found.")
            self.driver.quit()
            return

        time.sleep(5)
        if float(self.down) < PROMISED_DOWN or float(self.up) < PROMISED_UP:
            tweet_compose = self.driver.find_element(By.CSS_SELECTOR, value='div.public-DraftStyleDefault-block.public-DraftStyleDefault-ltr')
            tweet = f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"
            tweet_compose.send_keys(tweet)
            time.sleep(3)

            tweet_button = self.driver.find_element(By.XPATH, value='//div[@data-testid="tweetButtonInline"]')
            tweet_button.click()

        time.sleep(5)
        self.driver.quit()


bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
bot.tweet_at_provider()

