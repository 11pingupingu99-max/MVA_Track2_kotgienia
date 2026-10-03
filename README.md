# MVA Hackathon 2026 - Track 2 - kotgienia

## Mechanism-gated rescue for an unresolved BUB1B/MVA hypothesis

This repository is the Track 2 reproducibility package for the Rare Disease, Real Kid: MVA Hackathon 2026.

### Central result
The project does **not** claim that a drug has rescued BUB1B/MVA. It defines a falsifiable decision architecture:

`phase -> abundance-matched mechanism -> exact approved-drug coverage -> exposure plausibility -> causal rescue -> false-rescue hard gates -> conditional testing`

The Track 1 BUB1B L737* + N1002K ranking was scorer-confirmed at 100/100 rank points and F-max 1.000 at EPCR 0.78. That score is used only as a genetic anchor; phase and N1002K mechanism remain unresolved.

### Repository structure
- `report/` - submission report PDF and Markdown.
- `figures/` - decision-architecture figure.
- `core/notebooks/` - NB08R2, NB09, F0 abundance-matched addendum, NB10.
- `core/evidence/` - exact coverage, exposure and operating-characteristic outputs.
- `core/addenda/` - replicate-target and 95% CI reporting clarifications.
- `exploratory/` - NB11-NB16 exploratory extensions, explicitly non-efficacy evidence; NB15 is subordinate to the failed NB04B predictor calibration.
- `pitch/` - 3-minute script and storyboard.
- `docs/` - methods form, privacy/AI disclosure, deletion plan, execution profile and submission checklist.

### Key methodological corrections
1. ChEMBL activity not run is `NOT_RUN`, never numeric zero.
2. ChEMBL target mapping is exact component-aware (`target_components__accession`), not fuzzy text search.
3. Approved-drug coverage is not a therapeutic ranking.
4. Clinically plausible exposure is a separate gate.
5. N1002K is tested at matched BUBR1 abundance; no 30% WT cutoff defines mechanism.
6. FUNCTION-DOMINANT is a legitimate negative branch: no approved drug in the audited target space currently qualifies as a causal rescue.
7. Cytostasis and selective killing cannot count as rescue.
8. Four biological replicates are a hard minimum QC floor; eight are the preregistered target for the principal F0 comparison when feasible.
9. Result-bearing F0 analyses must report effect size and 95% CI, not only PASS/FAIL.


### Final audit boundary
A final pre-freeze audit found no additional computational module with a higher expected value than the risk of diluting the falsifiable core. In particular, larger ESM models were not pursued because the limiting issue is calibration to BUBR1 function, not model size. Readthrough analyses are therefore quarantined as exploratory constraints, and engineered ACE-tRNA approaches remain outside the market-approved-medication scope of Track 2.


### License
Submission materials are released under CC BY 4.0.



## NB17 final pre-registration freeze

NB17 v1.0.1 adds no treatment claim. It freezes phase as Gate 0 (10,911 bp between loci), F0V mechanism-compatibility scope, the corrected Brnich-style OddsPath ceiling (**PS3 ≈5.83; BS3 ≈0.194; Moderate only**), the 11-control count minimum, the matched-abundance F0M SAP, 95% CI/effect-size reporting, the 8-replicate execution target, reproducibility requirements, and the conditional NAD+–SIRT2 branch.

## 13. AI-assistance disclosure

**OpenAI ChatGPT (Plus)** was used for code review, literature evaluation, debugging and drafting on sanitized/public project materials. **No private patient genomic data, raw WGS/VCF, private genotype tables, patient identifiers, or the non-public case allele table were provided to or read by ChatGPT.**

The submitter confirms that ChatGPT's **"Improve the model for everyone" setting was disabled during the relevant project conversations**. This confirmation was recorded on 3 October 2026.

**Google DeepMind AlphaGenome** is disclosed separately because an earlier hypothesis-audit branch received exactly **two preselected patient-derived BUB1B variant coordinates and alleles**. No raw WGS/VCF, genome-wide genotype table, sample identifier, clinical record, or unrelated patient variant table was transmitted. AlphaGenome did not determine the Track 1 ranking and did not establish a primary N1002K RNA mechanism.
