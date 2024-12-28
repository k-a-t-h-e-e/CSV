# Database Design and Explanation

## Overview
This database schema follows the principles of **Third Normal Form (3NF)** to eliminate redundancy and maintain data integrity. It represents a hierarchical structure where:
- A **customer** can have multiple **locations**.
- Each **order** is associated with a specific **customer** and a particular **location**.
- Each **order** also references a specific **vendor**.

The schema consists of four main tables: `customer`, `location`, `orders`, and `vendor`.

---

## Schema Description

### **1. Customer Table**
This table stores general information about customers.

#### Schema
```sql
CREATE TABLE IF NOT EXISTS customer (
    akeed_customer_id TEXT PRIMARY KEY,
    gender TEXT,
    dob DATE,
    status INTEGER,
    verified INTEGER,
    language TEXT,
    created_at TEXT,
    updated_at TEXT
);
```

#### Key Points:
- **Primary Key**: `akeed_customer_id` uniquely identifies each customer.
- Contains basic customer information such as gender, date of birth, account status, verification status, and timestamps for creation and updates.

---

### **2. Location Table**
This table stores information about the various locations associated with each customer.

#### Schema
```sql
CREATE TABLE IF NOT EXISTS location (
    customer_id TEXT,
    location_number INTEGER,
    location_type TEXT,
    latitude REAL,
    longitude REAL,
    PRIMARY KEY (customer_id, location_number),
    FOREIGN KEY (customer_id) REFERENCES customer(akeed_customer_id)
);
```

#### Key Points:
- **Composite Primary Key**: Combination of `customer_id` and `location_number` ensures uniqueness of locations for each customer.
- **Foreign Key**: `customer_id` references the `customer` table.
- Stores masked latitude and longitude, as well as the type of location (e.g., Home, Work, Other).

---

### **3. Orders Table**
This table records all orders made by customers. Each order is associated with a specific customer and one of their locations.

#### Schema
```sql
CREATE TABLE IF NOT EXISTS orders (
    akeed_order_id REAL PRIMARY KEY,
    customer_id TEXT,
    location_number INTEGER,
    item_count INTEGER,
    grand_total REAL,
    payment_mode INTEGER,
    promo_code TEXT,
    vendor_discount_amount REAL,
    promo_code_discount_percentage REAL,
    is_favorite TEXT,
    is_rated TEXT,
    vendor_rating REAL,
    driver_rating REAL,
    deliverydistance REAL,
    preparationtime REAL,
    delivery_time TEXT,
    order_accepted_time TEXT,
    driver_accepted_time TEXT,
    ready_for_pickup_time TEXT,
    picked_up_time TEXT,
    delivered_time TEXT,
    delivery_date TEXT,
    vendor_id INTEGER,
    created_at TEXT,
    FOREIGN KEY (customer_id) REFERENCES customer(akeed_customer_id),
    FOREIGN KEY (customer_id, location_number) REFERENCES location(customer_id, location_number),
    FOREIGN KEY (vendor_id) REFERENCES vendor(id)
);
```

#### Key Points:
- **Primary Key**: `akeed_order_id` uniquely identifies each order.
- **Foreign Keys**:
  - `customer_id` references the `customer` table.
  - `(customer_id, location_number)` references the `location` table to link the order to a specific customer and location.
  - `vendor_id` references the `vendor` table.
- Stores detailed order information, including item count, total cost, payment details, vendor/customer ratings, timestamps, and delivery data.

---

### **4. Vendor Table**
This table stores information about vendors.

#### Schema
```sql
CREATE TABLE IF NOT EXISTS vendor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    authentication_id REAL,
    latitude REAL,
    longitude REAL,
    vendor_category_en TEXT,
    vendor_category_id REAL,
    delivery_charge REAL,
    serving_distance REAL,
    is_open REAL,
    OpeningTime TEXT,
    OpeningTime2 TEXT,
    prepration_time INTEGER,
    commission REAL,
    is_akeed_delivering TEXT,
    discount_percentage REAL,
    status REAL,
    verified INTEGER,
    rank INTEGER,
    language TEXT,
    vendor_rating REAL,
    primary_tags TEXT,
    open_close_flags REAL,
    vendor_tag TEXT,
    vendor_tag_name TEXT,
    one_click_vendor TEXT,
    country_id REAL,
    city_id REAL,
    created_at TEXT,
    updated_at TEXT,
    device_type INTEGER,
    display_orders INTEGER
);
```

#### Key Points:
- **Primary Key**: `id` uniquely identifies each vendor.
- Contains vendor-specific data such as location, ratings, operational details, and other descriptive tags.

---

## Relational Structure

### Relationships
1. **Customer to Location**:
   - A customer can have multiple locations.
   - Relationship: One-to-Many.
   - Implemented via the foreign key `customer_id` in the `location` table.

2. **Customer and Location to Orders**:
   - Each order is linked to a specific customer and one of their locations.
   - Relationship: Many-to-One.
   - Implemented via the foreign keys `customer_id` and `(customer_id, location_number)` in the `orders` table.

3. **Vendor to Orders**:
   - Each order references a vendor.
   - Relationship: Many-to-One.
   - Implemented via the foreign key `vendor_id` in the `orders` table.

---

## Example Use Case

### Data Flow
1. **Customer Table**:
   - Add a customer: `CUST001`.
2. **Location Table**:
   - Add locations for `CUST001`:
     - Location 0: Home.
     - Location 1: Work.
3. **Orders Table**:
   - Add orders for `CUST001`:
     - Order 1001: Delivered to Location 0 (Home).
     - Order 1002: Delivered to Location 1 (Work).
4. **Vendor Table**:
   - Add vendor data for the vendors referenced in the orders.

---

## Database Features
- **Normalization**:
  - All tables are in 3NF to avoid redundancy and maintain data integrity.
- **Foreign Key Constraints**:
  - Ensure relationships between customers, locations, orders, and vendors are valid.
- **Scalability**:
  - The schema can handle multiple locations per customer and large numbers of orders and vendors.

---

## How to Use

### Setting up the Database
1. Install the required libraries by running the following command in your terminal:
   ```bash
   pip install pandas matplotlib numpy
   ```

2. Run the `python-script.py` to create and populate the database.
   - This script will:
     - Create the `customer`, `location`, `orders`, and `vendor` tables.
     - Insert data into these tables from the cleaned data files.

### GUI Interface
1. Run `gui-interface.py` to launch the GUI.
   - Use the interface to:
     - Add new customers by entering their details (gender, DOB, status, etc.). The `akeed_customer_id` is auto-generated.
     - Perform specific queries:
       - Print mean, max, and min values of `grand_total` from the `orders` table.
       - Plot a histogram of `item_count` with a log-scaled y-axis.
       - Display `customer_id` of customers who ordered more than 40 items.

### Jupyter Notebook
1. Use `script.ipynb` to:
   - Run database creation and data insertion cells.
   - Use the Tkinter GUI within notebook cells.
   - Execute exploratory queries and visualizations.

---

## Additional Notes
- Ensure all required libraries (e.g., `pandas`, `tkinter`, `sqlite3`, `matplotlib`, `numpy`) are installed before running the scripts.
- Validate data cleanliness before inserting into the database to avoid integrity issues.
- Regularly back up the database file (`database.db`).

