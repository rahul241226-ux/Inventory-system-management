
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
        cursor = connection.cursor()
        return cursor, connection

    except pymysql.MySQLError as e:
        messagebox.showerror(
            "Database Error",
            f"Unable to connect to database:\n{e}"
        )
        return None, None


# ============================================================
# CREATE PRODUCT TABLE
# ============================================================

def create_product_table():
    cursor, connection = connect_database()

    if cursor is None:
        return

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(100) NOT NULL,
                supplier VARCHAR(100) NOT NULL,
                name VARCHAR(150) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                discount DECIMAL(5,2) NOT NULL DEFAULT 0,
                discounted_price DECIMAL(10,2) NOT NULL DEFAULT 0,
                quantity INT NOT NULL,
                status VARCHAR(20) NOT NULL
            )
        """)

        connection.commit()

    except pymysql.MySQLError as e:
        messagebox.showerror(
            "Database Error",
            f"Unable to create product table:\n{e}"
        )

    finally:
        cursor.close()
        connection.close()


# ============================================================
# PRODUCT FORM
# ============================================================

def product_form(window):

    # --------------------------------------------------------
    # MAIN FRAME
    # --------------------------------------------------------

    product_frame = Frame(
        window,
        width=1330,
        height=690,
        bg="white"
    )

    product_frame.place(x=200, y=100)

    # --------------------------------------------------------
    # HEADING
    # --------------------------------------------------------

    heading_label = Label(
        product_frame,
        text="Manage Product Details",
        font=("times new roman", 16, "bold"),
        bg="#0f4d7d",
        fg="white"
    )

    heading_label.place(x=0, y=0, relwidth=1)

    # ========================================================
    # VARIABLES
    # ========================================================

    selected_product_id = StringVar()

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

    category_label.place(x=20, y=55)

    category_combobox = ttk.Combobox(
        product_frame,
        font=("times new roman", 14),
        width=18,
        state="readonly"
    )

    category_combobox.place(x=20, y=90)

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

    supplier_label.place(x=260, y=55)

    supplier_combobox = ttk.Combobox(
        product_frame,
        font=("times new roman", 14),
        width=18,
        state="readonly"
    )

    supplier_combobox.place(x=260, y=90)

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

    name_label.place(x=20, y=140)

    name_entry = Entry(
        product_frame,
        font=("times new roman", 14),
        bg="lightyellow"
    )

    name_entry.place(x=20, y=175, width=210)

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

    price_label.place(x=260, y=140)

    price_entry = Entry(
        product_frame,
        font=("times new roman", 14),
        bg="lightyellow"
    )

    price_entry.place(x=260, y=175, width=210)

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

    quantity_label.place(x=20, y=225)

    quantity_entry = Entry(
        product_frame,
        font=("times new roman", 14),
        bg="lightyellow"
    )

    quantity_entry.place(x=20, y=260, width=210)

    # ========================================================
    # DISCOUNT
    # ========================================================

    discount_label = Label(
        product_frame,
        text="Discount (%)",
        font=("times new roman", 14, "bold"),
        bg="white",
        fg="black"
    )

    discount_label.place(x=260, y=225)

    discount_spinbox = Spinbox(
        product_frame,
        from_=0,
        to=100,
        font=("times new roman", 14),
        bg="lightyellow"
    )

    discount_spinbox.place(x=260, y=260, width=210)

    discount_spinbox.delete(0, END)
    discount_spinbox.insert(0, "0")

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

    status_label.place(x=20, y=310)

    status_combobox = ttk.Combobox(
        product_frame,
        values=("Active", "Inactive"),
        font=("times new roman", 14),
        width=18,
        state="readonly"
    )

    status_combobox.place(x=20, y=345)

    status_combobox.set("Active")

    # ========================================================
    # LOAD CATEGORIES
    # ========================================================

    def load_categories():

        cursor, connection = connect_database()

        if cursor is None:
            return

        try:
            cursor.execute("""
                SELECT category_name
                FROM category_data
                ORDER BY category_name
            """)

            categories = cursor.fetchall()

            category_combobox["values"] = [
                row[0] for row in categories
            ]

            if categories:
                category_combobox.set(categories[0][0])
            else:
                category_combobox.set("Empty")

        except pymysql.MySQLError as e:
            messagebox.showerror(
                "Database Error",
                f"Unable to load categories:\n{e}"
            )

        finally:
            cursor.close()
            connection.close()

    # ========================================================
    # LOAD SUPPLIERS
    # ========================================================

    def load_suppliers():

        cursor, connection = connect_database()

        if cursor is None:
            return

        try:
            cursor.execute("""
                SELECT supplier_name
                FROM supplier_data
                ORDER BY supplier_name
            """)

            suppliers = cursor.fetchall()

            supplier_combobox["values"] = [
                row[0] for row in suppliers
            ]

            if suppliers:
                supplier_combobox.set(suppliers[0][0])
            else:
                supplier_combobox.set("Empty")

        except pymysql.MySQLError as e:
            messagebox.showerror(
                "Database Error",
                f"Unable to load suppliers:\n{e}"
            )

        finally:
            cursor.close()
            connection.close()

    # ========================================================
    # GET PRODUCT DATA
    # ========================================================

    def get_product_data():

        category = category_combobox.get().strip()
        supplier = supplier_combobox.get().strip()
        name = name_entry.get().strip()
        price = price_entry.get().strip()
        discount = discount_spinbox.get().strip()
        quantity = quantity_entry.get().strip()
        status = status_combobox.get().strip()

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if category == "" or category == "Empty":
            messagebox.showerror(
                "Error",
                "Please select a category"
            )
            return None

        if supplier == "" or supplier == "Empty":
            messagebox.showerror(
                "Error",
                "Please select a supplier"
            )
            return None

        if name == "":
            messagebox.showerror(
                "Error",
                "Please enter product name"
            )
            return None

        if price == "":
            messagebox.showerror(
                "Error",
                "Please enter price"
            )
            return None

        if quantity == "":
            messagebox.showerror(
                "Error",
                "Please enter quantity"
            )
            return None

        # ----------------------------------------------------
        # PRICE VALIDATION
        # ----------------------------------------------------

        try:
            price = float(price)

            if price < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Error",
                "Price must be a valid positive number"
            )
            return None

        # ----------------------------------------------------
        # DISCOUNT VALIDATION
        # ----------------------------------------------------

        try:
            discount = float(discount)

            if discount < 0 or discount > 100:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Error",
                "Discount must be between 0 and 100"
            )
            return None

        # ----------------------------------------------------
        # QUANTITY VALIDATION
        # ----------------------------------------------------

        try:
            quantity = int(quantity)

            if quantity < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Error",
                "Quantity must be a valid positive integer"
            )
            return None

        # ----------------------------------------------------
        # CALCULATE DISCOUNTED PRICE
        # ----------------------------------------------------

        discounted_price = round(price * (1 - discount / 100),2)

        return (
            category,
            supplier,
            name,
            price,
            discount,
            discounted_price,
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

        (
            category,
            supplier,
            name,
            price,
            discount,
            discounted_price,
            quantity,
            status
        ) = data

        cursor, connection = connect_database()

        if cursor is None:
            return

        try:

            # ------------------------------------------------
            # CHECK DUPLICATE PRODUCT
            # ------------------------------------------------

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

            # ------------------------------------------------
            # INSERT PRODUCT
            # ------------------------------------------------

            cursor.execute(
                """
                INSERT INTO product_data
                (
                    category,
                    supplier,
                    name,
                    price,
                    discount,
                    discounted_price,
                    quantity,
                    status
                )
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    category,
                    supplier,
                    name,
                    price,
                    discount,
                    discounted_price,
                    quantity,
                    status
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Product added successfully"
            )

            show_all_products()
            clear_fields()

        except pymysql.MySQLError as e:

            connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to add product:\n{e}"
            )

        finally:

            cursor.close()
            connection.close()

    # ========================================================
    # UPDATE PRODUCT
    # ========================================================

    def update_product():

        if selected_product_id.get() == "":

            messagebox.showerror(
                "Error",
                "Please select a product first"
            )

            return

        data = get_product_data()

        if data is None:
            return

        (
            category,
            supplier,
            name,
            price,
            discount,
            discounted_price,
            quantity,
            status
        ) = data

        product_id = selected_product_id.get()

        cursor, connection = connect_database()

        if cursor is None:
            return

        try:

            cursor.execute(
                """
                UPDATE product_data
                SET
                    category=%s,
                    supplier=%s,
                    name=%s,
                    price=%s,
                    discount=%s,
                    discounted_price=%s,
                    quantity=%s,
                    status=%s
                WHERE id=%s
                """,
                (
                    category,
                    supplier,
                    name,
                    price,
                    discount,
                    discounted_price,
                    quantity,
                    status,
                    product_id
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Product updated successfully"
            )

            show_all_products()
            clear_fields()

        except pymysql.MySQLError as e:

            connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to update product:\n{e}"
            )

        finally:

            cursor.close()
            connection.close()

    # ========================================================
    # DELETE PRODUCT
    # ========================================================

    def delete_product():

        if selected_product_id.get() == "":

            messagebox.showerror(
                "Error",
                "Please select a product first"
            )

            return

        answer = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this product?"
        )

        if not answer:
            return

        cursor, connection = connect_database()

        if cursor is None:
            return

        try:

            cursor.execute(
                """
                DELETE FROM product_data
                WHERE id=%s
                """,
                (selected_product_id.get(),)
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Product deleted successfully"
            )

            show_all_products()
            clear_fields()

        except pymysql.MySQLError as e:

            connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to delete product:\n{e}"
            )

        finally:

            cursor.close()
            connection.close()

    # ========================================================
    # CLEAR FIELDS
    # ========================================================

    def clear_fields():

        selected_product_id.set("")

        category_combobox.set("Empty")

        supplier_combobox.set("Empty")

        name_entry.delete(0, END)

        price_entry.delete(0, END)

        quantity_entry.delete(0, END)

        discount_spinbox.delete(0, END)
        discount_spinbox.insert(0, "0")

        status_combobox.set("Active")

        # Remove Treeview selection
        for item in product_treeview.selection():
            product_treeview.selection_remove(item)

    # ========================================================
    # SELECT PRODUCT FROM TREEVIEW
    # ========================================================

    def select_product(event):

        selected = product_treeview.selection()

        if not selected:
            return

        values = product_treeview.item(
            selected[0],
            "values"
        )

        if not values:
            return

        # ----------------------------------------------------
        # TREEVIEW ORDER
        # 0 = ID
        # 1 = Category
        # 2 = Supplier
        # 3 = Name
        # 4 = Price
        # 5 = Discount
        # 6 = Discounted Price
        # 7 = Quantity
        # 8 = Status
        # ----------------------------------------------------

        selected_product_id.set(values[0])

        category_combobox.set(values[1])

        supplier_combobox.set(values[2])

        name_entry.delete(0, END)
        name_entry.insert(0, values[3])

        price_entry.delete(0, END)
        price_entry.insert(0, values[4])

        discount_spinbox.delete(0, END)
        discount_spinbox.insert(0, values[5])

        quantity_entry.delete(0, END)
        quantity_entry.insert(0, values[7])

        status_combobox.set(values[8])

    # ========================================================
    # SHOW ALL PRODUCTS
    # ========================================================

    def show_all_products():

        # Clear existing rows
        for item in product_treeview.get_children():
            product_treeview.delete(item)

        cursor, connection = connect_database()

        if cursor is None:
            return

        try:

            cursor.execute(
                """
                SELECT
                    id,
                    category,
                    supplier,
                    name,
                    price,
                    discount,
                    discounted_price,
                    quantity,
                    status
                FROM product_data
                ORDER BY id DESC
                """
            )

            products = cursor.fetchall()

            for product in products:

                product_treeview.insert(
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

            cursor.close()
            connection.close()

    # ========================================================
    # SEARCH PRODUCT
    # ========================================================

    def search_product():

        search_text = search_entry.get().strip()

        search_by = search_combobox.get()

        if search_text == "":

            show_all_products()
            return

        # ----------------------------------------------------
        # SEARCH COLUMN
        # ----------------------------------------------------

        column_map = {
            "ID": "id",
            "Category": "category",
            "Supplier": "supplier",
            "Name": "name",
            "Status": "status"
        }

        column = column_map.get(search_by)

        if column is None:

            messagebox.showerror(
                "Error",
                "Invalid search option"
            )

            return

        # Clear Treeview
        for item in product_treeview.get_children():
            product_treeview.delete(item)

        cursor, connection = connect_database()

        if cursor is None:
            return

        try:

            query = f"""
                SELECT
                    id,
                    category,
                    supplier,
                    name,
                    price,
                    discount,
                    discounted_price,
                    quantity,
                    status
                FROM product_data
                WHERE {column} LIKE %s
                ORDER BY id DESC
            """

            cursor.execute(
                query,
                (f"%{search_text}%",)
            )

            products = cursor.fetchall()

            for product in products:

                product_treeview.insert(
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
                f"Search failed:\n{e}"
            )

        finally:

            cursor.close()
            connection.close()

    # ========================================================
    # SEARCH AREA
    # ========================================================

    search_frame = Frame(
        product_frame,
        bg="white"
    )

    search_frame.place(
        x=500,
        y=50,
        width=800,
        height=90
    )

    search_label = Label(
        search_frame,
        text="Search By",
        font=("times new roman", 14, "bold"),
        bg="white"
    )

    search_label.grid(
        row=0,
        column=0,
        padx=5,
        pady=5
    )

    search_combobox = ttk.Combobox(
        search_frame,
        values=(
            "ID",
            "Category",
            "Supplier",
            "Name",
            "Status"
        ),
        font=("times new roman", 13),
        state="readonly",
        width=12
    )

    search_combobox.grid(
        row=0,
        column=1,
        padx=5
    )

    search_combobox.set("Name")

    search_entry = Entry(
        search_frame,
        font=("times new roman", 13),
        bg="lightyellow"
    )

    search_entry.grid(
        row=0,
        column=2,
        padx=5,
        ipadx=30,
        ipady=3
    )

    search_button = Button(
        search_frame,
        text="Search",
        font=("times new roman", 12, "bold"),
        bg="#0f4d7d",
        fg="white",
        cursor="hand2",
        command=search_product
    )

    search_button.grid(
        row=0,
        column=3,
        padx=5
    )

    show_all_button = Button(
        search_frame,
        text="Show All",
        font=("times new roman", 12, "bold"),
        bg="#0f4d7d",
        fg="white",
        cursor="hand2",
        command=show_all_products
    )

    show_all_button.grid(
        row=0,
        column=4,
        padx=5
    )

    # ========================================================
    # BUTTON FRAME
    # ========================================================
    back_button = Button(
        product_frame,
        text="Back",
        width=10,
        # height=3,
        cursor="hand2",
        bg="white",
        command=lambda: product_frame.place_forget()
    )
    back_button.place(x=10, y=30)

    button_frame = Frame(
        product_frame,
        bg="white"
    )

    button_frame.place(
        x=20,
        y=410
    )

    add_button = Button(
        button_frame,
        text="Add",
        font=("times new roman", 12, "bold"),
        bg="#0f4d7d",
        fg="white",
        width=10,
        cursor="hand2",
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
        font=("times new roman", 12, "bold"),
        bg="#0f4d7d",
        fg="white",
        width=10,
        cursor="hand2",
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
        font=("times new roman", 12, "bold"),
        bg="#0f4d7d",
        fg="white",
        width=10,
        cursor="hand2",
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
        font=("times new roman", 12, "bold"),
        bg="#0f4d7d",
        fg="white",
        width=10,
        cursor="hand2",
        command=clear_fields
    )

    clear_button.grid(
        row=0,
        column=3,
        padx=5
    )

    # ========================================================
    # TREEVIEW FRAME
    # ========================================================

    tree_frame = Frame(
        product_frame,
        bg="white"
    )

    tree_frame.place(
        x=20,
        y=470,
        width=1280,
        height=200
    )

    # --------------------------------------------------------
    # SCROLLBAR
    # --------------------------------------------------------

    tree_scrollbar = Scrollbar(
        tree_frame,
        orient=VERTICAL
    )

    tree_scrollbar.pack(
        side=RIGHT,
        fill=Y
    )

    horizontal_scrollbar = Scrollbar(
        tree_frame,
        orient=HORIZONTAL
    )

    horizontal_scrollbar.pack(
        side=BOTTOM,
        fill=X
    )

    # ========================================================
    # TREEVIEW
    # ========================================================

    product_treeview = ttk.Treeview(
        tree_frame,
        columns=(
            "id",
            "category",
            "supplier",
            "name",
            "price",
            "discount",
            "discounted_price",
            "quantity",
            "status"
        ),
        show="headings",
        yscrollcommand=tree_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set
    )

    product_treeview.pack(
        fill=BOTH,
        expand=True
    )

    tree_scrollbar.config(
        command=product_treeview.yview
    )

    horizontal_scrollbar.config(
        command=product_treeview.xview
    )

    # ========================================================
    # TREEVIEW HEADINGS
    # ========================================================

    product_treeview.heading(
        "id",
        text="ID"
    )

    product_treeview.heading(
        "category",
        text="Category"
    )

    product_treeview.heading(
        "supplier",
        text="Supplier"
    )

    product_treeview.heading(
        "name",
        text="Product Name"
    )

    product_treeview.heading(
        "price",
        text="Price"
    )

    product_treeview.heading(
        "discount",
        text="Discount (%)"
    )

    product_treeview.heading(
        "discounted_price",
        text="Discounted Amount"
    )

    product_treeview.heading(
        "quantity",
        text="Quantity"
    )

    product_treeview.heading(
        "status",
        text="Status"
    )

    # ========================================================
    # TREEVIEW COLUMNS
    # ========================================================

    product_treeview.column(
        "id",
        width=50,
        anchor="center"
    )

    product_treeview.column(
        "category",
        width=130,
        anchor="center"
    )

    product_treeview.column(
        "supplier",
        width=130,
        anchor="center"
    )

    product_treeview.column(
        "name",
        width=150,
        anchor="center"
    )

    product_treeview.column(
        "price",
        width=100,
        anchor="center"
    )

    product_treeview.column(
        "discount",
        width=100,
        anchor="center"
    )

    product_treeview.column(
        "discounted_price",
        width=130,
        anchor="center"
    )

    product_treeview.column(
        "quantity",
        width=100,
        anchor="center"
    )

    product_treeview.column(
        "status",
        width=100,
        anchor="center"
    )

    # ========================================================
    # TREEVIEW SELECT EVENT
    # ========================================================

    product_treeview.bind(
        "<ButtonRelease-1>",
        select_product
    )

    # ========================================================
    # INITIAL DATABASE SETUP
    # ========================================================

    create_product_table()

    load_categories()

    load_suppliers()

    show_all_products()
