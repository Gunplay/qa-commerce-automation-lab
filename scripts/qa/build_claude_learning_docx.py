"""Build the complete Ukrainian learning guide as a styled DOCX using stdlib."""
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED
import re

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'docs/learning/claude-code-for-qa.md'
OUTPUT = ROOT / 'docs/learning/artifacts/claude-code-for-qa.docx'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKG = 'http://schemas.openxmlformats.org/package/2006/relationships'
ET.register_namespace('w', W)
ET.register_namespace('r', R)


def el(name, attrs=None, text=None):
    node = ET.Element('{%s}%s' % (W, name))
    for k, v in (attrs or {}).items():
        node.set('{%s}%s' % (W, k), str(v))
    node.text = text
    return node


def sub(parent, name, attrs=None, text=None):
    node = el(name, attrs, text)
    parent.append(node)
    return node


def xml(node):
    return ET.tostring(node, encoding='utf-8', xml_declaration=True)


rels = ET.Element('Relationships', xmlns=PKG)
for ident, kind, target in [('styles', 'styles', 'styles.xml'), ('header', 'header', 'header1.xml'), ('footer', 'footer', 'footer1.xml')]:
    ET.SubElement(rels, 'Relationship', Id=ident, Type=R + '/' + kind, Target=target)

doc = el('document')
body = sub(doc, 'body')
link_number = 0


def run(p, text, bold=False, code=False, color=None):
    r = sub(p, 'r')
    if bold or code or color:
        props = sub(r, 'rPr')
        if bold:
            sub(props, 'b')
        if code:
            sub(props, 'rFonts', {'ascii': 'Consolas', 'hAnsi': 'Consolas'})
            sub(props, 'sz', {'val': 19})
        if color:
            sub(props, 'color', {'val': color})
            sub(props, 'u', {'val': 'single'})
    for i, part in enumerate(text.split('\n')):
        if i:
            sub(r, 'br')
        t = sub(r, 't', text=part)
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')


def inline(p, text):
    global link_number
    pattern = r'(\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*|`([^`]+)`)'
    start = 0
    for m in re.finditer(pattern, text):
        run(p, text[start:m.start()])
        if m.group(2):
            label, target = m.group(2), m.group(3)
            if '://' not in target:
                # Relative to artifacts/, so links remain useful after moving the repo.
                target = '../' + target
            link_number += 1
            ident = f'link{link_number}'
            ET.SubElement(rels, 'Relationship', Id=ident, Type=R + '/hyperlink', Target=target, TargetMode='External')
            h = sub(p, 'hyperlink', {'history': '1'})
            h.set('{%s}id' % R, ident)
            run(h, label, color='146B8A')
        elif m.group(4):
            run(p, m.group(4), bold=True)
        else:
            run(p, m.group(5), code=True)
        start = m.end()
    run(p, text[start:])


def para(text='', style='Normal', parent=body, before_page=False):
    p = sub(parent, 'p')
    props = sub(p, 'pPr')
    sub(props, 'pStyle', {'val': style})
    if before_page:
        sub(props, 'pageBreakBefore')
    inline(p, text)
    return p


def heading(text, n=1, anchor=None, new_page=False):
    p = para(text, 'Heading%d' % n, before_page=new_page)
    if anchor:
        p.insert(1, el('bookmarkStart', {'id': anchor, 'name': 'section' + anchor}))
        p.append(el('bookmarkEnd', {'id': anchor}))
    return p


def table(rows):
    tbl = sub(body, 'tbl')
    props = sub(tbl, 'tblPr')
    sub(props, 'tblW', {'w': 9638, 'type': 'dxa'})
    sub(props, 'tblLayout', {'type': 'fixed'})
    borders = sub(props, 'tblBorders')
    for side in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        sub(borders, side, {'val': 'single', 'sz': '4', 'color': 'D9E3EB'})
    margins = sub(props, 'tblCellMar')
    for side in ['top', 'left', 'bottom', 'right']:
        sub(margins, side, {'w': 100, 'type': 'dxa'})
    cols = len(rows[0])
    widths = [1800, 2800, 2600, 2438] if cols == 4 else ([1900, 3900, 3838] if cols == 3 else [4100, 5538])
    grid = sub(tbl, 'tblGrid')
    for width in widths:
        sub(grid, 'gridCol', {'w': width})
    for index, cells in enumerate(rows):
        tr = sub(tbl, 'tr')
        tr_props = sub(tr, 'trPr')
        sub(tr_props, 'cantSplit')
        if index == 0:
            sub(tr_props, 'tblHeader')
        for col, value in enumerate(cells):
            tc = sub(tr, 'tc')
            pr = sub(tc, 'tcPr')
            sub(pr, 'tcW', {'w': widths[col], 'type': 'dxa'})
            sub(pr, 'vAlign', {'val': 'center'})
            if index == 0 or index % 2 == 0:
                sub(pr, 'shd', {'fill': '163B57' if index == 0 else 'F1F5F8'})
            p = para(value, 'TableHeader' if index == 0 else 'TableText', parent=tc)
    para('', 'Spacer')


source = SOURCE.read_text()
title = source.splitlines()[0][2:]
para('QA COMMERCE AUTOMATION LAB', 'Eyebrow')
para(title, 'Title')
para('Практичний посібник\nПояснення • приклади • послідовність дій', 'Subtitle')
para('Для переходу від manual QA до усвідомленої роботи з AI та Playwright.', 'Lead')
para('Повний зміст навчальної інструкції та додатковий маршрут практики.', 'Lead')
para('21 жовтня 2026  |  Версія для Word', 'Meta')
para('Як користуватися', 'Heading2')
para('Спочатку прочитай розділи 1–4, потім 5–8. У розділах 9–11 знайдеш підготовку й джерела. Розділ 12 проведе тебе через практику: що відкрити, що написати, як перевірити та коли переходити далі.')
para('Готові тексти запитів виділені світлим блоком: їх можна скопіювати в чат. Команди з розділу 12 виконуй на відповідному кроці, з кореня qa-commerce-automation-lab.', 'Callout')

heading('Зміст', new_page=True)
headings = re.findall(r'^## (.+)$', source, re.M)
for i, name in enumerate(headings + ['12 Покрокова практика', '13 Словник для швидкого повторення'], 1):
    p = para()
    h = sub(p, 'hyperlink', {'anchor': 'section' + str(i)})
    run(h, name, color='146B8A')
para('Заголовки також доступні в області навігації Word. Для локальних посилань зберігай документ у папці docs/learning/artifacts; шляхи до файлів наведені в розділі 12.', 'Meta')

# Preserve all source paragraphs, list items, tables, and code blocks in order.
lines = source.splitlines()[1:]
i = 0
chapter = 0
while i < len(lines):
    line = lines[i]
    if not line.strip():
        i += 1
        continue
    if line.startswith('```'):
        block = []
        i += 1
        while i < len(lines) and not lines[i].startswith('```'):
            block.append(lines[i])
            i += 1
        p = para('', 'Code')
        run(p, '\n'.join(block), code=True)
    elif line.startswith('## '):
        chapter += 1
        heading(line[3:], anchor=str(chapter), new_page=chapter in [1, 3, 5, 7, 9, 10, 11])
    elif line.startswith('### '):
        heading(line[4:], 2)
    elif line.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            cells = [x.strip() for x in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?', c) for c in cells):
                rows.append(cells)
            i += 1
        table(rows)
        continue
    else:
        para(line, 'ListText' if re.match(r'^\d+\. ', line) else 'Normal')
    i += 1

heading('12 Покрокова практика', anchor='12', new_page=True)
para('Це додатковий маршрут до повної інструкції вище. Працюй по одному кроку. На підготовці достатньо читання та власного запиту; налаштування й цільовий тест розбиратимемо разом.')
steps = [
('Крок 1 Відкрий потрібний проєкт',
 'У редакторі відкрий qa-commerce-automation-lab. Знайди docs/learning/progress.md і docs/learning/artifacts/site-automation-plan.xlsx. В Excel відкрий вкладку «00 Прогрес» та знайди REG-04.',
 'Запиши своїми словами мету REG-04 та що вже покрито. Не змінюй статус кейсу лише після читання.'),
('Крок 2 Підготуй власний запит',
 'Прочитай розділ 3. За його зразком напиши 4–6 речень: задача, файли, обсяг допомоги, очікуваний результат. Надішли запит ментору.',
 'У відповідь маєш отримати пояснення та одну конкретну дію. Якщо відповідь завелика, попроси залишити лише найближчий крок.'),
('Крок 3 Простеж шлях виконання',
 'Відкрий tests/ui/registration.spec.ts і tests/pages/registrationPage.ts. Знайди створення екземпляра RegistrationPage, виклики open, fillRegForm і submit. Потім знайди assertions у spec.',
 'Поясни ланцюжок spec → екземпляр → метод → locator → дія → assertion. Незрозуміле місце познач для розбору.'),
('Крок 4 Уточни один негативний випадок',
 'Негативний сценарій перевіряє реакцію на некоректні або неповні дані. Разом обери одне обов’язкове поле. Запиши передумови, дію та очікувану реакцію. Звір очікування з кейсом і вимогами; поточну поведінку UI зафіксуй окремо.',
 'Має бути зрозуміло, яка саме перевірка підтвердить правило. Якщо вимоги не визначають поведінку, запиши питання до вимог.'),
('Крок 5 Зроби одну зміну та отримай review',
 'Реалізуй лише погоджений мікрокрок. Дії з елементами сторінки залишай у RegistrationPage, очікування сценарію — у spec. Збережи файл і попроси review за шаблоном розділу 3.',
 'Кожне зауваження має містити місце в коді та причину. Виправ одну проблему, поясни зміни й тільки потім переходь до наступної.'),
('Крок 6 Перевір типи та запусти погоджений тест',
 'Спочатку перевір список тестів і TypeScript командами нижче. Для браузерного запуску потрібні працюючі Docker, backend і storefront. Якщо середовище зупинено, запусти npm run dev в окремому терміналі. Точний тест обери за його назвою разом із ментором.',
 'Збережи повну команду та результат. Помилка типів, помилка запуску браузера й невідповідність assertion — різні причини, їх потрібно розбирати окремо.'),
('Крок 7 Зафіксуй доказ та поясни результат',
 'Після завершення сценарію переглянь diff. Поясни, яке правило перевірено і чого тест не доводить. Разом проведемо контрольоване падіння на тестовому випадку та відновимо правильне очікування.',
 'В Excel онови лише відповідний кейс: покриття, результат останнього запуску, дату та доказ. Навчальну допомогу й наступний крок зафіксуємо у progress.md.'),
('Крок 8 Повтори review та виріши чи потрібен skill',
 'На наступних двох-трьох змінах використовуй ті самі критерії. Запиши, що AI пропускає або трактує неправильно. Після цього окремо замовимо створення qa-playwright-review та перевіримо його на відомій помилці й новому прикладі.',
 'Успіх — корисні й перевірювані зауваження. Далі продовжуємо CI; браузерний MCP або CLI обираємо під конкретну задачу.'),
]
for name, action, result in steps:
    heading(name, 2)
    para('Що робити. ' + action)
    para('Результат кроку. ' + result, 'Callout')
    if name.startswith('Крок 6'):
        para('Перехід із батьківської папки QA-AUTO-ROAD-MAP:', 'Meta')
        para('cd qa-commerce-automation-lab', 'Code')
        para('Перелік тестів без запуску браузера та перевірка типів:', 'Meta')
        para('npx playwright test --list\nnpx tsc -p tests/tsconfig.json', 'Code')
        para('Наявний тест успішної реєстрації можна запустити окремо:', 'Meta')
        para('npx playwright test tests/ui/registration.spec.ts --headed -g "new customer can register"', 'Code')
        para('Ця остання команда виконує успішну реєстрацію й створює нового покупця. Для нового REG-04 обери його власну назву тесту. Seed і скидання БД для цього маршруту не потрібні.', 'Callout')

heading('13 Словник для швидкого повторення', anchor='13', new_page=True)
table([
 ['Термін', 'Що означає на нашому прикладі'],
 ['Prompt', 'Твій запит до AI із задачею та очікуваним результатом.'],
 ['Review', 'Перевірка роботи з конкретними поясненнями та зауваженнями.'],
 ['Spec', 'Файл із тестовими сценаріями, наприклад registration.spec.ts.'],
 ['POM та екземпляр', 'Клас описує роботу зі сторінкою; new RegistrationPage(page) створює конкретний об’єкт цього класу.'],
 ['Locator', 'Спосіб знайти елемент, наприклад поле email.'],
 ['Assertion', 'Перевірка очікування, наприклад показу email у кабінеті.'],
 ['await', 'Очікування завершення асинхронної операції перед продовженням коду.'],
 ['CLI', 'Командний інтерфейс: запускаєш інструмент командою в терміналі.'],
 ['CI', 'Автоматичні перевірки змін, у нас — GitHub Actions.'],
 ['Smoke', 'Невеликий набір перевірок найважливішої працездатності.'],
 ['Trace', 'Запис виконання тесту для діагностики дій і помилок.'],
 ['Cleanup', 'Очищення даних, створених тестом.'],
 ['Expected та actual', 'Очікуваний та фактичний результати.'],
])
para('Перед наступним заняттям', 'Heading2')
for text in ['Прочитав розділи 1–8 і виписав незрозумілі терміни.', 'Підготував власний запит для REG-04.', 'Знайшов spec, RegistrationPage і кейс у трекері.', 'Можу пояснити два критерії review.', 'Розумію різницю між аналізом коду, дослідженням браузера та запуском тесту.']:
    para('☐ ' + text, 'ListText')

# A4, a restrained blue palette, repeating table headers, page numbers.
sect = sub(body, 'sectPr')
for kind in ['header', 'footer']:
    ref = sub(sect, kind + 'Reference', {'type': 'default'})
    ref.set('{%s}id' % R, kind)
sub(sect, 'pgSz', {'w': 11906, 'h': 16838})
sub(sect, 'pgMar', {'top': 1134, 'right': 1134, 'bottom': 1134, 'left': 1134, 'header': 500, 'footer': 500})
styles = el('styles')
defaults = sub(styles, 'docDefaults')
rp = sub(sub(defaults, 'rPrDefault'), 'rPr')
sub(rp, 'rFonts', {'ascii': 'Calibri', 'hAnsi': 'Calibri', 'cs': 'Calibri'})
sub(rp, 'sz', {'val': 22})
sub(rp, 'lang', {'val': 'uk-UA'})
for name, size, color, bold, after in [
 ('Normal',22,'263445',False,130), ('Title',56,'163B57',True,360),
 ('Subtitle',30,'146B8A',False,300), ('Lead',25,'34495E',False,220),
 ('Eyebrow',20,'146B8A',True,420), ('Meta',19,'586B7D',False,180),
 ('Heading1',33,'163B57',True,180), ('Heading2',26,'146B8A',True,130),
 ('Callout',21,'163B57',False,170), ('Code',19,'163B57',False,180),
 ('TableText',20,'263445',False,60), ('TableHeader',20,'FFFFFF',True,60),
 ('ListText',22,'263445',False,100), ('Spacer',8,'263445',False,40),
]:
    st = sub(styles, 'style', {'type':'paragraph', 'styleId':name})
    sub(st, 'name', {'val':name})
    if name != 'Normal':
        sub(st, 'basedOn', {'val':'Normal'})
    pp = sub(st, 'pPr')
    spacing = {'after':after, 'line':280, 'lineRule':'auto'}
    if name.startswith('Heading'):
        spacing['before'] = 200
    sub(pp, 'spacing', spacing)
    sub(pp, 'widowControl')
    if name.startswith('Heading'):
        sub(pp, 'keepNext')
        sub(pp, 'outlineLvl', {'val':int(name[-1])-1})
    if name in ['Code','Callout']:
        sub(pp, 'shd', {'fill':'EEF4F8'})
        sub(pp, 'ind', {'left':160,'right':160})
    rr = sub(st, 'rPr')
    if name == 'Code':
        sub(rr, 'rFonts', {'ascii':'Consolas','hAnsi':'Consolas'})
    sub(rr, 'sz', {'val':size})
    sub(rr, 'color', {'val':color})
    if bold:
        sub(rr, 'b')

header = el('hdr')
para('QA LAB  /  Claude Code → Codex', 'Meta', header)
footer = el('ftr')
p = para('Навчальний посібник  •  ', 'Meta', footer)
field = sub(p, 'fldSimple', {'instr':'PAGE'})
run(field, '1')

content_types = ET.Element('Types', xmlns='http://schemas.openxmlformats.org/package/2006/content-types')
ET.SubElement(content_types, 'Default', Extension='rels', ContentType='application/vnd.openxmlformats-package.relationships+xml')
ET.SubElement(content_types, 'Default', Extension='xml', ContentType='application/xml')
for part, kind in [('document','document.main'),('styles','styles'),('header1','header'),('footer1','footer')]:
    ET.SubElement(content_types, 'Override', PartName='/word/'+part+'.xml', ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.'+kind+'+xml')
root_rels = ET.Element('Relationships', xmlns=PKG)
ET.SubElement(root_rels, 'Relationship', Id='doc', Type=R+'/officeDocument', Target='word/document.xml')
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(OUTPUT, 'w', ZIP_DEFLATED) as z:
    for name, node in [('word/document.xml',doc),('word/styles.xml',styles),('word/header1.xml',header),('word/footer1.xml',footer),('word/_rels/document.xml.rels',rels),('[Content_Types].xml',content_types),('_rels/.rels',root_rels)]:
        z.writestr(name, xml(node))
print(OUTPUT)

# Assert every source line and table cell survives conversion, without Markdown syntax.
plain = ''.join(doc.itertext())
def strip_md(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return text.replace('**','').replace('`','')
checked = 0
for line in source.splitlines():
    if not line.strip() or line.startswith('```'):
        continue
    if line.startswith('|'):
        cells = [c.strip() for c in line.strip('|').split('|')]
        if all(re.fullmatch(r':?-+:?',c) for c in cells):
            continue
    else:
        cells = [re.sub(r'^#{1,3} ', '', line)]
    for value in cells:
        assert strip_md(value) in plain, 'Missing source content: '+value
        checked += 1
print(f'Complete source coverage: {checked} text units verified; {link_number} links.')
