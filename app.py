import base64
import os
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# ==========================================
# 0. SETTING STREAMLIT & TANGGAL OTOMATIS
# ==========================================
st.set_page_config(page_title="Ragnarok Guild War Strategy", layout="wide")

now = datetime.now()
days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
tanggal_war = f"{days[now.weekday()]}, {now.day} {months[now.month - 1]} {now.year}"

# ==========================================
# FUNGSI HELPER
# ==========================================
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        ext = path.split(".")[-1].lower()
        mime = "image/png" if ext == "png" else "image/jpeg"
        return f"data:{mime};base64,{encoded}"
    return ""

poring_b64 = get_image_base64("poring.png")
ro_b64 = get_image_base64("ro.jpg")

# ==========================================
# KONFIGURASI DATA
# ==========================================
sheet_id = "1a__PWfdLc5XLcstIiexAtboh1iiKdCqtTxVzQ_8Jf6E"
url_main = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Main"
url_sub = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sub"
url_job = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Data"

@st.cache_data
def load_data():
    return pd.read_csv(url_main), pd.read_csv(url_sub), pd.read_csv(url_job)

df_main, df_sub, df_job = load_data()
sub_cols = list(df_sub.columns)
job_map = {str(row.iloc[0]).strip().lower(): str(row.iloc[1]).strip().lower() for _, row in df_job.iterrows() if pd.notna(row.iloc[0]) and pd.notna(row.iloc[1])}

job_colors = {"priest": "#0f5132", "swordman": "#842029", "wizard": "#084298", "hunter": "#664d03", "blacksmith": "#7b341e", "thief": "#432874", "gunner": "#53382c", "druid": "#40E0D0", "default": "#1e293b"}
job_text_colors = {"priest": "#d1e7dd", "swordman": "#f8d7da", "wizard": "#cfe2ff", "druid": "#212121", "hunter": "#fff3cd", "blacksmith": "#f8d7da", "thief": "#e2d9f3", "gunner": "#f8d7da", "default": "#f1f5f9"}

js_content = """
function openTab(evt, tabName) {
    var i, tabcontent, tabbtns;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) { tabcontent[i].classList.remove("active"); }
    tabbtns = document.getElementsByClassName("tab-btn");
    for (i = 0; i < tabbtns.length; i++) { tabbtns[i].classList.remove("active"); }
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}
function handleSearchKey(event) { if (event.key === 'Enter') { searchPlayer(); } }
function searchPlayer() {
    var input = document.getElementById('searchInput').value.trim().toLowerCase();
    var resultDiv = document.getElementById('searchResult');
    if (!input) { resultDiv.style.display = 'block'; resultDiv.innerHTML = "⚠️ Ketik nickname!"; return; }
    var players = document.querySelectorAll('.player');
    var found = false;
    players.forEach(function(p) { p.style.boxShadow = 'none'; });
    for (var i = 0; i < players.length; i++) {
        var p = players[i];
        if (p.getAttribute('data-nick').includes(input)) {
            found = true;
            var teamBox = p.closest('.team-box');
            if (teamBox.getAttribute('data-field') === 'Main Field') { document.querySelector('.tab-btn:nth-child(1)').click(); }
            else { document.querySelector('.tab-btn:nth-child(2)').click(); }
            setTimeout(function() { p.scrollIntoView({ behavior: 'smooth', block: 'center' }); }, 150);
            p.style.boxShadow = '0 0 15px 4px #facc15';
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = "✅ Ditemukan di " + teamBox.getAttribute('data-team');
            break;
        }
    }
    if (!found) { resultDiv.style.display = 'block'; resultDiv.innerHTML = "❌ Tidak ditemukan."; }
}
"""

html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;900&family=Roboto:wght@400;500;700&display=swap');
body {{ margin:0; padding:20px; color:#fff; font-family:'Roboto', sans-serif; background: #4FE8CC; background-image: linear-gradient(rgba(13,148,136,0.85), rgba(15,118,110,0.90)), url('{ro_b64}'); background-size: cover; background-attachment: fixed; }}
.container {{ max-width: 1200px; margin: auto; }}
.banner-header {{ text-align: center; padding: 20px 0; }}
.header {{ font-family:'Cinzel', serif; color:#facc15; font-size:38px; font-weight:900; letter-spacing:3px; }}
.search-container {{ max-width: 600px; margin: 0 auto 20px; background: rgba(15,23,42,0.85); border: 2px solid #d97706; padding: 15px; border-radius: 14px; text-align: center; }}
.search-input {{ padding: 10px; width: 60%; background: #1e293b; color: #fff; border: 1px solid #475569; border-radius: 8px; }}
.tab-menu {{ display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; }}
.tab-btn {{ padding: 12px 30px; cursor: pointer; background: rgba(15,23,42,0.85); border: 1px solid #d97706; color: #fff; border-radius: 10px; font-weight:700; }}
.tab-btn.active {{ background: #b45309; border-color: #f59e0b; }}
.tab-content {{ display: none; }}
.tab-content.active {{ display: block; }}
.section-title {{ color: #facc15; font-family:'Cinzel', serif; font-size:17px; margin: 20px 0 10px; border-bottom: 2px solid #d97706; padding-bottom: 8px; }}
.teams-flex-container {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }}
.team-box {{ flex: 1; min-width: 150px; max-width: 180px; background: rgba(15,23,42,0.85); padding: 8px; border-radius: 10px; border: 1px solid #475569; }}
.team-box h4 {{ margin: 0 0 8px; color: #93c5fd; text-align: center; border-bottom: 1px solid #334155; font-size: 13px; }}
.player {{ margin: 4px 0; padding: 6px; border-radius: 5px; background: var(--job-bg); color: var(--job-fg); font-size: 11px; text-align: center; font-weight: 700; border: 1px solid rgba(255,255,255,0.1); }}
.msg-box {{ padding: 15px; border-radius: 12px; background: rgba(15,23,42,0.9); border: 1px solid #d97706; margin-top: 20px; line-height: 1.6; font-size: 14px; }}
.msg-box h4 {{ color: #facc15; margin: 0 0 10px; border-bottom: 1px solid #334155; padding-bottom: 5px; }}
</style>
</head>
<body>
<div class="container">
    <div class="banner-header">
        <div class="header">RAGNAROK GUILD LEAGUE WAR</div>
        <div>📅 {tanggal_war}</div>
    </div>
    <div class="search-container">
        <input type="text" id="searchInput" class="search-input" placeholder="Ketik nickname...">
        <button onclick="searchPlayer()">CARI</button>
        <div id="searchResult" style="margin-top:10px; display:none; color:#38bdf8;"></div>
    </div>
    <div class="tab-menu">
        <button class="tab-btn active" onclick="openTab(event, 'main-tab')">⚔️ MAIN FIELD</button>
        <button class="tab-btn" onclick="openTab(event, 'sub-tab')">🛡️ SUB FIELD</button>
    </div>

    <!-- MAIN TAB -->
    <div id="main-tab" class="tab-content active">
        <div class="section-title">⚔️ PARTY RAID MAIN (TEAM 1 - 8)</div>
        <div class="teams-flex-container">
"""

# Main Loop Main Field
main_cols = list(df_main.columns)
for i, col in enumerate(main_cols[:8]):
    if col in df_main.columns:
        html += f'<div class="team-box" data-field="Main Field" data-team="TEAM {i+1}"><h4>TEAM {i+1}</h4>'
        for val in df_main[col].dropna():
            p_name = str(val).strip()
            job = job_map.get(p_name.lower().split("(")[0].strip(), "default")
            html += f'<div class="player" data-nick="{p_name.lower()}" style="--job-bg: {job_colors.get(job)}; --job-fg: {job_text_colors.get(job)};">{p_name}</div>'
        html += '</div>'

html += '</div><div class="section-title">🛡️ CHAOS PARTY MAIN</div><div class="teams-flex-container">'
for col in main_cols[8:]:
    html += f'<div class="team-box" data-field="Main Field" data-team="{col.upper()}"><h4>{col.upper()}</h4>'
    for val in df_main[col].dropna():
        p_name = str(val).strip()
        job = job_map.get(p_name.lower().split("(")[0].strip(), "default")
        html += f'<div class="player" data-nick="{p_name.lower()}" style="--job-bg: {job_colors.get(job)}; --job-fg: {job_text_colors.get(job)};">{p_name}</div>'
    html += '</div>'

html += f"""
        </div>
        <div class="msg-box">
            <h4>⚠️ CATATAN & INSTRUKSI MAIN FIELD</h4>
            <p>• Terbagi menjadi 2 Party Raid dan 4 Normal Party.<br>• Prepare di 20.45 untuk join party.<br>
            • <b>Team 1-4:</b> Lane Mid. <b>Team 5-6:</b> Lane Top. <b>Team 7-8:</b> Lane Bottom.<br>
            • <b>Team Chaos:</b> Tim rusuh/backup.</p>
        </div>
    </div>

    <!-- SUB TAB -->
    <div id="sub-tab" class="tab-content">
        <div class="section-title">🛡️ PARTY RAID SUB 1</div>
        <div class="teams-flex-container">
"""

# Main Loop Sub Field
for i, col in enumerate(sub_cols[:8]):
    html += f'<div class="team-box" data-field="Sub Field" data-team="TEAM {i+1}"><h4>TEAM {i+1}</h4>'
    for val in df_sub[col].dropna():
        p_name = str(val).strip()
        job = job_map.get(p_name.lower().split("(")[0].strip(), "default")
        html += f'<div class="player" data-nick="{p_name.lower()}" style="--job-bg: {job_colors.get(job)}; --job-fg: {job_text_colors.get(job)};">{p_name}</div>'
    html += '</div>'

html += '</div><div class="section-title">🛡️ EXTRA PARTY / CHAOS</div><div class="teams-flex-container">'
for col in sub_cols[16:]:
    html += f'<div class="team-box" data-field="Sub Field" data-team="{col.upper()}"><h4>{col.upper()}</h4>'
    for val in df_sub[col].dropna():
        p_name = str(val).strip()
        job = job_map.get(p_name.lower().split("(")[0].strip(), "default")
        html += f'<div class="player" data-nick="{p_name.lower()}" style="--job-bg: {job_colors.get(job)}; --job-fg: {job_text_colors.get(job)};">{p_name}</div>'
    html += '</div>'

html += f"""
        </div>
        <div class="section-title">🛡️ PARTY RAID SUB 2</div>
        <div class="teams-flex-container">
"""

for i, col in enumerate(sub_cols[8:16]):
    html += f'<div class="team-box" data-field="Sub Field" data-team="TEAM {i+1}"><h4>TEAM {i+1}</h4>'
    for val in df_sub[col].dropna():
        p_name = str(val).strip()
        job = job_map.get(p_name.lower().split("(")[0].strip(), "default")
        html += f'<div class="player" data-nick="{p_name.lower()}" style="--job-bg: {job_colors.get(job)}; --job-fg: {job_text_colors.get(job)};">{p_name}</div>'
    html += '</div>'

html += f"""
        </div>
        <div class="msg-box">
            <h4>⚠️ CATATAN & INSTRUKSI SUB FIELD</h4>
            <p>• Terbagi 2 Party Raid & 1 Chaos Party.<br>• <b>PVP:</b> Kill! <b>Farming:</b> Ambil batu/item bawa ke base.</p>
        </div>
    </div>
</div>
<script>{js_content}</script>
</body>
</html>
"""

components.html(html, height=2200, scrolling=True)
