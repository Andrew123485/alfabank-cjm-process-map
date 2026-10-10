import xml.etree.ElementTree as ET

def c(tag, parent, **kwargs):
    el = ET.SubElement(parent, tag)
    for k, v in kwargs.items():
        if v is not None:
            if k == 'parent_id': k = 'parent'
            el.set(k, str(v))
    return el

def g(parent, x, y, w, h):
    c("mxGeometry", parent, x=x, y=y, width=w, height=h, **{"as": "geometry"})

root = ET.Element("mxfile", host="drawio", version="26.0.0")
diagram = c("diagram", root, name="BPMN TO BE v3.0", id="bpmn")
model = c("mxGraphModel", diagram, dx="2000", dy="1200", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="0", pageScale="1", math="0", shadow="0")
mx_root = c("root", model)
c("mxCell", mx_root, id="0")
c("mxCell", mx_root, id="1", parent_id="0")

pool = c("mxCell", mx_root, id="pool", value="Покупка наличной валюты ФЛ (TO BE)", style="swimlane;html=1;childLayout=stackLayout;horizontal=1;startSize=40;horizontalStack=0;resizeParent=1;resizeParentMax=0;collapsible=0;fontStyle=1;fontSize=14;fillColor=#E6E6E6;", vertex="1", parent_id="1")
g(pool, 20, 20, 11000, 2000)

lanes = [
    ("lane1", "Клиент (ФЛ)", 240, "none", "none"),
    ("lane2", "Яндекс / Агрегаторы", 200, "#FFF2CC", "#D6B656"),
    ("lane3", "Сайт alfabank.ru", 300, "#DAE8FC", "#6C8EBF"),
    ("lane4", "Приложение / Чат-бот", 260, "#D5E8D4", "#82B366"),
    ("lane5", "Контакт-центр (IVR / Оператор)", 240, "#FFE6CC", "#D79B00"),
    ("lane6", "Терминал / Помощник зала (Отделение)", 300, "#F5F5F5", "#666666"),
    ("lane7", "Кассир / OPICS (АБС)", 280, "#F8CECC", "#B85450")
]

cy = 40
for lid, name, h, fill, stroke in lanes:
    style = f"swimlane;html=1;startSize=30;horizontal=0;collapsible=0;fontStyle=1;fontSize=11;"
    if fill != "none":
        style += f"fillColor={fill};strokeColor={stroke};"
    else:
        style += "fillColor=none;"
    l = c("mxCell", mx_root, id=lid, value=name, style=style, vertex="1", parent_id="pool")
    g(l, 0, cy, 11000, h)
    cy += h

def node(id, lane, x, y, w, h, value, style_type="task", is_new=False):
    style = ""
    if style_type == "start":
        style = "shape=mxgraph.bpmn.event;html=1;perimeter=ellipsePerimeter;aspect=fixed;outline=standard;symbol=general;verticalLabelPosition=bottom;verticalAlign=top;align=center;fontSize=9;"
    elif style_type == "end":
        style = "shape=mxgraph.bpmn.event;html=1;perimeter=ellipsePerimeter;aspect=fixed;outline=end;symbol=terminate;verticalLabelPosition=bottom;verticalAlign=top;fillColor=#F8CECC;strokeColor=#B85450;fontSize=9;"
    elif style_type == "end_ok":
        style = "shape=mxgraph.bpmn.event;html=1;perimeter=ellipsePerimeter;aspect=fixed;outline=end;symbol=general;verticalLabelPosition=bottom;verticalAlign=top;fillColor=#D5E8D4;strokeColor=#82B366;fontSize=9;"
    elif style_type == "gw":
        style = "shape=mxgraph.bpmn.gateway2;html=1;perimeter=rhombusPerimeter;outline=none;symbol=none;gwType=exclusive;verticalLabelPosition=bottom;verticalAlign=top;align=center;fontSize=9;"
    else:
        style = "shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;taskMarker=abstract;fontSize=9;"
        if is_new:
            style += "fillColor=#D5E8D4;strokeColor=#82B366;fontStyle=1;"
            value = "[НОВОЕ] " + value
            
    n = c("mxCell", mx_root, id=id, value=value, style=style, vertex="1", parent_id=lane)
    g(n, x, y, w, h)

def edge(id, src, tgt, label="", extra_style=""):
    style = f"edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;{extra_style}"
    e = c("mxCell", mx_root, id=id, value=label, style=style, edge="1", parent_id="1", source=src, target=tgt)
    c("mxGeometry", e, relative="1", **{"as": "geometry"})

def phase(id, x, text):
    n = c("mxCell", mx_root, id=id, value=text, style="text;html=1;fontSize=14;fontStyle=1;fontColor=#7F00FF;align=center;verticalAlign=middle;whiteSpace=wrap;", vertex="1", parent_id="lane1")
    g(n, x, 5, 400, 30)

phase("ph1", 200, "ФАЗА 1: Поиск и выбор банка")
phase("ph2", 1500, "ФАЗА 2: Цифровой путь (Подготовка)")
phase("ph3", 4400, "ФАЗА 3: Визит в отделение (Phygital)")
phase("ph4", 6400, "ФАЗА 4: Конвертация (Касса)")

# PHASE 1
node("e_start", "lane1", 50, 100, 50, 50, "Начало", "start")
node("t_1_1", "lane2", 150, 60, 200, 80, "1.1 SEO Landing\n/exchange/new-series-dollars/\nВыдача сразу на Альфу", is_new=True)
node("t_1_2", "lane2", 400, 60, 200, 80, "1.2 Banki.ru\nБейджи: «Новые купюры»\n+ «Проверка наличия онлайн»", is_new=True)
node("g_1", "lane1", 650, 100, 50, 50, "G1\nВыбирает Альфу?", "gw")
node("e_end_comp", "lane1", 655, 20, 40, 40, "Уход к конкуренту", "end")
node("g_2", "lane1", 800, 100, 50, 50, "G2\nКлиент банка?", "gw")
node("g_3", "lane1", 950, 100, 50, 50, "G3\nКакой канал?", "gw")

edge("e1", "e_start", "t_1_1")
edge("e2", "t_1_1", "t_1_2")
edge("e3", "t_1_2", "g_1")
edge("e4", "g_1", "e_end_comp", "Нет", "fontColor=#B85450;fontStyle=1;")
edge("e5", "g_1", "g_2", "Да", "fontColor=#82B366;fontStyle=1;")
edge("e6", "g_2", "g_3") # Да/Нет идут в G3

# PHASE 2 - WEBSITE
node("t_2_1", "lane3", 1100, 30, 200, 80, "2.1 Страница обмена\nОбновлён UX, WCAG 2.1\nNPS виджет, Кнопка чата", is_new=True)
node("g_4", "lane3", 1350, 45, 50, 50, "G4\nИностранец?", "gw")
node("t_2_1_1", "lane3", 1300, 150, 150, 60, "2.1.1 In-place перевод\nбез сброса формы", is_new=True)
node("t_2_2", "lane3", 1500, 30, 200, 80, "2.2 Калькулятор\nКурс синхр 15м, Выбор канала,\nQR-код в приложение", is_new=True)
node("t_2_2_1", "lane3", 1750, 30, 180, 80, "2.2.1 Динамич. контент:\nКарта с кэшбэком /\nPrice Alerts", is_new=True)
node("t_2_2_2", "lane3", 1980, 30, 180, 80, "2.2.2 Блок FAQ\nс фидбеком Да/Нет", is_new=True)

node("g_5", "lane3", 2200, 45, 50, 50, "G5\nВалюта?", "gw")
node("t_2_2_3", "lane3", 2150, 150, 150, 60, "2.2.3 AED корректно\nв калькуляторе", is_new=True)
node("g_6", "lane3", 2350, 45, 50, 50, "G6\nСиние $?", "gw")

node("t_2_3", "lane3", 2480, 30, 200, 80, "2.3 Интерактивная карта\nLive-статусы наличия,\nфильтр «Синие купюры»", is_new=True)
node("g_7", "lane3", 2730, 45, 50, 50, "G7\nЗаявка?", "gw")
node("t_2_3_1", "lane3", 2680, 150, 150, 70, "2.3.1 Обратный звонок\n(SLA 15 мин)", is_new=True)
node("t_2_4", "lane3", 2850, 30, 200, 80, "2.4 Форма «Уточнить наличие»\nЧестный нейминг,\nСумма, Дисклеймер", is_new=True)

# PHASE 2 - APP
node("t_3_1", "lane4", 1100, 30, 200, 80, "3.1 Внутренний поиск\nПрямой переход на валюту", is_new=True)
node("t_3_2", "lane4", 1350, 30, 200, 80, "3.2 Чат-бот\nАктуальная база знаний", is_new=True)
node("g_8", "lane4", 1600, 45, 50, 50, "G8\nСиние $?", "gw")
node("t_3_3", "lane4", 1750, 30, 200, 80, "3.3 Smart Routing\nГеолокация ближайшего ДО\nс синими купюрами", is_new=True)
node("g_9", "lane4", 2000, 45, 50, 50, "G9\nОформляет?", "gw")
node("t_3_4", "lane4", 2200, 30, 220, 80, "3.4 Оформление: защита от руб,\nUpsell, Вызов Такси, Талон", is_new=True)

# PHASE 2 - CALL CENTER
node("t_4_1", "lane5", 1100, 40, 200, 80, "4.1 Контакты\n3 блока: App / 8-800 / +7495", is_new=True)
node("t_4_2", "lane5", 1350, 40, 150, 80, "4.2 Клиент звонит")
node("g_10", "lane5", 1550, 55, 50, 50, "G10\nIVR", "gw")
node("t_4_2_1", "lane5", 1500, 150, 150, 60, "4.2.1 Стандартный IVR")
node("t_4_3", "lane5", 1750, 40, 200, 80, "4.3 Оператор сверяет наличие\nчерез интеграцию с OPICS", is_new=True)
node("t_4_4", "lane5", 2000, 40, 200, 80, "4.4 Оператор формирует Lead ID", is_new=True)

# PHASE 2 - LEAD ID & TRANSITION
node("t_2_5", "lane7", 3200, 50, 220, 80, "2.5 CRM / OPICS: Lead ID\n(MOMH/00142) + Вызов Такси", is_new=True)
node("t_go", "lane1", 3800, 90, 200, 80, "Клиент едет в отделение\n(без брони или с Lead ID)", "task", is_new=False)

# PHASE 3 - BRANCH
node("t_5_1", "lane2", 4100, 60, 200, 80, "5.1 Яндекс.Карты:\nстатус «Валюта в наличии»", is_new=True)
node("g_11", "lane6", 4400, 60, 50, 50, "G11\nЕсть валюта\nв кассе?", "gw")
node("e_end_nobucks", "lane6", 4405, 170, 40, 40, "Терминал блочит,\nКлиент уходит", "end")
node("t_5_2", "lane6", 4550, 45, 200, 80, "5.2 Терминал (Face ID/QR)\nПодтягивает Lead ID,\nТалон К010", is_new=True)
node("g_11_1", "lane6", 4800, 60, 50, 50, "G11.1\n>5000$?", "gw")
node("t_5_4_vip", "lane6", 4750, 170, 150, 70, "5.4 Alfa Only\nПремиальная зона", is_new=True)
node("t_5_3", "lane6", 4950, 45, 200, 80, "5.3 Умная маршрутизация:\nFast-track для кассы", is_new=True)
node("t_5_4", "lane6", 5200, 45, 220, 80, "5.4 Ожидание: ТВ 2 зоны,\nКрупный курс, Анонимность", is_new=True)
node("t_5_5", "lane6", 5480, 45, 220, 80, "5.5 Кросс-сейл Альфа-Тревел,\n>10м: Push-извинение + Кофе", is_new=True)
node("g_12", "lane6", 5780, 60, 50, 50, "G12\nЗависло табло?", "gw")
node("t_5_5_1", "lane6", 5730, 170, 150, 70, "5.5.1 Помощник зала\nпроактивно приглашает", is_new=True)

# PHASE 4 - CONVERSION
node("t_6_1", "lane7", 6100, 50, 200, 80, "6.1 Кассовая кабина:\nПолочка для сумок", is_new=True)
node("t_6_2", "lane7", 6350, 50, 200, 80, "6.2 Кассир видит Lead ID\n(без вопросов про сумму)", is_new=True)
node("g_13", "lane7", 6650, 65, 50, 50, "G13\n>= 40к ₽?", "gw")
node("t_6_3", "lane7", 6600, 170, 150, 60, "6.3 Предъявление паспорта\n(115-ФЗ)")
node("t_6_4", "lane7", 6800, 50, 200, 80, "6.4 Пересчёт купюр\nна счетчике на виду")
node("t_6_5", "lane7", 7050, 50, 200, 80, "6.5 Выдача валюты:\nБрендированный конверт,\n0 скрытых комиссий", is_new=True)
node("t_6_6", "lane7", 7300, 50, 200, 80, "6.6 Фиксация в OPICS\n(Списание остатков)")
node("e_end_success", "lane1", 7600, 105, 50, 50, "Успех\nNPS Push", "end_ok")


# EDGE ROUTING
# Phase 1
edge("e7", "g_3", "t_2_1", "Сайт")
edge("e8", "g_3", "t_3_1", "Приложение")
edge("e9", "g_3", "t_4_1", "Звонок")
edge("e10", "g_3", "t_5_1", "Карта")
edge("e11", "g_3", "t_go", "Визит")

# Website
edge("w1", "t_2_1", "g_4")
edge("w2", "g_4", "t_2_1_1", "Да")
edge("w3", "g_4", "t_2_2", "Нет")
edge("w4", "t_2_1_1", "t_2_2")
edge("w5", "t_2_2", "t_2_2_1")
edge("w6", "t_2_2_1", "t_2_2_2")
edge("w7", "t_2_2_2", "g_5")
edge("w8", "g_5", "t_2_2_3", "AED")
edge("w9", "g_5", "g_6", "USD/EUR/CNY")
edge("w10", "t_2_2_3", "g_6")
edge("w11", "g_6", "t_2_3")
edge("w12", "t_2_3", "g_7")
edge("w13", "g_7", "t_2_3_1", "Крупная сумма")
edge("w14", "g_7", "t_2_4", "Да (стандарт)")
edge("w15", "g_7", "t_go", "Нет (Едет)")
edge("w16", "t_2_3_1", "t_4_3") # Call center SLA
edge("w17", "t_2_4", "t_2_5")

# App
edge("a1", "t_3_1", "t_3_2")
edge("a2", "t_3_2", "g_8")
edge("a3", "g_8", "t_3_3", "Да")
edge("a4", "g_8", "g_9", "Нет")
edge("a5", "t_3_3", "g_9")
edge("a6", "g_9", "t_3_4", "Да")
edge("a7", "g_9", "t_go", "Нет")
edge("a8", "t_3_4", "t_2_5")

# Call Center
edge("c1", "t_4_1", "t_4_2")
edge("c2", "t_4_2", "g_10")
edge("c3", "g_10", "t_4_3", "Оператор")
edge("c4", "g_10", "t_4_2_1", "Иное")
edge("c5", "t_4_2_1", "t_4_3")
edge("c6", "t_4_3", "t_4_4")
edge("c7", "t_4_4", "t_2_5")

# Common to Visit
edge("cm1", "t_2_5", "t_go")
edge("cm2", "t_go", "t_5_1")

# Visit
edge("v1", "t_5_1", "g_11")
edge("v2", "g_11", "e_end_nobucks", "Нет", "fontColor=#B85450;fontStyle=1;")
edge("v3", "g_11", "t_5_2", "Да", "fontColor=#82B366;fontStyle=1;")
edge("v4", "t_5_2", "g_11_1")
edge("v5", "g_11_1", "t_5_4_vip", "Да (VIP)")
edge("v6", "g_11_1", "t_5_3", "Нет")
edge("v7", "t_5_3", "t_5_4")
edge("v8", "t_5_4_vip", "t_5_4")
edge("v9", "t_5_4", "t_5_5")
edge("v10", "t_5_5", "g_12")
edge("v11", "g_12", "t_5_5_1", "Да")
edge("v12", "g_12", "t_6_1", "Нет (Push ОК)")
edge("v13", "t_5_5_1", "t_6_1")

# Cashier
edge("ca1", "t_6_1", "t_6_2")
edge("ca2", "t_6_2", "g_13")
edge("ca3", "g_13", "t_6_3", "Да")
edge("ca4", "g_13", "t_6_4", "Нет")
edge("ca5", "t_6_3", "t_6_4")
edge("ca6", "t_6_4", "t_6_5")
edge("ca7", "t_6_5", "t_6_6")
edge("ca8", "t_6_6", "e_end_success")

tree = ET.ElementTree(root)
ET.indent(tree, space="  ")
tree.write("bpmn_to_be.drawio", encoding="utf-8", xml_declaration=True)
print("done")
