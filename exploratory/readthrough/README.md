# Exploratory readthrough audit: NB14-NB16

This extension is included for transparency and experiment design. It is **not** a Track 2 therapeutic lead and does not establish readthrough efficacy for BUB1B.

## Interpretation hierarchy

1. **NB14** confirms the public L737* molecular constraint: TTA -> TGA/UGA, a 736-aa premature-stop product, and EJC geometry compatible with NMD. This is an NMD prediction, not an RNA measurement.
2. **NB15** generates possible full-length amino-acid products and reports ESM-2 sequence-plausibility scores. These scores are **not functional evidence**. The preregistered NB04B BUBR1 calibration found `NO_PREDICTOR_CALIBRATED`; ESM2-150M did not track the experimentally defined BUBR1 abundance class. No sequence model in this project is calibrated to BUBR1 checkpoint or chromosome-segregation function. The identity of the inserted residue therefore defines an experiment, not a computational functional verdict.
3. **NB16** maps translational requirements across hypothetical RNA x readthrough x stability x function scenarios. The 432 scenarios are not patient-specific estimates and no compound receives a therapeutic PASS.

2,6-diaminopurine is retained only as a mechanistic UGA->W probe. ACE-tRNA^Leu is a future research direction outside the market-approved-medication scope of Track 2 and is not a candidate in the final panel.

## Reproduction

The public notebook copies are sanitized and write to a user-selected local/persistent root:

```bash
export MVA_READTHROUGH_ROOT=/path/to/READTHROUGH_EXTENSION_v1_0_0
```

Run NB14 -> NB15 -> NB16 in order. NB15 may download public ESM-2 weights when its optional ESM stage is enabled. No private WGS/VCF is required. Exact completed run bundles are provided in `results/` together with selected machine-readable outputs.

## Decisive experiment

The remaining question is functional: measure allele-specific RNA and compare WT/L737W/L737C/L737R products at matched BUBR1 abundance using kinetochore localization, spindle-assembly-checkpoint readouts and chromosome missegregation per completed division. The existing F0M `N1002K/WT` arm already tests whether one corrected/WT BUB1B allele would be functionally sufficient in the presence of N1002K.
