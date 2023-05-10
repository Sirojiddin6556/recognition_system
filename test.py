import sqlite3
import tkinter as tk
import tkinter.ttk as ttk


class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER)

        for row in rows:
            table.insert('', tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)


data = ()
with sqlite3.connect('people.db') as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    data = (row for row in cursor.fetchall())

root = tk.Tk()
table = Table(root, headings=('Фамилия', 'Имя', 'Отчество'), rows=data)
table.pack(expand=tk.YES, fill=tk.BOTH)
root.mainloop()




# check the password for change the password
# def save_pass():
#     assure_path_exists("trainingImageLabel/")
#     exists1 = os.path.isfile("rainingImageLabel\pass.txt")
#     if exists1:
#         tf = open("TrainingImageLabel\pass.txt", "r")
#         str = tf.read()
#     else:
#         master.destroy()
#         new_pas = tsd.askstring('Password not set', 'Please enter a new password below', show='*')
#         if new_pas == None:
#             mess.showinfo(title='Null Password Entered', message='Password not set.Please try again!')
#         else:
#             tf = open("TrainingImageLabel\pass.txt", "w")
#             tf.write(new_pas)
#             mess.showinfo(title='Password Registered!', message='New password was registered successfully!')
#             return
#     op = (old.get())
#     newp = (new.get())
#     nnewp = (nnew.get())
#     if (op == str):
#         if (newp == nnewp):
#             txf = open("TrainingImageLabel\pass.txt", "w")
#             txf.write(newp)
#         else:
#             mess.showerror(title='Error', message='Confirm new password again!!!')
#             return
#     else:
#         mess.showwarning(title='Wrong Password', message='Please enter correct old password.')
#         return
#     mess.showwarning(title='Password Changed', message='Password changed successfully!!')
#     master.destroy()


# change password
# def change_pass():
#     global master
#     master = tkinter.Tk()
#     master.geometry("400x160")
#     master.resizable(False, False)
#     master.title("Change Admin Password")
#     master.configure(background="white")
#     lbl4 = tkinter.Label(master, text='    Enter Old Password', bg='white', font=('times', 12, ' bold '))
#     lbl4.place(x=10, y=10)
#     global old
#     old = tkinter.Entry(master, width=25, fg="black", relief='solid', font=('times', 12, ' bold '), show='*')
#     old.place(x=180, y=10)
#     lbl5 = tkinter.Label(master, text='   Enter New Password', bg='white', font=('times', 12, ' bold '))
#     lbl5.place(x=10, y=45)
#     global new
#     new = tkinter.Entry(master, width=25, fg="black", relief='solid', font=('times', 12, ' bold '), show='*')
#     new.place(x=180, y=45)
#     lbl6 = tkinter.Label(master, text='Confirm New Password', bg='white', font=('times', 12, ' bold '))
#     lbl6.place(x=10, y=80)
#     global nnew
#     nnew = tkinter.Entry(master, width=25, fg="black", relief='solid', font=('times', 12, ' bold '), show='*')
#     nnew.place(x=180, y=80)
#     cancel = tkinter.Button(master, text="Cancel", command=master.destroy, fg="white", bg="#13059c", height=1, width=25,
#                             activebackground="white", font=('times', 10, ' bold '))
#     cancel.place(x=200, y=120)
#     save1 = tkinter.Button(master, text="Save", command=save_pass, fg="black", bg="#00aeff", height=1, width=25,
#                            activebackground="white", font=('times', 10, ' bold '))
#     save1.place(x=10, y=120)
#     master.mainloop()


# ask for password
# def psw():
#     assure_path_exists("TrainingImageLabel/")
#     exists1 = os.path.isfile("TrainingImageLabel\pass.txt")
#     if exists1:
#         tf = open("TrainingImageLabel\pass.txt", "r")
#         str_pass = tf.read()
#     else:
#         new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
#         if new_pas == None:
#             mess.showwarning(title='No Password Entered', message='Password not set!! Please try again')
#         else:
#             tf = open("TrainingImageLabel\pass.txt", "w")
#             tf.write(new_pas)
#             mess.showinfo(title='Password Registered', message='New password was registered successfully!!')
#             return
#     password = tsd.askstring('Password', 'Enter Password', show='*')
#     if (password == str_pass):
#         Reg().save_to_db
#
#     elif (password == None):
#         pass
#     else:
#         mess.showinfo(title='Wrong Password', message='You have entered wrong password')
