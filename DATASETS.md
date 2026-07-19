# Biological & chemical datasets for the algae-PFAS screen and future modeling

A curated catalog of real, accessible datasets, what each contains, and the modeling it
feeds. Compiled 2026-07. Entries used in this repo are marked **[in use]**.

## 1. Microalgae traits, taxonomy, availability (the screen's inputs)

| Dataset | What it gives | Access | Feeds |
|---|---|---|---|
| **AlgaeBase** (algaebase.org) | Accepted names, synonyms, classification for all algae | Web (no bulk API) | Taxonomy resolution (e.g. *Nannochloris* green vs *Nannochloropsis* eustigmatophyte) |
| **Culture collections** — UTEX, CCAP, NIES, NCMA/Bigelow, SAG, ATCC | Strain availability, media, temperature, origin | Web catalogs; NIES has structured metadata | Availability axis; strain provenance **[in use]** |
| **Phytoplankton functional-trait compilations** — Litchman & Klausmeier 2008; Edwards, Thomas, Klausmeier & Litchman 2015/2016; Kremer et al. 2017 | Measured growth rate, cell size, thermal & light traits across 100s of species, with public supplementary datasets | Journal SI (Ecology, Limnol. Oceanogr.) | Replaces hand-encoded `bubble_score` with measured growth/size traits |
| **BioNumbers** (bionumbers.hms.harvard.edu) | Quantitative biology numbers incl. algal O2 rate, doubling time | Web + BNID | O2/physiology values **[in use]** |
| **Nordic Microalgae** (nordicmicroalgae.org) | Morphology, imagery, size | Web | Cell size/shape |
| **BacDive** (DSMZ) | Structured strain-phenotype DB (bacteria) | API + bulk | Schema model for a future structured algal-trait DB |

## 2. Genomes & cell-wall/EPS biochemistry (the surface-property predictor's inputs)

Cell-surface hydrophobicity and EPS are set largely by cell-wall composition. Predicting them
from the genome lets the screen rank species never physically measured.

| Dataset | What it gives | Feeds |
|---|---|---|
| **JGI PhycoCosm** (phycocosm.jgi.doe.gov) | Algal genomes + annotations | Cell-wall & EPS biosynthesis gene features |
| **Phytozome / Ensembl Protists / NCBI Genome** | Green-algal & broader genomes/assemblies | Same |
| **CAZy** (cazy.org) | Carbohydrate-active enzyme families per genome | EPS/wall biosynthesis machinery |
| Primary lit on **algaenan** (resistant aliphatic biopolymer) | Which taxa have algaenan walls (Nannochloropsis, Botryococcus, some Chlorella/Scenedesmus, Tetraedron) | The single strongest genomic/biochemical proxy for cell-surface hydrophobicity |

**Modeling exercise (this repo):** label = measured contact angle/zeta; features = cell-wall type
+ algaenan presence + class + cell size; interpretable model maps biochemistry -> hydrophobicity,
extended to unmeasured species. See `code/surface_predictor.py`.

## 3. PFAS & chemical properties (the physics/removal side)

| Dataset | What it gives | Feeds |
|---|---|---|
| **EPA CompTox Chemicals Dashboard** (comptox.epa.gov) | PFAS structures, DTXSIDs, physchem (logKow, pKa), batch download | QSAR for air-water adsorption coefficient K_ia **[in use]** |
| **PubChem** | Structures, computed properties | Same |
| **EPA ECOTOX Knowledgebase** | Aquatic toxicity incl. algae EC50 for PFAS | Toxin/tolerance cross-check |
| **EPA UCMR5** | Nationwide PFAS occurrence in drinking water | Realistic influent distributions for field-scale modeling |
| **Brusseau/Guo air-water interfacial adsorption compilations** | Measured K_ia per PFAS | Calibrates the interfacial model **[in use, via Lyu 2022]** |
| **OECD / NIST PFAS lists** | Canonical PFAS structure sets | Scope definition |

## 4. Datasets for other future Steps modeling exercises

**Enzyme / protein bioprospecting** (e.g. PFAS-defluorinating enzymes, directed evolution):
- **UniProt** (sequences/annotation), **BRENDA** (enzyme kinetics Km/kcat), **PDB** (structures),
  **AlphaFold DB** (predicted structures, near-complete proteome coverage), **MGnify** (EBI
  metagenomes) and **JGI IMG/M** (metagenome mining for novel hydrolases/dehalogenases),
  **KEGG** (pathways/reactions), **MEROPS** (proteases), **ESTHER** (alpha/beta-hydrolases).

**Carbon removal / geochemistry** (ERW, marine CDR):
- **EarthChem / PetDB** (rock & mineral geochemistry for feedstock screening), **GLODAP**,
  **SOCAT**, **World Ocean Atlas** (ocean carbon system), **PHREEQC** thermodynamic databases.

**Environmental / water**:
- **USGS Water Quality Portal / NWIS**, **EPA ECHO**, state groundwater DBs (e.g. CA GAMA).

**Health / longevity** (if the second-brain work goes quantitative):
- **UK Biobank**, **GEO**, **GTEx**, **Human Protein Atlas**, **ChEMBL** (bioactivity),
  **DrugBank**, **Open Targets**.

---
Access notes: most are free/open (some require registration: UK Biobank, JGI). Respect each
source's terms; cite per-value provenance as in `data/species_sources.md`.
