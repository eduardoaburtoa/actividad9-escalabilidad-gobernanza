"""Secciones editoriales acumulativas; no modifica modelo ni evidencia histórica."""
def scaling(d,h,p,tab,root):
 h(d,'Escalabilidad vertical y horizontal')
 tab(d,['Dimensión','Qué cambia y límite','Costo y evidencia','Mi decisión'],[
 ['Escalabilidad vertical','CPU y RAM de una réplica. Límite: cuota máxima, memoria y paralelismo aprovechable.','Rightsizing simulado de 2 CPU/4 GiB a 1 CPU/1 GiB: API USD 231.26 a 105.12/mes; infraestructura USD 296.20 a 170.05.','Reducir tamaño sólo después de probar carga y memoria con cuotas reales.'],
 ['Escalabilidad horizontal','Número de réplicas independientes. Límite: coordinación, cuotas, cola y presupuesto.','Dos procesos locales alcanzan media 1,270.8 rps y p95 medio 9.08 ms; esto sólo evidencia paralelismo intrahost.','Proponer 2 a 6 réplicas pequeñas en Cloud Run: crecer por unidades y tolerar pérdida de una réplica.']])
 p(d,'Elijo escalabilidad horizontal para ajustar capacidad por demanda sin concentrarla en una única instancia. Una réplica adicional tiene costo incremental y puede aislar un fallo de proceso; no garantiza tolerancia regional. Mantengo el eje vertical como ajuste del tamaño por réplica y no como sustituto de redundancia.')
 p(d,'Dos procesos en un host no son escalado horizontal de nube. Las repeticiones de 3.51 a 8.01 segundos no prueban carga sostenida. El cambio vertical es un escenario económico, no una comparación experimental con límites de CPU y RAM impuestos. La decisión debe confirmarse en el ensayo cloud antes del piloto.')
