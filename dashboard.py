from tkinter import *
from tkinter import ttk
from tkinter.ttk import Treeview
from tkcalendar import DateEntry

from unicodedata import category
from PIL import Image, ImageTk

#Functionality part

def employee_form():
  employee_frame= Frame(window,width=1330,height=690,bg='white')
  employee_frame.place(x=200,y=100)
  heading_label=Label(employee_frame,text='Manage Employee Details', font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
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
  doj_entry=Entry(detail_frame,font=('times new roman', 12),bg='lightyellow')
  doj_entry.grid(row=3,column=3,padx=20,pady=10)

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
  add_button=Button(button_frame,text='Add',font=('times new roman',12),width=10,cursor='hand2',fg='white',bg='#0f4d74')
  add_button.grid(row=0,column=0,padx=20)


  update_button=Button(button_frame,text='Update',font=('times new roman',12),width=10,cursor='hand2',fg='white',bg='#0f4d74')
  update_button.grid(row=0,column=1,padx=20,pady=10)

  delete_button = Button(button_frame, text='Delete', font=('times new roman', 12), width=10, cursor='hand2',
                         fg='white', bg='#0f4d74')
  delete_button.grid(row=0, column=2, padx=20, pady=10)

  clear_button = Button(button_frame, text='Clear', font=('times new roman', 12), width=10, cursor='hand2',
                         fg='white', bg='#0f4d74')
  clear_button.grid(row=0, column=3, padx=20, pady=10)


#GUI PART





window=Tk()

#adding main window with size and color
window.title('Dashboard')
window.geometry("1530x880+0+0")
window.resizable(0,0)
window.config(bg='white')


#adding image and resize as you choice
image = Image.open("icons/checklist.png")
image = image.resize((64, 64))
bg_Image = ImageTk.PhotoImage(image)



#adding label
titleLabel = Label(window,image = bg_Image,compound=LEFT, text='  Inventory management system',font=('times new roman',40,'bold'),bg="#010c48",fg='white',anchor='w',padx=20)
titleLabel.place(x=0,y=0,relwidth=1)




#adding button
logoutButton = Button(window,text='Logout',font=('times new roman',20,'bold'),fg="#010c48")
logoutButton.place(x=1350,y=10)


#label
subtitlelabel= Label(window,text='Welcome Admin\t\t Date:09-03-2026\t\t Timme:11:53:45 am',font=('times new roman ',12),bg='#4d636d',fg='white')
subtitlelabel.place(x=0,y=70,relwidth=1)


#left-side bar (frame,logo,image,button)
leftframe = Frame(window)
leftframe.place(x=0,y=102,width=200,height=790)

#logoimage
logoimage = Image.open("icons/list.png")
logoimage = logoimage.resize((64, 64))
logoimage = ImageTk.PhotoImage(logoimage)
imageLabel = Label(leftframe, image=logoimage)
imageLabel.pack()

menulabel= Label(leftframe,text='Menu',font=('times new roman',20),bg='#009688')
menulabel.pack(fill=X)
employee_icon = Image.open("icons/employee.png")
employee_icon = employee_icon.resize((24, 24))
employee_icon = ImageTk.PhotoImage(employee_icon)

employee_button = Button(
    leftframe,
    image=employee_icon,
    compound=LEFT,
    text=' Employee',
    font=('times new roman', 20, 'bold'),
    anchor='w',
    padx=10,
    command=employee_form
)
employee_button.pack(fill=X)


supplier_icon = Image.open("icons/supplier.png")
supplier_icon = supplier_icon.resize((24, 24))
supplier_icon = ImageTk.PhotoImage(supplier_icon)

supplier_button = Button(
    leftframe,
    image=supplier_icon,
    compound=LEFT,
    text=' Supplier',
    font=('times new roman', 20, 'bold'),
    anchor='w',
    padx=10
)
supplier_button.pack(fill=X)


category_icon = Image.open("icons/catagory.png")
category_icon = category_icon.resize((24, 24))
category_icon = ImageTk.PhotoImage(category_icon)

category_button = Button(
    leftframe,
    image=category_icon,
    compound=LEFT,
    text=' Category',
    font=('times new roman', 20, 'bold'),
    anchor='w',
    padx=10
)
category_button.pack(fill=X)


product_icon = Image.open("icons/product.png")
product_icon = product_icon.resize((24, 24))
product_icon = ImageTk.PhotoImage(product_icon)

product_button = Button(
    leftframe,
    image=product_icon,
    compound=LEFT,
    text=' Product',
    font=('times new roman', 20, 'bold'),
    anchor='w',
padx=10
)
product_button.pack(fill=X)


sales_icon = Image.open("icons/sales.png")
sales_icon = sales_icon.resize((24, 24))
sales_icon = ImageTk.PhotoImage(sales_icon)

sales_button = Button(
    leftframe,
    image=sales_icon,
    compound=LEFT,
    text=' Sales',
    font=('times new roman', 20, 'bold'),
    anchor='w',
    padx=10

)
sales_button.pack(fill=X)


exit_icon = Image.open("icons/exit.png")
exit_icon = exit_icon.resize((24, 24))
exit_icon = ImageTk.PhotoImage(exit_icon)

exit_button = Button(
    leftframe,
    image=exit_icon,
    compound=LEFT,
    text=' Exit',
    font=('times new roman', 20, 'bold'),
    anchor='w',
    padx=10
)
exit_button.pack(fill=X)


#frames in main windoes

#1.employee
emp_frame = Frame(window,bg='#2C3E50',bd=3,relief=RIDGE)
emp_frame.place(x=400,y=125,width=300,height=200)


emp_icon = Image.open("icons/emp.png")
emp_icon = emp_icon.resize((80, 80))
emp_icon = ImageTk.PhotoImage(emp_icon)
emp_icon_label = Label(emp_frame, image=emp_icon,bg='#2C3E50')
emp_icon_label.pack()

emp_icon_label = Label(emp_frame,text='Total Employee',bg='#2C3E50',font=('times new roman',20),fg='white')
emp_icon_label.pack()


emp_icon_count_label = Label(emp_frame,text='0',bg='#2C3E50',font=('times new roman',30),fg='white')
emp_icon_count_label.pack()


#2.SUPPLIER


supp_frame = Frame(window,bg='#8E44AD',bd=3,relief=RIDGE)
supp_frame.place(x=800,y=125,width=300,height=200)


supp_icon = Image.open("icons/suppliers.png")
supp_icon = supp_icon.resize((80, 80))
supp_icon = ImageTk.PhotoImage(supp_icon)
supp_icon_label = Label(supp_frame, image=supp_icon,bg='#8E44AD')
supp_icon_label.pack()

supp_icon_label = Label(supp_frame,text='Total Suppliers',bg='#8E44AD',font=('times new roman',20),fg='white')
supp_icon_label.pack()


supp_icon_count_label = Label(supp_frame,text='0',bg='#8E44AD',font=('times new roman',30),fg='white')
supp_icon_count_label.pack()


#3.EMPLOYESS



cat_frame = Frame(window,bg='#27AE60',bd=3,relief=RIDGE)
cat_frame.place(x=1200,y=125,width=300,height=200)


cat_icon = Image.open("icons/catagory.png")
cat_icon = cat_icon.resize((80, 80))
cat_icon = ImageTk.PhotoImage(cat_icon)
cat_icon_label = Label(cat_frame, image=cat_icon,bg='#27AE60')
cat_icon_label.pack()

cat_icon_label = Label(cat_frame,text='Total Catagories',bg='#27AE60',font=('times new roman',20),fg='white')
cat_icon_label.pack()


cat_icon_count_label = Label(cat_frame,text='0',bg='#27AE60',font=('times new roman',30),fg='white')
cat_icon_count_label.pack()


#PRODUCTS



prod_frame = Frame(window,bg='#2C3E50',bd=3,relief=RIDGE)
prod_frame.place(x=400,y=525,width=300,height=200)


prod_icon = Image.open("icons/product.png")
prod_icon = prod_icon.resize((80, 80))
prod_icon = ImageTk.PhotoImage(prod_icon)
prod_icon_label = Label(prod_frame, image=prod_icon,bg='#2C3E50')
prod_icon_label.pack()

prod_icon_label = Label(prod_frame,text='Total Products',bg='#2C3E50',font=('times new roman',20),fg='white')
prod_icon_label.pack()


cat_icon_count_label = Label(prod_frame,text='0',bg='#2C3E50',font=('times new roman',30),fg='white')
cat_icon_count_label.pack()

#SALES

sale_frame = Frame(window,bg='#E74C3C',bd=3,relief=RIDGE)
sale_frame.place(x=800,y=525,width=300,height=200)


sale_icon = Image.open("icons/sales.png")
sale_icon = sale_icon.resize((80, 80))
sale_icon = ImageTk.PhotoImage(sale_icon)
sale_icon_label = Label(sale_frame, image=sale_icon,bg='#E74C3C')
sale_icon_label.pack()

sale_icon_label = Label(sale_frame,text='Total Sales',bg='#E74C3C',font=('times new roman',20),fg='white')
sale_icon_label.pack()


sale_icon_count_label = Label(sale_frame,text='0',bg='#E74C3C',font=('times new roman',30),fg='white')
sale_icon_count_label.pack()


window.mainloop()



