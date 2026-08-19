import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 1. Load Data
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

# 2. Gabungkan semuanya ke dalam satu variabel "html_content"
# Paste seluruh kode HTML, CSS, dan JS Anda di dalam sini:
html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        /* PASTE CSS ANDA DI SINI */
    </style>
</head>
<body>
    
    <!-- PASTE STRUKTUR HTML ANDA DI SINI -->

    <script>
        /* PASTE JAVASCRIPT ANDA DI SINI */
    </script>
</body>
</html>
"""

# 3. Render ke Streamlit
st.set_page_config(layout="wide")
components.html(html_content, height=2000, scrolling=True)
