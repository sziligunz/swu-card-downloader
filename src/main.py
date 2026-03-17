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
target = "https://starwarsunlimited.com/cards?expansion=73"
landing_folder_root = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
images_saved = 0

# Create landing folder
os.mkdir(landing_folder_root)

def scrape_section(current_page: str):
    global images_saved
    landing_folder_name = landing_folder_root + "/" + current_page
    os.mkdir(landing_folder_name)
    first_run = True
    while first_run or driver.find_element(By.CSS_SELECTOR, "[name='chevronRight']").find_element(By.XPATH, "..").get_attribute("aria-disabled") == "false":
        # Page turn logic
        if not first_run:
            driver.find_element(By.CSS_SELECTOR, "[name='chevronRight']").find_element(By.XPATH, "..").click()
        first_run = False
        # Get images on current page
        images = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[alt='Front Of Card Art']"))
        )
        print("- {page} page has {num} images.".format(page=current_page, num=len(images)))
        # Process images
        for image in images:
            try:
                image.click()
            except:
                driver.find_element(By.CSS_SELECTOR, "svg[name='closeX']").find_element(By.XPATH, "..").click()
                image.click()
            current_card_title = driver.find_element(By.CSS_SELECTOR, "h3.text-2xl.order-2.md\\:order-1.text-neutral-50.font-extrabold").text
            # Process front
            image_relative_src = driver\
                .find_element(By.CLASS_NAME, "ml\\:card-modal-grid-child-left")\
                .find_element(By.CSS_SELECTOR, "img")\
                .get_attribute("src")
            url = urljoin("https://starwarsunlimited.com", image_relative_src)
            response = requests.get(url)
            file_name = os.path.join(landing_folder_name, current_card_title.replace(" ", "-")+"-front.png")
            try:
                with open(file_name, "wb") as f:
                    f.write(response.content)
                    images_saved += 1
            except:
                print("- Couldn't save front image of {title}.".format(title=current_card_title))
            # Process back
            if current_page == "Leaders":
                driver.find_element(By.XPATH, "//button[text()='Back']").click()
                image_relative_src = driver\
                    .find_element(By.CLASS_NAME, "ml\\:card-modal-grid-child-left")\
                    .find_element(By.CSS_SELECTOR, "img")\
                    .get_attribute("src")
                url = urljoin("https://starwarsunlimited.com", image_relative_src)
                response = requests.get(url)
                file_name = os.path.join(landing_folder_name, current_card_title.replace(" ", "-")+"-back.png")
                try:
                    with open(file_name, "wb") as f:
                        f.write(response.content)
                        images_saved += 1
                except:
                    print("- Couldn't save back image of {title}.".format(title=current_card_title))
            driver.find_element(By.CSS_SELECTOR, "svg[name='closeX']").find_element(By.XPATH, "..").click()
            print("- Stolen '{title}'".format(title=current_card_title))

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

# Close pop ups
driver.execute_script("""
arguments[0].remove();
""", driver.find_element(By.ID, "maze-contextual-widget-host"))
driver.find_element(By.ID, "didomi-notice-disagree-button").click()

# Leaders
driver.find_element(By.XPATH, "//div[text()='Leaders']").click()
scrape_section("Leaders")

# Bases
driver.execute_script("window.scrollTo(0, 0);")
driver.find_element(By.XPATH, "//div[text()='Bases']").click()
scrape_section("Bases")

# Units, events, upgrades
driver.execute_script("window.scrollTo(0, 0);")
driver.find_element(By.XPATH, "//div[text()='Units, Events & Upgrades']").click()
scrape_section("Units-Events-Upgrades")

print("=======================")
print("== SCRAPING FINISHED ==")
print("=======================")
print("Saved {num} images.".format(num=images_saved))
