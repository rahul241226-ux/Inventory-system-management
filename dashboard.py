from tkinter import *
from tkinter import ttk, messagebox

from datetime import datetime
from PIL import Image, ImageTk

from employees import employee_form
from suppliers import supplier_form
from category import category_form
from products import product_form
from employees import connect_database
from view_bill import view_bill


# ============================================================
# GLOBAL VARIABLES
# ============================================================

current_frame = None
is_small = False


# ============================================================
# MAIN WINDOW
# ============================================================

window = Tk()

window.title("Dashboard")

# Starting size
window.geometry("1530x880+0+0")

# Allow resizing
window.resizable(True, True)

# Minimum size
window.minsize(900, 600)

window.config(bg="white")


# ============================================================
# RESPONSIVE SIZE VARIABLES
# ============================================================

# These variables are updated whenever the window is resized

current_width = 1530
current_height = 880


# ============================================================
# HEADER IMAGE
# ============================================================

image = Image.open(
    "icons/checklist.png"
)

image = image.resize(
    (64, 64)
)

bg_Image = ImageTk.PhotoImage(image)


# ============================================================
# HEADER
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
    relwidth=1,
    height=70
)


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
    relwidth=1,
    height=32
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
        text=(
            f"Welcome Admin"
            f"\t\t Date: {current_date}"
            f"\t\t Time: {current_time}"
        )
    )

    subtitlelabel.after(
        1000,
        update_datetime
    )


update_datetime()


# ============================================================
# LEFT SIDEBAR
# ============================================================

leftframe = Frame(
    window,
    bg="#eeeeee",
    bd=1,
    relief=RIDGE
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
    image=logoimage,
    bg="#eeeeee"
)

imageLabel.pack(
    pady=8
)


# ============================================================
# FUNCTION TO CREATE SIDEBAR BUTTONS
# ============================================================

def create_sidebar_button(
    parent,
    image_path,
    text,
    command
):

    icon = Image.open(
        image_path
    )

    icon = icon.resize(
        (24, 24)
    )

    icon = ImageTk.PhotoImage(
        icon
    )

    button = Button(
        parent,
        image=icon,
        compound=LEFT,
        text=text,
        font=("times new roman", 20, "bold"),
        anchor="w",
        padx=10,
        bg="#eeeeee",
        activebackground="#d5d5d5",
        cursor="hand2",
        command=command
    )

    # Important:
    # Keep image reference alive
    button.image = icon

    button.pack(
        fill=X,
        pady=1
    )

    return button


# ============================================================
# SHOW FORM FUNCTION
# ============================================================

def show_form(form_function):

    global current_frame

    # Remove previous form
    if current_frame is not None:

        try:
            current_frame.place_forget()
            current_frame.destroy()

        except Exception:
            pass

        current_frame = None

    # Create new form
    current_frame = form_function(window)

    # --------------------------------------------------------
    # RESPONSIVE FORM POSITION
    # --------------------------------------------------------

    # Leave sidebar area
    current_frame.place(
        relx=0.14,
        rely=0.10,
        relwidth=0.5,
        relheight=0.84
    )

    # Bring form to front
    current_frame.lift()


# ============================================================
# EMPLOYEE BUTTON
# ============================================================

employee_button = create_sidebar_button(
    leftframe,
    "icons/employee.png",
    " Employee",
    lambda: show_form(employee_form)
)


# ============================================================
# SUPPLIER BUTTON
# ============================================================

supplier_button = create_sidebar_button(
    leftframe,
    "icons/supplier.png",
    " Supplier",
    lambda: show_form(supplier_form)
)


# ============================================================
# CATEGORY BUTTON
# ============================================================

category_button = create_sidebar_button(
    leftframe,
    "icons/catagory.png",
    " Category",
    lambda: show_form(category_form)
)


# ============================================================
# PRODUCT BUTTON
# ============================================================

product_button = create_sidebar_button(
    leftframe,
    "icons/product.png",
    " Product",
    lambda: show_form(product_form)
)


# ============================================================
# SALES BUTTON
# ============================================================

sales_button = create_sidebar_button(
    leftframe,
    "icons/sales.png",
    " Sales",
    lambda: view_bill(window)
)


# ============================================================
# EXIT FUNCTION
# ============================================================

def exit_app():

    result = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?",
        parent=window
    )

    if result:
        window.destroy()


# ============================================================
# EXIT BUTTON
# ============================================================

exit_button = create_sidebar_button(
    leftframe,
    "icons/exit.png",
    " Exit",
    exit_app
)


# ============================================================
# TAX WINDOW
# ============================================================

def tax_window():

    def save_tax():

        value = tax_count.get()

        cursor, connection = connect_database()

        if cursor is None or connection is None:
            return

        try:

            cursor.execute(
                "USE inventory_system"
            )

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tax_table (
                    id INT PRIMARY KEY,
                    tax DECIMAL(5,2)
                )
            """)

            cursor.execute(
                "SELECT id FROM tax_table WHERE id = %s",
                (1,)
            )

            if cursor.fetchone():

                cursor.execute(
                    """
                    UPDATE tax_table
                    SET tax = %s
                    WHERE id = %s
                    """,
                    (value, 1)
                )

            else:

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

    tax_root.title(
        "Tax Calculator"
    )

    tax_root.geometry(
        "300x300"
    )

    tax_root.resizable(
        False,
        False
    )

    tax_root.grab_set()

    tax_percentage = Label(
        tax_root,
        text="Enter Tax Percentage (%)",
        font=("arial", 12)
    )

    tax_percentage.pack(
        pady=10
    )

    tax_count = Spinbox(
        tax_root,
        from_=0,
        to=100,
        font=("arial", 12)
    )

    tax_count.pack(
        pady=10
    )

    save_button = Button(
        tax_root,
        text="Save",
        font=("arial", 12, "bold"),
        command=save_tax
    )

    save_button.pack(
        pady=10
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


# ============================================================
# EMPLOYEE ICON
# ============================================================

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

emp_icon_label.pack(
    pady=(8, 0)
)


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


# ============================================================
# SUPPLIER ICON
# ============================================================

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

supp_icon_label.pack(
    pady=(8, 0)
)


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


# ============================================================
# CATEGORY ICON
# ============================================================

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

cat_icon_label.pack(
    pady=(8, 0)
)


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


# ============================================================
# PRODUCT ICON
# ============================================================

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

prod_icon_label.pack(
    pady=(8, 0)
)


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


# ============================================================
# SALES ICON
# ============================================================

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

sale_icon_label.pack(
    pady=(8, 0)
)


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
# RESPONSIVE DASHBOARD FUNCTION
# ============================================================

def handleResize(event):

    global current_width
    global current_height

    # --------------------------------------------------------
    # Only respond to main window
    # --------------------------------------------------------

    if event.widget != window:
        return

    current_width = event.width
    current_height = event.height

    # --------------------------------------------------------
    # Minimum dimensions
    # --------------------------------------------------------

    width = max(
        current_width,
        900
    )

    height = max(
        current_height,
        600
    )

    # ========================================================
    # RESPONSIVE SIDEBAR
    # ========================================================

    sidebar_width = int(
        width * 0.13
    )

    sidebar_width = max(
        160,
        min(
            sidebar_width,
            220
        )
    )

    leftframe.place(
        x=0,
        y=102,
        width=sidebar_width,
        height=height - 102
    )

    # ========================================================
    # RESPONSIVE SIDEBAR FONT
    # ========================================================

    if width < 1050:

        sidebar_font_size = 15

    elif width < 1250:

        sidebar_font_size = 17

    else:

        sidebar_font_size = 20

    sidebar_font = (
        "times new roman",
        sidebar_font_size,
        "bold"
    )

    employee_button.config(
        font=sidebar_font
    )

    supplier_button.config(
        font=sidebar_font
    )

    category_button.config(
        font=sidebar_font
    )

    product_button.config(
        font=sidebar_font
    )

    sales_button.config(
        font=sidebar_font
    )

    exit_button.config(
        font=sidebar_font
    )

    minimize_button.config(
        font=sidebar_font
    )

    # ========================================================
    # DASHBOARD CONTENT AREA
    # ========================================================

    content_x = sidebar_width + 20

    content_width = (
        width
        - sidebar_width
        - 40
    )

    # ========================================================
    # DASHBOARD CARD SIZE
    # ========================================================

    # Three cards per row
    card_width = int(
        content_width * 0.27
    )

    card_width = max(
        190,
        min(
            card_width,
            330
        )
    )

    # Responsive height
    card_height = int(
        height * 0.23
    )

    card_height = max(
        160,
        min(
            card_height,
            210
        )
    )

    # ========================================================
    # GAP CALCULATION
    # ========================================================

    total_card_width = (
        card_width * 3
    )

    available_gap = (
        content_width
        - total_card_width
    )

    gap = int(
        available_gap / 4
    )

    gap = max(
        10,
        gap
    )

    # ========================================================
    # X POSITIONS
    # ========================================================

    x1 = (
        content_x
        + gap
    )

    x2 = (
        x1
        + card_width
        + gap
    )

    x3 = (
        x2
        + card_width
        + gap
    )

    # ========================================================
    # Y POSITIONS
    # ========================================================

    top_y = 125

    row_gap = max(
        40,
        int(height * 0.07)
    )

    bottom_y = (
        top_y
        + card_height
        + row_gap
    )

    # ========================================================
    # EMPLOYEE
    # ========================================================

    emp_frame.place(
        x=x1,
        y=top_y,
        width=card_width,
        height=card_height
    )

    # ========================================================
    # SUPPLIER
    # ========================================================

    supp_frame.place(
        x=x2,
        y=top_y,
        width=card_width,
        height=card_height
    )

    # ========================================================
    # CATEGORY
    # ========================================================

    cat_frame.place(
        x=x3,
        y=top_y,
        width=card_width,
        height=card_height
    )

    # ========================================================
    # PRODUCT
    # ========================================================

    prod_frame.place(
        x=x1,
        y=bottom_y,
        width=card_width,
        height=card_height
    )

    # ========================================================
    # SALES
    # ========================================================

    sale_frame.place(
        x=x2,
        y=bottom_y,
        width=card_width,
        height=card_height
    )

    # ========================================================
    # RESPONSIVE DASHBOARD FONTS
    # ========================================================

    if width < 1050:

        title_size = 15
        count_size = 24

    elif width < 1200:

        title_size = 17
        count_size = 27

    else:

        title_size = 20
        count_size = 30

    # --------------------------------------------------------
    # Titles
    # --------------------------------------------------------

    emp_title_label.config(
        font=(
            "times new roman",
            title_size
        )
    )

    supp_title_label.config(
        font=(
            "times new roman",
            title_size
        )
    )

    cat_title_label.config(
        font=(
            "times new roman",
            title_size
        )
    )

    prod_title_label.config(
        font=(
            "times new roman",
            title_size
        )
    )

    sale_title_label.config(
        font=(
            "times new roman",
            title_size
        )
    )

    # --------------------------------------------------------
    # Counts
    # --------------------------------------------------------

    emp_icon_count_label.config(
        font=(
            "times new roman",
            count_size
        )
    )

    supp_icon_count_label.config(
        font=(
            "times new roman",
            count_size
        )
    )

    cat_icon_count_label.config(
        font=(
            "times new roman",
            count_size
        )
    )

    prod_icon_count_label.config(
        font=(
            "times new roman",
            count_size
        )
    )

    sale_icon_count_label.config(
        font=(
            "times new roman",
            count_size
        )
    )

    # ========================================================
    # RESPONSIVE HEADER FONT
    # ========================================================

    if width < 1050:

        header_size = 25

    elif width < 1250:

        header_size = 31

    else:

        header_size = 40

    titleLabel.config(
        font=(
            "times new roman",
            header_size,
            "bold"
        )
    )


# ============================================================
# MAXIMIZE / RESTORE
# ============================================================

def toggle_window_size():

    global is_small

    if not is_small:

        # ----------------------------------------------------
        # Smaller window
        # ----------------------------------------------------

        window.geometry(
            "1100x650+100+50"
        )

        minimize_button.config(
            text="↗  Restore"
        )

        is_small = True

    else:

        # ----------------------------------------------------
        # Restore window
        # ----------------------------------------------------

        window.geometry(
            "1530x880+0+0"
        )

        minimize_button.config(
            text="□  Maximize"
        )

        is_small = False


# ============================================================
# MAXIMIZE / RESTORE BUTTON
# ============================================================

minimize_button = Button(
    leftframe,
    text="□  Maximize",
    font=(
        "Arial",
        14,
        "bold"
    ),
    bg="#010c48",
    fg="white",
    bd=0,
    activebackground="#010c48",
    activeforeground="white",
    cursor="hand2",
    command=toggle_window_size
)

minimize_button.pack(
    fill=X,
    pady=5
)


# ============================================================
# DASHBOARD DATABASE COUNTS
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

        # ====================================================
        # EMPLOYEES
        # ====================================================

        cursor.execute(
            "SELECT COUNT(*) FROM employee_data"
        )

        employee_result = cursor.fetchone()

        employee_count = (
            employee_result[0]
            if employee_result
            else 0
        )

        # ====================================================
        # SUPPLIERS
        # ====================================================

        cursor.execute(
            "SELECT COUNT(*) FROM supplier_data"
        )

        supplier_result = cursor.fetchone()

        supplier_count = (
            supplier_result[0]
            if supplier_result
            else 0
        )

        # ====================================================
        # CATEGORIES
        # ====================================================

        cursor.execute(
            "SELECT COUNT(*) FROM category_data"
        )

        category_result = cursor.fetchone()

        category_count = (
            category_result[0]
            if category_result
            else 0
        )

        # ====================================================
        # PRODUCTS
        # ====================================================

        cursor.execute(
            "SELECT COUNT(*) FROM product_data"
        )

        product_result = cursor.fetchone()

        product_count = (
            product_result[0]
            if product_result
            else 0
        )

        # ====================================================
        # SALES
        # ====================================================

        try:

            cursor.execute(
                "SELECT COUNT(*) FROM sales_data"
            )

            sales_result = cursor.fetchone()

            sales_count = (
                sales_result[0]
                if sales_result
                else 0
            )

        except Exception:

            sales_count = 0

        # ====================================================
        # UPDATE LABELS
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

            try:
                cursor.close()
            except Exception:
                pass

        if connection is not None:

            try:
                connection.close()
            except Exception:
                pass

    # ========================================================
    # RUN AGAIN AFTER 1 SECOND
    # ========================================================

    window.after(
        1000,
        update_dashboard_counts
    )


# ============================================================
# RESIZE EVENT
# ============================================================

window.bind(
    "<Configure>",
    handleResize
)


# ============================================================
# START DASHBOARD COUNT
# ============================================================

update_dashboard_counts()


# ============================================================
# FIRST RESPONSIVE LAYOUT
# ============================================================

window.update_idletasks()

handleResize(
    type(
        "ResizeEvent",
        (),
        {
            "widget": window,
            "width": window.winfo_width(),
            "height": window.winfo_height()
        }
    )()
)


# ============================================================
# MAIN LOOP
# ============================================================

window.mainloop()
