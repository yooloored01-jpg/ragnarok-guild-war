import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Set Layout
st.set_page_config(layout="wide")

# 1. Load Data dari Google Sheets (Public)
@st.cache_data
def load_data():
    sheet_id = "1a__PWfdLc5XLcstIiexAtboh1iiKdCqtTxVzQ_8Jf6E"
    # Format URL untuk membaca CSV dari Google Sheets
    urls = {
        "main": f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Main",
        "sub": f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sub",
        "job": f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Data"
    }
    return pd.read_csv(urls["main"]), pd.read_csv(urls["sub"]), pd.read_csv(urls["job"])

# Ambil data
df_main, df_sub, df_job = load_data()
tanggal_war = "Jumat, 18 Agustus 2026"

# Mapping Job
job_map = {str(row.iloc[0]).strip().lower(): str(row.iloc[1]).strip().lower() 
           for _, row in df_job.iterrows() if pd.notna(row.iloc[0])}

job_colors = {"priest": "#0f5132", "swordman": "#842029", "wizard": "#084298", 
              "hunter": "#664d03", "blacksmith": "#7b341e", "thief": "#432874", 
              "gunner": "#53382c", "druid": "#40E0D0", "default": "#1e293b"}
job_text_colors = {"priest": "#d1e7dd", "swordman": "#f8d7da", "wizard": "#cfe2ff", 
                   "druid": "#212121", "hunter": "#fff3cd", "blacksmith": "#f8d7da", 
                   "thief": "#e2d9f3", "gunner": "#f8d7da", "default": "#f1f5f9"}

# 2. Fungsi Helper untuk HTML
def generate_players_html(df, cols):
    html_out = ""
    for col in cols:
        if col in df.columns:
            values = df[col].dropna()
            for val in values:
                p_name = str(val).strip()
                p_lower = p_name.lower().split("(")[0].strip()
                job = job_map.get(p_lower, "default")
                bg = job_colors.get(job, job_colors["default"])
                fg = job_text_colors.get(job, job_text_colors["default"])
                html_out += f'<div class="player" data-nick="{p_name.lower()}" style="--job-bg: {bg}; --job-fg: {fg};">{p_name}</div>'
    return html_out

# 3. Gabungkan semua HTML/JS/CSS ke dalam variabel
# (Struktur ini mempertahankan kode Anda, hanya mengganti cara baca datanya)
html_template = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    /* CSS ANDA TETAP SAMA - PASTE DI SINI */
    body {{ background: #0f172a; color: white; font-family: sans-serif; }}
    .tab-content {{ display: none; }}
    .tab-content.active {{ display: block; }}
    .player {{ padding: 5px; margin: 2px; border-radius: 4px; background: var(--job-bg); color: var(--job-fg); font-size: 12px; }}
</style>
</head>
<body>
    <div class="tab-menu">
        <button class="tab-btn active" onclick="openTab(event, 'main-tab')">⚔️ MAIN FIELD</button>
        <button class="tab-btn" onclick="openTab(event, 'sub-tab')">🛡️ SUB FIELD</button>
    </div>

    <div id="main-tab" class="tab-content active">
        <!-- Contoh Render Data Main -->
        <div class="teams-flex-container">
            {generate_players_html(df_main, df_main.columns[:8])}
        </div>
    </div>

    <div id="sub-tab" class="tab-content">
        <div class="teams-flex-container">
            {generate_players_html(df_sub, df_sub.columns[:8])}
        </div>
    </div>

    <script>
        function openTab(evt, tabName) {{
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
        }}
        // TAMBAHKAN FUNGSI SEARCH ANDA DI SINI
    </script>
</body>
</html>
"""

# 4. Tampilkan
components.html(html_template, height=1500, scrolling=True)
