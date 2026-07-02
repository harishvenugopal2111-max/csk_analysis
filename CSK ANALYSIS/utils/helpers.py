import os
import streamlit as st

def inject_css():
    """Reads the custom style.css and injects it into the Streamlit app."""
    css_path = os.path.join(os.path.dirname(__file__), "../assets/css/style.css")
    try:
        with open(css_path, "r") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Could not load custom styles: {e}")

def metric_card(label, value, delta=None, delta_type="up", is_yellow=False):
    """
    Renders a custom HTML metric card with premium glassmorphism.
    delta_type can be 'up', 'down', or 'warn'
    """
    cls = f"delta-{delta_type}"
    arrow = "↑" if delta_type == "up" else ("↓" if delta_type == "down" else "→")
    delta_html = f'<div class="metric-delta {cls}">{arrow} {delta}</div>' if delta else ""
    val_class = "metric-value-yellow" if is_yellow else ""
    
    card_html = f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value {val_class}">{value}</div>
        {delta_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def status_badge(label, level="blue"):
    """
    Returns the HTML string for a custom status badge.
    level can be 'green' (Excellent), 'blue' (Good), 'amber' (Average), 'red' (Poor), 'yellow'
    """
    level_lower = level.lower()
    if level_lower in ["excellent", "green", "fit"]:
        badge_class = "badge-green"
    elif level_lower in ["good", "blue", "rehab"]:
        badge_class = "badge-blue"
    elif level_lower in ["average", "amber", "rest"]:
        badge_class = "badge-amber"
    elif level_lower in ["poor", "red"]:
        badge_class = "badge-red"
    elif level_lower in ["yellow", "csk"]:
        badge_class = "badge-yellow"
    else:
        badge_class = "badge-blue"
        
    return f'<span class="badge {badge_class}">{label}</span>'

def section_header(title, subtitle=None):
    """Renders a styled section header with yellow border indicator."""
    sub_html = f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="section-header animate-fade-in">
        <div class="section-title">{title}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)

def render_player_card(player, role, age, nat, exp, runs, wkts, sr, econ, catches, fitness, form_score, form_label):
    """Generates the HTML string representing a premium player profile card UI."""
    nat_badge = status_badge("OS", "yellow") if nat == "Overseas" else status_badge("IND", "blue")
    fit_badge = status_badge(fitness, "green" if fitness == "Fit" else ("amber" if fitness == "Rest" else "blue"))
    form_badge = status_badge(form_label, "green" if form_label == "Excellent" else ("blue" if form_label == "Good" else ("amber" if form_label == "Average" else "red")))
    
    card_html = f"""
    <div class="player-card animate-fade-in">
        <div class="player-card-header">
            <div>
                <h4 class="player-card-name">{player}</h4>
                <div class="player-card-role">{role} ({age} yrs)</div>
            </div>
            <div style="display: flex; gap: 4px; align-items: center;">
                {nat_badge}
            </div>
        </div>
        <div class="player-card-stat-grid">
            <div class="player-card-stat-box">
                <div class="player-card-stat-val">{runs}</div>
                <div class="player-card-stat-lbl">Runs</div>
            </div>
            <div class="player-card-stat-box">
                <div class="player-card-stat-val">{wkts}</div>
                <div class="player-card-stat-lbl">Wickets</div>
            </div>
            <div class="player-card-stat-box">
                <div class="player-card-stat-val">{catches}</div>
                <div class="player-card-stat-lbl">Ctch</div>
            </div>
            <div class="player-card-stat-box">
                <div class="player-card-stat-val">{sr if sr > 0 else '-'}</div>
                <div class="player-card-stat-lbl">S/R</div>
            </div>
            <div class="player-card-stat-box">
                <div class="player-card-stat-val">{econ if econ > 0 else '-'}</div>
                <div class="player-card-stat-lbl">Econ</div>
            </div>
            <div class="player-card-stat-box">
                <div class="player-card-stat-val">{exp}</div>
                <div class="player-card-stat-lbl">Exp</div>
            </div>
        </div>
        <div class="player-card-footer" style="margin-top: 10px;">
            <div>Fit: {fit_badge}</div>
            <div>Form: {form_badge}</div>
        </div>
    </div>
    """
    return card_html

def render_retention_card(name, role, retention_score, label, reason, salary):
    """Generates the HTML string representing a release/retention dashboard panel."""
    # Determine visual category
    if label == "RETAIN":
        card_class = "retention-card retention-green"
        lbl_badge = status_badge("RETAIN (GREEN)", "green")
    elif label == "UNDER REVIEW":
        card_class = "retention-card retention-yellow"
        lbl_badge = status_badge("REVIEW (YELLOW)", "amber")
    else:
        card_class = "retention-card retention-red"
        lbl_badge = status_badge("RELEASE (RED)", "red")
        
    return f"""
    <div class="{card_class} animate-fade-in">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <div>
                <strong style="font-size: 1.05rem; color: var(--text);">{name}</strong>
                <span style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase; margin-left: 10px;">{role}</span>
            </div>
            <div>{lbl_badge}</div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem; margin-bottom: 0.5rem; color: var(--text-muted);">
            <div>Retention Score: <strong style="color: #FFD305; font-size: 0.95rem;">{retention_score}</strong></div>
            <div>Salary Space: <strong style="color: var(--text);">{salary} Cr</strong></div>
        </div>
        <div style="font-size: 0.78rem; color: #9CA3AF; line-height: 1.35; padding: 0.5rem; background: rgba(0,0,0,0.15); border-radius: 6px; border: 1px solid rgba(255,255,255,0.03);">
            <strong>Reasoning:</strong> {reason}
        </div>
    </div>
    """

def render_rating_indicator(label, value_out_of_100, color="#FFD305"):
    """Generates the HTML string representing a horizontal strength slider/progress bar."""
    return f"""
    <div style="margin-bottom: 0.8rem;" class="animate-fade-in">
        <div style="display: flex; justify-content: space-between; font-size: 0.78rem; margin-bottom: 3px; color: var(--text-muted);">
            <span>{label}</span><span style="color: {color}; font-weight: 700;">{value_out_of_100}%</span>
        </div>
        <div style="background: rgba(255,255,255,0.05); height: 6px; border-radius: 3px;">
            <div style="background: {color}; width: {value_out_of_100}%; height: 100%; border-radius: 3px;"></div>
        </div>
    </div>
    """

def custom_table(df, columns_map=None, formats=None):
    """Renders a custom styled HTML table from a pandas DataFrame."""
    if df.empty:
        st.markdown("<p style='color: var(--text-muted); font-style: italic;'>No data available.</p>", unsafe_allow_html=True)
        return
        
    if columns_map:
        df_display = df[list(columns_map.keys())].rename(columns=columns_map)
    else:
        df_display = df.copy()
        
    headers_html = "".join([f"<th>{col}</th>" for col in df_display.columns])
    
    rows_html = ""
    for idx, row in df_display.iterrows():
        row_cells = ""
        for i, val in enumerate(row):
            formatted_val = val
            if formats and df_display.columns[i] in formats:
                formatted_val = formats[df_display.columns[i]](val)
            row_cells += f"<td>{formatted_val}</td>"
        rows_html += f"<tr>{row_cells}</tr>"
        
    table_html = f"""
    <table class="data-table animate-fade-in">
        <thead>
            <tr>{headers_html}</tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)
