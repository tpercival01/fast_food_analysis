from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import csv

def open_selenium(url):
    headless_option = webdriver.FirefoxOptions()
    headless_option.add_argument("--headless")
    driver = webdriver.Firefox()
    driver.get(url)
    return driver

def close_selenium(driver):
    driver.close()
    return

def get_mcdonalds_data(town):
    # assign the ID of the input box for the location and the url 
    mcdonalds_location_input_id = "form-text-1673594539"
    mcdonalds_enter_search_id = "button-93a5672f18"
    mcdonalds_finder_url = "https://www.mcdonalds.com/gb/en-gb/restaurant-locator.html"
    
    # start an instance of selenium at the above url
    selenium_driver = open_selenium(mcdonalds_finder_url)

    sleep(2)

    # enter the town name to find the restaurants in that town
    selenium_driver.find_element("id", mcdonalds_location_input_id).send_keys(town)

    selenium_driver.find_element("id", mcdonalds_enter_search_id).click()

    sleep(1)

    selenium_driver.find_element("id", "onetrust-reject-all-handler").click()

    sleep(1)
    
    # find the element that holds the number of restaurants
    # get its child element then split that to find the specific number and return it as an int 
    number_of_restaurants = int(selenium_driver.find_element(By.CLASS_NAME, "cmp-restaurant-locator__info").find_element(By.TAG_NAME, "h2").text.split(" ")[4])
    
    for j in range(int(number_of_restaurants / 5) - 1):
        selenium_driver.find_element("id", "button-93a5672f17").click()
        sleep(1)
    
    sleep(2)

    all_location_names_html = selenium_driver.find_elements(By.CLASS_NAME, "cmp-restaurant-locator__restaurant-list-item-details-al1")
    all_location_addresses_html = selenium_driver.find_elements(By.CLASS_NAME, "cmp-restaurant-locator__restaurant-list-item-details-al2")
    all_location_names_str = []
    all_location_addresses_str = []

    for i in all_location_names_html:
       all_location_names_str.append(i.find_element(By.TAG_NAME, "a").text)

    for j in all_location_addresses_html:
        all_location_addresses_str.append(j.text)

    all_locations = zip(all_location_names_str, all_location_addresses_str)

    close_selenium(selenium_driver)
    return all_locations

def get_kfc_data(town):
    kfc_finder_url = "https://www.kfc.co.uk/kfc-near-me"
    kfc_search_class = "ibGAaX"
    kfc_search_button = "dkbljC"

    selenium_driver = open_selenium(kfc_finder_url)
    sleep(2)

    selenium_driver.find_element(By.ID, "onetrust-reject-all-handler").click()
    sleep(2)

    selenium_driver.find_element(By.CLASS_NAME, kfc_search_class).send_keys(town)
    selenium_driver.find_element(By.CLASS_NAME, kfc_search_button).click()
    sleep(2)

    selenium_driver.refresh()
    sleep(2)

    if selenium_driver.find_element(By.CSS_SELECTOR, 'button[title^="Zoom out"]').is_enabled():
        selenium_driver.find_element(By.CSS_SELECTOR, 'button[title^="Zoom out"]').click()
    
    sleep(1)

    if selenium_driver.find_element(By.CSS_SELECTOR, 'button[title^="Zoom out"]').is_enabled():
        selenium_driver.find_element(By.CSS_SELECTOR, 'button[title^="Zoom out"]').click()

    all_location_names = selenium_driver.find_elements(By.CLASS_NAME, "hyEoTK")

    all_locations_tuple = []

    for name in all_location_names:
        temp_tuple = (name.find_element(By.TAG_NAME, "h3").text, name.find_element(By.TAG_NAME, "p").text)
        if temp_tuple[0] == "" or temp_tuple[1] == "":
            continue
        else:
            all_locations_tuple.append(temp_tuple)
        
    close_selenium(selenium_driver)
    return all_locations_tuple

def get_subway_data(town):
    subway_url = "https://www.subway.com/en-GB/FindAStore"

    selenium_driver = open_selenium(subway_url)
    sleep(2)
    selenium_driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

    selenium_driver.find_element(By.CLASS_NAME, "searchLocationInput").send_keys(town)
    selenium_driver.find_element(By.CLASS_NAME, "searchLocationInput").send_keys(Keys.ENTER)
    sleep(2)

    num_pages = selenium_driver.find_element(By.CLASS_NAME, "locatorResultsPaging").text.split(" ")[3]
    arr_of_addresses = []
    for i in range(int(num_pages) - 1):
        parent_div = selenium_driver.find_elements(By.CLASS_NAME, "locatorMainInfo")
        
        for location_card in parent_div:
            find_town = location_card.find_element(By.CLASS_NAME, "locatorAddressCityState").text

            if find_town.split(",")[0] == town:
                main_address = location_card.find_element(By.CLASS_NAME, "storeMainAddress").text
                temp_tuple = (main_address, find_town)
                arr_of_addresses.append(temp_tuple)
    
        selenium_driver.find_element(By.CLASS_NAME, "sprite-next-page-arrow ").click()

    close_selenium(selenium_driver)

    return arr_of_addresses

def export_data_to_csv(arr_locations, restaurant_name, town):
    with open("test.csv", mode="a+", newline="") as store_file:
        fastfoodCSV = csv.writer(store_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

        if town == "London":
            fastfoodCSV.writerow(["restaurant", "street", "area", "post code", "city", "country"])

        country = "United Kingdom"
        for item in arr_locations:
            match(restaurant_name):
                case "McDonalds":
                    street = item[0]
                    area = item[1].split(",")[0]
                    post_code = item[1].split(",")[1].split("|")[0]
                case "KFC":
                    street = item[0]
                    area = item[1].split(",")[0]
                    post_code = item[1].split(",")[1]
                case "Subway":
                    street = item[0]
                    area = item[1].split(",")[0]
                    post_code = item[1].split(",")[1].split("|")[0]

            fastfoodCSV.writerow([restaurant_name, street, area, post_code, town, country])
        
        store_file.close()

if __name__ == "__main__":
    towns = ["London", "Edinburgh", "Cardiff"]
    for town in towns:
        temp_data = get_mcdonalds_data(town)
        temp_data2 = get_kfc_data(town)
        temp_data3 = get_subway_data(town)

        export_data_to_csv(temp_data, "McDonalds", town)
        export_data_to_csv(temp_data2, "KFC", town)
        export_data_to_csv(temp_data3, "Subway", town)