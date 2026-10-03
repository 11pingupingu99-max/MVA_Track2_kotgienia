# F0 design addendum v1.1.0

This addendum supersedes the interpretation of `>=4 biological replicates` as a target sample size.

- **Hard minimum QC floor:** 4 independent biological replicates.
- **Preregistered target for the principal F0 comparison:** 8 independent biological replicates when feasible.
- **Primary endpoint:** chromosome missegregation per completed division.
- **Mechanism design:** abundance-matched WT vs N1002K across an expression series; no single 30% WT threshold defines mechanism class.
- **Reporting:** control and treated rates, absolute difference, relative reduction, **95% confidence interval at biological-replicate level**, inferential p-value, completed-division output, apoptosis, and the final clean-rescue decision.

Four replicates remain a floor because NB10 v1.0.1 gives only ~48.5% clean-rescue call probability for a synthetic moderate effect at 150 divisions/replicate, versus ~80.5% at 8 replicates under the stated model.
