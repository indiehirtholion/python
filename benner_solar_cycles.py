import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from io import StringIO

def plot_solar_cycles_with_data(start_year, end_year):
    """
    Plots an approximate 11-year solar cycle and overlays actual sunspot data,
    with vertical lines for Benner's "panic", "hard times", and "good times" years.
    """
    years = end_year - start_year
    time = np.arange(start_year, end_year, 0.1)
    amplitude = -np.sin(2 * np.pi * (time - start_year) / 11)  # Inverted sine wave
    plt.figure(figsize=(14, 8))
    plt.plot(time, amplitude, label="Approximate 11-Year Cycle", linestyle='--')
    try:
        url = "https://www.sidc.be/silso/DATA/SN_m_tot_V2.0.txt"
        response = requests.get(url)
        response.raise_for_status()
        data = StringIO(response.text)
        df = pd.read_csv(data, sep='\s+', header=None, names=['year', 'month', 'decimal_year', 'sunspots', 'std', 'obs'], on_bad_lines='skip')
        df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
        plt.plot(df['decimal_year'], df['sunspots'] / max(df['sunspots']), label="Actual Sunspot Data (Normalized)")
        plt.xlabel("Year")
        plt.ylabel("Relative Solar Activity")
        plt.title(f"Solar Cycles and Benner's Cycles ({start_year} - {end_year})")
        plt.grid(True)
        # Vertical line for approximately March 2025
        plt.axvline(x=2025.25, color='red', linestyle='--', label='Approx. March 2025')
        # Vertical lines for "years of panic" (purple)
        panic_years = [1965, 1981, 1998, 2019]
        for year in panic_years:
            plt.axvline(x=year, color='purple', linestyle='-', label='Years of Panic' if year == panic_years[0] else "")
        # Vertical lines for "years of hard times" (orange)
        hard_times_years = [1951, 1958, 1969, 2005, 2012, 2023]
        for year in hard_times_years:
            plt.axvline(x=year, color='orange', linestyle='-', label='Years of Hard Times' if year == hard_times_years[0] else "")
        # Vertical lines for "years of good times" (green)
        good_times_years = [1953, 1962, 1972, 1980, 1989, 2001, 2007, 2016, 2026]
        for year in good_times_years:
            plt.axvline(x=year, color='green', linestyle='-', label='Years of Good Times' if year == good_times_years[0] else "")
        plt.legend(loc='lower left')
        plt.show()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except pd.errors.ParserError as e:
        print(f"Error parsing data: {e}")
    except Exception as e:
        print(f"An unexpected error occured: {e}")

if __name__ == "__main__":
    plot_solar_cycles_with_data(1950, 2030)
