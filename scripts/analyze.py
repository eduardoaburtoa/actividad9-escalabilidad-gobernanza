"""Análisis reproducible sin reentrenar ni modificar umbral."""
from pathlib import Path
import json,hashlib,time,platform
import numpy as np,pandas as pd,joblib
from sklearn.metrics import confusion_matrix,accuracy_score,precision_score,recall_score,f1_score,roc_auc_score
R=Path(__file__).resolve().parents[1]
def wilson(k,n):
 if not n:return [None,None]
 z=1.96;p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
 return [float(c-h),float(c+h)]
def metrics(y,p):
 pred=np.asarray(p)>=.20;tn,fp,fn,tp=confusion_matrix(y,pred,labels=[0,1]).ravel()
 return dict(n=len(y),positives=int(sum(y)),tn=int(tn),fp=int(fp),fn=int(fn),tp=int(tp),accuracy=accuracy_score(y,pred),precision=precision_score(y,pred,zero_division=0),recall=recall_score(y,pred,zero_division=0),f1=f1_score(y,pred,zero_division=0),auc=roc_auc_score(y,p) if len(set(y))==2 else None,selection_rate=float(np.mean(pred)),fpr=float(fp/(fp+tn)) if fp+tn else None,tpr_ci95=wilson(tp,tp+fn),fpr_ci95=wilson(fp,fp+tn))
def main():
 df=pd.read_csv(R/'datos/predicciones_test.csv');model=joblib.load(R/'modelos/modelo_SVM_calibrada.joblib');texts=df.texto.tolist();p=model.predict_proba(texts)[:,1]
 assert np.max(abs(p-df.SVM_calibrada))<1e-12
 # Cortes fijados por longitud, no elegidos por el resultado.
 length=df.texto.str.split().str.len(); groups=pd.cut(length,[0,15,30,np.inf],labels=['1-15 palabras','16-30 palabras','31+ palabras'])
 rows=[]
 for g in groups.cat.categories:
  idx=groups==g;rows.append({'group':g,**metrics(df.y[idx],p[idx])})
 gap=max(r['recall'] for r in rows)-min(r['recall'] for r in rows)
 rng=np.random.default_rng(42);boots=[]
 for _ in range(2000):
  tprs=[]
  for g in groups.cat.categories:
   positive=np.flatnonzero((groups==g)&(df.y==1));sample=rng.choice(positive,len(positive),replace=True);tprs.append(float(np.mean(p[sample]>=.2)))
  boots.append(max(tprs)-min(tprs))
 out={'scope':'Auditoría exploratoria de 452 noticias históricas; longitud no es atributo protegido. Sin edad, sexo ni etnia no se acredita fairness demográfica. Bootstrap estratificado por grupo y clase positiva; intervalos descriptivos, no prueba confirmatoria.','overall':metrics(df.y,p),'groups':rows,'recall_gap':gap,'recall_gap_bootstrap_ci95':np.quantile(boots,[.025,.975]).tolist(),'bootstrap_seed':42,'bootstrap_repetitions':2000,'threshold':.2}
 (R/'evidencias/fairness.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
 df.assign(word_count=length,group=groups,probability=p,prediction=(p>=.2).astype(int)).to_csv(R/'evidencias/predicciones_auditadas.csv',index=False)
 bench=[]
 for batch in [1,32,128]:
  for rep in range(5):
   start=time.perf_counter();got=np.concatenate([model.predict_proba(texts[i:i+batch])[:,1] for i in range(0,len(texts),batch)]);elapsed=time.perf_counter()-start
   bench.append({'batch_size':batch,'repeat':rep,'seconds':elapsed,'throughput_texts_second':len(texts)/elapsed,'amortized_ms_text':elapsed/len(texts)*1000,'max_delta':float(np.max(abs(got-p)))})
 (R/'evidencias/batching.json').write_text(json.dumps({'scope':'Inferencia offline, incluye vectorización, sin HTTP ni cola; latencia amortizada no es p95 interactivo. Mismo modelo, cinco repeticiones, orden fijo; posibles efectos de calentamiento.','runs':bench},indent=2)+'\n')
 print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
