# NB10 v1.0.1 result summary

Synthetic operating-characteristic audit; no biological efficacy result is claimed.

## 4 biological replicates, 150 completed divisions/replicate
- NO_RESCUE: clean-rescue call rate 0.035
- TRUE_RESCUE_SMALL: clean-rescue call rate 0.172
- TRUE_RESCUE_MODERATE: clean-rescue call rate 0.485
- TRUE_RESCUE_STRONG: clean-rescue call rate 0.680
- CYTOSTASIS_ONLY: clean-rescue call rate 0.000
- APPARENT_RESCUE_WITH_CYTOSTASIS: clean-rescue call rate 0.000
- APPARENT_RESCUE_WITH_SELECTIVE_KILLING: clean-rescue call rate 0.000

## 6 biological replicates, 150 completed divisions/replicate
- NO_RESCUE: clean-rescue call rate 0.039
- TRUE_RESCUE_SMALL: clean-rescue call rate 0.251
- TRUE_RESCUE_MODERATE: clean-rescue call rate 0.689
- TRUE_RESCUE_STRONG: clean-rescue call rate 0.860
- CYTOSTASIS_ONLY: clean-rescue call rate 0.000
- APPARENT_RESCUE_WITH_CYTOSTASIS: clean-rescue call rate 0.000
- APPARENT_RESCUE_WITH_SELECTIVE_KILLING: clean-rescue call rate 0.000

## 8 biological replicates, 150 completed divisions/replicate
- NO_RESCUE: clean-rescue call rate 0.035
- TRUE_RESCUE_SMALL: clean-rescue call rate 0.305
- TRUE_RESCUE_MODERATE: clean-rescue call rate 0.805
- TRUE_RESCUE_STRONG: clean-rescue call rate 0.951
- CYTOSTASIS_ONLY: clean-rescue call rate 0.000
- APPARENT_RESCUE_WITH_CYTOSTASIS: clean-rescue call rate 0.000
- APPARENT_RESCUE_WITH_SELECTIVE_KILLING: clean-rescue call rate 0.000

Interpretation:
- The replicate-level one-sided Welch gate reduces null false-positive rate below 5% in all tested designs.
- Cytostasis and selective-killing scenarios have clean-rescue call rate 0 because of explicit hard gates.
- At 4 biological replicates and 150 divisions/replicate, a synthetic 40% true relative reduction is detected in ~47.5% of runs; 50% in ~66.7%.
- At 8 biological replicates and 150 divisions/replicate, the same call rates rise to ~80.8% and ~94.8%.
- Increasing independent biological replicates is substantially more valuable than only counting more divisions once replicate heterogeneity dominates.
- The 25% RRR gate is a simulation operating point, not a validated biological threshold.