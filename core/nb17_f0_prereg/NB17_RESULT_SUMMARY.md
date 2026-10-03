# NB17 result summary v1.0.1

## PASS
This corrected release supersedes NB17 v1.0.0 for OddsPath calculations.

### Gate 0
Variant distance: **10,911 bp**.
Phase remains a hard diagnostic gate with explicit TRANS/CIS/UNRESOLVED actions.

### F0V controls
Frozen panel: **6 B/LB missense + 5 P/LP truncating**.
No splice/promoter/UTR control is encoded in the frozen manifest.
The truncating controls are restricted to protein-function validation; cDNA does not validate endogenous RNA/NMD.

### Corrected ClinGen ceiling
Brnich-style perfect-separation handling:
- modeled P1 = **6/13 = 0.462**;
- PS3: P2 = 5/6 -> OddsPath **5.833**, Moderate;
- BS3: P2 = 1/7 -> OddsPath **0.194**, Moderate.

Strong evidence remains impossible from the frozen panel.

The full-panel conclusion is robust to prior convention:
- observed-control prior (P1=5/11): PS3 6.00, BS3 0.200;
- balanced prior (P1=0.5): PS3 5.00, BS3 0.167.

### Corrected QC-loss interpretation
Losing any single real control leaves **10**, below the stated 11-control minimum for count-based Moderate evidence.
The reduced-panel arithmetic does **not** show the previously claimed pathogenic-side collapse:
- 4 P/LP + 6 B/LB -> PS3 **5.600** (Moderate arithmetic),
  BS3 **0.233** (Supporting arithmetic);
- 5 P/LP + 5 B/LB -> PS3 **5.000**, BS3 **0.200**,
  but the 11-control minimum is not met.

### SAP
Primary contrast, multiplicity, 95% CI, QC-failure definitions, and pre-unblinding threshold rules remain frozen.

No drug efficacy, PS3/BS3 assignment, or treatment recommendation is produced by NB17.
