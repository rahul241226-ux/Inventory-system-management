
from tkinter import *

from datetime import datetime
from PIL import Image, ImageTk

from employees import employee_form
from suppliers import supplier_form
from category import category_form
from products import product_form
from employees import connect_database
from view_bill import view_bill
# from dashboard import open_dashboard

# from login import login

from tkinter import ttk, messagebox


# ============================================================
# FUNCTIONALITY PART
# ============================================================


# ============================================================
# TAX WINDOW
# ============================================================

def open_dashboard():
    global window

    window = Tk()
    window.title("Dashboard")
    window.geometry("1530x880+0+0")

    # all your dashboard code here

    window.mainloop()


def exit_app():
    result = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )

    if result:
        window.destroy()



def tax_window():

    def save_tax():

        value = tax_count.get()

        cursor, connection = connect_database()

        if cursor is None or connection is None:
            return

        try:

            cursor.execute("USE inventory_system")

            # Create tax table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tax_table (
                    id INT PRIMARY KEY,
                    tax DECIMAL(5,2)
                )
            """)

            # Check whether tax already exists
            cursor.execute(
                "SELECT id FROM tax_table WHERE id = %s",
                (1,)
            )

            if cursor.fetchone():

                # Update existing tax
                cursor.execute(
                    """
                    UPDATE tax_table
                    SET tax = %s
                    WHERE id = %s
                    """,
                    (value, 1)
                )

            else:

                # Insert new tax
                cursor.execute(
                    """
                    INSERT INTO tax_table
                    (id, tax)
                    VALUES (%s, %s)
                    """,
                    (1, value)
                )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Tax saved successfully",
                parent=tax_root
            )

        except Exception as e:

            connection.rollback()

            messagebox.showerror(
                "Error",
                f"Database error: {e}",
                parent=tax_root
            )

        finally:

            cursor.close()
            connection.close()

    # --------------------------------------------------------
    # TAX WINDOW
    # --------------------------------------------------------

    tax_root = Toplevel(window)

    tax_root.title("Tax Calculator")

    tax_root.geometry("300x300")

    tax_root.grab_set()

    tax_percentage = Label(
        tax_root,
        text="Enter Tax Percentage (%)",
        font=("arial", 12)
    )

    tax_percentage.pack(pady=10)

    tax_count = Spinbox(
        tax_root,
        from_=0,
        to=100,
        font=("arial", 12)
    )

    tax_count.pack(pady=10)

    save_button = Button(
        tax_root,
        text="Save",
        font=("arial", 12, "bold"),
        command=save_tax
    )

    save_button.pack(pady=10)


# ============================================================
# SHOW FORM
# ============================================================

current_frame = None


def show_form(form_function):

    global current_frame

    if current_frame:
        current_frame.place_forget()

    current_frame = form_function(window)


# ============================================================
# MAIN WINDOW
# ============================================================

window = Tk()

window.title("Dashboard")

window.geometry("1530x880+0+0")

window.resizable(0, 0)

window.config(bg="white")


# ============================================================
# HEADER IMAGE
# ============================================================

image = Image.open(
    "icons/checklist.png"
)

image = image.resize(
    (64, 64)
)

bg_Image = ImageTk.PhotoImage(
    image
)


# ============================================================
# HEADER LABEL
# ============================================================

titleLabel = Label(
    window,
    image=bg_Image,
    compound=LEFT,
    text="  Inventory management system",
    font=("times new roman", 40, "bold"),
    bg="#010c48",
    fg="white",
    anchor="w",
    padx=20
)

titleLabel.place(
    x=0,
    y=0,
    relwidth=1
)


# ============================================================
# LOGOUT BUTTON
# ============================================================

# logoutButton = Button(
#     window,
#     text="Logout",
#     font=("times new roman", 20, "bold"),
#     fg="#010c48"
# )
#
# logoutButton.place(
#     x=1350,
#     y=10
# )


# ============================================================
# SUBTITLE
# ============================================================

subtitlelabel = Label(
    window,
    font=("times new roman", 12),
    bg="#4d636d",
    fg="white"
)

subtitlelabel.place(
    x=0,
    y=70,
    relwidth=1
)


# ============================================================
# DATE AND TIME
# ============================================================

def update_datetime():

    now = datetime.now()

    current_date = now.strftime(
        "%d-%m-%Y"
    )

    current_time = now.strftime(
        "%I:%M:%S %p"
    )

    subtitlelabel.config(
        text=f"Welcome Admin\t\t Date: {current_date}\t\t Time: {current_time}"
    )

    subtitlelabel.after(
        1000,
        update_datetime
    )


update_datetime()


# ============================================================
# DASHBOARD COUNT FUNCTION
# ============================================================

def update_dashboard_counts():

    cursor = None
    connection = None

    try:

        cursor, connection = connect_database()

        if cursor is None or connection is None:
            window.after(
                2000,
                update_dashboard_counts
            )
            return

        cursor.execute(
            "USE inventory_system"
        )

        # ----------------------------------------------------
        # TOTAL EMPLOYEES
        # ----------------------------------------------------

        cursor.execute(
            "SELECT COUNT(*) FROM employee_data"
        )

        employee_result = cursor.fetchone()

        employee_count = employee_result[0] if employee_result else 0


        # ----------------------------------------------------
        # TOTAL SUPPLIERS
        # ----------------------------------------------------

        cursor.execute(
            "SELECT COUNT(*) FROM supplier_data"
        )

        supplier_result = cursor.fetchone()

        supplier_count = supplier_result[0] if supplier_result else 0


        # ----------------------------------------------------
        # TOTAL CATEGORIES
        # ----------------------------------------------------

        cursor.execute(
            "SELECT COUNT(*) FROM category_data"
        )

        category_result = cursor.fetchone()

        category_count = category_result[0] if category_result else 0


        # ----------------------------------------------------
        # TOTAL PRODUCTS
        # ----------------------------------------------------

        cursor.execute(
            "SELECT COUNT(*) FROM product_data"
        )

        product_result = cursor.fetchone()

        product_count = product_result[0] if product_result else 0


        # ----------------------------------------------------
        # TOTAL SALES
        # ----------------------------------------------------

        # Change sales_data if your sales table has another name.

        try:

            cursor.execute(
                "SELECT COUNT(*) FROM sales_data"
            )

            sales_result = cursor.fetchone()

            sales_count = sales_result[0] if sales_result else 0

        except Exception:

            # If sales_data table does not exist yet,
            # display 0 instead of showing an error.

            sales_count = 0


        # ====================================================
        # UPDATE DASHBOARD LABELS
        # ====================================================

        emp_icon_count_label.config(
            text=str(employee_count)
        )

        supp_icon_count_label.config(
            text=str(supplier_count)
        )

        cat_icon_count_label.config(
            text=str(category_count)
        )

        prod_icon_count_label.config(
            text=str(product_count)
        )

        sale_icon_count_label.config(
            text=str(sales_count)
        )

    except Exception as e:

        print(
            "Dashboard count error:",
            e
        )

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


    # --------------------------------------------------------
    # UPDATE AGAIN AFTER 1 SECOND
    # --------------------------------------------------------

    window.after(
        1000,
        update_dashboard_counts
    )


# ============================================================
# LEFT SIDE BAR
# ============================================================

leftframe = Frame(
    window
)

leftframe.place(
    x=0,
    y=102,
    width=200,
    height=790
)


# ============================================================
# LOGO IMAGE
# ============================================================

logoimage = Image.open(
    "icons/list.png"
)

logoimage = logoimage.resize(
    (64, 64)
)

logoimage = ImageTk.PhotoImage(
    logoimage
)

imageLabel = Label(
    leftframe,
    image=logoimage
)

imageLabel.pack()


# ============================================================
# EMPLOYEE BUTTON
# ============================================================

employee_icon = Image.open(
    "icons/employee.png"
)

employee_icon = employee_icon.resize(
    (24, 24)
)

employee_icon = ImageTk.PhotoImage(
    employee_icon)


employee_button = Button(
    leftframe,
    image=employee_icon,
    compound=LEFT,
    text=" Employee",
    font=("times new roman", 20, "bold"),
    anchor="w",
    padx=10,
    command=lambda: show_form(employee_form)
)

employee_button.pack(
    fill=X
)


# ============================================================
# SUPPLIER BUTTON
# ============================================================

supplier_icon = Image.open(
    "icons/supplier.png"
)

supplier_icon = supplier_icon.resize(
    (24, 24)
)

supplier_icon = ImageTk.PhotoImage(
    supplier_icon
)


supplier_button = Button(
    leftframe,
    image=supplier_icon,
    compound=LEFT,
    text=" Supplier",
    font=("times new roman", 20, "bold"),
    anchor="w",
    padx=10,
    command=lambda: show_form(supplier_form)
)

supplier_button.pack(
    fill=X
)


# ============================================================
# CATEGORY BUTTON
# ============================================================

category_icon = Image.open(
    "icons/catagory.png"
)

category_icon = category_icon.resize(
    (24, 24)
)

category_icon = ImageTk.PhotoImage(
    category_icon
)


category_button = Button(
    leftframe,
    image=category_icon,
    compound=LEFT,
    text=" Category",
    font=("times new roman", 20, "bold"),
    anchor="w",
    padx=10,
    command=lambda: show_form(category_form)
)

category_button.pack(
    fill=X
)


# ============================================================
# PRODUCT BUTTON
# ============================================================

product_icon = Image.open(
    "icons/product.png"
)

product_icon = product_icon.resize(
    (24, 24)
)

product_icon = ImageTk.PhotoImage(
    product_icon
)


product_button = Button(
    leftframe,
    image=product_icon,
    compound=LEFT,
    text=" Product",
    font=("times new roman", 20, "bold"),
    anchor="w",
    padx=10,
    command=lambda: show_form(product_form)
)

product_button.pack(
    fill=X
)


# ============================================================
# SALES BUTTON
# ============================================================

sales_icon = Image.open(
    "icons/sales.png"
)

sales_icon = sales_icon.resize(
    (24, 24)
)

sales_icon = ImageTk.PhotoImage(
    sales_icon
)


sales_button = Button(
    leftframe,
    image=sales_icon,
    compound=LEFT,
    text=" Sales",
    font=("times new roman", 20, "bold"),
    anchor="w",
    padx=10, command=lambda: view_bill(window)
)

sales_button.pack(
    fill=X
)


# ============================================================
# TAX BUTTON
# ============================================================

# tax_icon = Image.open(
#     "icons/tax.png"
# )
#
# tax_icon = tax_icon.resize(
#     (24, 24)
# )
#
# tax_icon = ImageTk.PhotoImage(
#     tax_icon
# )
#
#
# tax_button = Button(
#     leftframe,
#     image=tax_icon,
#     compound=LEFT,
#     text=" Tax",
#     font=("times new roman", 20, "bold"),
#     anchor="w",
#     padx=10,
#     command=tax_window
# )
#
# tax_button.pack(
#     fill=X
# )


# ============================================================
# EXIT BUTTON
# ============================================================

exit_icon = Image.open(
    "icons/exit.png"
)

exit_icon = exit_icon.resize(
    (24, 24)
)

exit_icon = ImageTk.PhotoImage(
    exit_icon
)


exit_button = Button(
    leftframe,
    image=exit_icon,
    compound=LEFT,
    text=" Exit",
    font=("times new roman", 20, "bold"),
    anchor="w",
    padx=10,
    command=exit_app
)

exit_button.pack(
    fill=X
)


# ============================================================
# EMPLOYEE DASHBOARD FRAME
# ============================================================

emp_frame = Frame(
    window,
    bg="#2C3E50",
    bd=3,
    relief=RIDGE
)

emp_frame.place(
    x=400,
    y=125,
    width=300,
    height=200
)


emp_icon = Image.open(
    "icons/emp.png"
)

emp_icon = emp_icon.resize(
    (80, 80)
)

emp_icon = ImageTk.PhotoImage(
    emp_icon
)


emp_icon_label = Label(
    emp_frame,
    image=emp_icon,
    bg="#2C3E50"
)

emp_icon_label.pack()


emp_title_label = Label(
    emp_frame,
    text="Total Employee",
    bg="#2C3E50",
    font=("times new roman", 20),
    fg="white"
)

emp_title_label.pack()


emp_icon_count_label = Label(
    emp_frame,
    text="0",
    bg="#2C3E50",
    font=("times new roman", 30),
    fg="white"
)

emp_icon_count_label.pack()


# ============================================================
# SUPPLIER DASHBOARD FRAME
# ============================================================

supp_frame = Frame(
    window,
    bg="#8E44AD",
    bd=3,
    relief=RIDGE
)

supp_frame.place(
    x=800,
    y=125,
    width=300,
    height=200
)


supp_icon = Image.open(
    "icons/suppliers.png"
)

supp_icon = supp_icon.resize(
    (80, 80)
)

supp_icon = ImageTk.PhotoImage(
    supp_icon
)


supp_icon_label = Label(
    supp_frame,
    image=supp_icon,
    bg="#8E44AD"
)

supp_icon_label.pack()


supp_title_label = Label(
    supp_frame,
    text="Total Suppliers",
    bg="#8E44AD",
    font=("times new roman", 20),
    fg="white"
)

supp_title_label.pack()


supp_icon_count_label = Label(
    supp_frame,
    text="0",
    bg="#8E44AD",
    font=("times new roman", 30),
    fg="white"
)

supp_icon_count_label.pack()


# ============================================================
# CATEGORY DASHBOARD FRAME
# ============================================================

cat_frame = Frame(
    window,
    bg="#27AE60",
    bd=3,
    relief=RIDGE
)

cat_frame.place(
    x=1200,
    y=125,
    width=300,
    height=200
)


cat_icon = Image.open(
    "icons/catagory.png"
)

cat_icon = cat_icon.resize(
    (80, 80)
)

cat_icon = ImageTk.PhotoImage(
    cat_icon
)


cat_icon_label = Label(
    cat_frame,
    image=cat_icon,
    bg="#27AE60"
)

cat_icon_label.pack()


cat_title_label = Label(
    cat_frame,
    text="Total Categories",
    bg="#27AE60",
    font=("times new roman", 20),
    fg="white"
)

cat_title_label.pack()


cat_icon_count_label = Label(
    cat_frame,
    text="0",
    bg="#27AE60",
    font=("times new roman", 30),
    fg="white"
)

cat_icon_count_label.pack()


# ============================================================
# PRODUCT DASHBOARD FRAME
# ============================================================

prod_frame = Frame(
    window,
    bg="#2980B9",
    bd=3,
    relief=RIDGE
)

prod_frame.place(
    x=400,
    y=525,
    width=300,
    height=200
)


prod_icon = Image.open(
    "icons/product.png"
)

prod_icon = prod_icon.resize(
    (80, 80)
)

prod_icon = ImageTk.PhotoImage(
    prod_icon
)


prod_icon_label = Label(
    prod_frame,
    image=prod_icon,
    bg="#2980B9"
)

prod_icon_label.pack()


prod_title_label = Label(
    prod_frame,
    text="Total Products",
    bg="#2980B9",
    font=("times new roman", 20),
    fg="white"
)

prod_title_label.pack()


prod_icon_count_label = Label(
    prod_frame,
    text="0",
    bg="#2980B9",
    font=("times new roman", 30),
    fg="white"
)

prod_icon_count_label.pack()


# ============================================================
# SALES DASHBOARD FRAME
# ============================================================

sale_frame = Frame(
    window,
    bg="#E74C3C",
    bd=3,
    relief=RIDGE
)

sale_frame.place(
    x=800,
    y=525,
    width=300,
    height=200
)


sale_icon = Image.open(
    "icons/sales.png"
)

sale_icon = sale_icon.resize(
    (80, 80)
)

sale_icon = ImageTk.PhotoImage(
    sale_icon
)


sale_icon_label = Label(
    sale_frame,
    image=sale_icon,
    bg="#E74C3C"
)

sale_icon_label.pack()


sale_title_label = Label(
    sale_frame,
    text="Total Sales",
    bg="#E74C3C",
    font=("times new roman", 20),
    fg="white"
)

sale_title_label.pack()


sale_icon_count_label = Label(
    sale_frame,
    text="0",
    bg="#E74C3C",
    font=("times new roman", 30),
    fg="white"
)

sale_icon_count_label.pack()


# ============================================================
# START AUTOMATIC DASHBOARD COUNT
# ============================================================

update_dashboard_counts()


# ============================================================
# MAIN LOOP
# ============================================================

window.mainloop()
