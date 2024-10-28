from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service



def get_all_links(url):

    set_link = set()
    # Mở trình duyệt
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(2)
    # Lấy tất cả các link
    web_elements = driver.find_elements(By.XPATH, '//div[@class="re__srp-paging js__srp-paging"]/div/a')
    for element in web_elements:
        set_link.add(element.get_attribute('href'))
    driver.close()
    return set_link

url = "https://batdongsan.com.vn/ban-can-ho-chung-cu-tp-hcm"
print(get_all_links(url))