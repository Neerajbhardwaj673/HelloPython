import sqlite3
import tkinter as tk
from tkinter import ttk

class ShoppingCart:
    def _init_(self, master):
        self.master = master
        master.title("Shopping Cart")

        self.cart = {}

        # Create or connect to the database
        self.conn = sqlite3.connect('shopping_cart.db')
        self.create_table()

        # Create GUI elements
        self.item_label = tk.Label(master, text="Item:")
        self.item_label.pack()
        self.item_entry = tk.Entry(master)
        self.item_entry.pack()

        self.price_label = tk.Label(master, text="Price:")
        self.price_label.pack()
        self.price_entry = tk.Entry(master)
        self.price_entry.pack()

        self.quantity_label = tk.Label(master, text="Quantity:")
        self.quantity_label.pack()
        self.quantity_entry = tk.Entry(master)
        self.quantity_entry.pack()

        self.add_button = tk.Button(master, text="Add to Cart", command=self.add_item)
        self.add_button.pack()

        self.remove_button = tk.Button(master, text="Remove from Cart", command=self.remove_item)
        self.remove_button.pack()

        self.cart_text = tk.Text(master, height=10, width=40)
        self.cart_text.pack()

        self.show_cart_button = tk.Button(master, text="Show Cart", command=self.show_cart)
        self.show_cart_button.pack()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                item TEXT,
                price REAL,
                quantity INTEGER
            )
        """)
        self.conn.commit()

    def add_item(self):
        item = self.item_entry.get()
        price = float(self.price_entry.get())
        quantity = int(self.quantity_entry.get())

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cart WHERE item = ?", (item,))
        existing_item = cursor.fetchone()

        if existing_item:
            new_quantity = existing_item[2] + quantity
            cursor.execute("UPDATE cart SET quantity = ? WHERE item = ?", (new_quantity, item))
        else:
            cursor.execute("INSERT INTO cart VALUES (?, ?, ?)", (item, price, quantity))

        self.conn.commit()
        print(f"{quantity} {item}(s) added to the cart.")

    def remove_item(self):
        item = self.item_entry.get()
        quantity = int(self.quantity_entry.get())

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cart WHERE item = ?", (item,))
        existing_item = cursor.fetchone()

        if existing_item:
            if existing_item[2] <= quantity:
                cursor.execute("DELETE FROM cart WHERE item = ?", (item,))
            else:
                new_quantity = existing_item[2] - quantity
                cursor.execute("UPDATE cart SET quantity = ? WHERE item = ?", (new_quantity, item))

            self.conn.commit()
            print(f"{quantity} {item}(s) removed from the cart.")
        else:
            print(f"{item} not found in the cart.")

    def show_cart(self):
        total = 0
        self.cart_text.delete('1.0', tk.END)

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cart")
        cart_items = cursor.fetchall()

        if not cart_items:
            self.cart_text.insert(tk.END, "Your cart is empty.\n")
            return

        self.cart_text.insert(tk.END, "Your shopping cart:\n")

        for item, price, quantity in cart_items:
            item_total = price * quantity
            self.cart_text.insert(tk.END, f"{item}: ${price:.2f} x {quantity} = ${item_total:.2f}\n")
            total += item_total

        self.cart_text.insert(tk.END, f"\nTotal: ${total:.2f}")

root = tk.Tk()
shopping_cart = ShoppingCart(root)
root.mainloop()
