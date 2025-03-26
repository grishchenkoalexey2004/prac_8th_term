import tkinter as tk
from tkinter import ttk

# пример простейшего интерфейса для справки

def on_button_click():
    # Получаем значения из ползунков и числовых полей
    slider1_value = slider1.get()
    slider2_value = slider2.get()
    entry1_value = entry1.get()
    entry2_value = entry2.get()
    
    # Выводим значения в консоль
    print(f"Slider 1: {slider1_value}")
    print(f"Slider 2: {slider2_value}")
    print(f"Entry 1: {entry1_value}")
    print(f"Entry 2: {entry2_value}")

# Создаем главное окно
root = tk.Tk()
root.title("Пример интерфейса с ползунками и полями ввода")

# Создаем и размещаем ползунки
slider1_label = ttk.Label(root, text="Ползунок 1:")
slider1_label.grid(row=0, column=0, padx=10, pady=10)
slider1 = ttk.Scale(root, from_=0, to=100, orient="horizontal")
slider1.grid(row=0, column=1, padx=10, pady=10)

slider2_label = ttk.Label(root, text="Ползунок 2:")
slider2_label.grid(row=1, column=0, padx=10, pady=10)
slider2 = ttk.Scale(root, from_=0, to=100, orient="horizontal")
slider2.grid(row=1, column=1, padx=10, pady=10)

# Создаем и размещаем числовые поля
entry1_label = ttk.Label(root, text="Числовое поле 1:")
entry1_label.grid(row=2, column=0, padx=10, pady=10)
entry1 = ttk.Entry(root)
entry1.grid(row=2, column=2, padx=10, pady=10)

entry2_label = ttk.Label(root, text="Числовое поле 2:")
entry2_label.grid(row=3, column=0, padx=10, pady=10)
entry2 = ttk.Entry(root)
entry2.grid(row=3, column=1, padx=10, pady=10)

# Создаем и размещаем кнопку
button = ttk.Button(root, text="Получить значения", command=on_button_click)
button.grid(row=4, column=0, columnspan=2, pady=10)

# Запускаем главный цикл обработки событий
root.mainloop()