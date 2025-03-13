import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation, PillowWriter

np.random.seed(42)
population = np.random.uniform(low=0, high=100, size=100000)
sample_size = 30  
num_samples = 700  
means = []  
sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(20, 80)  # X-axis limits
ax.set_ylim(0, 100)  # Y-axis limits
ax.set_title("Demonstrating Central Limit Theorem", fontsize=14)
ax.set_xlabel("Sample Mean")
ax.set_ylabel("Frequency")

def update(frame):
    sample = np.random.choice(population, size=sample_size, replace=False)  
    sample_mean = np.mean(sample)  
    means.append(sample_mean)  
    
    ax.clear()  # Clear previous frame
    sns.histplot(means, bins=30, kde=True, color="blue", ax=ax)  
    
    if len(means) > 1:
        mean_of_means = np.mean(means)
        std_of_means = np.std(means, ddof=1)  
        
        # Plot 1 standard deviation range
        line1 = ax.axvline(mean_of_means - std_of_means, color="green", linestyle="dashed", label="±1 Std Dev")
        line2 = ax.axvline(mean_of_means + std_of_means, color="green", linestyle="dashed")
        
        # Plot 2 standard deviation range
        line3 = ax.axvline(mean_of_means - 2 * std_of_means, color="purple", linestyle="dotted", label="±2 Std Dev")
        line4 = ax.axvline(mean_of_means + 2 * std_of_means, color="purple", linestyle="dotted")
        
        # Annotate standard deviation values
        ax.text(mean_of_means - std_of_means, 85, "-1σ", fontsize=10, color="green", ha='right')
        ax.text(mean_of_means + std_of_means, 85, "+1σ", fontsize=10, color="green", ha='left')
        ax.text(mean_of_means - 2 * std_of_means, 70, "-2σ", fontsize=10, color="purple", ha='right')
        ax.text(mean_of_means + 2 * std_of_means, 70, "+2σ", fontsize=10, color="purple", ha='left')
        
        ax.legend(handles=[line1, line3])
        
    ax.set_xlim(20, 80)
    ax.set_ylim(0, 100)
    ax.set_title("Demonstrating Central Limit Theorem", fontsize=14)
    ax.set_xlabel("Sample Mean")
    ax.set_ylabel("Frequency")
    ax.text(65, 80, f"Samples Taken: {frame+1}", fontsize=12, color='red')  # Display count

# Animatation
ani = FuncAnimation(fig, update, frames=num_samples, interval=25, repeat=False)

# GIF
ani.save("clt_animation.gif", writer=PillowWriter(fps=10))

plt.show()
## GIF to Plt debug needed
