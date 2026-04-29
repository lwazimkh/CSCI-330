import pymysql.cursors

def main():
    # establish DB connection
    conn = create_connection('MuskieCo')
    if conn is None:
        exit()
    while True: 
        # ask the user what operation they want to perform
        choice = get_user_choice()
    
        # call the method corresponding to that operation
        if choice == 1:
            product_operation(conn)
        elif choice == 2:
            discount_operation(conn)
        elif choice == 3:
            get_store_edit_choice(conn)
        elif choice == 4:
            reports_choice(conn)
        elif choice == 5:
            break
    # close DB connection
    conn.close()

def create_connection(database_name):
    """ 
    Create a connection to the given database 
    Returns:
        conn: Connection object
    """

    try:
        conn = pymysql.connect(
            user='root',
            password='pabloss1', # TODO: add your password here 
            host='127.0.0.1',
            database=database_name) 
            # autocommit = false by default
    except pymysql.Error as err:
        print('Cannot connect to database:', err)
        return None

    return conn

def get_user_choice():
    """ 
    Gets the operation the user wants to perform 
    Returns:
        choice: the number corresponding to the operation
    """

    choice = -1
    while choice < 1 or choice > 3:
        choice = int(input("Welcome to MuskieCo!\n" +
                                "Which task would you like to perform?\n" +
                                "1. Enter/Update/Delete/Search for a Product\n" +
                                "2. Enter/Update/Delete/Search for a Discount\n" +
                                "3. Enter/Update/Delete/Search for a Store\n" +
                                "4. Reports\n" +
                                "5. Exit.\n"
                    ))

    return choice

def get_store_edit_choice(conn):
    choice = -1
    while choice < 1 or choice > 4:
        choice = int(input(
            "How would you like to edit the store?\n"
            "1. Enter store\n"
            "2. Update store\n"
            "3. Delete store\n"
            "4. Search store\n"
        ))
    if choice == 1:
        enter_store(conn)
    elif choice == 2:
        update_store(conn)
    elif choice == 3:
        delete_store(conn)
    elif choice == 4:
        search_store(conn)

def reports_choice(conn):
    choice = -1
    while choice < 1 or choice > 3:
        choice = int(input(
            "Select a report:\n"
            "1. Sales Report\n"
            "2. Store/Product Inventory Report\n"
            "3. Customer Total Purchase Report\n"
        ))
    if choice == 1:
        sales_report(conn)
    elif choice == 2:
        inverntory_report(conn)
    elif choice == 3:
        customer_report(conn)




def read_string(prompt):
    """ 
    Reads a string from the user 
    Returns:
        the string entered
    """
    return input(prompt)

def read_int(prompt):
    """ 
    Reads an int from the user 
    Returns:
        the int entered
    """

    return int(input(prompt))

def read_float(prompt):
    """ 
    Reads a float from the user 
    Returns:
        the float entered
    """
    return float(input(prompt))

def product_operation(conn):
    """
    Product operations 
    """
    choice = -1
    while choice < 1 or choice > 4:
        # Provide the User a choice of what they would like to do with the product, separating options by line
        choice = int(input("What would you like to do with the product:\n" +
                                "1. Enter a Product\n" +
                                "2. Update a Product\n" +
                                "3. Delete a Product\n" +
                                "4. Search for a product\n"
                    ))
    if choice == 1:
        enter_product(conn)
    elif choice == 2:
        update_product(conn)
    elif choice == 3:
        delete_product(conn)
    elif choice == 4:
        search_product(conn)

def enter_product(conn):
    """
    Entering a product
    Uses a transaction for consistency, and changes rollback if the insertion fails
    """
    Product_id = read_int("Product ID: ")
    name = read_string("Product Name: ")
    buy_price = read_float("Buy Price: ")
    sell_price = read_float("Sell Price: ")
    inventory_id = read_int("Inventory ID: ")
    # mySQL query that Inserts the read input for the new product 
    sql_enter_product = "INSERT INTO Product (ProductID, Name, buy_price, sell_price, InventoryID) VALUES (%s, %s, %s, %s, %s)"

    try: 
        # begin transaction
        conn.begin()
        cur = conn.cursor()
        lines_affected = cur.execute(sql_enter_product, (Product_id, name, buy_price, sell_price, inventory_id))

        if lines_affected != 1:
            raise Exception("Insert into invoice line did not affect just one line")
        # commit transaction
        conn.commit()
        print("Product entered.")

    except Exception as err: 
        print("Product wasn't entered:", err)
        # rollback if error occurs
        conn.rollback()

def update_product(conn):
    """
    Updating a product already in the database
    User selects which product they would like to update
    and what specifically they would like to update in the product
    """
    product_id = read_int("Product you would like to update: ")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Product WHERE ProductID = %s", (product_id,))
    if not cur.fetchone():
        print("Couldn't find product")
        return
    # prompt the user what they would like to update
    print("What would you like to update?")
    print("1. Name")
    print("2. Buy Price")
    print("3. Sell Price")
    print("4. Inventory ID")
    choice = read_int("Enter which you would like to update: ")
    # depending on choice made, update the product
    if choice == 1:
        value = read_string("New Product Name: ")
        update_sql = "UPDATE Product SET Name = %s WHERE ProductID = %s"
        params = (value, product_id)
    elif choice == 2:
        value = read_float("New Buy Price: ")
        update_sql = "UPDATE Product SET buy_price = %s WHERE ProductID = %s"
        params = (value, product_id)
    elif choice == 3:
        value = read_float("New Sell Price: ")
        update_sql = "UPDATE Product SET sell_price = %s WHERE ProductID = %s"
        params = (value, product_id)
    elif choice == 4:
        value = read_int("New Inventory ID: ")
        update_sql = "UPDATE Product SET InventoryID = %s WHERE ProductID = %s"
        params = (value, product_id)
    else:
        print("Not one of the choices.")
        return
    try:
        # begin transaction
        conn.begin()
        cur = conn.cursor()
        lines_affected = cur.execute(update_sql, params)

        if lines_affected != 1:
            raise Exception("Product update didn't affect exactly one row")
        # commit transaction
        conn.commit()
        print("Product Updated.")

    except Exception as err:
        print("Product wasn't updated", err)
        # rollback transaction if any error occurs
        conn.rollback()

def delete_product(conn):
    """
    Delete a product from the database that user selects
    """
    # prompt user to select the product to delete
    product_id = read_int("Product ID to delete: ")
    # sql query that deleted product selected
    sql_delete_product = "DELETE FROM Product WHERE ProductID = %s"

    try:
        # begin transaction
        conn.begin()
        cur = conn.cursor()
        lines_affected = cur.execute(sql_delete_product, (product_id,))

        if lines_affected != 1:
            raise Exception("Insert into invoice line did not affect just one line")
        # commit transaction
        conn.commit()
        print("Product Deleted.")

    except Exception as err:
        print("Product wasn't deleted:", err)
        # rollback transaction if error occurs
        conn.rollback()

def search_product(conn):
    """
    Search for a product by using the ProductID or Name 
    """
    search = input("Search by \n1. ID or \n2. Name \nEnter 1 or 2: ")
    # depending on what user selects, search for product information
    if search == "1":
        product_id = read_int("Product ID: ")
        sql_search = "SELECT * FROM Product WHERE ProductID = %s"
        params = (product_id,)
    else:
        name = read_string("Product name: ")
        sql_search = "SELECT * FROM Product WHERE Name LIKE %s"
        params = (f"%{name}%",)
    try: 
        # begin transaction
        cur = conn.cursor()
        cur.execute(sql_search, params)
        results = cur.fetchall()
        # fetch results and print them by grabbing indices
        if results: 
            print("Product: ")
            for row in results: 
                print(f"ID: {row[0]}, Name: {row[1]}, Buy Price: {row[2]}, Sell Price: {row[3]}, Inventory ID: {row[4]}")
        else:
            print("No Product.")
    # if search fails
    except Exception as err:
        print("Search failed", err)

def discount_operation(conn):
    """
    Discount Operations
    """
    choice = -1
    while choice < 1 or choice > 4:
        choice = int(input("What would you like to do with the Discount:\n" +
                                "1. Enter a Discount\n" +
                                "2. Update a Discount\n" +
                                "3. Delete a Discount\n" +
                                "4. Search for a Discount\n"
                    ))
    if choice == 1:
        enter_discount(conn)
    elif choice == 2:
        update_discount(conn)
    elif choice == 3:
        delete_discount(conn)
    elif choice == 4:
        search_discount(conn)

def enter_discount(conn):
    """
    Enter a Discount
    """
    discount_id = read_int("Enter Discount: ")
    discount_start_date = read_string("Enter Start Date (MM/DD/YYYY): ")
    discount_end_date = read_string("Enter End Date (MM/DD/YYYY): ")
    discount_amount = read_float("Discount Amount: ")

    sql_enter_discount = "INSERT INTO Discount (DiscountID, discount_start_date, discount_end_date, discount_amount) VALUES (%s, %s, %s, %s)"

    try: 
        conn.begin()
        cur = conn.cursor()
        lines_affected = cur.execute(sql_enter_discount, (discount_id, discount_start_date, discount_end_date, discount_amount))

        if lines_affected != 1:
            raise Exception("Discount insertion did not affect exactly one row")
        
        conn.commit()
        print("Discount Entered.")
    except Exception as err:
        print("Discount wasn't entered:", err)
        conn.rollback()

def update_discount(conn):
    discount_id = read_int("Discount ID you would like to update: ")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Discount WHERE DiscountID = %s", (discount_id,))
    if not cur.fetchone():
        print("No Discount Found")
        return
    print("What would you like to update?")
    print("1. Discount Start Date")
    print("2. Discount End Date")
    print("3. Discount Amount")

    choice = read_int("Enter Which you would like to update: ")
    if choice == 1:
        value = read_string("New Start Date (MM/DD/YYYY): ")
        update_sql = "UPDATE Discount SET discount_start_date = %s WHERE DiscountID = %s"
        params = (value, discount_id)
    elif choice == 2:
        value = read_string("New End Date (MM/DD/YYYY): ")
        update_sql = "UPDATE Discount SET discount_end_date = %s WHERE DiscountID = %s"
        params = (value, discount_id)
    elif choice == 3:
        value = read_float("New Discount Amound: ")
        update_sql = "UPDATE Discount SET discount_amount = %s WHERE DiscountID = %s"
        params = (value, discount_id)
    else: 
        print("Not a valid choice.")
        return
    
    try: 
        conn.begin()
        cur = conn.cursor()
        lines_affected = cur.execute(update_sql, params)

        if lines_affected != 1:
            raise Exception("Discount updated didn't affect exactly one row")
        
        conn.commit()
        print("Discount Updated.")
    except Exception as err:
        print("Discount wasn't updated.", err)
        conn.rollback()

def delete_discount(conn):
    """
    Delete a discount
    """

    discount_id = read_int("Discount ID to delete: ")
    sql_delete_discount = "DELETE FROM Discount WHERE DiscountID = %s"

    try: 
        conn.begin()
        cur = conn.cursor()
        lines_affected = cur.execute(sql_delete_discount, (discount_id,))

        if lines_affected != 1:
            raise Exception("Discount deletion did not affect exactly one row")
        conn.commit()
        print("Discount deleted.")
    except Exception as err:
        print("Discount wasn't deleted:", err)
        conn.rollback()

def search_discount(conn):
    """
    Search for a discount by the discount_id
    """
    discount_id = read_int("Discount ID: ")
    sql_search_discount = "SELECT * FROM Discount WHERE DiscountID = %s"

    try:
        cur = conn.cursor()
        cur.execute(sql_search_discount, (discount_id,))
        result = cur.fetchone()

        if result: 
            print("Discount: ")
            print(f"ID: {result[0]}, Start Date: {result[1]}, End Date: {result[2]}, Amount: {result[3]}")
        else: 
            print("Discount not found.")
    except Exception as err:
        print("Search failed:", err)


def enter_store(conn):
    StoreID = read_int("Store ID: ")
    ManagerID = read_int("ManagerID: ")
    store_address = read_string("Address: ")
    phone_number = read_string("Phone Number: ")

    sql = "INSERT INTO Store VALUES (%s, %s, %s, %s)"

    try:
        conn.begin()
        cur = conn.cursor()

        lines = cur.execute(sql, (StoreID, ManagerID, store_address,
                                  phone_number))
        if lines != 1:
            raise Exception("Insert failed")

    except Exception as err:
        print("Store not added:", err)
        conn.rollback()
    else:
        conn.commit()
        print("Store added successfully")


def update_store(conn):
    StoreID = read_int("Store ID: ")
    ManagerID = input("New ManagerID: ")
    store_address = input("New Address: ")
    phone_number = input("New Phone: ")

    updates = []
    values = []

    if ManagerID:
        updates.append("ManagerID = %s")
        values.append(int(ManagerID))
    if store_address:
        updates.append("store_address = %s")
        values.append(store_address)
    if phone_number:
        updates.append("phone_number = %s")
        values.append(phone_number)
    if not updates:
        print("No updates provided")
        return

    sql = f"UPDATE Store SET {', '.join(updates)} WHERE StoreID = %s"
    values.append(StoreID)

    try:
        conn.begin()
        cur = conn.cursor()

        lines = cur.execute(sql, values)
        if lines != 1:
            raise Exception("Update failed")

    except Exception as err:
        print("Update failed:", err)
        conn.rollback()
    else:
        conn.commit()
        print("Store updated successfully")


def delete_store(conn):
    StoreID = read_int("StoreID to delete: ")

    sql = "DELETE FROM Store WHERE StoreID = %s"

    try:
        conn.begin()
        cur = conn.cursor()

        lines = cur.execute(sql, (StoreID,))
        if lines != 1:
            raise Exception("Delete failed")

    except Exception as err:
        print("Delete failed:", err)
        conn.rollback()
    else:
        conn.commit()
        print("Store deleted successfully")


def search_store(conn):
    StoreID = read_int("StoreID to search: ")

    sql = "SELECT * FROM Store WHERE StoreID = %s"

    try:
        cur = conn.cursor()
        cur.execute(sql, (StoreID,))
        result = cur.fetchone()

        if result:
            print("Store Found:", result)
        else:
            print("No store found")

    except Exception as err:
        print("Search failed:", err)


def sales_report(conn):
    start_date = read_string("Start date (YYYY-MM-DD): ")
    end_date = read_string("End date (YYYY-MM-DD): ")

    sql = """
        SELECT SUM(price_total)
        FROM Transaction
        WHERE purchase_date BETWEEN %s AND %s
    """

    try:
        cur = conn.cursor()
        cur.execute(sql, (start_date, end_date))
        result = cur.fetchone()

        total = result[0] if result[0] else 0
        print("Total Sales:", total)

    except Exception as err:
        print("Report failed:", err)


def customer_report(conn):
    customer_id = read_int("CustomerID: ")
    start_date = read_string("Start date (YYYY-MM-DD): ")
    end_date = read_string("End date (YYYY-MM-DD): ")

    sql = """
        SELECT SUM(price_total)
        FROM Transaction
        WHERE CustomerID = %s
        AND purchase_date BETWEEN %s AND %s
    """

    try:
        cur = conn.cursor()
        cur.execute(sql, (customer_id, start_date, end_date))
        result = cur.fetchone()

        total = result[0] if result[0] else 0
        print("Total Customer Purchases:", total)

    except Exception as err:
        print("Report failed:", err)

if __name__ == '__main__':
    main()
