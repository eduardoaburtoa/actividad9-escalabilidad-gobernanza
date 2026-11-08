import json,sys
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R),str(R/'scripts')]
from costs import calculate
from governance import assess
from analyze import wilson
from backend.main import Scenario,scenario
C=json.loads((R/'config/governance.json').read_text())
def test_production_fails_closed():
 assert not assess(C,C['expected_model_sha256'])['production_authorized']
@pytest.mark.parametrize('change',[{'threshold':.5},{'human_review_required':False},{'live_trading_allowed':True}])
def test_guardrails(change):
 c={**C,**change};assert not assess(c,C['expected_model_sha256'])['production_authorized']
def test_hash_block():assert 'model_integrity' in assess(C,'bad')['blockers']
def test_cost_zero_variable_rates():
 c=json.loads((R/'config/costs.json').read_text());c.update(cpu_second=0,gib_second=0)
 assert all(r['infra_usd']==15 for r in calculate(c)['scenarios'])
def test_more_instances_cost_more():
 c=json.loads((R/'config/costs.json').read_text());r=calculate(c)['scenarios'];assert r[3]['infra_usd']>r[2]['infra_usd']>r[1]['infra_usd']
def test_unknown_denominator_not_zero():assert wilson(0,0)==[None,None]
def test_client_profile_guard():
 d=Scenario(cliente_id='C001',proporcion=.5,mejora_anual_pp=10,meses=12,gastos_adicionales_anuales_pp=0,perfil_destino='Agresivo');assert not scenario(d)['elegible_para_revision']
def test_costs_prevent_unprofitable_rotation():
 d=Scenario(cliente_id='C001',proporcion=.5,mejora_anual_pp=1,meses=12,gastos_adicionales_anuales_pp=0,perfil_destino='Moderado');assert not scenario(d)['elegible_para_revision']
