import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class DiaryApp:
    def __init__(self, root):
        self.root = root

    root.title("Электронный дневник")

    self.notes = {}  # словарь для хранения заметок
    self.current_note = None  # для отслеживания текущей выбранной заметки

    # Создание виджетов
    self.note_label = ttk.Label(root, text="Запись:")
    self.note_text = tk.Text(root, height=10, width=50)
    self.rating_label = ttk.Label(root, text="Оценка (1-5):")
    self.rating_scale = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL)
    self.add_button = ttk.Button(root, text="Добавить запись", command=self.add_note)
    self.view_button = ttk.Button(root, text="Просмотреть записи", command=self.view_notes)
    self.edit_button = ttk.Button(root, text="Редактировать запись", command=self.edit_note, state=tk.DISABLED)
    self.delete_button = ttk.Button(root, text="Удалить запись", command=self.delete_note, state=tk.DISABLED)

    # Размещение виджетов в окне
    self.note_label.grid(row=0, column=0, sticky=tk.W)
    self.note_text.grid(row=1, column=0, columnspan=2)
    self.rating_label.grid(row=2, column=0, sticky=tk.W)
    self.rating_scale.grid(row=3, column=0, columnspan=2)
    self.add_button.grid(row=4, column=0)
    self.view_button.grid(row=4, column=1)
    self.edit_button.grid(row=5, column=0)
    self.delete_button.grid(row=5, column=1)

    def add_note(self):
        note = self.note_text.get("1.0", tk.END).strip()

    rating = self.rating_scale.get()
    if note:
        self.notes[note] = rating
    messagebox.showinfo("Сохранено", "Запись добавлена!")
    self.note_text.delete("1.0", tk.END)
    self.rating_scale.set(1)
    self.enable_edit_delete_buttons(False)
    else:
    messagebox.showerror("Ошибка", "Запись не может быть пустой!")

    def view_notes(self):
        if self.notes:
            self.view_window = tk.Toplevel(self.root)

    self.view_window.title("Все записи")
    self.listbox = tk.Listbox(self.view_window, width=50, height=10)
    self.listbox.pack(padx=10, pady=10)
    for note in self.notes:
        self.listbox.insert(tk.END, note)
    self.listbox.bind("<<ListboxSelect>>", self.on_note_select)
    else:
    messagebox.showinfo("Пусто", "Нет сохраненных записей.")
    self.enable_edit_delete_buttons(False)

    def on_note_select(self, event):
        selected_note = self.listbox.get(self.listbox.curselection())

    self.current_note = selected_note
    self.enable_edit_delete_buttons(True)

    def edit_note(self):
        if self.current_note:
            self.edit_window = tk.Toplevel(self.root)

    self.edit_window.title("Редактировать запись")
    self.edit_note_label = ttk.Label(self.edit_window, text="Запись:")
    self.edit_note_text = tk.Text(self.edit_window, height=10, width=50)
    self.edit_note_text.insert("1.0", self.current_note)
    self.edit_rating_label = ttk.Label(self.edit_window, text="Оценка (1-5):")
    self.edit_rating_scale = tk.Scale(self.edit_window, from_=1, to=5, orient=tk.HORIZONTAL)
    self.edit_rating_scale.set(self.notes[self.current_note])
    self.save_button = ttk.Button(self.edit_window, text="Сохранить", command=self.save_edited_note)

    self.edit_note_label.grid(row=0, column=0, sticky=tk.W)
    self.edit_note_text.grid(row=1, column=0)
    self.edit_rating_label.grid(row=2, column=0, sticky=tk.W)
    self.edit_rating_scale.grid(row=3, column=0)
    self.save_button.grid(row=4, column=0)
    else:
    messagebox.showerror("Ошибка", "Нет выбранной заметки для редактирования.")

    def save_edited_note(self):
        new_note = self.edit_note_text.get("1.0", tk.END).strip()

    new_rating = self.edit_rating_scale.get()
    if new_note:
        self.notes.pop(self.current_note)
    self.notes[new_note] = new_rating
    messagebox.showinfo("Сохранено", "Запись изменена!")
    self.edit_window.destroy()
    self.view_window.destroy()
    self.enable_edit_delete_buttons(False)
    else:
    messagebox.showerror("Ошибка", "Запись не может быть пустой!")

    def delete_note(self):
        if self.current_note:
            result = messagebox.askyesno("Удалить", "Вы уверены, что хотите удалить эту запись?")

    if result:
        self.notes.pop(self.current_note)
    messagebox.showinfo("Удалено", "Запись удалена!")
    self.view_window.destroy()
    self.enable_edit_delete_buttons(False)
    else:
    messagebox.showerror("Ошибка", "Нет выбранной заметки для удаления.")

    def enable_edit_delete_buttons(self, enable):
        state = tk.NORMAL if enable else tk.DISABLED

    self.edit_button.config(state=state)
    self.delete_button.config(state=state)


root = tk.Tk()
app = DiaryApp(root)
root.mainloop()

