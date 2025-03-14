import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from PIL import Image

def archimedes_pi(sides):
    angle = 360.0 / sides
    half_angle_rad = math.radians(angle / 2.0)
    perimeter = sides * math.sin(half_angle_rad) * 2.0
    return perimeter / 2.0  

def animate_archimedes(max_sides=96):
    frames = []
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('off')
    
    def update(sides):
        ax.clear()
        ax.set_aspect('equal')
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.axis('off')
        
        if sides < 3:
            return
            
        angle = 360.0 / sides
        half_angle_rad = math.radians(angle / 2.0)
        apothem = math.cos(half_angle_rad)
        pi_approx = archimedes_pi(sides)
        
        points = []
        for i in range(sides):
            theta = math.radians(i * angle)
            x = math.cos(theta)
            y = math.sin(theta)
            points.append((x, y))
            
        points.append(points[0]) 
        
        xs, ys = zip(*points)
        ax.plot(xs, ys, 'b-')
        ax.plot(0, 0, 'ro')  # Center
        
        ax.annotate('', xy=(1, 0), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='g'))
        ax.text(0.5, -0.1, "Radius", ha='center', va='center', fontsize=8)
        
        x_side_start, y_side_start = points[0]
        x_side_end, y_side_end = points[1]
        ax.annotate('', xy=(x_side_start, y_side_start), xytext=(x_side_end, y_side_end), arrowprops=dict(arrowstyle='<->', color='m'))
        ax.text((x_side_start + x_side_end) / 2, (y_side_start + y_side_end) / 2, "Side", ha='center', va='center', fontsize=8)
        
        mid_theta = math.radians(angle / 2)
        mid_x = math.cos(mid_theta)
        mid_y = math.sin(mid_theta)
        
        ax.annotate('', xy=(mid_x, mid_y), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='c'))
        ax.text(mid_x / 2, mid_y / 2, "Apothem", ha='center', va='center', fontsize=8)
        
        ax.set_title(f"Sides: {sides}, Pi ≈ {pi_approx:.4f}")
        
        fig.canvas.draw()
        image = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
        frames.append(image)
        
    for i in range(3, max_sides + 1):
        update(i)
        
    frames[0].save('archimedes_pi.gif', save_all=True, append_images=frames[1:], loop=0, duration=1000)
    plt.close(fig)

animate_archimedes()

