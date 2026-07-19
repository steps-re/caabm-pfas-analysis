"""
Physical constants, PFAS properties, and the measured inputs used throughout the
first-principles analysis of Ni et al. (2026), "Boosting the Removal Rate of PFAS
by Algae Through Coagulant-Assisted Algae-Bubble Matrix," Environ. Eng. Sci.,
doi:10.1177/15579018261469619.

Every value is either (a) a fundamental constant, (b) a measured value extracted
from the Ni et al. (2026) supplementary information (marked NI2026), or (c) a value
from the external literature (marked with its source). Nothing here is fitted or
invented; ranges reflect genuine measurement uncertainty.
"""

# --- Fundamental constants (SI) ---
R = 8.314           # J mol^-1 K^-1
T = 296.15          # K  (23 C, the reported room temperature; NI2026 Text S1)
N_A = 6.022e23      # mol^-1
GAS_MOLAR_VOL_L = 0.0820574 * T   # L mol^-1, ideal gas at 1 atm, 23 C

# --- PFAS: total carbon number and molar mass (g/mol) ---
# Perfluorocarboxylates (PFCAs) and perfluorosulfonates (PFSAs) used in NI2026 Table S1.
PFAS = {
    "PFBA":  dict(carbons=4,  mw=214.04, cls="carboxylate"),
    "PFPeA": dict(carbons=5,  mw=264.05, cls="carboxylate"),
    "PFHxA": dict(carbons=6,  mw=314.05, cls="carboxylate"),
    "PFHpA": dict(carbons=7,  mw=364.06, cls="carboxylate"),
    "PFOA":  dict(carbons=8,  mw=414.07, cls="carboxylate"),
    "PFNA":  dict(carbons=9,  mw=464.08, cls="carboxylate"),
    "PFDA":  dict(carbons=10, mw=514.08, cls="carboxylate"),
    "PFUnA": dict(carbons=11, mw=564.09, cls="carboxylate"),
    "PFBS":  dict(carbons=4,  mw=300.10, cls="sulfonate"),
    "PFHxS": dict(carbons=6,  mw=400.11, cls="sulfonate"),
    "PFOS":  dict(carbons=8,  mw=500.13, cls="sulfonate"),
}

# --- Air-water interfacial adsorption (Brusseau and coworkers) ---
# log10 K_ia[cm] rises ~0.46-0.56 per carbon for perfluorocarboxylates.
# Anchor: measured K_ia(PFOA, C8) = 0.00285 cm (1 mg/L; PMC9645406). At the low
# (ug/L) concentrations here, K_ia is at its constant maximum (linear regime).
KIA_SLOPE_PER_CARBON = 0.50        # central; report 0.46-0.56 as the range
KIA_SLOPE_RANGE = (0.46, 0.56)
KIA_ANCHOR_CARBON = 8
KIA_ANCHOR_CM = 0.00285            # cm, PFOA

# --- Chain-length adsorption thermodynamics (air-water) ---
DG_PER_CF2_KJ = -5.1               # kJ/mol per CF2 (Janczuk 2021; Mukerjee & Handa 1981)
DG_PER_CH2_KJ = -2.6               # kJ/mol per CH2 (reference hydrocarbon value)

# --- Air bubble surface charge ---
BUBBLE_ZETA_MV = -35.0             # neutral pH, low ionic strength (Takahashi 2005)
BUBBLE_ZETA_RANGE_MV = (-45.0, -30.0)  # pH 7 range (Yang 2001; Takahashi 2005)

# --- NI2026 measured cell surface charge (zeta, in Bold's Basal Medium, ~pH 6) ---
ZETA_CHLORELLA_MV = -24.5          # NI2026 Fig 4 / Fig S7 (pH 6.09)
ZETA_ANKISTRODESMUS_MV = -13.8     # NI2026 Fig 4 (pH 6.12)

# --- NI2026 column and feed conditions (Text S2) ---
FEED_CONC_G_PER_L = 10e-6          # 10 ug/L per individual PFAS
FEED_FLOW_L_PER_MIN = 1.5e-3       # 1.5 mL/min
RESIDENCE_MIN = 60
EQUILIBRIUM_MIN = 97               # NI2026 removal-rate reference time

# --- NI2026 cell loadings (Text S1, S3) ---
CELLS_ANKISTRODESMUS = 1.823e9     # total cells loaded (2.026e7/mL x 90 mL)
CELLS_CHLORELLA = 116.2e6 * 90     # 1.046e10 total

# --- Photosynthetic O2 evolution (BioNumbers; Lee & Palsson lineage) ---
# Per-cell net O2 evolution spans this range across species/conditions.
O2_PER_CELL_FMOL_H = (25.0, 400.0)  # fmol O2 cell^-1 h^-1

# --- Bubble geometry (assumption; photosynthetic O2 bubbles) ---
BUBBLE_RADIUS_M = (5e-5, 5e-4)      # 0.05-0.5 mm

# --- Water surface tension ---
GAMMA_AW = 0.0728                   # N/m at 20-23 C
