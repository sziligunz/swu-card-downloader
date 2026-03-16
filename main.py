# Imports
from selenium import webdriver

# Global vars
target = "https://starwarsunlimited.com/cards?expansion=73"
images_saved = 0

# Set up driver
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

# Driver actions
# Click <div>Leaders</div>'s parent's parent
# Wait for load
scrape_section()
# Click <div>Bases</div>'s parent's parent
# Wait for load
scrape_section()
# Click <div>Units, Events & Upgrades</div>'s parent's parent
# Wait for load
scrape_section()

print("Finished scraping. Saved " + images_saved + " images.")

def scrape_section():
    # While <svg name="chevronRight">'s parent's attribute aria-disabled == false:
        # Get all <img alt="Front Of Card Art">
        # For all above:
            # Click on img
            # Try
                # Wait for all children of <div label="Card info modal"> to load
                # Save source image in <img class="ml:card-modal-grid-child-left">
                images_saved += 1
            # Click on <button>Back</button>
            # Try
                # Save source image in <img class="ml:card-modal-grid-child-left">
                # Click on <div label="Card info modal"> first div > first div > second button
                images_saved += 1
