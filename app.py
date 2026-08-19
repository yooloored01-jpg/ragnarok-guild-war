import pandas as pd
import streamlit as st

# ==========================================
# KONFIGURASI HALAMAN & STREAMLIT
# ==========================================
st.set_page_config(layout="wide", page_title="Ragnarok Guild War - Battle Strategy")

# ==========================================
# KONFIGURASI GOOGLE SHEETS
# ==========================================
# Masukkan link Google Sheets Anda yang sudah dipublish ke web dalam bentuk CSV
# Contoh format link CSV dari Google Sheets per sheet:
# https://docs.google.com/spreadsheets/d/ID_SPREADSHEET_ANDA/gviz/tq?tqx=out:csv&sheet=NAMA_SHEET
tanggal_war = "Jumat, 18 Agustus 2026"

# Ganti URL di bawah dengan link publis / CSV Google Sheets Anda
SHEET_ID = "MASUKKAN_SPREADSHEET_ID_ANDA_DISINI"
url_main = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Main"
url_sub = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sub"
url_job = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Data"

try:
    df_main = pd.read_csv(url_main)
    df_sub = pd.read_csv(url_sub)
    df_job = pd.read_csv(url_job)
except Exception:
    st.error(
        "Gagal memuat data dari Google Sheets. Pastikan Google Sheets sudah diset ke 'Anyone with the link can view' dan format URL Sheet ID sudah benar."
    )
    st.stop()

sub_cols = list(df_sub.columns)

# Mapping Job dari Sheet Data
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
    "default": "#1e293b",
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
    "default": "#f1f5f9",
}

# Rakit Tampilan HTML Langsung di Python
html_content = f"""
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
    padding: 25px;
    color: #ffffff;
    font-family: 'Roboto', Arial, sans-serif;
    background: 
        linear-gradient(rgba(10, 15, 30, 0.85), rgba(15, 23, 42, 0.85)),
        url('https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=1920&auto=format&fit=crop');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.container {{
    max-width: 1750px;
    margin: auto;
    padding: 20px;
}}

.banner-header {{ text-align: center; padding: 5px 0 15px; }}
.title-wrapper {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 18px;
}}
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

/* SEARCH BOX */
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
.search-result {{
    margin-top: 12px;
    font-size: 13px;
    color: #38bdf8;
    text-align: left;
    background: #1e293b;
    padding: 8px 12px;
    border-radius: 6px;
    border-left: 4px solid #38bdf8;
    display: none;
}}

/* TAB MENU */
.tab-menu {{
    display: flex;
    justify-content: center;
    gap: 12px;
    padding: 12px 0 18px;
    margin-bottom: 24px;
}}
.tab-btn {{
    font-family: 'Cinzel', serif;
    font-weight: 700;
    color: #ffffff;
    background: #0f172a;
    border: 1px solid #d97706;
    border-radius: 10px;
    padding: 12px 22px;
    cursor: pointer;
    min-width: 230px;
}}
.tab-btn.active {{
    background: #b45309;
    border-color: #f59e0b;
}}

.tab-content {{ display: none; }}
.tab-content.active {{ display: block; }}

/* CONTENT & SIDEBAR LAYOUT */
.content-wrapper {{
    display: flex;
    gap: 25px;
    align-items: flex-start;
    width: 100%;
}}
.main-content-area {{
    flex: 1;
    min-width: 0;
}}
.sidebar-area {{
    width: 350px;
    flex-shrink: 0;
    background: #0f172a;
    border: 1px solid #d97706;
    border-radius: 12px;
    padding: 18px;
    position: sticky;
    top: 20px;
}}

.section-title {{
    margin: 20px 0 12px;
    padding-bottom: 6px;
    color: #facc15;
    font-family: 'Cinzel', serif;
    font-size: 16px;
    border-bottom: 2px solid #d97706;
    font-weight: 700;
}}

.teams-flex-container {{
    display: flex;
    flex-wrap: nowrap;
    gap: 10px;
    overflow-x: auto;
    padding-bottom: 10px;
    margin-bottom: 15px;
}}

.team-box {{
    flex: 0 0 145px;
    padding: 8px;
    border: 1px solid #475569;
    border-radius: 10px;
    background: #0f172a;
}}
.team-box h4 {{
    margin: 0 0 8px;
    padding-bottom: 4px;
    color: #93c5fd;
    text-align: center;
    font-family: 'Cinzel', serif;
    font-size: 12px;
    border-bottom: 1px solid #334155;
}}

.player {{
    min-height: 32px;
    margin: 4px 0;
    padding: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    background: var(--job-bg);
    color: var(--job-fg);
    font-size: 13px;
    font-weight: 700;
    text-align: center;
    word-break: break-word;
    border: 1px solid rgba(255, 255, 255, 0.15);
}}

.msg-box h4 {{
    margin: 0 0 8px;
    color: #facc15;
    font-family: 'Cinzel', serif;
    font-size: 13px;
    border-bottom: 1px solid #334155;
    padding-bottom: 6px;
}}
.msg-box p {{
    font-size: 13px;
    line-height: 1.4;
    margin: 0;
}}

@media (max-width: 1100px) {{
    .content-wrapper {{ flex-direction: column; }}
    .sidebar-area {{ width: 100%; position: static; }}
}}
</style>
</head>
<body>

<div class="container">
    <div class="banner-header">
        <div class="title-wrapper">
            <div class="header">RAGNAROK GUILD LEAGUE WAR</div>
        </div>
        <div class="subheader">Official Deployment & Strategy Dashboard Guild Lumiere</div>
        <div class="date-badge">📅 Jadwal War: {tanggal_war}</div>
    </div>

    <!-- SEARCH -->
    <div class="search-container">
        <h3>🔍 CEK POSISI PLAYER</h3>
        <div class="search-box-wrapper">
            <input type="text" id="searchInput" class="search-input" placeholder="Ketik nickname kamu..." onkeypress="if(event.key==='Enter')searchPlayer()">
            <button class="search-btn" onclick="searchPlayer()">CARI</button>
        </div>
        <div id="searchResult" class="search-result"></div>
    </div>

    <!-- TABS -->
    <div class="tab-menu">
        <button class="tab-btn active" onclick="openTab(event, 'main-tab')">⚔️ MAIN FIELD (60)</button>
        <button class="tab-btn" onclick="openTab(event, 'sub-tab')">🛡️ SUB FIELD (85)</button>
    </div>

    <!-- TAB 1: MAIN -->
    <div id="main-tab" class="tab-content active">
        <div class="content-wrapper">
            <div class="main-content-area">
                <div class="section-title">⚔️ PARTY RAID MAIN (TEAM 1 - 8)</div>
                <div class="teams-flex-container">
"""

# Render Team Main 1-8
main_cols = list(df_main.columns)
for i, col in enumerate(main_cols[:8]):
    if col in df_main.columns:
        header_name = f"TEAM {i + 1}"
        html_content += f'<div class="team-box"><h4>{header_name}</h4>'
        for val in df_main[col].dropna():
            p_name = str(val).strip()
            p_lower = p_name.lower().split("(")[0].strip()
            job = job_map.get(p_lower, "default")
            html_content += f'<div class="player" data-nick="{p_name.lower()}" style="--job-bg: {job_colors.get(job, job_colors["default"])}; --job-fg: {job_text_colors.get(job, job_text_colors["default"])};">{p_name}</div>'
        html_content += "</div>"

html_content += """
                </div>
                <div class="section-title">🛡️ CHAOS PARTY MAIN</div>
                <div class="teams-flex-container">
"""

for col in main_cols[8:]:
    if col in df_main.columns:
        team_title = col.upper()
        html_content += f'<div class="team-box"><h4>{team_title}</h4>'
        for val in df_main[col].dropna():
            p_name = str(val).strip()
            p_lower = p_name.lower().split("(")[0].strip()
            job = job_map.get(p_lower, "default")
            html_content += f'<div class="player" data-nick="{p_name.lower()}" style="--job-bg: {job_colors.get(job, job_colors["default"])}; --job-fg: {job_text_colors.get(job, job_text_colors["default"])};">{p_name}</div>'
        html_content += "</div>"

html_content += f"""
                </div>
            </div>

            <!-- SIDEBAR CATATAN -->
            <div class="sidebar-area">
                <div class="msg-box">
                    <h4>⚠️ CATATAN & INSTRUKSI</h4>
                    <p>
                        <b>📊 Info Umum (Total 60 Player):</b><br>
                        • Terbagi jadi 2 Party Raid & 4 Normal Party.<br>
                        • Prepare jam 20.45.<br><br>
                        <b>🎯 Tugas:</b><br>
                        • Team 1-4: Lane Mid<br>
                        • Team 5-6: Lane Top<br>
                        • Team 7-8: Lane Bottom<br>
                        • Chaos: Tim Rusuh / Backup.
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 2: SUB -->
    <div id="sub-tab" class="tab-content">
        <div class="section-title">🛡️ SUB FIELD (DAFTAR TEAM)</div>
        <div class="teams-flex-container">
"""

for i, col in enumerate(sub_cols[:8]):
    if col in df_sub.columns:
        header_name = f"TEAM {i + 1}"
        html_content += f'<div class="team-box"><h4>{header_name}</h4>'
        for val in df_sub[col].dropna():
            p_name = str(val).strip()
            p_lower = p_name.lower().split("(")[0].strip()
            job = job_map.get(p_lower, "default")
            html_content += f'<div class="player" data-nick="{p_name.lower()}" style="--job-bg: {job_colors.get(job, job_colors["default"])}; --job-fg: {job_text_colors.get(job, job_text_colors["default"])};">{p_name}</div>'
        html_content += "</div>"

html_content += """
        </div>
    </div>
</div>

<script>
function openTab(evt, tabName) {
    var i, tabcontent, tabbtns;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) { tabcontent[i].classList.remove("active"); }
    tabbtns = document.getElementsByClassName("tab-btn");
    for (i = 0; i < tabbtns.length; i++) { tabbtns[i].classList.remove("active"); }
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}

function searchPlayer() {
    var input = document.getElementById('searchInput').value.trim().toLowerCase();
    var resultDiv = document.getElementById('searchResult');
    if (!input) {
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = "⚠️ Ketik nickname dulu!";
        return;
    }
    var players = document.querySelectorAll('.player');
    var found = false;
    players.forEach(function(p) {
        if (p.getAttribute('data-nick').includes(input)) {
            found = true;
            p.scrollIntoView({ behavior: 'smooth', block: 'center' });
            p.style.boxShadow = '0 0 15px 4px #facc15';
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = "✅ Ditemukan: <b>" + p.innerText + "</b>";
        }
    });
    if (!found) {
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = "❌ Tidak ditemukan.";
    }
}
</script>
</body>
</html>
"""

st.components.v1.html(html_content, height=1400, scrolling=True)
