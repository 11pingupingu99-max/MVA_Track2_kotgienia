# BUBR1-DOSE — Analysis B final closure v1.1.0

**Created:** 2026-09-22T22:07:03.238470+00:00  
**Final status:** `N1002K_ABUNDANCE_CLASS = AMBIGUOUS`  
**Predictor-calibration result:** `NO_PREDICTOR_CALIBRATED`

## Question

Can generic missense/pathogenicity or sequence-plausibility predictors distinguish experimentally
**low-abundance/destabilized BUBR1 substitutions** from experimentally **WT-like/stable BUBR1 substitutions**?

The answer on the complete frozen BUBR1 comparator set is **no**.

## Complete-set result

All predictors were evaluated on the same frozen 11-variant set:
- 7 low-abundance/destabilized;
- 4 WT-like/stable;
- N1002K excluded from calibration.

Frozen gate:
- AUC >= 0.80
- bootstrap 95% AUC lower bound > 0.50
- leave-one-out balanced accuracy >= 0.70

| Predictor | AUC | 95% CI lower | LOO balanced accuracy | N1002K score | Gate |
|---|---:|---:|---:|---:|---|
| PolyPhen | 0.679 | 0.300 | 0.589 | 0.997 | FAIL |
| SIFT harm | 0.607 | 0.268 | 0.482 | 0.990 | FAIL |
| ESM2-150M | 0.607 | 0.111 | 0.411 | 0.403 | FAIL |
| BLOSUM62 | 0.571 | 0.196 | 0.643 | 0 | FAIL |
| AlphaMissense | **0.464** | **0.000** | **0.268** | **0.9229** | **FAIL** |

## Central result

N1002K looks strongly damaging to several general pathogenicity predictors:
- AlphaMissense 0.9229
- PolyPhen 0.997
- SIFT 0.01 (harm score 0.99)

Yet these tools do not identify the **BUBR1 low-abundance mechanism** on experimentally labeled BUBR1 variants.

The clearest example is AlphaMissense:
- N1002K score = 0.9229
- abundance-class AUC = 0.464
- LOO balanced accuracy = 0.268

Therefore:

> A high pathogenicity-prediction score for N1002K cannot be translated into a claim that the mutant protein is unstable or abundance-limited.

## Mechanistic conclusion

`N1002K_ABUNDANCE_CLASS = AMBIGUOUS`

The proteostasis/arimoclomol branch remains a falsifiable experimental hypothesis but cannot be promoted
as allele-matched causal rescue from computational evidence.

The highest-information experiment remains direct measurement of:
1. BUBR1 abundance;
2. N1002K half-life;
3. kinetochore localization;
4. SAC function;
5. chromosome missegregation per completed division.

## Important distinction: abundance prediction vs ACMG pathogenicity prediction

This negative abundance calibration does **not** invalidate AlphaMissense for ACMG PP3.

The ClinGen SVI pathogenicity calibration asks a different question: pathogenic vs benign missense variation.
Under the 2025 ClinGen SVI AlphaMissense calibration, a score in the range 0.906–0.971 corresponds to
PP3_Moderate.

N1002K AlphaMissense = 0.9229, so it qualifies for **PP3_Moderate** in a generic ACMG/AMP framework
unless a BUB1B-specific specification supersedes the general calibration.

No BUB1B-specific ClinGen VCEP specification was identified in the current search.

## Final decision

- abundance/stability inference: **AMBIGUOUS**
- general pathogenicity computational evidence: **PP3_Moderate**
- no contradiction exists because the two analyses address different biological questions.
