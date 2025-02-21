import numpy as np
import matplotlib.pyplot as plt

def simulate_tariff_impact(tariff_rate, sector_percentages, elasticities, inflation_rate=0.02, retaliation_factor=0.05, years=4):
    gdp = {"USA": 27.0, "China": 17.7, "EU": 18.8, "Mexico": 1.7, "Canada": 2.2}
    exports = {"USA": 2.1, "China": 3.6, "EU": 2.7, "Mexico": 0.5, "Canada": 0.6}
    imports = {"USA": 3.3, "China": 2.7, "EU": 2.6, "Mexico": 0.6, "Canada": 0.5}
    
    gdp_impact_years = {country: [] for country in gdp.keys()}
    
    for year in range(years):
        gdp_impact = {}
        for country in gdp.keys():
            impact = 0
            for sector, percent in sector_percentages.items():
                export_loss = exports[country] * percent * (1 - tariff_rate * elasticities[sector])
                import_cost = imports[country] * percent * (1 + tariff_rate * elasticities[sector])
                sector_impact = export_loss - import_cost
                impact += sector_impact
            
            # Adjust for inflation and retaliatory tariffs over time
            impact *= (1 - inflation_rate) ** year
            impact *= (1 - retaliation_factor * year)
            
            gdp_impact[country] = (impact / gdp[country]) * 100
            gdp_impact_years[country].append(gdp_impact[country])
    
    return gdp_impact_years

def plot_results(gdp_impact_years):
    plt.figure(figsize=(10, 5))
    for country, impacts in gdp_impact_years.items():
        plt.plot(range(1, len(impacts) + 1), impacts, label=country, marker='o')
    plt.xlabel("Years")
    plt.ylabel("GDP Impact (% Change)")
    plt.title("GDP Impact of Tariffs Over 4 Years (With Inflation & Retaliation)")
    plt.legend()
    plt.grid()
    plt.show()

def main():
    tariff_rate = 0.20
    sector_percentages = {"Technology": 0.30, "Automotive": 0.20, "Agriculture": 0.15, "Energy": 0.20, "Manufacturing": 0.15}
    elasticities = {"Technology": 1.2, "Automotive": 0.8, "Agriculture": 0.9, "Energy": 0.6, "Manufacturing": 1.0}
    
    results = simulate_tariff_impact(tariff_rate, sector_percentages, elasticities, inflation_rate=0.02, retaliation_factor=0.05)
    
    print("GDP Impact of Tariffs (% Change in GDP):")
    for country, impacts in results.items():
        print(f"{country}: {impacts[-1]:.2f}% after 4 years")
    
    plot_results(results)

if __name__ == "__main__":
    main()
