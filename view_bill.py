from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os


# ============================================================
# VIEW CUSTOMER BILLS
# ============================================================

def view_bill(window):

    # ========================================================
    # BILL FOLDER
    # ========================================================

    # All generated customer bills should be saved here
    BILL_FOLDER = "bills"

    # Create bills folder automatically if it doesn't exist
    if not os.path.exists(BILL_FOLDER):
        os.makedirs(BILL_FOLDER)


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
    # FUNCTIONS
    # ========================================================

    def clear_bill_area():

        bill_area.config(state=NORMAL)

        bill_area.delete(
            "1.0",
            END
        )

        bill_area.config(state=DISABLED)


    # --------------------------------------------------------
    # LOAD ALL BILLS
    # --------------------------------------------------------

    def load_bills():

        bill_listbox.delete(
            0,
            END
        )

        try:

            files = os.listdir(BILL_FOLDER)

            bill_files = []

            for file in files:

                if file.lower().endswith(".txt"):

                    bill_files.append(file)


            # Sort invoice numbers
            bill_files.sort(
                key=lambda x: os.path.splitext(x)[0]
            )


            for file in bill_files:

                bill_listbox.insert(
                    END,
                    file
                )


        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to load bills:\n{e}"
            )


    # --------------------------------------------------------
    # SHOW SELECTED BILL
    # --------------------------------------------------------

    def show_bill(event=None):

        selected = bill_listbox.curselection()

        if not selected:
            return


        bill_name = bill_listbox.get(
            selected[0]
        )


        bill_path = os.path.join(
            BILL_FOLDER,
            bill_name
        )


        if not os.path.exists(bill_path):

            messagebox.showerror(
                "Error",
                "Bill file does not exist."
            )

            return


        try:

            with open(
                bill_path,
                "r",
                encoding="utf-8"
            ) as file:

                bill_data = file.read()


            bill_area.config(
                state=NORMAL
            )


            bill_area.delete(
                "1.0",
                END
            )


            bill_area.insert(
                END,
                bill_data
            )


            bill_area.config(
                state=DISABLED
            )


            # Start scrollbar at top
            bill_area.yview_moveto(0)


        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to open bill:\n{e}"
            )


    # --------------------------------------------------------
    # SEARCH BILL
    # --------------------------------------------------------

    def search_bill():

        invoice = invoice_entry.get().strip()


        if invoice == "":

            messagebox.showwarning(
                "Warning",
                "Please enter Invoice Number."
            )

            return


        found = False


        for i in range(
            bill_listbox.size()
        ):

            bill_name = bill_listbox.get(i)


            # Remove .txt
            invoice_number = os.path.splitext(
                bill_name
            )[0]


            if invoice_number == invoice:

                bill_listbox.selection_clear(
                    0,
                    END
                )


                bill_listbox.selection_set(
                    i
                )


                bill_listbox.see(i)


                show_bill()


                found = True

                break


        if not found:

            clear_bill_area()

            messagebox.showerror(
                "Error",
                f"Invoice No. {invoice} not found."
            )


    # --------------------------------------------------------
    # CLEAR SEARCH
    # --------------------------------------------------------

    def clear_search():

        invoice_entry.delete(
            0,
            END
        )


        bill_listbox.selection_clear(
            0,
            END
        )


        clear_bill_area()


        invoice_entry.focus()


    # --------------------------------------------------------
    # BACK BUTTON
    # --------------------------------------------------------

    def back():

        bill_frame.destroy()


    # --------------------------------------------------------
    # REFRESH BILL LIST
    # --------------------------------------------------------

    def refresh_bills():

        load_bills()

        clear_bill_area()

        invoice_entry.delete(
            0,
            END
        )


    # ========================================================
    # HEADING
    # ========================================================

    heading_label = Label(
        bill_frame,
        text="View Customer Bills",
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
    # SEARCH LABEL
    # ========================================================

    invoice_label = Label(
        bill_frame,
        text="Invoice No.",
        font=(
            "times new roman",
            16,
            "bold"
        ),
        bg="white",
        fg="black"
    )

    invoice_label.place(
        x=80,
        y=100
    )


    # ========================================================
    # INVOICE ENTRY
    # ========================================================

    invoice_entry = Entry(
        bill_frame,
        font=(
            "times new roman",
            16
        ),
        bg="#ffffe0",
        fg="black",
        bd=1,
        relief=SOLID
    )

    invoice_entry.place(
        x=225,
        y=95,
        width=195,
        height=40
    )


    # ========================================================
    # SEARCH BUTTON
    # ========================================================

    search_button = Button(
        bill_frame,
        text="Search",
        font=(
            "times new roman",
            15,
            "bold"
        ),
        bg="#0f4d7d",
        fg="white",
        activebackground="#083b5c",
        activeforeground="white",
        bd=2,
        cursor="hand2",
        command=search_bill
    )

    search_button.place(
        x=450,
        y=90,
        width=125,
        height=50
    )


    # ========================================================
    # CLEAR BUTTON
    # ========================================================

    clear_button = Button(
        bill_frame,
        text="Clear",
        font=(
            "times new roman",
            15,
            "bold"
        ),
        bg="#0f4d7d",
        fg="white",
        activebackground="#083b5c",
        activeforeground="white",
        bd=2,
        cursor="hand2",
        command=clear_search
    )

    clear_button.place(
        x=600,
        y=90,
        width=125,
        height=50
    )


    # ========================================================
    # BILL LIST FRAME
    # ========================================================

    list_frame = Frame(
        bill_frame,
        bg="white",
        bd=1,
        relief=SOLID
    )

    list_frame.place(
        x=30,
        y=195,
        width=300,
        height=495
    )


    # ========================================================
    # BILL LISTBOX
    # ========================================================

    bill_listbox = Listbox(
        list_frame,
        font=(
            "times new roman",
            14
        ),
        bg="white",
        fg="black",
        selectbackground="#0f4d7d",
        selectforeground="white",
        activestyle="none",
        bd=0
    )

    bill_listbox.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )


    # ========================================================
    # LIST SCROLLBAR
    # ========================================================

    list_scrollbar = Scrollbar(
        list_frame,
        orient=VERTICAL,
        command=bill_listbox.yview
    )

    list_scrollbar.pack(
        side=RIGHT,
        fill=Y
    )


    bill_listbox.config(
        yscrollcommand=list_scrollbar.set
    )


    # ========================================================
    # BILL LIST EVENTS
    # ========================================================

    bill_listbox.bind(
        "<<ListboxSelect>>",
        show_bill
    )


    # ========================================================
    # CUSTOMER BILL AREA
    # ========================================================

    bill_area_frame = Frame(
        bill_frame,
        bg="white",
        bd=1,
        relief=SOLID
    )

    bill_area_frame.place(
        x=375,
        y=195,
        width=620,
        height=495
    )


    # ========================================================
    # BILL AREA HEADING
    # ========================================================

    bill_heading = Label(
        bill_area_frame,
        text="Customer Bill Area",
        font=(
            "times new roman",
            18,
            "bold"
        ),
        bg="#0f4d7d",
        fg="white"
    )

    bill_heading.pack(
        fill=X
    )


    # ========================================================
    # BILL TEXT FRAME
    # ========================================================

    bill_text_frame = Frame(
        bill_area_frame,
        bg="white"
    )

    bill_text_frame.pack(
        fill=BOTH,
        expand=True
    )


    # ========================================================
    # BILL TEXT SCROLLBAR
    # ========================================================

    bill_scrollbar = Scrollbar(
        bill_text_frame,
        orient=VERTICAL
    )

    bill_scrollbar.pack(
        side=RIGHT,
        fill=Y
    )


    # ========================================================
    # BILL TEXT
    # ========================================================

    bill_area = Text(
        bill_text_frame,
        font=(
            "Courier New",
            11
        ),
        bg="white",
        fg="black",
        bd=0,
        wrap=NONE,
        yscrollcommand=bill_scrollbar.set
    )

    bill_area.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )


    bill_scrollbar.config(
        command=bill_area.yview
    )


    bill_area.config(
        state=DISABLED
    )


    # ========================================================
    # RIGHT SIDE IMAGE
    # ========================================================

    try:

        image = Image.open(
            "bill.png"
        )


        image = image.resize(
            (500, 400)
        )


        bill_image = ImageTk.PhotoImage(
            image
        )


        image_label = Label(
            bill_frame,
            image=bill_image,
            bg="white"
        )


        image_label.image = bill_image


        image_label.place(
            x=1010,
            y=200
        )


    except FileNotFoundError:

        print(
            "bill.png not found."
        )


    except Exception as e:

        print(
            "Unable to load bill image:",
            e
        )


    # ========================================================
    # LOAD ALL BILLS WHEN WINDOW OPENS
    # ========================================================

    load_bills()


    # Put cursor in invoice field
    invoice_entry.focus()