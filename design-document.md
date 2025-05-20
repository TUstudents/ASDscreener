Okay, let's draft a Design Document for the `ASDScreener` Python library. This document will outline the purpose, scope, architecture, and key design decisions for the project.

---

## `ASDScreener` - Design Document

**Version:** 0.1
**Date:** October 26, 2023
**Author(s):** AI Assistant / Project Lead

---

### 1. Introduction and Purpose

**1.1. Problem Statement:**
The development of Amorphous Solid Dispersions (ASDs) is a critical strategy for enhancing the bioavailability of poorly soluble drugs. However, the selection of suitable API-polymer combinations and optimal drug loads is a complex, resource-intensive process involving extensive experimentation. There is a need for computational tools that can aid in the early-stage screening of potential ASD systems by predicting key properties related to miscibility, stability, and processability.

**1.2. Proposed Solution: `ASDScreener` Library**
`ASDScreener` will be a Python library designed to provide a systematic, data-driven approach to evaluating and ranking potential API-polymer ASD systems. It will integrate physicochemical calculations, established thermodynamic models, empirical rules, and (eventually) machine learning predictions to generate comprehensive reports. These reports will assist pharmaceutical scientists in making informed decisions, prioritizing experiments, and accelerating the ASD formulation development pipeline.

**1.3. Goals of the Library:**
*   Provide a standardized framework for inputting API and polymer properties.
*   Estimate key thermodynamic parameters indicative of miscibility (e.g., $\chi$, $\Delta G_{mix}$, solubility parameters).
*   Predict the glass transition temperature ($T_g$) of ASD mixtures and the impact of plasticizers.
*   Offer a qualitative and (where feasible) semi-quantitative assessment of physical stability against recrystallization and AAPS.
*   Incorporate pre-trained machine learning models for relevant predictions (future scope).
*   Generate clear, actionable reports summarizing the analysis for specific API-polymer pairs across various drug loads.
*   Be modular and extensible to allow for the incorporation of new models and data.

**1.4. Target Users:**
*   Pharmaceutical formulation scientists.
*   Material scientists working on drug delivery.
*   Researchers in academia and industry involved in ASD development.
*   Students in pharmaceutical sciences and chemical/materials engineering.

---

### 2. Scope and Features

**2.1. In Scope:**
*   **Input:** Handling of API and polymer physicochemical properties (user-provided or estimated). Support for standard polymer grades and user-defined polymers.
*   **Descriptor Calculation:** Basic molecular descriptors from SMILES (MW, LogP, H-bond D/A, PSA). Estimation of solubility parameters and API $T_g$ via group contribution methods (GCMs) if not provided.
*   **Thermodynamic Analysis:**
    *   Hansen Solubility Parameter ($R_a$) and Hildebrand difference calculations.
    *   Estimation of Flory-Huggins $\chi$ (via HSPs or simple models; ML in future).
    *   Calculation and visualization of $\Delta G_{mix}/RT$ vs. composition.
    *   Estimation of crystalline API solubility in polymer ($S_p^{cry}$) (simplified models).
*   **Glass Transition Analysis:**
    *   Prediction of $T_{g,ASD}$ using Gordon-Taylor and Couchman-Karasz equations.
    *   Estimation of plasticized $T_{g,ASD}$ due to water uptake (simplified).
*   **Stability Assessment (Qualitative/Empirical):**
    *   $T_g - T_{storage}$ margin calculation.
    *   Rule-based risk flagging (e.g., high drug load vs. $S_p^{cry}$, poor miscibility indicators, high API crystallization tendency based on $T_g/T_m$).
    *   A qualitative stability score/ranking for API-polymer pairs.
*   **Reporting:** Generation of Markdown/HTML reports summarizing inputs, analyses, predictions, risk flags, and suggestive guidance for experimentation.
*   **Modularity:** Core calculations and predictions organized into logical modules.
*   **Documentation:** User guides, API reference, example notebooks.
*   **Testing:** Unit tests for core functionalities.

**2.2. Out of Scope (for initial version, potential future enhancements):**
*   **Advanced QM/MD Simulations:** The library will *not* perform these directly but could potentially interface with their outputs or use parameters derived from them.
*   **Training of New ML Models:** The library will initially focus on *using* pre-trained models. Training infrastructure is a separate project.
*   **Sophisticated Group Contribution Methods:** Implementation of complex GCMs for all properties from scratch is a major undertaking. Initially, rely on simpler GCMs or expect users to provide more input data.
*   **Detailed Kinetic Modeling of Crystallization from First Principles:** Shelf-life predictions will be conceptual or based on simplified Arrhenius extrapolations of *hypothetical* rate constants.
*   **Full Phase Diagram Construction:** Will focus on miscibility indicators rather than full binodal/spinodal calculations, unless simplified models can be readily implemented.
*   **Graphical User Interface (GUI):** Initial version will be a Python library callable from scripts or Jupyter notebooks.
*   **Extensive Polymer Database Curation:** Will start with a limited set of common polymers; users can add more.
*   **Chemical Stability Prediction.**

---

### 3. System Architecture and Design

**3.1. Overall Architecture:**
The library will follow a modular architecture, as outlined in the directory structure document.
*   **Core Data Structures:** Python classes for `API`, `Polymer`, and `ASDSystem` (representing an API-polymer-drug load combination).
*   **Calculation Modules:** Separate modules for `descriptor_calculator`, `thermodynamics_calculator`, `glass_transition_calculator`.
*   **Prediction Modules:** `stability_predictor`, `ml_model_interface`.
*   **Reporting Module:** `report_generator` utilizing templates.
*   **Data Module:** To store default polymer data and pre-trained models.

**3.2. Key Data Flow:**
1.  User instantiates `API` and `Polymer` objects (or loads polymers from library database).
2.  User creates `ASDSystem` objects for desired API-polymer pairs and drug loads.
3.  `descriptor_calculator` is called to populate missing API/polymer descriptors if SMILES are provided.
4.  The `ASDSystem` object (or a dedicated `AnalysisEngine`) calls methods from the calculator and predictor modules.
5.  Results are stored within the `ASDSystem` object or a dedicated results object.
6.  `report_generator` takes the results object(s) to produce the output report.

**3.3. Design Principles:**
*   **Object-Oriented Design:** Using classes to represent key entities and their properties/methods.
*   **Separation of Concerns:** Modules have distinct responsibilities.
*   **Configuration:** Allow some level of configuration (e.g., thresholds for risk flagging, choice of $T_g$ prediction model).
*   **Error Handling:** Implement robust error handling for invalid inputs or calculation failures.
*   **Logging:** Incorporate logging for debugging and tracking execution.

**3.4. Technology Stack:**
*   **Language:** Python (3.8+)
*   **Core Libraries:** NumPy, SciPy, Pandas, Matplotlib.
*   **Chemoinformatics:** RDKit.
*   **Machine Learning (Future):** Scikit-learn, XGBoost, etc.
*   **Reporting:** Jinja2 (for templating), Markdown.
*   **Testing:** Pytest.
*   **Documentation:** Sphinx.
*   **Packaging:** `pyproject.toml` with `setuptools` or `poetry`/`flit`.

---

### 4. Module Design Details (High-Level)

**4.1. `asdscreener.core`:**
    *   `api_properties.API`: Class to store and manage API data. Methods for basic property validation.
    *   `polymer_properties.Polymer`: Class for polymer data, including monomer info, MW, $T_g$, HSPs, degree of modification. Methods for estimating copolymer properties from monomer data (e.g., Fox eq for $T_g$).
    *   `system_definition.ASDSystem`: Represents a specific API-polymer-drug load combination. Stores calculated/predicted results for this system.

**4.2. `asdscreener.calculators`:**
    *   `descriptor_calculator.DescriptorCalculator`:
        *   `calculate_from_smiles(smiles)`: Returns dict of RDKit descriptors.
        *   `estimate_hsp_gcm(smiles_or_fragments)`: Returns estimated HSPs.
        *   `estimate_tg_api_gcm(smiles)`: Returns estimated API $T_g$.
    *   `thermodynamics_calculator.ThermoCalculator`:
        *   `calculate_hansen_Ra(api_obj, polymer_obj)`
        *   `estimate_chi(api_obj, polymer_obj, method='hsp_based'/'ml')`
        *   `calculate_delta_g_mix(asd_system_obj, chi_value)`
        *   `estimate_Sp_cry(asd_system_obj, chi_value)`
    *   `glass_transition_calculator.TgCalculator`:
        *   `predict_tg_gordon_taylor(asd_system_obj, k_GT=None)`
        *   `predict_tg_couchman_karasz(asd_system_obj)`
        *   `predict_tg_plasticized(asd_system_obj, water_uptake_percent, k_GT_water)`
    *   `group_contribution_methods.GCM`: (Placeholder for various GCM implementations or interfaces).

**4.3. `asdscreener.predictors`:**
    *   `stability_predictor.StabilityPredictor`:
        *   `assess_Tg_margin(asd_system_obj, storage_T)`
        *   `assess_crystallization_risk_rules(asd_system_obj)`
        *   `calculate_qualitative_stability_score(asd_system_obj)`
    *   `ml_model_interface.MLModel`: Base class for ML models.
        *   `load_model(filepath)`
        *   `predict(input_features)`
        *   `check_applicability_domain(input_features)`

**4.4. `asdscreener.reporting`:**
    *   `report_generator.ReportGenerator`:
        *   `generate_api_polymer_report(list_of_asd_systems, template_path, output_path)`

**4.5. `asdscreener.data`:**
    *   Contains `polymer_database.csv` with columns like: `Name`, `Type`, `Tg_C`, `Density_g_cm3`, `Mn_kDa`, `delta_d`, `delta_p`, `delta_h`, `Monomer1_SMILES`, `Monomer1_MolFrac`, `DegreeHydrolysis`, etc.
    *   Subdirectory `ml_models/` for serialized model files.

---

### 5. Data Management

*   **Internal Polymer Database:** A CSV file shipped with the library, easily updatable. Pandas will be used to read and query this.
*   **User-Provided Data:** Users can instantiate `API` and `Polymer` objects directly with known properties.
*   **Pre-trained ML Models:** Will be serialized (e.g., pickle, joblib) and stored in the `asdscreener/data/ml_models` directory.
*   **Output Reports:** Generated in user-specified formats (Markdown initially, then HTML/PDF).

---

### 6. Error Handling and Logging

*   **Error Handling:** Graceful handling of missing input data (e.g., attempting estimation if possible, otherwise raising informative errors). Validation of input types and ranges.
*   **Logging:** Use the standard Python `logging` module. Different log levels (DEBUG, INFO, WARNING, ERROR) to provide insights into calculations and potential issues. Users can configure the logging level.

---

### 7. Testing Strategy

*   **Unit Tests:** Each module and significant function will have unit tests using `pytest`. Focus on testing:
    *   Correctness of calculations with known inputs/outputs.
    *   Handling of edge cases and invalid inputs.
    *   Functionality of `API`, `Polymer`, `ASDSystem` classes.
*   **Integration Tests:** Testing the interaction between modules (e.g., data flow from descriptor calculation to thermodynamic analysis to report generation).
*   **Data Validation Tests:** Tests to ensure the integrity of the internal polymer database.
*   **Fixtures:** Use `pytest` fixtures for setting up common test data (e.g., sample API and polymer objects).

---

### 8. Documentation Plan

*   **User Documentation (Sphinx):**
    *   Installation guide.
    *   Quick start tutorial.
    *   Detailed usage guide for each module/functionality.
    *   Explanation of input parameters and output reports.
    *   Methodologies behind calculations and predictions (with references).
    *   How to contribute or extend the library.
*   **API Reference (Sphinx Autodoc):** Auto-generated from docstrings in the source code.
*   **Jupyter Notebooks (Examples/Tutorials):** The series of notebooks will serve as extended, interactive tutorials.
*   **README.md:** Overview, installation, basic usage.

---

### 9. Deployment and Distribution

*   Packaging using `pyproject.toml` (and `setuptools` or similar build backend).
*   Distribution via PyPI (`pip install asdscreener`).
*   Source code hosted on a public repository (e.g., GitHub).

---

### 10. Risks and Mitigation

*   **Accuracy of GCMs/Empirical Models:**
    *   *Risk:* Predictions may have significant errors.
    *   *Mitigation:* Clearly state assumptions and limitations. Validate against experimental data where possible. Provide options for users to input more accurate data if known.
*   **Complexity of Polymer Chemistry:**
    *   *Risk:* Oversimplification of copolymer behavior or effects of modifications.
    *   *Mitigation:* Modular design to allow for future refinement. Focus on well-characterized polymers initially. Allow detailed user input for polymer properties.
*   **ML Model Generalizability:**
    *   *Risk:* Pre-trained ML models may not perform well on new/diverse chemical spaces.
    *   *Mitigation:* Implement Applicability Domain checks. Encourage retraining/fine-tuning with user data (future scope).
*   **Maintenance of Polymer Database:**
    *   *Risk:* Database becomes outdated or contains errors.
    *   *Mitigation:* Provide clear contribution guidelines. Version control the database.
*   **Scope Creep:**
    *   *Risk:* Trying to implement too many advanced features in the initial version.
    *   *Mitigation:* Stick to the defined "In Scope" features for v0.1/v1.0. Plan future enhancements iteratively.

---

### 11. Future Considerations

*   Integration of more sophisticated thermodynamic models (e.g., direct PC-SAFT calculations if a Python interface exists or can be wrapped).
*   Advanced kinetic stability models.
*   More comprehensive GCM implementations.
*   Tools for users to train/retrain ML models with their own data.
*   GUI development.
*   Database integration for fetching API/polymer properties.

---

This design document provides a roadmap for developing `ASDScreener`. It will be a living document, updated as the project progresses and new insights are gained.