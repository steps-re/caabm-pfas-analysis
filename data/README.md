# Data provenance

All experimental values below were extracted from the machine-readable supplementary
information of Ni et al. (2026), *Environmental Engineering Science*,
doi:10.1177/15579018261469619. The original supplementary files are **not**
redistributed here; only the specific numeric values used in the analysis are
reported, with per-row source attribution, as is standard for a citing work.

| File | Contents | Source |
|---|---|---|
| `ni2026_removal.csv` | PFBA/PFOA removal % by species, support media, and coagulant treatment | Ni et al. 2026, Figs. 3, 5, 6 |
| `ni2026_zeta.csv` | Cell zeta potential vs pH, in Bold's Basal Medium, for both species | Ni et al. 2026, Fig. 4 |
| `ni2026_toc.csv` | Effluent total organic carbon vs culturing day (EPS leaching proxy) | Ni et al. 2026, Fig. 4 / S7b |
| `ni2026_literature_comparison.csv` | Prior algal PFAS-removal results (extent, time, normalized rate) used for the enhancement-factor comparison | Ni et al. 2026, Fig. 6, and the primary sources cited therein |
| `species_candidates.csv` | Cross-species surface properties for the selection screen | mixed literature (per-row `source` column) |
| `pfas_properties.csv` | Carbon number, molar mass, K_ia, surface excess Γ per PFAS | **generated** by `code/interfacial_adsorption.py` |

## Confidence flags

- `ni2026_*` values are read directly from the authors' SI data tables (high confidence).
- `species_candidates.csv`: `zeta_mV` and `contact_angle_deg` are literature measurements
  (see `source`); blank cells are genuine gaps ("no data found"), left blank rather than
  estimated. The columns **`bubble_score`** and **`lowEPS_score`** are coarse 0–1 encodings
  of qualitative literature (growth rate, EPS tendency), **not measured values** — they are
  inputs to the screen's lower-weighted terms and should be replaced with measurements as
  they become available.
- The single largest measurement gap is cell-surface hydrophobicity (contact angle),
  available for only a few species. Acquiring Ozkan & Berberoglu (2013),
  *Colloids Surf. B* 112:287 and 112:302, is the highest-value next step.

Full bibliographic detail with verified DOIs is in `../references.bib`.
