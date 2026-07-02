import streamlit as st
import os
import sqlite3
import pandas as pd
from utils.loader import get_db_connection, load_players, load_matches
from utils.helpers import section_header

section_header("Dashboard Settings", "Manage analyst configuration, databases, and CSV telemetry exports")

# Establish connection
conn = get_db_connection()
cursor = conn.cursor()

# --- LOAD SETTINGS FROM SQLITE ---
def get_setting(key, default):
    cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
    row = cursor.fetchone()
    return row[0] if row else default

def save_setting(key, value):
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
    conn.commit()

# Current settings
theme_sel = get_setting("theme", "Navy Blue (CSK Standard)")
refresh_rate = int(get_setting("refresh_rate", "5"))
notif_enable = get_setting("notifications", "Enabled") == "Enabled"

# --- DISPLAY CONTROLS ---
st.markdown("""
<div class="chart-wrap">
    <div class="chart-title">⚙️ Preferences Dashboard</div>
    <div class="chart-subtitle">System preferences stored in local SQLite settings database</div>
""", unsafe_allow_html=True)

theme_options = ["Navy Blue (CSK Standard)", "Carbon Dark Theme", "Vibrant Yellow Mode"]
new_theme = st.selectbox("Select Visual Theme", theme_options, index=theme_options.index(theme_sel))

new_refresh = st.number_input("Telemetry Refresh Interval (seconds)", min_value=1, max_value=60, value=refresh_rate)

new_notif = st.checkbox("Enable Coach Strategy Notifications", value=notif_enable)

if st.button("💾 Save System Preferences", use_container_width=True):
    save_setting("theme", new_theme)
    save_setting("refresh_rate", new_refresh)
    save_setting("notifications", "Enabled" if new_notif else "Disabled")
    st.success("Preferences successfully saved to SQLite database!")

st.markdown("</div>", unsafe_allow_html=True)

# --- EXPORT DATA SECTION ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="chart-wrap">
    <div class="chart-title">📥 Export System Datasets</div>
    <div class="chart-subtitle">Download matches and player files directly in Excel format</div>
""", unsafe_allow_html=True)

col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    st.markdown("**CSK Squad Dataset (players.csv)**")
    if st.button("Generate players.xlsx Export", use_container_width=True):
        try:
            df_players = load_players()
            xlsx_path = "database/players_export.xlsx"
            df_players.to_excel(xlsx_path, index=False)
            st.success("Generated players_export.xlsx in database folder!")
            
            with open(xlsx_path, "rb") as f:
                st.download_button(
                    label="📥 Download players.xlsx",
                    data=f,
                    file_name="players_export.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"Error exporting players: {e}")

with col_exp2:
    st.markdown("**CSK Matches History (matches.csv)**")
    if st.button("Generate matches.xlsx Export", use_container_width=True):
        try:
            df_matches = load_matches()
            xlsx_path = "database/matches_export.xlsx"
            df_matches.to_excel(xlsx_path, index=False)
            st.success("Generated matches_export.xlsx in database folder!")
            
            with open(xlsx_path, "rb") as f:
                st.download_button(
                    label="📥 Download matches.xlsx",
                    data=f,
                    file_name="matches_export.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"Error exporting matches: {e}")

st.markdown("</div>", unsafe_allow_html=True)

# --- BACKUP DATABASE SECTION ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="chart-wrap" style="border-color: rgba(245, 158, 11, 0.25);">
    <div class="chart-title" style="color: #F59E0B;">💾 Backup Database Center</div>
    <div class="chart-subtitle">Create copies of configuration and log databases</div>
""", unsafe_allow_html=True)

if st.button("Create SQL Database Backup", use_container_width=True):
    try:
        # Copy settings.db to settings_backup.db
        src_path = "database/settings.db"
        dst_path = "database/settings_backup.db"
        
        if os.path.exists(src_path):
            import shutil
            shutil.copy2(src_path, dst_path)
            st.success("Backup successfully created at database/settings_backup.db!")
        else:
            st.warning("Settings database not initialized yet. Save preferences first to initialize.")
    except Exception as e:
        st.error(f"Backup failed: {e}")

st.markdown("</div>", unsafe_allow_html=True)
conn.close()
