import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os


class SchoolJournalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Электронный журнал")
        self.journal_file = "journal.json"
        self.journal = self.load_journal()

        # добавление новых кнопок
        self.edit_button = tk.Button(root, text="Редактировать оценку", command=self.edit_grade)
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Удалить оценку", command=self.delete_grade)
        self.delete_button.pack(pady=5)

        # UI элементы
        self.label = tk.Label(root, text="Электронный журнал", font=("Arial", 16))
        self.label.pack(pady=10)

        self.name_button = tk.Button(root, text="Добавить ученика", command=self.add_student)
        self.name_button.pack(pady=5)

        self.grade_button = tk.Button(root, text="Добавить оценку", command=self.add_grade)
        self.grade_button.pack(pady=5)

        self.view_button = tk.Button(root, text="Посмотреть оценки", command=self.view_grades)
        self.view_button.pack(pady=5)

        self.avg_button = tk.Button(root, text="Средняя оценка", command=self.average_grade)
        self.avg_button.pack(pady=5)

        self.quit_button = tk.Button(root, text="Выход", command=self.on_quit)
        self.quit_button.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)  # Обработка закрытия окна

    # метод редактировать
    def edit_grade(self):
        name = simpledialog.askstring("Редактирование", "Введите имя ученика:")
        if name not in self.journal:
            messagebox.showerror("Ошибка", "Ученик не найден.")
            return
        subject = simpledialog.askstring("Редактирование", "Введите предмет:")
        if subject not in self.journal[name]:
            messagebox.showerror("Ошибка", "Предмет не найден.")
            return
        grades = self.journal[name][subject]
        if not grades:
            messagebox.showinfo("Редактирование", "Нет оценок для редактирования.")
            return

        grade_index = simpledialog.askinteger("Редактирование", f"Введите номер оценки (1 - {len(grades)}):")
        if not grade_index or not (1 <= grade_index <= len(grades)):
            messagebox.showerror("Ошибка", "Неверный номер.")
            return

        new_grade = simpledialog.askinteger("Редактирование", "Введите новую оценку (1-5):")
        if not new_grade or not (1 <= new_grade <= 5):
            messagebox.showerror("Ошибка", "Неверная оценка.")
            return

        grades[grade_index - 1] = new_grade
        messagebox.showinfo("Редактирование", "Оценка обновлена.")

    # метод удалить
    def delete_grade(self):
        name = simpledialog.askstring("Удаление", "Введите имя ученика:")
        if name not in self.journal:
            messagebox.showerror("Ошибка", "Ученик не найден.")
            return
        subject = simpledialog.askstring("Удаление", "Введите предмет:")
        if subject not in self.journal[name]:
            messagebox.showerror("Ошибка", "Предмет не найден.")
            return
        grades = self.journal[name][subject]
        if not grades:
            messagebox.showinfo("Удаление", "Нет оценок для удаления.")
            return

        grade_index = simpledialog.askinteger("Удаление", f"Введите номер оценки для удаления (1 - {len(grades)}):")
        if not grade_index or not (1 <= grade_index <= len(grades)):
            messagebox.showerror("Ошибка", "Неверный номер.")
            return

        removed = grades.pop(grade_index - 1)
        messagebox.showinfo("Удаление", f"Оценка {removed} удалена.")

    def load_journal(self):
        if os.path.exists(self.journal_file):
            try:
                with open(self.journal_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить данные: {e}")
        return {}

    def save_journal(self):
        try:
            with open(self.journal_file, "w", encoding="utf-8") as f:
                json.dump(self.journal, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные: {e}")

    def on_quit(self):
        self.save_journal()
        self.root.destroy()

    def add_student(self):
        name = simpledialog.askstring("Добавить ученика", "Введите имя ученика:")
        if name:
            if name not in self.journal:
                self.journal[name] = {}
                messagebox.showinfo("Успех", f"Ученик '{name}' добавлен.")
            else:
                messagebox.showwarning("Внимание", f"Ученик '{name}' уже существует.")

    def add_grade(self):
        name = simpledialog.askstring("Оценка", "Введите имя ученика:")
        if name not in self.journal:
            messagebox.showerror("Ошибка", "Ученик не найден.")
            return
        subject = simpledialog.askstring("Оценка", "Введите предмет:")
        grade_str = simpledialog.askstring("Оценка", "Введите оценку (1-5):")
        try:
            grade = int(grade_str)
            if 1 <= grade <= 5:
                if subject not in self.journal[name]:
                    self.journal[name][subject] = []
                self.journal[name][subject].append(grade)
                messagebox.showinfo("Успех", f"Оценка добавлена для '{name}' по '{subject}'.")
            else:
                messagebox.showerror("Ошибка", "Оценка должна быть от 1 до 5.")
        except (ValueError, TypeError):
            messagebox.showerror("Ошибка", "Введите корректное число.")

    def view_grades(self):
        name = simpledialog.askstring("Просмотр", "Введите имя ученика:")
        if name not in self.journal:
            messagebox.showerror("Ошибка", "Ученик не найден.")
            return
        result = f"Оценки ученика '{name}':\n"
        for subject, grades in self.journal[name].items():
            result += f"{subject}: {grades}\n"
        messagebox.showinfo("Оценки", result)

    def average_grade(self):
        name = simpledialog.askstring("Средняя оценка", "Введите имя ученика:")
        if name not in self.journal:
            messagebox.showerror("Ошибка", "Ученик не найден.")
            return
        total, count = 0, 0
        for grades in self.journal[name].values():
            total += sum(grades)
            count += len(grades)
        if count == 0:
            messagebox.showinfo("Средняя оценка", "Нет оценок.")
        else:
            avg = total / count
            messagebox.showinfo("Средняя оценка", f"Средняя оценка ученика '{name}': {avg:.2f}")

if name == "__main__":
    root = tk.Tk()
    app = SchoolJournalGUI(root)
    root.mainloop()

