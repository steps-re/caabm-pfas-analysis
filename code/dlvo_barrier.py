"""
Electrostatic attachment barrier: why Chlorella (0%) failed and Ankistrodesmus worked.

In flotation the bubble-particle attachment probability is governed by the thin
(wetting) liquid film between them. Its DLVO electrostatic term scales, at large
separation, with the PRODUCT of the two surface potentials:

    W_edl(D) ~ (eps0*eps*kappa/2) * [2*psi1*psi2 - (psi1^2 + psi2^2) e^-kappaD] / (e^kappaD - e^-kappaD)
    -> at large D collapses to  -2*eps0*eps*kappa^2 * psi1*psi2 * e^-kappaD
    (Israelachvili, Intermolecular & Surface Forces, Eq. 14.61)

Crucially, in a bubble/water/particle film the van der Waals term is ALSO repulsive
(air's Hamaker constant ~ 0), so the hydrophobic force is the only attraction. When
both DLVO terms repel, the barrier height sets P_attachment, which falls roughly
exponentially with the barrier.

Using zeta potential as a proxy for surface potential and a common partner (the
bubble at ~-35 mV, or a floc), replacing Chlorella with Ankistrodesmus lowers the
repulsive product term by |zeta_C| / |zeta_A|. For the symmetric self-term the
scaling is quadratic. Either way the reduction is large enough, through the
exponential, to move the system from "0%" to "works."

Run:  python dlvo_barrier.py
"""
import math
from constants import ZETA_CHLORELLA_MV, ZETA_ANKISTRODESMUS_MV, BUBBLE_ZETA_MV

zC = abs(ZETA_CHLORELLA_MV)
zA = abs(ZETA_ANKISTRODESMUS_MV)


def main():
    print(f"Measured zeta (Bold's Basal Medium, ~pH 6): "
          f"Chlorella {ZETA_CHLORELLA_MV} mV, Ankistrodesmus {ZETA_ANKISTRODESMUS_MV} mV")
    print(f"Air bubble zeta (partner): {BUBBLE_ZETA_MV} mV\n")

    lin = zC / zA
    quad = (zC / zA) ** 2
    print(f"Repulsive-barrier ratio, Chlorella / Ankistrodesmus:")
    print(f"  linear  (psi1*psi2, common partner): {lin:.2f}x")
    print(f"  quadratic (symmetric overlap):        {quad:.2f}x\n")

    print("Attachment probability ~ exp(-barrier). If the Ankistrodesmus barrier is")
    print("a few kT, the Chlorella attachment probability is suppressed by:")
    for nkT in (1, 3, 5, 8):
        ratio = math.exp(-(lin - 1) * nkT)
        print(f"  Ankistrodesmus barrier ~{nkT} kT  ->  P(Chlorella)/P(Ankistrodesmus) = {ratio:.3g}")
    print("\nEven the conservative linear scaling drops Chlorella attachment by 1-2")
    print("orders of magnitude, consistent with the observed 0% vs 4-14%.")


if __name__ == "__main__":
    main()
