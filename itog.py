import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("500x600")

        # Данные для генерации
        self.digits = "0123456789"
        self.letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"

        # История паролей
        self.history = []
        self.load_history()

        self.setup_ui()

    def setup_ui(self):
        # Ползунок длины пароля
        ttk.Label(self.root, text="Длина пароля:").pack(pady=5)
        self.length_scale = ttk.Scale(
            self.root, from_=4, to=32, orient="horizontal"
        )
        self.length_scale.set(12)
        self.length_scale.pack(pady=5, fill="x", padx=20)

        # Отображение текущей длины
        self.length_label = ttk.Label(self.root, text="12 символов")
        self.length_label.pack(pady=2)

        # Чекбоксы для выбора символов
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)

        ttk.Checkbutton(self.root, text="Цифры (0-9)", variable=self.use_digits).pack(anchor="w", padx=20)
        ttk.Checkbutton(self.root, text="Буквы (a-Z)", variable=self.use_letters).pack(anchor="w", padx=20)
        ttk.Checkbutton(self.root, text="Спецсимволы", variable=self.use_special).pack(anchor="w", padx=20)

        # Кнопка генерации
        self.generate_btn = ttk.Button(
            self.root, text="Сгенерировать пароль", command=self.generate_password
        )
        self.generate_btn.pack(pady=10)

        # Поле вывода пароля
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            self.root, textvariable=self.password_var, font=("Courier", 12), justify="center"
        )
        self.password_entry.pack(pady=5, fill="x", padx=20)

        # Таблица истории
        ttk.Label(self.root, text="История паролей:").pack(pady=5)
        columns = ("ID", "Пароль", "Длина", "Дата создания")
        self.history_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)

        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)

        self.history_tree.pack(pady=5, padx=20, fill="both", expand=True)

        # Обновление ползунка
        self.length_scale.config(command=self.update_length_label)

        # Загрузка истории в таблицу
        self.refresh_history_table()

    def update_length_label(self, value):
        self.length_label.config(text=f"{int(float(value))} символов")

    def generate_password(self):
        length = int(self.length_scale.get())

        # Проверка минимальной/максимальной длины
        if length < 4:
            messagebox.showerror("Ошибка", "Минимальная длина пароля — 4 символа!")
            return
        if length > 32:
            messagebox.showerror("Ошибка", "Максимальная длина пароля — 32 символа!")
            return

        # Формирование набора символов
        chars = ""
        if self.use_digits.get():
            chars += self.digits
        if self.use_letters.get():
            chars += self.letters
        if self.use_special.get():
            chars += self.special

        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return

        # Генерация пароля
        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)

        # Добавление в историю
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "id": len(self.history) + 1,
            "password": password,
            "length": length,
            "timestamp": timestamp
        }
        self.history.append(entry)
        self.save_history()
        self.refresh_history_table()

    def refresh_history_table(self):
        # Очистка таблицы
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Заполнение таблицы
        for entry in self.history:
            self.history_tree.insert("", "end", values=(
                entry["id"], entry["password"], entry["length"], entry["timestamp"]
            ))

    def save_history(self):
        with open("password_history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)

    def load_history(self):
        if os.path.exists("password_history.json"):
            try:
                with open("password_history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.history = []

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
