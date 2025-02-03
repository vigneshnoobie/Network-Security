import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk

class Product:
    def __init__(self, product_id, name, description, quantity, location, stage):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.quantity = quantity
        self.location = location
        self.stage = stage

class WarehouseManagementSystem:
    def __init__(self):
        self.products = []
        self.conn = sqlite3.connect("inventory.db")
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def add_product(self, product_id, name, description, quantity, location, stage):
        product = Product(product_id, name, description, quantity, location, stage)
        self.products.append(product)
        print(f"Product '{name}' added to inventory.")

    def update_inventory(self, product_id, new_quantity):
        for product in self.products:
            if product.product_id == product_id:
                product.quantity = new_quantity
                print(f"Inventory updated for product '{product.name}': New quantity - {product.quantity}")
                return
        print("Product not found in inventory.")

    def generate_inventory_report(self):
        report = ""
        for product in self.products:
            report += f"Product: {product.name}, Quantity: {product.quantity}, Location: {product.location}, Stage: {product.stage}\n"
        return report

    def save_to_database(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS products
                     (product_id INT PRIMARY KEY, name TEXT, description TEXT, quantity INT, location TEXT, stage TEXT)''')
        for product in self.products:
            self.c.execute("SELECT * FROM products WHERE product_id=?", (product.product_id,))
            existing_product = self.c.fetchone()
            if existing_product:
                self.c.execute('''UPDATE products SET name=?, description=?, quantity=?, location=?, stage=? WHERE product_id=?''',
                               (product.name, product.description, product.quantity, product.location, product.stage, product.product_id))
            else:
                self.c.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)",
                               (product.product_id, product.name, product.description, product.quantity, product.location, product.stage))
        self.conn.commit()
        print("Inventory data saved to database.")

    def view_database(self):
        self.c.execute("SELECT * FROM products")
        rows = self.c.fetchall()
        return rows

    def remove_product(self, product_id):
        self.c.execute("DELETE FROM products WHERE product_id=?", (product_id,))
        self.conn.commit()

        for idx, product in enumerate(self.products):
            if product.product_id == product_id:
                del self.products[idx]
                print(f"Product with ID {product_id} removed from inventory.")
                return
        print("Product not found in inventory.")

class WarehouseManagementGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Warehouse Management System")
        
        self.warehouse = WarehouseManagementSystem()

        
        background_image = Image.open("warehouse.jpg")  
        background_photo = ImageTk.PhotoImage(background_image)
        self.background_label = tk.Label(self.master, image=background_photo)
        self.background_label.image = background_photo 
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

     
        self.add_product_frame = tk.Frame(self.master, padx=20, pady=10)
        self.add_product_frame.pack()

        tk.Label(self.add_product_frame, text="Product ID:").grid(row=0, column=0, sticky="e")
        self.product_id_entry = tk.Entry(self.add_product_frame)
        self.product_id_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.add_product_frame, text="Name:").grid(row=1, column=0, sticky="e")
        self.name_entry = tk.Entry(self.add_product_frame)
        self.name_entry.grid(row=1, column=1, padx=5)

        tk.Label(self.add_product_frame, text="Description:").grid(row=2, column=0, sticky="e")
        self.description_entry = tk.Entry(self.add_product_frame)
        self.description_entry.grid(row=2, column=1, padx=5)

        tk.Label(self.add_product_frame, text="Quantity:").grid(row=3, column=0, sticky="e")
        self.quantity_entry = tk.Entry(self.add_product_frame)
        self.quantity_entry.grid(row=3, column=1, padx=5)

        tk.Label(self.add_product_frame, text="Location:").grid(row=4, column=0, sticky="e")
        self.location_var = tk.StringVar()
        self.location_combobox = ttk.Combobox(self.add_product_frame, textvariable=self.location_var, state="readonly")
        self.location_combobox['values'] = (
            'Dublin', 'Cork', 'Galway', 'Limerick', 'Waterford', 'Drogheda',
            'Dundalk', 'Sligo', 'Bray', 'Navan', 'Kilkenny', 'Ennis', 'Tralee',
            'Carlow', 'Naas', 'Athlone', 'Letterkenny', 'Tullamore', 'Killarney',
            'Arklow', 'Cobh', 'Castlebar', 'Midleton', 'Mallow', 'Ballina', 'Enniscorthy',
            'Wicklow', 'Cavan', 'Athy', 'Longford', 'Dungarvan', 'Nenagh', 'Trim', 
            'Thurles', 'Youghal', 'Monaghan', 'Buncrana', 'Ballinasloe', 'Fermoy', 
            'Westport', 'Carrick-on-Suir', 'Birr', 'Tipperary'
        )
        self.location_combobox.grid(row=4, column=1, padx=5)

        tk.Label(self.add_product_frame, text="Stage:").grid(row=5, column=0, sticky="e")
        self.stage_var = tk.StringVar()
        self.stage_combobox = ttk.Combobox(self.add_product_frame, textvariable=self.stage_var, state="readonly")
        self.stage_combobox['values'] = ('Pack Receiving', 'Pack Unloading Area', 'Material Storage', 'Handling', 'Picking & Packing', 'Quality control/Packing', 'Shipping Stage', 'Shipping')
        self.stage_combobox.grid(row=5, column=1, padx=5)

        self.add_button = tk.Button(self.add_product_frame, text="Add Product", command=self.add_product)
        self.add_button.grid(row=6, columnspan=2, pady=10)

      
        self.inventory_report_frame = tk.Frame(self.master)
        self.inventory_report_frame.pack(pady=10)

        tk.Label(self.inventory_report_frame, text="Inventory notes", font=("Helvetica", 14)).pack()

        self.report_text = tk.Text(self.inventory_report_frame, width=70, height=15)
        self.report_text.pack(pady=10)

        
        self.save_buttons_frame = tk.Frame(self.master)
        self.save_buttons_frame.pack(pady=10)

        self.save_db_button = tk.Button(self.save_buttons_frame, text="Save to SQLite", command=self.save_to_database)
        self.save_db_button.grid(row=0, column=0, padx=5)

        
        self.view_db_frame = tk.Frame(self.master)
        self.view_db_frame.pack(pady=10)

        self.view_db_button = tk.Button(self.view_db_frame, text="View Database", command=self.view_database)
        self.view_db_button.grid(row=0, column=0, padx=5)

        self.edit_db_button = tk.Button(self.view_db_frame, text="Edit Database", command=self.edit_database)
        self.edit_db_button.grid(row=0, column=1, padx=5)

    def add_product(self):
        product_id = int(self.product_id_entry.get())
        name = self.name_entry.get()
        description = self.description_entry.get()
        quantity = int(self.quantity_entry.get())
        location = self.location_var.get()
        stage = self.stage_var.get()

        self.warehouse.add_product(product_id, name, description, quantity, location, stage)
        self.update_inventory_report()

    def update_inventory_report(self):
        report = self.warehouse.generate_inventory_report()
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, report)

    def save_to_database(self):
        self.warehouse.save_to_database()
        messagebox.showinfo("Success", "Inventory data saved to SQLite database.")

    def view_database(self):
        rows = self.warehouse.view_database()
        self.show_database_info(rows)

    def show_database_info(self, rows):
        top = tk.Toplevel()
        top.title("View Database")

        label = tk.Label(top, text="Products in Database:")
        label.pack()

        for row in rows:
            label = tk.Label(top, text=row)
            label.pack()

    def edit_database(self):
        top = tk.Toplevel()
        top.title("Edit Database")

        tk.Label(top, text="Product ID:").grid(row=0, column=0, padx=5)
        self.edit_product_id_entry = tk.Entry(top)
        self.edit_product_id_entry.grid(row=0, column=1, padx=5)

        tk.Label(top, text="New Quantity:").grid(row=1, column=0, padx=5)
        self.new_quantity_entry = tk.Entry(top)
        self.new_quantity_entry.grid(row=1, column=1, padx=5)

        edit_button = tk.Button(top, text="Edit Quantity", command=self.edit_quantity)
        edit_button.grid(row=2, columnspan=2, pady=5)

        remove_button = tk.Button(top, text="Remove Product", command=self.remove_product)
        remove_button.grid(row=3, columnspan=2, pady=5)

    def edit_quantity(self):
        product_id = int(self.edit_product_id_entry.get())
        new_quantity = int(self.new_quantity_entry.get())
        self.warehouse.update_inventory(product_id, new_quantity)
        messagebox.showinfo("Success", "Product quantity updated.")
        self.update_inventory_report()

    def remove_product(self):
        product_id = int(self.edit_product_id_entry.get())
        self.warehouse.remove_product(product_id)
        messagebox.showinfo("Success", "Product removed from inventory.")
        self.update_inventory_report()

def main():
    root = tk.Tk()
    app = WarehouseManagementGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
