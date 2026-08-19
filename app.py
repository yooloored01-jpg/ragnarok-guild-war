import os
import pandas as pd

# ==========================================
# KONFIGURASI TANGGAL & FILE
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(BASE_DIR, 'Book1.xlsx')
tanggal_war = "Jumat, 18 Agustus 2026"

# 1. Baca data dari Excel
df_main = pd.read_excel(excel_path, sheet_name='Main')
df_sub = pd.read_excel(excel_path, sheet_name='Sub')
df_job = pd.read_excel(excel_path, sheet_name='Data')

main_cols = list(df_main.columns)
sub_cols = list(df_sub.columns)

# 2. Mapping Job dari Sheet 3
job_map = {}
for _, row in df_job.iterrows():
    p_name = row.iloc[0]
    j_name = row.iloc[1]
    if pd.notna(p_name) and pd.notna(j_name):
        job_map[str(p_name).strip().lower()] = str(j_name).strip().lower()

# Palet Warna Job Ragnarok
job_colors = {
    "priest": "#0f5132", "swordman": "#842029", "wizard": "#084298",
    "hunter": "#664d03", "blacksmith": "#7b341e", "thief": "#432874",
    "gunner": "#53382c", "druid": "#40E0D0", "default": "#1e293b"
}
job_text_colors = {
    "priest": "#d1e7dd", "swordman": "#f8d7da", "wizard": "#cfe2ff",
    "druid": "#212121", "hunter": "#fff3cd", "blacksmith": "#f8d7da",
    "thief": "#e2d9f3", "gunner": "#f8d7da", "default": "#f1f5f9"
}

# 3. Buat File Eksternal script.js
js_content = """
function toggleScreenshotMode() {
    document.body.classList.toggle('screenshot-mode');
    if (document.body.classList.contains('screenshot-mode')) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

function openTab(evt, tabName) {
    var i, tabcontent = document.getElementsByClassName("tab-content");
    var tabbtns = document.getElementsByClassName("tab-btn");
    for (i = 0; i < tabcontent.length; i++) tabcontent[i].classList.remove("active");
    for (i = 0; i < tabbtns.length; i++) tabbtns[i].classList.remove("active");
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}

function searchPlayer() {
    var input = document.getElementById('searchInput').value.trim().toLowerCase();
    var resultDiv = document.getElementById('searchResult');
    if (!input) { resultDiv.style.display = 'block'; resultDiv.innerHTML = "⚠️ Masukkan nickname!"; return; }
    
    var players = document.querySelectorAll('.player');
    var found = false;
    players.forEach(function(p) { p.style.boxShadow = 'none'; });

    for (var i = 0; i < players.length; i++) {
        var p = players[i];
        if (p.getAttribute('data-nick').includes(input)) {
            found = true;
            var teamBox = p.closest('.team-box');
            var fieldName = teamBox.getAttribute('data-field');
            
            if (fieldName === 'Main Field') document.querySelector('.tab-btn:nth-child(1)').click();
            else document.querySelector('.tab-btn:nth-child(2)').click();

            setTimeout(function() { p.scrollIntoView({ behavior: 'smooth', block: 'center' }); }, 150);
            p.style.boxShadow = '0 0 15px 4px #facc15';
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = "✅ Ditemukan: " + p.innerText + " di " + teamBox.getAttribute('data-group');
            break;
        }
    }
    if (!found) { resultDiv.style.display = 'block'; resultDiv.innerHTML = "❌ Tidak ditemukan."; }
}
"""
with open(os.path.join(BASE_DIR, "script.js"), "w", encoding="utf-8") as f: f.write(js_content)

# 4. Rakit HTML
html = f"""
<!DOCTYPE html><html><head>
<meta charset="utf-8"><title>Ragnarok Guild War</title>
<style>
    body{{background: #0f172a; color: #fff; font-family: sans-serif; padding: 20px;}}
    .teams-flex-container{{display: flex; gap: 10px; overflow-x: auto; padding-bottom: 10px;}}
    .team-box{{min-width: 140px; background: #1e293b; padding: 10px; border-radius: 8px;}}
    .player{{background: var(--job-bg); color: var(--job-fg); margin: 4px 0; padding: 5px; text-align: center; border-radius: 4px; font-weight: bold;}}
    .tab-content{{display: none;}} .tab-content.active{{display: block;}}
    .tab-btn{{padding: 10px 20px; cursor: pointer;}} .tab-btn.active{{background: #d97706;}}
</style></head><body>

<div class="tab-menu"><button class="tab-btn active" onclick="openTab(event, 'main-tab')">MAIN FIELD</button>
<button class="tab-btn" onclick="openTab(event, 'sub-tab')">SUB FIELD</button></div>

<div id="main-tab" class="tab-content active">
    <h3>⚔️ PARTY RAID MAIN</h3>
    <div class="teams-flex-container">
"""

# Logic Main
for i in range(8):
    col = main_cols[i] if i < len(main_cols) else None
    html += f'<div class="team-box" data-field="Main Field" data-group="Party Raid Main"><h4>TEAM {i+1}</h4>'
    if col and col in df_main.columns:
        for val in df_main[col].dropna():
            job = job_map.get(str(val).lower().split("(")[0].strip(), "default")
            html += f'<div class="player" data-nick="{str(val).lower()}" style="--job-bg: {job_colors.get(job, "#1e293b")}; --job-fg: {job_text_colors.get(job, "#fff")};">{val}</div>'
    html += '</div>'

html += '</div></div><div id="sub-tab" class="tab-content"><h3>🛡️ SUB FIELD</h3><div class="teams-flex-container">'

# Logic Sub (Dibagi menjadi Sub 1 dan Sub 2)
for i in range(16):
    col = sub_cols[i] if i < len(sub_cols) else None
    group = "Sub 1" if i < 8 else "Sub 2"
    html += f'<div class="team-box" data-field="Sub Field" data-group="Party {group}"><h4>TEAM {i+1}</h4>'
    if col and col in df_sub.columns:
        for val in df_sub[col].dropna():
            job = job_map.get(str(val).lower().split("(")[0].strip(), "default")
            html += f'<div class="player" data-nick="{str(val).lower()}" style="--job-bg: {job_colors.get(job, "#1e293b")}; --job-fg: {job_text_colors.get(job, "#fff")};">{val}</div>'
    html += '</div>'

html += '</div></div><script src="script.js"></script></body></html>'

with open(os.path.join(BASE_DIR, "guild_war_pro_final.html"), "w", encoding="utf-8") as f:
    f.write(html)

print("File berhasil dibuat!")
