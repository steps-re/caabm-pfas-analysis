"""
Staging model: how modest single-pass removal compounds into high total removal.

The CAABM system removes only ~10-14% of PFAS per pass. That is the headline weakness.
But single-pass extent is the wrong number to judge it on, because removal compounds.

In the dilute (linear) regime we established for this system, the per-pass removal fraction R
is approximately concentration-independent, so N stages in series (or N recirculation passes
through one column) give:

        total_removal(N) = 1 - (1 - R)^N
        stages to reach target T:  N = ceil( ln(1-T) / ln(1-R) )

The key design consequence: the bubbles are free (photosynthetic O2, no aeration energy), so
adding stages trades footprint/residence time for extent WITHOUT giving up the energy advantage
that is the system's real selling point. The number of stages is the design variable, not a
fundamental limit.

Two levers reach a target: more stages (N), or a higher single-pass R (via coagulant-dose
optimization -- the other Section 8 recommendation). This model shows how they trade off.

Run:  python staging_model.py
Assumptions/caveats: constant R per stage (valid in the linear regime; conservative because
real R often rises as competing organics are stripped); each stage supplies fresh bubbling
algae; ignores inter-stage handling losses and progressive EPS fouling. It is a design-scoping
model, not a plant prediction.
"""
import math

# Best measured single-pass removal, Ankistrodesmus + coagulant (Ni et al. 2026, Fig. 5).
SINGLE_PASS = {"PFOA": 0.139, "PFBA": 0.103}
TARGETS = [0.90, 0.99, 0.999]


def stages_to_target(R, T):
    return math.ceil(math.log(1 - T) / math.log(1 - R))


def total_removal(R, N):
    return 1 - (1 - R) ** N


def main():
    print("=== Total removal vs number of stages / recirculation passes ===")
    header = "  stages: " + "".join(f"{n:>7}" for n in (1, 2, 5, 10, 20, 30))
    print(header)
    for name, R in SINGLE_PASS.items():
        row = "".join(f"{total_removal(R, n)*100:>6.0f}%" for n in (1, 2, 5, 10, 20, 30))
        print(f"  {name} (R={R*100:.1f}%/pass): {row}")

    print("\n=== Stages (or recirculation passes) needed to hit a target ===")
    print(f"  {'compound':10}{'R/pass':>8}" + "".join(f"{t*100:g}%->N".rjust(9) for t in TARGETS))
    for name, R in SINGLE_PASS.items():
        cells = "".join(f"{stages_to_target(R, t):>9}" for t in TARGETS)
        print(f"  {name:10}{R*100:>7.1f}%{cells}")

    print("\n=== Lever trade-off: improving single-pass R (dose optimization) cuts stages ===")
    print("  Stages to reach 90% removal as a function of single-pass R:")
    for R in (0.10, 0.15, 0.20, 0.30, 0.50):
        print(f"    R = {R*100:>4.0f}% /pass  ->  {stages_to_target(R, 0.90):>2} stages to 90%")
    print("  So doubling single-pass R (from ~13% to ~26%, plausibly within reach by optimizing")
    print("  the coagulant dose to the isoelectric point) roughly HALVES the stages needed.")

    print("\n=== Mixture effluent after a 20-stage cascade (feed = 10 ug/L each) ===")
    for name, R in SINGLE_PASS.items():
        eff = 10.0 * (1 - R) ** 20
        print(f"  {name}: {eff:.2f} ug/L  ({total_removal(R,20)*100:.0f}% removed)")
    print("  For context, the US EPA MCL for PFOA is 4 ng/L = 0.004 ug/L; reaching that from")
    print("  10 ug/L needs 1-0.0004 = 99.96% removal, i.e. ~58 stages at R=13% or ~24 at R=30%.")
    print("  Staging alone gets you there in principle; whether it is practical is a")
    print("  footprint/residence economics question, which is the honest next study.")


if __name__ == "__main__":
    main()
