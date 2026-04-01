# Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from urllib.parse import urljoin
import requests
import os

# Global vars
target = "https://sw-unlimited-db.com/sets/legends-of-the-force"
landing_folder_root = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
images_saved = 0

def download_card(card):
    global images_saved
    first = True
    card.click()
    images = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sm\\:h-80"))
    )
    current_card_title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1.text-lg"))
    ).text
    print("- Steeling "+current_card_title)
    for image in images:
        url = urljoin("https://sw-unlimited-db.com", image.get_attribute("src"))
        response = requests.get(url)
        file_name = os.path.join(landing_folder_root, current_card_title.replace(" ", "-")+"-"+("front" if first else "back")+".png")
        with open(file_name, "wb") as f:
            f.write(response.content)
        images_saved += 1
        first = False
    driver.back()

# Create landing folder
os.mkdir(landing_folder_root)

print("=======================")
print("== SCRAPING STARTED ==")
print("=======================")

# Set up driver
options = webdriver.ChromeOptions()
#options.add_argument("--headless")
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

# Load page
driver.get(target)
driver.implicitly_wait(10)
time.sleep(5)

# Get cards
cards_len = len(WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#card-overview > .container > div > a"))
))

# Click through all cards
for i in range(cards_len):
    cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#card-overview > .container > div > a"))
    )
    try:
        download_card(cards[i])
    except Exception as error:
        print("- Couldn't steal a card.")
        driver.get(target)
    i += 1

print("=======================")
print("== SCRAPING FINISHED ==")
print("=======================")
print("Saved {num} images.".format(num=images_saved))
