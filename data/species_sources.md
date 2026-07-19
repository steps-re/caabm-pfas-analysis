# Species-screen data provenance

Sources for the values in `species_candidates.csv`. Compiled 2026-07-19 from a targeted
literature sweep. Confidence is flagged per source. Nothing was invented; blank cells in the
CSV mean "no data found" after a real search, not zero.

## The key dataset — ACQUIRED (was the top flagged gap)

**Ozkan A, Berberoglu H (2013)** — *Colloids Surf. B* 112:287 (doi:10.1016/j.colsurfb.2013.08.001)
and 112:302 (doi:10.1016/j.colsurfb.2013.08.007) — measured zeta **and** hydrophobicity (contact
angles, van Oss surface-energy components, free energy of cohesion ΔG_coh) for ~12 microalgae
under one consistent method. **The published papers are fully paywalled (Elsevier, no OA copy).
BUT the source tables were recovered with HIGH confidence from first author Altan Ozkan's
open-access PhD dissertation**, which the papers derive from:

> Ozkan, A. *Development of a novel algae biofilm photobioreactor for biofuel production.* Ph.D.
> dissertation, University of Texas at Austin, 2012 (advisor H. Berberoglu). Handle
> 2152/ETD-UT-2012-08-6224. Table 5.2 (surface properties) and Table 5.1 (morphology).

Values transcribed verbatim from that PDF now populate 10 species in the CSV (all `high`
confidence): Ankistrodesmus falcatus, Chlorella vulgaris, Nannochloris oculata (green alga),
Scenedesmus dimorphus, Amphora coffeaeformis, Botryococcus braunii, Botryococcus sudeticus,
Cylindrotheca fusiformis, Nitzschia frustulum. The 12th published species (a 2nd cyanobacterium)
was not recoverable. Synechococcus sp. ATCC 27184 came second-hand via Yang et al. 2023 (medium).

**Load-bearing caveat — zeta measured in NATIVE growth medium, not a common buffer:** freshwater
species in BG-11 (pH 7.42, ionic strength 21 mM); saltwater species (the 3 diatoms + Nannochloris
sp. UTEX LB1999) in ASP-M (pH 7.53, IS 584 mM). The ~28x higher saltwater ionic strength
compresses the double layer, so **saltwater zeta magnitudes run ~15% smaller and are NOT directly
comparable to the freshwater greens.** Diatoms are flagged accordingly in the CSV. The one
remaining check for a formal repo: confirm the dissertation numbers equal the published-paper
numbers (expected, but the paper is paywalled). Hydrophobicity metric ΔG_coh: more negative = more
hydrophobic; ΔG < 0 = hydrophobic. Botryococcus braunii is decisively most hydrophobic
(ΔG_coh −103.3, θ_w 112.3°).

## Surface charge (zeta) and hydrophobicity (contact angle)

- Matho C et al. 2019, *Algal Research* 44:101705, doi:10.1016/j.algal.2019.101705 — *Chlorella
  vulgaris* zeta (-22.4 mV DI / -30.1 mV growth medium) + flotation. **High** (read from author OA copy).
- Xia L et al. 2017, *R. Soc. Open Sci.* 4:170867, doi:10.1098/rsos.170867 — *Chlorella* sp.
  XJ-445 zeta -22.1 mV + coag-flotation up to 98.7%. **High** (OA PMC).
- Xia et al. 2017, *PLOS ONE*, doi:10.1371/journal.pone.0186434 — growth-phase contact angles
  for *Botryococcus* (28.7-75.3 deg), *Chlorella* XJ-445 (21.6-33.8), *Desmodesmus* (30.1-38.8). **High** (OA).
- Zhu R et al. 2023, *Front. Microbiol.*, doi:10.3389/fmicb.2023.1285229 — *Microcystis* zeta +
  van Oss surface energy (θw 22-32 deg); also reproduces Ozkan's *Synechococcus* (-32.2 mV, 64 deg)
  and *Anabaena variabilis* (-16.8 mV, 114 deg). **High** for own data; **Medium** for reproduced Ozkan values.
- Gerde et al. 2014 (via Gojkovic et al. 2025, *Physiol. Plant.* doi:10.1111/ppl.70366) —
  *Chlamydomonas* -19.95 mV, *Scenedesmus* -20.6 mV. **Medium** (second-hand table).
- Hadjoudja et al. 2010, *J. Colloid Interface Sci.* — *Chlorella vulgaris* / *Microcystis* zeta
  vs pH; IEPs ~pH 2.2-2.9. **Medium** (abstract synthesis).
- Garg & Schenk 2012 (*Bioresour. Technol.* 121:471, doi:10.1016/j.biortech.2012.06.111) and 2014
  (159:437, doi:10.1016/j.biortech.2014.03.030) — *Tetraselmis* flotation driven by hydrophobicity
  (6.4% -> 81.7% with cationic collector). **Medium** (recovery figures not independently re-verified).
- Ankistrodesmus falcatus zeta = **-13.8 mV from Ni et al. 2026 SI (High)**; one secondary report
  of positive charge could not be verified (Low, noted in CSV).

## Growth, O2 evolution, availability, toxin status

- Culture-collection strain numbers: UTEX (utex.org), CCAP (ccap.ac.uk), NIES (mcc.nies.go.jp),
  NCMA (ncma.bigelow.org) catalogs. **High** where a direct catalog page was found.
- *C. sorokiniana* O2 114 umol/mgChl/h: PMC3210360. *Synechocystis* O2 270-400: PMC4571542.
  *Nannochloropsis oculata* O2 182 (bicarbonate): OA study. Per-cell O2 25-400 fmol/cell/h:
  BioNumbers BNID 107311 (Lee & Palsson 1994).
- GRAS: *C. vulgaris* GRN 396/986; *D. salina* PMC6717104; *Arthrospira* (US+EU). **High**.
- Toxin: *Microcystis* toxic strains (UTEX LB2385/CCAP 1450/6) vs non-toxic (UTEX LB2386/NIES-44);
  microcystin inversely related to growth rate. **High**. Cyanobacteria (Anabaena, Synechococcus,
  Synechocystis) carry genus/handling toxin-and-regulatory concern for water use and are flagged.

## EPS (low = better) and PFAS-uptake cross-check

- EPS ranking (low->high): Nannochloropsis (low) < Chlorella spp. < Chlamydomonas < Tetraselmis <
  Scenedesmus/Desmodesmus (self-flocculating) < Ankistrodesmus (autoflocculating) < Microcystis <
  Dunaliella < Botryococcus (very high, up to 5 g/L). Sources: Ciempiel 2022 (Molecules 27:7153),
  Zhao 2023 (Chemosphere 323:138256), Foods 2022 11:110 (Botryococcus), *Microcystis* bloom-EPS lit.
  **Medium** overall (few clean mg/g values; several are flocculation-phenotype proxies).
- PFAS-uptake cross-check (NOT the flotation mechanism, weak validation only): *Scenedesmus
  quadricauda* 58.2% PFOA removal (Ha 2025, J. Hazard. Mater. 488:137508); *Chlorella* sp. PFOS
  BCF ~200 (Mao 2023, STOTEN 870); *Synechocystis* 88% PFOS (Marchetto 2021, Life 11:1300).
  Note: PFAS uptake tracks lipid/protein partitioning, not EPS-charge, so it does not predict
  the CAABM flotation performance.

## bubble_score and lowEPS_score encodings

These two CSV columns are 0-1 encodings, NOT measured values: `bubble_score` = normalized
growth-rate + O2-evolution vigor (from the availability/O2 dataset); `lowEPS_score` = inverse of
the EPS ranking above. They are grounded in real literature but are semi-quantitative rankings,
and should be replaced with direct measurements as they become available.
