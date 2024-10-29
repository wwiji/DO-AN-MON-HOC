import time
from pathlib import Path

from matplotlib.pyplot import title
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


driver = webdriver.Chrome()
url = ("https://batdongsan.com.vn/cho-thue-can-ho-chung-cu-tp-hcm/p{}")

list_href = []
for i in range(2, 10):
    driver.get(url.format(i))
    time.sleep(2)
    elements = driver.find_elements(By.CLASS_NAME,"js__product-link-for-product-id")
    for element in elements:
        list_href.append(element.get_attribute("href"))

def get_element_text(by, value):
    try:
        return driver.find_element(by, value).text
    except:
        return "N/A"

def get_element(link):
    driver.get(link)
    time.sleep(3)

    title = get_element_text(By.CLASS_NAME, "re__pr-short-description js__pr-address")
    name_project = get_element_text(By.CLASS_NAME, "re__project-title")
    city = get_element_text(By.CLASS_NAME, "re__long-text")

    # Thông tin
    arena = get_element_text(By.CLASS_NAME, "re__pr-specs-content-item-value")
    gia = get_element_text(By.CLASS_NAME, "re__pr-specs-content-item-value")
    phong = get_element_text(By.CLASS_NAME, "re__pr-specs-content-item-value")
    toilet = get_element_text(By.CLASS_NAME, "re__pr-specs-content-item-value")
    hopdong = get_element_text(By.CLASS_NAME, "re__pr-specs-content-item-value")
    noithat = get_element_text(By.CLASS_NAME, "re__pr-specs-content-item-value")

    # Mô tả
    return {
        "title": title,
        "name_project": name_project,
        "city": city,
        "arena": arena,
        "gia": gia,
        "phong": phong,
        "toilet": toilet,
        "hopdong": hopdong,
        "noithat": noithat
    }
