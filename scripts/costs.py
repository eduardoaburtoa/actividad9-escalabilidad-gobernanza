from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def calculate(c):
 rows=[];front=3600*c['month_hours']*(c['frontend_cpu']*c['cpu_second']+c['frontend_gib']*c['gib_second'])
 for s in c['scenarios']:
  hours=s['min_instances']*c['month_hours']+s['extra_instances']*s['extra_hours']
  api=3600*hours*(s['cpu']*c['cpu_second']+s['gib']*c['gib_second']);infra=api+front+c['observability_allowance']+c['storage_allowance'];tco=infra+c['labor_hours']*c['labor_usd_hour']
  rows.append({**s,'api_instance_hours':hours,'api_usd':api,'frontend_usd':front,'infra_usd':infra,'tco_usd':tco,'usd_per_1000_requests':{str(n):infra/n*1000 for n in c['requests_month']}})
 for row in rows:row['infra_saving_percent']=(1-row['infra_usd']/rows[0]['infra_usd'])*100
 return {'assumptions':c,'scenarios':rows}
if __name__=='__main__':
 out=calculate(json.loads((R/'config/costs.json').read_text()));(R/'evidencias/costos.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out['scenarios'],indent=2))
