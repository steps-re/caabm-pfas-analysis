"""
Deterministic species-selection screen.

Turns the 20-year "find a better algae" search into a reproducible ranking over
existing culture-collection strains, scored on the four measurable traits the
physics identifies. The score is:

    S = 100 * G_toxin * ( 0.35*f_charge + 0.25*f_hydro + 0.20*f_bubble + 0.20*f_lowEPS )

  f_charge = 1 - |zeta|/40mV        (clamped 0..1) - lowers the DLVO barrier
  f_hydro  = contact_angle / 90deg  (or MATH% proxy) - the only bubble-cell attraction
  f_bubble = normalized growth * O2 - generates interfacial area
  f_lowEPS = 1 - normalized EPS     - avoids competing anions / charge reloading
  G_toxin  = 0 if toxigenic else 1  - hard gate

Weights encode the evidence ranking (charge is the gate proven by the Chlorella vs
Ankistrodesmus result); re-fit once >2 strains are run through the actual column.
Missing traits are treated as neutral (0.5) so incomplete strains are neither
rewarded nor unfairly buried, and flagged in the output.

Run:  python species_screen.py   (reads ../data/species_candidates.csv)
"""
import csv, os

WEIGHTS = dict(charge=0.35, hydro=0.25, bubble=0.20, lowEPS=0.20)


def f_charge(zeta_mv):
    if zeta_mv is None:
        return None
    return max(0.0, min(1.0, 1.0 - abs(zeta_mv) / 40.0))


def f_hydro(contact_angle_deg):
    if contact_angle_deg is None:
        return None
    return max(0.0, min(1.0, contact_angle_deg / 90.0))


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def score_row(r):
    toxin = r["toxin"].strip().lower() in ("yes", "true", "1")
    g_toxin = 0.0 if toxin else 1.0

    feats = dict(
        charge=f_charge(_num(r.get("zeta_mV"))),
        hydro=f_hydro(_num(r.get("contact_angle_deg"))),
        bubble=_num(r.get("bubble_score")),      # 0..1 supplied where known
        lowEPS=_num(r.get("lowEPS_score")),      # 0..1 supplied where known
    )
    missing = [k for k, v in feats.items() if v is None]
    filled = {k: (0.5 if v is None else v) for k, v in feats.items()}
    S = 100.0 * g_toxin * sum(WEIGHTS[k] * filled[k] for k in WEIGHTS)
    return S, g_toxin, missing


def main():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "species_candidates.csv")
    with open(path) as f:
        rows = list(csv.DictReader(f))

    scored = []
    for r in rows:
        S, gate, missing = score_row(r)
        scored.append((S, gate, missing, r))
    scored.sort(key=lambda t: t[0], reverse=True)

    print(f"{'rank':>4}  {'species (strain)':38}{'zeta':>7}{'CA':>6}{'score':>8}  gaps")
    for i, (S, gate, missing, r) in enumerate(scored, 1):
        gated = "" if gate else "  [TOXIN-GATED to 0]"
        name = f"{r['species']} ({r.get('strain','') or '-'})"[:38]
        z = r.get("zeta_mV") or "-"
        ca = r.get("contact_angle_deg") or "-"
        print(f"{i:>4}  {name:38}{z:>7}{ca:>6}{S:>8.1f}  {','.join(missing) or 'complete'}{gated}")
    print("\nNote: missing traits scored neutral (0.5). Acquire measured contact angles")
    print("(e.g. Ozkan & Berberoglu 2013) to resolve the largest data gap.")


if __name__ == "__main__":
    main()
