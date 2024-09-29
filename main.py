from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter
from tkinter import filedialog
import random
import pymysql
import csv
from datetime import datetime
import datetime
import numpy

#########################################################################################################################

win= tkinter.Tk()
win.title("Inventory Management System")
win.geometry("2075x640")
win.configure(bg="#F1F8E8")
my_tree= ttk.Treeview(win,show="headings",height=20)
style=ttk.Style()

placeholdeArray=['','','','','']
num = "123456789"
alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

for i in range(0,5):
    placeholdeArray[i]=tkinter.StringVar()

#########################################################################################################################

def connect():
    con=pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='stock_mangement'
    )    
    return con


con = connect()
cursor=con.cursor()
def read():
    cursor.connection.ping()
    sql =f"SELECT `item id`, `name`, `price`, `quantity`, `category`, `date` FROM stock ORDER BY 'id' DESC"
    cursor.execute(sql)
    results=cursor.fetchall()
    con.commit()
    con.close()
    return results


def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)
    for array in read():
        my_tree.insert(parent='',index='end',iid=array,text="",values=(array),tag="orow")
    my_tree.tag_configure('orwo',background="#e5e5e5")
    my_tree.pack()

def savph(word,num):
    for ph in range(0,5):
        if ph == num:
            placeholdeArray[ph].set(word)

def genrateRand():
    itemid=''
    for i in range(0,3):
        ranno = random.randrange(0,(len(num)-1))
        itemid =itemid+str(num[ranno])
    ranal=random.randrange(0,(len(alpha)-1))
    itemid=itemid+'-'+str(alpha[ranal])
    print("genrated:"+ itemid)  
    savph(itemid,0)  
    

def save():
    itemid = str(itemidEntry.get())    
    name = str(nameEntry.get())    
    price = str(priceEntry.get())    
    quantity = str(qntEntry.get())    
    category = str(categoryCombo.get())
    
    valid = True
    if not(itemid and itemid.strip()) or not(name and name.strip()) or not(price and price.strip()) or not(quantity and quantity.strip()) or not(category and category.strip()):
        messagebox.showwarning("","Please fill all the fields")
        return
    if len(itemid) < 5:
        messagebox.showwarning("","Invalid item id") 
        return
    if (not(itemid[3]=='-')):
        valid = False
    for i in range(0,3):
        if(not(itemid[i] in num)):
            valid = False
            break
    if (not(itemid[4] in  alpha)):
        valid = False
    if not(valid):
        messagebox.showwarning("","Invalid Item ID")
        return    
    
    try:
        cursor.connection.ping()
        sql =f"SELECT * FROM stock WHERE `item id` = '{itemid}'"
        cursor.execute(sql)
        checkitem=cursor.fetchall()
        if len(checkitem) > 0 :
            messagebox.showwarning("","Item ID already exists")
            return
        else:
            cursor.connection.ping()
            sql = f"INSERT INTO stock(`item id`, `name`, `price`, `quantity`, `category`) VALUES ('{itemid}','{name}','{price}','{quantity}','{category}')"
            cursor.execute(sql)
            con.commit()
            con.close()   
            refreshTable()
    except Exception as e:
        print(e)
        messagebox.showwarning("","Error while saving")
        return

def update():
    selectedItemId = ''
    try:
        selectedItem = my_tree.selection()[0]
        selectedItemId = str(my_tree.item(selectedItem)['values'][0]) 
        
    except:
        messagebox.showwarning("","please select a data row")
        return
    itemid = str(itemidEntry.get())
    name = str(nameEntry.get())
    price = str(priceEntry.get())
    quantity = str(qntEntry.get())
    category = str(categoryCombo.get())
    if not(itemid and itemid.strip()) or not(name and name.strip()) or not(price and price.strip()) or not(quantity and quantity.strip()) or not(category and category.strip()):
        messagebox.showwarning("","Please fill all the fields")
        return
    if (selectedItemId!=itemid):
        messagebox.showwarning("","you can't change selected item")
        return
    try:
        cursor.connection.ping()
        sql =f"UPDATE stock SET `name`= '{name}',`price`= '{price}',`quantity`= '{quantity}',`category`= '{category}' WHERE `item id` = '{itemid}'"
        cursor.execute(sql)
        con.commit()
        refreshTable() 
    except Exception as err:
        messagebox.showwarning("","Error occured ref"+str(err))
        return


def drop():
    try:
        selectedItem = my_tree.selection()[0]
        decission = messagebox.askquestion("","Do Wou Want To Delete The Selected Data ?")
        if (decission!= 'yes'):
            return
        else:
            selectedItem = my_tree.selection()[0]
            itemid = str(my_tree.item(selectedItem)['values'][0])
            try:
                cursor.connection.ping()
                sql =f"DELETE FROM stock WHERE `item id` = '{itemid}'"
                cursor.execute(sql)
                con.commit()  
                con.close()
                messagebox.showinfo("", "Data Deleted Successfully")
                refreshTable()
            except:
                messagebox.showinfo("","Sorry an error occured..")
    except:
        messagebox.showwarning("","please select a data row")             
                


def select():
    try:
        selectedItem = my_tree.selection()[0]
        itemid = str(my_tree.item(selectedItem)['values'][0])
        name = str(my_tree.item(selectedItem)['values'][1])
        price = str(my_tree.item(selectedItem)['values'][2])
        quantity = str(my_tree.item(selectedItem)['values'][3])
        category = str(my_tree.item(selectedItem)['values'][4])
        savph(itemid,0)
        savph(name,1)
        savph(price,2)
        savph(quantity,3)
        savph(category,4)
    except:
        messagebox.showwarning("","please select a data row")
        return
    
    
def search():
    itemid = str(itemidEntry.get())
    name = str(nameEntry.get())
    price = str(priceEntry.get())
    quantity = str(qntEntry.get())
    category = str(categoryCombo.get())
    cursor.connection.ping()
    if (itemid and itemid.strip):
        sql = f"SELECT `item id`,`name`,`price`,`quantity`,`category` FROM stock WHERE `item id` LIKE '%{itemid}%'" 
    elif (name and name.strip):
        sql = f"SELECT `item id`,`name`,`price`,`quantity`,`category` FROM stock WHERE `name` LIKE '%{name}%'"
    elif (price and price.strip):
        sql = f"SELECT `item id`,`itemid`,`name`,`price`,`quantity`,`category` FROM stock WHERE `price` LIKE '%{price}%'"
    elif (quantity and quantity.strip):
        sql = f"SELECT `item id`,`name`,`price`,`quantity`,`category` FROM stock WHERE `quantity` LIKE '%{quantity}%'"
    elif (category and category.strip):
        sql = f"SELECT `item id`,`name`,`price`,`quantity`,`category` FROM stock WHERE `category` LIKE '%{category}%'"            
    else:
        messagebox.showwarning("","Please Fill Up One Of The Fields")
        return
    cursor.execute(sql)
    try:
        result = cursor.fetchall();
        for num in range(0,5):
            savph(result[0][num],(num))
        con.commit()
        con.close()    
    except:
        messagebox.showwarning("","No Data Found..") 

def clear():
    for num in range(0,5):
        savph("",(num))
        
def exportexcel():
    cursor.connection.ping()
    sql =f"SELECT `item id`, `name`, `price`, `quantity`, `category`, `date` FROM stock ORDER BY 'id' DESC"
    cursor.execute(sql)
    dataraw=cursor.fetchall()
    date = str(datetime.datetime.now())
    date = date.replace(' ','_')
    date = date.replace(':','-')
    datef = date[0:16]
    
    file_path = tkinter.filedialog.asksaveasfilename(defaultextension=".csv", initialfile=f"stock_{datef}.csv",filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if not file_path:
        return  messagebox.showinfo("","User cancelled the save operation")
    
    with open(file_path, 'w', newline='') as f:
        w = csv.writer(f, dialect='excel')
        for r in dataraw:
            w.writerow(r)
    
    print(f"Saved: {file_path}")
    con.commit()
    con.close()
    messagebox.showinfo("", f"Excel file saved: {file_path}")
    

#########################################################################################################################

def gettime(variant):
    if variant == 'hms':
        time = datetime.datetime.now().strftime("%I:%M:%S %p")
    else:
        time = datetime.datetime.now().strftime("%I:%M %p")
    return time

def updateclock():
    realtime.config(text=gettime('hms'))
    realtime.after(1000,updateclock)




#########################################################################################################################
        
frame=tkinter.Frame(win,bg="#31363F")
frame.pack(side=TOP,fill=X)

btncolor = "#42777A"

#########################################################################################################################

editframe =tkinter.LabelFrame(frame,bg="#76ABAE")
editframe.grid(row=1,column=1,sticky="e",padx=[10,10],pady=10,ipadx=2)




saveBtn = Button(editframe,text="SAVE",width=15,bg=btncolor,fg="#BEFCFF",command=save,font=("Arial Bold",10))
updateBtn = Button(editframe,text="UPDATE",width=15,bg=btncolor,fg="#BEFCFF",command=update,font=("Arial Bold",10))
deleteBtn = Button(editframe,text="DELETE",width=15,bg=btncolor,fg="#BEFCFF",command=drop,font=("Arial Bold",10))
selectBtn = Button(editframe,text="SELECT",width=15,bg=btncolor,fg="#BEFCFF",command=select,font=("Arial Bold",10))
findBtn = Button(editframe,text="FIND",width=15,bg=btncolor,fg="#BEFCFF",command=search,font=("Arial Bold",10))
clearBtn = Button(editframe,text="CLEAR",width=15,bg=btncolor,fg= "#BEFCFF",command=clear,font=("Arial Bold",10))
exportBtn = Button(editframe,text="EXPORT EXCEL",width=15,bg=btncolor,fg= "#BEFCFF",command=exportexcel,font=("Arial Bold",10))


saveBtn.grid(row=0,column=0,padx=5,pady=5)
updateBtn.grid(row=1,column=0,padx=5,pady=5)
selectBtn.grid(row=2,column=0,padx=5,pady=5)
deleteBtn.grid(row=3,column=0,padx=5,pady=5)
findBtn.grid(row=4,column=0,padx=5,pady=5)
clearBtn.grid(row=5,column=0,padx=5,pady=5)
exportBtn.grid(row=6,column=0,padx=5,pady=5)

#########################################################################################################################

manageframe =  tkinter.LabelFrame(frame, bg="#76ABAE",fg="#1A2130")
manageframe.grid(row=1, column=2, sticky="e", padx=[10,10],pady=10,ipadx=[2])

inbtn = Button(manageframe,text="login",width=15,bg=btncolor,fg="#BEFCFF",font=("Arial Bold",10))
outbtn = Button(manageframe,text="logout",width=15,bg=btncolor,fg="#BEFCFF",font=("Arial Bold",10))
dldbtn = Button(manageframe,text="Download Excel",width=15,bg=btncolor,fg="#BEFCFF",font=("Arial Bold",10))
clrbtn = Button(manageframe,text="clear",width=15,bg=btncolor,fg="#BEFCFF",font=("Arial Bold",10))

inbtn.grid(row=0,column=0,padx=5,pady=5)
outbtn.grid(row=1,column=0,padx=5,pady=5)
dldbtn.grid(row=2,column=0,padx=5,pady=5)
clrbtn.grid(row=3,column=0,padx=5,pady=5)

#########################################################################################################################

entriesframe =tkinter.LabelFrame(frame,bg="#76ABAE")
entriesframe.grid(row=1,column=0,sticky="NSEW",padx=[10,10],pady=10,ipadx=[6])


itemidlabel=Label(entriesframe,text="Item ID",anchor="e",width=10,bg="#76ABAE",fg="#222831",font=("Arial Bold",15))
namelabel=Label(entriesframe,text="Name",anchor="e",width=10,bg="#76ABAE",fg="#222831",font=("Arial Bold",15))
pricelabel=Label(entriesframe,text="Price",anchor="e",width=10,bg="#76ABAE",fg="#222831",font=("Arial Bold",15))
qntlabel=Label(entriesframe,text="Quantity",anchor="e",width=10,bg="#76ABAE",fg="#222831",font=("Arial Bold",15))
categorylabel=Label(entriesframe,text="Category",anchor="e",width=10,bg="#76ABAE",fg="#222831",font=("Arial Bold",15))

itemidlabel.grid(row=0,column=0,padx=10)
namelabel.grid(row=1,column=0,padx=10)
pricelabel .grid(row=2,column=0,padx=10)
qntlabel.grid(row=3,column=0,padx=10)
categorylabel.grid(row=4,column=0,padx=10)

categorialArray=["value 1", "value 2","value 3","value 4"] 

itemidEntry=Entry(entriesframe,width=50,textvariable=placeholdeArray[0])
nameEntry=Entry(entriesframe,width=50,textvariable=placeholdeArray[1])
priceEntry=Entry(entriesframe,width=50,textvariable=placeholdeArray[2])
qntEntry=Entry(entriesframe,width=50,textvariable=placeholdeArray[3])
categoryCombo=ttk.Combobox(entriesframe,width=47,textvariable=placeholdeArray[4],values=categorialArray)


itemidEntry.grid(row=0,column=2,padx=5,pady=5)
nameEntry.grid(row=1,column=2,padx=5,pady=5)
priceEntry .grid(row=2,column=2,padx=5,pady=5)
qntEntry.grid(row=3,column=2,padx=5,pady=5)
categoryCombo.grid(row=4,column=2,padx=5,pady=5)

#########################################################################################################################

genrateidbtn=Button(entriesframe,text="GENRATE ID",bg=btncolor,fg="#BEFCFF",command=genrateRand,font=("Arial Bold",10))
genrateidbtn.grid(row=0,column=3,padx=5,pady=5)

style.configure(win)

#########################################################################################################################

my_tree['columns']=('ITEM ID','NAME', 'PRICE','QUANTITY','CATEGORY','DATE')

my_tree.column("#0",width=0,stretch=NO)
my_tree.column("ITEM ID",anchor=W,width=70)
my_tree.column("NAME",anchor=W,width=125)
my_tree.column("PRICE",anchor=W,width=125)
my_tree.column("QUANTITY",anchor=W,width=100)
my_tree.column("CATEGORY",anchor=W,width=150)
my_tree.column("DATE",anchor=W,width=150)

my_tree.heading("ITEM ID",text="ITEM ID",anchor=W)
my_tree.heading("NAME",text="NAME",anchor=W)
my_tree.heading("PRICE",text="PRICE",anchor=W)
my_tree.heading("QUANTITY",text="QUANTITY",anchor=W)
my_tree.heading("CATEGORY",text="CATEGORY",anchor=W)
my_tree.heading("DATE",text="DATE",anchor=W)

my_tree.tag_configure('orow',background="#31363F",foreground="#BEFCFF")
my_tree.pack(fill=BOTH,expand=True)

refreshTable()

#########################################################################################################################

manageframe2 =  tkinter.LabelFrame(frame, bg="#76ABAE",fg="#EEEEEE")
manageframe2.grid(row=1, column=3, sticky="e", padx=(10,10),pady=10,ipadx=2,ipady=5)

my_tree_2 = ttk.Frame(manageframe2)
my_tree_2.grid(row=0,column=1,padx=5,pady=5,sticky="e")
my_tree_2_scroll = ttk.Scrollbar(my_tree_2)
my_tree_2_scroll.pack(side="right",fill="y")

cols = ("E-ID","NAME","TIME IN","TIME OUT")
my_tree_2_view = ttk.Treeview(my_tree_2,show="headings",yscrollcommand=my_tree_2_scroll.set,columns=cols,height=13)
my_tree_2_view.heading("E-ID",text="E-ID",anchor=W)
my_tree_2_view.heading("NAME",text="NAME",anchor=W)
my_tree_2_view.heading("TIME IN",text="TIME IN",anchor=W)
my_tree_2_view.heading("TIME OUT",text="TIME OUT",anchor=W)
my_tree_2_view.column("E-ID",width=134)
my_tree_2_view.column("NAME",width=134)
my_tree_2_view.column("TIME IN",width=134)
my_tree_2_view.column("TIME OUT",width=134)

my_tree_2_array = [
    [1,'e-213','mac','8:20 pm','6:00 am'],
    [2,'e-214','macr','8:21 pm','6:01 am'],
    [3,'e-215','macro','8:22 pm','6:02 am'],
    [4,'e-216','macroeco','8:23 pm','6:03 am'],
]

for d in my_tree_2_view.get_children():
    my_tree_2_view.delete(d)

for arr in my_tree_2_array:
    my_tree_2_view.insert('',tkinter.END,values=arr[1:],iid=arr[0])
    print(arr)


my_tree_2_view.pack()
my_tree_2_view.tag_configure('orow',background="#31363F",foreground="#BEFCFF")
my_tree_2_scroll.pack()
my_tree_2_scroll.config(command=my_tree_2_view.yview)



realtime = ttk.Label(text=gettime('hms'),font=('Arial Bold',20))
realtime.pack()
realtime.after(1000,updateclock)

#########################################################################################################################
win.resizable(TRUE,TRUE)
win.mainloop()