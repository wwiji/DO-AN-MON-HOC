from scr.MongoDB import MongoDB

class queries(MongoDB):
    def count_ap_district(self):
        pipeline = [
            {"$group": {"_id": "$District", "apartment_count": {"$sum": 1}}}
        ]
        return list(self.collection.aggregate(pipeline))

    def count_projects(self):
        return len(self.collection.distinct("Project Name"))

    def avr_price_district(self):
        pipeline = [
            {"$group": {"_id": "$District", "average_price": {"$avg": "$Price"}}}
        ]
        return list(self.collection.aggregate(pipeline))

    def sort_avr_price_district(self):
        pipeline = [
            {"$group": {"_id": "$District", "average_price": {"$avg": "$Price"}}},
            {"$sort": {"average_price": 1}}
        ]
        return list(self.collection.aggregate(pipeline))

    def sort_area_district(self):
        pipeline = [
            {"$group": {"_id": "$District", "average_area": {"$avg": "$Area"}}},
            {"$sort": {"average_area": 1}}
        ]
        return list(self.collection.aggregate(pipeline))

    def min_price_district(self):
        pipeline = [
            {"$sort": {"Price": 1}},
            {"$group": {"_id": "$District", "min_price_info": {"$first": "$$ROOT"}}}
        ]
        return list(self.collection.aggregate(pipeline))

    def max_price_district(self):
        pipeline = [
            {"$sort": {"Price": -1}},
            {"$group": {"_id": "$District", "max_price_info": {"$first": "$$ROOT"}}}
        ]
        return list(self.collection.aggregate(pipeline))

    def count_ap_balcony(self):
        return self.collection.count_documents({"Balcony Direction": {"$exists": True, "$ne": None}})

    def sort_price_bedrooms(self):
        return list(self.collection.find().sort("Bedrooms", 1))

    def sort_price_bathrooms(self):
        return list(self.collection.find().sort("Bathrooms", 1))

    def sort_price_area(self):
        return list(self.collection.find().sort("Area", 1))

    def sort_price_bedrooms_and_bathrooms(self):
        return list(self.collection.find().sort([("Bedrooms", 1), ("Bathrooms", 1)]))

    def sort_price_bedrooms_and_area(self):
        return list(self.collection.find().sort([("Bedrooms", 1), ("Area", 1)]))

    def print_q(self):
        print("Số căn hộ theo quận:", self.count_ap_district())
        print("Số dự án:", self.count_projects())
        print("Giá trung bình theo quận:", self.avr_price_district())
        print("Giá trung bình theo quận (sắp xếp):", self.sort_avr_price_district())
        print("Diện tích trung bình theo quận (sắp xếp):", self.sort_area_district())
        print("Giá thấp nhất theo quận:", self.min_price_district())
        print("Giá cao nhất theo quận:", self.max_price_district())
        print("Số căn hộ có ban công:", self.count_ap_balcony())
        print("Sắp xếp theo số phòng ngủ:", self.sort_price_bedrooms())
        print("Sắp xếp theo số toilet:", self.sort_price_bathrooms())
        print("Sắp xếp theo diện tích:", self.sort_price_area())
        print("Sắp xếp theo số phòng ngủ và số toilet:", self.sort_price_bedrooms_and_bathrooms())
        print("Sắp xếp theo số phòng ngủ và diện tích:", self.sort_price_bedrooms_and_area())