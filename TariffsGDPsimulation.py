import numpy as np
import matplotlib.pyplot as plt
import cv2

# Parameters for years 2025 to 2028
years = np.arange(2025, 2029, 1/12)  
total_months = len(years)

# GDP
canada_gdp_change = np.linspace(0, -5.6, total_months)
us_gdp_change = np.linspace(0, -0.8, total_months)

# IPL
frame_width = 800
frame_height = 600
fps = 30  
loop_duration = 5  
frames_per_loop = fps * loop_duration
num_loops = 4  
total_frames = frames_per_loop * num_loops
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  
out = cv2.VideoWriter("gdp_projection.mp4", fourcc, fps, (frame_width, frame_height))
for frame in range(total_frames):
    month_idx = frame % total_months  
   
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(2025, 2028)
    ax.set_ylim(-6, 1)
    ax.set_xlabel("Year")
    ax.set_ylabel("GDP Change (%)")
    ax.set_title("Projected GDP Change Due to US-Canada Tariffs")
   
    ax.plot(years[:month_idx+1], canada_gdp_change[:month_idx+1], marker="o", label="Canada GDP Change", color="red")
    ax.plot(years[:month_idx+1], us_gdp_change[:month_idx+1], marker="o", label="US GDP Change", color="blue")
    ax.legend()
   
    plt.savefig("temp_frame.png")
    plt.close(fig)
   
    frame_img = cv2.imread("temp_frame.png")
    frame_img = cv2.resize(frame_img, (frame_width, frame_height))
   
    out.write(frame_img)

# Pump out the video
out.release()
print("Video saved as gdp_projection.mp4")
