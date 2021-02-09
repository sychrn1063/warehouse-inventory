class Catalog:
    def __init__(self):
        self.products = {}

    def addToCatalog(self, sku, name):
        if self.checkProductExists(sku):
            print("ERROR ADDING PRODUCT: PRODUCT WITH SKU " + sku + " ALREADY EXISTS")
            return
        else:
            self.products[sku] = name
        return

    def checkProductExists(self, sku):
        return True if sku in self.products else False

    def getProductName(self, sku):
        return "" if sku not in self.products else self.products[sku]

    async def listProducts(self):
        for key in self.products:
            print(self.products[key] + " " + key)

