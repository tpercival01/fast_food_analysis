import csv

def export_(arr_locations, restaurant_name, town):
    with open("export files\\scraped_data.csv", mode="a+", newline="") as store_file:
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