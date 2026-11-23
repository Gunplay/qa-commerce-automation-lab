"""Create the short critical checklist. --overwrite resets manual progress: use deliberately."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from collections import Counter
from xml.sax.saxutils import escape
import json, sys
import xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/learning/artifacts/site-automation-plan.xlsx'
areas=json.loads((ROOT/'scripts/qa/critical_test_plan.json').read_text())
NS='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
REL='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
sheets=[]
def f(expr,n): return ('f',expr,n)
coverage_states=['Покрито','У роботі','Заплановано','Заблоковано']
run_states=['Пройдено','Впав']
allcases=[r for a in areas for r in a['cases']]
coverage=Counter(r[5] for r in allcases)
runs=Counter(r[6] for r in allcases)
summary=[
['Критичні перевірки магазину — основний файл прогресу'],
['Узгоджена коротка версія: 39 перевірок, по 3–4 на розділ. Покупка, гроші, акаунт і приватність. Детальний план — лише резерв.'],
['Кожен кейс запускаємо незалежно: новий браузерний контекст і власні тестові дані; A/B — різні покупці, не розміри. ID кейсів не змінюємо.'],
['Покрито = є автотест з усіма потрібними assertions. Заплановано = ще не написано; У роботі = пишемо; Заблоковано = немає вимоги/реалізації/середовища.'],
['Заплановано не означає готові дані. Числа в умовах — майбутній контрольний набір, а не поточні ціни. Наповнення БД відкладено; CI не підтверджений.'],
['Старт 20.10.2026: 3 перевірки у 2 наявних UI-тестах, створених з допомогою AI. REG-03 — частина того ж тесту, що REG-01. Нових запусків під час review не було.'],
['Ведемо прогрес ТУТ: змінюй Покриття й Останній запуск; у «Автотест / доказ» вписуй шлях тесту, дату, результат і лог/посилання. Порожнє посилання не є доказом проходження.'],
['Розділ','Кейсів','Покрито','У роботі','Заплановано','Заблоковано','Пройдено','Впав'],
]
links={}
for i,a in enumerate(areas,9):
 end=4+len(a['cases']); q="'"+a['name']+"'"; c=Counter(r[5] for r in a['cases']); rr=Counter(r[6] for r in a['cases'])
 row=[a['name'],len(a['cases'])]
 row += [f(f'COUNTIF({q}!F5:F{end},"{state}")',c[state]) for state in coverage_states]
 row += [f(f'COUNTIF({q}!G5:G{end},"{state}")',rr[state]) for state in run_states]
 summary.append(row)
 links[f'A{i}']=f"'{a['name']}'!A1"
last=len(summary)
totals=[len(allcases)]+[coverage[state] for state in coverage_states]+[runs[state] for state in run_states]
summary.append(['Разом']+[f(f'SUM({chr(65+j)}9:{chr(65+j)}{last})',v) for j,v in enumerate(totals,1)])
summary.append(['Наступне: REG-04 → AUTH-01/02/05 → PRD-02 → кошик → CHK-01. Класові Page Objects; assertions у spec. Один тест може покривати кілька рядків.'])
summary.append(['«Пройдено/Впав» — останні записані результати, не результат сьогоднішньої перевірки. Нову дату додаємо після реального запуску. Фільтри — у заголовках кожної вкладки.'])
summary.append(['Межі: покупецький сайт і пов’язані API; не повний security-аудит і не Admin UI. Реальна оплата, пошта та незавершені функції відкладені.'])
sheets.append(dict(name='00 Прогрес',rows=summary,widths=[32,12,14,17,19,20,17,14],header=8,merge=[f'A{i}:H{i}' for i in range(1,8)]+[f'A{i}:H{i}' for i in range(last+2,len(summary)+1)],links=links,feature=False))
headers=['ID','User story','Дані / умови','Кроки','Очікуваний результат','Покриття','Останній запуск','Автотест / доказ']
for a in areas:
 rows=[[a['name']+' — '+str(len(a['cases']))+' критичні перевірки'],['3–4 перевірки розділу. Умови готуємо до запуску. Покриття та результат — окремі статуси; шлях тесту, дату й лог вписуємо у «Автотест / доказ».'],['← Назад до прогресу'],headers]+a['cases']
 sheets.append(dict(name=a['name'],rows=rows,widths=[13,38,48,52,62,22,22,72],header=4,merge=['A1:H1','A2:H2','A3:H3'],links={'A3':"'00 Прогрес'!A1"},feature=True))

def col(n): return chr(64+n)
def sheet_xml(s):
 h=s['header']; end=len(s['rows']); maxcol=col(len(s['widths']))
 parts=[f'<worksheet xmlns="{NS}"><sheetViews><sheetView workbookViewId="0" zoomScale="85"><pane xSplit="1" ySplit="{h}" topLeftCell="B{h+1}" activePane="bottomRight" state="frozen"/></sheetView></sheetViews><cols>']
 parts += [f'<col min="{i}" max="{i}" width="{w}" customWidth="1"/>' for i,w in enumerate(s['widths'],1)]
 parts.append('</cols><sheetData>')
 for rn,row in enumerate(s['rows'],1):
  height=34 if rn<=h or not s['feature'] else 120
  parts.append(f'<row r="{rn}" ht="{height}" customHeight="1">')
  for cn,v in enumerate(row,1):
   addr=col(cn)+str(rn); style=1 if rn in [1,h] else (2 if rn%2==0 and rn>h else 0)
   if addr in s['links']:style=3
   if isinstance(v,tuple):parts.append(f'<c r="{addr}" s="{style}"><f>{escape(v[1])}</f><v>{v[2]}</v></c>')
   elif isinstance(v,int):parts.append(f'<c r="{addr}" s="{style}"><v>{v}</v></c>')
   else:parts.append(f'<c r="{addr}" t="inlineStr" s="{style}"><is><t xml:space="preserve">{escape(v)}</t></is></c>')
  parts.append('</row>')
 parts.append('</sheetData>')
 if s['feature']:parts.append(f'<autoFilter ref="A{h}:{maxcol}{end}"/>')
 parts.append(f'<mergeCells count="{len(s["merge"])}">'+''.join(f'<mergeCell ref="{ref}"/>' for ref in s['merge'])+'</mergeCells>')
 if s['feature']:
  for priority,(c,text,dxf) in enumerate([('F','Покрито',0),('F','Заблоковано',1),('F','У роботі',2),('G','Впав',3),('G','Пройдено',0)],1):
   parts.append(f'<conditionalFormatting sqref="{c}5:{c}{end}"><cfRule type="expression" dxfId="{dxf}" priority="{priority}"><formula>${c}5="{text}"</formula></cfRule></conditionalFormatting>')
  parts.append('<dataValidations count="2">')
  for c,choices in [('F','Заплановано,У роботі,Покрито,Заблоковано'),('G','Не запускали,Пройдено,Впав')]:
   parts.append(f'<dataValidation type="list" allowBlank="0" showErrorMessage="1" sqref="{c}5:{c}{end}"><formula1>"{choices}"</formula1></dataValidation>')
  parts.append('</dataValidations>')
 parts.append('<hyperlinks>')
 for ref,loc in s['links'].items():parts.append(f'<hyperlink ref="{ref}" location="{escape(loc)}"/>')
 parts.append('</hyperlinks></worksheet>')
 return ''.join(parts)
styles=f'<styleSheet xmlns="{NS}"><fonts count="3"><font><sz val="11"/><name val="Calibri"/></font><font><b/><color rgb="FFFFFFFF"/><sz val="12"/><name val="Calibri"/></font><font><u/><color rgb="FF0563C1"/><sz val="11"/><name val="Calibri"/></font></fonts><fills count="4"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF203864"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FFF2F6FC"/></patternFill></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="4">'
for font,fill in [(0,0),(1,2),(0,3),(2,0)]: styles+=f'<xf numFmtId="0" fontId="{font}" fillId="{fill}" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>'
styles+='</cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles><dxfs count="4">'
for color in ['E2EFDA','FFF2CC','DDEBF7','F8CBAD']:styles+=f'<dxf><fill><patternFill patternType="solid"><fgColor rgb="FF{color}"/></patternFill></fill></dxf>'
styles+='</dxfs></styleSheet>'
parts={
'[Content_Types].xml':'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'+''.join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1,len(sheets)+1))+'</Types>',
'_rels/.rels':f'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="{REL}/officeDocument" Target="xl/workbook.xml"/></Relationships>',
'xl/workbook.xml':f'<workbook xmlns="{NS}" xmlns:r="{REL}"><sheets>'+''.join(f'<sheet name="{s["name"]}" sheetId="{i}" r:id="rId{i}"/>' for i,s in enumerate(sheets,1))+'</sheets><calcPr fullCalcOnLoad="1"/></workbook>',
'xl/_rels/workbook.xml.rels':f'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(f'<Relationship Id="rId{i}" Type="{REL}/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1,len(sheets)+1))+f'<Relationship Id="rId{len(sheets)+1}" Type="{REL}/styles" Target="styles.xml"/></Relationships>',
'xl/styles.xml':styles}
parts.update({f'xl/worksheets/sheet{i}.xml':sheet_xml(s) for i,s in enumerate(sheets,1)})
assert all(3<=len(a['cases'])<=4 for a in areas)
ids=[r[0] for a in areas for r in a['cases']]
assert len(ids)==len(set(ids))==39
assert all(len(r)==8 and all(r[:7]) for r in allcases)
assert all(r[5] in coverage_states for r in allcases)
assert all(r[6] in ['Не запускали','Пройдено','Впав'] for r in allcases)
assert all((ROOT/r[7].split(' → ')[0]).is_file() for r in allcases if r[5]=='Покрито')
for xml in parts.values():E.fromstring(xml)
if OUT.exists() and '--overwrite' not in sys.argv:raise SystemExit('Workbook exists; --overwrite deliberately resets progress.')
with ZipFile(OUT,'w',ZIP_DEFLATED) as z:
 for name,xml in parts.items():z.writestr(name,'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+xml)
with ZipFile(OUT) as z:assert z.testzip() is None
print(f'Created and validated: {len(allcases)} checks, 11 feature tabs (3–4 each); {dict(coverage)}; {dict(runs)}.')
