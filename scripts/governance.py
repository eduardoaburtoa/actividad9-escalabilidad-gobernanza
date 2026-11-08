from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
def assess(config,model_hash):
 blockers=[]
 for key in ['commercial_license_cleared','mexico_spanish_external_validation','privacy_legal_approval','cloud_load_failover_validated','fairness_demographic_evidence']:
  if config.get(key) is not True:blockers.append(key)
 if model_hash!=config['expected_model_sha256']:blockers.append('model_integrity')
 if config.get('threshold')!=.2:blockers.append('threshold_changed')
 if not config.get('human_review_required') or config.get('live_trading_allowed'):blockers.append('human_control')
 return {'production_authorized':not blockers,'blockers':blockers,'note':'Control académico de aprobación; no sustituye firma de responsables ni certifica cumplimiento.'}
if __name__=='__main__':
 out=assess(json.loads((R/'config/governance.json').read_text()),hashlib.sha256((R/'modelos/modelo_SVM_calibrada.joblib').read_bytes()).hexdigest());(R/'evidencias/governance_gate.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
