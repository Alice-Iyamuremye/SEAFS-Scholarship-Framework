import numpy as np
import pytest
from seafs_engine import predict_one,RULES
def test_notebook_rule_count(): assert len(RULES)==10
@pytest.mark.parametrize('x',[(0,0,0),(100,100,100),(50,50,50),(40,80,90),(60,20,40)])
def test_outputs_are_finite_or_explicit_no_rule(x):
 r=predict_one(*x); assert r['decision'] in {'Reject','Waitlist','Approve','NoRuleFired'}
 if r['decision']!='NoRuleFired': assert np.isfinite(r['score']) and 0<=r['score']<=100
@pytest.mark.parametrize('x',[(-1,50,50),(50,101,50),(50,50,float('nan'))])
def test_invalid_inputs_raise(x):
 with pytest.raises(ValueError): predict_one(*x)
def test_rule_trace():
 assert predict_one(75,85,80)['rule_trace']
