from pathlib import Path
from streamlit.testing.v1 import AppTest
def test_dashboard():
 app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run(timeout=30)
 assert not app.exception
 assert len(app.tabs)==5
 app.slider[0].set_value(6).run()
 assert not app.exception
 assert any('380.29' in str(x.value) for x in app.metric)
