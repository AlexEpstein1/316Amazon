from flask import current_app as app

class Seller:
    def __init__(self, id, name, price, cat_name, description, image_file, available):
        self.id = id
        self.name = name
        self.cat_name = cat_name
        self.price = price
        self.description = description
        self.image_file = image_file
        self.available = available