"""Comprueba enlaces locales y conservación del texto de los entregables web."""
from pathlib import Path
import re
import zipfile
from urllib.parse import unquote
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def verify():
    checked = 0
    for page in ROOT.rglob('*.md'):
        if '.git' in page.parts:
            continue
        content = page.read_text()
        for link in re.findall(r'\]\(([^)]+)\)', content):
            if link.startswith(('https://', 'http://', 'mailto:')):
                continue
            target, _, anchor = unquote(link).partition('#')
            destination = (page.parent / target).resolve() if target else page
            assert destination.exists(), (page.relative_to(ROOT), link)
            if anchor and 'seccion-' in anchor:
                assert f'id="{anchor}"' in destination.read_text(), link
            checked += 1
    paragraphs = 0
    for name, folder in [('Reporte_tecnico','01-reporte-tecnico'), ('Anexo_tecnico','02-anexo-tecnico')]:
        with zipfile.ZipFile(ROOT / 'documentos' / (name + '.docx')) as source:
            xml = ET.fromstring(source.read('word/document.xml'))
        markdown = (ROOT / 'documentos' / folder / 'README.md').read_text().replace('\\|', '|')
        for paragraph in xml.findall('.//w:body/w:p', NS):
            text = ''.join(t.text or '' for t in paragraph.findall('.//w:t', NS))
            if text:
                assert text in markdown, (name, text[:100])
                paragraphs += 1
    print(f'Documentación válida: {checked} enlaces locales; {paragraphs} párrafos originales conservados.')

if __name__ == '__main__':
    verify()
