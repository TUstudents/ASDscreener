# ASDScreener/asdscreener/core/api_properties.py
from dataclasses import dataclass, field
from typing import Optional, Dict, List

@dataclass
class API:
    """
    Represents an Active Pharmaceutical Ingredient (API) and its properties.
    """
    name: str
    smiles: Optional[str] = None  # SMILES string for descriptor calculation
    mw: Optional[float] = None  # Molecular Weight (g/mol)
    tm_c: Optional[float] = None  # Melting Temperature (°C)
    hf_j_per_mol: Optional[float] = None  # Enthalpy of Fusion (J/mol)
    tg_api_c: Optional[float] = None  # Glass Transition Temperature of amorphous API (°C)
    sc_mg_per_ml: Optional[float] = None  # Crystalline Solubility (e.g., in water, mg/mL)
    log_p: Optional[float] = None
    h_bond_donors: Optional[int] = None
    h_bond_acceptors: Optional[int] = None
    psa: Optional[float] = None  # Polar Surface Area
    density_g_cm3: Optional[float] = None
    bcs_class: Optional[str] = None # e.g., "II", "IV"
    highest_dose_mg: Optional[float] = None
    
    # For calculated descriptors if SMILES is provided
    _calculated_descriptors: Dict[str, float] = field(default_factory=dict, repr=False)

    def __post_init__(self):
        if self.tm_c is not None:
            self.tm_k = self.tm_c + 273.15
        else:
            self.tm_k = None
            
        if self.tg_api_c is not None:
            self.tg_api_k = self.tg_api_c + 273.15
        else:
            self.tg_api_k = None

    def get_property(self, prop_name: str, calculate_if_missing: bool = False):
        """
        Gets a property, trying calculated descriptors if the direct attribute is None.
        Placeholder for future integration with descriptor_calculator.
        """
        value = getattr(self, prop_name, None)
        if value is not None:
            return value
        if calculate_if_missing and prop_name in self._calculated_descriptors:
            return self._calculated_descriptors[prop_name]
        # Here, one might eventually call a descriptor calculator if SMILES is present
        # For now, it just checks pre-calculated ones.
        return None

    def update_calculated_descriptors(self, descriptors: Dict[str, float]):
        """Updates the internal dictionary of calculated descriptors."""
        self._calculated_descriptors.update(descriptors)

    def __str__(self):
        return f"API(name='{self.name}', MW={self.mw:.2f} g/mol, Tm={self.tm_c}°C, Tg_API={self.tg_api_c}°C)" \
               if self.mw and self.tm_c and self.tg_api_c else f"API(name='{self.name}')"