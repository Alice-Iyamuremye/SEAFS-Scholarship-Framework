"""Notebook-aligned 10-rule Mamdani fuzzy inference implementation.
This is not a reconstruction of the thesis appendix's 25-rule design.
The notebook does not apply the thesis's fixed criterion weights.
"""
import numpy as np
RULES=[
 ((('financial_need','High'),('gpa','High')),'Approve'),
 ((('financial_need','High'),('gpa','Medium'),('recommendations','High')),'Approve'),
 ((('financial_need','High'),('gpa','Medium'),('recommendations','Medium')),'Waitlist'),
 ((('financial_need','High'),('gpa','Low'),('recommendations','High')),'Waitlist'),
 ((('financial_need','High'),('gpa','Low'),('recommendations','Low')),'Reject'),
 ((('financial_need','Low'),('gpa','High'),('recommendations','High')),'Approve'),
 ((('financial_need','Low'),('gpa','High'),('recommendations','Medium')),'Approve'),
 ((('financial_need','Medium'),('gpa','High')),'Approve'),
 ((('gpa','Low'),('recommendations','Low')),'Reject'),
 ((('financial_need','Medium'),('gpa','Low')),'Reject')]
def trapmf(x,p):
 a,b,c,d=p; x=np.asarray(x,float); y=np.zeros_like(x)
 if b>a:
  m=(x>=a)&(x<b); y[m]=(x[m]-a)/(b-a)
 y[(x>=b)&(x<=c)]=1
 if d>c:
  m=(x>c)&(x<=d); y[m]=(d-x[m])/(d-c)
 return np.clip(y,0,1)
def trimf(x,p):
 a,b,c=p; x=np.asarray(x,float); y=np.zeros_like(x)
 if b>a:
  m=(x>=a)&(x<=b); y[m]=(x[m]-a)/(b-a)
 if c>b:
  m=(x>=b)&(x<=c); y[m]=np.maximum(y[m],(c-x[m])/(c-b))
 y[x==b]=1
 return np.clip(y,0,1)
def membership_parameters(shift=0):
 d=float(shift)
 return {'gpa':{'Low':(0,0,40+d,60+d),'Medium':(40+d,60+d,80+d),'High':(60+d,80+d,100,100)},
 'financial_need':{'Low':(0,0,30+d,50+d),'Medium':(30+d,50+d,70+d),'High':(50+d,70+d,100,100)},
 'recommendations':{'Low':(0,0,40+d,60+d),'Medium':(40+d,60+d,80+d),'High':(60+d,80+d,100,100)}}
def predict_one(gpa,financial_need,recommendations,mf_shift=0):
 vals={'gpa':float(gpa),'financial_need':float(financial_need),'recommendations':float(recommendations)}
 for k,v in vals.items():
  if not np.isfinite(v) or v<0 or v>100: raise ValueError(f'{k} must be finite and within [0, 100]')
 p=membership_parameters(mf_shift); mem={}
 for k,v in vals.items():
  mem[k]={'Low':float(trapmf(np.array([v]),p[k]['Low'])[0]),'Medium':float(trimf(np.array([v]),p[k]['Medium'])[0]),'High':float(trapmf(np.array([v]),p[k]['High'])[0])}
 u=np.arange(101); out={'Reject':trapmf(u,(0,0,30,50)),'Waitlist':trimf(u,(30,50,75)),'Approve':trapmf(u,(50,75,100,100))}
 agg=np.zeros_like(u,dtype=float); trace=[]
 for i,(ants,con) in enumerate(RULES,1):
  fire=min(mem[k][term] for k,term in ants)
  if fire>0:
   agg=np.maximum(agg,np.minimum(fire,out[con])); trace.append({'rule':i,'antecedents':ants,'consequent':con,'activation':fire})
 area=float(agg.sum())
 if area<=0: return {'score':np.nan,'decision':'NoRuleFired','rule_trace':trace,'memberships':mem}
 score=float((u*agg).sum()/area)
 return {'score':score,'decision':'Reject' if score<45 else ('Waitlist' if score<68 else 'Approve'),'rule_trace':trace,'memberships':mem}
