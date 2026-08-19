import os
import pandas as pd
import streamlit as st

# ==========================================
# KONFIGURASI GOOGLE SHEETS VIA LINK CSV
# ==========================================
# Caranya di Google Sheets Anda: 
# 1. Klik File > Share > Publish to web
# 2. Pilih sheet yang ingin di-publish (atau seluruh dokumen) dan ubah formatnya menjadi "Comma-Separated Values (.csv)"
# 3. Salin link CSV untuk masing-masing sheet dan masukkan ke bawah ini:

URL_MAIN = "https://docs.google.com/spreadsheets/d/1a__PWfdLc5XLcstIiexAtboh1iiKdCqtTxVzQ_8Jf6E/edit?usp=sharing"
URL_SUB = "https://docs.google.com/spreadsheets/d/1a__PWfdLc5XLcstIiexAtboh1iiKdCqtTxVzQ_8Jf6E/edit?usp=sharing"
URL_JOB = "https://docs.google.com/spreadsheets/d/1a__PWfdLc5XLcstIiexAtboh1iiKdCqtTxVzQ_8Jf6E/edit?usp=sharing"

# Membaca data langsung via pandas (sangat stabil di cloud)
df_main = pd.read_csv(URL_MAIN)
df_sub = pd.read_csv(URL_SUB)
df_job = pd.read_csv(URL_JOB)

sub_cols = list(df_sub.columns)
tanggal_war = "Jumat, 18 Agustus 2026"

# 2. Mapping Job dari Sheet 3
job_map = {}
for _, row in df_job.iterrows():
    p_name = row.iloc[0]
    j_name = row.iloc[1]
    if pd.notna(p_name) and pd.notna(j_name):
        job_map[str(p_name).strip().lower()] = str(j_name).strip().lower()

# Palet Warna Job Ragnarok
job_colors = {
    "priest": "#0f5132",        
    "swordman": "#842029",      
    "wizard": "#084298",        
    "hunter": "#664d03",        
    "blacksmith": "#7b341e",   
    "thief": "#432874",         
    "gunner": "#53382c",        
    "druid": "#40E0D0",         
    "default": "#1e293b"        
}

job_text_colors = {
    "priest": "#d1e7dd",
    "swordman": "#f8d7da",
    "wizard": "#cfe2ff",
    "druid": "#212121",
    "hunter": "#fff3cd",
    "blacksmith": "#f8d7da",
    "thief": "#e2d9f3",
    "gunner": "#f8d7da",
    "default": "#f1f5f9"
}

# 3. Buat File Eksternal script.js agar tidak ada error f-string
js_content = """
function toggleScreenshotMode() {
    document.body.classList.toggle('screenshot-mode');
    if (document.body.classList.contains('screenshot-mode')) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

function openTab(evt, tabName) {
    var i, tabcontent, tabbtns;
    
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].classList.remove("active");
    }
    
    tabbtns = document.getElementsByClassName("tab-btn");
    for (i = 0; i < tabbtns.length; i++) {
        tabbtns[i].classList.remove("active");
    }
    
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}

function handleSearchKey(event) {
    if (event.key === 'Enter') {
        searchPlayer();
    }
}

function searchPlayer() {
    var input = document.getElementById('searchInput').value.trim().toLowerCase();
    var resultDiv = document.getElementById('searchResult');
    
    if (!input) {
        resultDiv.style.display = 'block';
        resultDiv.style.borderLeftColor = '#f87171';
        resultDiv.innerHTML = "⚠️ Silakan ketik nickname terlebih dahulu!";
        return;
    }

    var players = document.querySelectorAll('.player');
    var found = false;

    // Bersihkan highlight sebelumnya
    players.forEach(function(p) { p.style.boxShadow = 'none'; });

    for (var i = 0; i < players.length; i++) {
        var p = players[i];
        var nickAttr = p.getAttribute('data-nick');
        
        if (nickAttr && nickAttr.includes(input)) {
            found = true;
            var teamBox = p.closest('.team-box');
            var flexContainer = p.closest('.teams-flex-container');
            var fieldName = teamBox.getAttribute('data-field');
            var groupName = teamBox.getAttribute('data-group');
            var teamName = teamBox.getAttribute('data-team');
            var realName = p.innerText;

            // Pindah tab otomatis
            if (fieldName === 'Main Field') {
                document.querySelector('.tab-btn:nth-child(1)').click();
            } else {
                document.querySelector('.tab-btn:nth-child(2)').click();
            }

            // Beri jeda agar DOM tab sempat render sebelum digulirkan
            setTimeout(function() {
                if (flexContainer) {
                    flexContainer.scrollTo({
                        left: teamBox.offsetLeft - flexContainer.offsetLeft - 20,
                        behavior: 'smooth'
                    });
                }
                p.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 150);

            p.style.boxShadow = '0 0 15px 4px #facc15';

            resultDiv.style.display = 'block';
            resultDiv.style.borderLeftColor = '#38bdf8';
            resultDiv.innerHTML = "✅ Ditemukan! <b>" + realName + "</b> terdaftar di <b>" + fieldName + "</b> &gt; <b>" + groupName + "</b> &gt; <span style='color:#facc15;'>" + teamName + "</span>";
            break;
        }
    }

    if (!found) {
        resultDiv.style.display = 'block';
        resultDiv.style.borderLeftColor = '#f87171';
        resultDiv.innerHTML = "❌ Nickname \\"<b>" + input + "</b>\\" tidak ditemukan di daftar Main maupun Sub Field. Coba periksa ejaannya.";
    }
}
"""

with open(os.path.join(BASE_DIR, "script.js"), "w", encoding="utf-8") as f_js:
    f_js.write(js_content)


# 4. Rakit Tampilan HTML
html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ragnarok Guild War - Battle Strategy</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;900&family=Roboto:wght@400;500;700&display=swap');

* {{ box-sizing: border-box; }}

body {{
    margin: 0;
    min-height: 100vh;
    padding: 25px;
    color: #ffffff;
    font-family: 'Roboto', Arial, sans-serif;
    background: 
        linear-gradient(rgba(10, 15, 30, 0.5), rgba(15, 23, 42, 0.6)),
        url('ro.jpg') no-repeat center center fixed;
    background-size: cover;
    background-attachment: fixed;
    overflow-x: auto;
}}

.container {{
    position: relative;
    max-width: 1750px;
    margin: auto;
    padding: 35px;
    border: none;
    border-radius: 20px;
    background: transparent;
    box-shadow: none;
}}

.banner-header, .tab-menu, .tab-content, .search-container {{ position: relative; z-index: 1; }}

.banner-header {{ text-align: center; padding: 5px 0 15px; }}
.title-wrapper {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 18px;
}}
.poring-img {{ width: 65px; }}

.header {{
    font-family: 'Cinzel', serif;
    color: #facc15;
    font-size: clamp(22px, 2.5vw, 38px);
    font-weight: 900;
    letter-spacing: 3px;
}}
.subheader {{
    margin-top: 5px;
    color: #93c5fd;
    font-family: 'Cinzel', serif;
    font-size: 13px;
    letter-spacing: 4px;
    font-weight: 700;
}}
.date-container {{ text-align: center; }}
.date-badge {{
    display: inline-block;
    margin: 14px auto 12px;
    padding: 8px 24px;
    border: 1px solid #d97706;
    border-radius: 999px;
    color: #fef3c7;
    background: #0f172a;
    font-family: 'Cinzel', serif;
    font-size: 12px;
    letter-spacing: 1px;
    font-weight: 700;
}}

/* SEARCH BOX STYLING */
.search-container {{
    max-width: 600px;
    margin: 0 auto 25px auto;
    background: #0f172a;
    border: 2px solid #d97706;
    border-radius: 14px;
    padding: 15px 20px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
}}
.search-container h3 {{
    margin: 0 0 10px 0;
    color: #facc15;
    font-family: 'Cinzel', serif;
    font-size: 14px;
    letter-spacing: 1px;
}}
.search-box-wrapper {{ display: flex; gap: 8px; }}
.search-input {{
    flex: 1;
    padding: 10px 15px;
    background: #1e293b;
    border: 1px solid #475569;
    border-radius: 8px;
    color: #ffffff;
    font-size: 14px;
    outline: none;
}}
.search-input:focus {{ border-color: #facc15; }}
.search-btn {{
    font-family: 'Cinzel', serif;
    font-weight: 700;
    background: #d97706;
    color: #ffffff;
    border: none;
    padding: 0 20px;
    border-radius: 8px;
    cursor: pointer;
}}
.search-btn:hover {{ background: #f59e0b; }}
.search-result {{
    margin-top: 12px;
    font-size: 13px;
    color: #38bdf8;
    font-weight: 500;
    min-height: 20px;
    text-align: left;
    background: #1e293b;
    padding: 8px 12px;
    border-radius: 6px;
    border-left: 4px solid #38bdf8;
    display: none;
}}

.controls {{
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
    margin: 0 0 20px;
}}
.control-btn, .tab-btn {{
    font-family: 'Cinzel', serif;
    font-weight: 700;
    letter-spacing: 1px;
    color: #ffffff;
    background: #0f172a;
    border: 1px solid #d97706;
    border-radius: 10px;
    cursor: pointer;
}}
.control-btn {{ padding: 10px 18px; font-size: 12px; }}
.control-btn:hover, .tab-btn:hover {{
    border-color: #facc15;
    background: #1e293b;
}}

.tab-menu {{
    display: flex;
    justify-content: center;
    gap: 12px;
    padding: 12px 0 18px;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    margin-bottom: 24px;
}}
.tab-btn {{ min-width: 230px; padding: 12px 22px; font-size: 13px; }}
.tab-btn.active {{
    color: #ffffff;
    border-color: #f59e0b;
    background: #b45309;
}}

.tab-content {{ display: none; }}
.tab-content.active {{ display: block; }}

.content-wrapper {{
    display: flex;
    gap: 22px;
    align-items: flex-start;
}}
.main-content-area {{ flex: 1; min-width: 0; }}
.sidebar-area {{
    width: 370px;
    flex-shrink: 0;
    position: sticky;
    top: 20px;
    margin-top: 55px;
}}

.section-title {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 24px 0 14px;
    padding: 0 0 8px 4px;
    color: #facc15;
    font-family: 'Cinzel', serif;
    font-size: 17px;
    letter-spacing: .8px;
    border-bottom: 2px solid #d97706;
    font-weight: 700;
}}

.teams-flex-container {{
    display: flex;
    flex-wrap: nowrap;
    gap: 10px;
    margin-bottom: 20px;
    overflow-x: auto;
    padding-bottom: 8px;
}}

.team-box {{
    flex: 1;
    min-width: 130px;
    max-width: 160px;
    padding: 8px;
    border: 1px solid #475569;
    border-radius: 13px;
    background: #0f172a;
}}
.team-box:hover {{
    border-color: #facc15;
    background: #1e293b;
}}

.team-box.chaos-box {{
    background: #064e3b;
    border: 1px solid #059669;
}}
.team-box.chaos-box h4 {{
    color: #34d399;
    border-bottom: 1px solid #059669;
}}

.team-box h4 {{
    margin: 0 0 8px;
    padding: 2px 0 6px;
    color: #93c5fd;
    text-align: center;
    font-family: 'Cinzel', serif;
    font-size: 13px;
    letter-spacing: 1px;
    border-bottom: 1px solid #334155;
}}

.player {{
    min-height: 34px;
    margin: 5px 0;
    padding: 6px 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    background: var(--job-bg);
    color: var(--job-fg);
    font-size: 14px;
    font-weight: 700;
    text-align: center;
    word-break: break-word;
    border: 1px solid rgba(255, 255, 255, 0.15);
}}

.empty-team {{
    min-height: 34px;
    display: grid;
    place-items: center;
    color: #94a3b8;
    border: 1px dashed #475569;
    border-radius: 6px;
    font-size: 12px;
}}

.msg-box {{
    padding: 18px 20px;
    border-radius: 12px;
    background: #0f172a;
    line-height: 1.5;
    font-size: 15px;
    margin-bottom: 20px;
    border: 1px solid #d97706;
}}
.msg-box h4 {{
    margin: 0 0 8px;
    padding-bottom: 6px;
    font-family: 'Cinzel', serif;
    font-size: 13px;
    letter-spacing: 1px;
    border-bottom: 1px solid #334155;
    color: #facc15;
}}

/* SCREENSHOT MODE FULL */
body.screenshot-mode {{
    padding: 10px !important;
    background: #0f172a !important;
}}
.screenshot-mode .tab-menu, 
.screenshot-mode .controls,
.screenshot-mode .search-container {{ 
    display: none !important; 
}}
.screenshot-mode .tab-content {{ 
    display: block !important; 
}}
.screenshot-mode .container {{ 
    max-width: none !important; 
    border: none !important;
    box-shadow: none !important;
    padding: 20px 25px 35px !important;
    background: transparent !important;
}}

@media (max-width: 1200px) {{
    .content-wrapper {{ flex-direction: column; }}
    .sidebar-area {{ width: 100%; position: static; margin-top: 0 !important; }}
}}
</style>
</head>
<body>

<div class="container">
    <div class="banner-header">
        <div class="title-wrapper">
            <img src="poring.png" alt="Poring" class="poring-img">
            <div class="header">RAGNAROK GUILD LEAGUE WAR</div>
            <img src="poring.png" alt="Poring" class="poring-img" style="transform: scaleX(-1);">
        </div>
        <div class="subheader">Official Deployment & Strategy Dashboard Guild Lumiere</div>
        <div class="date-container">
            <div class="date-badge">📅 Jadwal War: {tanggal_war}</div>
        </div>
    </div>

    <!-- FITUR SEARCH NICKNAME -->
    <div class="search-container">
        <h3>🔍 CEK POSISI PLAYER</h3>
        <div class="search-box-wrapper">
            <input type="text" id="searchInput" class="search-input" placeholder="Ketik nickname kamu di sini..." onkeypress="handleSearchKey(event)">
            <button class="search-btn" onclick="searchPlayer()">CARI</button>
        </div>
        <div id="searchResult" class="search-result"></div>
    </div>

    <div class="controls">
        <button class="control-btn" onclick="toggleScreenshotMode()">📸 SCREENSHOT MODE (FULL)</button>
        <button class="control-btn" onclick="window.print()">🖨️ PRINT / PDF</button>
    </div>

    <!-- TAB MENU NAVIGATION -->
    <div class="tab-menu">
        <button class="tab-btn active" onclick="openTab(event, 'main-tab')">⚔️ MAIN FIELD (60)</button>
        <button class="tab-btn" onclick="openTab(event, 'sub-tab')">🛡️ SUB FIELD (85)</button>
    </div>

    <!-- TAB 1: MAIN FIELD -->
    <div id="main-tab" class="tab-content active">
        <div class="content-wrapper">
            <div class="main-content-area">
                
                <div class="section-title">⚔️ PARTY RAID MAIN (TEAM 1 - 8)</div>
                <div class="teams-flex-container">
"""

main_cols = list(df_main.columns)
for i, col in enumerate(main_cols[:8]):
    if col in df_main.columns:
        header_name = f"TEAM {i + 1}"
        html += f'<div class="team-box" data-field="Main Field" data-group="Party Raid Main" data-team="{header_name}"><h4>{header_name}</h4>'
        values = df_main[col].dropna()
        if len(values) == 0: html += '<div class="empty-team">—</div>'
        for val in values:
            p_name = str(val).strip()
            p_lower = p_name.lower().split("(")[0].strip()
            job = job_map.get(p_lower, "default")
            bg_col = job_colors.get(job, job_colors["default"])
            txt_col = job_text_colors.get(job, job_text_colors["default"])
            html += f'<div class="player" data-nick="{p_name.lower()}" style="--job-bg: {bg_col}; --job-fg: {txt_col};">{p_name}</div>'
        html += '</div>'

html += f"""
                </div>

                <div class="section-title">🛡️ CHAOS PARTY MAIN</div>
                <div class="teams-flex-container">
"""

for col in main_cols[8:]:
    if col in df_main.columns:
        team_title = col.upper()
        html += f'<div class="team-box" style="flex:unset; width:160px;" data-field="Main Field" data-group="Chaos Party Main" data-team="{team_title}"><h4>{team_title}</h4>'
        values = df_main[col].dropna()
        if len(values) == 0: html += '<div class="empty-team">—</div>'
        for val in values:
            p_name = str(val).strip()
            p_lower = p_name.lower().split("(")[0].strip()
            job = job_map.get(p_lower, "default")
            bg_col = job_colors.get(job, job_colors["default"])
            txt_col = job_text_colors.get(job, job_text_colors["default"])
            html += f'<div class="player" data-nick="{p_name.lower()}" style="--job-bg: {bg_col}; --job-fg: {txt_col};">{p_name}</div>'
        html += '</div>'

html += f"""
                </div>
            </div>

            <div class="sidebar-area">
                <div class="msg-box">
                    <h4>⚠️ CATATAN & INSTRUKSI MAIN FIELD</h4>
                    <p>
                        <b>📊 Info Umum (Total 60 Player):</b><br>
                        • Terbagi menjadi <b>2 Party Raid</b> dan <b>4 Normal Party</b>.<br>
                        • <b>Tolong prepare di 20.45 untuk join party raid / join party masing".<br><br>                        
                        <b>🎯 Pembagian Tugas:</b><br>
                        • <b>Team 1 - 4:</b> Lane Mid (stay push/defense di lane mid).<br>
                        • <b>Team 5 - 6:</b> Lane Top (push/defense lane top / atas).<br>
                        • <b>Team 7 - 8:</b> Lane Bottom (push/defense lane bottom / bawah).<br>
                        • <b>Team Chaos 1 - 4:</b> Tim Rusuh / Backup lane yang ke push dari 3 lane bantu cover, kalau bisa dorong musuh lewat belakang.
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 2: SUB FIELD -->
    <div id="sub-tab" class="tab-content">
        <div class="section-title">🛡️ PARTY RAID SUB 1 & CHAOS PARTY (TEAM 1 - 8)</div>
        <div class="teams-flex-container">
"""

for i, col in enumerate(sub_cols[:8]):
    if col in df_sub.columns:
        header_name = f"TEAM {i + 1}"
        html += f'<div class="team-box" data-field="Sub Field" data-group="Party Raid Sub 1" data-team="{header_name}"><h4>{header_name}</h4>'
        values = df_sub[col].dropna()
        if len(values) == 0: html += '<div class="empty-team">—</div>'
        for val in values:
            p_name = str(val).strip()
            p_lower = p_name.lower().split("(")[0].strip()
            job = job_map.get(p_lower, "default")
            bg_col = job_colors.get(job, job_colors["default"])
            txt_col = job_text_colors.get(job, job_text_colors["default"])
            html += f'<div class="player" data-nick="{p_name.lower()}" style="--job-bg: {bg_col}; --job-fg: {txt_col};">{p_name}</div>'
        html += '</div>'

# Membaca sisa kolom untuk Sub Field (Chaos / Penalty) dengan aman
for col in sub_cols[16:]:
    if col in df_sub.columns:
        c_name = col.upper()
        if "PINALTY" in c_name:
            header_color = "color: #f87171; border-bottom: 1px solid #ef4444;"
            box_class = "team-box"
            group_name = "Sub Field (Penalty)"
        else:
            header_color = "color: #34d399; border-bottom: 1px solid #059669;"
            box_class = "team-box chaos-box"
            group_name = "Sub Field (Chaos/Extra)"
            
        html += f'<div class="{box_class}" data-field="Sub Field" data-group="{group_name}" data-team="{c_name}"><h4 style="{header_color}">{c_name}</h4>'
        values = df_sub[col].dropna()
        if len(values) == 0: html += '<div class="empty-team">—</div>'
        for val in values:
            p_name = str(val).strip()
            p_lower = p_name.lower().split("(")[0].strip()
            job = job_map.get(p_lower, "default")
            bg_col = job_colors.get(job, job_colors["default"])
            txt_col = job_text_colors.get(job, job_text_colors["default"])
            html += f'<div class="player" data-nick="{p_name.lower()}" style="--job-bg: {bg_col}; --job-fg: {txt_col};">{p_name}</div>'
        html += '</div>'

html += f"""
        </div>

        <!-- PARTY RAID SUB 2 (TEAM 1 - 8) -->
        <div class="section-title">🛡️ PARTY RAID SUB 2 (TEAM 1 - 8)</div>
        <div class="teams-flex-container">
"""

for i, col in enumerate(sub_cols[8:16]):
    if col in df_sub.columns:
        header_name = f"TEAM {i + 1}"
        html += f'<div class="team-box" data-field="Sub Field" data-group="Party Raid Sub 2" data-team="{header_name}"><h4>{header_name}</h4>'
        values = df_sub[col].dropna()
        if len(values) == 0: html += '<div class="empty-team">—</div>'
        for val in values:
            p_name = str(val).strip()
            p_lower = p_name.lower().split("(")[0].strip()
            job = job_map.get(p_lower, "default")
            bg_col = job_colors.get(job, job_colors["default"])
            txt_col = job_text_colors.get(job, job_text_colors["default"])
            html += f'<div class="player" data-nick="{p_name.lower()}" style="--job-bg: {bg_col}; --job-fg: {txt_col};">{p_name}</div>'
        html += '</div>'

html += f"""
        </div>

        <!-- SIDEBAR SUB FIELD DI BAWAH -->
        <div style="margin-top: 30px; max-width: 100%;">
            <div class="msg-box">
                <h4>⚠️ CATATAN & INSTRUKSI SUB FIELD</h4>
                <p>
                    <b>📊 Info Umum (Total 85 Player):</b><br>
                    • Untuk party yang tidak mendapatkan <b>Priest</b>, mohon maaf karena keterbatasan player dan banyak yang mungkin tidak bisa ON.<br>
                    • Terbagi menjadi <b>2 Party Raid</b> dan <b>1 Chaos Party</b>.<br>
                    • <b>Tolong prepare di 20.45 untuk join party raid / join party masing".<br><br> 
                    
                    <b>🎯 Tugas di Sub Field:</b><br>
                    • <b>PVP:</b> Ketemu player lain langsung <b>KILL!</b><br>
                    • <b>Farming Monster:</b> Bunuh monster, ambil <b>Batu/Item</b>, bawa balik ke base!<br>
                    • <b>Fungsi Batu:</b> Buff ATK/DEF + Repair Tower di Main Field.
                </p>                
            </div>
        </div>
    </div>
</div>

<!-- SCRIPT DIPISAH KE FILE EXTERNAL AGAR AMAN DARI ERROR -->
<script src="script.js"></script>

</body>
</html>
"""

# Simpan file HTML
with open(os.path.join(BASE_DIR, "guild_war_pro_final.html"), "w", encoding="utf-8") as f:
    f.write(html)

print("Berhasil! File script.js dan guild_war_pro_final.html berhasil dibuat dengan struktur lengkap.")
