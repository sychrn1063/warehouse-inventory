from warehouse import Warehouse
from catalog import Catalog
from product import Product
import asyncio
import sys

def checkValidNum(val):
    if val.isnumeric():
        return int(val)
    else:
        return None

async def addProduct(inputStr, catalog):
    splitStr = inputStr.split("\"")
    # Check valid command
    if len(splitStr) != 3:
        print("COMMAND IS NOT VALID. PLEASE ENTER A VALID COMMAND.")
        return

    productName = splitStr[1]
    sku = splitStr[-1].strip()

    catalog.addToCatalog(sku, productName)
    return


async def addWarehouse(inputStr, warehouses):
    splitStr = inputStr.split(" ")
    # Check valid command
    if len(splitStr) < 3:
        print("COMMAND IS NOT VALID. PLEASE ENTER A VALID COMMAND.")
        return

    wNum = checkValidNum(splitStr[2])
    if not wNum:
        print("COMMAND IS NOT VALID. PLEASE ENTER A VALID COMMAND.")
        return

    if wNum in warehouses:
        print("WAREHOUSE #" + str(wNum) + " ALREADY EXISTS")
        return

    # Check if stock limit quantified
    if len(splitStr) == 3:
        # No stock limit
        wh = Warehouse(wNum, -1)
    elif len(splitStr) == 4:
        # Stock limit exists
        limit = checkValidNum(splitStr[-1])
        if not limit:
            print("COMMAND IS NOT VALID. PLEASE ENTER A VALID COMMAND.")
            return

        wh = Warehouse(wNum, limit)
    warehouses[wNum] = wh
    return

def getValidStockQty(wh, inputQty):
    # Infinite stock limit
    if wh.stockLimit == -1:
        return inputQty

    if wh.size + inputQty <= wh.stockLimit:
        return inputQty
    elif wh.size == wh.stockLimit:
        return 0
    else:
        return wh.stockLimit - wh.size


async def stock(inputStr, warehouses, catalog):
    splitStr = inputStr.split(" ")
    # Check valid command
    if len(splitStr) < 4:
        print("COMMAND IS NOT VALID. PLEASE ENTER A VALID COMMAND")
        return

    sku = splitStr[1]
    wNum = checkValidNum(splitStr[2])
    if not wNum:
        print("COMMAND IS NOT VALID. PLEASE ENTER A VALID COMMAND.")
        return
    qty = checkValidNum(splitStr[-1])
    if not qty:
        print("COMMAND IS NOT VALID. PLEASE ENTER A VALID COMMAND.")
        return

    # Check if sku exists in catalog
    if not catalog.checkProductExists(sku):
        print("STOCK ERROR: PRODUCT with SKU " + sku + " DOES NOT EXIST IN CATALOG")
        return
    # Check if warehouse exists
    if wNum not in warehouses:
        print("STOCK ERROR: WAREHOUSE #" + str(wNum) + " DOES NOT EXIST")
        return
    # Check if qty is valid value
    if qty <= 0:
        print("STOCK ERROR: STOCK QUANTITY MUST BE GREATER THAN 0")
        return

    wh = warehouses[wNum]
    inputQty = getValidStockQty(wh, qty)
    if inputQty == 0:
        print("STOCK ERROR: WAREHOUSE #" + str(wNum) + " IS ALREADY FULL")
        return

    # Product already in warehouse (add qty)
    if wh.checkProductInWH(sku):
        wh.addQuantity(sku, inputQty)
    else:
        # New product is being stocked in warehouse
        newProduct = Product(sku, catalog.getProductName(sku), inputQty)
        wh.addNewProduct(sku, newProduct)

def getValidUnstockQty(wh, sku, inputQty):
    if inputQty > wh.storage[sku].qty:
        return wh.storage[sku].qty
    else:
        return inputQty


async def unstock(inputStr, warehouses, catalog):
    splitStr = inputStr.split(" ")
    # Check valid command
    if len(splitStr) < 4:
        print("COMMAND IS NOT VALID. PLEASE ENTER A VALID COMMAND.")
        return

    sku = splitStr[1]
    wNum = checkValidNum(splitStr[2])
    if not wNum:
        print("COMMAND IS NOT VALID. PLEASE ENTER A VALID COMMAND.")
        return
    qty = checkValidNum(splitStr[-1])
    if not qty:
        print("COMMAND IS NOT VALID. PLEASE ENTER A VALID COMMAND.")
        return

    # Check if sku exists in catalog
    if not catalog.checkProductExists(sku):
        print("UNSTOCK ERROR: PRODUCT WITH SKU " + sku + " DOES NOT EXIST IN CATALOG")
        return
    # Check if warehouse exists
    if wNum not in warehouses:
        print("UNSTOCK ERROR: WAREHOUSE #" + str(wNum) + " DOES NOT EXIST")
        return
    # Check if qty is valid value
    if qty <= 0:
        print("UNSTOCK ERROR: UNSTOCK QUANTITY MUST BE GREATER THAN 0")
        return
    # Check product is stored in warehouse
    wh = warehouses[wNum]
    if not wh.checkProductInWH(sku):
        print("UNSTOCK ERROR: PRODUCT TO UNSTOCK DOES NOT EXIST IN WAREHOUSE #" + str(wNum))
        return

    inputQty = getValidUnstockQty(wh, sku, qty)
    if inputQty == 0:
        # Can't unstock
        print("UNSTOCK ERROR: PRODUCT ALREADY HAS QUANTITY OF 0")
        return
    else:
        wh.subQuantity(sku, inputQty)

async def listWarehouses(warehouses):
    print("WAREHOUSES")
    for key in warehouses:
        print(key)


async def updateLog(f, commandCount, commandLog, inputStr):
    if inputStr.lower() == "quit":
        return

    commandCount += 1
    commandLog += inputStr + "\n"
    if commandCount % 2 == 0:
        f.write(commandLog)
        commandCount = 0
        commandLog = ""
        f.write("-\n")

    return commandCount, commandLog


def main():
    print("SESSION STARTED")
    print("ENTER COMMAND \"QUIT\" to EXIT PROGRAM")
    print("--------------------------------------")

    f = open("command_log.txt", "w")

    commandCount = 0
    commandLog = ""

    warehouses = {}
    catalog = Catalog()

    while True:
        inputStr = input('Please enter command: ')

        # Process command
        splitStr = inputStr.split(" ")

        if splitStr[0].lower() == "add":
            # Check valid command
            if len(splitStr) < 2:
                print("COMMAND IS NOT VALID. PLEASE ENTER A VALID COMMAND.")
                continue

            if splitStr[1].lower() == "product":
                # ADD PRODUCT
                funcToRun = addProduct(inputStr, catalog)
            elif splitStr[1].lower() == "warehouse":
                # ADD WAREHOUSE
                funcToRun = addWarehouse(inputStr, warehouses)
                # check if updated properly
            else:
                print("COMMAND IS NOT VALID. PLEASE ENTER A VALID COMMAND.")
                continue

        elif splitStr[0].lower() == "stock":
            # STOCK
            funcToRun = stock(inputStr, warehouses, catalog)
        elif splitStr[0].lower() == "unstock":
            # UNSTOCK
            funcToRun = unstock(inputStr, warehouses, catalog)
        elif splitStr[0].lower() == "list":
            # Check valid command
            if len(splitStr) < 2:
                print("COMMAND IS NOT VALID. PLEASE ENTER A VALID COMMAND.")
                continue

            if splitStr[1].lower() == "products":
                # LIST PRODUCTS
                funcToRun = catalog.listProducts()
            elif splitStr[1].lower() == "warehouses":
                # LIST WAREHOUSES
                funcToRun = listWarehouses(warehouses)
            elif splitStr[1].lower() == "warehouse":
                # Check valid command
                if len(splitStr) < 3:
                    print("COMMAND IS NOT VALID. PLEASE ENTER A VALID COMMAND.")
                    continue

                # LIST WAREHOUSE
                wNum = int(splitStr[-1])
                if wNum not in warehouses:
                    print("LIST ERROR: WAREHOUSE # " + str(wNum) + " DOES NOT EXIST")
                    continue
                else:
                    funcToRun = warehouses[wNum].listWarehouse()
            else:
                print("COMMAND IS NOT VALID. PLEASE ENTER A VALID COMMAND.")
                continue
        elif splitStr[0].lower() == 'quit':
            sys.exit()
        else:
            print("COMMAND IS NOT VALID. PLEASE ENTER A VALID COMMAND.")
            continue

        loop = asyncio.get_event_loop()
        temp = loop.run_until_complete(asyncio.gather(funcToRun, updateLog(f, commandCount, commandLog, inputStr)))

        commandCount, commandLog = temp[1]


if __name__ == "__main__":
    main()

# Have input checking system
# Error messages
# Check edge cases
# Status messages?
# get rid of all leading and trailing whitespaces (sku)

