from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import os


# ============================================================
# DATABASE CONNECTION
# ============================================================

def connect_database():

    try:

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sswashank@12345",
            database="inventory_system"
        )

        return connection

    except mysql.connector.Error as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to connect to database:\n{e}"
        )

        return None


# ============================================================
# LOGIN WINDOW
# ============================================================

window = Tk()

window.title("Login")

window.geometry("1510x900+0+0")

window.resizable(False, False)

window.config(bg="white")


# ============================================================
# TOP TITLE
# ============================================================

title_label = Label(
    window,
    text="Inventory Management System",
    font=("times new roman", 48, "bold"),
    bg="#4d94d9",
    fg="white"
)

title_label.place(
    x=0,
    y=0,
    width=1510,
    height=140
)


# ============================================================
# LEFT SIDE IMAGE
# ============================================================

try:

    image = Image.open("icons/inventory.png")

    image = image.resize(
        (650, 550)
    )

    inventory_image = ImageTk.PhotoImage(
        image
    )

    image_label = Label(
        window,
        image=inventory_image,
        bg="white"
    )

    image_label.image = inventory_image

    image_label.place(
        x=40,
        y=250
    )

except FileNotFoundError:

    print("inventory.png not found.")

except Exception as e:

    print("Image error:", e)


# ============================================================
# LOGIN FRAME
# ============================================================

login_frame = Frame(
    window,
    bg="#d3d3d3"
)

login_frame.place(
    x=935,
    y=190,
    width=465,
    height=660
)


# ============================================================
# EMPLOYEE IMAGE
# ============================================================

try:

    employee_image = Image.open(
        "icons/emp.png"
    )

    employee_image = employee_image.resize(
        (230, 230)
    )

    employee_photo = ImageTk.PhotoImage(
        employee_image
    )

    employee_label = Label(
        login_frame,
        image=employee_photo,
        bg="#d3d3d3"
    )

    employee_label.image = employee_photo

    employee_label.place(
        x=115,
        y=30
    )

except FileNotFoundError:

    print("emp.png not found.")

except Exception as e:

    print("Employee image error:", e)


# ============================================================
# EMPLOYEE ID LABEL
# ============================================================

employee_id_label = Label(
    login_frame,
    text="Employee Id",
    font=(
        "times new roman",
        18
    ),
    bg="#d3d3d3",
    fg="black"
)

employee_id_label.place(
    x=75,
    y=310
)


# ============================================================
# EMPLOYEE ID ENTRY
# ============================================================

employee_id_entry = Entry(
    login_frame,
    font=(
        "times new roman",
        18
    ),
    bg="white",
    fg="black",
    bd=1
)

employee_id_entry.place(
    x=75,
    y=350,
    width=310,
    height=40
)


# ============================================================
# PASSWORD LABEL
# ============================================================

password_label = Label(
    login_frame,
    text="Password",
    font=(
        "times new roman",
        18
    ),
    bg="#d3d3d3",
    fg="black"
)

password_label.place(
    x=75,
    y=405
)


# ============================================================
# PASSWORD ENTRY
# ============================================================

password_entry = Entry(
    login_frame,
    font=(
        "times new roman",
        18
    ),
    bg="white",
    fg="black",
    show="*",
    bd=1
)

password_entry.place(
    x=75,
    y=445,
    width=310,
    height=40
)


# ============================================================
# SHOW / HIDE PASSWORD
# ============================================================

password_visible = False


def toggle_password():

    global password_visible

    if password_visible:

        password_entry.config(
            show="*"
        )

        eye_button.config(
            text="👁"
        )

        password_visible = False

    else:

        password_entry.config(
            show=""
        )

        eye_button.config(
            text="🙈"
        )

        password_visible = True


eye_button = Button(
    login_frame,
    text="👁",
    font=("Arial", 14),
    bg="white",
    fg="black",
    bd=0,
    cursor="hand2",
    command=toggle_password
)

eye_button.place(
    x=390,
    y=448,
    width=40,
    height=34
)


# ============================================================
# LOGIN FUNCTION
# ============================================================

def login():

    employee_id = employee_id_entry.get().strip()

    password = password_entry.get().strip()


    # --------------------------------------------------------
    # Empty field validation
    # --------------------------------------------------------

    if employee_id == "":

        messagebox.showerror(
            "Error",
            "Please enter Employee Id.",
            parent=window
        )

        employee_id_entry.focus()

        return


    if password == "":

        messagebox.showerror(
            "Error",
            "Please enter Password.",
            parent=window
        )

        password_entry.focus()

        return


    # --------------------------------------------------------
    # Connect to database
    # --------------------------------------------------------

    connection = connect_database()

    if connection is None:

        return


    cursor = None


    try:

        cursor = connection.cursor()


        # ----------------------------------------------------
        # Check employee login
        # ----------------------------------------------------

        query = """
            SELECT empid, password, usertype
            FROM employee_data
            WHERE empid = %s
        """

        cursor.execute(
            query,
            (employee_id,)
        )

        result = cursor.fetchone()


        # ----------------------------------------------------
        # Employee not found
        # ----------------------------------------------------

        if result is None:

            messagebox.showerror(
                "Login Failed",
                "Invalid Employee Id.",
                parent=window
            )

            employee_id_entry.focus()

            return


        database_empid = result[0]

        database_password = result[1]

        usertype = result[2]


        # ----------------------------------------------------
        # Check password
        # ----------------------------------------------------

        if str(database_password) != password:

            messagebox.showerror(
                "Login Failed",
                "Invalid Password.",
                parent=window
            )

            password_entry.delete(
                0,
                END
            )

            password_entry.focus()

            return


        # ----------------------------------------------------
        # Login successful
        # ----------------------------------------------------

        messagebox.showinfo(
            "Success",
            "Login Successful!",
            parent=window
        )


        # ----------------------------------------------------
        # Close login window
        # ----------------------------------------------------

        window.destroy()


        # ----------------------------------------------------
        # Open dashboard
        #
        # IMPORTANT:
        # Do NOT use:
        #
        # from dashboard import open_dashboard
        #
        # because open_dashboard() does not exist in your
        # current dashboard.py.
        # ----------------------------------------------------

        import dashboard


    except mysql.connector.Error as e:

        messagebox.showerror(
            "Database Error",
            f"Database error:\n{e}",
            parent=window
        )


    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Something went wrong:\n{e}",
            parent=window
        )


    finally:

        if cursor is not None:

            cursor.close()

        if connection is not None:

            connection.close()


# ============================================================
# FORGOT PASSWORD
# ============================================================

def forgot_password():

    forgot_window = Toplevel(window)

    forgot_window.title(
        "Forgot Password"
    )

    forgot_window.geometry(
        "450x300"
    )

    forgot_window.resizable(
        False,
        False
    )

    forgot_window.config(
        bg="white"
    )


    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    Label(
        forgot_window,
        text="Reset Password",
        font=(
            "times new roman",
            24,
            "bold"
        ),
        bg="#0f4d7d",
        fg="white"
    ).pack(
        fill=X
    )


    # --------------------------------------------------------
    # EMPLOYEE ID
    # --------------------------------------------------------

    Label(
        forgot_window,
        text="Employee Id",
        font=(
            "times new roman",
            16
        ),
        bg="white"
    ).place(
        x=50,
        y=80
    )


    forgot_id = Entry(
        forgot_window,
        font=(
            "times new roman",
            16
        )
    )

    forgot_id.place(
        x=50,
        y=115,
        width=340,
        height=35
    )


    # --------------------------------------------------------
    # NEW PASSWORD
    # --------------------------------------------------------

    Label(
        forgot_window,
        text="New Password",
        font=(
            "times new roman",
            16
        ),
        bg="white"
    ).place(
        x=50,
        y=160
    )


    new_password = Entry(
        forgot_window,
        font=(
            "times new roman",
            16
        ),
        show="*"
    )

    new_password.place(
        x=50,
        y=195,
        width=340,
        height=35
    )


    # ========================================================
    # RESET PASSWORD FUNCTION
    # ========================================================

    def reset_password():

        empid = forgot_id.get().strip()

        new_pass = new_password.get().strip()


        # ----------------------------------------------------
        # Validate fields
        # ----------------------------------------------------

        if empid == "" or new_pass == "":

            messagebox.showerror(
                "Error",
                "Please fill all fields.",
                parent=forgot_window
            )

            return


        # ----------------------------------------------------
        # Connect to database
        # ----------------------------------------------------

        connection = connect_database()

        if connection is None:

            return


        cursor = None


        try:

            cursor = connection.cursor()


            # ------------------------------------------------
            # Check employee
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT empid
                FROM employee_data
                WHERE empid = %s
                """,
                (empid,)
            )


            if cursor.fetchone() is None:

                messagebox.showerror(
                    "Error",
                    "Employee Id not found.",
                    parent=forgot_window
                )

                return


            # ------------------------------------------------
            # Update password
            # ------------------------------------------------

            cursor.execute(
                """
                UPDATE employee_data
                SET password = %s
                WHERE empid = %s
                """,
                (new_pass, empid)
            )


            connection.commit()


            # ------------------------------------------------
            # Success
            # ------------------------------------------------

            messagebox.showinfo(
                "Success",
                "Password updated successfully.",
                parent=forgot_window
            )


            forgot_window.destroy()


        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=forgot_window
            )


        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e),
                parent=forgot_window
            )


        finally:

            if cursor is not None:

                cursor.close()

            if connection is not None:

                connection.close()


    # ========================================================
    # RESET PASSWORD BUTTON
    # ========================================================

    Button(
        forgot_window,
        text="Reset Password",
        font=(
            "times new roman",
            15,
            "bold"
        ),
        bg="#0f4d7d",
        fg="white",
        cursor="hand2",
        command=reset_password
    ).place(
        x=125,
        y=245,
        width=200,
        height=40
    )


# ============================================================
# FORGOT PASSWORD BUTTON
# ============================================================

forgot_button = Button(
    login_frame,
    text="Forgot Password?",
    font=(
        "times new roman",
        14
    ),
    bg="#d3d3d3",
    fg="#4d94d9",
    activebackground="#d3d3d3",
    activeforeground="#0f4d7d",
    bd=0,
    cursor="hand2",
    command=forgot_password
)

forgot_button.place(
    x=75,
    y=490
)


# ============================================================
# LOGIN BUTTON
# ============================================================

login_button = Button(
    login_frame,
    text="Login",
    font=(
        "times new roman",
        18
    ),
    bg="#4d94d9",
    fg="white",
    activebackground="#0f4d7d",
    activeforeground="white",
    cursor="hand2",
    bd=1,
    command=login
)

login_button.place(
    x=75,
    y=555,
    width=315,
    height=55
)


# ============================================================
# ENTER KEY = LOGIN
# ============================================================

window.bind(
    "<Return>",
    lambda event: login()
)


# ============================================================
# INITIAL FOCUS
# ============================================================

employee_id_entry.focus()


# ============================================================
# START APPLICATION
# ============================================================

window.mainloop()
