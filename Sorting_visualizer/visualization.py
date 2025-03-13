def visualize_sorting(data_generator, title, interval=100):
    fig, ax = plt.subplots()
    ax.set_title(title)

    data = next(data_generator)
    bars = ax.bar(range(len(data)), data, color='skyblue')

    def update_fig(data):
        for bar, val in zip(bars, data):
            bar.set_height(val)
            if hasattr(data_generator, 'highlight') and bar.get_x() in data_generator.highlight:
                bar.set_color('red')
            else:
                bar.set_color('skyblue')
        return bars

    anim = animation.FuncAnimation(fig, update_fig, frames=data_generator, repeat=False, interval=interval)
    plt.show()