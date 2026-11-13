"""One-factor-at-a-time sensitivity analysis for the 10-rule notebook FIS."""
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluate_synthetic_cohort import make_cohort,evaluate
if __name__=='__main__':
 rows=[]; cohort=make_cohort(42)
 for shift in [-5,0,5]:
  for threshold in [60,65,68,70,73,75,80]:
   d=evaluate(cohort,mf_shift=shift,approval_threshold=threshold)
   for name,g in d.groupby('Cohort'):
    rows.append({'mf_boundary_shift':shift,'approval_threshold':threshold,'cohort':name,'n':len(g),'pass_rate_pct':100*g.Passed_SEAFS.mean(),'mean_score':g.SEAFS_Score.mean(),'no_rule_cases':int(g.SEAFS_Score.isna().sum())})
 f=pd.DataFrame(rows); f.to_csv('seafs_sensitivity_results.csv',index=False)
 print(f.pivot_table(index=['mf_boundary_shift','approval_threshold'],columns='cohort',values='pass_rate_pct').round(1).to_string())
 print('Criterion-weight sensitivity is excluded because this notebook implementation does not apply the thesis AHP weights.')
