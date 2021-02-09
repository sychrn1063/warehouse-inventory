class Product:
    def __init__(self, sku, name, qty):
        self.sku = sku
        self.name = name
        self.qty = qty

    def addQty(self, qtyToAdd):
        self.qty += qtyToAdd

    def subQty(self, qtyToSub):
        self.qty -= qtyToSub