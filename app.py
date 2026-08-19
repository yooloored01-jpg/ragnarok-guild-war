import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# --- DATA LOADING ---
@st.cache_data
def load_data():
    sheet_id = "1a__PWfdLc5XLcstIiexAtboh1iiKdCqtTxVzQ_8Jf6E"
    urls = {
        "main": f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Main",
        "sub": f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sub",
        "job": f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Data"
    }
    return pd.read_csv(urls["main"]), pd.read_csv(urls["sub"]), pd.read_csv(urls["job"])

df_main, df_sub, df_job = load_data()
tanggal_war = "Jumat, 18 Agustus 2026"

# Mapping Data
job_map = {str(r[0]).strip().lower(): str(r[1]).strip().lower() for _, r in df_job.iterrows() if pd.notna(r[0])}
job_colors = {"priest": "#0f5132", "swordman": "#842029", "wizard": "#084298", "hunter": "#664d03", "blacksmith": "#7b341e", "thief": "#432874", "gunner": "#53382c", "druid": "#40E0D0", "default": "#1e293b"}
job_text_colors = {"priest": "#d1e7dd", "swordman": "#f8d7da", "wizard": "#cfe2ff", "druid": "#212121", "hunter": "#fff3cd", "blacksmith": "#f8d7da", "thief": "#e2d9f3", "gunner": "#f8d7da", "default": "#f1f5f9"}

# --- FUNGSI RENDER HTML ---
def get_player_html(val):
    p_name = str(val).strip()
    p_lower = p_name.lower().split("(")[0].strip()
    job = job_map.get(p_lower, "default")
    return f'<div class="player" data-nick="{p_name.lower()}" style="--job-bg: {job_colors.get(job)}; --job-fg: {job_text_colors.get(job)};">{p_name}</div>'

# (Di sini Anda masukkan isi string HTML panjang Anda)
# INGAT: Pastikan isi script.js Anda ditaruh di dalam tag <script> di bagian bawah file ini.
html = f"""
<!DOCTYPE html>
<html>
<head>
    <style> /* Masukkan CSS Anda di sini */ </style>
</head>
<body>
    <!-- Masukkan seluruh struktur div/header Anda di sini -->
    
    <script>
        // Masukkan seluruh fungsi JavaScript Anda di sini (seperti toggleScreenshotMode, searchPlayer, dll)
    </script>
</body>
</html>
"""

# TAMPILKAN DI STREAMLIT
components.html(html, height=1200, scrolling=True)
