```
ASDScreener/
├── asdscreener/               # Main library source code package
│   ├── __init__.py            # Makes the directory a Python package
│   ├── data/                  # Default data files (e.g., polymer database, pre-trained models)
│   │   ├── polymer_database.csv
│   │   └── ml_models/
│   │       └── chi_predictor_rf.pkl
│   ├── core/                  # Core modules renamed for clarity
│   │   ├── __init__.py
│   │   ├── api_properties.py
│   │   ├── polymer_properties.py
│   │   └── system_definition.py # Handles API-Polymer pairing and drug loads
│   ├── calculators/           # Modules for calculations and estimations
│   │   ├── __init__.py
│   │   ├── descriptor_calculator.py
│   │   ├── thermodynamics_calculator.py
│   │   ├── glass_transition_calculator.py
│   │   └── group_contribution_methods.py # (Potentially complex module)
│   ├── predictors/              # Modules for predictive modeling
│   │   ├── __init__.py
│   │   ├── stability_predictor.py
│   │   └── ml_model_interface.py
│   ├── reporting/               # Module for generating reports
│   │   ├── __init__.py
│   │   ├── report_generator.py
│   │   └── templates/           # Report templates (e.g., Jinja2 templates for HTML/Markdown)
│   │       └── default_report_template.md
│   └── utils/                 # Utility functions (e.g., file I/O, plotting helpers)
│       ├── __init__.py
│       └── helpers.py
│
├── docs/                      # Documentation
│   ├── conf.py                # Sphinx configuration file
│   ├── index.rst              # Main documentation page (or .md if using MyST)
│   ├── installation.rst
│   ├── usage.rst
│   ├── api_reference/         # Auto-generated API documentation
│   │   └── ...
│   ├── tutorials/             # More in-depth tutorials (could link to notebooks)
│   └── _static/               # Static files (CSS, images for docs)
│   └── _templates/            # Sphinx templates
│
├── examples/                  # Example scripts showing how to use the library
│   └── run_screening_example.py
│
├── notebooks/                 # Jupyter notebooks (as outlined previously)
│   ├── 00_ASD_Series_Introduction.ipynb
│   ├── 01_BCS_and_Solubility_Enhancement.ipynb
│   ├── 02_ASD_Thermodynamics_Miscibility_Solubility.ipynb
│   ├── 03_ASD_Glass_Transition_Mobility.ipynb
│   ├── 04_ASD_Characterization_Amorphousness_Interactions.ipynb
│   ├── 05_ASD_Recrystallization_Kinetics_Stability.ipynb
│   ├── 06_ASD_Manufacturing_Dissolution.ipynb
│   └── data/                  # Data specific to notebooks (if any, e.g., sample CSVs)
│       └── hypothetical_api_data.csv
│
├── tests/                     # Unit and integration tests
│   ├── __init__.py
│   ├── test_descriptor_calculator.py
│   ├── test_thermodynamics_calculator.py
│   ├── test_glass_transition_calculator.py
│   ├── test_stability_predictor.py
│   ├── test_report_generator.py
│   └── fixtures/              # Test fixtures or sample data for tests
│       └── sample_api_for_test.json
│
├── .gitignore                 # Specifies intentionally untracked files
├── LICENSE                    # License file (e.g., MIT, Apache 2.0)
├── MANIFEST.in                # For specifying files to include in source distributions
├── pyproject.toml             # Build system requirements & package metadata (PEP 517/518)
├── README.md                  # Project overview, installation, quick start
├── requirements.txt           # Core dependencies for running the library
├── requirements-dev.txt       # Dependencies for development (testing, linting, docs)
└── setup.py                   # (Optional, if not fully using pyproject.toml for packaging)
```

---

**Explanation of Key Directories and Files:**

*   **`ASDScreener/` (Root Directory):**
    *   Contains the entire project.

*   **`asdscreener/` (Package Directory):**
    *   This is where the actual Python source code of your library resides. The name should be the import name (e.g., `import asdscreener`).
    *   **`__init__.py`**: Makes this directory a Python package. It can also be used to expose key functions/classes at the package level (e.g., `from .core.api_properties import API`).
    *   **`data/`**: For default data files bundled with the library.
        *   `polymer_database.csv`: A CSV file containing properties of common pharmaceutical polymers.
        *   `ml_models/`: Directory to store serialized pre-trained machine learning models.
    *   **`core/`**: Fundamental classes for representing APIs, Polymers, and the ASD System being evaluated.
    *   **`calculators/`**: Modules responsible for performing specific calculations (thermodynamics, $T_g$, descriptors).
        *   `group_contribution_methods.py`: This could become quite complex, potentially broken down further if many GCMs are implemented.
    *   **`predictors/`**: Modules for stability predictions and interfacing with ML models.
    *   **`reporting/`**: Code for generating output reports.
        *   `templates/`: Stores report templates (e.g., Markdown or HTML templates using Jinja2).
    *   **`utils/`**: Helper functions, plotting utilities, file I/O operations that are used across different modules.

*   **`docs/`:**
    *   All documentation files. Sphinx is a common tool for generating Python project documentation.
    *   `conf.py`: Sphinx configuration.
    *   `.rst` or `.md` files: Source files for documentation pages.
    *   `api_reference/`: Often auto-generated from docstrings in your source code by Sphinx.

*   **`examples/`:**
    *   Simple Python scripts demonstrating common use cases of the library. These help users get started quickly.

*   **`notebooks/`:**
    *   The Jupyter notebooks as we've been outlining. These serve as interactive tutorials and case studies.
    *   `data/` (inside `notebooks`): For any data files specifically required by the notebooks that are not part of the core library data.

*   **`tests/`:**
    *   Contains all test code. Using a test runner like `pytest` is highly recommended.
    *   `test_*.py`: Test files for each module in your `asdscreener` package.
    *   `fixtures/`: Data or pre-configured objects used specifically for testing.

*   **Root Files:**
    *   **`.gitignore`**: Specifies files and directories that Git should ignore (e.g., `__pycache__/`, `*.pyc`, virtual environment folders, build artifacts).
    *   **`LICENSE`**: Contains the license under which the software is released (e.g., MIT, Apache 2.0, GPL).
    *   **`MANIFEST.in`**: Used by `setuptools` to specify which non-code files (like data files in `asdscreener/data/`) should be included when creating a source distribution (`sdist`).
    *   **`pyproject.toml`**: The modern standard for specifying build system requirements (PEP 518) and package metadata (PEP 621). Tools like `Poetry`, `Flit`, or `setuptools` (with build backend) use this.
    *   **`README.md`**: The front page of your project. Should include:
        *   Project title and brief description.
        *   Installation instructions.
        *   A quick start example.
        *   Link to documentation.
        *   How to contribute (if applicable).
        *   License information.
    *   **`requirements.txt`**: Lists the core Python packages required to run your library. Can be generated from `pyproject.toml` or maintained separately for `pip install -r requirements.txt`.
    *   **`requirements-dev.txt`**: Lists packages needed for development, such as `pytest`, `flake8`, `black`, `sphinx`.
    *   **`setup.py`**: Traditionally used for packaging with `setuptools`. With `pyproject.toml`, its role is reduced or can be minimal if the build backend handles everything. If you use `Poetry` or `Flit`, you might not have a `setup.py` at all.

This structure provides a good separation of concerns and follows common best practices in Python software development. It will make the `ASDScreener` library easier to develop, test, document, and distribute.