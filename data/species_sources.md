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
growth-rate + O2-evolution vigor; `lowEPS_score` = inverse of the EPS ranking above. They are
grounded in real literature but are semi-quantitative rankings. The CSV now also carries the raw
measured `mu_max_per_day` and `cell_diameter_um` alongside them (see below), so the encodings can
be replaced with harmonized measured values via the bulk trait DBs.

## Functional traits (mu_max, cell size) and the bulk-pull path

Per-species `mu_max_per_day` and `cell_diameter_um` are from strain-specific culture papers and
the Litchman/Edwards trait-compilation lineage; conditions (light, temperature, trophic mode)
differ across rows, so raw mu is not perfectly cross-comparable (flagged per row). For a
harmonized bulk pull (recommended before hard-coding these into the score):
- **BCO-DMO "Phytoplankton Traits" (Litchman/Klausmeier/Edwards, MSU), CC-BY-4.0:**
  temp optima `bco-dmo.org/dataset/544801` (temp_traits.csv); growth-rate raw series
  `bco-dmo.org/dataset/544814` (growth_rates.csv); cell biovolumes
  `bco-dmo.org/dataset/636302` (nut_traits_T3.csv).
- **Kremer et al. 2014**, *Ecology* 95:2984, "A compendium of cell and natural unit biovolumes
  for >1200 freshwater phytoplankton species" (doi:10.1890/14-0603.1; Wiley/Figshare) - the best
  freshwater biovolume source for Scenedesmus/Desmodesmus/Ankistrodesmus/Anabaena/Microcystis.

**Bulk-pull outcome (2026-07-19).** The BCO-DMO CSVs were downloaded and parsed directly. Result:
the harmonized cell BIOVOLUMES cross-validate our `cell_diameter_um` values (BCO-DMO ESD vs ours:
Ankistrodesmus 7.5/7.4, Chlorella 3.7/3.5, Scenedesmus 7.0/8, Chlamydomonas 6.0, Tetraselmis 7.7,
Dunaliella 6.3, Microcystis 5.0, Synechocystis 2.5 - all consistent). But the compilation's
GROWTH rates are strain-specific and marine-skewed (e.g. Chlorella 0.15/d from a cold strain; a
Nitzschia entry that is actually Pseudo-nitzschia; the anomalous Nannochloris 3.13/d), so they are
NOT a clean drop-in for our freshwater target strains' mu_max. Conclusion: cell sizes are now
compilation-validated; `bubble_score` stays a documented growth-vigor encoding rather than being
overwritten with mismatched cross-study growth rates. Attempting the pull was the right call; the
honest finding is that a clean measured mu_max per target strain still requires strain-specific
sources, not a genus match against a marine-focused compilation.

## Taxonomy (AlgaeBase accepted names; corrections applied)

Several requested binomials are now synonyms of different accepted names (recorded in the
`accepted_name` column): Scenedesmus dimorphus -> *Tetradesmus dimorphus*; S. obliquus ->
*Tetradesmus obliquus*; Chlorococcum littorale -> *Alvikia littoralis*; Botryococcus sudeticus ->
*Botryosphaerella sudetica* (Chlorophyceae, distinct from true *B. braunii* which is
Trebouxiophyceae); Anabaena variabilis -> *Trichormus variabilis*; Amphora coffeaeformis ->
*Halamphora coffeiformis*; Nannochloris oculata -> *Picochlorum oculatum* (a green alga, NOT the
eustigmatophyte *Nannochloropsis oculata*). Source: AlgaeBase (algaebase.org).

## Cell-wall biochemistry (predictor input; see cell_wall_features.csv)

Confirmed **algaenan** producers (aliphatic, hydrophobic wall biopolymer): *Nannochloropsis*,
*Botryococcus braunii*, and the *Scenedesmus/Tetradesmus/Desmodesmus* trilaminar-sheath complex.
Non-algaenan (glycoprotein / cellulosic / wall-less): *Chlamydomonas* (HRGP), *Tetraselmis*
(theca), *Dunaliella* (wall-less), *Chlorella vulgaris* (lacks classic TLS, Bernaerts 2022).
N/A: cyanobacteria (peptidoglycan/LPS), diatoms (silica frustule). Genomes: most greens are in
JGI PhycoCosm / NCBI (see the genome column in the genome-features research). Sources: Scholz et
al. 2014; Metzger & Largeau 2005; Voigt/Frank 2024; Hoiczyk & Hansel 2000; JGI PhycoCosm.

## PFAS physicochemistry and algae toxicity (data/pfas_physchem.csv, pfas_algae_toxicity.csv)

Physchem: MW and logKow (PubChem XLogP, a *computed* Crippen value, labeled "calc") from PubChem
PUG-REST; DTXSID/CAS cross-verified via EPA HERO/IRIS mirrors (the CompTox Dashboard is a JS SPA
and did not scrape); pKa values are ATSDR *estimates* (Toxicological Profile Table 4-2) and the
field is genuinely unsettled (PFAS acids are essentially fully dissociated at environmental pH).
Bulk pull: EPA CompTox **Batch Search** accepts a DTXSID list -> TSV/Excel (use the DTXSIDs in
`pfas_physchem.csv`); the EPA "EPAPFASRL" list bundles ~400 PFAS DTXSIDs. Toxicity: algal EC50s
from primary/ECOTOX-indexed literature; note that EPA ECOTOX covers only ~7 PFAS for algae, so
most short-chain/sulfonate/FTS compounds have no clean algal EC50 (a real, flagged gap).
