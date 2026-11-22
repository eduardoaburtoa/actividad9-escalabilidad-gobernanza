# Revisión final · Actividad 9 · versión 1.1.0

La revisión conserva el modelo, las 40,680 solicitudes, las nueve mediciones y los bloqueos productivos. La cantidad de menciones sólo verifica visibilidad editorial: no sustituye la evaluación de calidad.

| Rama | Criterio | Resultado | PR y validación |
|---|---|---|---|
| mejora/01-vertical-y-horizontal | 1 | Contraste vertical/horizontal | [PR #2](https://github.com/eduardoaburtoa/actividad9-escalabilidad-gobernanza/pull/2) · [CI verde](https://github.com/eduardoaburtoa/actividad9-escalabilidad-gobernanza/actions/runs/42559502504) |
| mejora/02-costos-anclados-al-negocio | 2 y 4 | Costos ligados a Fase I | [PR #3](https://github.com/eduardoaburtoa/actividad9-escalabilidad-gobernanza/pull/3) · [CI verde](https://github.com/eduardoaburtoa/actividad9-escalabilidad-gobernanza/actions/runs/42559711389) |
| mejora/03-fairness-en-el-reporte | 3 | Fairness con incertidumbre | [PR #4](https://github.com/eduardoaburtoa/actividad9-escalabilidad-gobernanza/pull/4) · [CI verde](https://github.com/eduardoaburtoa/actividad9-escalabilidad-gobernanza/actions/runs/42560057474) |
| mejora/04-anexo-completo | 1, 2 y 3 | Anexo con métricas explícitas | [PR #5](https://github.com/eduardoaburtoa/actividad9-escalabilidad-gobernanza/pull/5) · [CI verde](https://github.com/eduardoaburtoa/actividad9-escalabilidad-gobernanza/actions/runs/42560211502) |
| mejora/05-cierre-formal | 4 | Declaración y cierre formal | [PR #6](https://github.com/eduardoaburtoa/actividad9-escalabilidad-gobernanza/pull/6) · [CI verde](https://github.com/eduardoaburtoa/actividad9-escalabilidad-gobernanza/actions/runs/42560474463) |
| mejora/06-continuidad-y-perfil | 4 | Continuidad y perfil | [PR #7](https://github.com/eduardoaburtoa/actividad9-escalabilidad-gobernanza/pull/7) · [CI verde](https://github.com/eduardoaburtoa/actividad9-escalabilidad-gobernanza/actions/runs/42560590536) |
| mejora/07-exportacion-final | Todos | DOCX/PDF, XLSX, enlaces y paridad | [PR #8](https://github.com/eduardoaburtoa/actividad9-escalabilidad-gobernanza/pull/8) · [Checks de la rama](https://github.com/eduardoaburtoa/actividad9-escalabilidad-gobernanza/actions?query=branch%3Amejora%2F07-exportacion-final) |

El perfil recibió un [commit separado](https://github.com/eduardoaburtoa/eduardoaburtoa/commit/f93cb650a10e29bd48ec78ff46390185bc6dfced) con la tabla de siete entregas. Se conserva la salvedad de portafolio personal.

| Indicador editorial | Antes | Después |
|---|---:|---:|
| «escalabilidad vertical» en reporte | 0 | 2 |
| «escalabilidad horizontal» en reporte | 0 | 2 |
| «fairness» en reporte | 2 | 6 |
| «Fase I» en reporte, sin contar Fase II | 0 | 6 |
| «Fase I» en anexo | 0 | 8 |
| Apartados del anexo con encabezado explícito: costos, latencia, throughput, recursos y fairness | 2/5 | 5/5 |

Reporte PDF: 18 páginas. Anexo PDF: 12 páginas. Las tablas de cobertura usan secciones, por lo que no dependen de variaciones de paginación en Google Docs. README remite a páginas del PDF.

## Verificación sobre main

```bash
git clone https://github.com/eduardoaburtoa/actividad9-escalabilidad-gobernanza.git
cd actividad9-escalabilidad-gobernanza
git switch main
git pull --ff-only
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest pruebas -q
python scripts/verify.py
python scripts/validate_delivery.py
streamlit run app.py
```

No ejecutar benchmark.py para esta validación: generaría tiempos nuevos. El checkout debe conservar historial para comparar con f770a14. En Windows: `.venv\\Scripts\\activate`.

## Documentos y fórmulas

- [Reporte PDF](Reporte_tecnico.pdf) · [Word](Reporte_tecnico.docx).
- [Anexo PDF](Anexo_tecnico.pdf) · [Word](Anexo_tecnico.docx) · [Excel editable](Anexo_tecnico.xlsx).
- [Google Docs: reporte](https://docs.google.com/document/d/1cMp3WDCrJkl1x_W6ingDuwyoSVslExBId_ULa-wSJVs/edit) y [anexo](https://docs.google.com/document/d/12Pbozhz5y7g3ldfxwKvP_1mU0_0ilrX4OxzmVmfxns4/edit), editables por su propietario y consultables por enlace. Verificados en incógnito.
- El XLSX compara cuatro escenarios y contiene 78 fórmulas. Se probó aumentar la tarifa CPU, observar el cambio y restaurarla. [Resultado de esa prueba](../evidencias/validacion_xlsx.json).
- [Paridad de texto y tablas de Google Docs/Word](../evidencias/paridad_documentos.json) y [conteos reproducibles](../evidencias/revision_editorial.json).

Los binarios se generaron únicamente en la rama 07. La reconstrucción editorial requiere python-docx y pandas, LibreOffice/Poppler para renderizar, y Node con @oai/artifact-tool para el XLSX. Esas herramientas no son necesarias para ejecutar el tablero o validar la entrega; las fórmulas pueden editarse en Excel o Google Sheets.

La nube sigue siendo propuesta; cinco aprobaciones pendientes impiden el uso productivo. La auditoría por longitud es exploratoria, no equidad demográfica. La IA no sustituye el criterio del banquero; lo aumenta.

