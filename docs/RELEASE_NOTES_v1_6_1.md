# Release notes v1.6.1

This release supersedes v1.6.0.

Changes:
- corrected NB17 OddsPath implementation to the Brnich P1/P2 formula with perfect-separation pseudocount handling;
- full-panel perfect-separation values are PS3 ≈5.83 and BS3 ≈0.194, both Moderate, never Strong;
- corrected QC-loss interpretation: any single real-control loss leaves 10 controls, below the count-based 11-control Moderate minimum; the thin numerical margin is on the BS3 side;
- synchronized the AI/external-service disclosure across the report, README and privacy/disclosure documents;
- corrected full citations for North et al. 2014, Choi et al. 2009 and Brnich et al. 2020;
- added the condition-aware ClinVar aggregation generalization;
- retimed the 3-minute pitch to 422 words and surfaced Gate 0 geometry plus the NB17 evidence ceiling.
