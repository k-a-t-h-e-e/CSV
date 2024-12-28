# %%
import pandas as pd
import os

# List of columns to ignore
ignore_columns = [
    'sunday_from_time1', 'sunday_to_time1', 'sunday_from_time2', 'sunday_to_time2',
    'monday_from_time1', 'monday_to_time1', 'monday_from_time2', 'monday_to_time2',
    'tuesday_from_time1', 'tuesday_to_time1', 'tuesday_from_time2', 'tuesday_to_time2',
    'wednesday_from_time1', 'wednesday_to_time1', 'wednesday_from_time2', 'wednesday_to_time2',
    'thursday_from_time1', 'thursday_to_time1', 'thursday_from_time2', 'thursday_to_time2',
    'friday_from_time1', 'friday_to_time1', 'friday_from_time2', 'friday_to_time2',
    'saturday_from_time1', 'saturday_to_time1', 'saturday_from_time2', 'saturday_to_time2'
]

# Folder containing CSV files
folder_path = "/home/kerupakaran/Videos/AnyDesk/CSV/"

# List all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Dictionary to store DataFrames
dataframes = {}

for file in csv_files:
    file_path = os.path.join(folder_path, file)
    print(f"Processing file: {file}")
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Drop the columns to be ignored
    df_filtered = df.drop(columns=[col for col in ignore_columns if col in df.columns], errors='ignore')
    
    # Store the filtered DataFrame in the dictionary
    dataframes[file] = df_filtered
    
    # Display column details
    print("Remaining Columns:")
    print(df_filtered.columns.tolist())
    print("\n")

# Access the DataFrames by their filenames, e.g., dataframes['example.csv']


# %%
# Example: Access the DataFrame for a specific file
df_orders = dataframes['orders.csv']
df_train_customers=dataframes['train_customers.csv']
df_train_full=dataframes['train_full.csv']
df_train_locations=dataframes['train_locations.csv']
df_vendors=dataframes['vendors.csv']

df_orders.columns = df_orders.columns.str.replace(' ', '_')

# %%
# Function to print column names, types, and sample values
def print_column_details(df, df_name):
    print(f"Column Details for {df_name},,")
    for col in df.columns:
        sample_value = df[col].iloc[0] if not df[col].isnull().all() else "NULL"
        print(f"{col},{df[col].dtypes},{sample_value}")
    print("\n")

# Example: Print column details for each DataFrame
dataframes = {
    "orders.csv": df_orders,
    "train_customers.csv": df_train_customers,
    "train_full.csv": df_train_full,
    "train_locations.csv": df_train_locations,
    "vendors.csv": df_vendors,
}

for name, df in dataframes.items():
    print_column_details(df, name)


# %%
# Find duplicate rows based on 'akeed_customer_id'
duplicates = df_train_customers[df_train_customers['akeed_customer_id'].duplicated(keep=False)]



# Sort by 'akeed_customer_id' and 'updated_at' (latest first)
duplicates_sorted = df_train_customers.sort_values(by=['akeed_customer_id', 'updated_at'], ascending=[True, False])

# Drop duplicates while keeping the latest 'updated_at'
cleaned_df_train_customers = duplicates_sorted.drop_duplicates(subset='akeed_customer_id', keep='first')

print("Rows with Latest 'updated_at' for Each Duplicate 'akeed_customer_id':")

cleaned_df_train_customers

# %%
# Find duplicate rows based on 'akeed_customer_id'
duplicates = df_vendors[df_vendors['id'].duplicated(keep=False)]
duplicates
# No duplicates for vendors

# %%
# Find duplicate rows based on 'akeed_customer_id'
duplicates = df_train_locations[df_train_locations['customer_id'].duplicated(keep=False)]
duplicates
# No duplicates for vendors

# %%
# Find duplicates based on 'akeed_order_id'
duplicates = df_orders[df_orders.duplicated(subset=['akeed_order_id'], keep=False)]

# Show distinct entries from these duplicates
distinct_duplicates = duplicates.drop_duplicates(subset=['akeed_order_id'])

df_orders


# %%
df_orders.rename(columns={'LOCATION_NUMBER': 'location_number'}, inplace=True)

# Drop the columns 'LOCATION_TYPE' and 'CID_X_LOC_NUM_X_VENDOR'
df_orders.drop(columns=['LOCATION_TYPE', 'CID_X_LOC_NUM_X_VENDOR'], inplace=True)

# Display the updated DataFrame
df_orders

# Find duplicate rows based on 'akeed_customer_id'
duplicates = df_orders[df_orders['akeed_order_id'].duplicated(keep=False)]
duplicates
# No duplicates for vendors

# Find duplicate rows based on 'akeed_customer_id'


# Sort by 'akeed_customer_id' and 'updated_at' (latest first)
cleaned_df_orders = df_orders.sort_values(by=['akeed_order_id', 'order_accepted_time'], ascending=[True, False])

# Drop duplicates while keeping the latest 'updated_at'
cleaned_df_orders = cleaned_df_orders.drop_duplicates(subset='akeed_order_id', keep='first')

print("Rows with Latest 'updated_at' for Each Duplicate 'akeed_customer_id':")

cleaned_df_orders



# %%
import sqlite3
import os
import pandas as pd

# Clean the data if needed
# Example: Replace NaN values with a placeholder
# customers_df.fillna(value={"dob": None}, inplace=True)  # Replace NaN dob with None
# vendors_df.fillna(value={"authentication_id": None}, inplace=True)  # Replace NaN auth_id with None

# Define the database file name
db_file = "database.db"

# Check if the file exists and delete it
if os.path.exists(db_file):
    os.remove(db_file)
    print(f"{db_file} has been deleted.")
else:
    print(f"{db_file} does not exist. Creating a new database.")

# Create a new SQLite database connection
conn = sqlite3.connect(db_file)
print(f"Connected to {db_file}.")
cursor = conn.cursor()

# Create Customer Table
cursor.execute('''
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
''')

# Create Vendor Table
cursor.execute('''
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
''')

# Create Locations Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS location (
    customer_id TEXT,
    location_number INTEGER,
    location_type TEXT,
    latitude REAL,
    longitude REAL,
    PRIMARY KEY (customer_id, location_number),
    FOREIGN KEY (customer_id) REFERENCES customer(akeed_customer_id)
);
''')

# Insert data into Customer Table
cleaned_df_train_customers.to_sql("customer", conn, if_exists="append", index=False)

# Insert data into Vendor Table
df_vendors.to_sql("vendor", conn, if_exists="append", index=False)

# Insert data into Locations Table
df_train_locations.to_sql("location", conn, if_exists="append", index=False)


cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    akeed_order_id REAL PRIMARY KEY,
    customer_id TEXT,
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
    location_number INTEGER,
    FOREIGN KEY(customer_id) REFERENCES customer(akeed_customer_id),
    FOREIGN KEY (customer_id, location_number) REFERENCES location(customer_id, location_number),
    FOREIGN KEY(vendor_id) REFERENCES vendor(id)
);
''')

cleaned_df_orders.to_sql("orders", conn, if_exists="append", index=False)

# Commit and close the connection
conn.commit()
conn.close()

print("Data inserted successfully into customers, vendors, and locations tables.")


# %%
import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import uuid  # Import for generating unique IDs


# Database file
DB_FILE = "database.db"

# Connect to the database
def connect_to_db():
    return sqlite3.connect(DB_FILE)

# Add a new customer to the database
def add_customer():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        akeed_customer_id = str(uuid.uuid4())  
        
        gender = gender_var.get()
        dob = dob_var.get()
        status = int(status_var.get())
        verified = int(verified_var.get())
        language = language_var.get()
        created_at = created_at_var.get()
        updated_at = updated_at_var.get()
        
        # Insert customer into the database
        cursor.execute('''
        INSERT INTO customer (akeed_customer_id, gender, dob, status, verified, language, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (akeed_customer_id,gender, dob, status, verified, language, created_at, updated_at))
        
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Customer added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Display mean, max, min of grand_total
def show_grand_total_stats():
    conn = connect_to_db()
    df = pd.read_sql_query("SELECT grand_total FROM orders", conn)
    conn.close()
    
    mean_val = df['grand_total'].mean()
    max_val = df['grand_total'].max()
    min_val = df['grand_total'].min()
    
    messagebox.showinfo("Grand Total Stats", f"Mean: {mean_val:.2f}\nMax: {max_val:.2f}\nMin: {min_val:.2f}")

# Plot histogram of item_count
def plot_item_count_histogram():
    conn = connect_to_db()
    df = pd.read_sql_query("SELECT item_count FROM orders", conn)
    conn.close()
    
    plt.figure(figsize=(8, 6))
    plt.hist(df['item_count'], bins=20, log=True, color='skyblue', edgecolor='black')
    plt.xlabel("Item Count")
    plt.ylabel("Frequency (Log Scale)")
    plt.title("Histogram of Item Count")
    plt.show()

# Show customers with orders > 40 items
def show_customers_large_orders():
    conn = connect_to_db()
    query = '''
    SELECT DISTINCT customer_id
    FROM orders
    WHERE item_count > 40
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    customers = df['customer_id'].tolist()
    customer_list = "\n".join(customers)
    messagebox.showinfo("Customers with >40 Items", f"Customer IDs:\n{customer_list}")

# Main GUI
root = tk.Tk()
root.title("Customer and Order Dashboard")

# Input fields for adding a customer
tk.Label(root, text="Add New Customer").grid(row=0, columnspan=2)

tk.Label(root, text="Gender:").grid(row=1, column=0)
gender_var = tk.StringVar()
tk.Entry(root, textvariable=gender_var).grid(row=1, column=1)

tk.Label(root, text="DOB:").grid(row=2, column=0)
dob_var = tk.StringVar()
tk.Entry(root, textvariable=dob_var).grid(row=2, column=1)

tk.Label(root, text="Status:").grid(row=3, column=0)
status_var = tk.StringVar()
tk.Entry(root, textvariable=status_var).grid(row=3, column=1)

tk.Label(root, text="Verified:").grid(row=4, column=0)
verified_var = tk.StringVar()
tk.Entry(root, textvariable=verified_var).grid(row=4, column=1)

tk.Label(root, text="Language:").grid(row=5, column=0)
language_var = tk.StringVar()
tk.Entry(root, textvariable=language_var).grid(row=5, column=1)

tk.Label(root, text="Created At:").grid(row=6, column=0)
created_at_var = tk.StringVar()
tk.Entry(root, textvariable=created_at_var).grid(row=6, column=1)

tk.Label(root, text="Updated At:").grid(row=7, column=0)
updated_at_var = tk.StringVar()
tk.Entry(root, textvariable=updated_at_var).grid(row=7, column=1)

tk.Button(root, text="Add Customer", command=add_customer).grid(row=8, columnspan=2)

# Buttons for database queries
tk.Button(root, text="Show Grand Total Stats", command=show_grand_total_stats).grid(row=9, columnspan=2)
tk.Button(root, text="Plot Item Count Histogram", command=plot_item_count_histogram).grid(row=10, columnspan=2)
tk.Button(root, text="Show Customers with >40 Items", command=show_customers_large_orders).grid(row=11, columnspan=2)

# Run the GUI
root.mainloop()



