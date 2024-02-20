import csv
import requests
import scrape_restaurants

def open_selenium(url):
    headless_option = webdriver.FirefoxOptions()
    headless_option.add_argument("--headless")
    driver = webdriver.Firefox()
    driver.get(url)
    return driver

def close_selenium(driver):
    driver.close()
    return

def get_long_lat(address):
    base_url = "https://api.opencagedata.com/geocode/v1/json"
    api_key = "6646d8f7bf764442b0766b38e70a9856"

    params = {
        "q": address,
        "key": api_key
    }

    response = requests.get(base_url, params)
    data = response.json()

    if 'results' in data and data['results']:
        latitude = data['results'][0]['geometry']['lat']
        longitude = data['results'][0]['geometry']['lng']
        return latitude, longitude
    else:
        return None

def add_coords_export_file(file_item, coords):
    if file_item is None or coords is None:
        pass    
    else:
        file_item = file_item + "," + str(coords)

    with open("export files\\scraped_data_with_coords.csv", mode="a+", newline="") as store_file:
        store_file.write(file_item)
        store_file.write("\n")

def read_file(file):
    temp_arr = []
    with open(file, "r") as open_file:
        for line in open_file:
            temp_arr.append(line.strip())
    
    return temp_arr

if __name__ == "__main__":
    print(scrape_restaurants.main())
    # file_arr = scrape_restaurants.main()
    # for item in file_arr:
    #     coords = get_long_lat(item)
    #     add_coords_export_file(item, coords)