class Product:
    def __init__(self, id, name, price, category, stock, description=""):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.stock = stock
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "stock": self.stock,
            "description": self.description
        }