"""Puente de alcance y costo, sin recalcular ROI ni modificar costos históricos."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def main():
 f=json.loads((R/'config/fase1.json').read_text());c=json.loads((R/'evidencias/costos.json').read_text());stable=c['scenarios'][1]['infra_usd'];monthly=f['clients']*f['planning_days_month']*f['inferences_per_evaluation_assumption'];annual=stable*12*f['fx_mxn_per_usd']
 out={'source_inputs':f,'monthly_evaluations':monthly,'pilot_monthly_evaluations':f['pilot_advisors']*f['clients_per_advisor']*f['planning_days_month'],'infra_month_usd':stable,'infra_month_mxn':stable*f['fx_mxn_per_usd'],'infra_year_mxn':annual,'share_of_fase1_opex_percent':annual/f['annual_operation_mxn']*100,'infra_mxn_client_month':stable*f['fx_mxn_per_usd']/f['clients'],'scenario_multiples':{str(n):n/monthly for n in c['assumptions']['requests_month']},'scope':'Una inferencia por evaluación es supuesto de dimensionamiento. Infraestructura de NLP es sólo un componente del proyecto; no ahorro del presupuesto total ni validación del ROI.'}
 (R/'evidencias/negocio_fase1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
