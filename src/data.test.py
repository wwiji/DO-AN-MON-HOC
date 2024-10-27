import time
import pandas as pd
import os
import json

from openpyxl import Workbook
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("import lib oke!")

path_local = './src'

driver_path = Path(f"{path_local}/msedgedriver.exe").resolve()
if not driver_path.is_file():
    raise FileNotFoundError(f"Không tìm thấy msedgedriver tại đường dẫn: {driver_path}")
edge_service = Service(str(driver_path)) 
driver = webdriver.Edge(service=edge_service)

url = "https://batdongsan.com.vn/du-an-can-ho-chung-cu-tp-hcm"
driver.get(url)

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".re__project-main-container.re__clearfix")))

def get_element_text(element, css_selector, default="N/A"):
    try:
        return element.find_element(By.CSS_SELECTOR, css_selector).text.strip()
    except:
        return default

def save_content(write_header=False):
    project_list = []
    projects = driver.find_elements(By.CSS_SELECTOR, "div.re__prj-card-info-content")
    
    for project in projects:
        name = get_element_text(project, "h3.re__prj-card-title")
        area = get_element_text(project, "span.re__prj-card-config-value")
        apartment = get_element_text(project, "span.re__prj-card-config-value span")
        location = get_element_text(project, "div.re__prj-card-location")
        description = get_element_text(project, "div.re__prj-card-summary")
        company = get_element_text(project, "div.re__prj-card-contact-avatar.re__avatar-full-max-width span.re__span-full-max-width")

        project_list.append({
            "Tên dự án": name,
            "Diện tích": area,
            "Số căn hộ": apartment,
            "Vị trí": location,
            "Mô tả": description,
            "Tên công ty": company
        })

    df = pd.DataFrame(project_list)
    print(df)

    # kiểm tra file có tồn tại hay không 
    patch_project_execel = f"{path_local}/projectExcel.xlsx"
    file_exists = os.path.isfile(patch_project_execel)
    
    # tạo file nếu file không tồn tại 
    if not file_exists:
        wb = Workbook()
        wb.save(patch_project_execel)

    with pd.ExcelWriter(patch_project_execel, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, index=False, header=write_header, startrow=writer.sheets['Sheet'].max_row if 'Sheet' in writer.sheets else 0)
    
    with open(f"{path_local}/projectData.json", "a", encoding="utf-8") as jsonfile:
        json.dump(project_list, jsonfile, ensure_ascii=False, indent=4)



pagination_group = driver.find_element(By.CLASS_NAME, "re__pagination-group")
pagination_numbers = pagination_group.find_elements(By.TAG_NAME, "a")
pid_value = pagination_numbers[-2].get_attribute("pid")

if pid_value is not None:
    last_page_number = int(pid_value)
else:
    last_page_number = 0

for page_number in range(1, last_page_number):
    # lưu nội dung của trang hiện tại
    save_content(write_header=(page_number == 1))
    
    # kiểm tra xem có trang kế tiếp hay không 
    try:
        next_page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".re__pagination-icon .re__icon-chevron-right"))
        )
        next_page.click()
        print(f"Page {page_number}")
        time.sleep(3)  # chờ 3 giây để trang load xong
    except Exception as e:
        print(f"Error on page {page_number}: {e}")
        break