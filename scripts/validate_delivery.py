"""Verifica la entrega editorial sin modificar ni volver a medir el servicio."""
from pathlib import Path
import io,json,re,subprocess,zipfile,hashlib
from xml.etree import ElementTree as ET
R=Path(__file__).resolve().parents[1]
W={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
S={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def body(data):
 with zipfile.ZipFile(io.BytesIO(data)) as z:root=ET.fromstring(z.read('word/document.xml'))
 return '\n'.join(''.join(t.text or '' for t in p.findall('.//w:t',W)) for p in root.findall('.//w:p',W))
def counts(text):
 return {k:len(re.findall(v,text,re.I)) for k,v in {'escalabilidad_vertical':r'escalabilidad vertical','escalabilidad_horizontal':r'escalabilidad horizontal','fairness':r'\bfairness\b','fase_i':r'\bFase I\b','animo':r'\bánimo\b'}.items()}
def annex_coverage(text):
 return {k:bool(re.search(v,text,re.I|re.M)) for k,v in {'costos':r'^Costeo reproducible','latencia':r'^Latencia \(p50','throughput':r'^Throughput \(solicitudes','uso_de_recursos':r'^Uso de recursos \(CPU','fairness':r'^Calidad y evaluación exploratoria de fairness'}.items()}
result={'baseline_commit':'f770a14ac8afe3bb4bdac8f49e285c64950ea574','documents':{},'scope':'Conteo literal del cuerpo DOCX, incluyendo tablas y declaración de IA; Fase I excluye Fase II. No mide calidad por frecuencia.'}
closure='Este documento fue estructurado precisamente para cubrir esos 4 apartados de forma explícita y verificable.'
for name in ['Reporte_tecnico','Anexo_tecnico']:
 path=f'documentos/{name}.docx'
 old=body(subprocess.check_output(['git','show','f770a14:'+path],cwd=R));new=body((R/path).read_bytes())
 assert new.strip().endswith(closure)
 assert counts(new)['animo']==1
 assert 'No redactó el código ni los documentos.' in new
 assert 'No se realizó una nueva revisión independiente con Claude' not in new
 assert 'La IA no sustituye el criterio del banquero; lo aumenta.' in new
 assert (R/f'documentos/{name}.pdf').read_bytes().startswith(b'%PDF')
 result['documents'][name]={'before':counts(old),'after':counts(new)}
 if name=='Anexo_tecnico':result['annex_named_requirements']={'before':annex_coverage(old),'after':annex_coverage(new)}
with zipfile.ZipFile(R/'documentos/Anexo_tecnico.xlsx') as z:
 book=ET.fromstring(z.read('xl/workbook.xml'));names=[s.attrib['name'] for s in book.findall('s:sheets/s:sheet',S)]
 assert names==['Supuestos','Escenarios','Costo por volumen','Comparación']
 formulas=0
 for f in ['xl/worksheets/sheet1.xml','xl/worksheets/sheet2.xml','xl/worksheets/sheet3.xml','xl/worksheets/sheet4.xml']:
  root=ET.fromstring(z.read(f));assert not [c for c in root.findall('.//s:c',S) if c.attrib.get('t')=='e'];formulas+=len(root.findall('.//s:f',S))
 assert formulas>=50
 result['xlsx']={'sheets':names,'formula_count':formulas,'cached_errors':0}
# Exact equality against the audited baseline for protected evidence and code assertions.
protected=['modelos/modelo_SVM_calibrada.joblib','evidencias/benchmark.json','evidencias/benchmark_requests.csv','evidencias/fairness.json','scripts/verify.py']+sorted(str(p.relative_to(R)) for p in (R/'pruebas').glob('test_*.py'))
for p in protected:assert (R/p).read_bytes()==subprocess.check_output(['git','show','f770a14:'+p],cwd=R),p
result['protected_files_unchanged']=protected
(R/'evidencias/revision_editorial.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
