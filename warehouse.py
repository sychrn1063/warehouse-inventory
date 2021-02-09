class Warehouse:
    def __init__(self, num, stockLimit):
        self.storage = {}
        self.num = num
        self.stockLimit = stockLimit
        self.size = 0

    def addNewProduct(self, sku, product):
        self.storage[sku] = product
        self.size += product.qty

    def addQuantity(self, sku, qtyToAdd):
        self.storage[sku].qty += qtyToAdd
        self.size += qtyToAdd

    def subQuantity(self, sku, qtyToSub):
        self.storage[sku].qty -= qtyToSub
        self.size -= qtyToSub

    def checkProductInWH(self, sku):
        return True if sku in self.storage else False

    async def listWarehouse(self):
        print("ITEM NAME | ITEM_SKU | QTY")
        for key in self.storage:
            product = self.storage[key]
            print(product.name + "\t" + product.sku + "\t" + str(product.qty))
