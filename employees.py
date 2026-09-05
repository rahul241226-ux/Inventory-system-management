import pymysql
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date




# DATABASE CONNECTION

def connect_database():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Sswashank@12345'
        )

        cursor = connection.cursor()
        return cursor, connection

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            f"Database connectivity problem:\n{e}"
        )
        return None, None


# CREATE DATABASE AND TABLE


def create_database_table():
    cursor, connection = connect_database()

    if not cursor or not connection:
        return False

    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS inventory_system"
        )

        cursor.execute(
            "USE inventory_system"
        )

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employee_data
            (
                empid INT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(150),
                gender VARCHAR(50),
                dob VARCHAR(100),
                contact VARCHAR(100),
                employement_type VARCHAR(50),
                education VARCHAR(50),
                work_shift VARCHAR(100),
                address VARCHAR(255),
                doj VARCHAR(100),
                salary VARCHAR(100),
                usertype VARCHAR(100),
                password VARCHAR(100)
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



# LOAD TREEVIEW DATA

def treeview_data():
    cursor, connection = connect_database()

    if not cursor or not connection:
        return

    try:
        cursor.execute("USE inventory_system")

        # IMPORTANT:
        # Do NOT use SELECT *
        # Explicit column order prevents Education/Shift problems.
        cursor.execute("""
            SELECT
                empid,
                name,
                email,
                gender,
                dob,
                contact,
                employement_type,
                education,
                work_shift,
                address,
                doj,
                salary,
                usertype,
                password
            FROM employee_data
            ORDER BY empid
        """)

        employee_records = cursor.fetchall()

        employee_treeview.delete(
            *employee_treeview.get_children()
        )

        for record in employee_records:
            employee_treeview.insert(
                '',
                END,
                values=record
            )

    except Exception as e:
        messagebox.showerror(
            'Error',
            f'Error loading employee data:\n{e}'
        )

    finally:
        cursor.close()
        connection.close()




# SELECT TREEVIEW DATA

def select_data(
        event,
        empid_entry,
        name_entry,
        email_entry,
        gender_combobox,
        dob_entry,
        contact_entry,
        employement_type_combobox,
        education_combobox,
        work_shift_combobox,
        address_text,
        doj_label_entry,
        salary_entry,
        usertype_type_combobox,
        password_entry
):

    selected = employee_treeview.selection()

    if not selected:
        return

    item = employee_treeview.item(selected[0])
    row = item['values']

    if not row:
        return

    # Clear existing values without removing selection
    clear_fields(
        empid_entry,
        name_entry,
        email_entry,
        gender_combobox,
        dob_entry,
        contact_entry,
        employement_type_combobox,
        education_combobox,
        work_shift_combobox,
        address_text,
        doj_label_entry,
        salary_entry,
        usertype_type_combobox,
        password_entry,
        False
    )

    # 0 = empid
    # 1 = name
    # 2 = email
    # 3 = gender
    # 4 = dob
    # 5 = contact
    # 6 = employment type
    # 7 = education
    # 8 = work shift
    # 9 = address
    # 10 = doj
    # 11 = salary
    # 12 = usertype
    # 13 = password

    empid_entry.insert(0, row[0])

    name_entry.insert(0, row[1])

    email_entry.insert(0, row[2])

    gender_combobox.set(row[3])

    dob_entry.set_date(row[4])

    contact_entry.insert(0, row[5])

    employement_type_combobox.set(row[6])

    # EDUCATION
    education_combobox.set(row[7])

    # WORK SHIFT
    work_shift_combobox.set(row[8])

    address_text.insert("1.0", row[9])

    doj_label_entry.set_date(row[10])

    salary_entry.insert(0, row[11])

    usertype_type_combobox.set(row[12])

    password_entry.insert(0, row[13])




# ADD EMPLOYEE

def add_employee(
        empid,
        name,
        email,
        gender,
        dob,
        contact,
        employment_type,
        education,
        work_shift,
        address,
        doj,
        salary,
        user_type,
        password
):

    # Remove unnecessary spaces
    empid = empid.strip()
    name = name.strip()
    email = email.strip()
    contact = contact.strip()
    address = address.strip()
    salary = salary.strip()
    password = password.strip()



    # VALIDATION

    if empid == "":
        messagebox.showerror("Error", "Please enter Employee ID")
        return

    if name == "":
        messagebox.showerror("Error", "Please enter employee name")
        return

    if email == "":
        messagebox.showerror("Error", "Please enter email")
        return

    if gender == "Select Gender":
        messagebox.showerror("Error", "Please select gender")
        return

    if contact == "":
        messagebox.showerror("Error", "Please enter contact")
        return

    if employment_type == "Select Employment Type":
        messagebox.showerror(
            "Error",
            "Please select employment type"
        )
        return

    if education == "Select Education":
        messagebox.showerror(
            "Error",
            "Please select education"
        )
        return

    if work_shift == "Select Shift":
        messagebox.showerror(
            "Error",
            "Please select work shift"
        )
        return

    if address == "":
        messagebox.showerror(
            "Error",
            "Please enter address"
        )
        return

    if salary == "":
        messagebox.showerror(
            "Error",
            "Please enter salary"
        )
        return

    if user_type == "Select User Type":
        messagebox.showerror(
            "Error",
            "Please select user type"
        )
        return

    if password == "":
        messagebox.showerror(
            "Error",
            "Please enter password"
        )
        return

    cursor, connection = connect_database()

    if not cursor or not connection:
        return

    try:
        cursor.execute("USE inventory_system")

        # Check duplicate ID
        cursor.execute(
            """
            SELECT empid
            FROM employee_data
            WHERE empid = %s
            """,
            (empid,)
        )

        if cursor.fetchone():
            messagebox.showerror(
                "Error",
                "Employee ID already exists"
            )
            return


        # IMPORTANT:
        # Explicit column names

        cursor.execute(
            """
            INSERT INTO employee_data
            (
                empid,
                name,
                email,
                gender,
                dob,
                contact,
                employement_type,
                education,
                work_shift,
                address,
                doj,
                salary,
                usertype,
                password
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s
            )
            """,
            (
                empid,
                name,
                email,
                gender,
                dob,
                contact,
                employment_type,
                education,
                work_shift,
                address,
                doj,
                salary,
                user_type,
                password
            )
        )

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Employee added successfully"
        )

        treeview_data()

    except Exception as e:

        connection.rollback()

        messagebox.showerror(
            "Error",
            f"Error inserting employee:\n{e}"
        )

    finally:
        cursor.close()
        connection.close()




# CLEAR FIELDS

def clear_fields(
        empid_entry,
        name_entry,
        email_entry,
        gender_combobox,
        dob_entry,
        contact_entry,
        employement_type_combobox,
        education_combobox,
        work_shift_combobox,
        address_text,
        doj_label_entry,
        salary_entry,
        usertype_type_combobox,
        password_entry,
        check=True
):

    empid_entry.delete(0, END)

    name_entry.delete(0, END)

    email_entry.delete(0, END)

    gender_combobox.set("Select Gender")

    dob_entry.set_date(date.today())

    contact_entry.delete(0, END)

    employement_type_combobox.set(
        "Select Employment Type"
    )

    education_combobox.set(
        "Select Education"
    )

    work_shift_combobox.set(
        "Select Shift"
    )

    address_text.delete("1.0", END)

    doj_label_entry.set_date(date.today())

    salary_entry.delete(0, END)

    usertype_type_combobox.set(
        "Select User Type"
    )

    password_entry.delete(0, END)

    if check:
        employee_treeview.selection_remove(
            employee_treeview.selection()
        )




# UPDATE EMPLOYEE

def update_employee(
        empid,
        name,
        email,
        gender,
        dob,
        contact,
        employment_type,
        education,
        work_shift,
        address,
        doj,
        salary,
        user_type,
        password
):

    selected = employee_treeview.selection()

    if not selected:
        messagebox.showerror(
            "Error",
            "Please select an employee first"
        )
        return

    # Validation
    if empid == "":
        messagebox.showerror(
            "Error",
            "Employee ID is required"
        )
        return

    if name == "":
        messagebox.showerror(
            "Error",
            "Name is required"
        )
        return

    if email == "":
        messagebox.showerror(
            "Error",
            "Email is required"
        )
        return

    if gender == "Select Gender":
        messagebox.showerror(
            "Error",
            "Please select gender"
        )
        return

    if contact == "":
        messagebox.showerror(
            "Error",
            "Contact is required"
        )
        return

    if employment_type == "Select Employment Type":
        messagebox.showerror(
            "Error",
            "Please select employment type"
        )
        return

    if education == "Select Education":
        messagebox.showerror(
            "Error",
            "Please select education"
        )
        return

    if work_shift == "Select Shift":
        messagebox.showerror(
            "Error",
            "Please select work shift"
        )
        return

    if address.strip() == "":
        messagebox.showerror(
            "Error",
            "Address is required"
        )
        return

    if salary == "":
        messagebox.showerror(
            "Error",
            "Salary is required"
        )
        return

    if user_type == "Select User Type":
        messagebox.showerror(
            "Error",
            "Please select user type"
        )
        return

    if password == "":
        messagebox.showerror(
            "Error",
            "Password is required"
        )
        return

    cursor, connection = connect_database()

    if not cursor or not connection:
        return

    try:
        cursor.execute("USE inventory_system")

        # Check employee exists
        cursor.execute(
            """
            SELECT empid
            FROM employee_data
            WHERE empid = %s
            """,
            (empid,)
        )

        if not cursor.fetchone():
            messagebox.showerror(
                "Error",
                "Employee not found"
            )
            return

        address = address.strip()


        # EXPLICIT COLUMN UPDATE

        cursor.execute(
            """
            UPDATE employee_data
            SET
                name = %s,
                email = %s,
                gender = %s,
                dob = %s,
                contact = %s,
                employement_type = %s,
                education = %s,
                work_shift = %s,
                address = %s,
                doj = %s,
                salary = %s,
                usertype = %s,
                password = %s
            WHERE empid = %s
            """,
            (
                name,
                email,
                gender,
                dob,
                contact,
                employment_type,
                education,
                work_shift,
                address,
                doj,
                salary,
                user_type,
                password,
                empid
            )
        )

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Employee updated successfully"
        )

        treeview_data()

    except Exception as e:

        connection.rollback()

        messagebox.showerror(
            "Error",
            f"Error updating employee:\n{e}"
        )

    finally:
        cursor.close()
        connection.close()




# DELETE EMPLOYEE

def delete_employee():

    selected = employee_treeview.selection()

    if not selected:
        messagebox.showerror(
            "Error",
            "Please select an employee first"
        )
        return

    item = employee_treeview.item(selected[0])

    row = item["values"]

    if not row:
        return

    empid = row[0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Do you want to delete Employee ID {empid}?"
    )

    if not confirm:
        return

    cursor, connection = connect_database()

    if not cursor or not connection:
        return

    try:
        cursor.execute("USE inventory_system")

        cursor.execute(
            """
            DELETE FROM employee_data
            WHERE empid = %s
            """,
            (empid,)
        )

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Employee deleted successfully"
        )

        treeview_data()

    except Exception as e:

        connection.rollback()

        messagebox.showerror(
            "Error",
            f"Error deleting employee:\n{e}"
        )

    finally:
        cursor.close()
        connection.close()




# SEARCH EMPLOYEE

def search_employee(search_by, search_value):

    search_value = search_value.strip()

    if search_by == "Search By":
        messagebox.showerror(
            "Error",
            "Please select Search By option"
        )
        return

    if search_value == "":
        messagebox.showerror(
            "Error",
            "Please enter search value"
        )
        return

    cursor, connection = connect_database()

    if not cursor or not connection:
        return

    try:
        cursor.execute("USE inventory_system")

        # Map combobox values to actual DB columns
        column_map = {
            "Id": "empid",
            "Name": "name",
            "Email": "email",
            "Employment Type": "employement_type",
            "Education": "education",
            "Work Shift": "work_shift",
            "Salary": "salary"
        }

        column = column_map.get(search_by)

        if not column:
            messagebox.showerror(
                "Error",
                "Invalid search option"
            )
            return


        # Explicit SELECT column order

        query = f"""
            SELECT
                empid,
                name,
                email,
                gender,
                dob,
                contact,
                employement_type,
                education,
                work_shift,
                address,
                doj,
                salary,
                usertype,
                password
            FROM employee_data
            WHERE {column} LIKE %s
            ORDER BY empid
        """

        cursor.execute(
            query,
            (f"%{search_value}%",)
        )

        records = cursor.fetchall()

        employee_treeview.delete(
            *employee_treeview.get_children()
        )

        for record in records:
            employee_treeview.insert(
                "",
                END,
                values=record
            )

        if not records:
            messagebox.showinfo(
                "Search",
                "No employee found"
            )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Search error:\n{e}"
        )

    finally:
        cursor.close()
        connection.close()



# SHOW ALL EMPLOYEES

def show_all_employees():
    treeview_data()




# EMPLOYEE FORM

def employee_form(window):

    global employee_treeview


    # CREATE DATABASE FIRST

    if not create_database_table():
        return


    # MAIN EMPLOYEE FRAME

    employee_frame = Frame(
        window,
        width=1330,
        height=690,
        bg="white"
    )

    employee_frame.place(
        x=200,
        y=100
    )


    # HEADING

    heading_label = Label(
        employee_frame,
        text="Manage Employee Details",
        font=("times new roman", 16, "bold"),
        bg="#0f4d7d",
        fg="white"
    )

    heading_label.place(
        x=0,
        y=0,
        relwidth=1
    )


    # TOP FRAME

    topFrame = Frame(
        employee_frame,
        bg="white"
    )

    topFrame.place(
        x=0,
        y=50,
        relwidth=1,
        height=245
    )


    # BACK BUTTON

    back_button = Button(
        topFrame,
        text="Back",
        width=10,
        cursor="hand2",
        bg="white",
        command=lambda: employee_frame.place_forget()
    )

    back_button.place(
        x=10,
        y=10
    )


    # SEARCH FRAME

    searchframe = Frame(
        topFrame,
        bg="white"
    )

    searchframe.pack(
        pady=(5, 0)
    )

    # Search combobox
    search_combobox = ttk.Combobox(
        searchframe,
        values=(
            "Id",
            "Name",
            "Email",
            "Employment Type",
            "Education",
            "Work Shift",
            "Salary"
        ),
        font=("times new roman", 12),
        width=18,
        state="readonly"
    )

    search_combobox.set("Search By")

    search_combobox.grid(
        row=0,
        column=0,
        padx=10
    )

    # Search entry
    search_entry = Entry(
        searchframe,
        font=("times new roman", 12),
        bg="lightyellow",
        width=25
    )

    search_entry.grid(
        row=0,
        column=1,
        padx=5
    )

    # Search button
    search_button = Button(
        searchframe,
        text="Search",
        font=("times new roman", 12),
        width=10,
        cursor="hand2",
        fg="white",
        bg="#0f4d74",
        command=lambda: search_employee(
            search_combobox.get(),
            search_entry.get()
        )
    )

    search_button.grid(
        row=0,
        column=2,
        padx=10
    )

    # Show All
    show_button = Button(
        searchframe,
        text="Show All",
        font=("times new roman", 12),
        width=10,
        cursor="hand2",
        fg="white",
        bg="#0f4d74",
        command=show_all_employees
    )

    show_button.grid(
        row=0,
        column=3,
        padx=10
    )



    # SCROLLBARS


    horizontal_scrollbar = Scrollbar(
        topFrame,
        orient=HORIZONTAL
    )

    vertical_scrollbar = Scrollbar(
        topFrame,
        orient=VERTICAL
    )



    # TREEVIEW

    employee_treeview = ttk.Treeview(
        topFrame,

        columns=(
            "empid",
            "name",
            "email",
            "gender",
            "dob",
            "contact",
            "employement_type",
            "education",
            "work_shift",
            "address",
            "doj",
            "salary",
            "usertype",
            "password"
        ),

        show="headings",

        yscrollcommand=vertical_scrollbar.set,

        xscrollcommand=horizontal_scrollbar.set
    )

    vertical_scrollbar.config(
        command=employee_treeview.yview
    )

    horizontal_scrollbar.config(
        command=employee_treeview.xview
    )

    vertical_scrollbar.pack(
        side=RIGHT,
        fill=Y,
        pady=(10, 0)
    )

    horizontal_scrollbar.pack(
        side=BOTTOM,
        fill=X
    )

    employee_treeview.pack(
        pady=(10, 0),
        fill=BOTH,
        expand=True
    )


    # TREEVIEW HEADINGS

    employee_treeview.heading(
        "empid",
        text="EmpId"
    )

    employee_treeview.heading(
        "name",
        text="Name"
    )

    employee_treeview.heading(
        "email",
        text="Email"
    )

    employee_treeview.heading(
        "gender",
        text="Gender"
    )

    employee_treeview.heading(
        "dob",
        text="Date of Birth"
    )

    employee_treeview.heading(
        "contact",
        text="Contact"
    )

    employee_treeview.heading(
        "employement_type",
        text="Employment Type"
    )

    employee_treeview.heading(
        "education",
        text="Education"
    )

    employee_treeview.heading(
        "work_shift",
        text="Shift"
    )

    employee_treeview.heading(
        "address",
        text="Address"
    )

    employee_treeview.heading(
        "doj",
        text="Date of Joining"
    )

    employee_treeview.heading(
        "salary",
        text="Salary"
    )

    employee_treeview.heading(
        "usertype",
        text="User Type"
    )

    employee_treeview.heading(
        "password",
        text="Password"
    )


    # TREEVIEW COLUMN WIDTH

    employee_treeview.column(
        "empid",
        width=60
    )

    employee_treeview.column(
        "name",
        width=140
    )

    employee_treeview.column(
        "email",
        width=200
    )

    employee_treeview.column(
        "gender",
        width=80
    )

    employee_treeview.column(
        "dob",
        width=120
    )

    employee_treeview.column(
        "contact",
        width=130
    )

    employee_treeview.column(
        "employement_type",
        width=140
    )

    employee_treeview.column(
        "education",
        width=120
    )

    employee_treeview.column(
        "work_shift",
        width=120
    )

    employee_treeview.column(
        "address",
        width=180
    )

    employee_treeview.column(
        "doj",
        width=120
    )

    employee_treeview.column(
        "salary",
        width=120
    )

    employee_treeview.column(
        "usertype",
        width=100
    )

    employee_treeview.column(
        "password",
        width=120
    )


    # LOAD DATA

    treeview_data()




    # DETAIL FRAME

    detail_frame = Frame(
        employee_frame,
        bg="white"
    )

    detail_frame.place(
        x=100,
        y=305
    )



    # EMPLOYEE ID

    empid_label = Label(
        detail_frame,
        text="EmpId:",
        font=("times new roman", 12)
    )

    empid_label.grid(
        row=0,
        column=0,
        padx=20,
        pady=10,
        sticky="w"
    )

    empid_entry = Entry(
        detail_frame,
        font=("times new roman", 12),
        bg="lightyellow"
    )

    empid_entry.grid(
        row=0,
        column=1,
        padx=20,
        pady=10
    )



    # NAME

    name_label = Label(
        detail_frame,
        text="Name:",
        font=("times new roman", 12)
    )

    name_label.grid(
        row=0,
        column=2,
        padx=20,
        pady=10,
        sticky="w"
    )

    name_entry = Entry(
        detail_frame,
        font=("times new roman", 12),
        bg="lightyellow"
    )

    name_entry.grid(
        row=0,
        column=3,
        padx=20,
        pady=10
    )




    # EMAIL

    email_label = Label(
        detail_frame,
        text="Email:",
        font=("times new roman", 12)
    )

    email_label.grid(
        row=0,
        column=4,
        padx=20,
        pady=10,
        sticky="w"
    )

    email_entry = Entry(
        detail_frame,
        font=("times new roman", 12),
        bg="lightyellow"
    )

    email_entry.grid(
        row=0,
        column=5,
        padx=20,
        pady=10
    )


    # GENDER

    gender_label = Label(
        detail_frame,
        text="Gender:",
        font=("times new roman", 12)
    )

    gender_label.grid(
        row=1,
        column=0,
        padx=20,
        pady=10,
        sticky="w"
    )

    gender_combobox = ttk.Combobox(
        detail_frame,
        values=("Male", "Female"),
        font=("times new roman", 12),
        width=18,
        state="readonly"
    )

    gender_combobox.set(
        "Select Gender"
    )

    gender_combobox.grid(
        row=1,
        column=1,
        padx=20,
        pady=10
    )


    # DATE OF BIRTH

    dob_label = Label(
        detail_frame,
        text="Date of Birth:",
        font=("times new roman", 12)
    )

    dob_label.grid(
        row=1,
        column=2,
        padx=20,
        pady=10,
        sticky="w"
    )

    dob_entry = DateEntry(
        detail_frame,
        font=("times new roman", 12),
        width=18,
        date_pattern="dd/mm/yyyy"
    )

    dob_entry.grid(
        row=1,
        column=3,
        padx=20,
        pady=10
    )



    # CONTACT

    contact_label = Label(
        detail_frame,
        text="Contact:",
        font=("times new roman", 12)
    )

    contact_label.grid(
        row=1,
        column=4,
        padx=20,
        pady=10,
        sticky="w"
    )

    contact_entry = Entry(
        detail_frame,
        font=("times new roman", 12),
        bg="lightyellow"
    )

    contact_entry.grid(
        row=1,
        column=5,
        padx=20,
        pady=10
    )


    # EMPLOYMENT TYPE

    employment_type_label = Label(
        detail_frame,
        text="Employment Type:",
        font=("times new roman", 12)
    )

    employment_type_label.grid(
        row=2,
        column=0,
        padx=20,
        pady=10,
        sticky="w"
    )

    employment_type_combobox = ttk.Combobox(
        detail_frame,
        values=(
            "full time",
            "part time"
        ),
        font=("times new roman", 12),
        width=18,
        state="readonly"
    )

    employment_type_combobox.set(
        "Select Employment Type"
    )

    employment_type_combobox.grid(
        row=2,
        column=1,
        padx=20,
        pady=10
    )



    # EDUCATION

    education_label = Label(
        detail_frame,
        text="Education:",
        font=("times new roman", 12)
    )

    education_label.grid(
        row=2,
        column=2,
        padx=20,
        pady=10,
        sticky="w"
    )

    education_combobox = ttk.Combobox(
        detail_frame,
        values=(
            "B.tech",
            "B.com",
            "M.com",
            "B.Sc",
            "M.Sc",
            "BBA",
            "MBA"
        ),
        font=("times new roman", 12),
        width=18,
        state="readonly"
    )

    education_combobox.set(
        "Select Education"
    )

    education_combobox.grid(
        row=2,
        column=3,
        padx=20,
        pady=10
    )


    # WORK SHIFT

    work_shift_label = Label(
        detail_frame,
        text="Work Shift:",
        font=("times new roman", 12)
    )

    work_shift_label.grid(
        row=2,
        column=4,
        padx=20,
        pady=10,
        sticky="w"
    )

    work_shift_combobox = ttk.Combobox(
        detail_frame,
        values=(
            "Morning",
            "Evening",
            "Night"
        ),
        font=("times new roman", 12),
        width=18,
        state="readonly"
    )

    work_shift_combobox.set(
        "Select Shift"
    )

    work_shift_combobox.grid(
        row=2,
        column=5,
        padx=20,
        pady=10
    )


    # ADDRESS

    address_label = Label(
        detail_frame,
        text="Address:",
        font=("times new roman", 12)
    )

    address_label.grid(
        row=3,
        column=0,
        padx=20,
        pady=10,
        sticky="w"
    )

    address_text = Text(
        detail_frame,
        width=20,
        height=3,
        font=("times new roman", 12),
        bg="lightyellow"
    )

    address_text.grid(
        row=3,
        column=1,
        padx=20,
        pady=10
    )


    # DATE OF JOINING

    doj_label = Label(
        detail_frame,
        text="Date of Joining:",
        font=("times new roman", 12)
    )

    doj_label.grid(
        row=3,
        column=2,
        padx=20,
        pady=10,
        sticky="w"
    )

    doj_label_entry = DateEntry(
        detail_frame,
        font=("times new roman", 12),
        width=18,
        date_pattern="dd/mm/yyyy"
    )

    doj_label_entry.grid(
        row=3,
        column=3,
        padx=20,
        pady=10
    )

    # SALARY

    salary_label = Label(
        detail_frame,
        text="Salary:",
        font=("times new roman", 12)
    )

    salary_label.grid(
        row=3,
        column=4,
        padx=20,
        pady=10,
        sticky="w"
    )

    salary_entry = Entry(
        detail_frame,
        font=("times new roman", 12),
        bg="lightyellow"
    )

    salary_entry.grid(
        row=3,
        column=5,
        padx=20,
        pady=10
    )


    # USER TYPE


    usertype_label = Label(
        detail_frame,
        text="User Type:",
        font=("times new roman", 12)
    )

    usertype_label.grid(
        row=4,
        column=2,
        padx=20,
        pady=10,
        sticky="w"
    )

    usertype_type_combobox = ttk.Combobox(
        detail_frame,
        values=(
            "Admin",
            "Employee"
        ),
        font=("times new roman", 12),
        width=18,
        state="readonly"
    )

    usertype_type_combobox.set(
        "Select User Type"
    )

    usertype_type_combobox.grid(
        row=4,
        column=3,
        padx=20,
        pady=10
    )


    # PASSWORD

    password_label = Label(
        detail_frame,
        text="Password:",
        font=("times new roman", 12)
    )

    password_label.grid(
        row=4,
        column=4,
        padx=20,
        pady=10,
        sticky="w"
    )

    password_entry = Entry(
        detail_frame,
        font=("times new roman", 12),
        bg="lightyellow",
        show="*"
    )

    password_entry.grid(
        row=4,
        column=5,
        padx=20,
        pady=10
    )



    # BUTTON FRAME

    button_frame = Frame(
        employee_frame,
        bg="white"
    )

    button_frame.place(
        x=230,
        y=610
    )



    # ADD BUTTON

    add_button = Button(
        button_frame,
        text="Add",
        font=("times new roman", 12),
        width=10,
        cursor="hand2",
        fg="white",
        bg="#0f4d74",

        command=lambda: add_employee(
            empid_entry.get(),
            name_entry.get(),
            email_entry.get(),
            gender_combobox.get(),
            dob_entry.get(),
            contact_entry.get(),
            employment_type_combobox.get(),
            education_combobox.get(),
            work_shift_combobox.get(),
            address_text.get("1.0", END),
            doj_label_entry.get(),
            salary_entry.get(),
            usertype_type_combobox.get(),
            password_entry.get()
        )
    )

    add_button.grid(
        row=0,
        column=0,
        padx=10
    )



    # UPDATE BUTTON

    update_button = Button(
        button_frame,
        text="Update",
        font=("times new roman", 12),
        width=10,
        cursor="hand2",
        fg="white",
        bg="#0f4d74",

        command=lambda: update_employee(
            empid_entry.get(),
            name_entry.get(),
            email_entry.get(),
            gender_combobox.get(),
            dob_entry.get(),
            contact_entry.get(),
            employment_type_combobox.get(),
            education_combobox.get(),
            work_shift_combobox.get(),
            address_text.get("1.0", END),
            doj_label_entry.get(),
            salary_entry.get(),
            usertype_type_combobox.get(),
            password_entry.get()
        )
    )

    update_button.grid(
        row=0,
        column=1,
        padx=10
    )


    # DELETE BUTTON

    delete_button = Button(
        button_frame,
        text="Delete",
        font=("times new roman", 12),
        width=10,
        cursor="hand2",
        fg="white",
        bg="#0f4d74",
        command=delete_employee
    )

    delete_button.grid(
        row=0,
        column=2,
        padx=10
    )


    # CLEAR BUTTON

    clear_button = Button(
        button_frame,
        text="Clear",
        font=("times new roman", 12),
        width=10,
        cursor="hand2",
        fg="white",
        bg="#0f4d74",

        command=lambda: clear_fields(
            empid_entry,
            name_entry,
            email_entry,
            gender_combobox,
            dob_entry,
            contact_entry,
            employment_type_combobox,
            education_combobox,
            work_shift_combobox,
            address_text,
            doj_label_entry,
            salary_entry,
            usertype_type_combobox,
            password_entry,
            True
        )
    )

    clear_button.grid(
        row=0,
        column=3,
        padx=10
    )



    # TREEVIEW CLICK EVENT

    employee_treeview.bind(
        "<ButtonRelease-1>",
        lambda event: select_data(
            event,
            empid_entry,
            name_entry,
            email_entry,
            gender_combobox,
            dob_entry,
            contact_entry,
            employment_type_combobox,
            education_combobox,
            work_shift_combobox,
            address_text,
            doj_label_entry,
            salary_entry,
            usertype_type_combobox,
            password_entry
        )
    )




# MAIN WINDOW

if __name__ == "__main__":

    window = Tk()

    window.title(
        "Employee Management System"
    )

    window.geometry(
        "1530x850"
    )

    window.config(
        bg="white"
    )

    employee_form(window)

    window.mainloop()

