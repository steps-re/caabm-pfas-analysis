"""
Foam-fractionation removal ceiling from photosynthetic bubble interfacial area.

Physical model (first principles):
  The air-water interface is the sorbent. A gas volumetric flow Q_g of bubbles of
  radius r_b generates interfacial area at rate  A_rate = 3 * Q_g / r_b  (area/volume
  of a sphere = 3/r). Each unit of bubble surface leaves the system loaded to the
  equilibrium surface excess Gamma. So the maximum PFAS removal rate is

        removal_rate [mol/s] = Gamma * (3 * Q_g / r_b)

  and the single-pass fractional ceiling is removal_rate / (feed molar rate).

This is an OPTIMISTIC upper bound: it assumes every bubble reaches equilibrium
loading and that the loaded film leaves with the foam (no drainage back). The wide
output range reflects genuine uncertainty in the photosynthetic O2 rate (16x) and
bubble size. The purpose is an order-of-magnitude consistency check, not a fit.

Result: the PFOA ceiling brackets the observed 4.4%; the PFBA ceiling lies ~1-2
orders of magnitude BELOW its observed removal, i.e. PFBA cannot be removed by
foam fractionation in this device.

Run:  python flotation_ceiling.py
"""
from constants import (PFAS, GAS_MOLAR_VOL_L, CELLS_ANKISTRODESMUS,
                       O2_PER_CELL_FMOL_H, BUBBLE_RADIUS_M, FEED_CONC_G_PER_L,
                       FEED_FLOW_L_PER_MIN)
from interfacial_adsorption import surface_excess

OBSERVED = {"PFBA": 4.2, "PFOA": 4.4, "PFDA": None}   # algae-only, NI2026 Fig 5/3


def feed_mol_per_h(name):
    cw_mol_L = FEED_CONC_G_PER_L / PFAS[name]["mw"]
    return cw_mol_L * FEED_FLOW_L_PER_MIN * 60.0       # mol/h


def area_rate_m2_per_h(o2_fmol_cell_h, r_b_m, n_cells=CELLS_ANKISTRODESMUS):
    n_o2_mol_h = n_cells * o2_fmol_cell_h * 1e-15      # mol O2 / h
    q_gas_m3_h = n_o2_mol_h * GAS_MOLAR_VOL_L / 1000.0 # m^3 gas / h
    return 3.0 * q_gas_m3_h / r_b_m


def ceiling_bounds(name):
    lo, hi = float("inf"), 0.0
    gamma = surface_excess(name)
    for o2 in O2_PER_CELL_FMOL_H:
        for r_b in BUBBLE_RADIUS_M:
            frac = gamma * area_rate_m2_per_h(o2, r_b) / feed_mol_per_h(name)
            lo, hi = min(lo, frac), max(hi, frac)
    return lo * 100, hi * 100


def main():
    print("O2 range: %.0f-%.0f fmol/cell/h  |  bubble radius: %.2f-%.2f mm  |  cells: %.2e"
          % (O2_PER_CELL_FMOL_H[0], O2_PER_CELL_FMOL_H[1],
             BUBBLE_RADIUS_M[0]*1e3, BUBBLE_RADIUS_M[1]*1e3, CELLS_ANKISTRODESMUS))
    print(f"\n{'PFAS':7}{'ceiling (%)':>22}{'observed (%)':>14}{'verdict':>28}")
    for name in ("PFBA", "PFOA", "PFDA"):
        lo, hi = ceiling_bounds(name)
        obs = OBSERVED[name]
        if obs is None:
            verdict = "feed-limited (removal seen)"
        elif obs <= hi:
            verdict = "consistent with foam FF"
        else:
            verdict = "observed >> ceiling: NOT foam FF"
        obs_s = "-" if obs is None else f"{obs:.1f}"
        print(f"{name:7}{f'{lo:.3f} - {hi:.2f}':>22}{obs_s:>14}{verdict:>28}")


if __name__ == "__main__":
    main()
