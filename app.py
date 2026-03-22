"""
Guild Quest — RPG Task Manager
Supabase 永続化対応版

必要ライブラリ:
pip install streamlit supabase python-dotenv

.env (または Streamlit Secrets) に以下を設定:
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=your-anon-key
"""

import streamlit as st
import random
import os
import uuid
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# ─── ページ設定 ────────────────────────────────────────────

st.set_page_config(
    page_title="Guild Quest — RPG Task Manager",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Supabase クライアント ─────────────────────────────────

@st.cache_resource
def get_supabase() -> Client:
    url = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", ""))
    key = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY", ""))
    if not url or not key:
        st.error("⚠️ SUPABASE_URL と SUPABASE_KEY を設定してください（.env または Streamlit Secrets）")
        st.stop()
    return create_client(url, key)

supabase = get_supabase()

# ─── DB ヘルパー ───────────────────────────────────────────

def db_load_tasks() -> list:
    res = supabase.table("tasks").select("*").order("created_at", desc=True).execute()
    return res.data or []

def db_load_monsters() -> list:
    res = supabase.table("monsters").select("*").order("captured_at", desc=True).execute()
    return res.data or []

def db_insert_task(task: dict) -> dict:
    res = supabase.table("tasks").insert(task).execute()
    return res.data[0] if res.data else task

def db_insert_monster(monster: dict) -> dict:
    res = supabase.table("monsters").insert(monster).execute()
    return res.data[0] if res.data else monster

def db_mark_task_done(task_id: str):
    supabase.table("tasks").update({"done": True}).eq("id", task_id).execute()

def db_mark_monster_defeated(monster_id: str):
    supabase.table("monsters").update({"defeated": True}).eq("id", monster_id).execute()

def db_set_party(monster_id: str, in_party: bool):
    supabase.table("monsters").update({"in_party": in_party}).eq("id", monster_id).execute()

# ─── グローバルCSS ─────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=IM+Fell+English:ital@0;1&display=swap');

:root {
    --gold:#c9a84c; --gold2:#f0d070; --dark:#0d0a06;
    --border:#5a3e10; --text:#e8d5a3; --dim:#8a7355;
}
html,body,[data-testid="stAppViewContainer"] {
    background:var(--dark) !important; color:var(--text) !important;
    font-family:'IM Fell English',serif !important;
}
h1,h2,h3 { font-family:'Cinzel',serif !important; color:var(--gold) !important;
    text-shadow:0 0 20px rgba(201,168,76,0.4); letter-spacing:2px; }
[data-testid="stSidebar"] { background:#0a0806 !important; border-right:2px solid var(--border) !important; }
.stButton>button {
    background:linear-gradient(180deg,#2a1a08,#1a0f04) !important;
    border:2px solid var(--gold) !important; color:var(--gold2) !important;
    font-family:'Cinzel',serif !important; font-weight:700 !important;
    letter-spacing:2px !important; transition:all 0.2s !important; border-radius:3px !important;
}
.stButton>button:hover { background:linear-gradient(180deg,#3d2710,#2a1a08) !important;
    box-shadow:0 0 15px rgba(201,168,76,0.5) !important; transform:translateY(-1px) !important; }
.stTextInput>div>div>input,.stNumberInput>div>div>input,.stSelectbox>div>div {
    background:#120e07 !important; border:1px solid var(--border) !important;
    color:var(--text) !important; border-radius:3px !important; }
.stTabs [data-baseweb="tab-list"] { background:transparent !important; border-bottom:2px solid var(--border) !important; }
.stTabs [data-baseweb="tab"] { background:transparent !important; color:var(--dim) !important;
    font-family:'Cinzel',serif !important; font-size:13px !important; }
.stTabs [aria-selected="true"] { color:var(--gold) !important; border-bottom:2px solid var(--gold) !important; }
::-webkit-scrollbar{width:6px} ::-webkit-scrollbar-track{background:var(--dark)}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
.parchment {
    background:linear-gradient(135deg,#1c1409 0%,#120e07 50%,#1a1208 100%);
    border:2px solid var(--border); border-radius:4px; padding:20px; margin:10px 0;
    box-shadow:inset 0 0 30px rgba(0,0,0,0.5),0 4px 15px rgba(0,0,0,0.8); position:relative;
}
.parchment::before { content:''; position:absolute; top:4px;left:4px;right:4px;bottom:4px;
    border:1px solid rgba(201,168,76,0.15); border-radius:2px; pointer-events:none; }
.hp-bar-wrap { background:#1a0a0a; border:1px solid #5a1a1a; border-radius:3px; height:18px; margin:4px 0; overflow:hidden; }
.hp-bar { height:100%; background:linear-gradient(90deg,#8b0000,#e74c3c); border-radius:3px; transition:width 0.5s; }
.stat-bar-wrap { background:#0a0a1a; border:1px solid #1a1a5a; border-radius:3px; height:12px; margin:2px 0; overflow:hidden; }
.agi-bar { height:100%; background:linear-gradient(90deg,#1a3a8a,#2471a3); border-radius:3px; }
.sta-bar { height:100%; background:linear-gradient(90deg,#1a5a2a,#27ae60); border-radius:3px; }
.monster-card {
    background:linear-gradient(160deg,#150f08,#0d0a06); border:1px solid var(--border);
    border-radius:4px; padding:12px; text-align:center; transition:all 0.2s; overflow:hidden;
}
.monster-card:hover { border-color:var(--gold); box-shadow:0 0 20px rgba(201,168,76,0.2); transform:translateY(-2px); }
.monster-sprite { font-size:52px; display:block; filter:drop-shadow(0 0 10px rgba(201,168,76,0.4)); }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
.monster-battle { animation:float 2s ease-in-out infinite; font-size:80px; display:block; text-align:center; }
.victory-banner {
    background:linear-gradient(135deg,#1a1208,#2a1c08); border:2px solid var(--gold);
    border-radius:4px; padding:24px; text-align:center; box-shadow:0 0 40px rgba(201,168,76,0.3);
}
.tag { display:inline-block; padding:2px 10px; border-radius:2px; font-size:11px;
    font-family:'Cinzel',serif; margin:2px; border:1px solid; }
.tag-short{background:#1a0a0a;border-color:#8b2222;color:#e07070}
.tag-long {background:#0a1a0a;border-color:#226622;color:#70e070}
.tag-burst{background:#1a1a0a;border-color:#666622;color:#e0e070}
.tag-grind{background:#0a0a1a;border-color:#222266;color:#7070e0}
.db-badge { display:inline-block;padding:2px 8px;background:#0a1a0a;border:1px solid #226622;
    border-radius:2px;color:#70e070;font-size:10px;font-family:'Cinzel',serif; }
</style>
""", unsafe_allow_html=True)

# ─── モンスター生成 ────────────────────────────────────────

MONSTER_TABLE = [
    {"name": "ゴブリン・スプリンター", "emoji": "👺", "rarity": "C", "color": "#27ae60"},
    {"name": "スライム",               "emoji": "🟢", "rarity": "C", "color": "#2ecc71"},
    {"name": "コボルト",               "emoji": "🦊", "rarity": "C", "color": "#e67e22"},
    {"name": "スケルトン",             "emoji": "💀", "rarity": "B", "color": "#95a5a6"},
    {"name": "オーク・バーサーカー",   "emoji": "👹", "rarity": "B", "color": "#e74c3c"},
    {"name": "ウィスプ",               "emoji": "🔮", "rarity": "B", "color": "#9b59b6"},
    {"name": "ストーンゴーレム",       "emoji": "🗿", "rarity": "A", "color": "#7f8c8d"},
    {"name": "ドラゴンライダー",       "emoji": "🐉", "rarity": "A", "color": "#e74c3c"},
    {"name": "フェニックス",           "emoji": "🦅", "rarity": "S", "color": "#f39c12"},
    {"name": "シャドウロード",         "emoji": "👁️", "rarity": "S", "color": "#8e44ad"},
]
RARITY_COLOR = {"C": "#95a5a6", "B": "#27ae60", "A": "#2471a3", "S": "#c9a84c"}
TAG_MAP = {
    "ShortDistance": ("tag-short", "短距離"),
    "LongDistance":  ("tag-long",  "長距離"),
    "Burst":         ("tag-burst", "バースト"),
    "Grind":         ("tag-grind", "グラインド"),
    "Balanced":      ("tag-long",  "バランス"),
    "Endurance":     ("tag-grind", "持久"),
}


def generate_monster_data(task_name: str, minutes: int) -> dict:
    seed = sum(ord(c) for c in task_name) + minutes
    random.seed(seed)
    if minutes <= 15:
        pool = [m for m in MONSTER_TABLE if m["rarity"] == "C"]
        agility, stamina = 70 + random.randint(0, 20), 30 + random.randint(0, 10)
        tags = ["ShortDistance", "Burst"]
    elif minutes <= 45:
        pool = [m for m in MONSTER_TABLE if m["rarity"] in ("C", "B")]
        agility, stamina = 50 + random.randint(-10, 10), 50 + random.randint(-10, 10)
        tags = ["Balanced"]
    elif minutes <= 90:
        pool = [m for m in MONSTER_TABLE if m["rarity"] in ("B", "A")]
        agility, stamina = 30 + random.randint(0, 10), 70 + random.randint(0, 20)
        tags = ["LongDistance", "Grind"]
    else:
        pool = [m for m in MONSTER_TABLE if m["rarity"] in ("A", "S")]
        agility, stamina = 40 + random.randint(-5, 5), 80 + random.randint(0, 20)
        tags = ["LongDistance", "Endurance", "Grind"]
    base = random.choice(pool)
    return {
        "id":        str(uuid.uuid4()),
        "name":      base["name"],    "emoji":   base["emoji"],
        "rarity":    base["rarity"],  "color":   base["color"],
        "task_name": task_name,       "minutes": minutes,
        "agility":   min(agility, 99), "stamina": min(stamina, 99),
        "tags":      tags,
        "max_hp":    50 + minutes * 2 + random.randint(0, 30),
        "defeated":  False,           "in_party": False,
    }


def tag_html(tags):
    return "".join(
        f'<span class="tag {TAG_MAP.get(t, ("tag-short", t))[0]}">{TAG_MAP.get(t, (t, t))[1]}</span>'
        for t in (tags or [])
    )


def hp_bar(current, max_hp):
    pct = max(0, int(current / max_hp * 100))
    return (
        f'<div class="hp-bar-wrap"><div class="hp-bar" style="width:{pct}%;"></div></div>'
        f'<small style="color:var(--dim);">HP: {current} / {max_hp}</small>'
    )


def stat_bar(val, cls, label):
    return (
        f'<div style="display:flex;align-items:center;gap:8px;margin:2px 0;">'
        f'<span style="color:var(--dim);font-size:11px;width:60px;">{label}</span>'
        f'<div class="stat-bar-wrap" style="flex:1;"><div class="{cls}" style="width:{val}%;"></div></div>'
        f'<span style="color:var(--text);font-size:11px;width:24px;text-align:right;">{val}</span></div>'
    )

# ─── セッション初期化 ─────────────────────────────────────

for k, v in {
    "battle_monster_id": None, "battle_task_id": None,
    "battle_hp": 0, "battle_log": [], "battle_phase": "idle",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── DB データロード（30秒キャッシュ） ───────────────────

@st.cache_data(ttl=30)
def load_all_data():
    return db_load_tasks(), db_load_monsters()


def invalidate_cache():
    load_all_data.clear()


tasks, monsters = load_all_data()
pending_tasks = [t for t in tasks    if not t["done"]]
defeated_mons = [m for m in monsters if m["defeated"]]
party_mons    = [m for m in monsters if m["in_party"]]

# ─── サイドバー ───────────────────────────────────────────

with st.sidebar:
    st.markdown('<h2 style="font-size:18px;">⚔️ GUILD QUEST</h2>', unsafe_allow_html=True)
    st.markdown('<span class="db-badge">🗄️ Supabase 接続中</span>', unsafe_allow_html=True)
    st.markdown('<hr style="border-color:var(--border);">', unsafe_allow_html=True)
    st.markdown('<p style="color:var(--dim);font-family:Cinzel,serif;font-size:11px;letter-spacing:2px;">— PARTY —</p>', unsafe_allow_html=True)

    if party_mons:
        for m in party_mons[:3]:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:4px 0;padding:6px;
                background:#120e07;border:1px solid var(--border);border-radius:3px;">
                <span style="font-size:24px;">{m['emoji']}</span>
                <div>
                    <div style="color:var(--gold2);font-size:12px;font-family:Cinzel,serif;">{m['name']}</div>
                    <div style="color:{RARITY_COLOR[m['rarity']]};font-size:10px;">★{m['rarity']} — {m['minutes']}分</div>
                </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:var(--dim);font-size:12px;text-align:center;padding:10px 0;">パーティは空です</p>', unsafe_allow_html=True)

    st.markdown('<hr style="border-color:var(--border);">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("討伐数", len(defeated_mons))
    c2.metric("図鑑", f"{len(defeated_mons)}体")
    if st.button("🔄 データ更新", use_container_width=True):
        invalidate_cache()
        st.rerun()

# ─── メインタブ ───────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs(["📜 依頼書", "⚔️ バトル", "📚 図鑑", "🎮 パーティ"])

# ══════════════════════════════════════════════
# TAB 1 — ギルドの依頼書
# ══════════════════════════════════════════════

with tab1:
    st.markdown("""
    <div class="parchment" style="max-width:600px;margin:0 auto;">
        <div style="font-size:40px;text-align:center;filter:drop-shadow(0 0 8px rgba(201,168,76,0.6));">🏰</div>
        <div style="font-family:'Cinzel',serif;color:var(--gold);font-size:22px;text-align:center;
            letter-spacing:4px;border-bottom:1px solid var(--border);padding-bottom:10px;margin-bottom:16px;">
            ギルドの依頼書</div>
        <p style="text-align:center;color:var(--dim);font-style:italic;font-size:13px;">
            依頼を受理すると、対応するモンスターが出現する。</p>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        task_name = st.text_input("📋 依頼内容（タスク名）", placeholder="例: 企画書を書く")
    with col2:
        task_minutes = st.number_input("⏱ 予定時間（分）", min_value=5, max_value=480, value=30, step=5)

    ca, cb = st.columns(2)
    with ca:
        priority = st.selectbox("優先度", ["🔴 緊急", "🟡 通常", "🟢 余裕"])
    with cb:
        category = st.selectbox("カテゴリ", ["💼 仕事", "📚 勉強", "🏃 運動", "🏠 家事", "🎯 趣味"])

    if st.button("⚔️ 依頼を受理してモンスターを召喚", use_container_width=True):
        if task_name.strip():
            with st.spinner("モンスターを召喚中…"):
                mdata = generate_monster_data(task_name.strip(), task_minutes)
                saved = db_insert_monster(mdata)
                monster_id = saved.get("id", mdata["id"])
                db_insert_task({
                    "name": task_name.strip(), "minutes": task_minutes,
                    "priority": priority, "category": category,
                    "monster_id": monster_id, "done": False,
                })
                invalidate_cache()
            st.success(f"✨ {mdata['name']} が出現した！（Supabaseに保存済み）")
            st.markdown(f"""
            <div class="parchment" style="max-width:400px;margin:10px auto;text-align:center;">
                <span style="font-size:72px;display:block;filter:drop-shadow(0 0 15px {mdata['color']});">{mdata['emoji']}</span>
                <div style="color:var(--gold);font-family:Cinzel,serif;font-size:18px;margin:8px 0;">{mdata['name']}</div>
                <div style="color:{RARITY_COLOR[mdata['rarity']]};font-family:Cinzel,serif;margin-bottom:12px;">★ {mdata['rarity']}</div>
                {stat_bar(mdata['agility'], 'agi-bar', '⚡ AGI')}
                {stat_bar(mdata['stamina'], 'sta-bar', '💪 STA')}
                <div style="margin-top:10px;">{tag_html(mdata['tags'])}</div>
            </div>""", unsafe_allow_html=True)
            st.rerun()
        else:
            st.warning("依頼内容を入力してください。")

    st.markdown('<hr style="border-color:var(--border);margin:20px 0;">', unsafe_allow_html=True)
    st.markdown("### 📋 受理中の依頼")

    if not pending_tasks:
        st.markdown('<p style="color:var(--dim);text-align:center;padding:20px;">受理中の依頼はない。</p>', unsafe_allow_html=True)
    else:
        for task in pending_tasks:
            monster = next((m for m in monsters if str(m["id"]) == str(task.get("monster_id", ""))), None)
            if not monster:
                continue
            cm, ct, cb2 = st.columns([1, 4, 1])
            with cm:
                st.markdown(f'<span style="font-size:36px;">{monster["emoji"]}</span>', unsafe_allow_html=True)
            with ct:
                st.markdown(f"""
                <div style="padding:6px 0;">
                    <div style="color:var(--gold2);font-family:Cinzel,serif;font-size:14px;">{task['name']}</div>
                    <div style="color:var(--dim);font-size:12px;">{task.get('priority', '—')} | {task.get('category', '—')} | ⏱ {task['minutes']}分</div>
                    <div style="color:{RARITY_COLOR[monster['rarity']]};font-size:11px;font-family:Cinzel,serif;">{monster['name']} — ★{monster['rarity']}</div>
                </div>""", unsafe_allow_html=True)
            with cb2:
                if st.button("⚔️", key=f"go_{task['id']}", help="バトル開始"):
                    st.session_state.battle_monster_id = str(monster["id"])
                    st.session_state.battle_task_id    = str(task["id"])
                    st.session_state.battle_hp         = monster["max_hp"]
                    st.session_state.battle_log        = []
                    st.session_state.battle_phase      = "fighting"
                    st.rerun()
            st.markdown('<hr style="border-color:#1a1408;margin:4px 0;">', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 2 — バトル
# ══════════════════════════════════════════════

with tab2:
    if st.session_state.battle_phase == "idle" or not st.session_state.battle_monster_id:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:var(--dim);">
            <div style="font-size:64px;margin-bottom:20px;">🗡️</div>
            <div style="font-family:Cinzel,serif;font-size:16px;color:var(--gold);margin-bottom:8px;">戦場は静まり返っている</div>
            <div style="font-size:13px;">「依頼書」タブでモンスターを召喚してバトルを開始せよ。</div>
        </div>""", unsafe_allow_html=True)
    else:
        monster = next((m for m in monsters if str(m["id"]) == st.session_state.battle_monster_id), None)
        if not monster:
            st.warning("モンスターが見つかりません。")
        else:
            current_hp = st.session_state.battle_hp
            max_hp     = monster["max_hp"]
            tags       = monster.get("tags") or []

            if st.session_state.battle_phase == "fighting":
                cm2, ci = st.columns([1, 1])
                with cm2:
                    st.markdown(f"""
                    <div class="parchment" style="text-align:center;padding:30px;">
                        <div style="color:var(--gold);font-family:Cinzel,serif;font-size:13px;letter-spacing:3px;margin-bottom:16px;">— ENEMY —</div>
                        <span class="monster-battle">{monster['emoji']}</span>
                        <div style="color:var(--gold2);font-family:Cinzel,serif;font-size:18px;margin:12px 0;">{monster['name']}</div>
                        <div style="color:{RARITY_COLOR[monster['rarity']]};font-family:Cinzel,serif;font-size:12px;margin-bottom:12px;">★ {monster['rarity']}</div>
                        {hp_bar(current_hp, max_hp)}
                    </div>""", unsafe_allow_html=True)
                with ci:
                    st.markdown(f"""
                    <div class="parchment">
                        <div style="color:var(--gold);font-family:Cinzel,serif;font-size:13px;letter-spacing:2px;margin-bottom:12px;">📋 依頼内容</div>
                        <div style="color:var(--text);font-size:15px;margin-bottom:8px;">{monster['task_name']}</div>
                        <div style="color:var(--dim);font-size:12px;margin-bottom:16px;">⏱ {monster['minutes']}分</div>
                        <div style="color:var(--gold);font-family:Cinzel,serif;font-size:11px;margin-bottom:8px;letter-spacing:2px;">CHEMISTRY</div>
                        {tag_html(tags)}
                        <hr style="border-color:var(--border);margin:12px 0;">
                        {stat_bar(monster['agility'], 'agi-bar', '⚡ AGI')}
                        {stat_bar(monster['stamina'], 'sta-bar', '💪 STA')}
                    </div>""", unsafe_allow_html=True)

                st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
                ba, bb, bc = st.columns(3)
                with ba:
                    if st.button("⚔️ 通常攻撃", use_container_width=True):
                        dmg = random.randint(8, 18) + monster["agility"] // 10
                        st.session_state.battle_hp = max(0, current_hp - dmg)
                        st.session_state.battle_log.append(f"⚔️ {dmg} ダメージ！")
                        if st.session_state.battle_hp <= 0:
                            st.session_state.battle_phase = "victory"
                        st.rerun()
                with bb:
                    if st.button("🔥 必殺技", use_container_width=True):
                        dmg = random.randint(25, 45) + monster["stamina"] // 5
                        st.session_state.battle_hp = max(0, current_hp - dmg)
                        st.session_state.battle_log.append(f"🔥 必殺！ {dmg} ダメージ！！")
                        if st.session_state.battle_hp <= 0:
                            st.session_state.battle_phase = "victory"
                        st.rerun()
                with bc:
                    if st.button("🏳️ 撤退", use_container_width=True):
                        st.session_state.battle_monster_id = None
                        st.session_state.battle_phase = "idle"
                        st.rerun()

                if st.session_state.battle_log:
                    log_html = "".join(
                        f'<div style="color:var(--dim);font-size:12px;padding:2px 0;border-bottom:1px solid #1a1408;">{e}</div>'
                        for e in reversed(st.session_state.battle_log[-5:])
                    )
                    st.markdown(f'<div class="parchment" style="max-height:120px;overflow:auto;">{log_html}</div>', unsafe_allow_html=True)

            elif st.session_state.battle_phase == "victory":
                st.markdown(f"""
                <div class="victory-banner">
                    <div style="font-size:72px;margin-bottom:12px;">🏆</div>
                    <div style="font-family:Cinzel,serif;font-size:28px;color:var(--gold);letter-spacing:4px;margin-bottom:8px;">VICTORY!</div>
                    <div style="font-size:15px;color:var(--text);margin-bottom:20px;">
                        <strong style="color:var(--gold2);">{monster['name']}</strong> を討伐した！
                    </div>
                    <div style="font-size:60px;margin:10px 0;filter:drop-shadow(0 0 20px {monster['color']});">{monster['emoji']}</div>
                </div>""", unsafe_allow_html=True)

                cx, cy = st.columns(2)
                with cx:
                    if st.button("✨ パーティに加える", use_container_width=True):
                        if len(party_mons) < 3:
                            db_mark_monster_defeated(monster["id"])
                            db_set_party(monster["id"], True)
                            if st.session_state.battle_task_id:
                                db_mark_task_done(st.session_state.battle_task_id)
                            invalidate_cache()
                            st.session_state.battle_monster_id = None
                            st.session_state.battle_phase = "idle"
                            st.rerun()
                        else:
                            st.warning("パーティは最大3体まで。先にメンバーを外してください。")
                with cy:
                    if st.button("📚 図鑑に登録のみ", use_container_width=True):
                        db_mark_monster_defeated(monster["id"])
                        if st.session_state.battle_task_id:
                            db_mark_task_done(st.session_state.battle_task_id)
                        invalidate_cache()
                        st.session_state.battle_monster_id = None
                        st.session_state.battle_phase = "idle"
                        st.rerun()

# ══════════════════════════════════════════════
# TAB 3 — 図鑑
# ══════════════════════════════════════════════

with tab3:
    st.markdown("### 📚 モンスター図鑑")
    st.markdown(f'<p style="color:var(--dim);font-size:13px;">討伐数: {len(defeated_mons)} 体 <span class="db-badge">🗄️ Supabase</span></p>', unsafe_allow_html=True)

    if not defeated_mons:
        st.markdown("""
        <div style="text-align:center;padding:40px;color:var(--dim);">
            <div style="font-size:48px;margin-bottom:16px;">📖</div>
            <div style="font-family:Cinzel,serif;">図鑑はまだ空白のページだ</div>
        </div>""", unsafe_allow_html=True)
    else:
        rarity_filter = st.multiselect("レアリティ絞り込み", ["C", "B", "A", "S"], default=["C", "B", "A", "S"])
        filtered = [m for m in defeated_mons if m["rarity"] in rarity_filter]
        cols = st.columns(4)
        for idx, m in enumerate(filtered):
            captured = (m.get("captured_at") or "")[:10]
            with cols[idx % 4]:
                st.markdown(f"""
                <div class="monster-card">
                    <span class="monster-sprite">{m['emoji']}</span>
                    <div style="color:var(--gold2);font-family:Cinzel,serif;font-size:12px;margin:8px 0 4px;">{m['name']}</div>
                    <div style="color:{RARITY_COLOR[m['rarity']]};font-size:11px;font-family:Cinzel,serif;">★ {m['rarity']}</div>
                    <div style="color:var(--dim);font-size:10px;margin-top:4px;">{captured}</div>
                    {tag_html(m.get('tags') or [])}
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 4 — パーティ管理
# ══════════════════════════════════════════════

with tab4:
    st.markdown("### 🎮 パーティ編成")
    st.markdown(f'<p style="color:var(--dim);font-size:13px;">最大3体 <span class="db-badge">🗄️ Supabase</span></p>', unsafe_allow_html=True)

    if not party_mons:
        st.markdown("""
        <div style="text-align:center;padding:40px;color:var(--dim);">
            <div style="font-size:48px;margin-bottom:16px;">🛡️</div>
            <div style="font-family:Cinzel,serif;">パーティに仲間がいない</div>
        </div>""", unsafe_allow_html=True)
    else:
        p_cols = st.columns(3)
        for i, m in enumerate(party_mons):
            tags = m.get("tags") or []
            with p_cols[i]:
                st.markdown(f"""
                <div class="parchment" style="text-align:center;">
                    <div style="color:var(--dim);font-family:Cinzel,serif;font-size:10px;letter-spacing:2px;margin-bottom:8px;">SLOT {i+1}</div>
                    <span style="font-size:56px;display:block;filter:drop-shadow(0 0 12px {m['color']});">{m['emoji']}</span>
                    <div style="color:var(--gold2);font-family:Cinzel,serif;font-size:14px;margin:10px 0 4px;">{m['name']}</div>
                    <div style="color:{RARITY_COLOR[m['rarity']]};font-size:11px;margin-bottom:10px;">★ {m['rarity']}</div>
                    {stat_bar(m['agility'], 'agi-bar', '⚡ AGI')}
                    {stat_bar(m['stamina'], 'sta-bar', '💪 STA')}
                    <div style="margin-top:10px;">{tag_html(tags)}</div>
                </div>""", unsafe_allow_html=True)
                if st.button("外す", key=f"remove_{m['id']}", use_container_width=True):
                    db_set_party(m["id"], False)
                    invalidate_cache()
                    st.rerun()

        total_agi = sum(m["agility"] for m in party_mons)
        total_sta = sum(m["stamina"] for m in party_mons)
        st.markdown('<hr style="border-color:var(--border);margin:20px 0;">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="parchment" style="text-align:center;">
            <div style="color:var(--gold);font-family:Cinzel,serif;font-size:14px;letter-spacing:3px;margin-bottom:12px;">PARTY STATUS</div>
            <div style="display:flex;justify-content:center;gap:40px;">
                <div>
                    <div style="color:var(--dim);font-size:11px;font-family:Cinzel,serif;">⚡ TOTAL AGI</div>
                    <div style="color:#2471a3;font-family:Cinzel,serif;font-size:28px;font-weight:700;">{total_agi}</div>
                </div>
                <div>
                    <div style="color:var(--dim);font-size:11px;font-family:Cinzel,serif;">💪 TOTAL STA</div>
                    <div style="color:#27ae60;font-family:Cinzel,serif;font-size:28px;font-weight:700;">{total_sta}</div>
                </div>
            </div>
            <div style="color:var(--dim);font-size:11px;margin-top:12px;font-style:italic;">🔒 AIケミストリー診断はプレミアム限定</div>
        </div>""", unsafe_allow_html=True)

    addable = [m for m in defeated_mons if not m["in_party"]]
    if addable and len(party_mons) < 3:
        st.markdown('<hr style="border-color:var(--border);margin:20px 0;">', unsafe_allow_html=True)
        st.markdown("#### 📚 図鑑から編成")
        options = {f"{m['emoji']} {m['name']} (★{m['rarity']})": m for m in addable}
        chosen  = st.selectbox("パーティに追加するモンスター", list(options.keys()))
        if st.button("➕ パーティに追加", use_container_width=True):
            db_set_party(options[chosen]["id"], True)
            invalidate_cache()
            st.rerun()
