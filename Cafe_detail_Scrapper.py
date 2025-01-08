from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
from Services_scrapper import service_scrapper
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-usb')
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--v=1')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)


# Open Google Maps search page
def Scrapper(location):
    driver.get(f"https://www.google.co.in/maps/search/cafe+with+wifi+and+remote+working+in+{location}")

    # Initialize variables
    result_links = set()

    # Locate the scrollable element
    scrollable_element_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]'
    scrollable_element = driver.find_element(By.XPATH, scrollable_element_xpath)

    # Scroll and collect cafe links
    for _ in range(7):
        time.sleep(2)  # Wait to load results
        scrollable_element.send_keys(Keys.PAGE_DOWN)

        # Collect unique cafe links
        cafe_links = driver.find_elements(By.XPATH, "//a[contains(@aria-label, 'Cafe') and @href]")
        for link in cafe_links:
            result_links.add(link.get_attribute("href"))

    # Convert set to list
    result_links = list(result_links)

    # Function to extract cafe details

    def extract_cafe_details(driver, link):
        driver.get(link)
        time.sleep(5)  # Allow page to load fully

        # Initialize details dictionary
        details = {
            "Link": link,
            "Name": "Not Found",
            "Address": "Not Found",
            "Image": "Not Found",
            "Rating": "Not Found",
            "Reviews": "Not Found",
            "Price Range": "Not Found",
            "Wheelchair Accessible": "Not Found",
            "Menu": "Not Found",
            "Website": "Not Found"
        }

        try:
            # Locate the name of the cafe dynamically
            name_xpath = '//*[@id="QA0Szd"]//h1'
            name_element = driver.find_element(By.XPATH, name_xpath)
            details["Name"] = name_element.text.strip()
        except:
            print("Name not found")

        try:
            # Locate the address dynamically
            address_elements = driver.find_elements(By.XPATH,
                                                    '//*[@id="QA0Szd"]//button[contains(@aria-label, "Address")]/div/div[2]')
            for element in address_elements:
                if element.text.strip():
                    details["Address"] = element.text.strip()
                    break
        except:
            print("Address not found")

        try:
            # Locate the image dynamically
            image_xpath = '//*[@id="QA0Szd"]//img[contains(@src, "googleusercontent")]'
            image_element = driver.find_element(By.XPATH, image_xpath)
            details["Image"] = image_element.get_attribute("src")
        except:
            print("Image not found")

        try:
            # Locate rating dynamically
            rating_element = driver.find_element(By.XPATH, '//div[contains(@aria-label, "stars")]')
            details["Rating"] = rating_element.get_attribute("aria-label").split(" ")[0]
        except:
            print("Rating not found")

        try:
            # Locate reviews dynamically
            reviews_element = driver.find_element(By.XPATH,
                                                  '//span[contains(@aria-label, "reviews") or contains(text(), "reviews")]')
            details["Reviews"] = reviews_element.get_attribute("aria-label").split(" ")[0]
        except:
            print("Reviews not found")

        try:
            # Locate price range dynamically (searching for ₹, $, or general price indicators)
            price_elements = driver.find_elements(By.XPATH,
                                                  '//*[contains(@aria-label, "Price range") or contains(text(), "₹") or contains(text(), "$")]')
            for price_element in price_elements:
                text = price_element.text.strip()
                if text:
                    details["Price Range"] = text
                    break
        except:
            print("Price range not found")

        try:
            # Locate wheelchair accessibility dynamically
            wheelchair_element = driver.find_element(By.XPATH,
                                                     '//*[contains(@aria-label, "Wheelchair-accessible") or contains(@aria-label, "accessible entrance")]')
            details["Wheelchair Accessible"] = wheelchair_element.get_attribute("aria-label")
        except:
            print("Wheelchair accessibility not found")
        try:
            menu_element = driver.find_element(By.PARTIAL_LINK_TEXT, "Menu")
            details["Menu"] = menu_element.get_attribute("href")
        except:
            details["Menu"] = "Not Found"

        # Extract Website link
        try:
            details["Website"] = driver.find_element(By.XPATH, '//a[contains(@aria-label, "Website")]').get_attribute(
                "href")

        except:
            print("website not found")

        return details

    # Extract and print cafe details
    print("\nCafe Details:")
    cafe_details_list = []  # Store cafe details as a list of dictionaries

    for index, link in enumerate(result_links):
        print(f"Extracting details for cafe {index + 1}/{len(result_links)}...")
        cafe_details = extract_cafe_details(driver, link)
        cafe_details_list.append(cafe_details)

    # Print collected cafe details
    # for cafe in cafe_details_list:
    #     print(f"Name: {cafe['Name']}")
    #     print(f"Address: {cafe['Address']}")
    #     print(f"Image Link: {cafe['Image']}")
    #     print(f"Rating: {cafe['Rating']}")
    #     print(f"Reviews: {cafe['Reviews']}")
    #     print(f"Price Range: {cafe['Price Range']}")
    #     print(f"Wheelchair Accessible: {cafe['Wheelchair Accessible']}")
    #     print(f"Menu: {cafe['Menu']}")
    #     print(f"Website: {cafe['Website']}\n")

    with open("cafe_details.json", "w") as json_file:
        json.dump(cafe_details_list, json_file, indent=4)
    print("Details have been saved to 'cafe_details.json'.")

    driver.quit()
    service_scrapper()
