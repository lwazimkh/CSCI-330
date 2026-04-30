### CSCI-335
Database Project
MuskieCo


## Nicolas Salvador
- Implemented Product and Discount operations
- Transaction management on database operations to ensure ACID properties. Each transation uses conn.begin() to start the transaction, conn.commit() to commit the transaction, and then conn.rollback() to undo transactions if it were to fail in and erach the Exception. 
# Product Operations
1. Enter Product
- Enter product details to be added to Product table.
- Input : ProductID, name, buy_price, sell_price
- Output : Confirmed Enter
2. Update Product
- Change specific Product details that is selected
- Input : ProductID, fields that were updated
- Output : Confirmation of update
3. Delete Product
- Remove product selected by user
- Input : ProductID
- Output : Confirmation of deletion
4. Search Product
- Find a specific products details
- Input : ProductID and Name
- Output : Product details
  
## Discount Operations
1. Enter Discount
- Enter Discount details to be added to Discount table
- Input : DiscountID, dicount_start_date, discount_end_date, discount_amount
- Output : Confirmation of it being entered
2. Update Discount
- Update specific field of discount
- Input : discountID
- Output : Confirmed update
3. Delete Discount
- Remove Discount selected by user
- Input : dicountID
- Output : Confirmed deletion of discount
4. Search Discount
- Find specific discount details
- Input : discountID
- Output : Discount Details

## Colin Toghill
- Implemented stores and reports
- Each entity has a dedicated set of functions that use similar transaction management as above.

## Store Operations
1. Operation: Enter Store 
- Input: StoreID, ManagerID, store_address, phone_number 
- Output: Confirmation 
2. Operation: Update Store 
- Input: StoreID, Fields that were updated 
- Output: Confirmation 
3. Operation: Delete Store 
- Input: StoreID 
- Output: Confirmation 
4. Operation: Search Store 
- Input: StoreID 
- Output: Store details

## Reports
1.  Operation: Sales Report 
- Input: date_range  
- Output: total sales (price_total summed from give range of dates) 
2.  Operation: Store/Product Inventory Report 
- Input: StoreID, ProductID 
- Output: All inventory records from that store or inventory from all stores of a 
specific product 
3.  Operation: Customer Total Purchase Report 
- Input: CustomerID, date_range 
- Output: Total purchase amount

## Nurbol Kanatbek uulu
- Implemented Customer and Staff operations
- Each operation is divided into seperated functions

## Customer Operations
1. Enter New Customer
- Enter Customer details to be added to Customer table
- Input: CurstomerID, first_name, last_name, email, phone, home_address, active_status
- Output: Confirmation
3. Update Existing Customer
- Change specific field of a Customer
- Input: CustomerID, then new changes
- Output: Confirmation
4. Search Customer
- Find specific customer
- Input: CustomerID
- Output: Customer Information
5. Delete Customer
- Delete specific customer
- Input: CustomerID
- Output: Confirmed deletion of customer

## Staff Operations
1. Enter New Staff
- Enter Customer details to be added to Customer table
- Input: StaffID, first_name, last_name, age, home_address, job_title, phone, email, time_of_employment, StoreID
- Output: Confirmation
3. Update Existing Staff
- Change specific field of a Staff
- Input: StaffID, then new changes
- Output: Confirmation
4. Search Staff
- Find specific staff
- Input: StaffID
- Output: Staff Information
5. Delete Staff
- Delete specific staff
- Input: StaffID
- Output: Confirmed deletion of staff

## Lwazi Mkhwanazi
- Implemented Inventory, Reward, and Transaction operations
- Each operation is divided into separate functions which all have consistent transaction management

## Inventory Operations
1. Increase Inventory
- Add/Update inventory stock
- Input: InventoryID, StoreID, amount
- Output: Confirmation of inventory increase
2. Decrease Inventory
- Reduce inventory stock for a specific store and item
- Input: InventoryID, StoreID, amount
- Output: Confirmation of inventory decrease
3. Check Inventory
- Input: InventoryID
- Output: Quantity available

## Rewards Operations
1. Generate Member Rewards
- Identify active members eligible for rewards based on transaction activity
- Input: Month, Year
- Output: List of eligible CustomerIDs
2. Generate Employee Rewards
- Identify employees eligible for rewards based on transactions within a specific quarter
- Input: Quarter, Year
- Output: List of eligible StaffIDs

## Transaction Operations
1. Create Transaction
- Insert a new transaction record into the database
- Input: TransactionID, date, total, CustomerID, StaffID, StoreID
- Output: Confirmation of transaction creation
2. Add Item to Transaction
- Add items to a transaction via the Quantity table
- Input: TransactionID, ProductID, Amount
- Output: Confirmation of item added
3. Calculate Transaction Total
- Calculate transaction total using product pride and applied discount
- Input: TransactionID, DiscountID
- Output: Final calculated total
4. View Transaction Details
- Retrieve full transaction breakdown
- Input: TransactionID
- Output: Transaction details like date, total price, product names, and quantities
  
