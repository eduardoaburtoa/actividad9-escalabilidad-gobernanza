"""Tablero académico: lee evidencia histórica, no tráfico productivo."""
from pathlib import Path
import json
import pandas as pd
import streamlit as st
from scripts.costs import calculate
R=Path(__file__).resolve().parent
st.set_page_config(page_title='Vértice AI · Actividad 9',layout='wide')
st.image(str(R/'documentos/vertice_logo.png'),width=120)
st.title('Escalabilidad y gobernanza responsable')
st.caption('Eduardo Aburto Angulo · Actividad 9 · Evidencia local del 8 de noviembre de 2026')
st.info('Resultados históricos, costos estimados y arquitectura propuesta. No es un servicio bancario productivo ni una recomendación de inversión.')
def load(n):return json.loads((R/'evidencias'/n).read_text())
b=load('benchmark.json');f=load('fairness.json');c=load('costos.json');gate=load('governance_gate.json')
cols=st.columns(4)
cols[0].metric('Solicitudes locales',f"{sum(x['requests'] for x in b['runs']):,}")
cols[1].metric('Recall histórico',f"{f['overall']['recall']:.1%}")
cols[2].metric('Ahorro estimado infra',f"{c['scenarios'][1]['infra_saving_percent']:.2f}%")
cols[3].metric('Producción','Bloqueada' if not gate['production_authorized'] else 'Requiere firma institucional')
tabs=st.tabs(['Desempeño','FinOps','Fairness','Gobernanza','Entregables'])
with tabs[0]:
 st.image(str(R/'evidencias/rendimiento.png'));st.dataframe(pd.DataFrame(b['runs']),hide_index=True)
 st.warning('Dos procesos en un mismo equipo no demuestran escalado horizontal cloud. Cada repetición dura 3.51–8.01 segundos; faltan WAN, cold starts y carga sostenida.')
 st.write(b['scope']);st.subheader('Lotes offline');st.dataframe(pd.DataFrame(load('batching.json')['runs']),hide_index=True)
with tabs[1]:
 st.image(str(R/'evidencias/costos.png'));st.dataframe(pd.DataFrame(c['scenarios']).drop(columns=['usd_per_1000_requests']),hide_index=True)
 st.subheader('Explora un escenario estimado')
 replicas=st.slider('Réplicas permanentes de API',1,6,2);hours=st.slider('Horas mensuales por réplica',1,744,730)
 cfg=json.loads((R/'config/costs.json').read_text());cfg['month_hours']=hours;cfg['scenarios']=[dict(name='Exploración',cpu=1,gib=1,min_instances=replicas,extra_instances=0,extra_hours=0)]
 s=calculate(cfg)['scenarios'][0];st.metric('Infraestructura estimada USD',f"{s['infra_usd']:.2f}")
 st.caption('El control de horas también ajusta el frontend; no es factura ni prueba de capacidad.');st.write(cfg['exclusions']);st.link_button('Fuente pública de tarifas',cfg['source'])
with tabs[2]:
 st.image(str(R/'evidencias/fairness.png'));st.dataframe(pd.DataFrame(f['groups']),hide_index=True)
 st.warning('Longitud no es atributo protegido. No hay evidencia suficiente para afirmar fairness demográfica.')
 st.write(f['scope']);st.write('Brecha de recall:',round(f['recall_gap'],4),'· IC bootstrap descriptivo:',f['recall_gap_bootstrap_ci95'])
with tabs[3]:
 st.error('Cinco aprobaciones productivas pendientes');st.json(gate)
 st.image(str(R/'documentos/Arquitectura.png'))
 st.write('NIST AI RMF e ISO 42001 se usan como referencias, sin afirmar certificación. La revisión humana es obligatoria; el modelo clasifica noticias en inglés, no ejecuta órdenes.')
with tabs[4]:
 st.write('Reporte y anexo incluyen métodos, supuestos, riesgos, responsables y referencias.')
 for name in ['Reporte_tecnico.pdf','Reporte_tecnico.docx','Anexo_tecnico.pdf','Anexo_tecnico.docx','Arquitectura.pdf']:
  path=R/'documentos'/name
  if path.exists():st.download_button(name,path.read_bytes(),file_name=name)
 st.caption('Los 150 personajes ficticios y las fichas históricas se conservan en contexto; no alimentan la evaluación de fairness.')
