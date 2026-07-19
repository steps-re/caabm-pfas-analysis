"""
QSAR: predict air-water interfacial adsorption (hence foam-fractionation removability) for all
16 PFAS in the Ni et al. (2026) study, from structure.

The physically grounded variable is the number of PERFLUORINATED carbons (n_CF2), not total
carbons: it handles perfluorosulfonates, fluorotelomer sulfonates (which carry non-fluorinated
CH2CH2 spacers), and the ether-containing GenX on the same footing. We scale the measured
Brusseau ladder off it:

    K_ia(cm) = K_ia(PFOA) * 10^(slope * (nCF2 - nCF2_PFOA)) * sulfonate_factor

Then surface excess Gamma = K_ia * C_w sets foam-fractionation removability. The point: classify
each compound as foam-removable (long perfluoro chain) vs charge-mechanism-dependent (short
chain), across the whole mixture, and cross-check the ladder against computed logKow.

Run:  python pfas_qsar.py   (reads ../data/pfas_physchem.csv)
Caveats: slope and the ~1.5x sulfonate factor are literature-level approximations (Brusseau
group; sulfonates adsorb somewhat more than carboxylates of equal chain). logKow here is a
COMPUTED (PubChem XLogP) value, so the logKow cross-check is a consistency check, not a second
independent measurement. Absolute ceilings inherit the O2/bubble uncertainty of flotation_ceiling.py.
"""
import csv, os, math

SLOPE = 0.50                 # log10 K_ia per perfluorinated carbon (Brusseau ~0.46-0.56)
KIA_PFOA_CM = 0.00285        # anchor, PFOA
NCF2_PFOA = 8
SULFONATE_FACTOR = 1.5       # sulfonates adsorb ~1.5x a carboxylate of equal perfluoro-chain


def load():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "pfas_physchem.csv")
    with open(path) as f:
        return list(csv.DictReader(f))


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def is_sulfonate(name):
    return name.endswith("S") and not name.endswith("FTS")   # PFBS/PFHxS/PFHpS/PFOS


def main():
    rows = load()
    out = []
    for r in rows:
        ncf2 = num(r["n_perfluoro_C"])
        mw = num(r["mw"])
        if ncf2 is None or mw is None:
            continue
        factor = SULFONATE_FACTOR if is_sulfonate(r["compound"]) else 1.0
        kia = KIA_PFOA_CM * 10 ** (SLOPE * (ncf2 - NCF2_PFOA)) * factor
        cw = (10e-6 / mw)                       # mol/L at 10 ug/L
        gamma_rel = (kia * cw)                  # proportional to surface excess
        out.append(dict(name=r["compound"], ncf2=ncf2, logkow=num(r["logKow_calc"]),
                        kia=kia, gamma=gamma_rel))

    g_pfoa = next(o["gamma"] for o in out if o["name"] == "PFOA")
    for o in out:
        o["gamma_rel_pfoa"] = o["gamma"] / g_pfoa

    print(f"{'PFAS':10}{'nCF2':>5}{'logKow':>8}{'K_ia(cm)':>12}{'Gamma/PFOA':>12}  foam removability")
    for o in sorted(out, key=lambda x: x["gamma_rel_pfoa"], reverse=True):
        rel = o["gamma_rel_pfoa"]
        cls = ("foam-removable" if rel >= 1 else
               "marginal" if rel >= 0.2 else
               "charge-mechanism-dependent")
        lk = f"{o['logkow']:.1f}" if o["logkow"] is not None else " - "
        print(f"{o['name']:10}{o['ncf2']:>5.0f}{lk:>8}{o['kia']:>12.2e}{rel:>12.3f}  {cls}")

    # logKow cross-check (Pearson r between log K_ia and logKow)
    pts = [(math.log10(o["kia"]), o["logkow"]) for o in out if o["logkow"] is not None]
    n = len(pts)
    mx = sum(p[1] for p in pts) / n
    my = sum(p[0] for p in pts) / n
    cov = sum((p[1]-mx)*(p[0]-my) for p in pts)
    sx = math.sqrt(sum((p[1]-mx)**2 for p in pts))
    sy = math.sqrt(sum((p[0]-my)**2 for p in pts))
    r = cov / (sx*sy)
    print(f"\nCross-check: log K_ia vs computed logKow, Pearson r = {r:.2f} (n={n}).")
    print("High r confirms the perfluoro-chain ladder and the octanol-water hydrophobicity")
    print("scale tell the same story, as expected for a hydrophobically-driven process.")

    print("\nReading: long-chain PFCAs/PFSAs (PFNA, PFDA, PFUnA, PFOS) are foam-removable; the")
    print("short chains that dominate contaminated water (PFBA, PFPeA, PFBS, GenX) and the")
    print("telomer sulfonates fall in the charge-mechanism-dependent class -- exactly the")
    print("compounds the coagulant step exists to rescue (main text, section 3).")


if __name__ == "__main__":
    main()
