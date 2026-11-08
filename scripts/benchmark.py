"""Prueba HTTP local cerrada; no usa ni reemplaza evidencia de Actividad 8."""
from pathlib import Path
import concurrent.futures as cf,json,os,platform,secrets,socket,subprocess,sys,time,threading,hashlib
import numpy as np,pandas as pd,psutil,requests
R=Path(__file__).resolve().parents[1]
def main():
 data=pd.read_csv(R/'datos/predicciones_test.csv'); output=[]; raw=[]
 for workers,concurrency in [(1,1),(1,8),(2,8)]:
  with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
  token=secrets.token_urlsafe(32);env={**os.environ,'API_TOKEN':token,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1'}
  with open(R/'evidencias'/f'benchmark_w{workers}_c{concurrency}.log','w') as log:
   proc=subprocess.Popen([sys.executable,'-m','uvicorn','backend.main:app','--host','127.0.0.1','--port',str(port),'--workers',str(workers),'--no-access-log'],cwd=R,env=env,stdout=log,stderr=log)
   url=f'http://127.0.0.1:{port}';headers={'X-API-Key':token}
   try:
    for _ in range(300):
     try:
      if requests.get(url+'/health',timeout=1).status_code==200:break
     except requests.RequestException:pass
     time.sleep(.1)
    else:raise RuntimeError('API no inició')
    for _ in range(20):requests.post(url+'/v1/predict',json={'texto':data.texto.iloc[0],'idioma':'en'},headers=headers,timeout=30).raise_for_status()
    for rep in range(3):
     stop=threading.Event();samples=[];cpu_start={};cpu_end={};local=threading.local();sessions=[]
     def monitor():
      while not stop.is_set():
       total=0
       for p in [psutil.Process(proc.pid)]+psutil.Process(proc.pid).children(recursive=True):
        try:
         c=p.cpu_times();val=c.user+c.system;cpu_start.setdefault(p.pid,val);cpu_end[p.pid]=val;total+=p.memory_info().rss
        except psutil.Error:pass
       samples.append(total);stop.wait(.02)
     thread=threading.Thread(target=monitor);thread.start()
     def call(row):
      if not hasattr(local,'session'):local.session=requests.Session();sessions.append(local.session)
      start=time.perf_counter();res=local.session.post(url+'/v1/predict',json={'texto':row.texto,'idioma':'en'},headers=headers,timeout=30);elapsed=(time.perf_counter()-start)*1000
      return {'id':row.id,'workers':workers,'concurrency':concurrency,'repeat':rep,'latency_ms':elapsed,'status':res.status_code,'probability':res.json().get('probabilidad_negativa'),'reference':row.SVM_calibrada}
     start=time.perf_counter()
     try:
      with cf.ThreadPoolExecutor(max_workers=concurrency) as pool:rows=list(pool.map(call,pd.concat([data]*10,ignore_index=True).itertuples()))
     finally:
      stop.set();thread.join()
      for session in sessions:session.close()
     elapsed=time.perf_counter()-start;raw.extend(rows)
     ok=[r for r in rows if r['status']==200];lat=[r['latency_ms'] for r in rows];cpu=sum(cpu_end[p]-v for p,v in cpu_start.items())
     output.append({'workers':workers,'concurrency':concurrency,'repeat':rep,'requests':len(rows),'successes':len(ok),'elapsed_seconds':elapsed,'throughput_rps':len(ok)/elapsed,'p50_ms':float(np.percentile(lat,50)),'p95_ms':float(np.percentile(lat,95)),'p99_ms':float(np.percentile(lat,99)),'peak_rss_mib':max(samples)/2**20,'cpu_core_equivalents':cpu/elapsed,'max_probability_delta':max(abs(r['probability']-r['reference']) for r in ok)})
   finally:
    proc.terminate()
    try:proc.wait(timeout=10)
    except subprocess.TimeoutExpired:proc.kill();proc.wait()
 meta={'scope':'HTTP loopback, cliente/servidor en el mismo host; carga cerrada y Session persistente por hilo. No cloud, autoscaling ni SLA mensual. 20 warmups excluidos/configuración. Cada repetición recorre 10 veces las 452 noticias; 4520 peticiones, no ejemplos independientes. RSS suma procesos; puede contar páginas compartidas. CPU 1.0 equivale a un núcleo ocupado.','platform':platform.platform(),'machine':platform.machine(),'logical_cpus':psutil.cpu_count(),'ram_gib':psutil.virtual_memory().total/2**30,'python':sys.version,'model_sha256':hashlib.sha256((R/'modelos/modelo_SVM_calibrada.joblib').read_bytes()).hexdigest(),'runs':output}
 (R/'evidencias/benchmark.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n');pd.DataFrame(raw).to_csv(R/'evidencias/benchmark_requests.csv',index=False)
 print(pd.DataFrame(output).to_string(index=False))
if __name__=='__main__':main()
