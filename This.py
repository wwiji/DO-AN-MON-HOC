import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor

# Initialize the driver
driver = webdriver.Chrome()
url = "https://batdongsan.com.vn/ban-can-ho-chung-cu-tp-hcm/p{}"

# Get list of links from the main page
list_href = []
for i in range(2, 50):
    driver.get(url.format(i))
    try:
        # Use WebDriverWait instead of sleep for better efficiency
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "js__product-link-for-product-id"))
        )
        elements = driver.find_elements(By.CLASS_NAME, "js__product-link-for-product-id")
        for element in elements:
            list_href.append(element.get_attribute("href"))
    except:
        print(f"Page {i} could not be loaded properly.")

# Function to get element text
def get_element_text(driver, by, value):
    try:
        return driver.find_element(by, value).text
    except:
        return "N/A"

# Function to get information from a listing page
def get_element(link):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run headless Chrome for efficiency
    local_driver = webdriver.Chrome()
    local_driver.get(link)
    try:
        WebDriverWait(local_driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "re__pr-short-description"))
        )
    except:
        print(f"Could not load details for {link}")
        local_driver.quit()
        return {
            "Title": "N/A",
            "Name Project": "N/A",
            "Dien Tich": "N/A",
            "Gia": "N/A",
            "Phong": "N/A",
            "Toalet": "N/A",
            "Thong Tin": "N/A",
            "Dia Chi": "N/A",
            "Thong Tin Chi Tiet": "N/A"
        }

    # Get the relevant information from the page
    title = get_element_text(local_driver, By.CLASS_NAME, "re__pr-short-description.js__pr-address")
    name_project = get_element_text(local_driver, By.CLASS_NAME, "re__project-title")
    thontinch = get_element_text(local_driver, By.CLASS_NAME, "re__long-text")

    # Get additional information
    try:
        thongtin = local_driver.find_elements(By.CLASS_NAME, "re__pr-specs-content-item-value")
        dientich = thongtin[0].text if len(thongtin) > 0 else "N/A"
        gia = thongtin[1].text if len(thongtin) > 1 else "N/A"
        phong = thongtin[2].text if len(thongtin) > 2 else "N/A"
        toalet = thongtin[3].text if len(thongtin) > 3 else "N/A"
        thontin = thongtin[4].text if len(thongtin) > 4 else "N/A"
    except:
        dientich = "N/A"
        gia = "N/A"
        phong = "N/A"
        toalet = "N/A"
        thontin = "N/A"

    # Get district information
    try:
        qian = local_driver.find_element(By.CLASS_NAME, "re__breadcrumb.js__breadcrumb.js__ob-breadcrumb")
        diachi = qian.find_elements(By.TAG_NAME, "a")[2].text
    except:
        diachi = "N/A"

    # Close the local driver
    local_driver.quit()

    # Return the collected information
    return {
        "Title": title,
        "Name Project": name_project,
        "Dien Tich": dientich,
        "Gia": gia,
        "Phong": phong,
        "Toalet": toalet,
        "Thong Tin": thontin,
        "Dia Chi": diachi,
        "Thong Tin Chi Tiet": thontinch
    }

# Use ThreadPoolExecutor to speed up crawling
data = []
with ThreadPoolExecutor(max_workers=5) as executor:
    data = list(executor.map(get_element, list_href))

# Print the collected data
print(data)

# Print the total number of records collected
print(len(data))

# Close the main driver
driver.quit()