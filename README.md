# ASDScreener

A Python library for screening and evaluating potential API-Polymer Amorphous Solid Dispersion (ASD) systems. This library aims to assist pharmaceutical scientists by providing tools for thermodynamic analysis, glass transition prediction, and qualitative stability assessment.

## DISCLAIMER

⚠️ Important Notice:
This library is currently in a pre-alpha, developmental stage and is provided strictly for educational, conceptual exploration, and brainstorming purposes only.
It is NOT intended for productive, commercial, or research decision-making use where accurate quantitative predictions are required. It is broken by design and likely never be fixed. Data is not curated and formulas not checked.

## Features (Planned)

*   Calculation of miscibility indicators (Hansen Solubility Parameters, Flory-Huggins $\chi$).
*   Prediction of ASD glass transition temperatures ($T_g$).
*   Estimation of API solubility in polymers.
*   Qualitative stability risk assessment.
*   Generation of summary reports.

## Installation

This library is currently under development. Once released, it will be installable via pip:

```bash
pip install asdscreener


For development:
```bash
git clone https://github.com/yourusername/ASDScreener.git
cd ASDScreener
pip install -e .[dev] 
# (Assuming you'll add a [dev] extra in pyproject.toml for dev dependencies)
```

## Quick Start

```python
from asdscreener import API, Polymer, ASDSystem

# Define API
api_data = {
    "name": "Indomethacin", 
    "mw": 357.79, 
    "tm_c": 160.0, 
    "hf_j_per_mol": 30000, 
    "tg_api_c": 42.0
}
indomethacin = API(**api_data)

# Define Polymer
pvp_k30_monomer = MonomerInfo(name="Vinylpyrrolidone", molecular_weight_monomer=111.14, tg_homopolymer_c=175) # Hypothetical Tg for pure PVP
pvp_k30 = Polymer(
    name="PVP K30", 
    polymer_type="Homopolymer",
    monomers=[pvp_k30_monomer],
    tg_polymer_c=170.0, # Tg of PVP K30 can vary
    density_g_cm3=1.23,
    hsp_delta_d=18.5, hsp_delta_p=12.0, hsp_delta_h=10.5
)

# Create an ASD System
asd_system = ASDSystem(api=indomethacin, polymer=pvp_k30, drug_load_wt_percent=20.0)

print(asd_system)
print(f"API Volume Fraction (conceptual): {asd_system.volume_fraction_api}") 
# Needs densities in API/Polymer objects to calculate volume_fraction_api

```

## Development

(Details on setting up dev environment, running tests, etc.)