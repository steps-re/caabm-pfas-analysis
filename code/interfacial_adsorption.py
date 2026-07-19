"""
Air-water interfacial adsorption of PFAS: the chain-length ladder.

Computes the interfacial adsorption coefficient K_ia and the equilibrium surface
excess Gamma = K_ia * C_w for each PFAS at the feed concentration, using Brusseau's
per-carbon regression anchored at the measured PFOA value. This quantifies the
"chain-length wall": short-chain PFBA adsorbs ~50x more weakly than PFOA, which is
why a pure foam-fractionation (interfacial) process cannot remove PFBA efficiently.

Run:  python interfacial_adsorption.py
Writes: ../data/pfas_properties.csv
"""
import csv, os
from constants import (PFAS, KIA_SLOPE_PER_CARBON, KIA_SLOPE_RANGE,
                       KIA_ANCHOR_CARBON, KIA_ANCHOR_CM, FEED_CONC_G_PER_L, N_A)


def kia_cm(carbons, slope=KIA_SLOPE_PER_CARBON):
    """Air-water interfacial adsorption coefficient (cm), Brusseau ladder."""
    return KIA_ANCHOR_CM * 10 ** (slope * (carbons - KIA_ANCHOR_CARBON))


def surface_excess(name, slope=KIA_SLOPE_PER_CARBON):
    """Equilibrium surface excess Gamma (mol/m^2) at the feed concentration."""
    mw = PFAS[name]["mw"]
    cw_mol_m3 = (FEED_CONC_G_PER_L / mw) * 1000.0      # mol/m^3
    kia_m = kia_cm(PFAS[name]["carbons"], slope) / 100.0
    return kia_m * cw_mol_m3


def main():
    rows = []
    g_pfoa = surface_excess("PFOA")
    for name, p in PFAS.items():
        g = surface_excess(name)
        rows.append(dict(
            pfas=name, carbons=p["carbons"], mw=p["mw"], cls=p["cls"],
            kia_cm=f"{kia_cm(p['carbons']):.3e}",
            gamma_mol_m2=f"{g:.3e}",
            gamma_per_nm2=f"{g * N_A / 1e18:.3e}",
            gamma_rel_pfoa=f"{g / g_pfoa:.3f}",
        ))

    print(f"{'PFAS':7}{'C':>3}{'K_ia (cm)':>12}{'Gamma (mol/m2)':>16}{'rel PFOA':>10}")
    for r in rows:
        print(f"{r['pfas']:7}{r['carbons']:>3}{r['kia_cm']:>12}"
              f"{r['gamma_mol_m2']:>16}{r['gamma_rel_pfoa']:>10}")

    # Robust ratio (independent of absolute K_ia calibration)
    for s in KIA_SLOPE_RANGE:
        ratio = surface_excess("PFOA", s) / surface_excess("PFBA", s)
        print(f"  Gamma_PFOA / Gamma_PFBA at slope {s}: {ratio:.0f}x")
    print("  -> If foam fractionation were the mechanism, PFOA must out-remove PFBA")
    print("     by ~30-90x. Ni et al. observe 1.05x (algae) to 1.23x (+coagulant).")

    out = os.path.join(os.path.dirname(__file__), "..", "data", "pfas_properties.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"\nwrote {os.path.normpath(out)}")


if __name__ == "__main__":
    main()
