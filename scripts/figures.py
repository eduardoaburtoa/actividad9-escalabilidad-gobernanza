from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import pandas as pd
R=Path(__file__).resolve().parents[1];E=R/'evidencias';O=R/'documentos';plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
b=pd.DataFrame(json.loads((E/'benchmark.json').read_text())['runs']);g=b.groupby(['workers','concurrency']).mean(numeric_only=True);labels=['1 proceso\n1 concurrente','1 proceso\n8 concurrentes','2 procesos\n8 concurrentes']
fig,axs=plt.subplots(1,3,figsize=(12,3.8))
for ax,col,title in zip(axs,['throughput_rps','p95_ms','peak_rss_mib'],['Solicitudes por segundo','p95 HTTP en ms','RSS máximo medio en MiB']):
 ax.bar(labels,g[col],color=['#004481','#1464A5','#5BBEFF']);ax.set_title(title);ax.tick_params(axis='x',labelsize=9)
 for i,v in enumerate(g[col]):ax.text(i,v,f'{v:.1f}',ha='center',va='bottom')
fig.suptitle('Prueba local · medias de tres repeticiones por configuración');fig.tight_layout();fig.savefig(E/'rendimiento.png',dpi=170);plt.close(fig)
f=json.loads((E/'fairness.json').read_text());fig,ax=plt.subplots(figsize=(8,3.6));gs=f['groups'];ys=[x['recall'] for x in gs];ax.errorbar(range(3),ys,yerr=[[y-x['tpr_ci95'][0] for x,y in zip(gs,ys)],[x['tpr_ci95'][1]-y for x,y in zip(gs,ys)]],fmt='o',capsize=7,color='#004481');ax.set_xticks(range(3),[x['group']+'\n'+str(x['positives'])+' positivos' for x in gs]);ax.set_ylim(0,1);ax.set_ylabel('Recall e IC Wilson 95 %');ax.set_title('Auditoría exploratoria por longitud de texto');fig.tight_layout();fig.savefig(E/'fairness.png',dpi=170);plt.close(fig)
c=json.loads((E/'costos.json').read_text())['scenarios'];fig,ax=plt.subplots(figsize=(9,3.6));ax.barh(['Base simulada','Rediseño estable','Con picos','Seis instancias 730 h'],[x['infra_usd'] for x in c],color=['#004481','#1464A5','#5BBEFF','#A32A30']);ax.axvline(300,color='#A32A30',ls='--',label='Presupuesto propuesto USD 300');ax.set_xlabel('USD por mes estimados · sin impuestos ni egress');ax.legend();fig.tight_layout();fig.savefig(E/'costos.png',dpi=170);plt.close(fig)
fig,axs=plt.subplots(2,1,figsize=(12,9))
for ax in axs:ax.set_xlim(0,12);ax.set_ylim(0,4);ax.axis('off')
def box(ax,x,y,w,t):
 ax.add_patch(FancyBboxPatch((x,y),w,.8,boxstyle='round,pad=.08',facecolor='#EAF3FA',edgecolor='#004481'));ax.text(x+w/2,y+.4,t,ha='center',va='center',fontsize=10)
def arrow(ax,a,b):ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':'#004481','lw':1.8})
a=axs[0];a.set_title('ACTUAL · integración y observabilidad locales',loc='left',color='#004481',weight='bold');
for x,w,t in [(0.2,2,'Streamlit\nrevisión humana'),(3,2.4,'FastAPI local\nclave de servicio'),(6.2,2.3,'TF IDF + SVM\numbral 0.20'),(9.3,2.4,'Resultado\nnoticia negativa')]:box(a,x,2.3,w,t)
for s,t in [(2.2,3),(5.4,6.2),(8.5,9.3)]:arrow(a,(s,2.7),(t,2.7))
box(a,3,.5,5.5,'Actividad 8 · logs y spans locales · MLflow\n900 solicitudes y tres incidentes simulados');arrow(a,(4.2,2.3),(4.2,1.3));a.text(.2,.05,'Sin SLA de nube comprobado · modelo en inglés · no ejecuta inversiones',fontsize=10)
a=axs[1];a.set_title('PROPUESTO · nube simulada para el análisis FinOps',loc='left',color='#004481',weight='bold')
for x,w,t in [(.2,2,'Streamlit + OIDC\nacceso por rol'),(3,2.4,'Cloud Run API\n2 a 6 réplicas'),(6.2,2.3,'Modelo inmutable\n1 CPU y 1 GiB'),(9.3,2.4,'Banquero revisa\ny documenta')]:box(a,x,2.3,w,t)
for s,t in [(2.2,3),(5.4,6.2),(8.5,9.3)]:arrow(a,(s,2.7),(t,2.7))
box(a,.2,.5,3.3,'Registro y secretos gestionados\nversiones y mínimo privilegio');box(a,4.1,.5,3.3,'Métricas y trazas centralizadas\nSLO y alertas de gasto');box(a,8,.5,3.7,'Puertas de aprobación\ncanario y rollback humano')
arrow(a,(4.2,2.3),(5.7,1.3));arrow(a,(7.2,1.3),(7.2,2.3));a.text(.2,.05,'Escalado horizontal propuesto, no ejecutado · sin órdenes automáticas · producción bloqueada',fontsize=10)
fig.tight_layout(pad=2);fig.savefig(O/'Arquitectura.png',dpi=180);fig.savefig(O/'Arquitectura.pdf');plt.close(fig)
