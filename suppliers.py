import pymysql
from tkinter import *
from tkinter import ttk, messagebox


# ============================================================
# DATABASE CONNECTION
# ============================================================

def connect_database():

    try:

        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="Sswashank@12345"
        )

        cursor = connection.cursor()

        return cursor, connection

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Database connection failed:\n{e}"
        )

        return None, None


# ============================================================
# CREATE DATABASE AND TABLE
# ============================================================

def create_database_table():

    cursor, connection = connect_database()

    if cursor is None or connection is None:
        return False

    try:

        # Create database
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS inventory_system"
        )

        # Select database
        cursor.execute(
            "USE inventory_system"
        )

        # Create supplier table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS supplier_data
            (
                invoice_no INT PRIMARY KEY,
                supplier_name VARCHAR(100) NOT NULL,
                contact VARCHAR(100) NOT NULL,
                description VARCHAR(500) NOT NULL
            )
        """)

        connection.commit()

        return True

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Error creating database/table:\n{e}"
        )

        return False

    finally:

        cursor.close()
        connection.close()


# ============================================================
# LOAD DATA INTO TREEVIEW
# ============================================================

def treeview_data():

    cursor, connection = connect_database()

    if cursor is None or connection is None:
        return

    try:

        cursor.execute(
            "USE inventory_system"
        )

        cursor.execute("""
            SELECT
                invoice_no,
                supplier_name,
                contact,
                description
            FROM supplier_data
            ORDER BY invoice_no
        """)

        records = cursor.fetchall()

        # Remove old Treeview data
        treeview.delete(
            *treeview.get_children()
        )

        # Insert new data
        for record in records:

            treeview.insert(
                "",
                END,
                values=record
            )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Error loading supplier data:\n{e}"
        )

    finally:

        cursor.close()
        connection.close()


# ============================================================
# SELECT TREEVIEW DATA
# ============================================================

def select_data(event):

    selected = treeview.selection()

    if not selected:
        return

    data = treeview.item(
        selected[0],
        "values"
    )

    if not data:
        return

    # Clear old values
    invoice_entry.delete(
        0,
        END
    )

    supplier_name_entry.delete(
        0,
        END
    )

    contact_entry.delete(
        0,
        END
    )

    description_text.delete(
        "1.0",
        END
    )

    # Insert selected values
    invoice_entry.insert(
        0,
        data[0]
    )

    supplier_name_entry.insert(
        0,
        data[1]
    )

    contact_entry.insert(
        0,
        data[2]
    )

    description_text.insert(
        "1.0",
        data[3]
    )


# ============================================================
# ADD SUPPLIER
# ============================================================

def add_supplier():

    invoice_no = invoice_entry.get().strip()
    supplier_name = supplier_name_entry.get().strip()
    contact = contact_entry.get().strip()
    description = description_text.get(
        "1.0",
        END
    ).strip()

    # ========================================================
    # VALIDATION
    # ========================================================

    if invoice_no == "":

        messagebox.showerror(
            "Error",
            "Please enter Invoice No."
        )

        invoice_entry.focus()

        return

    if supplier_name == "":

        messagebox.showerror(
            "Error",
            "Please enter Supplier Name"
        )

        supplier_name_entry.focus()

        return

    if contact == "":

        messagebox.showerror(
            "Error",
            "Please enter Contact"
        )

        contact_entry.focus()

        return

    if description == "":

        messagebox.showerror(
            "Error",
            "Please enter Description"
        )

        description_text.focus()

        return

    # ========================================================
    # CONVERT INVOICE TO INTEGER
    # ========================================================

    try:

        invoice_no = int(invoice_no)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Invoice No. must be a number"
        )

        invoice_entry.focus()

        return

    # ========================================================
    # DATABASE
    # ========================================================

    cursor, connection = connect_database()

    if cursor is None or connection is None:
        return

    try:

        cursor.execute(
            "USE inventory_system"
        )

        # Check duplicate invoice
        cursor.execute(
            """
            SELECT invoice_no
            FROM supplier_data
            WHERE invoice_no=%s
            """,
            (invoice_no,)
        )

        if cursor.fetchone():

            messagebox.showerror(
                "Error",
                "Invoice No. already exists"
            )

            return

        # Insert supplier
        cursor.execute(
            """
            INSERT INTO supplier_data
            (
                invoice_no,
                supplier_name,
                contact,
                description
            )
            VALUES
            (%s, %s, %s, %s)
            """,
            (
                invoice_no,
                supplier_name,
                contact,
                description
            )
        )

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Supplier added successfully"
        )

        treeview_data()

        clear_fields()

    except Exception as e:

        connection.rollback()

        messagebox.showerror(
            "Error",
            f"Error adding supplier:\n{e}"
        )

    finally:

        cursor.close()
        connection.close()


# ============================================================
# UPDATE SUPPLIER
# ============================================================

def update_supplier():

    selected = treeview.selection()

    if not selected:

        messagebox.showerror(
            "Error",
            "Please select a supplier from the table"
        )

        return

    invoice_no = invoice_entry.get().strip()
    supplier_name = supplier_name_entry.get().strip()
    contact = contact_entry.get().strip()
    description = description_text.get(
        "1.0",
        END
    ).strip()

    # ========================================================
    # VALIDATION
    # ========================================================

    if invoice_no == "":

        messagebox.showerror(
            "Error",
            "Please enter Invoice No."
        )

        return

    if supplier_name == "":

        messagebox.showerror(
            "Error",
            "Please enter Supplier Name"
        )

        return

    if contact == "":

        messagebox.showerror(
            "Error",
            "Please enter Contact"
        )

        return

    if description == "":

        messagebox.showerror(
            "Error",
            "Please enter Description"
        )

        return

    try:

        invoice_no = int(invoice_no)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Invoice No. must be a number"
        )

        return

    # ========================================================
    # DATABASE
    # ========================================================

    cursor, connection = connect_database()

    if cursor is None or connection is None:
        return

    try:

        cursor.execute(
            "USE inventory_system"
        )

        # Check whether supplier exists
        cursor.execute(
            """
            SELECT invoice_no
            FROM supplier_data
            WHERE invoice_no=%s
            """,
            (invoice_no,)
        )

        if not cursor.fetchone():

            messagebox.showerror(
                "Error",
                "Supplier not found"
            )

            return

        # Update supplier
        cursor.execute(
            """
            UPDATE supplier_data
            SET
                supplier_name=%s,
                contact=%s,
                description=%s
            WHERE invoice_no=%s
            """,
            (
                supplier_name,
                contact,
                description,
                invoice_no
            )
        )

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Supplier updated successfully"
        )

        treeview_data()

        clear_fields()

    except Exception as e:

        connection.rollback()

        messagebox.showerror(
            "Error",
            f"Error updating supplier:\n{e}"
        )

    finally:

        cursor.close()
        connection.close()


# ============================================================
# DELETE SUPPLIER
# ============================================================

def delete_supplier():

    selected = treeview.selection()

    if not selected:

        messagebox.showerror(
            "Error",
            "Please select a supplier first"
        )

        return

    data = treeview.item(
        selected[0],
        "values"
    )

    if not data:
        return

    invoice_no = data[0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Do you want to delete supplier\n"
        f"Invoice No.: {invoice_no}?"
    )

    if not confirm:
        return

    cursor, connection = connect_database()

    if cursor is None or connection is None:
        return

    try:

        cursor.execute(
            "USE inventory_system"
        )

        cursor.execute(
            """
            DELETE FROM supplier_data
            WHERE invoice_no=%s
            """,
            (invoice_no,)
        )

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Supplier deleted successfully"
        )

        treeview_data()

        clear_fields()

    except Exception as e:

        connection.rollback()

        messagebox.showerror(
            "Error",
            f"Error deleting supplier:\n{e}"
        )

    finally:

        cursor.close()
        connection.close()


# ============================================================
# SEARCH SUPPLIER
# ============================================================

def search_supplier():

    invoice_no = search_entry.get().strip()

    if invoice_no == "":

        messagebox.showerror(
            "Error",
            "Please enter Invoice No."
        )

        search_entry.focus()

        return

    try:

        invoice_no = int(invoice_no)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Invoice No. must be a number"
        )

        search_entry.focus()

        return

    cursor, connection = connect_database()

    if cursor is None or connection is None:
        return

    try:

        cursor.execute(
            "USE inventory_system"
        )

        cursor.execute(
            """
            SELECT
                invoice_no,
                supplier_name,
                contact,
                description
            FROM supplier_data
            WHERE invoice_no=%s
            """,
            (invoice_no,)
        )

        records = cursor.fetchall()

        # Clear Treeview
        treeview.delete(
            *treeview.get_children()
        )

        # Insert result
        for record in records:

            treeview.insert(
                "",
                END,
                values=record
            )

        if not records:

            messagebox.showinfo(
                "Search",
                "No supplier found"
            )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Search error:\n{e}"
        )

    finally:

        cursor.close()
        connection.close()


# ============================================================
# SHOW ALL
# ============================================================

def show_all():

    search_entry.delete(
        0,
        END
    )

    treeview_data()


# ============================================================
# CLEAR
# ============================================================

def clear_fields():

    invoice_entry.delete(
        0,
        END
    )

    supplier_name_entry.delete(
        0,
        END
    )

    contact_entry.delete(
        0,
        END
    )

    description_text.delete(
        "1.0",
        END
    )

    search_entry.delete(
        0,
        END
    )

    # Clear Treeview selection
    treeview.selection_remove(
        treeview.selection()
    )


# ============================================================
# SUPPLIER FORM
# ============================================================

def supplier_form(window):

    global supplier_frame

    global invoice_entry
    global supplier_name_entry
    global contact_entry
    global description_text
    global search_entry
    global treeview

    # ========================================================
    # CREATE DATABASE
    # ========================================================

    if not create_database_table():
        return

    # ========================================================
    # MAIN SUPPLIER FRAME
    # ========================================================

    supplier_frame = Frame(
        window,
        width=1330,
        height=690,
        bg="white"
    )

    supplier_frame.place(
        x=200,
        y=100
    )

    # ========================================================
    # HEADING
    # ========================================================

    heading_label = Label(
        supplier_frame,
        text="Manage Supplier Details",
        font=("times new roman", 16, "bold"),
        bg="#0f4d7d",
        fg="white"
    )

    heading_label.place(
        x=0,
        y=0,
        relwidth=1,
        height=40
    )

    # ========================================================
    # TOP FRAME
    # ========================================================

    topFrame = Frame(
        supplier_frame,
        bg="white"
    )

    topFrame.place(
        x=0,
        y=50,
        relwidth=1,
        height=245
    )

    # ========================================================
    # BACK BUTTON
    # ========================================================

    back_button = Button(
        topFrame,
        text="Back",
        width=10,
        cursor="hand2",
        bg="white",
        command=lambda: supplier_frame.place_forget()
    )

    back_button.place(
        x=10,
        y=5
    )

    # ========================================================
    # LEFT FRAME
    # ========================================================

    left_frame = Frame(
        supplier_frame,
        bg="white"
    )

    left_frame.place(
        x=10,
        y=100
    )

    # ========================================================
    # INVOICE
    # ========================================================

    invoice_label = Label(
        left_frame,
        text="Invoice No.",
        font=("times new roman", 14),
        bg="white"
    )

    invoice_label.grid(
        row=0,
        column=0,
        padx=(20, 40),
        sticky="w"
    )

    invoice_entry = Entry(
        left_frame,
        font=("times new roman", 14),
        width=22,
        bg="lightyellow"
    )

    invoice_entry.grid(
        row=0,
        column=1
    )

    # ========================================================
    # SUPPLIER NAME
    # ========================================================

    supplier_name_label = Label(
        left_frame,
        text="Supplier Name",
        font=("times new roman", 14),
        bg="white"
    )

    supplier_name_label.grid(
        row=1,
        column=0,
        padx=(20, 40),
        pady=20,
        sticky="w"
    )

    supplier_name_entry = Entry(
        left_frame,
        font=("times new roman", 14),
        width=22,
        bg="lightyellow"
    )

    supplier_name_entry.grid(
        row=1,
        column=1
    )

    # ========================================================
    # CONTACT
    # ========================================================

    contact_label = Label(
        left_frame,
        text="Contact",
        font=("times new roman", 14),
        bg="white"
    )

    contact_label.grid(
        row=2,
        column=0,
        padx=(20, 40),
        sticky="w"
    )

    contact_entry = Entry(
        left_frame,
        font=("times new roman", 14),
        width=22,
        bg="lightyellow"
    )

    contact_entry.grid(
        row=2,
        column=1
    )

    # ========================================================
    # DESCRIPTION
    # ========================================================

    description_label = Label(
        left_frame,
        text="Description",
        font=("times new roman", 14),
        bg="white"
    )

    description_label.grid(
        row=3,
        column=0,
        pady=20,
        padx=20,
        sticky="nw"
    )

    description_text = Text(
        left_frame,
        font=("times new roman", 14),
        width=22,
        height=6,
        bd=2,
        bg="lightyellow"
    )

    description_text.grid(
        row=3,
        column=1,
        pady=20
    )

    # ========================================================
    # BUTTON FRAME
    # ========================================================

    button_frame = Frame(
        left_frame,
        bg="white"
    )

    button_frame.grid(
        row=4,
        columnspan=2,
        pady=20
    )

    # ========================================================
    # ADD BUTTON
    # ========================================================

    add_button = Button(
        button_frame,
        text="Add",
        font=("times new roman", 14),
        width=8,
        cursor="hand2",
        fg="white",
        bg="#0f4d74",
        command=add_supplier
    )

    add_button.grid(
        row=0,
        column=0,
        padx=20
    )

    # ========================================================
    # UPDATE BUTTON
    # ========================================================

    update_button = Button(
        button_frame,
        text="Update",
        font=("times new roman", 14),
        width=8,
        cursor="hand2",
        fg="white",
        bg="#0f4d74",
        command=update_supplier
    )

    update_button.grid(
        row=0,
        column=1
    )

    # ========================================================
    # DELETE BUTTON
    # ========================================================

    delete_button = Button(
        button_frame,
        text="Delete",
        font=("times new roman", 14),
        width=8,
        cursor="hand2",
        fg="white",
        bg="#0f4d74",
        command=delete_supplier
    )

    delete_button.grid(
        row=0,
        column=2,
        padx=20
    )

    # ========================================================
    # CLEAR BUTTON
    # ========================================================

    clear_button = Button(
        button_frame,
        text="Clear",
        font=("times new roman", 14),
        width=8,
        cursor="hand2",
        fg="white",
        bg="#0f4d74",
        command=clear_fields
    )

    clear_button.grid(
        row=0,
        column=3
    )

    # ========================================================
    # RIGHT FRAME
    # ========================================================

    right_frame = Frame(
        supplier_frame,
        bg="white"
    )

    right_frame.place(
        x=550,
        y=70,
        width=700,
        height=500
    )

    # ========================================================
    # SEARCH FRAME
    # ========================================================

    search_frame = Frame(
        right_frame,
        bg="white"
    )

    search_frame.pack(
        pady=(0, 10)
    )

    # ========================================================
    # SEARCH LABEL
    # ========================================================

    num_label = Label(
        search_frame,
        text="Invoice No.",
        font=("times new roman", 14),
        bg="white"
    )

    num_label.grid(
        row=0,
        column=0,
        padx=(0, 15),
        sticky="w"
    )

    # ========================================================
    # SEARCH ENTRY
    # ========================================================

    search_entry = Entry(
        search_frame,
        font=("times new roman", 14),
        width=22
    )

    search_entry.grid(
        row=0,
        column=1,
        padx=15
    )

    # ========================================================
    # SEARCH BUTTON
    # ========================================================

    search_button = Button(
        search_frame,
        text="Search",
        font=("times new roman", 14),
        width=8,
        cursor="hand2",
        fg="white",
        bg="#0f4d74",
        command=search_supplier
    )

    search_button.grid(
        row=0,
        column=2,
        padx=15
    )

    # ========================================================
    # SHOW ALL BUTTON
    # ========================================================

    show_button = Button(
        search_frame,
        text="Show all",
        font=("times new roman", 14),
        width=8,
        cursor="hand2",
        fg="white",
        bg="#0f4d74",
        command=show_all
    )

    show_button.grid(
        row=0,
        column=3
    )

    # ========================================================
    # SCROLLBARS
    # ========================================================

    scrolly = Scrollbar(
        right_frame,
        orient=VERTICAL
    )

    scrollx = Scrollbar(
        right_frame,
        orient=HORIZONTAL
    )

    # ========================================================
    # TREEVIEW
    # ========================================================

    treeview = ttk.Treeview(
        right_frame,
        columns=(
            "invoice",
            "name",
            "contact",
            "description"
        ),
        show="headings",
        yscrollcommand=scrolly.set,
        xscrollcommand=scrollx.set,
        selectmode="browse"
    )

    # ========================================================
    # SCROLLBAR CONFIG
    # ========================================================

    scrolly.config(
        command=treeview.yview
    )

    scrollx.config(
        command=treeview.xview
    )

    scrolly.pack(
        side=RIGHT,
        fill=Y
    )

    scrollx.pack(
        side=BOTTOM,
        fill=X
    )

    treeview.pack(
        fill=BOTH,
        expand=True
    )

    # ========================================================
    # TREEVIEW HEADINGS
    # ========================================================

    treeview.heading(
        "invoice",
        text="Invoice Id"
    )

    treeview.heading(
        "name",
        text="Supplier Name"
    )

    treeview.heading(
        "contact",
        text="Contact"
    )

    treeview.heading(
        "description",
        text="Description"
    )

    # ========================================================
    # TREEVIEW COLUMNS
    # ========================================================

    treeview.column(
        "invoice",
        width=100,
        anchor="center"
    )

    treeview.column(
        "name",
        width=300,
        anchor="w"
    )

    treeview.column(
        "contact",
        width=240,
        anchor="center"
    )

    treeview.column(
        "description",
        width=600,
        anchor="w"
    )

    # ========================================================
    # TREEVIEW CLICK EVENT
    # ========================================================

    treeview.bind(
        "<ButtonRelease-1>",
        select_data
    )

    # ========================================================
    # ENTER KEY SEARCH
    # ========================================================

    search_entry.bind(
        "<Return>",
        lambda event: search_supplier()
    )

    # ========================================================
    # LOAD DATA
    # ========================================================

    treeview_data()