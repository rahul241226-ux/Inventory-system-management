

import pymysql
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date



def connect_database():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Sswashank@12345'
        )
        cursor = connection.cursor()

    except:
        messagebox.showerror(
            "Error",
            "Database connectivity issue, try again!, please open mysql command line client"

        )
        return None,None


    return cursor,connection

    connection.commit()
    connection.close()



def create_database_table():
        cursor,connection = connect_database()
        cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_system')
        cursor.execute('USE inventory_system')

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS employee_data
                       (
                           empid
                           INT
                           PRIMARY
                           KEY,
                           name
                           VARCHAR
                       (
                           100
                       ),
                           email VARCHAR
                       (
                           150
                       ),
                           gender VARCHAR
                       (
                           50
                       ),
                           dob VARCHAR
                       (
                           100
                       ),
                           contact VARCHAR
                       (
                           100
                       ),
                           employement_type VARCHAR
                       (
                           50
                       ),
                           work_shift VARCHAR
                       (
                           50
                       ),
                           education VARCHAR
                       (
                           100
                       ),
                           address VARCHAR
                       (
                           100
                       ),
                           doj VARCHAR
                       (
                           100
                       ),
                           salary VARCHAR
                       (
                           100
                       ),
                           usertype VARCHAR
                       (
                           100
                       ),
                           password VARCHAR
                       (
                           100
                       )
                           )
                       ''')


def treeview_data():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    cursor.execute('use inventory_system')


    try:
        cursor.execute('SELECT * FROM employee_data')
        employee_records=cursor.fetchall()
        employee_treeview.delete(*employee_treeview.get_children())
        for record in employee_records:
            employee_treeview.insert('',END,values=record)

    except EXCEPTION as e:
        messagebox.showerror('Error',f'Error due to {e}')


    finally:
        cursor.close()
        connection.close()






def add_employee(empid,name,email,gender,dob,contact,empolyement_type
                 ,education,work_shift,
                 address,doj,salary,user_type,password):


    if (
            empid=='' or name =='' or email=='' or gender =='Select Gender' or contact =='' or empolyement_type=='Select type' or
            education == 'Select Education' or work_shift =="Select s=Shift" or address=='\n' or salary=='' or user_type=="Select User Type" or password==''):
        messagebox.showerror("Error","All details is required!")

    else:
        cursor,connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        try:
            cursor.execute(
                'SELECT empid FROM employee_data WHERE empid=%s',
                (empid,)
            )

            if cursor.fetchone():
                messagebox.showerror('Error', 'Id already exists')
                return

            cursor.execute(
                '''INSERT INTO employee_data
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (
                    empid,
                    name,
                    email,
                    gender,
                    dob,
                    contact,
                    empolyement_type,
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
            treeview_data()

            messagebox.showinfo(
                'Success',
                'Data is inserted successfully'
            )

        except Exception as e:
            messagebox.showerror(
                'Error',
                f'Error due to {e}'
            )

        finally:
            cursor.close()
            connection.close()




def clear_fields(empid_entry,
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
password_entry):

    empid_entry.delete(0, END)
    name_entry.delete(0, END)
    email_entry.delete(0, END)

    gender_combobox.set('Select Gender')
    dob_entry.set_date(date.today())
    contact_entry.delete(0, END)

    employement_type_combobox.set('')
    education_combobox.set('Education Type')
    work_shift_combobox.set('Select shift')

    address_text.delete(1.0, END)

    doj_label_entry.set_date(date.today())
    salary_entry.delete(0, END)

    usertype_type_combobox.set('Select usertype')
    password_entry.delete(0, END)



def employee_form(window):
  global employee_treeview
  employee_frame= Frame(window,width=1330,height=690,bg='white')
  employee_frame.place(x=200,y=100)
  heading_label=Label(employee_frame,text='Manage Employee Details',
                      font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
  heading_label.place(x=0,y=0,relwidth=1)


  #back button




  #frame
  topFrame=Frame(employee_frame,bg='white')
  topFrame.place(x=0,y=60,relwidth=1,height=235)

  back_button = Button(topFrame, text='Back', width=10, cursor='hand2', bg='white',
                       command=lambda: employee_frame.place_forget())
  back_button.place(x=10, y=10)
  searchframe=Frame(topFrame,bg='white')
  searchframe.pack()

  search_combobox=ttk.Combobox(searchframe,values=('Id','Name','Email','employment_type','work_shift','Education','Salary'),font=('times new roman',12),state='readonly')
  search_combobox.set('Search By')
  search_combobox.grid(row=0,column=0,padx=20)

  search_entry= Entry(searchframe,font=('times new roman',12),bg='lightyellow')
  search_entry.grid(row=0,column=1)

  search_button=Button(searchframe,text='Search',font=('times new roman',12),width=10,cursor='hand2',fg='white',bg='#0f4d74')
  search_button.grid(row=0,column=2,padx=20)

  #scrollbar

  horizontal_scrollbar=Scrollbar(topFrame,orient=HORIZONTAL)
  vertical_scrollbar=Scrollbar(topFrame,orient=VERTICAL)

  show_button = Button(searchframe, text='Show All', font=('times new roman', 12),width=10,cursor='hand2',fg='white',bg='#0f4d74')
  show_button.grid(row=0, column=3)

  employee_treeview = ttk.Treeview(
      topFrame,
      columns=(
          'empid',
          'name',
          'email',
          'gender',
          'dob',
          'contact',
          'employement_type',
          'education',
          'work_shift',
          'address',
          'doj',
          'salary',
          'usertype'
      ),
      show='headings',
      yscrollcommand=vertical_scrollbar.set,
      xscrollcommand=horizontal_scrollbar.set
  )


  vertical_scrollbar.pack(side=RIGHT, fill=Y,pady=(10,0))
  horizontal_scrollbar.pack(side=BOTTOM, fill=X)
  horizontal_scrollbar.config(command=employee_treeview.xview)
  vertical_scrollbar.config(command=employee_treeview.yview)

  employee_treeview.pack(pady=(10,0))

  employee_treeview.heading('empid', text='EmpId')
  employee_treeview.heading('name', text='Name')
  employee_treeview.heading('email', text='Email')
  employee_treeview.heading('gender', text='Gender')
  employee_treeview.heading('dob', text='Date of birth')
  employee_treeview.heading('contact', text='Contact')
  employee_treeview.heading('employement_type', text='Employment Type')
  employee_treeview.heading('education', text='Education')
  employee_treeview.heading('work_shift', text='Shift')
  employee_treeview.heading('address', text='Address')
  employee_treeview.heading('doj', text='Date of joining')
  employee_treeview.heading('salary', text='Salary')
  employee_treeview.heading('usertype', text='Usertype')

  employee_treeview.column('empid',width=60)
  employee_treeview.column('name',width=140)
  employee_treeview.column('email',width=200)
  employee_treeview.column('gender',width=60)
  employee_treeview.column('dob',width=140)
  employee_treeview.column('contact',width=140)
  employee_treeview.column('employement_type',width=120)
  employee_treeview.column('education',width=140)
  employee_treeview.column('work_shift',width=120)
  employee_treeview.column('address',width=190)
  employee_treeview.column('doj',width=140)
  employee_treeview.column('salary',width=120)
  employee_treeview.column('usertype',width=140)

  treeview_data()

  detail_frame=Frame(employee_frame,bg='white')
  detail_frame.place(x=100,y=300)


  empid_label=Label(detail_frame,text='EmpId:', font=('times new roman', 12))
  empid_label.grid(row=0,column=0,padx=20,pady=10,sticky='w')
  empid_entry=Entry(detail_frame,font=('times new roman', 12),bg='lightyellow')
  empid_entry.grid(row=0,column=1,padx=20,pady=10)

  name_label=Label(detail_frame,text='Name:', font=('times new roman', 12))
  name_label.grid(row=0,column=2,padx=20,pady=10,sticky='w')
  name_entry=Entry(detail_frame,font=('times new roman', 12),bg='lightyellow')
  name_entry.grid(row=0,column=3,padx=20,pady=10)

  email_label=Label(detail_frame,text='Email:', font=('times new roman', 12))
  email_label.grid(row=0,column=4,padx=20,pady=10,sticky='w')
  email_entry=Entry(detail_frame,font=('times new roman', 12),bg='lightyellow')
  email_entry.grid(row=0,column=5,padx=20,pady=10)

  gender_label=Label(detail_frame,text='Gender:', font=('times new roman', 12))
  gender_label.grid(row=1,column=0,padx=20,pady=10,sticky='w')
  gender_combobox=ttk.Combobox(detail_frame,values=('Male','Female'),font=('times new roman',12),width=18,state='readonly')
  gender_combobox.set('Select Gender')
  gender_combobox.grid(row=1,column=1)


  dob_label=Label(detail_frame,text='Date of birth:', font=('times new roman', 12))
  dob_label.grid(row=1,column=2,padx=20,pady=10,sticky='w')
  dob_entry=DateEntry(detail_frame,font=('times new roman', 12),width=18,date_pattern='dd/mm/yyyy')
  dob_entry.grid(row=1,column=3,padx=20,pady=10)

  contact_label=Label(detail_frame,text='Contact:', font=('times new roman', 12))
  contact_label.grid(row=1,column=4,padx=20,pady=10,sticky='w')
  contact_entry=Entry(detail_frame,font=('times new roman', 12),bg='lightyellow')
  contact_entry.grid(row=1,column=5,padx=20,pady=10)

  employement_type_label=Label(detail_frame,text='Employement Type:', font=('times new roman', 12))
  employement_type_label.grid(row=2,column=0,padx=20,pady=10,sticky='w')
  employement_type_combobox = ttk.Combobox(detail_frame, values=('full time', 'part time'), font=('times new roman', 12), width=18,state='readonly')
  employement_type_combobox.set('Employement Type')
  employement_type_combobox.grid(row=2, column=1)


  education_label=Label(detail_frame,text='Education:', font=('times new roman', 12))
  education_label.grid(row=2,column=2,padx=20,pady=10,sticky='w')
  education_combobox = ttk.Combobox(detail_frame, values=('B.tech', 'B.com','M.com','B.Sc','M.Sc','BBA','MBA'), font=('times new roman', 12), width=18, state='readonly')
  education_combobox.set('Select Education')
  education_combobox.grid(row=2, column=3)



  work_shift_label=Label(detail_frame,text='Work Shift:', font=('times new roman', 12))
  work_shift_label.grid(row=2,column=4,padx=20,pady=10,sticky='w')
  work_shift_combobox = ttk.Combobox(detail_frame, values=('Morning', 'Evening', 'Night'),
                                    font=('times new roman', 12), width=18, state='readonly')
  work_shift_combobox.set('Select shift')
  work_shift_combobox.grid(row=2, column=5)


  address_label=Label(detail_frame,text='Address:', font=('times new roman', 12))
  address_label.grid(row=3,column=0,padx=20,pady=10,sticky='w')
  # address_entry=Entry(detail_frame,)
  address_text=Text(detail_frame,width=20,height=3,font=('times new roman', 12),bg='lightyellow')
  address_text.grid(row=3,column=1,padx=20,pady=10)

  doj_label=Label(detail_frame,text='Date of joining:', font=('times new roman', 12))
  doj_label.grid(row=3,column=2,padx=20,pady=10,sticky='w')
  doj_label_entry = DateEntry(detail_frame, font=('times new roman', 12), width=18, date_pattern='dd/mm/yyyy')
  doj_label_entry.grid(row=3, column=3, padx=20, pady=10)


  salary_label=Label(detail_frame,text='Salary:', font=('times new roman', 12))
  salary_label.grid(row=3,column=4,padx=20,pady=10,sticky='w')
  salary_entry=Entry(detail_frame,font=('times new roman', 12),bg='lightyellow')
  salary_entry.grid(row=3,column=5,padx=20,pady=10)

  usertype_label=Label(detail_frame,text='Usertype:', font=('times new roman', 12))
  usertype_label.grid(row=4,column=2,padx=20,pady=10,sticky='w')
  usertype_type_combobox = ttk.Combobox(detail_frame, values=('Admin', 'Employee'),
                                           font=('times new roman', 12), width=18, state='readonly')
  usertype_type_combobox.set('User Type')
  usertype_type_combobox.grid(row=4, column=3)


  password_label=Label(detail_frame,text='Password:', font=('times new roman', 12))
  password_label.grid(row=4,column=4,padx=20,pady=10,sticky='w')
  password_entry=Entry(detail_frame,font=('times new roman', 12),bg='lightyellow')
  password_entry.grid(row=4,column=5,padx=20,pady=10)


  button_frame=Frame(employee_frame,bg='white')
  button_frame.place(x=250,y=600)
  add_button=Button(button_frame,text='Add',font=('times new roman',12),width=10,cursor='hand2',fg='white',bg='#0f4d74',command=lambda :add_employee(empid_entry.get(),name_entry.get(),email_entry.get(),gender_combobox.get(),
                                                                                                                                           dob_entry.get(),contact_entry.get(),employement_type_combobox.get()
                                                                                                                                             ,education_combobox.get(),work_shift_combobox.get(),address_text.get(1.0,END),
                                                                                                                                             doj_label_entry.get(),salary_entry.get(),usertype_type_combobox.get(),password_entry.get() ))
  add_button.grid(row=0,column=0,padx=20)


  update_button=Button(button_frame,text='Update',font=('times new roman',12),width=10,cursor='hand2',fg='white',bg='#0f4d74')
  update_button.grid(row=0,column=1,padx=20,pady=10)

  delete_button = Button(button_frame, text='Delete', font=('times new roman', 12), width=10, cursor='hand2',
                         fg='white', bg='#0f4d74')
  delete_button.grid(row=0, column=2, padx=20, pady=10)

  clear_button = Button(button_frame, text='Clear', font=('times new roman', 12), width=10, cursor='hand2',
                         fg='white', bg='#0f4d74',command=lambda :clear_fields(empid_entry,
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
password_entry))
  clear_button.grid(row=0, column=3, padx=20, pady=10)


  create_database_table()