



















from tkinter import *
from tkinter import ttk, messagebox
import pymysql


# ============================================================
# DATABASE SETTINGS
# ============================================================

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Sswashank@12345"
DB_NAME = "inventory_system"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def connect_database():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="Sswashank@12345",
            database="inventory_system"
        )

        return connection

    except pymysql.MySQLError as e:
        messagebox.showerror(
            "Database Error",
            f"Unable to connect to database:\n{e}"
        )
        return None


# ============================================================
# PRODUCT FORM
# ============================================================

def product_form(window):

    # ========================================================
    # MAIN FRAME
    # ========================================================

    product_frame = Frame(
        window,
        width=1330,
        height=690,
        bg="white"
    )

    product_frame.place(
        x=200,
        y=100
    )


    # ========================================================
    # TITLE
    # ========================================================

    title_label = Label(
        product_frame,
        text="Manage Product Details",
        font=("times new roman", 16, "bold"),
        bg="#0f4d7d",
        fg="white"
    )

    title_label.place(
        x=0,
        y=0,
        relwidth=1
    )


    # ========================================================
    # CATEGORY
    # ========================================================

    category_label = Label(
        product_frame,
        text="Category",
        font=("times new roman", 14, "bold"),
        bg="white",
        fg="black"
    )

    category_label.place(
        x=20,
        y=60
    )


    category_combobox = ttk.Combobox(
        product_frame,
        font=("times new roman", 14),
        width=18,
        state="readonly"
    )

    category_combobox.place(
        x=20,
        y=90
    )

    category_combobox.set("Empty")


    # ========================================================
    # SUPPLIER
    # ========================================================

    supplier_label = Label(
        product_frame,
        text="Supplier",
        font=("times new roman", 14, "bold"),
        bg="white",
        fg="black"
    )

    supplier_label.place(
        x=260,
        y=60
    )


    supplier_combobox = ttk.Combobox(
        product_frame,
        font=("times new roman", 14),
        width=18,
        state="readonly"
    )

    supplier_combobox.place(
        x=260,
        y=90
    )

    supplier_combobox.set("Empty")


    # ========================================================
    # PRODUCT NAME
    # ========================================================

    name_label = Label(
        product_frame,
        text="Product Name",
        font=("times new roman", 14, "bold"),
        bg="white",
        fg="black"
    )

    name_label.place(
        x=20,
        y=145
    )


    name_entry = Entry(
        product_frame,
        font=("times new roman", 14),
        bg="lightyellow",
        width=20
    )

    name_entry.place(
        x=20,
        y=175
    )


    # ========================================================
    # PRICE
    # ========================================================

    price_label = Label(
        product_frame,
        text="Price",
        font=("times new roman", 14, "bold"),
        bg="white",
        fg="black"
    )

    price_label.place(
        x=260,
        y=145
    )


    price_entry = Entry(
        product_frame,
        font=("times new roman", 14),
        bg="lightyellow",
        width=20
    )

    price_entry.place(
        x=260,
        y=175
    )


    # ========================================================
    # QUANTITY
    # ========================================================

    quantity_label = Label(
        product_frame,
        text="Quantity",
        font=("times new roman", 14, "bold"),
        bg="white",
        fg="black"
    )

    quantity_label.place(
        x=20,
        y=230
    )


    quantity_entry = Entry(
        product_frame,
        font=("times new roman", 14),
        bg="lightyellow",
        width=20
    )

    quantity_entry.place(
        x=20,
        y=260
    )


    # ========================================================
    # STATUS
    # ========================================================

    status_label = Label(
        product_frame,
        text="Status",
        font=("times new roman", 14, "bold"),
        bg="white",
        fg="black"
    )

    status_label.place(
        x=260,
        y=230
    )


    status_combobox = ttk.Combobox(
        product_frame,
        values=(
            "Active",
            "Inactive"
        ),
        font=("times new roman", 14),
        width=18,
        state="readonly"
    )

    status_combobox.place(
        x=260,
        y=260
    )

    status_combobox.set("Select Status")


    # ========================================================
    # BUTTON FRAME
    # ========================================================

    button_frame = Frame(
        product_frame,
        bg="white"
    )

    button_frame.place(
        x=20,
        y=320
    )


    # ========================================================
    # CLEAR FIELDS
    # ========================================================

    def clear_fields():

        if category_combobox["values"]:
            category_combobox.set(
                category_combobox["values"][0]
            )
        else:
            category_combobox.set("Empty")


        if supplier_combobox["values"]:
            supplier_combobox.set(
                supplier_combobox["values"][0]
            )
        else:
            supplier_combobox.set("Empty")


        name_entry.delete(
            0,
            END
        )

        price_entry.delete(
            0,
            END
        )

        quantity_entry.delete(
            0,
            END
        )

        status_combobox.set(
            "Select Status"
        )

        search_entry.delete(
            0,
            END
        )

        for item in treeview.selection():
            treeview.selection_remove(item)


    # ========================================================
    # LOAD CATEGORIES
    # ========================================================

    def load_categories():

        con = None
        cursor = None

        try:

            con = connect_database()

            if con is None:
                return

            cursor = con.cursor()

            cursor.execute(
                """
                SELECT category_name
                FROM category_data
                ORDER BY category_name
                """
            )

            categories = cursor.fetchall()

            category_values = [
                row[0]
                for row in categories
            ]

            category_combobox["values"] = category_values

            if category_values:

                category_combobox.set(
                    category_values[0]
                )

            else:

                category_combobox.set(
                    "Empty"
                )

        except pymysql.MySQLError as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load categories:\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if con:
                con.close()


    # ========================================================
    # LOAD SUPPLIERS
    # ========================================================

    def load_suppliers():

        con = None
        cursor = None

        try:

            con = connect_database()

            if con is None:
                return

            cursor = con.cursor()

            cursor.execute(
                """
                SELECT supplier_name
                FROM supplier_data
                ORDER BY supplier_name
                """
            )

            suppliers = cursor.fetchall()

            supplier_values = [
                row[0]
                for row in suppliers
            ]

            supplier_combobox["values"] = supplier_values

            if supplier_values:

                supplier_combobox.set(
                    supplier_values[0]
                )

            else:

                supplier_combobox.set(
                    "Empty"
                )

        except pymysql.MySQLError as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load suppliers:\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if con:
                con.close()


    # ========================================================
    # VALIDATE PRODUCT
    # ========================================================

    def get_product_data():

        category = category_combobox.get().strip()
        supplier = supplier_combobox.get().strip()
        name = name_entry.get().strip()
        price = price_entry.get().strip()
        quantity = quantity_entry.get().strip()
        status = status_combobox.get().strip()


        # Category

        if not category or category == "Empty":

            messagebox.showerror(
                "Error",
                "Please select category"
            )

            return None


        # Supplier

        if not supplier or supplier == "Empty":

            messagebox.showerror(
                "Error",
                "Please select supplier"
            )

            return None


        # Product Name

        if not name:

            messagebox.showerror(
                "Error",
                "Please enter product name"
            )

            return None


        # Price

        if not price:

            messagebox.showerror(
                "Error",
                "Please enter price"
            )

            return None


        # Quantity

        if not quantity:

            messagebox.showerror(
                "Error",
                "Please enter quantity"
            )

            return None


        # Status

        if not status or status == "Select Status":

            messagebox.showerror(
                "Error",
                "Please select status"
            )

            return None


        # Price validation

        try:

            price = float(price)

        except ValueError:

            messagebox.showerror(
                "Error",
                "Price must be a number"
            )

            return None


        # Quantity validation

        try:

            quantity = int(quantity)

        except ValueError:

            messagebox.showerror(
                "Error",
                "Quantity must be an integer"
            )

            return None


        # Negative price

        if price < 0:

            messagebox.showerror(
                "Error",
                "Price cannot be negative"
            )

            return None


        # Negative quantity

        if quantity < 0:

            messagebox.showerror(
                "Error",
                "Quantity cannot be negative"
            )

            return None


        return (
            category,
            supplier,
            name,
            price,
            quantity,
            status
        )


    # ========================================================
    # ADD PRODUCT
    # ========================================================

    def add_product():

        data = get_product_data()

        if data is None:
            return


        category, supplier, name, price, quantity, status = data

        con = None
        cursor = None

        try:

            con = connect_database()

            if con is None:
                return

            cursor = con.cursor()


            # Check duplicate product

            cursor.execute(
                """
                SELECT id
                FROM product_data
                WHERE name=%s
                """,
                (name,)
            )

            if cursor.fetchone():

                messagebox.showerror(
                    "Error",
                    "Product already exists"
                )

                return


            # Insert product

            cursor.execute(
                """
                INSERT INTO product_data
                (
                    category,
                    supplier,
                    name,
                    price,
                    quantity,
                    status
                )
                VALUES
                (%s,%s,%s,%s,%s,%s)
                """,
                (
                    category,
                    supplier,
                    name,
                    price,
                    quantity,
                    status
                )
            )


            con.commit()


            messagebox.showinfo(
                "Success",
                "Product added successfully"
            )


            clear_fields()
            show_all_products()


        except pymysql.MySQLError as e:

            if con:
                con.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to add product:\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if con:
                con.close()


    # ========================================================
    # UPDATE PRODUCT
    # ========================================================

    def update_product():

        selected = treeview.selection()

        if not selected:

            messagebox.showerror(
                "Error",
                "Please select a product from the table"
            )

            return


        values = treeview.item(
            selected[0],
            "values"
        )

        if not values:
            return


        product_id = values[0]


        data = get_product_data()

        if data is None:
            return


        category, supplier, name, price, quantity, status = data


        con = None
        cursor = None

        try:

            con = connect_database()

            if con is None:
                return

            cursor = con.cursor()


            # Check duplicate product name

            cursor.execute(
                """
                SELECT id
                FROM product_data
                WHERE name=%s
                AND id!=%s
                """,
                (
                    name,
                    product_id
                )
            )


            if cursor.fetchone():

                messagebox.showerror(
                    "Error",
                    "Another product with this name already exists"
                )

                return


            # Update

            cursor.execute(
                """
                UPDATE product_data
                SET
                    category=%s,
                    supplier=%s,
                    name=%s,
                    price=%s,
                    quantity=%s,
                    status=%s
                WHERE id=%s
                """,
                (
                    category,
                    supplier,
                    name,
                    price,
                    quantity,
                    status,
                    product_id
                )
            )


            con.commit()


            messagebox.showinfo(
                "Success",
                "Product updated successfully"
            )


            clear_fields()
            show_all_products()


        except pymysql.MySQLError as e:

            if con:
                con.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to update product:\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if con:
                con.close()


    # ========================================================
    # DELETE PRODUCT
    # ========================================================

    def delete_product():

        selected = treeview.selection()

        if not selected:

            messagebox.showerror(
                "Error",
                "Please select a product"
            )

            return


        values = treeview.item(
            selected[0],
            "values"
        )

        if not values:
            return


        product_id = values[0]
        product_name = values[3]


        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{product_name}'?"
        )


        if not confirm:
            return


        con = None
        cursor = None

        try:

            con = connect_database()

            if con is None:
                return

            cursor = con.cursor()


            cursor.execute(
                """
                DELETE FROM product_data
                WHERE id=%s
                """,
                (product_id,)
            )


            con.commit()


            messagebox.showinfo(
                "Success",
                "Product deleted successfully"
            )


            clear_fields()
            show_all_products()


        except pymysql.MySQLError as e:

            if con:
                con.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to delete product:\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if con:
                con.close()


    # ========================================================
    # SELECT PRODUCT FROM TREEVIEW
    # ========================================================

    def select_product(event):

        selected = treeview.selection()

        if not selected:
            return


        values = treeview.item(
            selected[0],
            "values"
        )

        if not values:
            return


        # ID = values[0]

        category_combobox.set(
            values[1]
        )

        supplier_combobox.set(
            values[2]
        )


        name_entry.delete(
            0,
            END
        )

        name_entry.insert(
            0,
            values[3]
        )


        price_entry.delete(
            0,
            END
        )

        price_entry.insert(
            0,
            values[4]
        )


        quantity_entry.delete(
            0,
            END
        )

        quantity_entry.insert(
            0,
            values[5]
        )


        status_combobox.set(
            values[6]
        )


    # ========================================================
    # SHOW ALL PRODUCTS
    # ========================================================

    def show_all_products():

        con = None
        cursor = None

        try:

            con = connect_database()

            if con is None:
                return

            cursor = con.cursor()


            # Clear Treeview

            for item in treeview.get_children():

                treeview.delete(
                    item
                )


            cursor.execute(
                """
                SELECT
                    id,
                    category,
                    supplier,
                    name,
                    price,
                    quantity,
                    status
                FROM product_data
                ORDER BY id DESC
                """
            )


            products = cursor.fetchall()


            for product in products:

                treeview.insert(
                    "",
                    END,
                    values=product
                )


        except pymysql.MySQLError as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load products:\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if con:
                con.close()


    # ========================================================
    # SEARCH PRODUCT
    # ========================================================

    def search_product():

        search_by = search_combobox.get()
        search_value = search_entry.get().strip()


        if not search_value:

            messagebox.showerror(
                "Error",
                "Please enter search value"
            )

            return


        column_map = {

            "Category": "category",

            "Supplier": "supplier",

            "Name": "name",

            "Status": "status"

        }


        column = column_map.get(
            search_by
        )


        if column is None:

            messagebox.showerror(
                "Error",
                "Please select search type"
            )

            return


        con = None
        cursor = None

        try:

            con = connect_database()

            if con is None:
                return

            cursor = con.cursor()


            # Clear Treeview

            for item in treeview.get_children():

                treeview.delete(
                    item
                )


            query = f"""
                SELECT
                    id,
                    category,
                    supplier,
                    name,
                    price,
                    quantity,
                    status
                FROM product_data
                WHERE {column} LIKE %s
                ORDER BY id DESC
            """


            cursor.execute(
                query,
                (
                    f"%{search_value}%",
                )
            )


            products = cursor.fetchall()


            for product in products:

                treeview.insert(
                    "",
                    END,
                    values=product
                )


            if not products:

                messagebox.showinfo(
                    "Search",
                    "No product found"
                )


        except pymysql.MySQLError as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to search product:\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if con:
                con.close()


    # ========================================================
    # BUTTONS
    # ========================================================

    add_button = Button(
        button_frame,
        text="Add",
        font=("times new roman", 14),
        width=10,
        cursor="hand2",
        bg="#0f4d74",
        fg="white",
        command=add_product
    )

    add_button.grid(
        row=0,
        column=0,
        padx=5
    )


    update_button = Button(
        button_frame,
        text="Update",
        font=("times new roman", 14),
        width=10,
        cursor="hand2",
        bg="#0f4d74",
        fg="white",
        command=update_product
    )

    update_button.grid(
        row=0,
        column=1,
        padx=5
    )


    delete_button = Button(
        button_frame,
        text="Delete",
        font=("times new roman", 14),
        width=10,
        cursor="hand2",
        bg="#0f4d74",
        fg="white",
        command=delete_product
    )

    delete_button.grid(
        row=0,
        column=2,
        padx=5
    )


    clear_button = Button(
        button_frame,
        text="Clear",
        font=("times new roman", 14),
        width=10,
        cursor="hand2",
        bg="#0f4d74",
        fg="white",
        command=clear_fields
    )

    clear_button.grid(
        row=0,
        column=3,
        padx=5
    )


    # ========================================================
    # SEARCH FRAME
    # ========================================================

    search_frame = Frame(
        product_frame,
        bg="white"
    )

    search_frame.place(
        x=480,
        y=70
    )


    search_combobox = ttk.Combobox(
        search_frame,
        values=(
            "Category",
            "Supplier",
            "Name",
            "Status"
        ),
        font=("times new roman", 14),
        width=12,
        state="readonly"
    )

    search_combobox.grid(
        row=0,
        column=0,
        padx=5
    )

    search_combobox.set(
        "Search By"
    )


    search_entry = Entry(
        search_frame,
        font=("times new roman", 14),
        width=18
    )

    search_entry.grid(
        row=0,
        column=1,
        padx=5
    )


    search_button = Button(
        search_frame,
        text="Search",
        font=("times new roman", 14),
        width=10,
        cursor="hand2",
        bg="#0f4d74",
        fg="white",
        command=search_product
    )

    search_button.grid(
        row=0,
        column=2,
        padx=5
    )


    show_button = Button(
        search_frame,
        text="Show All",
        font=("times new roman", 14),
        width=10,
        cursor="hand2",
        bg="#0f4d74",
        fg="white",
        command=show_all_products
    )

    show_button.grid(
        row=0,
        column=3,
        padx=5
    )


    # ========================================================
    # TREEVIEW FRAME
    # ========================================================

    treeview_frame = Frame(
        product_frame,
        bg="white"
    )

    treeview_frame.place(
        x=480,
        y=125,
        width=750,
        height=550
    )


    # ========================================================
    # SCROLLBARS
    # ========================================================

    scrolly = Scrollbar(
        treeview_frame,
        orient=VERTICAL
    )

    scrollx = Scrollbar(
        treeview_frame,
        orient=HORIZONTAL
    )


    # ========================================================
    # TREEVIEW
    # ========================================================

    treeview = ttk.Treeview(
        treeview_frame,
        columns=(
            "id",
            "category",
            "supplier",
            "name",
            "price",
            "quantity",
            "status"
        ),
        show="headings",
        yscrollcommand=scrolly.set,
        xscrollcommand=scrollx.set
    )


    scrolly.pack(
        side=RIGHT,
        fill=Y
    )

    scrollx.pack(
        side=BOTTOM,
        fill=X
    )


    scrolly.config(
        command=treeview.yview
    )

    scrollx.config(
        command=treeview.xview
    )


    treeview.pack(
        fill=BOTH,
        expand=True
    )


    # ========================================================
    # TREEVIEW HEADINGS
    # ========================================================

    treeview.heading(
        "id",
        text="ID"
    )

    treeview.heading(
        "category",
        text="Category"
    )

    treeview.heading(
        "supplier",
        text="Supplier"
    )

    treeview.heading(
        "name",
        text="Name"
    )

    treeview.heading(
        "price",
        text="Price"
    )

    treeview.heading(
        "quantity",
        text="Quantity"
    )

    treeview.heading(
        "status",
        text="Status"
    )


    # ========================================================
    # TREEVIEW COLUMNS
    # ========================================================

    treeview.column(
        "id",
        width=50,
        anchor="center"
    )

    treeview.column(
        "category",
        width=130,
        anchor="center"
    )

    treeview.column(
        "supplier",
        width=130,
        anchor="center"
    )

    treeview.column(
        "name",
        width=150,
        anchor="center"
    )

    treeview.column(
        "price",
        width=100,
        anchor="center"
    )

    treeview.column(
        "quantity",
        width=100,
        anchor="center"
    )

    treeview.column(
        "status",
        width=100,
        anchor="center"
    )


    # ========================================================
    # TREEVIEW SELECT EVENT
    # ========================================================

    treeview.bind(
        "<ButtonRelease-1>",
        select_product
    )


    # ========================================================
    # LOAD DATA WHEN FORM OPENS
    # ========================================================

    load_categories()
    load_suppliers()
    show_all_products()
