# ASDScreener/asdscreener/core/system_definition.py
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from .api_properties import API
from .polymer_properties import Polymer

@dataclass
class ASDSystem:
    """
    Represents a specific API-Polymer system at a given drug load.
    This class will hold results from various calculations and predictions.
    """
    api: API
    polymer: Polymer
    drug_load_wt_percent: float  # API weight percent in the ASD (e.g., 20.0 for 20%)

    # Predicted/Calculated properties for this specific system
    # Thermodynamics
    hansen_Ra_mpa_half: Optional[float] = None
    delta_hildebrand_mpa_half: Optional[float] = None
    chi_interaction_parameter: Optional[float] = None # Flory-Huggins chi
    delta_g_mix_values: Optional[Dict[float, float]] = None # {phi_api: dGmix/RT}
    sp_cry_wt_percent: Optional[float] = None # API solubility in polymer (wt%)

    # Glass Transition
    tg_asd_c: Optional[float] = None # Predicted Tg of the ASD
    tg_asd_plasticized_c: Optional[float] = None # Predicted Tg after water uptake

    # Stability
    tg_margin_K: Optional[float] = None # Tg_ASD - T_storage
    qualitative_stability_score: Optional[float] = None # e.g., 0-10 scale
    stability_risk_flags: list[str] = field(default_factory=list)
    predicted_shelf_life_conceptual: Optional[str] = None # e.g. "Rank: High"

    # ML Predictions
    ml_predictions: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not (0 < self.drug_load_wt_percent < 100):
            raise ValueError("Drug load must be between 0 and 100 wt%")
        self.drug_load_frac = self.drug_load_wt_percent / 100.0 # as fraction
        self.polymer_load_frac = 1.0 - self.drug_load_frac

    @property
    def volume_fraction_api(self) -> Optional[float]:
        """Calculates API volume fraction if densities are known."""
        if self.api.density_g_cm3 and self.polymer.density_g_cm3:
            mass_api = self.drug_load_frac
            mass_poly = self.polymer_load_frac
            vol_api = mass_api / self.api.density_g_cm3
            vol_poly = mass_poly / self.polymer.density_g_cm3
            if (vol_api + vol_poly) == 0: return None
            return vol_api / (vol_api + vol_poly)
        return None # Cannot calculate without densities

    def add_risk_flag(self, flag_message: str):
        if flag_message not in self.stability_risk_flags:
            self.stability_risk_flags.append(flag_message)

    def __str__(self):
        return f"ASDSystem(API='{self.api.name}', Polymer='{self.polymer.name}', DrugLoad={self.drug_load_wt_percent}%)"