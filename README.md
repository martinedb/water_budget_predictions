# Water Budget Predictions for Wetland Engineering in Beaverlodge, Alberta

## Project Overview

This repository contains Python scripts for estimating water budgets essential to wetland engineering, focusing on the hydrological processes of snowmelt, precipitation, and evapotranspiration. The analysis leverages high-quality Government of Canada climate data from Beaverlodge, Alberta—specifically total snow and total precipitation records—to inform and validate the calculations. Understanding these components is critical for the design, restoration, and management of engineered wetlands, as accurate water budgeting dictates wetland viability, habitat conditions, and flood mitigation.

---

## 1. Snowmelt Estimates

### File: `snowmelt_estimates.py`

**Purpose:**  
Calculates the amount of water entering the wetland system via snowmelt. The script converts recorded snowfall to its water equivalent and models seasonal melt dynamics, which is crucial for predicting spring inflows and annual catchment water yield.

**Process:**
- **Data Import:** Reads Beaverlodge snow data (CSV or Excel) from Government of Canada sources.
- **Conversion:** Transforms snowfall (cm) to water equivalent (mm) using empirically derived density ratios.
- **Modeling:** Simulates snowpack accumulation and melt periods, employing temperature and degree-day methods to estimate timing and volume of runoff.
- **Output:** Monthly and annual snowmelt values, which become vital inputs to the wetland water budget.

**Sample Usage:**
```python
import pandas as pd
from snowmelt_estimates import estimate_snowmelt

data = pd.read_csv('beaverlodge_snow.csv')
snowmelt_mm = estimate_snowmelt(data)
print(snowmelt_mm)
```

---

## 2. Evapotranspiration and Precipitation

### Files: `evapotranspiration.py` & `precipitation.py`

**Purpose:**  
These scripts quantify the main water fluxes:
- **Evapotranspiration:** Represents water lost from the wetland surface and vegetation, a key factor in water balance and wetland sustainability.
- **Precipitation:** Includes both rainfall and snowmelt contributions, measured directly from Beaverlodge climate records.

**Process:**
- **Evapotranspiration Calculation:** Uses climate variables (temperature, solar radiation, humidity, wind speed) and established formulas (e.g., Penman-Monteith) to estimate monthly/annual ET rates.
- **Precipitation Analysis:** Extracts and processes total precipitation values, enabling direct comparison with modeled snowmelt and ET.
- **Integration:** These scripts work together to provide a comprehensive assessment of water inputs and losses, supporting engineering decisions for wetland design.

**Sample Usage:**
```python
from evapotranspiration import estimate_et
from precipitation import get_precipitation

climate = pd.read_csv('beaverlodge_climate.csv')
et_mm = estimate_et(climate)
precip_mm = get_precipitation(climate)

print(f"Evapotranspiration: {et_mm}")
print(f"Precipitation: {precip_mm}")
```

---

## 3. How These Components Connect

The water budget for an engineered wetland can be summarized as:
```
Water In (Precipitation + Snowmelt) - Water Out (Evapotranspiration) = Net Water Availability
```
- **Snowmelt Estimates** provide critical spring and annual inflows.
- **Precipitation Analysis** quantifies direct inputs across seasons.
- **Evapotranspiration Modelling** assesses losses that must be compensated for wetland sustainability.

Collectively, these scripts enable engineers and scientists to:
- Predict water availability and variability.
- Design wetlands with sufficient retention and resilience.
- Support habitat creation and flood management using robust, site-specific data.

---

## 4. Data Source and Integration

- **Government of Canada climate data** for Beaverlodge, Alberta is used for snow and precipitation inputs.
- Scripts are tailored to read official CSV/Excel formats, ensuring data integrity and ease of use.
- Outputs are suitable for further hydrological modeling, wetland design, and environmental impact assessment.

---

## 5. Getting Started

1. **Install dependencies:**  
   ```bash
   pip install pandas numpy
   ```
2. **Download Beaverlodge climate data** from the Government of Canada and place files in the project directory.
3. **Run each script** as demonstrated above to generate water budget components.

---

## 6. Relevance to Wetland Engineering

Accurate water budget predictions are crucial for:
- **Sizing and siting wetlands**
- **Ensuring year-round water availability**
- **Managing flood and drought risk**
- **Supporting biodiversity targets and ecological function**

These scripts provide the quantitative foundation for these engineering decisions.

---

## 7. License & Attribution

- Data © Government of Canada
- Scripts © [Your Name or Organization], MIT License

---

## 8. Questions & Collaboration

Please open an issue or pull request for support, improvements, or collaborative research.
