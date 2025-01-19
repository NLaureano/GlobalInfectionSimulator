# QuackHacksW25
Quackhacks Project W25

# Global Infection Simulator

An interactive visualization tool that simulates the spread of infection across different countries, taking into account various factors such as Human Development Index (HDI) and country interconnections.

<img width="1159" alt="Screen Shot 2025-01-19 at 11 19 32 AM" src="https://github.com/user-attachments/assets/7c91cd4a-fc1c-4b4e-a5a5-3e368c57dd66" />




## Features

- **Interactive World Map**: Click on countries to select infection starting points
- **Real-time Visualization**: Watch as the infection spreads across countries
- **Country-specific Modeling**: Uses real-world data including:
  - Population data
  - Human Development Index (HDI)
  - Geographic borders and connections

## Components

### main.py
The main GUI application that provides:
- World map visualization
- Country selection interface
- Simulation controls
- Real-time statistics

Controls:
1. **Virulence**: Adjust the infection spread rate (0-100%)
2. **Starting Country**: Click to select the initial infection point
3. **Start/Step**: Control simulation progression
4. **Reset**: Clear all infections and start over
5. **Total Infected**: View current infection statistics

### infectionSimulator.py
The core simulation engine that handles:
- Infection spread calculations
- Country response modeling
- Population dynamics
- Geographic spread patterns

Features:
- HDI-based country response simulation
- Realistic spread patterns based on country connections
- Population-aware infection modeling

## How to Use

1. **Setup**:
   ```bash
   python3 main.py
   ```

2. **Start Simulation**:
   - Adjust virulence using the slider
   - Click "Starting Country" button
   - Select a country on the map
   - Use "Start/Step" to begin simulation

3. **Monitor Progress**:
   - Red areas indicate infected regions
   - Check statistics for detailed infection counts
   - Use reset to start a new simulation

## Requirements
- Python 3.x
- tkinter
- PIL (Python Imaging Library)
- numpy

## Data Sources
- Country borders data (`borders.py`)
- Population and HDI data (`datasets/seed.json`)
- World map image (`world.png`)

## Implementation Details

### Infection Spread Model
- Uses probabilistic modeling based on virulence
- Considers country HDI for response effectiveness
- Accounts for geographic proximity and connections

### Visualization
- Grid-based country representation
- Color intensity indicates infection severity
- Real-time updates during simulation


## Resources
- [CIA World Factbook - National Air Transport System](https://www.cia.gov/the-world-factbook/field/national-air-transport-system/)
- [Maps of World](https://www.mapsofworld.com/)
- [CDC Wonder - NNDSS Data](https://wonder.cdc.gov/nndss/static/2018/annual/2018-table1.html)
- [CIA World Factbook - Population Country Comparison](https://www.cia.gov/the-world-factbook/field/population/country-comparison/)
- [Human Development Index Data Center](https://hdr.undp.org/data-center/human-development-index#/indicies/HDI)
- [Disease Prediction Using Machine Learning - GeeksforGeeks](https://www.geeksforgeeks.org/disease-prediction-using-machine-learning/)
