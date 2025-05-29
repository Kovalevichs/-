import tkinter as tk
from tkinter import messagebox, simpledialog

class DiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Электронный дневник")

        self.subjects = {}  # Словарь для хранения предметов и оценок

        self.label = tk.Label(root, text="Электронный дневник", font=("Arial", 16))
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(root, width=50, height=15)
        self.listbox.pack(pady=10)

        self.entry_subject = tk.Entry(root, width=30)
        self.entry_subject.pack(pady=5)
        self.entry_subject.insert(0, "Название предмета")

        self.entry_grade = tk.Entry(root, width=30)
        self.entry_grade.pack(pady=5)
        self.entry_grade.insert(0, "Оценка")

        self.button_add = tk.Button(root, text="Добавить", command=self.add_subject)
        self.button_add.pack(pady=5)

        self.button_delete = tk.Button(root, text="Удалить", command=self.delete_subject)
        self.button_delete.pack(pady=5)

    def add_subject(self):
        subject_name = self.entry_subject.get()
        try:
            subject_grade = int(self.entry_grade.get())
            if subject_name and subject_grade >= 0:
                self.subjects[subject_name] = subject_grade
                self.update_listbox()
                self.entry_subject.delete(0, tk.END)
                self.entry_grade.delete(0, tk.END)
            else:
                messagebox.showerror("Ошибка", "Пожалуйста, введите корректные данные.")
        except ValueError:
            messagebox.showerror("Ошибка", "Оценка должна быть числом.")

    def delete_subject(self):
        selected_subject = self.listbox.curselection()
        if selected_subject:
            subject_name = self.listbox.get(selected_subject)
            del self.subjects[subject_name]
            self.update_listbox()
        else:
            messagebox.showwarning("Предупреждение", "Выберите предмет для удаления.")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for subject, grade in self.subjects.items():
            self.listbox.insert(tk.END, f"{subject}: {grade}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DiaryApp(root)
    root.mainloop()

