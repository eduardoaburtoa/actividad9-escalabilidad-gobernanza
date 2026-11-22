"""Secciones editoriales acumulativas; no modifica modelo ni evidencia histórica."""
def scaling(d,h,p,tab,root):
 h(d,'Escalabilidad vertical y horizontal')
 tab(d,['Dimensión','Qué cambia y límite','Costo y evidencia','Mi decisión'],[
 ['Escalabilidad vertical','CPU y RAM de una réplica. Límite: cuota máxima, memoria y paralelismo aprovechable.','Rightsizing simulado de 2 CPU/4 GiB a 1 CPU/1 GiB: API USD 231.26 a 105.12/mes; infraestructura USD 296.20 a 170.05.','Reducir tamaño sólo después de probar carga y memoria con cuotas reales.'],
 ['Escalabilidad horizontal','Número de réplicas independientes. Límite: coordinación, cuotas, cola y presupuesto.','Dos procesos locales alcanzan media 1,270.8 rps y p95 medio 9.08 ms; esto sólo evidencia paralelismo intrahost.','Proponer 2 a 6 réplicas pequeñas en Cloud Run: crecer por unidades y tolerar pérdida de una réplica.']])
 p(d,'Elijo escalabilidad horizontal para ajustar capacidad por demanda sin concentrarla en una única instancia. Una réplica adicional tiene costo incremental y puede aislar un fallo de proceso; no garantiza tolerancia regional. Mantengo el eje vertical como ajuste del tamaño por réplica y no como sustituto de redundancia.')
 p(d,'Dos procesos en un host no son escalado horizontal de nube. Las repeticiones de 3.51 a 8.01 segundos no prueban carga sostenida. El cambio vertical es un escenario económico, no una comparación experimental con límites de CPU y RAM impuestos. La decisión debe confirmarse en el ensayo cloud antes del piloto.')

def business(d,h,p,tab,root):
 import json
 x=json.loads((root/'evidencias/negocio_fase1.json').read_text());f=x['source_inputs']
 h(d,'Fase I y dimensionamiento del negocio')
 p(d,'La Fase I aporta el business case: 24 asesores con 150 clientes cada uno, 3,600 clientes y AUM simulado de $54,397 millones MXN. Preserva 7,200 revisiones al año y evaluación diaria de la cartera. Copio estas cifras del antecedente proporcionado por el autor; no recalculo su ROI.')
 p(d,'Bajo treinta días y una inferencia por evaluación, dimensiono 108,000 evaluaciones mensuales. Una evaluación de cartera puede requerir varias noticias, o compartir noticias entre clientes: esa relación debe medirse en el piloto. Las revisiones anuales son un proceso humano distinto y no se suman como inferencias.')
 tab(d,['Escenario de solicitudes','Relación con Fase I','Uso'],[['100,000','Aproximación al alcance de 108,000; no equivalencia exacta','Referencia inicial de costo unitario'],['1,000,000',f"{x['scenario_multiples']['1000000']:.2f} veces el alcance (aproximadamente diez)",'Crecimiento regional hipotético'],['5,000,000',f"{x['scenario_multiples']['5000000']:.2f} veces el alcance",'Techo de escenario, no capacidad demostrada']])
 p(d,f"La infraestructura estable de USD {x['infra_month_usd']:.2f}/mes equivale a MXN {x['infra_month_mxn']:,.2f}/mes y MXN {x['infra_year_mxn']:,.2f}/año al FIX de 18.6297 del 6 de noviembre de 2026 (Banco de México). Representa {x['share_of_fase1_opex_percent']:.3f} % de los MXN 4,769,996 anuales de operación de Fase I y MXN {x['infra_mxn_client_month']:.4f} por cliente al mes. Comparo un componente NLP con el presupuesto integral; no afirmo que lo sustituya ni que la diferencia sea ahorro realizable.")
 p(d,'Conservo inversión de piloto de MXN 9,083,448, beneficio anual esperado a plena operación de MXN 40,540,443, ROI a tres años de 298.6 % y recuperación en mes 13. El caso conservador conserva 38.8 % y mes 25. Por cada peso de corretaje, el cliente conserva $1.04 según Fase I; el umbral de rotación es 3.0 puntos porcentuales por encima del 2 % de costo. Son hipótesis del business case, no resultados de esta prueba.')
 p(d,'La Actividad 9 dimensiona infraestructura; no valida que el ROI de 298.6 % se materialice. Lo mediré en el piloto con seis asesores de los meses 1 a 9. Propongo dos réplicas mínimas de 1 CPU/1 GiB y máximo dos en piloto en sombra; al aprobar el paso a 24 asesores, mantendría dos mínimas y permitiría hasta seis. Ambas configuraciones requieren ensayo cloud. Seis permanentes costarían USD 380.29 y excederían el presupuesto académico de USD 300.')

def fairness_report(d,h,p,tab,root):
 import json
 f=json.loads((root/'evidencias/fairness.json').read_text())
 h(d,'Evaluación de fairness por grupo')
 interval=lambda x: f'{x[0]:.3f}–{x[1]:.3f}'
 tab(d,['Longitud / n','Selección','TPR [IC 95 %]','FPR [IC 95 %]'],[[f"{x['group']} / {x['n']}",f"{x['selection_rate']:.3f}",f"{x['recall']:.3f} [{interval(x['tpr_ci95'])}]",f"{x['fpr']:.3f} [{interval(x['fpr_ci95'])}]"] for x in f['groups']])
 p(d,'Observo mayor TPR en textos de 16–30 palabras y menor TPR en textos de 1–15 palabras. Los intervalos Wilson al 95 % se traslapan entre los tres grupos, tanto en TPR como en FPR. Ese traslape no prueba ausencia de diferencias ni reemplaza una prueba estadística; señala incertidumbre relevante con sólo 12, 35 y 14 positivos. La diferencia máxima de TPR es 13.57 puntos porcentuales; su intervalo bootstrap descriptivo es [3.57, 42.89] puntos. Distingo Wilson por grupo del bootstrap de la brecha.')
 p(d,'Esta fairness exploratoria usa longitud como condición técnica, no como atributo protegido ni proxy validado de una población. Sin edad, sexo o etnia no acredito equidad demográfica. La mayor tasa de falsas alertas en textos largos supone más revisión humana, pero no demuestra discriminación. Mantengo la evaluación demográfica pendiente, con base legítima y muestra suficiente antes de ampliar el uso.')

def frameworks(d,h,p,tab,root):
 h(d,'Controles y marcos de gobernanza')
 tab(d,['Marco / función','Control concreto y evidencia','Decisión'],[
 ['NIST AI RMF · Govern','Responsables y cinco puertas en config/governance.json','Comité aprueba; producción bloqueada mientras falte una puerta.'],
 ['NIST AI RMF · Map','Uso limitado a noticias inglesas y revisión humana; contexto y licencia documentados','No extrapolar a rendimiento de fondos ni a clientes mexicanos.'],
 ['NIST AI RMF · Measure','Métricas, fairness con IC y benchmark preservados en evidencias/','Evaluar errores, grupos y dominio externo antes del piloto.'],
 ['NIST AI RMF · Manage','Canario, pausa y rollback propuestos; evidencia operativa de Actividad 8','Conservar incidente, responsable y criterio de recuperación.'],
 ['ISO/IEC 42001 · sistema de gestión','Registro de riesgos, responsables, evaluación de impacto, seguimiento y revisión de cambios','Propuesta de controles del ciclo de vida; no certificación ni auditoría de conformidad.']])
 p(d,'CC BY-NC-SA 3.0 restringe el uso comercial del corpus. Mantengo el bloqueo comercial hasta que jurídico resuelva los derechos del dato y del modelo derivado o se sustituya el corpus con nueva validación. NIST AI RMF e ISO/IEC 42001 son referencias de trabajo; no sustituyen obligaciones legales mexicanas ni acreditan cumplimiento institucional.')


def performance_blocks(d,h,p,tab,root):
 import json
 import pandas as pd
 runs=json.loads((root/'evidencias/benchmark.json').read_text())['runs']
 h(d,'Latencia (p50, p95, p99)')
 tab(d,['Procesos / concurrencia / rep','p50 ms','p95 ms','p99 ms'],[[f"{x['workers']}/{x['concurrency']}/{x['repeat']+1}"]+[f"{x[k]:.3f}" for k in ['p50_ms','p95_ms','p99_ms']] for x in runs])
 p(d,'Percentiles cliente HTTP de cada repetición completa; no incluyen warmup ni red externa. El p99 refleja la cola observada en una prueba corta, no un compromiso contractual.')
 d.add_page_break();h(d,'Throughput (solicitudes por segundo)')
 g=pd.DataFrame(runs).groupby(['workers','concurrency']).mean(numeric_only=True)
 tab(d,['Procesos / concurrencia','Media solicitudes/s','Lectura'],[[f'{a}/{b}',f'{x.throughput_rps:.2f}','Media de tres repeticiones locales'] for (a,b),x in g.iterrows()])
 p(d,'Cada corrida divide sus 4,520 respuestas entre su duración. No extrapolo estas tasas de ráfaga a demanda mensual sostenida. El objetivo cloud de 10 solicitudes/s por una hora sigue sin validar.')
 h(d,'Uso de recursos (CPU y memoria)')
 tab(d,['Procesos / concurrencia','CPU observada, núcleos equivalentes','RSS observado, MiB'],[[f'{a}/{b}',f'{x.cpu_core_equivalents:.3f}',f'{x.peak_rss_mib:.2f}'] for (a,b),x in g.iterrows()])
 p(d,'Los valores son medias de CPU total y de picos RSS de los procesos servidor en un host con 10 CPU lógicas y 16 GiB. No se aislaron recursos ni se midió memoria por réplica cloud; no reparto artificialmente el agregado entre procesos. La suma RSS puede duplicar páginas compartidas.')
 tab(d,['Aprovisionamiento propuesto por réplica','CPU','Memoria GiB','Estado'],[['Base cloud simulada',2,4,'Sin medición con cuotas'],['Rediseño y piloto',1,1,'Sin medición por réplica cloud']])
 p(d,'Comparar recursos observados y aprovisionados orienta el ensayo futuro, pero no prueba que una réplica de 1 CPU sostenga la concurrencia objetivo. Debo medir saturación, memoria y latencia con límites efectivos antes de aprobar el cambio.')
