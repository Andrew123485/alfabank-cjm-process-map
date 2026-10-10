from dotenv import load_dotenv
load_dotenv()
import requests
import json
import time
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = os.getenv('MIRO_TOKEN', 'YOUR_MIRO_TOKEN')
BOARD_ID = os.getenv('MIRO_BOARD_ID', 'YOUR_BOARD_ID')
HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {TOKEN}'
}
IMAGE_DIR = r'C:\Users\Андрей\.gemini\antigravity\playground\Изучение новых тем для альфы\Miro_Screenshots'

def create_shape(content, x, y, width, height, bg_color, border_color="#ffffff", shape="rectangle", font_color="#000000", text_align="center", text_valign="middle", font_size="14", border_width="1.0", border_style="normal"):
    url = f'https://api.miro.com/v2/boards/{BOARD_ID}/shapes'
    payload = {
        'data': {'content': content, 'shape': shape},
        'style': {
            'fillColor': bg_color,
            'borderColor': border_color,
            'color': font_color,
            'textAlign': text_align,
            'textAlignVertical': text_valign,
            'fontSize': font_size,
            'borderWidth': border_width,
            'borderStyle': border_style
        },
        'position': {'x': x, 'y': y},
        'geometry': {'width': width, 'height': height}
    }
    if border_color == "transparent":
        payload['style']['borderOpacity'] = "0.0"
        payload['style']['borderColor'] = "#ffffff"
    if bg_color == "transparent":
        payload['style']['fillOpacity'] = "0.0"
        payload['style']['fillColor'] = "#ffffff"

    res = requests.post(url, headers=HEADERS, json=payload)
    if res.status_code != 201:
        print(f"Failed shape: {res.text}")
    return res.json()

def create_sticky(content, x, y, color, width=200):
    url = f'https://api.miro.com/v2/boards/{BOARD_ID}/sticky_notes'
    payload = {
        'data': {'content': content, 'shape': 'rectangle'},
        'style': {'fillColor': color, 'textAlign': 'left', 'textAlignVertical': 'top'},
        'position': {'x': x, 'y': y},
        'geometry': {'width': width}
    }
    res = requests.post(url, headers=HEADERS, json=payload)
    if res.status_code != 201:
        print(f"Failed sticky: {res.text}")
    return res.json()

def create_connector(start_id, end_id, color="#000000", style="dashed"):
    url = f'https://api.miro.com/v2/boards/{BOARD_ID}/connectors'
    payload = {
        'startItem': {'id': str(start_id), 'snapTo': 'right'},
        'endItem': {'id': str(end_id), 'snapTo': 'left'},
        'style': {
            'strokeColor': color, 
            'strokeWidth': '2.0', 
            'strokeStyle': style, 
            'startStrokeCap': 'none', 
            'endStrokeCap': 'arrow'
        }
    }
    res = requests.post(url, headers=HEADERS, json=payload)
    return res.json()

def upload_image(filename, x, y, width=200):
    filepath = os.path.join(IMAGE_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Image not found: {filepath}")
        return None
    url = f'https://api.miro.com/v2/boards/{BOARD_ID}/images'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    with open(filepath, 'rb') as f:
        files = {'resource': (filename, f, 'image/png')}
        data = {
            'position': json.dumps({'x': x, 'y': y}),
            'geometry': json.dumps({'width': width})
        }
        res = requests.post(url, headers=headers, files=files, data=data)
    if res.status_code != 201:
        print(f"Failed image {filename}: {res.text}")
    return res.json()

with open('full_cjm_data.json', 'r', encoding='utf-8') as f:
    steps = json.load(f)

# Layout parameters
START_X = 82000
START_Y = 0

COL_WIDTH = 360
GAP_X = 20
GAP_Y = 20
STICKY_WIDTH = 340
STICKY_Y_STEP = 220
ROW_HEADER_WIDTH = 250

RED_COLOR = "#f24726" 

max_exp = max([len(s.get('pos', [])) + len(s.get('neg', [])) for s in steps])
max_ideas = max([len(s.get('ideas', [])) for s in steps])
max_imgs = max([len(s.get('images', [])) for s in steps])

row_heights = {
    "action": 250,
    "touchpoint": 180,
    "goal": 180,
    "emotion": 300,
    "importance": 180,
    "experience": max(800, max_exp * STICKY_Y_STEP + 200), 
    "ideas": max(800, max_ideas * STICKY_Y_STEP + 200),
    "images": max(300, max_imgs * 400 + 200)
}

row_y = {}
current_y = START_Y
for key, h in row_heights.items():
    row_y[key] = current_y + h/2
    current_y += h

def create_row_header(text, y_key, is_split=False):
    y_center = row_y[y_key]
    height = row_heights[y_key]
    create_shape("", START_X, y_center, ROW_HEADER_WIDTH, height, bg_color=RED_COLOR, border_color="#ffffff", border_width="1.0")
    
    if is_split:
        create_shape(f"<p><strong>{text}</strong></p>", START_X - 35, y_center, 150, height, bg_color="transparent", border_color="transparent", font_color="#ffffff", font_size="14", text_align="center")
    else:
        create_shape(f"<p><strong>{text}</strong></p>", START_X, y_center, ROW_HEADER_WIDTH, height, bg_color="transparent", border_color="transparent", font_color="#ffffff", font_size="14", text_align="center")

# 1. Create GIANT white background frame
bg_width = ROW_HEADER_WIDTH + COL_WIDTH * len(steps) + 100
bg_height = sum(row_heights.values()) + 1200 # Space for images
bg_x = START_X - ROW_HEADER_WIDTH / 2 + bg_width / 2 - 50
bg_y = START_Y + sum(row_heights.values()) / 2 + 300
print(f"Creating background {bg_width}x{bg_height} at {bg_x}, {bg_y}...")
create_shape("", bg_x, bg_y, bg_width, bg_height, bg_color="#f9fafb", border_color="#d1d5db", border_width="2.0")
time.sleep(1)

# 2. Draw horizontal grid lines
content_width = COL_WIDTH * len(steps) + 100
content_x = START_X + (ROW_HEADER_WIDTH / 2) + (content_width / 2) - 50

for key, h in row_heights.items():
    top_y = row_y[key] - h/2
    if top_y != START_Y:
        create_shape("", content_x, top_y, content_width, 8, bg_color="#e5e7eb", border_color="transparent")

# 3. Create Stage Headers
stages = []
current_stage_title = None
current_stage_start_col = 0
current_stage_steps = 0
for i, step in enumerate(steps):
    if step["stage_title"] != current_stage_title:
        if current_stage_title is not None:
            stages.append({"title": current_stage_title, "start": current_stage_start_col, "count": current_stage_steps})
        current_stage_title = step["stage_title"]
        current_stage_start_col = i
        current_stage_steps = 1
    else:
        current_stage_steps += 1
if current_stage_title is not None:
    stages.append({"title": current_stage_title, "start": current_stage_start_col, "count": current_stage_steps})

for i, stage in enumerate(stages):
    if i == 0:
        stage_w = ROW_HEADER_WIDTH + COL_WIDTH * stage["count"]
        stage_x = START_X + (stage_w / 2) - (ROW_HEADER_WIDTH / 2)
    else:
        stage_w = COL_WIDTH * stage["count"]
        stage_x = START_X + ROW_HEADER_WIDTH/2 + (stage["start"] * COL_WIDTH) + (stage_w / 2)
    create_shape(f"<p><strong>{stage['title']}</strong></p>", stage_x, START_Y - 40, stage_w, 80, bg_color=RED_COLOR, border_color="#ffffff", border_width="1.0", font_color="#ffffff", font_size="16")

# 4. Create Row Headers
create_row_header("ДЕЙСТВИЯ<br>КЛИЕНТА", "action")
create_row_header("ТОЧКИ<br>КОНТАКТА", "touchpoint")
create_row_header("ЦЕЛИ И<br>ОЖИДАНИЯ", "goal")

create_row_header("ЭМОЦИИ", "emotion", is_split=True)
em_labels = [("Отлично 😀", 5), ("Хорошо 🙂", 4), ("Нормально 😐", 3), ("Печально 🙁", 2), ("Ужасно 😫", 1)]
em_top_y = row_y["emotion"] - (row_heights["emotion"]/2)
for lbl, val in em_labels:
    sub_y = em_top_y + ((5 - val) * 60) + 30
    create_shape(f"<strong>{lbl}</strong>", START_X + 60, sub_y, 110, 30, bg_color="transparent", border_color="transparent", font_color="#ffffff", text_align="right", font_size="12")

create_row_header("ВАЖНОСТЬ", "importance", is_split=True)
imp_labels = [("Высокая 🔴", 3), ("Средняя 🟡", 2), ("Низкая 🟢", 1)]
imp_top_y = row_y["importance"] - (row_heights["importance"]/2)
for lbl, val in imp_labels:
    sub_y = imp_top_y + ((3 - val) * 60) + 30
    create_shape(f"<strong>{lbl}</strong>", START_X + 60, sub_y, 110, 30, bg_color="transparent", border_color="transparent", font_color="#ffffff", text_align="right", font_size="12")

create_row_header("ОПЫТ КЛИЕНТА", "experience")
create_row_header("РЕКОМЕНДАЦИИ", "ideas")
create_row_header("ИЛЛЮСТРАЦИИ", "images")

# 5. Process Steps
current_x = START_X + (ROW_HEADER_WIDTH / 2) + (COL_WIDTH / 2)
prev_em_id = None
prev_imp_id = None

for i, step in enumerate(steps):
    print(f"Drawing step {i+1}/{len(steps)}: {step['title']}...")
    
    # Clean emojis or formatting if needed
    title = step['title'].replace("**", "")
    
    create_sticky(title, current_x, row_y["action"], color="yellow", width=STICKY_WIDTH)
    create_shape(step['touchpoint'], current_x, row_y["touchpoint"], STICKY_WIDTH, 140, bg_color="#ffffff", border_color="#d1d5db", font_size="14")
    create_shape(step['goal'], current_x, row_y["goal"], STICKY_WIDTH, 140, bg_color="#ffffff", border_color="#d1d5db", font_size="14")
    
    # Emotion Node
    em_top_y = row_y["emotion"] - (row_heights["emotion"]/2)
    em_y = em_top_y + ((5 - step["emotion_val"]) * 60) + 30
    emojis = {5: "😀", 4: "🙂", 3: "😐", 2: "🙁", 1: "😫"}
    node = create_shape(emojis[step["emotion_val"]], current_x, em_y, 36, 36, shape="circle", bg_color="#e5e7eb", border_color="#374151", border_width="2.0", font_size="18")
    if node and 'id' in node:
        if prev_em_id:
            create_connector(prev_em_id, node['id'], color="#9ca3af", style="dashed")
        prev_em_id = node['id']
        
    # Importance Node
    imp_top_y = row_y["importance"] - (row_heights["importance"]/2)
    imp_y = imp_top_y + ((3 - step["importance_val"]) * 60) + 30
    imp_colors = {3: "#ef4444", 2: "#facc15", 1: "#22c55e"} 
    node = create_shape("", current_x, imp_y, 24, 24, shape="circle", bg_color=imp_colors.get(step["importance_val"], "#facc15"), border_color="#1f2937", border_width="2.0")
    if node and 'id' in node:
        if prev_imp_id:
            create_connector(prev_imp_id, node['id'], color="#9ca3af", style="dashed")
        prev_imp_id = node['id']

    import re
    def format_text(text):
        # Replace **text** with <strong>text</strong>
        return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

    # Experience
    exp_top_y = row_y["experience"] - (row_heights["experience"]/2)
    cur_y = exp_top_y + (STICKY_Y_STEP / 2) + 10
    for pos_txt in step.get("pos", []):
        create_sticky(format_text(pos_txt), current_x, cur_y, color="light_green", width=STICKY_WIDTH)
        cur_y += STICKY_Y_STEP
    for neg_txt in step.get("neg", []):
        create_sticky(format_text(neg_txt), current_x, cur_y, color="pink", width=STICKY_WIDTH)
        cur_y += STICKY_Y_STEP
        
    # Ideas
    idea_top_y = row_y["ideas"] - (row_heights["ideas"]/2)
    cur_y = idea_top_y + (STICKY_Y_STEP / 2) + 10
    for idea_txt in step.get("ideas", []):
        create_sticky(format_text(idea_txt), current_x, cur_y, color="light_blue", width=STICKY_WIDTH)
        cur_y += STICKY_Y_STEP

    # Images
    img_top_y = row_y["images"] - (row_heights["images"]/2)
    cur_y = img_top_y + 150
    for img in step.get("images", []):
        res = upload_image(img, current_x, cur_y, width=STICKY_WIDTH)
        if res and 'geometry' in res:
            cur_y += res['geometry'].get('height', 300) + GAP_Y
            
    current_x += COL_WIDTH
    time.sleep(0.5)

print("Full 5-stage CJM with white background frame generated successfully!")
