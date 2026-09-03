from tkinter import *


from PIL import Image, ImageTk
from unicodedata import category

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
    font=('times new roman', 20, 'bold'),anchor='w',padx=10
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



