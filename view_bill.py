from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


# ============================================================
# SALES / CUSTOMER HISTORY
# ============================================================

def view_bill(window):

    # ========================================================
    # DATABASE
    # ========================================================

    DATABASE = "sales.db"


    # ========================================================
    # CREATE DATABASE AND TABLE
    # ========================================================

    def create_database():

        connection = sqlite3.connect(DATABASE)

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (

                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,

                customer_id TEXT NOT NULL,

                customer_name TEXT NOT NULL,

                items TEXT NOT NULL,

                quantity INTEGER NOT NULL DEFAULT 1,

                total_cost REAL NOT NULL,

                payment_method TEXT,

                sale_date TEXT NOT NULL,

                invoice_no TEXT

            )
        """)

        connection.commit()

        connection.close()


    create_database()


    # ========================================================
    # MAIN FRAME
    # ========================================================

    bill_frame = Frame(
        window,
        bg="white"
    )

    bill_frame.place(
        x=200,
        y=100,
        width=1330,
        height=690
    )


    # ========================================================
    # BACK BUTTON
    # ========================================================

    def back():

        bill_frame.destroy()


    # ========================================================
    # GET SELECTED SALE ID
    # ========================================================

    def get_selected_sale_id():

        selected = sales_tree.selection()

        if not selected:
            return None

        item = sales_tree.item(
            selected[0]
        )

        values = item.get("values")

        if not values:
            return None

        return values[0]


    # ========================================================
    # UPDATE RECORD COUNT
    # ========================================================

    def update_record_count():

        count = len(
            sales_tree.get_children()
        )

        record_count_label.config(
            text=f"Total Sales: {count}"
        )


    # ========================================================
    # CLEAR SALES DETAILS
    # ========================================================

    def clear_details():

        # Sale ID
        sale_id_entry.config(
            state=NORMAL
        )

        sale_id_entry.delete(
            0,
            END
        )

        sale_id_entry.config(
            state=DISABLED
        )


        # Customer ID
        customer_id_entry.delete(
            0,
            END
        )


        # Customer Name
        customer_name_entry.delete(
            0,
            END
        )


        # Items
        items_entry.delete(
            0,
            END
        )


        # Quantity
        quantity_entry.delete(
            0,
            END
        )


        # Total Cost
        total_cost_entry.delete(
            0,
            END
        )


        # Payment
        payment_combo.set(
            ""
        )


        # Date
        date_entry.delete(
            0,
            END
        )


        # Invoice
        invoice_entry.delete(
            0,
            END
        )


        # Remove Treeview selection
        selected = sales_tree.selection()

        if selected:

            sales_tree.selection_remove(
                selected
            )


    # ========================================================
    # LOAD SALES
    # ========================================================

    def load_sales():

        # Clear Treeview
        for item in sales_tree.get_children():

            sales_tree.delete(
                item
            )


        try:

            connection = sqlite3.connect(
                DATABASE
            )

            cursor = connection.cursor()


            cursor.execute("""
                SELECT
                    sale_id,
                    customer_id,
                    customer_name,
                    items,
                    quantity,
                    total_cost,
                    payment_method,
                    sale_date,
                    invoice_no

                FROM sales

                ORDER BY sale_id DESC
            """)


            records = cursor.fetchall()

            connection.close()


            # Insert records
            for record in records:

                sales_tree.insert(
                    "",
                    END,
                    values=record
                )


            update_record_count()


        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load sales:\n{e}"
            )


    # ========================================================
    # SEARCH SALES
    # ========================================================

    def search_sales():

        search_text = search_entry.get().strip()

        search_type = search_combo.get()


        if search_text == "":

            messagebox.showwarning(
                "Search",
                "Please enter something to search."
            )

            search_entry.focus()

            return


        # Clear Treeview
        for item in sales_tree.get_children():

            sales_tree.delete(
                item
            )


        try:

            connection = sqlite3.connect(
                DATABASE
            )

            cursor = connection.cursor()


            # =================================================
            # SEARCH BY SALE ID
            # =================================================

            if search_type == "Sale ID":

                cursor.execute("""
                    SELECT
                        sale_id,
                        customer_id,
                        customer_name,
                        items,
                        quantity,
                        total_cost,
                        payment_method,
                        sale_date,
                        invoice_no

                    FROM sales

                    WHERE CAST(sale_id AS TEXT) LIKE ?

                    ORDER BY sale_id DESC
                """, (
                    f"%{search_text}%",
                ))


            # =================================================
            # SEARCH BY CUSTOMER ID
            # =================================================

            elif search_type == "Customer ID":

                cursor.execute("""
                    SELECT
                        sale_id,
                        customer_id,
                        customer_name,
                        items,
                        quantity,
                        total_cost,
                        payment_method,
                        sale_date,
                        invoice_no

                    FROM sales

                    WHERE customer_id LIKE ?

                    ORDER BY sale_id DESC
                """, (
                    f"%{search_text}%",
                ))


            # =================================================
            # SEARCH BY NAME
            # =================================================

            elif search_type == "Name":

                cursor.execute("""
                    SELECT
                        sale_id,
                        customer_id,
                        customer_name,
                        items,
                        quantity,
                        total_cost,
                        payment_method,
                        sale_date,
                        invoice_no

                    FROM sales

                    WHERE customer_name LIKE ?

                    ORDER BY sale_id DESC
                """, (
                    f"%{search_text}%",
                ))


            # =================================================
            # SEARCH BY ITEMS
            # =================================================

            elif search_type == "Items":

                cursor.execute("""
                    SELECT
                        sale_id,
                        customer_id,
                        customer_name,
                        items,
                        quantity,
                        total_cost,
                        payment_method,
                        sale_date,
                        invoice_no

                    FROM sales

                    WHERE items LIKE ?

                    ORDER BY sale_id DESC
                """, (
                    f"%{search_text}%",
                ))


            # =================================================
            # SEARCH BY DATE
            # =================================================

            elif search_type == "Date":

                cursor.execute("""
                    SELECT
                        sale_id,
                        customer_id,
                        customer_name,
                        items,
                        quantity,
                        total_cost,
                        payment_method,
                        sale_date,
                        invoice_no

                    FROM sales

                    WHERE sale_date LIKE ?

                    ORDER BY sale_id DESC
                """, (
                    f"%{search_text}%",
                ))


            # =================================================
            # SEARCH ALL
            # =================================================

            else:

                cursor.execute("""
                    SELECT
                        sale_id,
                        customer_id,
                        customer_name,
                        items,
                        quantity,
                        total_cost,
                        payment_method,
                        sale_date,
                        invoice_no

                    FROM sales

                    WHERE
                        CAST(sale_id AS TEXT) LIKE ?
                        OR customer_id LIKE ?
                        OR customer_name LIKE ?
                        OR items LIKE ?
                        OR sale_date LIKE ?

                    ORDER BY sale_id DESC
                """, (
                    f"%{search_text}%",
                    f"%{search_text}%",
                    f"%{search_text}%",
                    f"%{search_text}%",
                    f"%{search_text}%"
                ))


            records = cursor.fetchall()

            connection.close()


            # Insert search results
            for record in records:

                sales_tree.insert(
                    "",
                    END,
                    values=record
                )


            update_record_count()


            # No results
            if not records:

                messagebox.showinfo(
                    "Search",
                    "No sales records found."
                )


        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to search sales:\n{e}"
            )


    # ========================================================
    # CLEAR SEARCH
    # ========================================================

    def clear_search():

        search_entry.delete(
            0,
            END
        )


        search_combo.set(
            "All"
        )


        load_sales()


        clear_details()


        search_entry.focus()


    # ========================================================
    # SHOW SELECTED SALE DETAILS
    # ========================================================

    def show_sale_details(event=None):

        selected = sales_tree.selection()


        if not selected:

            return


        item = sales_tree.item(
            selected[0]
        )


        values = item.get(
            "values"
        )


        if not values:

            return


        # ====================================================
        # SALE ID
        # ====================================================

        sale_id_entry.config(
            state=NORMAL
        )

        sale_id_entry.delete(
            0,
            END
        )

        sale_id_entry.insert(
            0,
            str(values[0])
        )

        sale_id_entry.config(
            state=DISABLED
        )


        # ====================================================
        # CUSTOMER ID
        # ====================================================

        customer_id_entry.delete(
            0,
            END
        )

        customer_id_entry.insert(
            0,
            str(values[1])
        )


        # ====================================================
        # CUSTOMER NAME
        # ====================================================

        customer_name_entry.delete(
            0,
            END
        )

        customer_name_entry.insert(
            0,
            str(values[2])
        )


        # ====================================================
        # ITEMS
        # ====================================================

        items_entry.delete(
            0,
            END
        )

        items_entry.insert(
            0,
            str(values[3])
        )


        # ====================================================
        # QUANTITY
        # ====================================================

        quantity_entry.delete(
            0,
            END
        )

        quantity_entry.insert(
            0,
            str(values[4])
        )


        # ====================================================
        # TOTAL COST
        # ====================================================

        total_cost_entry.delete(
            0,
            END
        )

        total_cost_entry.insert(
            0,
            str(values[5])
        )


        # ====================================================
        # PAYMENT METHOD
        # ====================================================

        payment_combo.set(
            str(values[6]) if values[6] else ""
        )


        # ====================================================
        # DATE
        # ====================================================

        date_entry.delete(
            0,
            END
        )

        date_entry.insert(
            0,
            str(values[7])
        )


        # ====================================================
        # INVOICE
        # ====================================================

        invoice_entry.delete(
            0,
            END
        )

        invoice_entry.insert(
            0,
            str(values[8]) if values[8] else ""
        )


    # ========================================================
    # ADD SALE
    # ========================================================

    def add_sale():

        customer_id = customer_id_entry.get().strip()

        customer_name = customer_name_entry.get().strip()

        items = items_entry.get().strip()

        quantity = quantity_entry.get().strip()

        total_cost = total_cost_entry.get().strip()

        payment_method = payment_combo.get().strip()

        sale_date = date_entry.get().strip()

        invoice_no = invoice_entry.get().strip()


        # ====================================================
        # VALIDATION
        # ====================================================

        if customer_id == "":

            messagebox.showwarning(
                "Validation",
                "Please enter Customer ID."
            )

            customer_id_entry.focus()

            return


        if customer_name == "":

            messagebox.showwarning(
                "Validation",
                "Please enter Customer Name."
            )

            customer_name_entry.focus()

            return


        if items == "":

            messagebox.showwarning(
                "Validation",
                "Please enter Items."
            )

            items_entry.focus()

            return


        if quantity == "":

            messagebox.showwarning(
                "Validation",
                "Please enter Quantity."
            )

            quantity_entry.focus()

            return


        if total_cost == "":

            messagebox.showwarning(
                "Validation",
                "Please enter Total Cost."
            )

            total_cost_entry.focus()

            return


        if sale_date == "":

            messagebox.showwarning(
                "Validation",
                "Please enter Sale Date."
            )

            date_entry.focus()

            return


        # ====================================================
        # VALIDATE QUANTITY
        # ====================================================

        try:

            quantity = int(
                quantity
            )

            if quantity <= 0:

                raise ValueError


        except ValueError:

            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a positive whole number."
            )

            quantity_entry.focus()

            return


        # ====================================================
        # VALIDATE TOTAL COST
        # ====================================================

        try:

            total_cost = float(
                total_cost
            )

            if total_cost < 0:

                raise ValueError


        except ValueError:

            messagebox.showerror(
                "Invalid Total Cost",
                "Total Cost must be a valid number."
            )

            total_cost_entry.focus()

            return


        # ====================================================
        # INSERT INTO DATABASE
        # ====================================================

        try:

            connection = sqlite3.connect(
                DATABASE
            )

            cursor = connection.cursor()


            cursor.execute("""
                INSERT INTO sales (
                    customer_id,
                    customer_name,
                    items,
                    quantity,
                    total_cost,
                    payment_method,
                    sale_date,
                    invoice_no
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                customer_id,
                customer_name,
                items,
                quantity,
                total_cost,
                payment_method,
                sale_date,
                invoice_no
            ))


            connection.commit()

            connection.close()


            messagebox.showinfo(
                "Success",
                "Sale added successfully."
            )


            clear_details()

            load_sales()


        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to add sale:\n{e}"
            )


    # ========================================================
    # UPDATE SALE
    # ========================================================

    def update_sale():

        # ====================================================
        # GET SELECTED TREEVIEW ROW
        # ====================================================

        sale_id = get_selected_sale_id()


        if sale_id is None:

            messagebox.showwarning(
                "Update",
                "Please select a sale from the Treeview first."
            )

            return


        # ====================================================
        # GET FORM DATA
        # ====================================================

        customer_id = customer_id_entry.get().strip()

        customer_name = customer_name_entry.get().strip()

        items = items_entry.get().strip()

        quantity = quantity_entry.get().strip()

        total_cost = total_cost_entry.get().strip()

        payment_method = payment_combo.get().strip()

        sale_date = date_entry.get().strip()

        invoice_no = invoice_entry.get().strip()


        # ====================================================
        # VALIDATION
        # ====================================================

        if customer_id == "":

            messagebox.showwarning(
                "Validation",
                "Please enter Customer ID."
            )

            return


        if customer_name == "":

            messagebox.showwarning(
                "Validation",
                "Please enter Customer Name."
            )

            return


        if items == "":

            messagebox.showwarning(
                "Validation",
                "Please enter Items."
            )

            return


        if quantity == "":

            messagebox.showwarning(
                "Validation",
                "Please enter Quantity."
            )

            return


        if total_cost == "":

            messagebox.showwarning(
                "Validation",
                "Please enter Total Cost."
            )

            return


        if sale_date == "":

            messagebox.showwarning(
                "Validation",
                "Please enter Sale Date."
            )

            return


        # ====================================================
        # VALIDATE QUANTITY
        # ====================================================

        try:

            quantity = int(
                quantity
            )

            if quantity <= 0:

                raise ValueError


        except ValueError:

            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a positive whole number."
            )

            return


        # ====================================================
        # VALIDATE TOTAL COST
        # ====================================================

        try:

            total_cost = float(
                total_cost
            )

            if total_cost < 0:

                raise ValueError


        except ValueError:

            messagebox.showerror(
                "Invalid Total Cost",
                "Total Cost must be a valid number."
            )

            return


        # ====================================================
        # CONFIRM UPDATE
        # ====================================================

        confirm = messagebox.askyesno(
            "Confirm Update",
            f"Are you sure you want to update Sale ID {sale_id}?"
        )


        if not confirm:

            return


        # ====================================================
        # UPDATE DATABASE
        # ====================================================

        try:

            connection = sqlite3.connect(
                DATABASE
            )

            cursor = connection.cursor()


            cursor.execute("""
                UPDATE sales

                SET
                    customer_id = ?,
                    customer_name = ?,
                    items = ?,
                    quantity = ?,
                    total_cost = ?,
                    payment_method = ?,
                    sale_date = ?,
                    invoice_no = ?

                WHERE sale_id = ?
            """, (
                customer_id,
                customer_name,
                items,
                quantity,
                total_cost,
                payment_method,
                sale_date,
                invoice_no,
                sale_id
            ))


            updated_rows = cursor.rowcount


            connection.commit()

            connection.close()


            if updated_rows == 0:

                messagebox.showerror(
                    "Update Error",
                    f"Sale ID {sale_id} was not found."
                )

                return


            messagebox.showinfo(
                "Success",
                f"Sale ID {sale_id} updated successfully."
            )


            clear_details()

            load_sales()


        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to update sale:\n{e}"
            )


    # ========================================================
    # DELETE SALE
    # ========================================================

    def delete_sale():

        # ====================================================
        # GET SELECTED TREEVIEW ROW
        # ====================================================

        sale_id = get_selected_sale_id()


        if sale_id is None:

            messagebox.showwarning(
                "Delete",
                "Please select a sale from the Treeview first."
            )

            return


        # ====================================================
        # CONFIRM DELETE
        # ====================================================

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete Sale ID {sale_id}?\n\n"
            "This action cannot be undone."
        )


        if not confirm:

            return


        # ====================================================
        # DELETE FROM DATABASE
        # ====================================================

        try:

            connection = sqlite3.connect(
                DATABASE
            )

            cursor = connection.cursor()


            cursor.execute("""
                DELETE FROM sales

                WHERE sale_id = ?
            """, (
                sale_id,
            ))


            deleted_rows = cursor.rowcount


            connection.commit()

            connection.close()


            # =================================================
            # CHECK DELETE
            # =================================================

            if deleted_rows == 0:

                messagebox.showerror(
                    "Delete Error",
                    f"Sale ID {sale_id} was not found in the database."
                )

                return


            # =================================================
            # SUCCESS
            # =================================================

            messagebox.showinfo(
                "Success",
                f"Sale ID {sale_id} deleted successfully."
            )


            clear_details()

            load_sales()


        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to delete sale:\n{e}"
            )


    # ========================================================
    # HEADING
    # ========================================================

    heading_label = Label(
        bill_frame,
        text="Sales & Customer History",
        font=(
            "times new roman",
            25,
            "bold"
        ),
        bg="#0f4d7d",
        fg="white"
    )

    heading_label.pack(
        fill=X
    )


    # ========================================================
    # BACK BUTTON
    # ========================================================

    back_button = Button(
        bill_frame,
        text="←",
        font=(
            "Arial",
            28
        ),
        bg="white",
        fg="black",
        bd=0,
        activebackground="white",
        cursor="hand2",
        command=back
    )

    back_button.place(
        x=5,
        y=45
    )


    # ========================================================
    # SEARCH FRAME
    # ========================================================

    search_frame = Frame(
        bill_frame,
        bg="white"
    )

    search_frame.place(
        x=30,
        y=85,
        width=970,
        height=75
    )


    # ========================================================
    # SEARCH LABEL
    # ========================================================

    search_label = Label(
        search_frame,
        text="Search By",
        font=(
            "times new roman",
            15,
            "bold"
        ),
        bg="white"
    )

    search_label.place(
        x=10,
        y=15
    )


    # ========================================================
    # SEARCH COMBOBOX
    # ========================================================

    search_combo = ttk.Combobox(
        search_frame,
        values=[
            "All",
            "Sale ID",
            "Customer ID",
            "Name",
            "Items",
            "Date"
        ],
        font=(
            "times new roman",
            14
        ),
        state="readonly"
    )

    search_combo.set(
        "All"
    )

    search_combo.place(
        x=105,
        y=10,
        width=150,
        height=38
    )


    # ========================================================
    # SEARCH ENTRY
    # ========================================================

    search_entry = Entry(
        search_frame,
        font=(
            "times new roman",
            15
        ),
        bg="#ffffe0",
        fg="black",
        bd=1,
        relief=SOLID
    )

    search_entry.place(
        x=270,
        y=10,
        width=290,
        height=40
    )


    # ========================================================
    # SEARCH BUTTON
    # ========================================================

    search_button = Button(
        search_frame,
        text="Search",
        font=(
            "times new roman",
            14,
            "bold"
        ),
        bg="#0f4d7d",
        fg="white",
        activebackground="#083b5c",
        activeforeground="white",
        bd=2,
        cursor="hand2",
        command=search_sales
    )

    search_button.place(
        x=575,
        y=7,
        width=115,
        height=45
    )


    # ========================================================
    # CLEAR SEARCH BUTTON
    # ========================================================

    clear_search_button = Button(
        search_frame,
        text="Clear",
        font=(
            "times new roman",
            14,
            "bold"
        ),
        bg="#6c757d",
        fg="white",
        activebackground="#5c636a",
        activeforeground="white",
        bd=0,
        cursor="hand2",
        command=clear_search
    )

    clear_search_button.place(
        x=705,
        y=7,
        width=115,
        height=45
    )


    # ========================================================
    # RECORD COUNT
    # ========================================================

    record_count_label = Label(
        search_frame,
        text="Total Sales: 0",
        font=(
            "times new roman",
            13,
            "bold"
        ),
        bg="white",
        fg="#0f4d7d"
    )

    record_count_label.place(
        x=835,
        y=17
    )


    # ========================================================
    # TREEVIEW FRAME
    # ========================================================

    tree_frame = Frame(
        bill_frame,
        bg="white",
        bd=1,
        relief=SOLID
    )

    tree_frame.place(
        x=30,
        y=170,
        width=970,
        height=270
    )


    # ========================================================
    # TREEVIEW VERTICAL SCROLLBAR
    # ========================================================

    tree_scroll_y = Scrollbar(
        tree_frame,
        orient=VERTICAL
    )

    tree_scroll_y.pack(
        side=RIGHT,
        fill=Y
    )


    # ========================================================
    # TREEVIEW HORIZONTAL SCROLLBAR
    # ========================================================

    tree_scroll_x = Scrollbar(
        tree_frame,
        orient=HORIZONTAL
    )

    tree_scroll_x.pack(
        side=BOTTOM,
        fill=X
    )


    # ========================================================
    # TREEVIEW COLUMNS
    # ========================================================

    columns = (
        "Sale ID",
        "Customer ID",
        "Name",
        "Items",
        "Quantity",
        "Total Cost",
        "Payment",
        "Date",
        "Invoice"
    )


    sales_tree = ttk.Treeview(
        tree_frame,
        columns=columns,
        show="headings",
        yscrollcommand=tree_scroll_y.set,
        xscrollcommand=tree_scroll_x.set,
        selectmode="browse"
    )


    tree_scroll_y.config(
        command=sales_tree.yview
    )


    tree_scroll_x.config(
        command=sales_tree.xview
    )


    # ========================================================
    # TREEVIEW HEADINGS
    # ========================================================

    sales_tree.heading(
        "Sale ID",
        text="Sale ID"
    )

    sales_tree.heading(
        "Customer ID",
        text="Customer ID"
    )

    sales_tree.heading(
        "Name",
        text="Customer Name"
    )

    sales_tree.heading(
        "Items",
        text="Items Bought"
    )

    sales_tree.heading(
        "Quantity",
        text="Qty"
    )

    sales_tree.heading(
        "Total Cost",
        text="Total Cost"
    )

    sales_tree.heading(
        "Payment",
        text="Payment Method"
    )

    sales_tree.heading(
        "Date",
        text="Sale Date"
    )

    sales_tree.heading(
        "Invoice",
        text="Invoice No."
    )


    # ========================================================
    # TREEVIEW COLUMN WIDTH
    # ========================================================

    sales_tree.column(
        "Sale ID",
        width=70,
        anchor=CENTER
    )

    sales_tree.column(
        "Customer ID",
        width=100,
        anchor=CENTER
    )

    sales_tree.column(
        "Name",
        width=180,
        anchor=W
    )

    sales_tree.column(
        "Items",
        width=300,
        anchor=W
    )

    sales_tree.column(
        "Quantity",
        width=120,
        anchor=CENTER
    )

    sales_tree.column(
        "Total Cost",
        width=110,
        anchor=E
    )

    sales_tree.column(
        "Payment",
        width=120,
        anchor=CENTER
    )

    sales_tree.column(
        "Date",
        width=110,
        anchor=CENTER
    )

    sales_tree.column(
        "Invoice",
        width=200,
        anchor=CENTER
    )


    sales_tree.pack(
        fill=BOTH,
        expand=True
    )


    # ========================================================
    # TREEVIEW STYLE
    # ========================================================

    style = ttk.Style()

    style.configure(
        "Treeview",
        font=(
            "times new roman",
            11
        ),
        rowheight=30,
        background="white",
        foreground="black",
        fieldbackground="white"
    )

    style.configure(
        "Treeview.Heading",
        font=(
            "times new roman",
            10,
            "bold"
        ),
        background="#0f4d7d",
        foreground="black"
    )

    style.map(
        "Treeview",
        background=[
            ("selected", "#0f4d7d")
        ],
        foreground=[
            ("selected", "black")
        ]
    )


    # ========================================================
    # TREEVIEW SELECT EVENT
    # ========================================================

    sales_tree.bind(
        "<<TreeviewSelect>>",
        show_sale_details
    )


    # ========================================================
    # SALES DETAILS FRAME
    # ========================================================

    details_frame = Frame(
        bill_frame,
        bg="white",
        bd=1,
        relief=SOLID
    )

    details_frame.place(
        x=30,
        y=455,
        width=970,
        height=220
    )


    # ========================================================
    # SALES DETAILS HEADING
    # ========================================================

    details_heading = Label(
        details_frame,
        text="Sales Details",
        font=(
            "times new roman",
            17,
            "bold"
        ),
        bg="#0f4d7d",
        fg="white"
    )

    details_heading.pack(
        fill=X
    )


    # ========================================================
    # SALE ID
    # ========================================================

    Label(
        details_frame,
        text="Sale ID",
        font=(
            "times new roman",
            13,
            "bold"
        ),
        bg="white"
    ).place(
        x=15,
        y=50
    )


    sale_id_entry = Entry(
        details_frame,
        font=(
            "times new roman",
            13
        ),
        bg="#e8e8e8",
        fg="black",
        bd=1,
        relief=SOLID
    )

    sale_id_entry.place(
        x=105,
        y=47,
        width=120,
        height=32
    )

    sale_id_entry.config(
        state=DISABLED
    )


    # ========================================================
    # CUSTOMER ID
    # ========================================================

    Label(
        details_frame,
        text="Customer ID",
        font=(
            "times new roman",
            13,
            "bold"
        ),
        bg="white"
    ).place(
        x=15,
        y=95
    )


    customer_id_entry = Entry(
        details_frame,
        font=(
            "times new roman",
            13
        ),
        bg="#ffffe0",
        fg="black",
        bd=1,
        relief=SOLID
    )

    customer_id_entry.place(
        x=105,
        y=92,
        width=120,
        height=32
    )


    # ========================================================
    # CUSTOMER NAME
    # ========================================================

    Label(
        details_frame,
        text="Name",
        font=(
            "times new roman",
            13,
            "bold"
        ),
        bg="white"
    ).place(
        x=15,
        y=140
    )


    customer_name_entry = Entry(
        details_frame,
        font=(
            "times new roman",
            13
        ),
        bg="#ffffe0",
        fg="black",
        bd=1,
        relief=SOLID
    )

    customer_name_entry.place(
        x=105,
        y=137,
        width=120,
        height=32
    )


    # ========================================================
    # PAYMENT
    # ========================================================

    Label(
        details_frame,
        text="Payment",
        font=(
            "times new roman",
            13,
            "bold"
        ),
        bg="white"
    ).place(
        x=240,
        y=50
    )


    payment_combo = ttk.Combobox(
        details_frame,
        values=[
            "Cash",
            "Card",
            "eSewa",
            "Khalti",
            "Bank",
            "Other"
        ],
        font=(
            "times new roman",
            12
        ),
        state="readonly"
    )

    payment_combo.place(
        x=315,
        y=47,
        width=130,
        height=32
    )


    # ========================================================
    # DATE
    # ========================================================

    Label(
        details_frame,
        text="Date",
        font=(
            "times new roman",
            13,
            "bold"
        ),
        bg="white"
    ).place(
        x=240,
        y=95
    )


    date_entry = Entry(
        details_frame,
        font=(
            "times new roman",
            13
        ),
        bg="#ffffe0",
        fg="black",
        bd=1,
        relief=SOLID
    )

    date_entry.place(
        x=315,
        y=92,
        width=130,
        height=32
    )


    # ========================================================
    # INVOICE
    # ========================================================

    Label(
        details_frame,
        text="Invoice",
        font=(
            "times new roman",
            13,
            "bold"
        ),
        bg="white"
    ).place(
        x=240,
        y=140
    )


    invoice_entry = Entry(
        details_frame,
        font=(
            "times new roman",
            13
        ),
        bg="#ffffe0",
        fg="black",
        bd=1,
        relief=SOLID
    )

    invoice_entry.place(
        x=315,
        y=137,
        width=130,
        height=32
    )


    # ========================================================
    # ITEMS
    # ========================================================

    Label(
        details_frame,
        text="Items",
        font=(
            "times new roman",
            13,
            "bold"
        ),
        bg="white"
    ).place(
        x=470,
        y=50
    )


    items_entry = Entry(
        details_frame,
        font=(
            "times new roman",
            13
        ),
        bg="#ffffe0",
        fg="black",
        bd=1,
        relief=SOLID
    )

    items_entry.place(
        x=540,
        y=47,
        width=400,
        height=32
    )


    # ========================================================
    # QUANTITY
    # ========================================================

    Label(
        details_frame,
        text="Quantity",
        font=(
            "times new roman",
            13,
            "bold"
        ),
        bg="white"
    ).place(
        x=470,
        y=95
    )


    quantity_entry = Entry(
        details_frame,
        font=(
            "times new roman",
            13
        ),
        bg="#ffffe0",
        fg="black",
        bd=1,
        relief=SOLID
    )

    quantity_entry.place(
        x=540,
        y=92,
        width=120,
        height=32
    )


    # ========================================================
    # TOTAL COST
    # ========================================================

    Label(
        details_frame,
        text="Total Cost",
        font=(
            "times new roman",
            13,
            "bold"
        ),
        bg="white"
    ).place(
        x=680,
        y=95
    )


    total_cost_entry = Entry(
        details_frame,
        font=(
            "times new roman",
            13,
            "bold"
        ),
        bg="#e8f5e9",
        fg="green",
        bd=1,
        relief=SOLID
    )

    total_cost_entry.place(
        x=775,
        y=92,
        width=165,
        height=32
    )


    # ========================================================
    # ADD BUTTON
    # ========================================================

    add_button = Button(
        details_frame,
        text="Add",
        font=(
            "times new roman",
            12,
            "bold"
        ),
        bg="#198754",
        fg="white",
        activebackground="#146c43",
        activeforeground="white",
        bd=0,
        cursor="hand2",
        command=add_sale
    )

    add_button.place(
        x=470,
        y=175,
        width=105,
        height=35
    )


    # ========================================================
    # UPDATE BUTTON
    # ========================================================

    update_button = Button(
        details_frame,
        text="Update",
        font=(
            "times new roman",
            12,
            "bold"
        ),
        bg="#0d6efd",
        fg="white",
        activebackground="#0a58ca",
        activeforeground="white",
        bd=0,
        cursor="hand2",
        command=update_sale
    )

    update_button.place(
        x=585,
        y=175,
        width=105,
        height=35
    )


    # ========================================================
    # DELETE BUTTON
    # ========================================================

    delete_button = Button(
        details_frame,
        text="Delete",
        font=(
            "times new roman",
            12,
            "bold"
        ),
        bg="#dc3545",
        fg="white",
        activebackground="#b02a37",
        activeforeground="white",
        bd=0,
        cursor="hand2",
        command=delete_sale
    )

    delete_button.place(
        x=700,
        y=175,
        width=105,
        height=35
    )


    # ========================================================
    # CLEAR DETAILS BUTTON
    # ========================================================

    clear_details_button = Button(
        details_frame,
        text="Clear",
        font=(
            "times new roman",
            12,
            "bold"
        ),
        bg="#6c757d",
        fg="white",
        activebackground="#5c636a",
        activeforeground="white",
        bd=0,
        cursor="hand2",
        command=clear_details
    )

    clear_details_button.place(
        x=815,
        y=175,
        width=105,
        height=35
    )


    # ========================================================
    # LOAD SALES WHEN WINDOW OPENS
    # ========================================================

    load_sales()


    # ========================================================
    # ENTER KEY = SEARCH
    # ========================================================

    search_entry.bind(
        "<Return>",
        lambda event: search_sales()
    )


    # ========================================================
    # FOCUS SEARCH
    # ========================================================

    search_entry.focus()
