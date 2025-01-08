from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-usb')
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--v=1')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)


# Load JSON data from a file (or create a new file if it doesn't exist)
def service_scrapper():
    try:
        with open('cafe_details.json', 'r') as file:
            cafes_data = json.load(file)
    except FileNotFoundError:
        cafes_data = []

    # Extracting links from the cafes data and scraping additional details
    for cafe in cafes_data:
        Link = cafe.get("Link")
        if Link:
            driver.get(Link)
            try:
                # Click on the "About" button to load more information
                about_button = driver.find_element(By.XPATH,
                                                   '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[3]/div[2]')
                about_button.click()
                time.sleep(3)

                # Scroll down to ensure all content is visible
                body = driver.find_element(By.TAG_NAME, "body")
                for _ in range(10):  # Adjust the range for sufficient scrolling
                    body.send_keys(Keys.PAGE_DOWN)
                    time.sleep(1)

                # Locate all list items with a checkmark (services provided by the cafe)
                services = driver.find_elements(By.XPATH, "//li[.//span[contains(@class, 'SwaGS')]]")

                # Extract and clean the service data
                filtered_services = [
                    service.text.replace("\ue5ca\n", "").strip() for service in services if service.text.strip()
                ]

                # Add the extracted services to the cafe data
                cafe["Services"] = filtered_services


            except Exception as e:
                cafe["Services"] = []  # If there is an issue, assign an empty list for services

    # Save the updated cafe data back to the JSON file
    with open('cafe_details.json', 'w') as file:
        json.dump(cafes_data, file, indent=4)

    print("Updated cafe data with services saved to cafe_details.json")
