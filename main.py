
import tkinter as tk
from tkinter import Frame, ttk
import sqlite3
from tkinter import messagebox as mess
import cv2
import os
import numpy as np
from PIL import Image
import datetime, time


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Face detector")
        self.geometry('700x500')
        self.resizable = (False, False)
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (Main, Reg, Aut,):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Main)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Main(Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.lable = tk.Label(self, text="Добро Пожаловать", font=("Arial", 16))
        self.reg = tk.Button(self, text="Регистрация", command=lambda: controller.show_frame(Reg))
        self.auth = tk.Button(self, text="Авторизация", command=lambda: controller.show_frame(Aut))
        self.exit = tk.Button(self, text="Выход", command=exit)
        self.lable.pack(side="top", ipadx=150, ipady=5)
        self.reg.pack(ipadx=150, ipady=5, pady=15, anchor=tk.CENTER)
        self.auth.pack(ipadx=150, ipady=5, anchor=tk.CENTER)
        self.exit.pack(side="bottom", pady=10, ipadx=50, ipady=5)

    def exit(self):
        App.destroy(self)



class Reg(Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.welcome = tk.Label(self, text="Окно регистрации")
        self.id = tk.Label(self, text="Введите ID")
        self.name = tk.Label(self, text="Введите имя")
        self.save_btn = tk.Button(self, text="Сохранить данные", command=self.save_to_db)
        self.fics_btn = tk.Button(self, text="Фиксировать", command=self.takeimages)
        self.back = tk.Button(self, text="Назад", command=lambda: controller.show_frame(Main))
        self.entID = tk.Entry(self)
        self.entNAme = tk.Entry(self)

        self.welcome.pack(side="top", pady=5, padx=1, ipadx=5, ipady=5)
        self.id.pack(pady=1, padx=1, ipadx=5, ipady=5)
        self.entID.pack(pady=1, padx=1, ipadx=5, ipady=5)
        self.name.pack(pady=1, padx=1, ipadx=5, ipady=5)
        self.entNAme.pack(pady=1, padx=1, ipadx=5, ipady=5)
        self.back.pack(side="bottom", pady=10, padx=30, ipadx=50, ipady=2)
        self.fics_btn.pack(side="bottom", pady=10, padx=5, ipadx=80, ipady=1)
        self.save_btn.pack(side="bottom", pady=10, padx=5, ipadx=61, ipady=1)


    def save_to_db(self):
        user_id = self.entID.get()
        user_name = self.entNAme.get()
        if not user_id or not user_name:
            mess.showerror("Ошибка", "Пожалуйста, заполните все поля.")
            return
        connection = sqlite3.connect('people.db')
        crsr = connection.cursor()
        crsr.execute("""INSERT INTO registration (Numb, name, datetime) values(?, ?, datetime('now'))""",
                     (user_id, user_name))
        connection.commit()
        mess.showinfo("Успешно", "Данные успешно сохранены.")
        connection.close()


    def takeimages(self):
        assure_path_exists("images/")
        user_id = self.entID.get()
        user_name = self.entNAme.get()
        if user_name == "" or user_id == "":
            mess.showwarning("Предупреждение", "Пожалуйста, заполните данные!")
        else:
            # Подключение к базе данных SQLite3
            conn = sqlite3.connect('people.db')
            c = conn.cursor()

            # Проверка, что таблица users не пуста
            c.execute("SELECT COUNT(*) FROM registration ")
            count = c.fetchone()[0]
            if count == 0:
                mess.showwarning("Предупреждение", "Таблица пользователей пуста!")
            else:
                c.execute("SELECT COUNT(*) FROM registration WHERE NOT Name GLOB '[A-Za-z]*'")
                count = c.fetchone()[0]
                serial = (count // 2) + 1

                # Проверка, что имя студента состоит только из букв и пробелов
                if count == 0:
                    cam = cv2.VideoCapture(0)
                    harcascadePath = "haarcascade_frontalface_default.xml"
                    detector = cv2.CascadeClassifier(harcascadePath)
                    sampleNum = 0
                    while (True):
                        ret, img = cam.read()
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        faces = detector.detectMultiScale(gray, 1.05, 5)
                        for (x, y, w, h) in faces:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            # увеличение счетчика номера образца
                            sampleNum = sampleNum + 1
                            # сохранение захваченного изображения лица в папке dataset/TrainingImage
                            cv2.imwrite("images/ " + user_name + "." + user_id + '.' + str(
                                sampleNum) + ".jpg",
                                        gray[y:y + h, x:x + w])
                            # отображение изображения
                            cv2.imshow('Taking Images', img)
                        # ожидание 100 миллисекунд
                        if cv2.waitKey(100) & 0xFF == ord('q'):
                            break
                        # прерывание цикла, если количество образцов больше 100
                        elif sampleNum > 100:
                            break
                    cam.release()
                    cv2.destroyAllWindows()
                self.entID.delete



class Aut(Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.headings = ('ID', 'Номер', 'Имя', 'Время')
        self.lable = tk.Label(self, text="Окно авторизации")
        self.exp = tk.Button(self, text="Проверка", command=self.track_images)
        self.upda = tk.Button(self, text="Обновить", command=self.update_table)
        self.back = tk.Button(self, text="Назад", command=lambda: controller.show_frame(Main))
        with sqlite3.connect('people.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM authorization")
            data = (row for row in cursor.fetchall())
        self.row = data
        self.tb = ttk.Treeview(self, show="headings", selectmode="browse")
        self.tb["columns"] = self.headings
        self.tb.column("0", width=100)
        self.tb.column("1", width=100)
        self.tb.column("2", width=100)
        self.tb.column("3", width=150)
        self.tb["displaycolumns"] = self.headings

        for head in self.headings:
            self.tb.heading(head, text=head, anchor=tk.CENTER)
            self.tb.column(head, anchor=tk.CENTER)

        for row in self.row:
            self.tb.insert('', tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.tb.yview)
        self.tb.configure(yscrollcommand=scrolltable.set)
        self.tb.pack(expand=True, side=tk.LEFT, fill=tk.Y)
        scrolltable.pack(side=tk.LEFT, fill=tk.Y)

        self.lable.pack(side="top")
        self.exp.pack(side="top")
        self.upda.pack(side="top")  # добавляем кнопку обновления в интерфейс
        self.back.pack(side="bottom")

    def update_table(self):
        with sqlite3.connect('people.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM authorization")
            data = (row for row in cursor.fetchall())
        self.row = data
        for item in self.tb.get_children():
            self.tb.delete(item)
        for row in self.row:
            self.tb.insert('', tk.END, values=tuple(row))



    def track_images(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        exists3 = os.path.isfile("Traing/Trainner.yml")
        if exists3:
            recognizer.read("Traing/Trainner.yml")
        else:
            mess.showinfo(title='Data Missing', message='Please click on Save Profile to reset data!!')
            return

        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)

        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        person_recognized = False  # флаг, чтобы понять, кто-то был распознан

        # Connect to the SQLite database
        conn = sqlite3.connect('people.db')
        cursor = conn.cursor()
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute("SELECT COUNT(*) FROM registration")
        except sqlite3.OperationalError:
            mess.showinfo(title='Details Missing', message='Details are missing, please check!')
            cam.release()
            cv2.destroyAllWindows()
            return

        while not person_recognized:  # продолжать работать, пока кто-то не будет распознан
            ret, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)

            for i, (x, y, w, h) in enumerate(faces):
                cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
                iD, conf = recognizer.predict(gray[y:y + h, x:x + w])

                if conf < 50:
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    cursor.execute("SELECT ID, NAME FROM registration WHERE ID = ?", (iD,))
                    result = cursor.fetchone()
                    if result:
                        # user exists, update attendance
                        ID = result[0]
                        bb = result[1]
                        cursor.execute("UPDATE registration SET datetime = ? WHERE ID = ?", (timeStamp, ID))
                        cursor.execute("INSERT INTO authorization (NUMB, NAME, datetime) VALUES (?, ?, ?)",
                                       (iD, bb, timeStamp))
                    else:
                        # user not found, insert new attendance record
                        bb = 'Unknown'

                else:
                    bb = 'Unknown'

                cv2.putText(im, bb, (x, y + h), font, 1, (0, 251, 255), 2)

            cv2.imshow('Taking Attendance', im)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            # если кто-то был распознан, установите флаг и выйдите из цикла
            if 'bb' in locals() and bb != 'Unknown':
                person_recognized = True

        conn.commit()
        conn.close()
        cam.release()
        cv2.destroyAllWindows()


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


# check for haarcascade file
def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess.showinfo(title='fechar file missing', message='some file is missing.Please contact me for help')



def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empty face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])

        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

def trainimage():
    check_haarcascadefile()
    assure_path_exists("Traing/Trainner.yml")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("images")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess.showinfo(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("Traing/Trainner.yml")
    res = "Profile Saved Successfully"




if __name__ == '__main__':
    app = App()
    app.mainloop()