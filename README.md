# warehouse-inventory
Rooms To Go Take Home Assessment

## Running the Program
Run `main.py` to start the program. Once the program starts to run, enter one of the 7 commands listed below with the correct format:

**ADD PRODUCT** *"PRODUCT NAME" SKU*

**ADD WAREHOUSE** *WAREHOUSE# [STOCK_LIMIT]*

**STOCK** *SKU WAREHOUSE# QTY* 

**UNSTOCK** *SKU WAREHOUSE# QTY*

**LIST PRODUCTS** 

**LIST WAREHOUSES**

**LIST WAREHOUSE** *WAREHOUSE#*

Check `command_log.txt` to view command history. 
Enter command "**QUIT**" to exit the program. 

## Notes
* A valid warehouse number must be greater than 0.
* A valid SKU must only consist of alphanumerics and "-" with no whitespaces.
* Command history only records command logs in batches of 2. 
* Stock and unstock quantities must be greater than 0.
* Commands are not case-sensitive.