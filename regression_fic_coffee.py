import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

def generate_coffee_data(num_points=50):
    weather = np.random.normal(0, 1, num_points)  # Standard normal distribution
    yield_ = np.random.normal(0, 1, num_points)  # Standard normal distribution
    demand = np.random.normal(0, 1, num_points)  # Standard normal distribution
    price = 5 + 2 * weather - 1.5 * yield_ + 3 * demand + np.random.normal(0, 1, num_points)  # Price with noise
    return weather, yield_, demand, price

def animate_regression():
    weather, yield_, demand, price = generate_coffee_data()
    fig, ax = plt.subplots()
    ax.set_xlabel("Demand")
    ax.set_ylabel("Coffee Bean Price (Fictitious)")
    ax.set_title("Regression Analysis:- Price of Coffee Bean vs Demand")
    
    scatter = ax.scatter([], [])
    line, = ax.plot([], [], 'r-')
    
    def init():
        ax.set_xlim(min(demand) - 1, max(demand) + 1)
        ax.set_ylim(min(price) - 1, max(price) + 1)
        return scatter, line,
    
    def update(frame):
        frame_data = demand[:frame + 1]
        frame_price = price[:frame + 1]
    
        scatter.set_offsets(np.c_[frame_data, frame_price])
    
        if len(frame_data) > 1:
            m, b = np.polyfit(frame_data, frame_price, 1)  # Linear regression
            x_line = np.linspace(min(demand), max(demand), 100)
            y_line = m * x_line + b
            line.set_data(x_line, y_line)
        else:
            line.set_data([], [])
        
        return scatter, line,
    
    ani = animation.FuncAnimation(fig, update, frames=len(demand), init_func=init, blit=True, repeat=False)
    ani.save('coffee_regression.gif', writer='pillow', fps=10)
    plt.close(fig)

animate_regression()
