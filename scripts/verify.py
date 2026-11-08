"""Recalcula la evidencia publicada; no vuelve a ejecutar pruebas de carga."""
from pathlib import Path
import sys,json,hashlib
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from analyze import metrics
from costs import calculate
from governance import assess

def main():
 manifest=json.loads((R/'modelos/manifest.json').read_text());sha=hashlib.sha256((R/'modelos/modelo_SVM_calibrada.joblib').read_bytes()).hexdigest();assert sha==manifest['sha256'];assert manifest['threshold']==.2
 df=pd.read_csv(R/'datos/predicciones_test.csv');fair=json.loads((R/'evidencias/fairness.json').read_text());m=metrics(df.y,df.SVM_calibrada)
 for k in ['accuracy','precision','recall','f1','auc']:assert np.isclose(m[k],fair['overall'][k])
 raw=pd.read_csv(R/'evidencias/benchmark_requests.csv');bench=json.loads((R/'evidencias/benchmark.json').read_text())
 assert len(bench['runs'])==9
 for r in bench['runs']:
  x=raw[(raw.workers==r['workers'])&(raw.concurrency==r['concurrency'])&(raw.repeat==r['repeat'])];assert len(x)==r['requests']==4520;assert (x.status==200).all();assert np.max(abs(x.probability-x.reference))<1e-12
  assert np.isclose(np.percentile(x.latency_ms,95),r['p95_ms']);assert np.isclose(len(x)/r['elapsed_seconds'],r['throughput_rps'])
 c=json.loads((R/'config/costs.json').read_text());assert calculate(c)==json.loads((R/'evidencias/costos.json').read_text())
 g=json.loads((R/'config/governance.json').read_text());assert assess(g,sha)==json.loads((R/'evidencias/governance_gate.json').read_text());assert not assess(g,sha)['production_authorized']
 for r in json.loads((R/'evidencias/batching.json').read_text())['runs']:assert r['max_delta']<1e-12
 clients=pd.read_csv(R/'contexto/clientes_simulados.csv');assert len(clients)==150;assert clients.posicion_mxn.between(5e6,20e6).all()
 print('OK: modelo conservado; 40680 solicitudes; 9 mediciones; métricas, costos y bloqueo productivo verificados.')
if __name__=='__main__':main()
