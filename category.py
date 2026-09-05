from tkinter import *

from tkinter import ttk
from tkinter import messagebox
import pymysql


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

        return connection

    except pymysql.MySQLError as e:

        messagebox.showerror(
            "Database Error",
            f"Database connection failed:\n{e}"
        )

        return None


# ============================================================
# CREATE DATABASE AND TABLE
# ============================================================

def create_database_table():

    connection = connect_database()

    if connection is None:
        return

    try:

        cursor = connection.cursor()

        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS inventory_system"
        )

        cursor.execute(
            "USE inventory_system"
        )

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS category_data
            (
                id INT PRIMARY KEY,
                category_name VARCHAR(100) NOT NULL,
                description VARCHAR(500)
            )
        """)

        connection.commit()

        cursor.close()
        connection.close()

    except pymysql.MySQLError as e:

        messagebox.showerror(
            "Database Error",
            f"Error creating database/table:\n{e}"
        )


# ============================================================
# SHOW DATA
# ============================================================

def treeview_data():

    for item in treeview.get_children():
        treeview.delete(item)

    connection = connect_database()

    if connection is None:
        return

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, category_name, description
            FROM inventory_system.category_data
            ORDER BY id
        """)

        rows = cursor.fetchall()

        for row in rows:

            treeview.insert(
                "",
                END,
                values=row
            )

        cursor.close()
        connection.close()

    except pymysql.MySQLError as e:

        messagebox.showerror(
            "Database Error",
            f"Error loading data:\n{e}"
        )


# ============================================================
# ADD CATEGORY
# ============================================================

def add_category():

    id_value = id_entry.get().strip()
    category_name = category_name_entry.get().strip()
    description = description_text.get("1.0", END).strip()

    if id_value == "":

        messagebox.showerror(
            "Error",
            "Please enter Id"
        )

        return

    if category_name == "":

        messagebox.showerror(
            "Error",
            "Please enter Category Name"
        )

        return

    try:

        id_value = int(id_value)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Id must be a number"
        )

        return

    connection = connect_database()

    if connection is None:
        return

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT id
            FROM inventory_system.category_data
            WHERE id=%s
        """, (id_value,))

        if cursor.fetchone():

            messagebox.showerror(
                "Error",
                "Category Id already exists"
            )

            cursor.close()
            connection.close()

            return

        cursor.execute("""
            INSERT INTO inventory_system.category_data
            (id, category_name, description)
            VALUES (%s, %s, %s)
        """, (
            id_value,
            category_name,
            description
        ))

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Category added successfully"
        )

        cursor.close()
        connection.close()

        clear_fields()
        treeview_data()

    except pymysql.MySQLError as e:

        messagebox.showerror(
            "Database Error",
            f"Error adding category:\n{e}"
        )


# ============================================================
# DELETE CATEGORY
# ============================================================

def delete_category():

    id_value = id_entry.get().strip()

    if id_value == "":

        messagebox.showerror(
            "Error",
            "Please select a category"
        )

        return

    try:

        id_value = int(id_value)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Invalid Id"
        )

        return

    answer = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this category?"
    )

    if not answer:
        return

    connection = connect_database()

    if connection is None:
        return

    try:

        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM inventory_system.category_data
            WHERE id=%s
        """, (id_value,))

        connection.commit()

        if cursor.rowcount == 0:

            messagebox.showerror(
                "Error",
                "Category not found"
            )

        else:

            messagebox.showinfo(
                "Success",
                "Category deleted successfully"
            )

        cursor.close()
        connection.close()

        clear_fields()
        treeview_data()

    except pymysql.MySQLError as e:

        messagebox.showerror(
            "Database Error",
            f"Error deleting category:\n{e}"
        )


# ============================================================
# CLEAR FIELDS
# ============================================================

def clear_fields():

    id_entry.delete(
        0,
        END
    )

    category_name_entry.delete(
        0,
        END
    )

    description_text.delete(
        "1.0",
        END
    )


# ============================================================
# SELECT TREEVIEW DATA
# ============================================================

def select_data(event):

    selected_item = treeview.selection()

    if not selected_item:
        return

    row = treeview.item(
        selected_item[0]
    )["values"]

    clear_fields()

    id_entry.insert(
        0,
        row[0]
    )

    category_name_entry.insert(
        0,
        row[1]
    )

    description_text.insert(
        "1.0",
        row[2]
    )


# ============================================================
# CATEGORY FORM
# ============================================================

def category_form(window):

    global id_entry
    global category_name_entry
    global description_text
    global treeview

    create_database_table()

    category_frame = Frame(
        window,
        width=1330,
        height=690,
        bg="white"
    )
    category_frame.place(x=200, y=100)

    heading_label = Label(
        category_frame,
        text="Manage Category Details",
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

    back_button = Button(
        category_frame,
        text="Back",
        width=10,
        cursor="hand2",
        bg="white",
        command=lambda: category_frame.place_forget()
    )
    back_button.place(x=10, y=50)

    details_frame = Frame(
        category_frame,
        bg="white"
    )
    details_frame.place(x=500, y=60)

    id_label = Label(
        details_frame,
        text="Id",
        font=("times new roman", 14),
        bg="white"
    )
    id_label.grid(
        row=0,
        column=0,
        padx=20,
        sticky="w"
    )

    id_entry = Entry(
        details_frame,
        font=("times new roman", 14),
        width=22,
        bg="lightyellow"
    )

    id_entry.grid(
        row=0,
        column=1
    )

    category_name_label = Label(
        details_frame,
        text="Category Name",
        font=("times new roman", 14),
        bg="white"
    )
    category_name_label.grid(
        row=1,
        column=0,
        padx=20,
        sticky="w"
    )

    category_name_entry = Entry(
        details_frame,
        font=("times new roman", 14),
        width=22,
        bg="lightyellow"
    )

    category_name_entry.grid(
        row=1,
        column=1,
        pady=20
    )

    description_label = Label(
        details_frame,
        text="Description ",
        font=("times new roman", 14),
        bg="white"
    )
    description_label.grid(
        row=2,
        column=0,
        padx=20,
        sticky="nw"
    )

    description_text = Text(
        details_frame,
        font=("times new roman", 14),
        width=22,
        height=6,
        bd=2,
        bg="lightyellow"
    )

    description_text.grid(
        row=2,
        column=1,
        pady=20
    )

    button_frame = Frame(
        category_frame,
        bg="white"
    )
    button_frame.place(x=660, y=280)

    add_button = Button(
        button_frame,
        text="Add",
        font=("times new roman", 14),
        width=8,
        cursor="hand2",
        fg="white",
        bg="#0f4d74",
        command=add_category
    )

    add_button.grid(
        row=0,
        column=0,
        pady=30
    )

    delete_button = Button(
        button_frame,
        text="Delete",
        font=("times new roman", 14),
        width=8,
        cursor="hand2",
        fg="white",
        bg="#0f4d74",
        command=delete_category
    )

    delete_button.grid(
        row=0,
        column=1,
        padx=20,
        pady=30
    )

    treeview_frame = Frame(
        category_frame,
        bg="white",
        pady=30
    )

    treeview_frame.place(
        x=530,
        y=340,
        height=350,
        width=500
    )

    scrolly = Scrollbar(
        treeview_frame,
        orient=VERTICAL
    )

    scrollx = Scrollbar(
        treeview_frame,
        orient=HORIZONTAL
    )

    treeview = ttk.Treeview(
        treeview_frame,
        columns=(
            "id",
            "name",
            "description"
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

    treeview.heading(
        "id",
        text="Id"
    )

    treeview.heading(
        "name",
        text="Name"
    )

    treeview.heading(
        "description",
        text="Description"
    )

    treeview.column(
        "id",
        width=180,
        anchor="center"
    )

    treeview.column(
        "name",
        width=300,
        anchor="w"
    )

    treeview.column(
        "description",
        width=600,
        anchor="center"
    )

    # ========================================================
    # TREEVIEW SELECT EVENT
    # ========================================================

    treeview.bind(
        "<ButtonRelease-1>",
        select_data
    )

    # ========================================================
    # LOAD DATABASE DATA
    # ========================================================

    treeview_data()