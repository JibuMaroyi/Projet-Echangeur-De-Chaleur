# Heat Exchanger Design Tool

A desktop application for the **thermal and hydraulic sizing of shell-and-tube heat exchangers**, built with Python and PyQt5.

> This tool automates the engineering calculations required to determine the main design parameters of an industrial heat exchanger — from fluid selection to cost estimation.

---

## Features

- Graphical user interface (PyQt5) with step-by-step wizard
- Automatic retrieval of thermophysical properties via **CoolProp**
- Support for **Air**, **Water**, and **Lubricating oil** as working fluids
- NTU-effectiveness method for 1-pass and 2-pass configurations
- Tube bundle geometry calculation (number of tubes, shell diameter, baffle spacing)
- Convective heat transfer coefficients (tube-side & shell-side)
- Overall heat transfer coefficient validation (convergence check ≤ 30%)
- Pressure drop estimation (tube-side & shell-side)
- Cost estimation based on heat transfer surface area
- Export results to **PDF** and **TXT**

--- 

## Project Structure

```
Projet-Echangeur-De-Chaleur/
├── main.py                  # Application entry point (PyQt5 GUI)
├── modules/
│   ├── fluids.py            # Fluid selection & thermophysical properties (CoolProp)
│   └── calculations.py      # Engineering calculations (NTU, heat transfer, pressure drop)
├── config/                  # Font configuration files for PDF export
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Prerequisites

- **Python 3.12** (tested with 3.12.3)

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/JibuMaroyi/Echangeur-De-Chaleur.git
cd Projet-Echangeur-De-Chaleur
```

2. **Create a virtual environment**

```bash
python -m venv .venv
```

3. **Activate the virtual environment**

- Windows:
  ```bash
  .venv\Scripts\activate
  ```
- macOS / Linux:
  ```bash
  source .venv/bin/activate
  ```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py
```

The application opens a graphical interface that guides you through the following steps:

1. **Fluid selection** — Choose hot and cold fluids
2. **Operating conditions** — Enter temperatures, pressures, and flow rates
3. **Thermophysical properties** — Automatically computed or manually entered (oil)
4. **Thermal performance** — NTU, effectiveness, and required heat transfer surface
5. **Tube geometry** — Define tube dimensions and layout
6. **Heat transfer coefficients** — Tube-side and shell-side calculations
7. **Validation** — Compare assumed vs. calculated overall coefficient
8. **Pressure drops** — Shell-side and tube-side hydraulic losses
9. **Cost estimation & synthesis** — Final summary with export options

---

## Calculation Method

The program follows the classical **NTU-effectiveness method** for shell-and-tube heat exchanger design:

| Step | Description |
|------|-------------|
| Heat capacity rates | $C_{h} = \dot{m}_{h} \cdot c_{p,h}$ and $C_{c} = \dot{m}_{c} \cdot c_{p,c}$ |
| Effectiveness | $\varepsilon = \frac{Q}{Q_{max}}$ |
| NTU | Number of Transfer Units for 1-pass or 2-pass configuration |
| Surface area | $S_0 = \frac{NTU \cdot C_{min}}{U_0}$ |
| Cost | $\text{Cost} = 2143 \times S^{0.514}$ (USD) |

---

## Example Output

| Parameter | Value |
|-----------|-------|
| Heat transfer surface area | 52.13 m² |
| Overall heat transfer coefficient | 123.89 W/m²·K |
| Shell-side pressure drop | 21 479 Pa |
| Tube-side pressure drop | 0.446 Pa |
| Estimated cost | 16 352 USD |

---

## Technologies

| Technology | Role |
|------------|------|
| **Python 3.12** | Core language |
| **PyQt5** | Desktop GUI framework |
| **CoolProp** | Thermophysical property library |
| **NumPy** | Numerical computations |
| **fpdf2** | PDF report generation |

---

## Credits

### Jonathan Maroyi
**Mechanical Engineer (Bac+5)** – Faculty of Engineering, University of Kinshasa  

Developed the **engineering methodology and thermodynamic modeling** for this tool as part of his **final-year thesis on shell-and-tube heat exchanger design**.

Key contributions:
- Definition of the **thermal sizing methodology**
- Formulation of **heat transfer and fluid mechanics models**
- Development of the **dimensioning workflow** (NTU-effectiveness method)
- Validation of the engineering calculations and design assumptions


### Benjamin Maroyi
**Software Engineer – Python Developer**

Designed and implemented the **software architecture and computational tool**.

Key contributions:
- Implementation of the **engineering models in Python**
- Development of the **modular calculation backend**
- Integration of **CoolProp** for thermophysical properties
- Development of the **PyQt5 graphical interface**
- Implementation of **result export and reporting features**