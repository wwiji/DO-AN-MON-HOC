import json
import pandas as pd
import re

class clear_data:
    translation = {
        "Title": "Title",
        "Name_project": "Project Name",
        "Diện tích": "Area",
        "Mức giá": "Price",
        "Số phòng ngủ": "Bedrooms",
        "Số toilet": "Bathrooms",
        "Pháp lý": "Legal",
        "Nội thất": "Furniture",
        "Hướng nhà": "House Direction",
        "Hướng ban công": "Balcony Direction"
    }

    # Danh sách chuyển đổi giá trị
    list_convert = ["Diện tích", "Mức giá", "Số phòng ngủ", "Số toilet"]

    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.data = []
        self.t_data = []

    def load_data(self):
        with open(self.input, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    def convert_to_float(self, value):
        value = re.sub(r'[^\d.,]', '', value)
        value = value.replace(',', '.')
        try:
            return float(value)
        except ValueError:
            return value

    def t_entry(self, entry):
        transformed_entry = {
            self.translation["Title"]: entry.get("Title", "N/A"),
            self.translation["Name_project"]: entry.get("Name_project", "N/A")
        }

        # Tách "Quận" từ "Title" (phần tử đầu tiên sau dấu phẩy)
        title = entry.get("Title", "N/A")
        district = title.split(",")[-2].strip() if len(title.split(",")) > 1 else "N/A"
        transformed_entry["District"] = district

        # Chuyển đổi các Specifications
        for spec in entry.get("Specifications", []):
            title = spec['title']
            value = spec['value']
            # Chuyển tiêu đề sang tiếng Anh
            title_in_english = self.translation.get(title, title)
            # Chuyển đổi thành số thực nếu tiêu đề nằm trong danh sách list_convert
            if title in self.list_convert:
                transformed_entry[title_in_english] = self.convert_to_float(value)
            else:
                transformed_entry[title_in_english] = value

        return transformed_entry

    def tr_data(self):
        self.t_data = [self.t_entry(entry) for entry in self.data]

    def save_data(self):
        df = pd.DataFrame(self.t_data)
        df.to_json(self.output, orient='records', force_ascii=False, indent=4)

    def process(self):
        self.load_data()
        self.tr_data()
        self.save_data()

