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
            customer_operation(conn)
        elif choice == 6:
            staff_operation(conn)
        elif choice == 7:
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
    while choice < 1 or choice > 7:
        choice = int(input("Welcome to MuskieCo!\n" +
                                "Which task would you like to perform?\n" +
                                "1. Enter/Update/Delete/Search for a Product\n" +
                                "2. Enter/Update/Delete/Search for a Discount\n" +
                                "3. Enter/Update/Delete/Search for a Store\n" +
                                "4. Reports\n" +
                                "5. Enter/Update/Delete/Search for a Customer\n" +
                                "6. Enter/Update/Delete/Search for a Staff\n" +
                                "7. Exit.\n"
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
    discount_start_date = read_string("Enter Start Date (YYYY/MM/DD): ")
    discount_end_date = read_string("Enter End Date (YYYY/MM/DD): ")
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
        value = read_string("New Start Date (YYYY/MM/DD): ")
        update_sql = "UPDATE Discount SET discount_start_date = %s WHERE DiscountID = %s"
        params = (value, discount_id)
    elif choice == 2:
        value = read_string("New End Date (YYYY/MM/DD): ")
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


def customer_operation(conn):
    """
    customer operations 
    """
    choice = -1
    while choice < 1 or choice > 4:
        # Provide the User a choice of what they would like to do with the customer, separating options by line
        choice = int(input("What would you like to do with the Customer:\n" +
                                "1. Add New Customer\n" +
								"2. Update Member\n" +
								"3. Delete Customer\n" +
                                "4. Search Customer\n" 
                    ))
    if choice == 1:
        enter_new_customer(conn)
    elif choice == 2:
        update_customer(conn)
    elif choice == 3:
        delete_customer(conn)
    elif choice == 4:
        search_customer(conn)


# CUSTOMER FUNCTIONS
def enter_new_customer(conn):
    """
	Allows to enter a new Customer and Member to the database.
    In result, inserts a row into Customer then a row into Member tables.
	"""
    print("\n--- Enter New Customer ---")
    customer_id = read_int("CustomerID: ")
    first_name = read_string("First name: ")
    last_name  = read_string("Last name: ")
    email = read_string("Email address: ")
    phone  = read_string("Phone number: ")
    home_address  = read_string("Home address: ")
    active_status = read_int("Active status (1 = active, 0 = inactive): ")

    sql_customer = "INSERT INTO Customer (CustomerID) VALUES (%s);"
    sql_member = (
        "INSERT INTO Member "
        "(CustomerID, first_name, last_name, email_address, phone_number, home_address, active_status) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s);"
    )

    try:
        conn.begin()
        cur = conn.cursor()
        cur.execute(sql_customer, (customer_id,))
        cur.execute(sql_member, (
            customer_id, first_name, last_name,
            email, phone, home_address, active_status
        ))
    except Exception as err:
        conn.rollback()
        print(f"  Error: Customer was not added – {err}")
    else:
        conn.commit()
        print(f"  Success! Customer {first_name} {last_name} (ID {customer_id}) has been added.")

# Updating a field of a an existing member
def update_customer(conn):
    """
    Allows to update existing Member's information
    Provides a list of things that can be modified
    """
    print("\n--- Update Customer ---")
    fields = {
        "1": ("first_name",    "First name"),
        "2": ("last_name",     "Last name"),
        "3": ("email_address", "Email address"),
        "4": ("phone_number",  "Phone number"),
        "5": ("home_address",  "Home address"),
        "6": ("active_status", "Active status (1/0)"),
    }

    customer_id = read_int("CustomerID to update: ")

    print("Which field would you like to update?")
    for key, (_, label) in fields.items():
        print(f"  {key}. {label}")

    choice = ""
    while choice not in fields:
        choice = input("Enter the number corresponding to your choice: ").strip()

    column, label = fields[choice]
    new_value = input(f"New {label}: ").strip()

    sql_update = f"UPDATE Member SET {column} = %s WHERE CustomerID = %s;"

    try:
        conn.begin()
        cur = conn.cursor()
        rows = cur.execute(sql_update, (new_value, customer_id))
        if rows == 0:
            raise Exception(f"No customer found with ID {customer_id}.")
    except Exception as err:
        conn.rollback()
        print(f"  Error: Customer was not updated – {err}")
    else:
        conn.commit()
        print(f"  Success! {label} for CustomerID {customer_id} has been updated.")


# Deleting a Customer
# Deletes child rows in order: Transactions → Member → Customer
def delete_customer(conn):
    """
    Allows to remove existing customer and member from the database by their CustomerID
    """
    print("\n--- Delete Customer ---")
    customer_id = read_int("CustomerID to delete: ")

    sql_del_transactions = "DELETE FROM Transactions WHERE CustomerID = %s;"
    sql_del_member       = "DELETE FROM Member WHERE CustomerID = %s;"
    sql_del_customer     = "DELETE FROM Customer WHERE CustomerID = %s;"

    try:
        conn.begin()
        cur = conn.cursor()
        cur.execute(sql_del_transactions, (customer_id,))
        cur.execute(sql_del_member, (customer_id,))          # ← add this line
        rows = cur.execute(sql_del_customer, (customer_id,))
        if rows == 0:
            raise Exception(f"No customer found with ID {customer_id}.")
    except Exception as err:
        conn.rollback()
        print(f"  Error: Customer was not deleted – {err}")
    else:
        conn.commit()
        print(f"  Success! CustomerID {customer_id} and all related records have been removed.")



# Searching a Customer by their ID or Name
def search_customer(conn):
    """
    Allows to search a Customer by their CustomerID and provides their information
    """
    print("\n--- Search Customer ---")
    print("Search by:")
    print("  1. CustomerID")
    print("  2. Name")
 
    choice = ""
    while choice not in ("1", "2"):
        choice = input("Enter 1 or 2: ").strip()
 
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
 
        if choice == "1":
            customer_id = read_int("CustomerID: ")
            cur.execute("SELECT * FROM Member WHERE CustomerID = %s;", (customer_id,))
        else:
            name = read_string("Enter first or last name: ")
            cur.execute(
                "SELECT * FROM Member WHERE first_name LIKE %s OR last_name LIKE %s;",
                (f"%{name}%", f"%{name}%")
            )
 
        results = cur.fetchall()
        if not results:
            print("  No customers found.")
        else:
            print(f"\n  {'ID':<6} {'First':<15} {'Last':<15} {'Email':<30} {'Phone':<15} {'Address':<25} {'Active'}")
            print("  " + "-" * 115)
            for row in results:
                print(
                    f"  {row['CustomerID']:<6} {row['first_name']:<15} {row['last_name']:<15} "
                    f"{row['email_address']:<30} {row['phone_number']:<15} "
                    f"{row['home_address']:<25} {row['active_status']}"
                )
 
    except Exception as err:
        print(f"  Error: Search failed – {err}")
        





def staff_operation(conn):
    """
    staff operations 
    """
    choice = -1
    while choice < 1 or choice > 4:
        # Provide the User a choice of what they would like to do with the staff, separating options by line
        choice = int(input("What would you like to do with the Staff:\n" +
                                "1. Add New Staff\n" +
                                "2. Update Staff\n" +
                                "3. Search Staff\n" +
                                "4. Delete Customer\n" 
                    ))
    if choice == 1:
        enter_staff(conn)
    elif choice == 2:
        update_staff(conn)
    elif choice == 3:
        search_staff(conn)
    elif choice == 4:
        delete_staff(conn)

# STAFF FUNCTIONS

# Add New Staff
def enter_staff(conn):
    """
    Allows to add new staff
    In result, inserts a row into Staff table
    """
    print("\n--- Enter New Staff ---")
    staff_id           = read_int("StaffID: ")
    first_name         = read_string("First name: ")
    last_name          = read_string("Last name: ")
    age                = read_int("Age: ")
    home_address       = read_string("Home address: ")
    job_title          = read_string("Job title: ")
    phone_number       = read_string("Phone number: ")
    email              = read_string("Email (name@domain.com): ")
    time_of_employment = read_string("Start date (YYYY-MM-DD): ")
    store_id           = read_int("StoreID: ")

    sql_insert = (
        "INSERT INTO Staff "
        "(StaffID, first_name, last_name, age, home_address, job_title, "
        "phone_number, email, time_of_employment, StoreID) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    )
 
    try:
        conn.begin()
        cur = conn.cursor()
        rows = cur.execute(sql_insert, (staff_id, first_name, last_name, age,
                                        home_address, job_title, phone_number,
                                        email, time_of_employment, store_id))
        if rows != 1:
            raise Exception("Insert did not affect exactly one row.")
    except Exception as err:
        conn.rollback()
        print(f"  Error: Staff member was not added – {err}")
    else:
        conn.commit()
        print(f"  Success! {first_name} {last_name} (StaffID {staff_id}) has been added.")
        

# Update Staff Fields
def update_staff(conn):
    """
    Allows to update existing staff's information
    Provides a list of fields that can be modified
    """
    print("\n--- Update Staff ---")
 
    fields = {
        "1": ("first_name",         "First name"),
        "2": ("last_name",          "Last name"),
        "3": ("age",                "Age"),
        "4": ("home_address",       "Home address"),
        "5": ("job_title",          "Job title"),
        "6": ("phone_number",       "Phone number"),
        "7": ("email",              "Email"),
        "8": ("time_of_employment", "Start date (YYYY-MM-DD)"),
        "9": ("storeID",            "StoreID"),
    }
 
    staff_id = read_int("StaffID to update: ")
 
    print("Which field would you like to update?")
    for key, (_, label) in fields.items():
        print(f"  {key}. {label}")
 
    choice = ""
    while choice not in fields:
        choice = input("Enter the number corresponding to your choice: ").strip()
 
    column, label = fields[choice]
    new_value = input(f"New {label}: ").strip()
 
    sql_update = f"UPDATE Staff SET {column} = %s WHERE StaffID = %s;"
 
    try:
        conn.begin()
        cur = conn.cursor()
        rows = cur.execute(sql_update, (new_value, staff_id))
        if rows == 0:
            raise Exception(f"No staff member found with ID {staff_id}.")
    except Exception as err:
        conn.rollback()
        print(f"  Error: Staff was not updated – {err}")
    else:
        conn.commit()
        print(f"  Success! {label} for StaffID {staff_id} has been updated.")
        

# Search for Staff by their ID or Name
def search_staff(conn):
    """
    Allows to search existing staff by their StaffID
    In result, shows their information
    """
    print("\n--- Search Staff ---")
    print("Search by:")
    print("  1. StaffID")
    print("  2. Name")
 
    choice = ""
    while choice not in ("1", "2"):
        choice = input("Enter 1 or 2: ").strip()
 
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
 
        if choice == "1":
            staff_id = read_int("StaffID: ")
            cur.execute("SELECT * FROM Staff WHERE StaffID = %s;", (staff_id,))
        else:
            name = read_string("Enter first or last name: ")
            cur.execute(
                "SELECT * FROM Staff WHERE first_name LIKE %s OR last_name LIKE %s;",
                (f"%{name}%", f"%{name}%")
            )
 
        results = cur.fetchall()
        if not results:
            print("  No staff members found.")
        else:
            print(f"\n  {'ID':<6} {'First':<12} {'Last':<12} {'Age':<5} {'Title':<15} {'Phone':<15} {'Email':<28} {'Store'}")
            print("  " + "-" * 100)
            for row in results:
                print(
                    f"  {row['StaffID']:<6} {row['first_name']:<12} {row['last_name']:<12} "
                    f"{row['age']:<5} {row['job_title']:<15} {row['phone_number']:<15} "
                    f"{row['email']:<28} {row['StoreID']}"
                )
 
    except Exception as err:
        print(f"  Error: Search failed – {err}")
        

# Delete Staff
# Deletes from Transactions first to respect FK constraints, then Staff.
def delete_staff(conn):
    """
    Deletes existing staff by their StaffID
    """
    print("\n--- Delete Staff ---")
    staff_id = read_int("StaffID to delete: ")
 
    sql_del_transactions = "DELETE FROM Transactions WHERE StaffID = %s;"
    sql_del_staff        = "DELETE FROM Staff WHERE StaffID = %s;"
 
    try:
        conn.begin()
        cur = conn.cursor()
        cur.execute(sql_del_transactions, (staff_id,))
        rows = cur.execute(sql_del_staff, (staff_id,))
        if rows == 0:
            raise Exception(f"No staff member found with ID {staff_id}.")
    except Exception as err:
        conn.rollback()
        print(f"  Error: Staff was not deleted – {err}")
    else:
        conn.commit()
        print(f"  Success! StaffID {staff_id} and their transaction records have been removed.")
 

if __name__ == '__main__':
    main()
