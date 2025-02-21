import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def simulate_tariff_impact(tariff_rate, sector_percentages, elasticities, inflation_rate=0.02, retaliation_factor=0.05, years=4, quarters_per_year=4):
    gdp = {"USA": 27.0, "China": 17.7, "EU": 18.8, "Mexico": 1.7, "Canada": 2.2}
    exports = {"USA": 2.1, "China": 3.6, "EU": 2.7, "Mexico": 0.5, "Canada": 0.6}
    imports = {"USA": 3.3, "China": 2.7, "EU": 2.6, "Mexico": 0.6, "Canada": 0.5}
    
    total_quarters = years * quarters_per_year
    gdp_impact_quarters = {country: [] for country in gdp.keys()}
    
    for quarter in range(total_quarters):
        gdp_impact = {}
        year_fraction = quarter / quarters_per_year
        for country in gdp.keys():
            impact = 0
            for sector, percent in sector_percentages.items():
                export_loss = exports[country] * percent * (1 - tariff_rate * elasticities[sector])
                import_cost = imports[country] * percent * (1 + tariff_rate * elasticities[sector])
                sector_impact = export_loss - import_cost
                impact += sector_impact
            impact *= (1 - inflation_rate) ** year_fraction
            impact *= (1 - retaliation_factor * year_fraction)
            gdp_impact[country] = max(-20, (impact / gdp[country]) * 100)  # Ensure Y values stay within 0 to -20
            gdp_impact_quarters[country].append(gdp_impact[country])
    
    return gdp_impact_quarters

def create_animation(gdp_impact_quarters, filename="tariff_impact.mp4", frame_width=640, frame_height=480, fps=2, loops=4):
    temp_dir = "temp_frames"
    os.makedirs(temp_dir, exist_ok=True)
    frame_files = []
    
    for _ in range(loops):
        for frame, _ in enumerate(next(iter(gdp_impact_quarters.values()))):
            fig, ax = plt.subplots(figsize=(10, 5))
            for country, impact in gdp_impact_quarters.items():
                ax.plot(range(frame + 1), impact[:frame + 1], label=country, marker='o')
            ax.set_xlim(0, len(next(iter(gdp_impact_quarters.values()))))
            ax.set_ylim(-20, 0)  # Keep Y values between 0 and -20
            ax.set_xlabel("Quarters")
            ax.set_ylabel("GDP Impact (% Change)")
            ax.set_title("GDP Impact of Tariffs Over Time (With Inflation & Retaliation)")
            ax.legend()
            ax.grid()
            frame_path = os.path.join(temp_dir, f"frame_{len(frame_files):04d}.png")
            plt.savefig(frame_path)
            plt.close(fig)
            frame_files.append(frame_path)
    
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))
    
    for frame_file in frame_files:
        frame_img = cv2.imread(frame_file)
        frame_img = cv2.resize(frame_img, (frame_width, frame_height))
        video.write(frame_img)
    
    video.release()
    for frame_file in frame_files:
        os.remove(frame_file)
    os.rmdir(temp_dir)

def main():
    tariff_rate = 0.20
    sector_percentages = {"Technology": 0.30, "Automotive": 0.20, "Agriculture": 0.15, "Energy": 0.20, "Manufacturing": 0.15}
    elasticities = {"Technology": 1.2, "Automotive": 0.8, "Agriculture": 0.9, "Energy": 0.6, "Manufacturing": 1.0}
    
    results = simulate_tariff_impact(tariff_rate, sector_percentages, elasticities, inflation_rate=0.02, retaliation_factor=0.05)
    
    print("GDP Impact of Tariffs (% Change in GDP):")
    for country, impacts in results.items():
        print(f"{country}: {impacts[-1]:.2f}% after {len(impacts)} quarters")
    
    create_animation(results, "tariff_impact.mp4", loops=4)
    print("Animation saved as 'tariff_impact.mp4'")

if __name__ == "__main__":
    main()
