"""Genera los dos documentos conservando la plantilla institucional del proyecto."""
from pathlib import Path
import json
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import pandas as pd
from revision_sections import scaling
R=Path(__file__).resolve().parents[1];E=R/'evidencias';O=R/'documentos';T=O/'Plantilla.docx'
b=json.loads((E/'benchmark.json').read_text());f=json.loads((E/'fairness.json').read_text());c=json.loads((E/'costos.json').read_text());g=pd.DataFrame(b['runs']).groupby(['workers','concurrency']).mean(numeric_only=True)
def replace(el,s):
 ts=el.findall('.//'+qn('w:t'))
 if ts:
  ts[0].text=s
  for t in ts[1:]:t.text=''
def base(sub):
 d=Document(T);body=d.element.body;replace(body[4],'ACTIVIDAD 9');replace(body[6],sub)
 d.tables[0].cell(1,1).text='Actividad 9 · Módulo 3 / Semana 11 · Temas 21 y 22';d.tables[0].cell(5,1).text='8 de noviembre de 2026'
 d.tables[1].cell(1,2).text='ChatGPT/Codex: apoyo en programación, pruebas locales, investigación de fuentes públicas, documentación y revisión visual. Distingo mediciones reales de escenarios y propuestas.'
 d.tables[1].cell(2,1).text='No';d.tables[1].cell(2,2).text='No se realizó una nueva revisión independiente con Claude para esta actividad. Se conservaron los antecedentes del proyecto y se ejecutaron comprobaciones reproducibles.'
 for row in d.tables[1].rows[3:]:
  row.cells[1].text='No'
  row.cells[2].text='No utilizada en la ejecución de la Actividad 9.'
 for el in list(body)[25:]:
  if el.tag!=qn('w:sectPr'):body.remove(el)
 d.core_properties.title=sub;d.core_properties.author='Eduardo Aburto Angulo';return d
def h(d,t):d.add_heading(t,level=1)
def p(d,t):d.add_paragraph(t)
def page(d,t):d.add_page_break();h(d,t)
def tab(d,heads,rows):
 t=d.add_table(rows=1,cols=len(heads));t.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
 for cell,v in zip(t.rows[0].cells,heads):cell.text=str(v)
 for row in rows:
  for cell,v in zip(t.add_row().cells,row):cell.text=str(v)
 for i,row in enumerate(t.rows):
  row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
  for cell in row.cells:
   sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'004481' if i==0 else ('EAF3FA' if i%2 else 'FFFFFF'));cell._tc.get_or_add_tcPr().append(sh)
   for pa in cell.paragraphs:
    pa.paragraph_format.space_after=Pt(5)
    for run in pa.runs:run.font.size=Pt(9);run.font.color.rgb=RGBColor.from_string('FFFFFF' if i==0 else '072146')
 d.add_paragraph()
def img(d,path,caption,width=6):d.add_picture(str(path),width=Inches(width));p(d,caption)
refs=[
'Google Cloud. (s. f.). Cloud Run pricing. Tarifas consultadas el 8 de noviembre de 2026. https://cloud.google.com/run/pricing',
'Google Cloud. (s. f.). About instance autoscaling. https://docs.cloud.google.com/run/docs/about-instance-autoscaling',
'FinOps Foundation. (s. f.). FinOps Framework. https://www.finops.org/framework/',
'NIST. (2023). Artificial Intelligence Risk Management Framework AI RMF 1.0. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf',
'ISO. (2023). ISO/IEC 42001 Artificial intelligence management system. https://www.iso.org/standard/81230.html',
'Gobierno de México. (2025). Ley Federal de Protección de Datos Personales en Posesión de los Particulares. https://www.ordenjuridico.gob.mx/Documentos/Federal/html/wo125102.html',
'Comisión Europea. (s. f.). AI Act Article 2 Scope. https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-2',
'CNBV. (s. f.). Anexo 13 Conflictos de interés en servicios de inversión. https://www.cnbv.gob.mx/Anexos/Anexo%2013%20Entidades%20y%20personas.pdf',
'BBVA México. (s. f.). Normativa de fondos. https://www.bbva.mx/personas/productos/inversion/normativa-de-fondos.html',
'Malo, P., Sinha, A., Korhonen, P., Wallenius, J., & Takala, P. (2014). Good debt or bad debt: Detecting semantic orientations in economic texts. Journal of the Association for Information Science and Technology, 65(4), 782–796. https://doi.org/10.1002/asi.23062',
'Universidad Tecmilenio. (2026). Temas 21 y 22 y rúbrica de la Actividad 9 [Material del curso].'
]
d=base('Escalabilidad y gobernanza responsable del asistente de portafolios')
h(d,'Decisión y alcance')
p(d,'Propongo escalar el servicio de clasificación de noticias con réplicas pequeñas y conservar una aprobación humana antes de cualquier decisión de inversión. El análisis estima una reducción de 42.59 % en infraestructura frente a una base cloud simulada. La prueba HTTP local procesó 40,680 solicitudes sin errores y mantuvo las predicciones; estos resultados no acreditan disponibilidad mensual ni capacidad en nube.')
p(d,'Desde mi enfoque de banquero Sr., la eficiencia sólo tiene valor si mejora la preparación de la revisión y protege al cliente. Por ello, mi decisión es continuar en un entorno académico. El uso productivo permanece bloqueado hasta resolver licenciamiento, validación en español y México, privacidad, pruebas cloud y evidencia de fairness demográfica.')
p(d,'Doy continuidad a la SVM calibrada de Actividades 5 y 6, a la API de Fase II y a los aprendizajes operativos de Actividad 8. No vuelvo a entrenar ni a seleccionar el modelo con el test. La clase positiva identifica noticia negativa en inglés; no predice rendimientos ni recomienda comprar o vender fondos.')
tab(d,['Entregable','Contenido verificable'],[['Reporte técnico','Arquitectura, rediseño, FinOps, auditoría y plan de aprobación'],['Anexo técnico','Nueve corridas HTTP, costos, calidad y brechas por longitud'],['Arquitectura PNG y PDF','Estado local actual y nube propuesta claramente separados'],['Repositorio y Streamlit','Scripts, configuraciones, datos de evidencia y exploración de resultados']])
page(d,'Arquitectura actual y diagnóstico')
p(d,'El sistema integra Streamlit, FastAPI y un pipeline TF IDF con SVM calibrada. La API verifica la integridad del archivo de modelo y exige una clave de servicio; expone salud, descripción del modelo e inferencia. Fase II comprobó integración y contenedorización local. No atribuyo a ese antecedente un despliegue cloud público que no consta en la evidencia.')
p(d,'Actividad 8 añadió métricas, logs, spans locales y registro en MLflow. Sus 900 solicitudes incluyeron tres incidentes inyectados: se recuperó la operación, pero 120 solicitudes lentas excedieron el presupuesto de nueve. Recuperarse no borra el incumplimiento. Esta entrega añade un benchmark sano; no reemplaza ni altera esa evidencia histórica.')
tab(d,['Limitación actual','Consecuencia','Decisión'],[['Proceso y almacenamiento locales','Un host concentra falla y estado','Separar servicio sin estado de evidencia persistente'],['Clave estática de laboratorio','Rotación y autorización limitadas','Proponer OIDC, identidad de servicio y secretos gestionados'],['Spans locales','Sin correlación distribuida comprobada','Proponer colector y trazabilidad centralizada'],['Noticias en inglés y corpus histórico','Dominio mexicano sin validar','Bloquear recomendación financiera y expansión productiva'],['Sin factura ni carga cloud','No hay costo ni SLA observado en nube','Costeo por escenario y ensayo cloud como puerta futura']])
p(d,'La versión de Fase II usada como antecedente es b6ecb7a0e6b01ece989369b7b67178fe7d7cc2a4. El modelo conserva SHA256 f48c7496d5a12bd15d535721e3e83c6ef895b1ae7eaccbe7f4f4c60705bb1916 y umbral 0.20.')
page(d,'Sistema actual y sistema propuesto')
img(d,O/'Arquitectura.png','Figura 1. Arquitectura propia. El bloque superior representa antecedentes locales; el inferior es una propuesta no desplegada.',6.3)
p(d,'Conservaría el artefacto inmutable y su versión en cada resultado. El flujo termina en revisión documentada del banquero. La arquitectura no contiene un enlace que ejecute órdenes de inversión.')
page(d,'Rediseño de escalabilidad e inferencia')
scaling(d,h,p,tab,R)
page(d,'Decisiones de capacidad e inferencia')
tab(d,['Decisión','Justificación y límite'],[['Escalado vertical','Evaluar 1 frente a 2 CPU y 1 frente a 2 GiB por réplica en nube. Más RAM no acelera necesariamente TF IDF. El ensayo local de dos procesos no impone cuotas cloud.'],['Escalado horizontal','Proponer Cloud Run con dos réplicas mínimas y seis máximas, concurrencia inicial ocho. Réplicas sin estado, revisiones versionadas y rollback. No se midió autoscaling real.'],['Disponibilidad','Dos réplicas reducen dependencia de un proceso, pero no acreditan tolerancia regional. Probar pérdida de réplica y restauración; documentar dependencia del proveedor.'],['Inferencia','Cargar una vez el modelo; conexiones persistentes; lotes offline de hasta 128. Mantener ruta interactiva sin espera de lote.'],['Cache','Sólo textos públicos con clave hash de texto, versión y umbral. TTL propuesto 15 min; medir hit rate. No implementada ni incluida en ahorro.'],['Optimización descartada','No usar GPU, poda ni cuantización por moda: este modelo pequeño no tiene beneficio demostrado y debe conservar sus predicciones.']])
p(d,'Cloud Run considera CPU y concurrencia para autoscaling; la utilización de memoria requiere vigilancia propia. Una aplicación que no aproveche varias CPU puede quedar mal dimensionada si se observa sólo su promedio. Probaría una CPU por réplica antes de ampliar verticalmente. El máximo de instancias limita expansión, pero puede generar cola y rechazos; no es una garantía exacta de gasto (Google Cloud, s. f.).')
p(d,'En lotes offline, tamaño 128 obtuvo alrededor de 29 mil textos por segundo frente a 1.19 mil con tamaño uno, sin cambios de probabilidad. Es tiempo amortizado sin HTTP; no equivale a latencia p95 de un usuario. No traslado esa aceleración al cálculo del SLA.')
page(d,'Desempeño medido y objetivos de servicio')
img(d,E/'rendimiento.png','Figura 2. Medias de tres repeticiones por configuración. Fuente: benchmark HTTP local reproducible.')
tab(d,['Procesos / concurrencia','Solicitudes por segundo','p95 medio ms','RSS medio MiB'],[[f'{a} / {z}',f'{r.throughput_rps:.1f}',f'{r.p95_ms:.2f}',f'{r.peak_rss_mib:.1f}'] for (a,z),r in g.iterrows()])
p(d,'Cada repetición ejecutó 4,520 solicitudes sobre las mismas 452 noticias; duró entre 3.51 y 8.01 segundos. El host ARM dispone de diez CPU lógicas y 16 GiB. Cliente y servidor comparten equipo, la carga es cerrada y se excluyen veinte warmups por configuración. No medí WAN, cold starts, sostenimiento por una hora ni fallas de infraestructura. RSS suma procesos y puede duplicar páginas compartidas.')
p(d,'Defino como objetivos propuestos disponibilidad mensual de 99.9 % y p95 ≤250 ms a diez solicitudes por segundo. El presupuesto temporal es 43.2 minutos en treinta días. Es un SLO de diseño, no un SLA contractual demostrado. Antes de aprobar el piloto exigiré una hora de carga, ráfagas, pérdida de réplica y medición desde otra máquina; el SLA formal deberá acordarse con negocio y proveedor.')
page(d,'Costos y decisiones FinOps')
img(d,E/'costos.png','Figura 3. Infraestructura mensual estimada en USD. El escenario máximo supera el presupuesto propuesto.')
tab(d,['Escenario','Infra USD','TCO USD','Ahorro infra'],[[s['name'],f"{s['infra_usd']:.2f}",f"{s['tco_usd']:.2f}",f"{s['infra_saving_percent']:.2f} %"] for s in c['scenarios']])
p(d,'El costo usa 730 horas y tarifas on demand instance based de Cloud Run us central1: USD 0.000018 por vCPU segundo y 0.000002 por GiB segundo, consultadas el 8 de noviembre de 2026. Comparo una base simulada de dos instancias con dos CPU y cuatro GiB contra dos instancias de una CPU y un GiB. No son facturas de la entrega anterior.')
p(d,'Mantengo un frontend de USD 49.93, provisiones académicas de USD 10 para observabilidad y 5 para almacenamiento. El TCO agrega ocho horas de trabajo a USD 40. Excluyo impuestos, egress, licencias, soporte y balanceador externo; no aplico free tier ni descuentos. Estos conceptos deben cotizarse antes de contratar. Con un millón de solicitudes, el costo unitario de infraestructura estable es USD 0.1701 por mil; ese denominador no acredita capacidad.')
page(d,'Control de gasto y sostenibilidad')
p(d,'Aplico FinOps como responsabilidad compartida entre ingeniería, finanzas y negocio. Etiquetaría proyecto, ambiente, versión y responsable; revisaría semanalmente costo por mil inferencias, utilización, gasto acumulado y pronóstico mensual. El responsable de finanzas valida presupuesto y el de plataforma explica variaciones.')
tab(d,['Control propuesto','Acción y responsable'],[['USD 300 de infraestructura al mes','Aviso a 80 % y 100 %, con pronóstico. Finanzas revisa gasto; plataforma investiga réplicas y logs. No detener automáticamente un servicio crítico.'],['Seis réplicas sostenidas','USD 380.29 estimados: 28.39 % más que la base. Revisar sizing y demanda antes de ampliar.'],['Error budget agotado','Suspender liberaciones no urgentes; plataforma recupera servicio y documenta causa antes de volver a escalar.'],['Optimización periódica','Comparar costo y p95 con mismo tráfico. Usar compromisos sólo con demanda estable; spot únicamente para trabajos tolerantes a interrupción.'],['Sostenibilidad','Medir CPU segundos por mil inferencias y tiempo ocioso; apagar entornos de práctica. No convertir consumo a CO2 sin factor energético y región verificables.']])
p(d,'El escenario con picos añade dos réplicas durante cuarenta horas cada una y cuesta USD 175.81. Es sensibilidad de costo, no una curva de autoscaling medida. La mejora económica es aceptable sólo si se mantiene el objetivo de servicio y se superan las puertas de gobernanza; ahorrar recursos a costa de alertas omitidas sería una falsa eficiencia.')
page(d,'Auditoría técnica y de sesgos')
p(d,'Recalculé el test histórico de 452 noticias, con 61 negativas. Conservo umbral 0.20: TN 366, FP 25, FN 10 y TP 51; accuracy 0.9226, precisión 0.6711, recall 0.8361, F1 0.7445 y AUC 0.9548. La precisión implica carga de revisión humana; los diez falsos negativos justifican mantener fuentes y controles adicionales. No interpreto sentimiento como rendimiento futuro.')
img(d,E/'fairness.png','Figura 4. Recall por longitud e intervalos Wilson al 95 %. Longitud es una condición técnica, no un atributo protegido.',5.8)
p(d,'La diferencia máxima de recall es 13.57 puntos porcentuales. El intervalo bootstrap descriptivo de la brecha es 3.57 a 42.89 puntos, con 2,000 repeticiones y semilla 42. La amplitud y los pocos positivos por grupo impiden una conclusión firme. El máximo de brechas es no negativo por construcción: este intervalo no es una prueba confirmatoria de discriminación.')
p(d,'No contamos con edad, sexo o etnia; no puedo acreditar fairness demográfica. Tampoco infiero esos atributos a partir de personajes ficticios. La siguiente evaluación requeriría finalidad legítima, minimización, revisión legal y muestras adecuadas; compararía TPR y FPR por grupos, prevalencias e incertidumbre. No impondría igualdad de selección sin analizar diferencias de base y daño.')
page(d,'Auditoría ética legal y de seguridad')
tab(d,['Riesgo y nivel','Evidencia y control requerido','Responsable'],[['Licencia comercial crítico','Corpus con CC BY NC SA 3.0. No aprobar uso comercial sin resolver derechos del dato y del modelo derivado.','Jurídico'],['Dominio y sesgo alto','Inglés e historia financiera; sin prueba externa mexicana ni atributos protegidos. Validación nueva y revisión de errores.','Riesgo de modelo'],['Privacidad alto','No hay clientes reales en el repositorio. Antes de producción: inventario, aviso, base de tratamiento, ARCO, seguridad y transferencias.','Privacidad'],['Conflicto de interés alto','1 % compra y 1 % venta son supuestos didácticos. Rentabilidad neta y perfil antes que volumen de operaciones.','Cumplimiento y negocio'],['Seguridad alto','Joblib sólo desde origen confiable; hash no elimina código malicioso. Secretos, OIDC, mínimos privilegios y análisis de dependencias.','Seguridad'],['Trazabilidad medio','Versión, umbral, fuente, acción humana y motivo. Logs sin texto sensible; acceso limitado y retención aprobada.','Plataforma']])
p(d,'La LFPDPPP publicada en 2025 orienta el tratamiento de datos personales privados en México; el expediente debe incluir obligaciones aplicables y revisión profesional antes de usar información patrimonial. La referencia de conflictos de interés de CNBV y la normativa pública de fondos guían esa revisión, sin declarar aquí cumplimiento integral ni una tarifa bancaria real.')
p(d,'Uso NIST AI RMF para organizar Govern, Map, Measure y Manage; ISO IEC 42001 como referencia de gestión, no como certificación obtenida. El AI Act europeo requiere analizar su ámbito territorial si se amplía a la Unión Europea; no afirmo que toda esta práctica mexicana quede automáticamente sujeta ni que sea un sistema de calificación crediticia.')
page(d,'Plan de escalamiento responsable')
tab(d,['Etapa y responsable','Evidencia y criterio de salida'],[['Semanas 1 y 2 · jurídico y privacidad','Resolver licencia comercial, finalidad y transferencias. Acta firmada y matriz normativa. Sin aprobación, conservar sólo laboratorio.'],['Semanas 2 a 4 · riesgo de modelo','Corpus externo en español y contexto mexicano; etiquetado independiente. Predefinir métricas y grupos antes de evaluar. Objetivos propuestos recall ≥0.80 y precisión ≥0.65; no garantizados.'],['Semanas 3 y 4 · plataforma','Prueba cloud ≥60 min a 10 rps, ráfagas, pérdida de réplica y restauración. p95 ≤250 ms, sin errores atribuibles al servicio en ensayo; seguimiento mensual posterior.'],['Semana 5 · comité de riesgo','Revisar TPR y FPR con IC por segmentos. Brecha >10 pp o IC demasiado amplio exige investigación, no aprobación automática. Plan de muestreo y límites documentados.'],['Semana 6 · negocio y operaciones','Piloto en sombra, sin órdenes: revisión humana de todas las señales. Canario 5 %, luego 25 % y 100 % sólo con aprobación y ventanas sanas.'],['Continuo · responsables asignados','Revisión semanal FinOps y mensual de calidad, sesgos y accesos; renovación de licencias y reevaluación ante cambio de modelo o datos.']])
p(d,'Gobernar exige una decisión verificable: config/governance.json contiene cinco aprobaciones pendientes y scripts/governance.py produce production_authorized=false. Es un control académico que no sustituye firmas institucionales. Ningún cambio de una casilla del tablero concede autorización real.')
p(d,'Ante degradación, operaciones pausa el canario, conserva evidencia y vuelve a la versión firmada anterior; riesgo de modelo valida muestras y cumplimiento decide si el piloto puede reanudarse. La actualización no se promueve automáticamente por ahorrar dinero. Si hay exposición de datos, seguridad activa el procedimiento institucional y jurídico evalúa obligaciones de notificación.')
page(d,'Impacto de negocio y conclusiones')
p(d,'Conservo 150 clientes ficticios con posiciones de cinco a veinte millones de pesos para fines didácticos. Superhéroes y villanos permiten explicar personalidades sin revelar datos reales; no se usan como atributos predictivos ni como evidencia de sesgo. El tablero de esta actividad prioriza desempeño, costos y gobernanza.')
p(d,'Mi prioridad es que una revisión ayude al cliente a decidir con su perfil, horizonte y liquidez. El supuesto de 1 % al vender y 1 % al comprar exige descontar ambos cargos; los gastos de cada fondo dependen de su serie y documentación vigente. No sumaría nuevamente un gasto ya incluido en el rendimiento neto publicado. El banco no debe optimizar rotación para generar corretaje a costa del cliente.')
p(d,'Se revisó la accesibilidad de las fichas DICI del catálogo heredado y se guardaron fecha, URL, estado y hash. Eso no certifica que el catálogo abarque todos los fondos actuales ni actualiza las comisiones históricas. Antes de una propuesta real se deberá verificar la ficha y serie concretas y registrar su vigencia.')
p(d,'Concluyo que el rediseño tiene una hipótesis económica favorable y evidencia local de paralelismo sin alterar el modelo. Aún no demuestra operación cloud sostenida, adecuación al español ni equidad demográfica. Recomiendo avanzar por etapas, manteniendo los cinco bloqueos de producción y la revisión humana. La confianza del cliente vale más que presentar como concluida una validación que todavía falta.')
h(d,'Cobertura de la rúbrica')
tab(d,['Criterio de 25 puntos','Secciones y evidencia'],[['Arquitectura y escalabilidad','Diagnóstico, arquitectura, rediseño y Arquitectura.pdf'],['Costos y desempeño','Benchmark de nueve corridas, modelo FinOps y anexo'],['Auditoría responsable','Sesgos, auditoría legal, riesgos y governance_gate.json'],['Plan integral','Etapas, responsables, criterios de salida y rollback']])
page(d,'Referencias')
for ref in refs:p(d,ref)
d.save(O/'Reporte_tecnico.docx')
a=base('Anexo técnico de desempeño costos y gobernanza')
h(a,'Cómo verificar este anexo')
p(a,'Este anexo separa mediciones locales, supuestos económicos y controles pendientes. Los archivos JSON y CSV son la fuente de las tablas. scripts/verify.py recalcula métricas, p95, throughput, costos, integridad del modelo y bloqueo productivo; no genera una nueva carga. Los scripts de experimentación permiten repetir los ensayos en otro equipo, con tiempos que pueden variar.')
tab(a,['Archivo','Origen y alcance'],[['benchmark_requests.csv','40,680 respuestas HTTP; identificadores y latencia por solicitud'],['benchmark.json','Nueve resúmenes, plataforma y condiciones del ensayo'],['fairness.json','Calidad y segmentos retrospectivos del test de 452 noticias'],['batching.json','Cinco repeticiones por tamaño offline 1, 32 y 128'],['costos.json','Cálculo determinista desde config/costs.json'],['governance_gate.json','Cinco aprobaciones pendientes y producción bloqueada']])
p(a,'Se preservó un intento fallido de carga con conexiones nuevas que agotó puertos efímeros del cliente. Después se corrigió con sesiones persistentes por hilo y se repitió todo. intentos_benchmark.json distingue ese problema de un fallo del modelo. Sólo las nueve repeticiones completas integran los resultados.')
page(a,'Resultados completos de rendimiento')
tab(a,['P / C / rep','rps','p95 ms','RSS MiB','CPU núcleos'],[[f"{r['workers']}/{r['concurrency']}/{r['repeat']+1}",f"{r['throughput_rps']:.2f}",f"{r['p95_ms']:.3f}",f"{r['peak_rss_mib']:.2f}",f"{r['cpu_core_equivalents']:.3f}"] for r in b['runs']])
p(a,'P significa procesos y C concurrencia del cliente. CPU 1.0 equivale a un núcleo ocupado. Cada fila contiene 4,520 solicitudes exitosas; el máximo cambio de probabilidad es 1.11 × 10⁻¹⁶, atribuible a precisión numérica. No se midió escalado horizontal entre servidores.')
p(a,'Throughput = solicitudes completadas / segundos transcurridos. p95 = percentil 95 de tiempos cliente HTTP por repetición. Reporto media de los tres p95 al resumir, no un p95 combinado. RSS es el máximo muestreado de la suma de procesos del servidor; puede duplicar memoria compartida.')
img(a,E/'rendimiento.png','Figura 1. Comparación local. Tres repeticiones cortas no reemplazan prueba de estabilidad.',6)
page(a,'Costeo reproducible y sensibilidad')
p(a,'API USD = 3600 × horas instancia × (CPU × 0.000018 + GiB × 0.000002). Horas instancia = mínimas × 730 + extras × horas pico. Infraestructura = API + frontend + 10 + 5. TCO = infraestructura + 8 × 40. Moneda USD; no conversión a MXN.')
tab(a,['Escenario','Horas API','API USD','Infra USD','TCO USD'],[[s['name'],s['api_instance_hours'],f"{s['api_usd']:.2f}",f"{s['infra_usd']:.2f}",f"{s['tco_usd']:.2f}"] for s in c['scenarios']])
tab(a,['Escenario','100 mil req','1 millón req','5 millones req'],[[s['name']]+[f"{s['usd_per_1000_requests'][str(n)]:.4f}" for n in [100000,1000000,5000000]] for s in c['scenarios']])
p(a,'La segunda tabla expresa USD por mil solicitudes, no costo total. Dividir por más solicitudes no demuestra que puedan atenderse con la misma configuración. No se han incluido gastos variables de salida de red, impuestos, licencias o soporte. El ahorro de 42.59 % se calcula sobre infraestructura, no sobre TCO ni sobre una factura real.')
page(a,'Calidad y evaluación exploratoria de fairness')
tab(a,['Grupo','n / positivos','TP / FN','FP / TN','TPR','FPR'],[[x['group'],f"{x['n']} / {x['positives']}",f"{x['tp']} / {x['fn']}",f"{x['fp']} / {x['tn']}",f"{x['recall']:.4f}",f"{x['fpr']:.4f}"] for x in f['groups']])
tab(a,['Grupo','IC Wilson TPR 95 %','Selección','Precisión'],[[x['group'],f"{x['tpr_ci95'][0]:.4f} a {x['tpr_ci95'][1]:.4f}",f"{x['selection_rate']:.4f}",f"{x['precision']:.4f}"] for x in f['groups']])
p(a,'TPR = TP/(TP+FN), FPR = FP/(FP+TN), selección = (TP+FP)/n. Equal opportunity compara TPR; equalized odds compara TPR y FPR; paridad demográfica compara selección; paridad predictiva compara precisión. En esta muestra sólo exploro condiciones de longitud: no son resultados por colectivos protegidos ni una auditoría demográfica concluida.')
p(a,'Los grupos usan límites fijos de 15 y 30 palabras. Hay sólo 12, 35 y 14 positivos. La brecha TPR máxima de 0.1357 y su bootstrap descriptivo [0.0357, 0.4289] no constituyen una prueba de significancia confirmatoria. No reajusté el umbral a partir de estos resultados. Para la siguiente etapa predefiniré segmentos y muestra externa antes de evaluar.')
img(a,E/'fairness.png','Figura 2. Incertidumbre de recall por longitud.',5.8)
page(a,'Lotes y controles operativos')
batch=pd.DataFrame(json.loads((E/'batching.json').read_text())['runs']).groupby('batch_size').mean(numeric_only=True)
tab(a,['Lote','Textos por segundo media','ms amortizados por texto'],[[i,f'{r.throughput_texts_second:.1f}',f'{r.amortized_ms_text:.4f}'] for i,r in batch.iterrows()])
p(a,'Cinco repeticiones por tamaño y orden fijo, con posible calentamiento. El cronómetro incluye vectorización e inferencia, sin HTTP ni espera de cola. Todos los tamaños conservaron las probabilidades. Usaría lotes para preparación offline; no inferiría que un usuario recibe una respuesta en el tiempo amortizado.')
tab(a,['Puerta pendiente','Evidencia necesaria para evaluar'],[['Licencia comercial','Autorización o sustitución del corpus y análisis del modelo derivado'],['Validación México y español','Test externo, revisión de etiquetas y métricas con incertidumbre'],['Privacidad y jurídico','Expediente de finalidad, aviso, seguridad y transferencias'],['Carga y failover cloud','Logs de carga sostenida, pérdida de réplica y recuperación'],['Fairness demográfica','Evaluación lícita con muestra suficiente o limitación de uso acordada']])
p(a,'La salida actual es production_authorized=false. Las pruebas automatizadas verifican bloqueos, integridad y controles económicos; no equivalen a una certificación ni a una auditoría legal externa.')
page(a,'Fuentes y reproducibilidad')
p(a,'Entorno de medición: macOS ARM64, Python 3.12.14, diez CPU lógicas y 16 GiB. requirements.txt fija versiones. Para verificar: instalar dependencias, ejecutar pytest pruebas -q y python scripts/verify.py. Para repetir: python scripts/benchmark.py, python scripts/analyze.py, python scripts/costs.py y python scripts/governance.py. La nueva ejecución sobrescribe evidencias locales; conservar un commit antes de repetir.')
p(a,'El test y modelo se reutilizan con su atribución y licencia en modelos/LICENSE_DATASET.txt. No se usan clientes reales. El directorio contexto conserva la simulación de 150 personajes y las fuentes públicas de fondos como continuidad, separado del benchmark y del análisis de fairness.')
for ref in refs[:6]+[refs[9],refs[10]]:p(a,ref)
a.save(O/'Anexo_tecnico.docx')
print('Documentos generados')
