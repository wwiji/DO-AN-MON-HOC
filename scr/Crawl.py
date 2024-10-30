import json
from selenium import webdriver
from selenium.webdriver.common.by import By


class Get_Data:
    def __init__(self, start_page, end_page):
        self.start_page = start_page
        self.end_page = end_page
        self.list_href = []
        self.data = []


    def get_driver(self):
        return webdriver.Chrome()

    # get full link chung cu
    def get_links(self):
        url = "https://batdongsan.com.vn/ban-can-ho-chung-cu-tp-hcm/p{}"
        driver = self.get_driver()

        for i in range(self.start_page, self.end_page):
            print(f"Page {i}")
            driver.get(url.format(i))
            try:
                elements = driver.find_elements(By.CLASS_NAME, "js__product-link-for-product-id")
                for element in elements:
                    href = element.get_attribute("href")
                    if href:
                        self.list_href.append(href)
            except:
                print(f"Page {i} errol")

        driver.quit()

    # get thuoc tinh
    def get_feature(self, link):
        driver = self.get_driver()
        driver.get(link)

        # General Information
        try:
            title_element = driver.find_element(By.CLASS_NAME, "re__pr-short-description.js__pr-address")
            title = title_element.text if title_element else "N/A"
        except:
            title = "N/A"

        try:
            name_project_element = driver.find_element(By.CLASS_NAME, "re__project-title")
            name_project = name_project_element.text if name_project_element else "N/A"
        except:
            name_project = "N/A"

        list_items = []

        # Property Specifications
        try:
            dict_items = driver.find_elements(By.CLASS_NAME, "re__pr-specs-content.js__other-info")
            for items in dict_items:
                titles = items.find_elements(By.CLASS_NAME, "re__pr-specs-content-item-title")
                values = items.find_elements(By.CLASS_NAME, "re__pr-specs-content-item-value")
                for title_element, value_element in zip(titles, values):
                    list_items.append({
                        "title": title_element.text if title_element else "N/A",
                        "value": value_element.text if value_element else "N/A"
                    })
        except:
            pass

        driver.quit()

        return {
            "Title": title,
            "Name_project": name_project,
            "Specifications": list_items
        }

    def properties(self):
        for link in self.list_href:
            property_details = self.get_feature(link)
            self.data.append(property_details)

    def save_data_to_json(self, filename='property_data.json'):
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(self.data, json_file, indent=2, ensure_ascii=False)
        print(f"Data has been saved to '{filename}'")
        print(f"Total records collected: {len(self.data)}")

