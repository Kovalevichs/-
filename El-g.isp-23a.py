import tkinter as tk
from tkinter import messagebox
import hashlib
import sqlite3

class DiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Электронный дневник")

        # Цветовая палитра (сине-белая)
        self.bg_color = "#E0F2F7"  # Светло-синий фон
        self.fg_color = "#003366"  # Темно-синий текст
        self.button_bg = "#AED6F1"  # Синий фон для кнопок
        self.button_fg = "#003366"  # Темно-синий текст для кнопок

        self.root.configure(bg=self.bg_color)

        self.conn = sqlite3.connect('diary.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                name TEXT,
                surname TEXT,
                class TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                subject TEXT NOT NULL,
                grade INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        self.conn.commit()

        self.current_user_id = None
        self.current_user_role = None

        self.create_login_page()

    def create_login_page(self):
        self.clear_window()

        self.login_label = tk.Label(self.root, text="Авторизация", bg=self.bg_color, fg=self.fg_color)
        self.login_label.pack(pady=10)

        self.username_label = tk.Label(self.root, text="Имя пользователя:", bg=self.bg_color, fg=self.fg_color)
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Пароль:", bg=self.bg_color, fg=self.fg_color)
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, width=30, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.root, text="Войти", command=self.login, bg=self.button_bg, fg=self.button_fg)
        self.login_button.pack(pady=5)

        self.register_button = tk.Button(self.root, text="Регистрация", command=self.create_registration_page, bg=self.button_bg, fg=self.button_fg)
        self.register_button.pack(pady=5)

    def create_registration_page(self):
        self.clear_window()

        self.register_label = tk.Label(self.root, text="Регистрация", bg=self.bg_color, fg=self.fg_color)
        self.register_label.pack(pady=10)

        self.username_label = tk.Label(self.root, text="Имя пользователя:", bg=self.bg_color, fg=self.fg_color)
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Пароль:", bg=self.bg_color, fg=self.fg_color)
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, width=30, show="*")
        self.password_entry.pack()

        self.role_label = tk.Label(self.root, text="Роль:", bg=self.bg_color, fg=self.fg_color)
        self.role_label.pack()
        self.role_var = tk.StringVar(value="Ученик")
        self.role_student_radio = tk.Radiobutton(self.root, text="Ученик", variable=self.role_var, value="Ученик", bg=self.bg_color, fg=self.fg_color)
        self.role_teacher_radio = tk.Radiobutton(self.root, text="Учитель", variable=self.role_var, value="Учитель", bg=self.bg_color, fg=self.fg_color)
        self.role_student_radio.pack()
        self.role_teacher_radio.pack()

        self.name_label = tk.Label(self.root, text="Имя:", bg=self.bg_color, fg=self.fg_color)
        self.name_label.pack()
        self.name_entry = tk.Entry(self.root, width=30)
        self.name_entry.pack()

        self.surname_label = tk.Label(self.root, text="Фамилия:", bg=self.bg_color, fg=self.fg_color)
        self.surname_label.pack()
        self.surname_entry = tk.Entry(self.root, width=30)
        self.surname_entry.pack()

        self.class_label = tk.Label(self.root, text="Класс:", bg=self.bg_color, fg=self.fg_color)
        self.class_label.pack()
        self.class_entry = tk.Entry(self.root, width=30)
        self.class_entry.pack()

        self.register_button = tk.Button(self.root, text="Зарегистрироваться", command=self.register, bg=self.button_bg, fg=self.button_fg)
        self.register_button.pack(pady=5)

        self.back_button = tk.Button(self.root, text="Назад", command=self.create_login_page, bg=self.button_bg, fg=self.button_fg)
        self.back_button.pack(pady=5)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        klass = self.class_entry.get()

        if not username or not password or not name or not surname or not klass:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            self.cursor.execute("INSERT INTO users (username, password, role, name, surname, class) VALUES (?, ?, ?, ?, ?, ?)",
                                (username, hashed_password, role, name, surname, klass))
            self.conn.commit()
            messagebox.showinfo("Успех", "Регистрация прошла успешно!")
            self.create_login_page()
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Имя пользователя уже существует.")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        self.cursor.execute("SELECT id, role FROM users WHERE username=? AND password=?", (username, hashed_password))
        result = self.cursor.fetchone()

        if result:
            self.current_user_id = result[0]
            self.current_user_role = result[1]
            messagebox.showinfo("Успех", "Авторизация прошла успешно!")
            if self.current_user_role == "Ученик":
                self.show_student_grades()
            else:
                self.create_teacher_page()
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль.")

    def create_teacher_page(self):
        self.clear_window()

        self.label_name = tk.Label(self.root, text="Имя:", bg=self.bg_color, fg=self.fg_color)
        self.label_name.pack()
        self.entry_name = tk.Entry(self.root, width=30)
        self.entry_name.pack()

        self.label_surname = tk.Label(self.root, text="Фамилия:", bg=self.bg_color, fg=self.fg_color)
        self.label_surname.pack()
        self.entry_surname = tk.Entry(self.root, width=30)
        self.entry_surname.pack()

        self.label_class = tk.Label(self.root, text="Класс:", bg=self.bg_color, fg=self.fg_color)
        self.label_class.pack()
        self.entry_class = tk.Entry(self.root, width=30)
        self.entry_class.pack()

        self.listbox = tk.Listbox(self.root, width=50, height=15, bg=self.bg_color)
        self.listbox.pack(pady=10)

        self.entry_subject = tk.Entry(self.root, width=30)
        self.entry_subject.pack(pady=5)
        self.entry_subject.insert(0, "Название предмета")
        self.entry_subject.bind("<FocusIn>", self.clear_subject_name)

        self.entry_grade = tk.Entry(self.root, width=30)
        self.entry_grade.pack(pady=5)
        self.entry_grade.insert(0, "Оценка")
        self.entry_grade.bind("<FocusIn>", self.clear_grade)

        self.button_add = tk.Button(self.root, text="Добавить", command=self.add_subject, bg=self.button_bg, fg=self.button_fg)
        self.button_add.pack(pady=5)

        self.button_delete = tk.Button(self.root, text="Удалить", command=self.delete_subject, bg=self.button_bg, fg=self.button_fg)
        self.button_delete.pack(pady=5)

        self.button_show_info = tk.Button(self.root, text="Показать информацию", command=self.show_info, bg=self.button_bg, fg=self.button_fg)
        self.button_show_info.pack(pady=5)

        #Поле поиска
        self.search_label = tk.Label(self.root, text="Поиск предмета:", bg=self.bg_color, fg=self.fg_color)
        self.search_label.pack()
        self.search_entry = tk.Entry(self.root, width=30)
        self.search_entry.pack()
        self.search_button = tk.Button(self.root, text="Поиск", command=self.search_subject, bg=self.button_bg, fg=self.button_fg)
        self.search_button.pack(pady=5)

        self.logout_button = tk.Button(self.root, text="Выйти", command=self.logout, bg=self.button_bg, fg=self.button_fg)
        self.logout_button.pack(pady=5)

        self.subjects = {}  # Словарь для хранения предметов и оценок

        # Кнопки для управления учениками
        self.button_view_students = tk.Button(self.root, text="Просмотр всех учеников", command=self.show_all_students,
                                              bg=self.button_bg, fg=self.button_fg)
        self.button_view_students.pack(pady=5)

        self.button_filter_students = tk.Button(self.root, text="Фильтрация учеников по классу",
                                                command=self.create_filter_students_page, bg=self.button_bg,
                                                fg=self.button_fg)
        self.button_filter_students.pack(pady=5)

        self.logout_button = tk.Button(self.root, text="Выйти", command=self.logout, bg=self.button_bg,
                                       fg=self.button_fg)
        self.logout_button.pack(pady=5)

    def create_filter_students_page(self):
        self.clear_window()

        self.filter_label = tk.Label(self.root, text="Введите класс для фильтрации:", bg=self.bg_color,
                                     fg=self.fg_color)
        self.filter_label.pack(pady=10)

        self.filter_entry = tk.Entry(self.root, width=30)
        self.filter_entry.pack()

        self.filter_button = tk.Button(self.root, text="Фильтровать", command=self.show_filtered_students,
                                       bg=self.button_bg, fg=self.button_fg)
        self.filter_button.pack(pady=5)

        self.back_button = tk.Button(self.root, text="Назад", command=self.create_teacher_page, bg=self.button_bg,
                                     fg=self.button_fg)
        self.back_button.pack(pady=5)

    def show_all_students(self):
        self.clear_window()

        self.students_listbox = tk.Listbox(self.root, width=50, height=15, bg=self.bg_color)
        self.students_listbox.pack(pady=10)

        self.cursor.execute("SELECT name, surname, class FROM users WHERE role=?", ("Ученик",))
        students = self.cursor.fetchall()

        for name, surname, klass in students:
            self.students_listbox.insert(tk.END, f"{name} {surname}, Класс: {klass}")

        self.back_button = tk.Button(self.root, text="Назад", command=self.create_teacher_page, bg=self.button_bg,
                                     fg=self.button_fg)
        self.back_button.pack(pady=5)

    def show_filtered_students(self):
        filter_class = self.filter_entry.get()
        self.clear_window()

        self.students_listbox = tk.Listbox(self.root, width=50, height=15, bg=self.bg_color)
        self.students_listbox.pack(pady=10)

        self.cursor.execute("SELECT name, surname, class FROM users WHERE role=? AND class=?", ("Ученик", filter_class))
        students = self.cursor.fetchall()

        if students:
            for name, surname, klass in students:
                self.students_listbox.insert(tk.END, f"{name} {surname}, Класс: {klass}")
        else:
            messagebox.showinfo("Информация", "Ученики данного класса не найдены.")

        self.back_button = tk.Button(self.root, text="Назад", command=self.create_teacher_page, bg=self.button_bg,
                                     fg=self.button_fg)
        self.back_button.pack(pady=5)


        

    def show_student_grades(self):
        self.clear_window()

        self.cursor.execute("SELECT name, surname, class FROM users WHERE id=?", (self.current_user_id,))
        user_data = self.cursor.fetchone()
        name, surname, klass = user_data

        self.info_label = tk.Label(self.root, text=f"Оценки ученика: {name} {surname}, Класс: {klass}", bg=self.bg_color, fg=self.fg_color)
        self.info_label.pack(pady=10)

        self.grades_listbox = tk.Listbox(self.root, width=50, height=15,  bg=self.bg_color)
        self.grades_listbox.pack(pady=10)

        #Поле поиска
        self.search_label = tk.Label(self.root, text="Поиск предмета:", bg=self.bg_color, fg=self.fg_color)
        self.search_label.pack()
        self.search_entry = tk.Entry(self.root, width=30)
        self.search_entry.pack()
        self.search_button = tk.Button(self.root, text="Поиск", command=self.search_student_subject, bg=self.button_bg, fg=self.button_fg)
        self.search_button.pack(pady=5)

        self.cursor.execute("SELECT subject, grade FROM grades WHERE user_id=?", (self.current_user_id,))
        grades = self.cursor.fetchall()

        for subject, grade in grades:
            self.grades_listbox.insert(tk.END, f"{subject}: {grade}")

        self.logout_button = tk.Button(self.root, text="Выйти", command=self.logout, bg=self.button_bg, fg=self.button_fg)
        self.logout_button.pack(pady=5)

    def clear_subject_name(self, event):
        if self.entry_subject.get() == "Название предмета":
            self.entry_subject.delete(0, tk.END)

    def clear_grade(self, event):
        if self.entry_grade.get() == "Оценка":
            self.entry_grade.delete(0, tk.END)

    def add_subject(self):
        subject_name = self.entry_subject.get()
        try:
            subject_grade = int(self.entry_grade.get())
            if subject_name and subject_grade >= 0:
                name = self.entry_name.get()
                surname = self.entry_surname.get()
                klass = self.entry_class.get()
                self.cursor.execute("SELECT id FROM users WHERE name=? AND surname=? AND class=?", (name, surname, klass))
                result = self.cursor.fetchone()
                if result:
                   user_id = result[0]
                   self.cursor.execute("INSERT INTO grades (user_id, subject, grade) VALUES (?, ?, ?)", (user_id, subject_name, subject_grade))
                   self.conn.commit()
                   self.update_listbox()
                   self.entry_subject.delete(0, tk.END)
                   self.entry_grade.delete(0, tk.END)
                else:
                    messagebox.showerror("Ошибка", "Пользователь не найден.")
            else:
                messagebox.showerror("Ошибка", "Пожалуйста, введите корректные данные.")
        except ValueError:
            messagebox.showerror("Ошибка", "Оценка должна быть числом.")

    def delete_subject(self):
        selected_subject = self.listbox.curselection()
        if selected_subject:
            subject_name = self.listbox.get(selected_subject)
            name = self.entry_name.get()
            surname = self.entry_surname.get()
            klass = self.entry_class.get()
            self.cursor.execute("SELECT id FROM users WHERE name=? AND surname=? AND class=?", (name, surname, klass))
            result = self.cursor.fetchone()
            if result:
               user_id = result[0]
               self.cursor.execute("DELETE FROM grades WHERE user_id=? AND subject=?", (user_id, subject_name))
               self.conn.commit()
               self.update_listbox()
            else:
                messagebox.showerror("Ошибка", "Пользователь не найден.")

        else:
            messagebox.showwarning("Предупреждение", "Выберите предмет для удаления.")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        name = self.entry_name.get()
        surname = self.entry_surname.get()
        klass = self.entry_class.get()
        self.cursor.execute("SELECT id FROM users WHERE name=? AND surname=? AND class=?", (name, surname, klass))
        result = self.cursor.fetchone()
        if result:
           user_id = result[0]
           self.cursor.execute("SELECT subject, grade FROM grades WHERE user_id=?", (user_id,))
           grades = self.cursor.fetchall()
           for subject, grade in grades:
              self.listbox.insert(tk.END, f"{subject}: {grade}")
        else:
           messagebox.showerror("Ошибка", "Пользователь не найден.")

    def show_info(self):
        name = self.entry_name.get()
        surname = self.entry_surname.get()
        klass = self.entry_class.get()
        messagebox.showinfo("Информация об ученике", f"Имя: {name}\nФамилия: {surname}\nКласс: {klass}")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def logout(self):
        self.current_user_id = None
        self.current_user_role = None
        self.create_login_page()

    def search_subject(self):
        search_term = self.search_entry.get().lower()
        self.listbox.delete(0, tk.END)
        name = self.entry_name.get()
        surname = self.entry_surname.get()
        klass = self.entry_class.get()
        self.cursor.execute("SELECT id FROM users WHERE name=? AND surname=? AND class=?", (name, surname, klass))
        result = self.cursor.fetchone()
        if result:
           user_id = result[0]
           self.cursor.execute("SELECT subject, grade FROM grades WHERE user_id=?", (user_id,))
           grades = self.cursor.fetchall()
           for subject, grade in grades:
               if search_term in subject.lower():
                  self.listbox.insert(tk.END, f"{subject}: {grade}")
        else:
           messagebox.showerror("Ошибка", "Пользователь не найден.")

    def search_student_subject(self):
        search_term = self.search_entry.get().lower()
        self.grades_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT subject, grade FROM grades WHERE user_id=?", (self.current_user_id,))
        grades = self.cursor.fetchall()

        for subject, grade in grades:
            if search_term in subject.lower():
                self.grades_listbox.insert(tk.END, f"{subject}: {grade}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DiaryApp(root)
    root.mainloop()
