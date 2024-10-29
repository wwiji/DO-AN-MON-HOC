import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the driver
driver = webdriver.Chrome()
url = "https://batdongsan.com.vn/ban-can-ho-chung-cu-tp-hcm"
driver.get(url)

# Get list of links from the main page
list_href = []
elements = driver.find_elements(By.CLASS_NAME, "js__product-link-for-product-id")
for element in elements:
    list_href.append(element.get_attribute("href"))

def get_element_text(driver, by, value):
    try:
        return driver.find_element(by, value).text
    except:
        return "N/A"

def get_element(link):
    driver.get(link)
    time.sleep(3)

    # Get the relevant information from the page
    title = get_element_text(driver, By.CLASS_NAME, "re__pr-short-description.js__pr-address")
    name_project = get_element_text(driver, By.CLASS_NAME, "re__project-title")
    city = get_element_text(driver, By.CLASS_NAME, "re__long-text")

    # Get additional information
    try:
        thongtin = driver.find_elements(By.CLASS_NAME, "re__pr-specs-content-item-value")
        gia = thongtin[0].text if len(thongtin) > 0 else "N/A"
        phong = thongtin[1].text if len(thongtin) > 1 else "N/A"
        toilet = thongtin[2].text if len(thongtin) > 2 else "N/A"
        hopdong = thongtin[3].text if len(thongtin) > 3 else "N/A"
        noithat = thongtin[4].text if len(thongtin) > 4 else "N/A"
    except:
        gia = phong = toilet = hopdong = noithat = "N/A"

    # Get district information
    try:
        qian = driver.find_element(By.CLASS_NAME, "re__breadcrumb.js__breadcrumb.js__ob-breadcrumb")
        diachi = qian.find_elements(By.TAG_NAME, "a")[2].text
    except:
        diachi = "N/A"

    # Return the collected information
    return {
        "title": title,
        "name_project": name_project,
        "city": city,
        "gia": gia,
        "phong": phong,
        "toilet": toilet,
        "hopdong": hopdong,
        "noithat": noithat,
        "diachi": diachi
    }

# Loop through all the links and collect data
data = []
for link in list_href:
    data.append(get_element(link))

# Print the collected data
print(data)

# Close the driver
driver.quit()
