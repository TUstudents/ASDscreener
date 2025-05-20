# ASDScreener/asdscreener/core/polymer_properties.py
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class MonomerInfo:
    """Information about a single monomer unit in a polymer."""
    name: str
    smiles: Optional[str] = None
    mole_fraction: float = 1.0
    molecular_weight_monomer: Optional[float] = None
    # Add other monomer-specific properties if needed for GCMs (e.g., Tg_homopolymer)
    tg_homopolymer_c: Optional[float] = None # Tg if this monomer formed a homopolymer

@dataclass
class Polymer:
    """
    Represents a polymer and its properties.
    """
    name: str
    polymer_type: str = "Homopolymer" # e.g., Homopolymer, Copolymer-Random, Copolymer-Block
    monomers: List[MonomerInfo] = field(default_factory=list)
    tg_polymer_c: Optional[float] = None  # Glass Transition Temperature (°C)
    density_g_cm3: Optional[float] = None
    mn_g_per_mol: Optional[float] = None  # Number Average Molecular Weight (g/mol)
    mw_g_per_mol: Optional[float] = None  # Weight Average Molecular Weight (g/mol)
    
    # Hansen Solubility Parameters (MPa^0.5)
    hsp_delta_d: Optional[float] = None 
    hsp_delta_p: Optional[float] = None
    hsp_delta_h: Optional[float] = None
    
    delta_cp_j_g_k: Optional[float] = None # Heat capacity change at Tg (J/g·K)
    hygroscopicity: Optional[str] = None # e.g., "Low", "Medium", "High"

    # Specific modification details
    degree_of_hydrolysis_mol_percent: Optional[float] = None # For PVA
    degree_of_substitution: Optional[Dict[str, float]] = None # For HPMC { "methoxy": 0.2, "hydroxypropoxy": 0.1}
    
    _calculated_properties: Dict[str, Any] = field(default_factory=dict, repr=False)


    def __post_init__(self):
        if self.tg_polymer_c is not None:
            self.tg_polymer_k = self.tg_polymer_c + 273.15
        else:
            # Try to estimate from Fox equation if it's a copolymer and monomer Tgs are known
            self.tg_polymer_k = self._estimate_copolymer_tg_k()
            if self.tg_polymer_k is not None:
                self.tg_polymer_c = self.tg_polymer_k - 273.15

        if not self.monomers and self.polymer_type == "Homopolymer":
            # If it's a homopolymer and no explicit monomer info given, create a placeholder
            # This assumes properties like HSP might be directly on the Polymer object
            # or derived from its overall name/type if in a database.
            pass
        elif self.monomers:
            self._validate_monomer_fractions()


    def _validate_monomer_fractions(self):
        if self.polymer_type != "Homopolymer" and self.monomers:
            total_fraction = sum(m.mole_fraction for m in self.monomers)
            if not (0.999 < total_fraction < 1.001): # Allowing for minor float precision issues
                raise ValueError(f"Sum of monomer mole fractions for {self.name} must be 1.0, got {total_fraction}")

    def _estimate_copolymer_tg_k(self) -> Optional[float]:
        """
        Estimates copolymer Tg using the Fox equation if applicable.
        Requires monomer Tgs and their weight fractions.
        """
        if self.polymer_type == "Homopolymer" or not self.monomers or len(self.monomers) < 2:
            return getattr(self, 'tg_polymer_k', None) # return known Tg_K or None

        # Check if all monomers have Tg_homopolymer and MW defined
        if not all(m.tg_homopolymer_c is not None and m.molecular_weight_monomer is not None for m in self.monomers):
            # print(f"Warning: Cannot estimate copolymer Tg for {self.name} due to missing monomer Tg or MW.")
            return None

        total_mw_weighted_sum = sum(m.mole_fraction * m.molecular_weight_monomer for m in self.monomers)
        if total_mw_weighted_sum == 0: return None

        sum_wi_over_Tgi = 0
        for m in self.monomers:
            weight_fraction_i = (m.mole_fraction * m.molecular_weight_monomer) / total_mw_weighted_sum
            tg_homopolymer_k_i = m.tg_homopolymer_c + 273.15
            if tg_homopolymer_k_i == 0: return None # Avoid division by zero
            sum_wi_over_Tgi += weight_fraction_i / tg_homopolymer_k_i
        
        if sum_wi_over_Tgi == 0: return None
        return 1.0 / sum_wi_over_Tgi
        

    @property
    def pdi(self) -> Optional[float]:
        if self.mw_g_per_mol and self.mn_g_per_mol and self.mn_g_per_mol > 0:
            return self.mw_g_per_mol / self.mn_g_per_mol
        return None

    def get_property(self, prop_name: str, calculate_if_missing: bool = False):
        """
        Gets a property, trying calculated properties if the direct attribute is None.
        Placeholder for future integration with descriptor_calculator.
        """
        value = getattr(self, prop_name, None)
        if value is not None:
            return value
        if calculate_if_missing and prop_name in self._calculated_properties:
            return self._calculated_properties[prop_name]
        return None

    def update_calculated_properties(self, properties: Dict[str, Any]):
        """Updates the internal dictionary of calculated properties."""
        self._calculated_properties.update(properties)

    def __str__(self):
        return f"Polymer(name='{self.name}', Type='{self.polymer_type}', Tg={self.tg_polymer_c}°C, Mn={self.mn_g_per_mol} g/mol)" \
               if self.tg_polymer_c and self.mn_g_per_mol else f"Polymer(name='{self.name}', Type='{self.polymer_type}')"