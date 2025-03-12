import tkinter as tk
from tkinter import ttk
from algorithms import bubble_sort, quick_sort, merge_sort
from visualization import visualize_sorting
from utils import generate_data

def start_sorting():
    size = int(size_entry.get())
    algorithm = algorithm_combobox.get()
    data = generate_data(size)

    if algorithm == "Bubble Sort":
        generator = bubble_sort(data)
    elif algorithm == "Quick Sort":
        generator = quick_sort(data)
    elif algorithm == "Merge Sort":
        generator = merge_sort(data)
    else:
        return

    visualize_sorting(generator, algorithm)

# Создаем интерфейс
root = tk.Tk()
root.title("Интерактивная сортировка")

# Поле для ввода размера данных
size_label = tk.Label(root, text="Размер данных:")
size_label.pack()
size_entry = tk.Entry(root)
size_entry.pack()

# Выбор алгоритма
algorithm_label = tk.Label(root, text="Алгоритм сортировки:")
algorithm_label.pack()
algorithm_combobox = ttk.Combobox(root, values=["Bubble Sort", "Quick Sort", "Merge Sort"])
algorithm_combobox.pack()

# Кнопка запуска
start_button = tk.Button(root, text="Начать сортировку", command=start_sorting)
start_button.pack()

root.mainloop()