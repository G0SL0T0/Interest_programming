import matplotlib.pyplot as plt
import matplotlib.animation as animation

def visualize_sorting(data_generator, title, interval=100):
    fig, ax = plt.subplots()
    ax.set_title(title)

    # Инициализация столбцов
    data = next(data_generator)
    bars = ax.bar(range(len(data)), data, color='skyblue')

    # Функция обновления графика
    def update_fig(data):
        for bar, val in zip(bars, data):
            bar.set_height(val)
        return bars

    # Создание анимации
    anim = animation.FuncAnimation(fig, update_fig, frames=data_generator, repeat=False, interval=interval)
    plt.show()