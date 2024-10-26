import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
conn = sqlite3.connect('inventory.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL
    )
''')
conn.commit()

# Functions for User Authentication
def register_user(username, password):
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")

def authenticate_user(username, password):
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return c.fetchone() is not None

# Functions for Inventory Management
def add_product(name, quantity, price):
    c.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
    conn.commit()
    messagebox.showinfo("Success", f"Product '{name}' added successfully")

def delete_product(name):
    c.execute("DELETE FROM products WHERE name = ?", (name,))
    conn.commit()
    messagebox.showinfo("Success", f"Product '{name}' deleted successfully")

def edit_product(name, quantity, price):
    c.execute("UPDATE products SET quantity = ?, price = ? WHERE name = ?", (quantity, price, name))
    conn.commit()
    messagebox.showinfo("Success", f"Product '{name}' updated successfully")

def view_product(name):
    c.execute("SELECT * FROM products WHERE name = ?", (name,))
    product = c.fetchone()
    return product

def show_inventory():
    c.execute("SELECT * FROM products")
    return c.fetchall()

def check_low_stock(min_quantity):
    c.execute("SELECT * FROM products WHERE quantity <= ?", (min_quantity,))
    return c.fetchall()

# GUI Setup
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        
        # User Authentication Frame
        self.auth_frame = tk.Frame(root)
        self.auth_frame.pack(pady=10)
        
        tk.Label(self.auth_frame, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.auth_frame)
        self.username_entry.grid(row=0, column=1)
        
        tk.Label(self.auth_frame, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.auth_frame, show="*")
        self.password_entry.grid(row=1, column=1)
        
        tk.Button(self.auth_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.auth_frame, text="Register", command=self.register).grid(row=3, column=0, columnspan=2)

        # Inventory Frame
        self.inventory_frame = tk.Frame(root)
        
        tk.Label(self.inventory_frame, text="Product Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.inventory_frame)
        self.name_entry.grid(row=0, column=1)
        
        tk.Label(self.inventory_frame, text="Quantity:").grid(row=1, column=0)
        self.quantity_entry = tk.Entry(self.inventory_frame)
        self.quantity_entry.grid(row=1, column=1)
        
        tk.Label(self.inventory_frame, text="Price:").grid(row=2, column=0)
        self.price_entry = tk.Entry(self.inventory_frame)
        self.price_entry.grid(row=2, column=1)
        
        tk.Button(self.inventory_frame, text="Add Product", command=self.add_product).grid(row=3, column=0)
        tk.Button(self.inventory_frame, text="Edit Product", command=self.edit_product).grid(row=3, column=1)
        tk.Button(self.inventory_frame, text="Delete Product", command=self.delete_product).grid(row=4, column=0)
        tk.Button(self.inventory_frame, text="View Product", command=self.view_product).grid(row=4, column=1)
        tk.Button(self.inventory_frame, text="Show Inventory", command=self.show_inventory).grid(row=5, column=0, columnspan=2)
        
        tk.Label(self.inventory_frame, text="Low Stock Alert Quantity:").grid(row=6, column=0)
        self.low_stock_entry = tk.Entry(self.inventory_frame)
        self.low_stock_entry.grid(row=6, column=1)
        
        tk.Button(self.inventory_frame, text="Check Low Stock", command=self.check_low_stock).grid(row=7, column=0, columnspan=2)
        
        self.output_text = tk.Text(self.inventory_frame, height=10, width=50)
        self.output_text.grid(row=8, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if authenticate_user(username, password):
            self.auth_frame.pack_forget()
            self.inventory_frame.pack(pady=10)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        register_user(username, password)

    def add_product(self):
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get())
        price = float(self.price_entry.get())
        add_product(name, quantity, price)

    def delete_product(self):
        name = self.name_entry.get()
        delete_product(name)

    def edit_product(self):
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get())
        price = float(self.price_entry.get())
        edit_product(name, quantity, price)

    def view_product(self):
        name = self.name_entry.get()
        product = view_product(name)
        self.output_text.delete(1.0, tk.END)
        if product:
            self.output_text.insert(tk.END, f"Product: {product[1]}, Quantity: {product[2]}, Price: ${product[3]:.2f}\n")
        else:
            self.output_text.insert(tk.END, "Product not found\n")

    def show_inventory(self):
        products = show_inventory()
        self.output_text.delete(1.0, tk.END)
        for product in products:
            self.output_text.insert(tk.END, f"Product: {product[1]}, Quantity: {product[2]}, Price: ${product[3]:.2f}\n")

    def check_low_stock(self):
        min_quantity = int(self.low_stock_entry.get())
        low_stock_items = check_low_stock(min_quantity)
        self.output_text.delete(1.0, tk.END)
        for item in low_stock_items:
            self.output_text.insert(tk.END, f"Product: {item[1]}, Quantity:2 {item[2]}, Price: ${item[3]:.2f}\n")

root = tk.Tk()
app = InventoryApp(root)
root.mainloop()
