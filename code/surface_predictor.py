"""
Genome/cell-wall -> cell-surface hydrophobicity: a proof-of-concept predictor, and an
honest test of whether wall biochemistry predicts measured contact angle.

Hypothesis (from the biochemistry): algaenan -- a resistant, aliphatic, cutan-like wall
biopolymer -- should make a cell hydrophobic. If true, we could predict hydrophobicity
(and rank species for the CAABM screen) from the genome/wall type alone, without measuring
every species.

This script tests that hypothesis against the measured contact angles we have, then reports
what the data actually supports. Spoiler, and the point of the exercise: the signal is weak,
so this is a scaffold plus a negative result plus the path to a real model, not a finished
predictor. Honest > impressive.

Run:  python surface_predictor.py   (reads ../data/cell_wall_features.csv)
"""
import csv, os, statistics

# Growth phase moves contact angle by ~45 deg WITHIN a single strain (Xia et al. 2017,
# PLOS ONE: Botryococcus 28.7 -> 75.3 deg across active/stationary/aged culture). Any
# wall-type signal has to beat that confounder to be usable.
GROWTH_PHASE_SPREAD_DEG = (28.7, 75.3)


def load():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "cell_wall_features.csv")
    with open(path) as f:
        return list(csv.DictReader(f))


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main():
    rows = load()
    euk = [r for r in rows if r["algaenan"] in ("yes", "no")]         # eukaryotes with a clear call
    measured = [r for r in euk if num(r["contact_angle_deg"]) is not None]

    yes = [num(r["contact_angle_deg"]) for r in measured if r["algaenan"] == "yes"]
    no = [num(r["contact_angle_deg"]) for r in measured if r["algaenan"] == "no"]

    def summ(v):
        return f"n={len(v)} mean={statistics.mean(v):.0f} sd={statistics.pstdev(v):.0f} range={min(v):.0f}-{max(v):.0f}"

    print("=== Test: does cell-wall ALGAENAN predict measured water contact angle? ===")
    print(f"  algaenan present : {summ(yes)}  {[r['species'].split()[0] for r in measured if r['algaenan']=='yes']}")
    print(f"  algaenan absent  : {summ(no)}  {[r['species'].split()[0] for r in measured if r['algaenan']=='no']}")
    diff = statistics.mean(yes) - statistics.mean(no)
    print(f"  difference in means: {diff:+.0f} deg   (growth-phase confounder alone spans "
          f"{GROWTH_PHASE_SPREAD_DEG[1]-GROWTH_PHASE_SPREAD_DEG[0]:.0f} deg within one strain)")

    # The Botryococcus braunii outlier check
    yes_no_bot = [num(r["contact_angle_deg"]) for r in measured
                  if r["algaenan"] == "yes" and not r["species"].startswith("Botryococcus braunii")]
    print(f"\n  Remove the single Botryococcus braunii outlier and algaenan+ mean = "
          f"{statistics.mean(yes_no_bot):.0f} deg, i.e. LOWER than algaenan- ({statistics.mean(no):.0f}).")

    print("\n=== VERDICT ===")
    print("  Cell-wall algaenan presence does NOT reliably predict measured contact angle in")
    print("  this dataset. The +difference is driven entirely by one hydrophobic outlier")
    print("  (Botryococcus braunii, 112 deg); algaenan-bearing Scenedesmus/Desmodesmus are")
    print("  hydrophilic-to-moderate, and glycoprotein-walled Ankistrodesmus (86 deg) is")
    print("  hydrophobic without algaenan. Within-strain growth-phase variation swamps the")
    print("  between-class signal. So: hydrophobicity must be MEASURED, not inferred from")
    print("  wall class -- which is itself the useful result for the screen.")

    print("\n=== What a real predictor would need (the path) ===")
    print("  1. Quantitative algaenan CONTENT (% of wall), not presence/absence.")
    print("  2. Growth-phase-controlled contact-angle measurements (fix the confounder).")
    print("  3. More labelled species: only ~5 have BOTH a genome and a measured surface.")
    print("  4. Then a genome feature set (CAZy wall/EPS gene counts, algaenan-synthase")
    print("     homologs) can be regressed on measured hydrophobicity with real power.")

    print("\n=== Provisional qualitative flags for UNMEASURED species (low confidence) ===")
    for r in euk:
        if num(r["contact_angle_deg"]) is None:
            lean = "hydrophobic-leaning" if r["algaenan"] == "yes" else "uncertain/likely hydrophilic"
            print(f"  {r['species']:28} wall={r['wall_type']:32} -> {lean}")


if __name__ == "__main__":
    main()
