# MVA Track 2 - F0 Statistical Analysis Plan (SAP) v1.0.1

**Frozen before N1002K unblinding and before any result-bearing F0 acquisition.**

## 1. Gate 0: genetic phase
The two project loci are 10,911 bp apart (chr15:40209701 and chr15:40220612 in the project coordinate set).
Short-read read-backed phasing is not treated as capable of directly spanning this pair.

Accepted resolution routes:
1. parental/trio genotyping of both variants;
2. long-read sequencing (ONT or PacBio HiFi);
3. long-range PCR spanning the interval followed by amplicon sequencing.

Interpretation is prospectively fixed:
- TRANS: compound-heterozygous BUB1B model remains coherent.
- CIS: the current pair is not a biallelic recessive explanation; reopen the second-allele/gene search.
- UNRESOLVED: all disease-context and drug claims remain conditional.

## 2. F0V validation layer
Primary validation endpoint: chromosome missegregation per completed division.
N1002K remains held out until control-only calibration is frozen.

The 11-control panel contains:
- 6 B/LB missense controls;
- 5 P/LP truncating controls.

The cDNA assay is interpreted as a protein-function assay. Truncating controls may validate loss of protein function,
but they do not validate RNA/NMD because cDNA bypasses endogenous transcript processing.

Binary thresholding rule:
- derive the abnormal/normal threshold only from frozen validation controls;
- lock threshold before unblinding N1002K;
- if B/LB and P/LP control distributions are not separable with an auditable threshold, do not force a binary PS3/BS3 call;
  report continuous effect sizes and classify the assay as insufficiently calibrated for that use.

## 3. ClinGen functional-evidence ceiling
OddsPath follows Brnich et al.:

OddsPath = [P2 x (1 - P1)] / [(1 - P2) x P1]

where P1 is the proportion of pathogenic variants in the modeled data and P2 is the posterior pathogenic proportion
within the relevant assay-readout group.

For perfect separation, the Brnich handling adds exactly one misclassified variant to each readout set.
For the frozen 5 P/LP + 6 B/LB real-control panel:
- modeled P1 = 6/13 = 0.462;
- abnormal group P2 = 5/6 = 0.833 -> PS3 OddsPath about 5.83;
- normal group P2 = 1/7 = 0.143 -> BS3 OddsPath about 0.194.

Therefore the prospective maximum is Moderate in both directions, not Strong.
The conclusion is robust to alternative prior conventions:
- P1 = 5/11 -> PS3 6.00 and BS3 0.200;
- P1 = 0.5 -> PS3 5.00 and BS3 0.167.

The benign direction has little headroom relative to the BS3_Moderate threshold (<0.23).

QC loss rule:
Brnich/ClinGen state that, in the absence of rigorous statistical calibration, at least 11 total pathogenic+benign controls
are required to reach Moderate. Losing any single real control leaves only 10 and therefore Moderate is not claimed
from the reduced count-based panel even when the reduced-panel OddsPath arithmetic remains numerically Moderate.

For completeness, loss of one P/LP control (4 P/LP + 6 B/LB) yields about PS3 5.60 and BS3 0.233;
the arithmetic therefore weakens the benign direction, not the pathogenic direction.
Loss of one B/LB control (5 P/LP + 5 B/LB) yields about PS3 5.00 and BS3 0.200,
but still fails the 11-control minimum.

No PS3_Strong/BS3_Strong claim is admissible from this control panel.

## 4. F0M primary mechanistic question
Primary question:
At the same measured BUBR1 abundance, does N1002K have a different chromosome-missegregation rate from WT?

Primary analysis:
- unit of biological inference: independent biological replicate;
- outcome: missegregation count with completed divisions as denominator;
- preferred model: binomial or beta-binomial mixed model, with measured abundance as a continuous term,
  variant (WT vs N1002K), variant-by-abundance interaction, and replicate blocking/random intercept where supported;
- two-sided alpha = 0.05 for the primary matched-abundance variant effect because either direction is biologically possible;
- report model estimate, absolute rate difference, relative rate/risk ratio where estimable, and 95% CI.

The approximate 10/30/50/75/100% abundance targets are design targets, not five independent primary hypotheses.
Measured abundance, not nominal expression dose, is the analysis variable.

## 5. Multiplicity
Only the matched-abundance WT-vs-N1002K interaction/contrast for the primary missegregation endpoint is primary.
Secondary endpoints (SAC, alignment, half-life, kinetochore localization, mitotic duration/output, viability/apoptosis)
are supportive and corrected within endpoint families using Holm's method.
Drug comparisons are not opened unless the F0 mechanism gate admits them.

## 6. Mechanism classification
The classification algorithm is frozen before N1002K unblinding.

ABUNDANCE-DOMINANT:
- N1002K shows reduced abundance and/or half-life relative to WT; and
- after abundance matching, the primary functional contrast does not show a material residual defect;
- any equivalence/noninferiority margin used for the residual functional contrast must be fixed from control-only assay
  variability before N1002K is unblinded.

FUNCTION-DOMINANT:
- a material residual functional defect persists after abundance matching.

MIXED:
- N1002K is abundance/half-life impaired and retains a material residual functional defect at matched abundance.

INDETERMINATE:
- QC fails, confidence intervals cross mechanistically relevant regions, or the assay cannot classify the state.

No post-hoc threshold tuning around N1002K is permitted.

## 7. Rescue definition
A clean rescue requires:
- improvement in missegregation per completed division;
- effect estimate and 95% CI reported at biological-replicate level;
- no >10% reduction in completed-division output sufficient to explain the apparent improvement;
- no >10 percentage-point increase in apoptosis/selective loss;
- no abundance-only increase without functional rescue.

For NB10-style drug decision simulations, 25% relative reduction remains a planning decision threshold,
not a biological truth. The moderate synthetic scenario used 40% true relative reduction.

## 8. Replication
- hard minimum QC floor: 4 independent biological replicates;
- preregistered target: 8 independent biological replicates for the principal F0 comparison;
- >=100 completed divisions per replicate/key condition.

## 9. Failed run vs negative biological result
FAILED_RUN:
- contamination/misidentification;
- missing construct/genotype confirmation;
- prespecified imaging/scoring QC failure;
- insufficient completed divisions below hard minimum;
- unresolvable assay-control failure.

NEGATIVE_RESULT:
- technical/QC gates pass, but the prespecified biological contrast does not support the hypothesized mechanism.

## 10. Blinding/randomization
- well positions randomized within plates;
- image acquisition order randomized or balanced;
- scorers blinded to genotype/treatment;
- unblinding occurs only after the control-only F0V threshold and SAP version/hash are frozen.
