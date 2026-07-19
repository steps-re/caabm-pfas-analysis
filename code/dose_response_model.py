"""
Coagulant dose-response: predict the optimal dose, to guide the dose-optimization experiment.

Physics: removal peaks when the cell's net surface charge is neutralized (isoelectric point,
zeta = 0). Below the optimum, residual negative charge repels the negative PFAS head and the
negative bubble; above it, charge reversal re-stabilizes the cells and excess free polycation
sequesters PFAS in the bulk. So removal is a PEAK in net zeta centered at zero. The DLVO
barrier scales with |zeta|, so a Gaussian in zeta is the natural first-order form:

        removal(zeta) = R_max * exp( -(zeta / w)^2 )

We calibrate the charge-tolerance width w from Ni et al.'s own numbers, then read off how tight
the dose has to be and where each coagulant's optimum sits.

Run:  python dose_response_model.py
This is design guidance from a peaked-at-IEP model calibrated on a few points, NOT a fitted
plant curve. Its main output is an experimental procedure (titrate dose to zeta = 0) plus the
dose windows and tolerance to scan, which is exactly what the optimization study needs.
"""
import math

# Ni et al. 2026 (Fig. 4-5), PFOA, Ankistrodesmus:
ZETA_NO_COAG = -13.8     # mV, no coagulant
R_NO_COAG = 4.4          # % removal, no coagulant (net charge -13.8 mV)
R_BEST = 13.9            # % removal, best observed (1 ppm pDADMAC, taken as near the peak)

# Calibrate the charge-tolerance width w from the no-coagulant point:
#   R_NO_COAG / R_BEST = exp(-(ZETA_NO_COAG / w)^2)
w = abs(ZETA_NO_COAG) / math.sqrt(-math.log(R_NO_COAG / R_BEST))


def removal(zeta, r_max=R_BEST):
    return r_max * math.exp(-(zeta / w) ** 2)


def zeta_for_fraction(frac):
    # |zeta| that gives `frac` of peak removal
    return w * math.sqrt(-math.log(frac))


def main():
    print(f"Calibrated charge-tolerance width w = {w:.1f} mV")
    print(f"(from no-coagulant point: zeta {ZETA_NO_COAG} mV gives {R_NO_COAG}% vs peak {R_BEST}%)\n")

    print("=== How tight does the dose have to be? ===")
    for frac in (0.95, 0.90, 0.75, 0.50):
        print(f"  to keep >={int(frac*100)}% of peak removal, need |net zeta| < {zeta_for_fraction(frac):4.1f} mV")
    print("  -> the useful window is only a few mV wide, so dose PRECISION matters; a coarse")
    print("     dose scan will step over the peak. This is the key operational finding.\n")

    print("=== Mapping the observed doses onto the charge axis ===")
    print("  Coagulant / dose        observed removal   inferred net charge state")
    obs = [("none",              "4.4%", "-13.8 mV (measured): under-neutralized"),
           ("1 ppm pDADMAC",     "13.9%", "~0 mV: near the isoelectric peak"),
           ("100 ppm FeCl3",     "12.7%", "~0 mV: near IEP (Fe needs ~100x the polycation dose)"),
           ("60 ppm alum",       "3.0%",  "still negative: under-dosed (weaker neutralizer here)"),
           ("100 ppm pDADMAC",   "1.3%",  "strongly positive: charge-reversed / re-stabilized")]
    for d, r, s in obs:
        print(f"  {d:20} {r:>8}      {s}")

    print("\n=== Predicted optimum and the scan to run ===")
    print("  pDADMAC: optimum is O(1 ppm). Since 1 ppm already sits near the peak and 100 ppm is")
    print("           far over, scan FINELY 0.3-3 ppm (e.g. 0.3, 0.5, 0.75, 1, 1.5, 2, 3).")
    print("  FeCl3:   optimum is O(100 ppm). Scan 40-150 ppm (40, 60, 80, 100, 125, 150).")
    print("  alum:    under-dosed at 60 ppm; scan higher, 80-250 ppm, or drop it.")
    print("  Operational rule: MEASURE ZETA AT EACH DOSE and pick the dose where zeta crosses 0.")
    print("  That dose is the optimum regardless of which coagulant; the removal peak rides on it.")

    print("\n=== Expected upside ===")
    print(f"  Best observed is {R_BEST}% (PFOA), but 1 ppm/100 ppm need not be exactly at zeta=0.")
    print(f"  Landing within +/-{zeta_for_fraction(0.95):.1f} mV of the IEP recovers >=95% of the true")
    print(f"  peak; the true peak R_max is >= {R_BEST}% and is what a fine, zeta-guided scan finds.")


if __name__ == "__main__":
    main()
