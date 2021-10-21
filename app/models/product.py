from flask import current_app as app


class Product:
    def __init__(self, id, name, price, description, image_file, available):
        self.id = id
        self.name = name
        self.cat_name = cat_name
        self.price = price
        self.description = description
        self.image_file = image_file
        self.available = available

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]
