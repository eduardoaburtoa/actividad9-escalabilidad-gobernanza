"""Comprueba documentos públicos heredados; no estima tarifas ni rentabilidades."""
from pathlib import Path
import concurrent.futures as cf,hashlib,json
import pandas as pd,requests
R=Path(__file__).resolve().parents[1]
def check(row):
 result={'fondo':row.fondo,'url_dici':row.url_dici,'checked_date':'2026-11-08'}
 try:
  r=requests.get(row.url_dici,timeout=45);result['http_status']=r.status_code;result['is_pdf']=r.content.startswith(b'%PDF');result['sha256']=hashlib.sha256(r.content).hexdigest() if result['is_pdf'] else None
 except requests.RequestException as e:result['error']=type(e).__name__
 return result
if __name__=='__main__':
 df=pd.read_csv(R/'contexto/fichas_bbva.csv')
 with cf.ThreadPoolExecutor(max_workers=4) as pool:out=list(pool.map(check,df.itertuples()))
 (R/'evidencias/fuentes_fondos.json').write_text(json.dumps({'scope':'Consulta de accesibilidad de los DICI enumerados en la continuidad del proyecto; no certifica exhaustividad del catálogo actual ni actualiza los gastos por serie del CSV histórico.','results':out},ensure_ascii=False,indent=2)+'\n');print(len(out),sum(x.get('is_pdf',False) for x in out))
