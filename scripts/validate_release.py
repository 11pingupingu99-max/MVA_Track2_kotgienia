from pathlib import Path
import json, zipfile
root=Path(__file__).resolve().parents[1]
required=[
'report/kotgienia_track2_report.pdf','report/kotgienia_track2_report.md',
'figures/track2_decision_architecture.png',
'core/notebooks/MVA_NB08R2_AUDITED_COVERAGE_v1_0_2_EXACT_COMPONENT.ipynb',
'core/notebooks/MVA_NB09_EXPOSURE_MECHANISM_v1_0_0.ipynb',
'core/notebooks/MVA_F0_ABUNDANCE_MATCHED_ADDENDUM_v1_1_0.ipynb',
'core/notebooks/MVA_NB10_RESCUE_RULE_POWER_SIMULATION_v1_0_1.ipynb',
'core/snapshots/drugcentral_interactions_snapshot.csv','core/snapshots/drugcentral_approved_snapshot_NORMALIZED.csv',
'docs/DATA_DELETION_PLAN.md','docs/AI_ASSISTANCE_DISCLOSURE.md','docs/REPRODUCIBILITY_AND_PRIVACY.md',
'docs/kotgienia_track2_methods_description.xlsx',
'pitch/MVA_Track2_3min_Presentation_FINAL.pptx','pitch/MVA_Track2_3min_Presentation_FINAL.pdf','pitch/3MIN_NARRATION_FINAL.md',
'exploratory/readthrough/context/NB04B_NEGATIVE_PREDICTOR_CALIBRATION.md',
'exploratory/readthrough/notebooks/MVA_NB14_L737_STOP_NMD_AUDIT_v1_0_0_PUBLIC.ipynb',
'exploratory/readthrough/notebooks/MVA_NB15_READTHROUGH_PRODUCT_FUNCTION_v1_0_0_PUBLIC.ipynb',
'exploratory/readthrough/notebooks/MVA_NB16_READTHROUGH_TRANSLATIONAL_GATES_v1_0_0_PUBLIC.ipynb',
'exploratory/readthrough/results/NB14_RESULTS_EXACT.zip',
'exploratory/readthrough/results/NB15_RESULTS_EXACT.zip',
'exploratory/readthrough/results/NB16_RESULTS_EXACT.zip',
'core/nb17_f0_prereg/MVA_NB17_F0_PREREG_VALIDITY_v1_0_1.ipynb',
'core/nb17_f0_prereg/NB17_F0_SAP_v1_0_1.md',
'core/nb17_f0_prereg/NB17_HANDOFF.json']
missing=[x for x in required if not (root/x).exists()]
assert not missing, missing
for nbdir in [root/'core/notebooks',root/'exploratory/readthrough/notebooks']:
    for p in nbdir.glob('*.ipynb'):
        nb=json.loads(p.read_text(encoding='utf-8'))
        assert all(c.get('outputs',[])==[] for c in nb['cells'] if c.get('cell_type')=='code'), p
        assert all(c.get('execution_count') is None for c in nb['cells'] if c.get('cell_type')=='code'), p
        for i,c in enumerate(nb['cells']):
            if c.get('cell_type')=='code':
                compile(''.join(c.get('source',[])),f'{p.name}:cell{i}','exec')
# text leak scan; exact result ZIPs are immutable historical run bundles and are binary
scan=[]
for p in root.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.md','.json','.py','.txt','.csv','.ipynb'} and p.name!='validate_release.py':
        scan.append(p.read_text(errors='ignore'))
text='\n'.join(scan)
for bad in ['/content/drive/'+'MyDrive/','BEGIN PRIVATE KEY','api_key =']:
    assert bad not in text, bad
# Claim-boundary checks
report=(root/'report/kotgienia_track2_report.md').read_text(encoding='utf-8')
assert 'Final Report v1.6.1' in report
assert 'NO_PREDICTOR_CALIBRATED' in report
assert 'NB14-NB16' in report
assert 'Gate 0' in report
assert '5.83' in report and '0.194' in report
assert 'SIRT2 epistasis' in report
assert 'ACE-tRNA' in report
assert 'no approved drug in the audited target space currently qualifies as a credible causal rescue' in report
# Disclosure synchronization checks
section=report.split('## 13. AI-assistance disclosure',1)[1].split('## Final proposal',1)[0].strip()
for p in [root/'README.md',root/'docs/AI_ASSISTANCE_DISCLOSURE.md',root/'docs/REPRODUCIBILITY_AND_PRIVACY.md']:
    doc=p.read_text(encoding='utf-8').split('## 13. AI-assistance disclosure',1)[1].strip()
    assert doc==section, p
assert 'PS3 **5.60**' in report and 'BS3 **0.233**' in report
print('RELEASE_VALIDATION_PASS')
