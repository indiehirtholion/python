import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fs = 1000  
t = np.linspace(0, 1, fs, endpoint=False) 
freqs = [5, 20, 50] 
amplitudes = [1, 0.5, 0.3]
waves = [amplitudes[i] * np.sin(2 * np.pi * freqs[i] * t) for i in range(len(freqs))]
signal = sum(waves)
fft_values = np.fft.fft(signal)
fft_freqs = np.fft.fftfreq(len(t), 1/fs)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 9))
plt.subplots_adjust(hspace=0.25) 
line1, = ax1.plot(t, np.zeros_like(t), 'b', label="Sum of Waves")
lines_waves = [ax1.plot(t, np.zeros_like(t), '--', label=f"{freqs[i]} Hz Wave")[0] for i in range(len(freqs))]
ax1.set_xlim(0, 1)
ax1.set_ylim(-2, 2)
ax1.set_title("Unveiling a Complex Wave into Its Fundamental Sines & Cosines")
ax1.set_xlabel("Time (seconds)")
ax1.set_ylabel("Amplitude")
ax1.legend()
line2, = ax2.plot(fft_freqs[:fs//2], np.zeros_like(fft_freqs[:fs//2]), 'r')
ax2.set_xlim(0, 60)
ax2.set_ylim(0, max(amplitudes) * fs/2)
ax2.set_title("Core FFT discomposition of pure Sine or Cosine frequencies")
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Amplitude")

def update(frame):
    for i in range(len(freqs)):
        lines_waves[i].set_ydata(amplitudes[i] * np.sin(2 * np.pi * freqs[i] * t + frame * 0.1))
    
    signal = sum(amplitudes[i] * np.sin(2 * np.pi * freqs[i] * t + frame * 0.1) for i in range(len(freqs)))
    line1.set_ydata(signal)
    
    fft_values = np.fft.fft(signal)
    magnitude = np.abs(fft_values[:fs//2]) 
    line2.set_ydata(magnitude)
    
    return [line1, line2] + lines_waves

# Animation
ani = animation.FuncAnimation(fig, update, frames=100, interval=50, blit=True)

# pump out the gif file and also show it
ani.save('fft_visualization.gif', writer='pillow', fps=20)

plt.show()
