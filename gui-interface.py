
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



