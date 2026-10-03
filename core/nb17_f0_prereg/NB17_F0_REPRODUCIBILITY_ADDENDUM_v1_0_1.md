# F0 reproducibility addendum v1.0.0

## Cell models
- U2OS: RRID CVCL_0042 (F0V protein-function validation architecture).
- hTERT-RPE1: RRID CVCL_4388 (F0M endogenous isogenic disease-context mechanism).

## Required implementation freeze before wet-lab start
The following must be versioned in a lab-specific implementation sheet before acquisition:
- exact RNAi sequence(s) used to deplete endogenous BUBR1 in F0V;
- RNAi-resistant BUB1B plasmid maps and sequence hashes;
- exact CRISPR guide(s), donor design(s), clone IDs and genotype-confirmation method for F0M;
- antibody catalogue numbers/lot IDs where practical;
- microscope, objective NA, camera, pixel size, exposure/gain, z-step, frame interval and acquisition duration;
- plate map/randomization seed;
- scorer blinding key and unblinding procedure.

## Operational phenotype definitions
- lagging chromosome: chromatin mass clearly separated from the main segregating chromosome masses during anaphase,
  located between poles and not forming a continuous DNA bridge;
- anaphase bridge: continuous DNA connection between daughter chromatin masses during anaphase/telophase;
- micronucleus: discrete extranuclear chromatin body in an interphase daughter cell after completed division;
- completed division: a mitotic event progressing through cytokinesis into two daughter-cell compartments;
- aborted/failed mitosis is counted in mitotic-output/QC metrics and is never silently removed from the denominator logic.

Primary endpoint should preserve component categories in the raw annotation table even if a prespecified composite
'missegregation per completed division' is used for the primary analysis.

## Practical execution profile
- U2OS F0V implementation/pilot: approximately 6-8 weeks after constructs/reagents are available.
- hTERT-RPE1 isogenic 5-arm generation/validation: approximately 3-4 months; longer if clone regeneration is needed.
- planning-level assay budget: roughly EUR 15k-40k excluding institutional salary/overhead and major capital equipment;
  this is a planning range, not a vendor quotation.
