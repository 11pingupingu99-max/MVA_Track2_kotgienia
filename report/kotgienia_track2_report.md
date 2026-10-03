# Rare Disease, Real Kid: MVA Hackathon 2026: Track 2 Final Report v1.6.1

## Mechanism-gated rescue for an unresolved BUB1B/MVA hypothesis
### Coverage, exposure and falsification before therapeutic claims

**Case hypothesis:** BUB1B L737* + N1002K; phase unresolved.  
**Track 1 automated validation:** 100/100 rank points; F-max 1.000 at EPCR 0.78 (scorer-confirmed against the challenge answer key).  
**Interpretation of that score:** it validates the genetic ranking used as the Track 2 input; it does not validate cis/trans phase, the N1002K molecular mechanism, or any drug hypothesis.  
**N1002K:** missense VUS; direct mechanism unresolved.  
**Causal rescue benchmark:** WT BUB1B restoration.  
**Therapeutic status:** preclinical hypothesis generation only.

## For the family and clinical team: what this work changes now

The genome analysis has produced one leading explanation, but it has **not** proved the diagnosis and it has **not** identified a treatment to start. The strongest current hypothesis is that the child carries two relevant BUB1B changes, L737* and N1002K. The highest-value next test remains parental genotyping of both variants. If the two variants are in trans, the recessive BUB1B model becomes substantially stronger. If they are in cis, the search for another disease-causing allele should reopen.

After phase, the decisive biological question is whether N1002K mainly reduces the amount or stability of BUBR1, mainly impairs function at a given protein amount, or does both. Drug testing should wait for that distinction. This Track 2 submission therefore provides a **predefined mechanism-discrimination framework, exposure gates and falsification rules**, not a clinical treatment recommendation.

## 0. Gate 0: phase determines whether the disease model is admissible

The two prioritized BUB1B loci in the project coordinate set are chr15:40209701 and chr15:40220612, **10,911 bp apart**. Ordinary short-read read-backed phasing is not treated as capable of directly spanning this pair. Phase is therefore not a footnote; it is the first hard gate in the Track 2 decision tree.

Three practical resolution routes are available: (1) parental/trio genotyping of both variants, the simplest and preferred route; (2) long-read sequencing with ONT or PacBio HiFi; or (3) long-range PCR spanning the interval followed by amplicon sequencing. Exact local cost and turnaround depend on laboratory and jurisdiction, so this report does not present a universal quotation.

The interpretation is frozen prospectively:

- **TRANS:** the compound-heterozygous BUB1B model remains coherent and the `L737*/N1002K` F0M arm is the appropriate disease-context genotype.
- **CIS:** the current pair does not constitute a biallelic recessive explanation. The search for a second causal allele or gene must reopen; the compound F0M arm cannot be presented as the established patient genotype.
- **UNRESOLVED:** all downstream mechanism and drug statements remain conditional.

For the family and clinical team, this makes parental genotyping the highest-value next diagnostic test before any therapeutic interpretation.

## 1. Why the therapeutic branch is conditional

The computational work narrowed rather than solved the mechanism.

- The leading pair is L737* + N1002K.
- L737* is a credible loss-of-function anchor.
- N1002K remains a VUS.
- cis/trans phase remains unresolved.
- gene-specific predictor calibration did **not** establish a BUBR1 abundance defect.
- the RNA-layer audit did not support a primary N1002K RNA mechanism.

The prospective F0 design is therefore no longer based on a single 30% WT abundance cutoff. The revised abundance-matched experiment compares WT and N1002K across approximately 10%, 30%, 50%, 75% and 100% WT BUBR1 abundance. The primary question is:

> At the same measured BUBR1 abundance, does N1002K still produce more chromosome-segregation error than WT?

The mechanism classes are:

**ABUNDANCE-DOMINANT:** N1002K reduces abundance and/or half-life, but function approaches WT when mutant protein amount is matched to WT.

**FUNCTION-DOMINANT:** a functional defect persists at matched abundance.

**MIXED:** N1002K both reduces abundance and retains a residual functional defect after abundance matching.

**INDETERMINATE:** assay precision or confidence intervals do not distinguish these states.

The primary cellular endpoint remains **chromosome missegregation per completed division**. WT BUB1B restoration remains the causal positive rescue benchmark.

![Figure 1. Mechanism-gated Track 2 decision architecture. The scorer-confirmed Track 1 pair is an input, not a therapeutic validation. Phase and abundance-matched F0 determine whether drug repurposing is admissible. Exposure and false-rescue gates precede any rescue claim.](track2_decision_architecture.png)

**Figure 1. Mechanism-gated Track 2 decision architecture.** A FUNCTION-DOMINANT result ends approved-drug repurposing in the audited space and redirects the programme toward functional correction.

## 2. Arimoclomol: regulatory, clinical and exposure context

Arimoclomol remains a biologically interesting proteostasis-branch candidate, but this report deliberately lowers the confidence attached to it because regulatory, efficacy and exposure evidence are mixed.

### United States

The FDA approved Miplyffa (arimoclomol) in 2024, in combination with miglustat, for neurological manifestations of Niemann-Pick disease type C in adults and children aged 2 years and older.

### European Union

The EU history is materially different. A prior EMA application was withdrawn in 2022 after unresolved efficacy concerns. A new application under the name Meplyffa received a negative CHMP opinion in July 2026, followed by re-examination. This regulatory discordance weakens any argument based on demonstrated clinical efficacy while leaving the heat-shock/proteostasis mechanism available for experimental testing.

### Clinical trials

The earlier SOD1 ALS study was small and imprecise. More importantly, the 2024 phase III ORARIALS-01 trial included 239 participants in the modified intention-to-treat population and did **not** show a difference in the primary Combined Assessment of Function and Survival outcome (p=0.62). This does not test MVA and does not falsify a BUBR1-specific cellular hypothesis, but it prevents use of ALS as a positive efficacy precedent.

In the published NPC phase 2/3 trial, the 12-month 5-domain NPCCSS result numerically favoured arimoclomol, but EMA subsequently judged the submitted evidence insufficiently robust for a positive EU benefit-risk conclusion.

### Exposure gate

NB09 added a quantitative exposure requirement. In pediatric NPC patients receiving recommended regimens, estimated steady-state arimoclomol Cmax is approximately **523 ng/mL**. Conversion uses the arimoclomol free-base molecular weight (**313.78 g/mol**), because the label reports arimoclomol concentrations rather than citrate-salt mass. This gives about **1.67 µM total** and, using approximately 10% protein binding, **1.50 µM nominally unbound** drug. The prescribing information lists arimoclomol citrate at **505.90 g/mol**; applying that salt molecular weight to 523 ng/mL would give about **1.03 µM**. The direction of the exposure-gap conclusion is unchanged under either conversion.

Some nonclinical proteostasis experiments motivating the project use concentrations in the 100-400 µM range. Those experiments are not directly comparable to MVA, but the nominal exposure gap is large enough that arimoclomol can no longer be described as a strong lead simply because it is approved and mechanistically attractive.

**Current disposition:** mechanistically interesting, but requires a clinically anchored low-µM exposure-response experiment before any higher-concentration mechanistic probe can be interpreted as translationally plausible.

## 3. NB08R2: what the drug databases actually show

The original NB08 prototype used composite scores and weight perturbations. Those numerical rankings are rejected and are not used for final candidate selection.

The first corrective audit separated `HIT`, `NO_HIT`, `NOT_RUN`, `ERROR` and `NO_TARGET_RESOLVED`, filtered DrugCentral against an approved-drug snapshot, and deduplicated structures by DrugCentral `STRUCT_ID`. A second precision audit then removed fuzzy ChEMBL target search and used:

`frozen core ChEMBL target -> exact UniProt accession -> target_components__accession`

This exact component-aware mapping resolved the principal review concern.

### 3.1 Audited approved-mechanism coverage

The final v1.0.2 result is:

| Target | Role | ChEMBL exact target representations | ChEMBL approved mechanism parent drugs | DrugCentral approved structures |
|---|---|---:|---:|---:|
| HSF1 | proximal | 1 | 0 | 0 |
| HSP90AA1 | proximal | 8 | 0 | 1 |
| PSMB5 | probe only | 7 | 3 | 2 |
| SIRT2 | proximal | 1 | 0 | 0 |
| CREBBP | exploratory | 1 | 0 | 0 |
| AURKB | probe only | 2 | 0 | 2 |
| PPP2CA | proximal | 5 | 0 | 0 |
| PLK1 | antitarget | 2 | 0 | 0 |
| CDK1 | antitarget | 2 | 0 | 1 |
| TTK | antitarget | 1 | 0 | 1 |
| JAK1 | downstream | 4 | 8 | 4 |
| JAK2 | downstream | 3 | 9 | 4 |
| MTOR | downstream | 5 | 1 | 2 |

The PSMB5 positive-control branch correctly recovers approved proteasome inhibitors, including bortezomib, carfilzomib and ixazomib-class mechanisms in ChEMBL. The earlier statement that PSMB5 had no ChEMBL mechanism coverage was therefore wrong and is withdrawn.

The ChEMBL activity channel remains explicitly **NOT_RUN**, not zero.

Across the **13 prespecified target symbols**, the exact-component audit recovered **14 unique approved ChEMBL parent-drug identifiers** and **11 unique approved DrugCentral structures** after source-specific deduplication. These are deduplicated source-specific totals; they do not equal the row-wise sums in the table because JAK1/JAK2 and related branches share approved drugs. The counts are reported separately rather than summed because the two resources use different identifiers and contain overlapping drugs. This is the auditable size of the approved-drug mechanism space actually interrogated by NB08R2.

### 3.2 Revised interpretation

The result is not that "drug databases fail." The narrower and defensible conclusion is:

> Target-centric approved-drug databases recover direct inhibitors and database-rich downstream kinases well, but they are poorly matched to several desired-direction, indirect or localisation-specific rescue mechanisms such as HSF1 activation and BUBR1-dependent PP2A-B56 recruitment.

This matters because **annotation density is not therapeutic credibility**. JAK1/JAK2 are database-rich, but that does not make downstream JAK inhibition a causal rescue for a chromosome-segregation defect. Conversely, poor approved-target coverage for HSF1 or localized PP2A does not prove those biological axes are irrelevant.

No final NB08 ranking is issued.

## 4. What the coverage map rules out or demotes

### Proteasome inhibition

The repaired audit correctly recovers approved proteasome inhibitors. This makes proteasome inhibition a useful positive control for target-mapping completeness, not a chronic MVA therapy. Oncology-grade proteasome inhibition can alter BUBR1 turnover biology but has an unfavourable chronic-toxicity and proliferation profile for this use.

**Disposition:** mechanistic probe / chronic-therapy hard stop.

### SIRT2 and NAD+

SIRT2-mediated BUBR1 deacetylation and stabilization remains biologically well motivated, but the audited approved-drug layer did not identify a qualifying direct SIRT2 lead in the desired activation direction. This negative database result is narrower than the biological hypothesis: it does not test whether increasing NAD+ availability can increase BUBR1 abundance. Likewise, the exploratory NB13 transcriptomic analysis did not measure NAD+, SIRT2 activity or BUBR1 protein abundance.

Mechanistically, CBP-mediated acetylation of BUBR1 K668 promotes ubiquitination/degradation, whereas SIRT2-dependent deacetylation stabilizes BUBR1. In the hypomorphic `BubR1H/H` mouse model, SIRT2 overexpression or NAD+ precursor intervention increased BubR1 abundance, and SIRT2 overexpression increased median lifespan. This is most relevant to the **ABUNDANCE-DOMINANT** branch, not to a protein with a persistent matched-abundance functional defect [9].

The sign of the intervention cannot be assumed from K668 alone. BUBR1 acetylation at K250 has a different mitotic role: loss of K250 acetylation destabilizes BUBR1 and accelerates mitosis, while an acetylation-mimetic form delays chromosome segregation. Systemic NAD+/sirtuin manipulation therefore cannot be reduced to a one-directional 'more deacetylation is better' model [10].

The branch is prospectively constrained by three rules: (1) it opens only if F0 is ABUNDANCE-DOMINANT; (2) abundance increase is not success unless chromosome missegregation per completed division and mitotic timing improve; and (3) mechanistic attribution requires **SIRT2 epistasis**, so any putative NAD+-raising effect must disappear or materially attenuate after SIRT2 suppression. Nicotinamide and nicotinic acid are not treated as interchangeable interventions.

**Disposition:** open conditional cell-model hypothesis if F0 = ABUNDANCE-DOMINANT; no approved direct rescue lead and no human intervention proposed.

### PP2A-B56 / Aurora B

BUBR1-dependent PP2A-B56 recruitment and Aurora-B opposition are directly relevant to chromosome congression. General Aurora-B or mitotic kinase inhibition is not equivalent to restoring BUBR1-localized phosphatase control and risks suppressing the machinery required for accurate mitosis.

**Disposition:** causal-pathway probes and antitargets, not chronic rescue leads.

**FUNCTION-DOMINANT branch:** if abundance-matched F0 shows a persistent N1002K functional defect, **no approved drug in the audited target space is currently a credible causal rescue**. The correct Track 2 output in that branch is a functional-correction research programme, not a repurposing claim. This is specified prospectively so that a negative mechanism result cannot be converted into a weaker drug recommendation after the fact.

### TTK/MPS1, PLK1 and CDK1

These functions must be preserved for normal mitosis. Their inhibition cannot be credited as rescue merely because abnormal mitoses disappear.

**Disposition:** preserve-axis antitargets.

### JAK/mTOR/ROS

These are database-covered downstream branches. They remain comparators unless chromosome segregation itself improves.

**Disposition:** downstream ceiling, not causal rescue by default.

## 5. Exposure-filtered, non-ranked candidate panel

No candidate is treated as effective in BUB1B/MVA. The panel is admitted only if F0 establishes a mechanism that the drug could plausibly rescue.

### Arimoclomol

Heat-shock-response co-inducer with an approved indication in NPC, but now explicitly downgraded because of the large nominal exposure gap and negative ORARIALS-01 efficacy result.

**Status:** testable only with a clinically anchored low-µM range and explicit exposure-response interpretation.

### Sodium phenylbutyrate / 4-PBA

Approved for urea-cycle disorders and widely used experimentally as a chemical chaperone. NB09 estimates phenylbutyrate Cmax after a 5 g fasting dose at about **1.33 mM**, whereas one chemical-chaperone exemplar used 5 mM. That nominal gap is substantially smaller than for arimoclomol, although intracellular exposure, high protein binding, HDAC activity and polypharmacology remain major confounders.

**Status:** pharmacologically more plausible than a simple "approved vs experimental" comparison would suggest, but mechanistically non-specific.

### Geranylgeranylacetone / teprenone

Rather than inferring plasma overlap, the strongest evidence is human pharmacodynamics: clinical dosing has increased HSP70 in gastric mucosa.

**Status:** useful HSP-induction comparator with direct human target-engagement precedent, but no evidence of BUBR1 rescue.

### Ambroxol

Human CNS exposure and target engagement exist in the GCase system, but classic GCase chaperone experiments use concentrations far above nominal CSF concentrations. The pharmacology is also target-specific to GCase.

**Status:** secondary pharmacological-chaperone comparator, not a direct BUBR1 lead.

### Drug-test rule

A candidate is credited only if it:

1. increases the relevant BUBR1 quantity or function readout;
2. reduces chromosome missegregation **per completed division**;
3. does not reduce completed-division output enough to explain the apparent improvement;
4. does not selectively kill abnormal cells;
5. does not merely improve downstream stress;
6. shows an exposure-response relationship that includes clinically relevant concentrations where such exposure data exist.

No human dosing recommendation is made.

## 6. F0 rescue logic and NB10 false-rescue audit

The F0 redesign adds abundance matching and a `MIXED` mechanism class. WT BUB1B restoration is still necessary as the causal positive benchmark, but WT rescue alone does not prove that stabilizing N1002K will work.

A proteostasis drug is admitted only if:

1. N1002K abundance and/or half-life is reduced, **and**
2. raising N1002K abundance itself moves function toward WT on the abundance-function curve.

If abundance rises without functional improvement, a stabilizer or chaperone is not credited as causal rescue.

NB10 then stress-tested the rescue-decision architecture using synthetic beta-binomial scenarios. A clean rescue call in v1.0.1 required:

- at least 25% relative reduction in missegregation per completed division as a simulation operating point;
- a one-sided replicate-level Welch p <= 0.05;
- no >10% reduction in completed-division output;
- no >10 percentage-point increase in apoptosis;
- at least 100 completed divisions per biological replicate.

The table separates the decision threshold from the simulated truth: **25% relative reduction** is the clean-rescue decision threshold, while the **moderate synthetic-rescue scenario assumes a 40% true relative reduction** and the strong scenario assumes a 50% true relative reduction.

At 150 completed divisions per replicate:

| Biological replicates | Null clean-rescue call | Moderate synthetic rescue (40% true RRR) | Strong synthetic rescue (50% true RRR) |
|---:|---:|---:|---:|
| 4 | 3.5% | 48.5% | 68.0% |
| 6 | 3.9% | 68.9% | 86.0% |
| 8 | 3.5% | 80.5% | 95.1% |

Cytostasis-only, apparent rescue plus cytostasis, and apparent rescue plus selective killing all produced **0 clean-rescue calls** under the hard gates.

These are operating characteristics of a synthetic model, not efficacy data. Their practical implication is that **four biological replicates are a minimum QC floor rather than a high-power design for moderate effects**. The preregistered execution target is therefore **8 independent biological replicates for the principal F0 comparison**, with 4 retained only as the hard minimum below which the experiment is not interpreted as a clean mechanistic test. Increasing independent biological replicates is more valuable than only counting more mitoses once replicate heterogeneity dominates.

For every result-bearing F0 comparison, the report must show the control and treated missegregation rates, the absolute difference, the relative reduction, and a **95% confidence interval** derived at the biological-replicate level (bootstrap or a model that preserves replicate structure), alongside the inferential p-value and the binary rescue decision. Pass/fail alone is not an adequate result.

## 6A. NB17 final pre-registration and assay-validity audit

NB17 freezes the remaining design choices before any N1002K unblinding or result-bearing F0 acquisition. It generates no biological data and does not re-rank drugs.

### 6A.1 ClinGen functional-evidence ceiling

The frozen F0V panel contains **6 B/LB missense controls and 5 P/LP truncating controls**, i.e. **11 total**. Brnich et al. report that, in the absence of rigorous statistical calibration, at least 11 total pathogenic and benign validation controls are required to reach moderate-level functional evidence [11].

OddsPath is calculated as:

`OddsPath = [P2 x (1 - P1)] / [(1 - P2) x P1]`

where `P1` is the proportion of pathogenic variants in the modeled control data and `P2` is the posterior proportion of pathogenic variants within the relevant assay-readout group. Following the Brnich treatment of perfect separation, exactly one misclassified variant is added to each readout set. The modeled data therefore contain 6 pathogenic and 7 benign observations, giving `P1 = 6/13 = 0.462`.

Under perfect separation:

| Direction | P2 | OddsPath | ClinGen-equivalent strength |
|---|---:|---:|---|
| PS3, abnormal readout | 5/6 = 0.833 | **5.83** | Moderate (>4.3); Strong (>18.7) not reached |
| BS3, normal readout | 1/7 = 0.143 | **0.194** | Moderate (<0.23); Strong (<0.053) not reached |

Strong functional evidence is therefore prospectively inadmissible from this panel even under ideal separation. The conclusion is insensitive to the prior convention: using the uncorrected control-set proportion `P1 = 5/11` gives PS3 6.00 and BS3 0.200, while a balanced-prior simplification `P1 = 0.5` gives PS3 5.00 and BS3 0.167. All three conventions remain Moderate in both directions.

Two asymmetries are frozen prospectively. First, the **benign direction has little numerical headroom**: approximately 0.19-0.20 against a Moderate boundary of `<0.23`. Second, QC loss is governed by the control-count minimum rather than by the reduced-panel OddsPath alone. Losing any single real control leaves **10**, below the stated 11-control minimum for count-based Moderate evidence, so Moderate strength is not claimed from a 10-control panel.

For completeness, if one P/LP control is lost, a `4 P/LP + 6 B/LB` reduced panel gives approximately PS3 **5.60** but BS3 **0.233**; the pathogenic-direction arithmetic remains Moderate while the benign-direction arithmetic falls to Supporting. If one B/LB control is lost, `5 P/LP + 5 B/LB` gives approximately PS3 **5.00** and BS3 **0.200**, but again fails the 11-control minimum. Evidence strength will be calculated from the actual observed calibration rather than inferred from nominal counts, and if the control distributions do not support defensible binary separation, no PS3/BS3 call is forced.

NB17 **v1.0.1** supersedes v1.0.0 for these OddsPath calculations.
### 6A.2 Mechanism compatibility of the 11 controls

The frozen manifest contains six missense B/LB controls (`T40M, V4M, V618A, N1004S, R349Q, E390D`) and five truncating P/LP controls (`R194*, R120*, H856fs, S788fs, R80_Y81ins*`). None is encoded in the frozen panel as a splice/promoter/UTR control. All 11 can remain in the **protein-function** validation layer, but the five truncating controls have a strict scope limitation: cDNA complementation bypasses endogenous transcript processing and therefore cannot validate their RNA/NMD mechanism.

This distinction is recorded explicitly so that a protein-function assay is not later described as validating endogenous RNA processing. Q467H remains excluded from this calibration because its known disease mechanism is splice-mediated.

### 6A.3 Frozen statistical analysis plan

The primary F0M question is: **at the same measured BUBR1 abundance, does N1002K differ functionally from WT?** Measured abundance is analysed continuously; nominal 10/30/50/75/100% expression targets are design targets, not five independent primary hypotheses.

The preferred primary model is binomial or beta-binomial at the completed-division level with measured abundance, variant, and variant-by-abundance interaction, while preserving biological-replicate structure. The primary test is two-sided at alpha 0.05 because either functional direction is possible. Every result-bearing comparison must report the model estimate, absolute rate difference, relative effect where estimable, and a **95% confidence interval** at the biological-replicate level.

Only the matched-abundance WT-versus-N1002K missegregation contrast is primary. Secondary endpoint families use Holm adjustment. The normal/abnormal F0V threshold is derived only from frozen controls and locked before N1002K unblinding. If the control distributions do not support defensible binary separation, no PS3/BS3 call is forced.

Mechanism classification remains `ABUNDANCE-DOMINANT / FUNCTION-DOMINANT / MIXED / INDETERMINATE`, with no post-hoc threshold tuning around N1002K. Four independent biological replicates remain the hard QC floor; **8 are the preregistered target** for the principal comparison.

### 6A.4 Reproducibility freeze

The implementation addendum specifies U2OS (RRID CVCL_0042) for F0V and hTERT-RPE1 (RRID CVCL_4388) for F0M. Before wet-lab acquisition, the performing laboratory must version the RNAi sequences, RNAi-resistant BUB1B plasmid maps and sequence hashes, F0M CRISPR guide/donor sequences and clone IDs, antibody identifiers, imaging parameters, plate-randomization seed, blinding key and unblinding procedure. Raw scoring preserves lagging chromosomes, anaphase bridges and micronuclei as separate event classes even if the preregistered primary endpoint uses a composite missegregation-per-completed-division measure.

## 7. Assertion-aware validation: condition and mechanism matter

### R814H

The broad VCV-level aggregate should not be used as a disease-specific truth. For `BUB1B c.2441G>A (p.Arg814His)`, the current MVA1-specific RCV is Pathogenic/Likely pathogenic with multiple submitters and no conflicts.

This creates an important correction to the earlier summary of the frozen ClinVar dataset: the statement "0 P/LP missense in residues 766-1050" is valid only for the **specific VCV-level aggregation/filter used in that frozen audit**. It is not a valid general statement about disease-specific ClinVar assertions in that region.

The mechanism of this discordance is generalizable. ClinVar VCV records aggregate submissions by **variant regardless of condition**, whereas RCV records aggregate by **variant-condition pair**. In this BUB1B example, the Likely benign assertion belongs to the separately coded *premature chromatid separation trait* rather than to MVA1. Recessive genes with a separately coded carrier or heterozygous trait can therefore acquire an apparent VCV-level conflict even when the disease-specific RCV remains P/LP. A pipeline that removes variants solely because the VCV aggregate is conflicting can consequently discard disease-relevant assertions; condition-aware RCV/SCV review is required.

### Q467H

The MVA1 Likely pathogenic assertion is splice-mediated. A cDNA complementation assay bypasses that mechanism and could make a clinically abnormal allele appear protein-function-normal.

**Consequence:** validation controls must match both **condition** and **molecular mechanism**.

## 8. Quantified ClinVar bottleneck in BUB1B

Frozen ClinVar snapshot: **23 September 2026**.

The project audit contained:

- total BUB1B audit records: **2,471**
- missense_or_other_protein_change: **1,497**
- VUS within that class: **1,426**
- records in UniProt-annotated residues 766-1050: **405**
- VUS in that region: **387**

The previous `P/LP missense = 0` value is retained only as a descriptor of that specific frozen VCV-level aggregation and filter. Disease-specific RCV review demonstrates that at least R814H is P/LP for MVA1. This is precisely why assertion-aware RCV-level curation is part of the assay-design workflow.

## 9. Scalability beyond BUB1B

A targeted portability demonstration on six CEP57/MVA2 ClinVar RCVs separates straightforward loss-of-function/splice controls from benign, VUS and conflicting missense records. This is intentionally not an exhaustive CEP57 census.

The purpose is methodological: condition-specific assertion parsing and mechanism matching are portable beyond BUB1B and prevent clinically heterogeneous records from being treated as equivalent functional standards.

## 10. Exploratory extension: mitochondrial context, BUB1B restoration and partial correction

NB11-NB13 were added as an exploratory annex after the main repurposing framework was already defined.

### NB11: BubR1 model transcriptomes

Six contrasts were analysed with gene-level differential expression and sample-level module tests. No module contrast passed the prespecified combination of FDR <= 0.05 and stable effect > 0.1. OXPHOS and mitochondrial-translation module directions were negative across the examined contrasts, but the analyses share controls, involve small sample sizes, different tissues and alleles, and do not measure mitochondrial function, NAD+, SIRT2 activity or treatment efficacy.

**Interpretation:** mitochondrial function remains worth measuring in a future rescue experiment, but NB11 does not establish a general mitochondrial defect in BUB1B/MVA.

### NB12: feasibility of restoring BUB1B

RefSeq `NM_001211.6` contains a 3153-nt CDS encoding 1050 aa, consistent with UniProt O60566. Under an assumed 4700-nt ssAAV genome budget and two 145-nt ITRs, approximately **1257 nt** remain for all non-CDS regulatory elements. Eleven of sixteen explicitly hypothetical size configurations fit that arithmetic envelope.

This is a payload-budget calculation, not a vector design. No promoter sequence, guide RNA, editing window, off-target profile, delivery strategy, expression-level safety or durability in dividing cells has been established. Full BUB1B does not fit a typical self-complementary AAV budget.

**Interpretation:** gene restoration is plausible enough to remain a research direction, but NB12 does not define a therapy.

### NB13: niacin response as a metabolic adjunct

The public niacin RNA-seq dataset contains 29 libraries, not 29 independent participants. Complete paired comparisons included four patient pairs at 4 months and three at 10 months. With four pairs, the minimum two-sided sign-flip p is 0.125; with three pairs it is 0.25. Therefore a p < 0.05 confirmation was mathematically impossible before FDR.

No module contrast passed the prespecified FDR/effect gate. OXPHOS and mitochondrial-translation effects did not show a convincing reversal of the BubR1-model directions. RNA expression also does not measure NAD+, SIRT2 activation, BUBR1 stabilization or mitochondrial respiration.

**Interpretation:** niacin remains a hypothesis-generating adjunct, not a supported rescue candidate.

### NB14-NB16: readthrough audit as a constraint, not a Track 2 lead

A final exploratory branch examined whether the public L737* nonsense allele creates a tractable readthrough question. NB14 confirmed the reference chemistry `TTA -> TGA (UGA)`, a 736-aa truncated product, and predicted EJC-dependent nonsense-mediated decay because the stop lies 73 nt upstream of the next exon junction. This is a mechanistic constraint, not a measurement of transcript abundance or spontaneous readthrough.

NB15 generated full-length products for possible amino-acid insertions at residue 737 and completed an ESM-2 sequence-plausibility analysis. The sequence-model scores are **not treated as functional evidence**. This is required for internal consistency: the preregistered NB04B calibration had already shown that generic pathogenicity/sequence-plausibility predictors, including ESM2-150M, did not recover the experimentally defined BUBR1 low-abundance class (`NO_PREDICTOR_CALIBRATED`). No sequence model has been calibrated here against BUBR1 checkpoint, kinetochore or chromosome-segregation function. Therefore the identity of a readthrough-inserted residue defines an experimental question, not a computational functional ranking. The correct endpoint remains matched-abundance testing of WT, L737W, L737C and L737R products.

NB16 integrated RNA availability, readthrough efficiency, protein stability and protein function into 432 hypothetical scenarios. These scenarios are not fitted to the patient and do not establish therapeutic efficacy. The branch produced **no therapeutic PASS for BUB1B-L737***. 2,6-diaminopurine is retained only as a mechanistic UGA-to-W probe, not as a Track 2 medication proposal.

An ACE-tRNA approach capable of inserting leucine at UGA is scientifically interesting because restoring Leu737 would recreate the wild-type residue at the L737* allele; CFTR models provide proof-of-concept that ACE-tRNA^Leu can rescue nonsense alleles in other diseases [18]. However, ACE-tRNA is an engineered experimental platform, not a market-approved medication, so it is **outside the scope of the present Track 2 proposal**. Its principal safety question is transcriptome-wide suppression of native UGA termination sites, particularly important in a cancer-predisposition syndrome. The existing `N1002K/WT` F0M arm already tests the key prerequisite for any one-allele correction concept: whether a WT copy paired with N1002K is functionally sufficient in the assay. No therapeutic correction threshold is inferred.

**Interpretation:** NB14-NB16 strengthen the submission by defining what would need to be measured before any readthrough claim is credible. They do not add a new treatment candidate to the core approved-drug panel.

### Future experiment

If a metabolic adjunct is pursued, the informative design is factorial:

1. control;
2. BUB1B restoration;
3. metabolic adjunct;
4. combination.

The study should separately quantify:

- BUBR1 abundance, localization and matched-abundance function;
- chromosome missegregation per completed division;
- completed-division output and cell death;
- mitochondrial respiration, spare respiratory capacity and redox state;
- tissue-model function where relevant.

Improved ATP or survival alone is not clean rescue.

### Partial-correction hypothesis

A separate future question is what fraction of cells must regain functional BUBR1 to improve tissue-level behaviour. This is conceptually related to mosaic correction but should not be assigned an arbitrary therapeutic percentage from simulation alone. BUBR1 acts cell-autonomously; corrected cells do not provide a functional spindle checkpoint to neighbouring cells, and preventing new segregation errors does not automatically remove pre-existing aneuploidies or reverse developmental consequences.

The XIST-based chromosome-silencing work in trisomy 21 provides an important proof that chromosome-scale dosage manipulation is experimentally possible, but MVA is fundamentally different because different cells can gain or lose different chromosomes and the underlying segregation defect continues to generate new errors. Chromosome silencing is therefore a future conceptual reference, not a current MVA rescue strategy.

## 11. Impact: what is actionable and what is not

### Actionable now

1. **Parental genotyping/Sanger of L737* and N1002K** remains the cheapest decisive test.
2. If trans is supported, perform the direct abundance-matched N1002K functional experiment.
3. Use WT BUB1B restoration as the causal positive benchmark.
4. If drug rescue is tested, include clinically anchored exposure ranges and the NB10 false-rescue gates.
5. Treat four biological replicates as the hard minimum QC floor; preregister **8 independent biological replicates** for the principal F0 comparison when feasible.

### Practical execution profile for F0

F0 is designed for a mammalian cell-biology / mitosis laboratory with quantitative fluorescence or live-cell imaging, standard transfection or complementation capability, and access to protein-quantification assays. As a planning estimate rather than a vendor quotation, a complementation-based pilot can be run in roughly **6-10 weeks** if constructs and cell lines are already available. A full abundance-matched, 8-biological-replicate study is more realistically **3-4 months**. If an endogenous isogenic N1002K line must first be generated and validated, the overall programme becomes approximately **4-6 months**. Direct consumables and core-imaging costs are expected to be on the order of **EUR 15,000-40,000** for the assay phase, excluding personnel and de novo cell-line engineering. The purpose of this estimate is to show operational scale, not to claim a fixed budget.

### Not actionable now

- no drug should be started from this report;
- no candidate has demonstrated BUB1B/MVA efficacy;
- N1002K should not be reclassified from computational evidence alone;
- niacin is not established as a metabolic rescue;
- AAV payload arithmetic is not a therapeutic vector design;
- ESM/readthrough sequence-model output is not BUBR1 functional evidence, and ACE-tRNA is outside the approved-medication scope of Track 2;
- negative bulk-blood mCA does not exclude cell-to-cell MVA.

The immediate value is therefore **diagnostic and experimental prioritisation**, not treatment selection.

## 12. Reproducibility, privacy and deletion commitment

The public repository contains only sanitized code, public-data analyses, source audits, aggregate handoffs and non-reconstructive findings. It excludes raw WGS/VCF/BAM/CRAM, genome-scale genotype tables, patient identifiers, private blinding keys, and notebook state or caches that contain genome-wide patient genotypes.

NB08R2 uses frozen DrugCentral snapshots and exact ChEMBL component-aware target resolution. The non-ClinVar case allele `c.3006T>G` is not transmitted to remote variant-annotation APIs in this branch.

A prior AlphaGenome branch used the official Google DeepMind AlphaGenome client/API on **two preselected patient-derived BUB1B variant coordinates and alleles** for an orthogonal RNA/cis-regulatory hypothesis audit. This was limited variant-level case information. No raw WGS/VCF, genome-wide genotype table, sample identifier, clinical record, or unrelated patient variant table was sent. AlphaGenome did not determine the Track 1 ranking and did not establish a primary RNA mechanism for N1002K.

The hackathon deletion obligation is treated as a project requirement. Within 30 days of hackathon close, all controlled genomic data and participant-controlled copies, slices, reformats, genotype-scale intermediate tables, caches and notebook state carrying the child's genome will be deleted from participant-controlled systems. The retained public materials are limited to allowed findings such as the ranked candidate variants, HPO terms, mechanism analyses, drug hypotheses, sanitized code, report and pitch. Deletion will then be confirmed to the organisers by email as required.

## 13. AI-assistance disclosure

**OpenAI ChatGPT (Plus)** was used for code review, literature evaluation, debugging and drafting on sanitized/public project materials. **No private patient genomic data, raw WGS/VCF, private genotype tables, patient identifiers, or the non-public case allele table were provided to or read by ChatGPT.**

The submitter confirms that ChatGPT's **"Improve the model for everyone" setting was disabled during the relevant project conversations**. This confirmation was recorded on 3 October 2026.

**Google DeepMind AlphaGenome** is disclosed separately because an earlier hypothesis-audit branch received exactly **two preselected patient-derived BUB1B variant coordinates and alleles**. No raw WGS/VCF, genome-wide genotype table, sample identifier, clinical record, or unrelated patient variant table was transmitted. AlphaGenome did not determine the Track 1 ranking and did not establish a primary N1002K RNA mechanism.
## Final proposal

The final Track 2 proposal is not "arimoclomol is the answer."

It is:

**phase -> abundance-matched mechanism -> exact approved-drug coverage -> exposure plausibility -> causal rescue -> false-rescue hard gates -> conditional, non-ranked testing**

If F0 shows an abundance-dominant or mixed mechanism in which raising N1002K abundance restores function, proteostasis candidates can be tested.

If abundance matching fails to restore N1002K function, a stabilizer is not credited as causal rescue. In that FUNCTION-DOMINANT branch, no approved drug in the audited target space currently qualifies as a credible causal rescue; the output is a functional-correction research programme rather than a repurposing recommendation.

If phase or F0 remains unresolved, no therapeutic claim is made.

The strongest result of the project is therefore not a drug name. It is a **falsifiable decision architecture** that distinguishes genetic prioritisation, mechanism, pharmacological plausibility and genuine rescue.

## References

1. FDA / DailyMed. MIPLYFFA (arimoclomol) prescribing information, including pediatric pharmacokinetics, protein binding and arimoclomol-citrate molecular weight.
2. EMA. Miplyffa/Meplyffa regulatory assessments and 2026 CHMP proceedings.
3. Benatar M et al. Safety and efficacy of arimoclomol in early ALS (ORARIALS-01). Lancet Neurol. 2024. PMID 38782015.
4. Benatar M et al. Randomized trial of arimoclomol in rapidly progressive SOD1 ALS. Neurology. 2018. PMID 29367439.
5. Mengel E et al. Arimoclomol in Niemann-Pick disease type C. J Inherit Metab Dis. 2021. PMID 34418116.
6. Fog CK et al. Arimoclomol and glucocerebrosidase proteostasis. EBioMedicine. 2018. PMID 30497978.
7. Suijkerbuijk SJE et al. Molecular causes for BUBR1 dysfunction in MVA. Cancer Res. 2010. PMID 20516114.
8. Xu P, Raetz EA, Kitagawa M, Virshup DM, Lee SH. BUBR1 recruits PP2A via the B56 family of targeting subunits to promote chromosome congression. Biol Open. 2013;2(5):479-486. PMID 23789096; PMCID PMC3654266; DOI 10.1242/bio.20134051.
9. North BJ, Rosenberg MA, Jeganathan KB, Hafner AV, Michan S, Dai J, Baker DJ, Cen Y, Wu LE, Sauve AA, van Deursen JM, Rosenzweig A, Sinclair DA. SIRT2 induces the checkpoint kinase BubR1 to increase lifespan. EMBO J. 2014;33(13):1438-1453. PMID 24825348; PMCID PMC4194088; DOI 10.15252/embj.201386907.
10. Choi E, Choe H, Min J, Choi JY, Kim J, Lee H. BubR1 acetylation at prometaphase is required for modulating APC/C activity and timing of mitosis. EMBO J. 2009;28(14):2077-2089. PMID 19407811; PMCID PMC2684026; DOI 10.1038/emboj.2009.123.
11. Brnich SE, Abou Tayoun AN, Couch FJ, Cutting GR, Greenblatt MS, Heinen CD, Kanavy DM, Luo X, McNulty SM, Starita LM, Tavtigian SV, Wright MW, Harrison SM, Rehm HL, Fowler DM. Recommendations for application of the functional evidence PS3/BS3 criterion using the ACMG/AMP sequence variant interpretation framework. Genome Med. 2020;12(1):3. PMID 31892348; PMCID PMC6938631; DOI 10.1186/s13073-019-0690-2.
12. NCBI ClinVar. BUB1B p.Arg814His and MVA1, RCV000007160.
13. DrugCentral. Drug-target interaction and approved-drug resources.
14. ChEMBL. Mechanism and target-component resources.
15. Public GEO datasets used in NB11 and NB13: GSE134780, GSE134781, GSE129811; GSE277997 used only as author-result context for the heart branch.
16. PubChem. Arimoclomol free base, CID 208924, molecular weight 313.78 g/mol.
17. XIST chromosome-silencing proof-of-concept studies in trisomy 21; future-direction context only.
18. Ko W et al. ACE-tRNAs are a platform technology for suppressing nonsense mutations that cause cystic fibrosis. Nucleic Acids Res. 2025;53(13):gkaf675. PMID 40650978; DOI 10.1093/nar/gkaf675.
19. Rare Disease, Real Kid: MVA Hackathon 2026. Track 2 rules, FAQ and submission instructions; current 2026 challenge materials.
