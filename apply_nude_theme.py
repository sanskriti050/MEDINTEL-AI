"""Apply a warm nude visual theme. Run once from the folder containing app.py."""
from pathlib import Path
from datetime import datetime
import re, shutil

ROOT = Path(__file__).resolve().parent
BACKUP = ROOT / ("before_nude_theme_" + datetime.now().strftime("%Y%m%d_%H%M%S"))

# Original UI colours -> warm ivory, terracotta, sage and cocoa palette.
PALETTE = {
    '#0B1220':'#F7EEE8', '#111827':'#F1E4DC', '#172033':'#FFF9F5',
    '#2B3648':'#DCCBC0', '#334155':'#C9B6AA', '#1e293b':'#E4D6CD',
    '#2563EB':'#B8664B', '#1D4ED8':'#914735', '#7C3AED':'#A56655',
    '#059669':'#71845E', '#0891B2':'#A56E55', '#D97706':'#B77A3B',
    '#DC2626':'#B94C46', '#16A34A':'#71845E', '#F59E0B':'#C38A3E',
    '#F87171':'#C96B62', '#FBBF24':'#C99A45', '#92400E':'#8F5A35',
    '#CBD5E1':'#4A3932', '#64748B':'#7A665D', '#94A3B8':'#806C63',
    '#475569':'#8C7266', '#60A5FA':'#A9573F', '#93C5FD':'#7B4A3D',
    '#6EE7B7':'#5F6F4F', '#34D399':'#5F7653', '#A78BFA':'#8C5143',
    '#C4B5FD':'#8C5143', '#D1FAE5':'#42533A', '#FCD34D':'#8B6228',
    '#bfdbfe':'#6B4539', '#e2e8f0':'#4A3932', '#fef3c7':'#634B2E',
    '#1E3A5F':'#F0DDD2', '#1e3a5f':'#F0DDD2', '#052E16':'#E4F0E1',
    '#052e16':'#E4F0E1', '#451A03':'#F4E4CF', '#451a03':'#F4E4CF',
    '#450A0A':'#F3D7D0', '#450a0a':'#F3D7D0', '#1c1207':'#F5E5D6',
    '#1c1a07':'#F5E5D6', '#0f1f3d':'#4A332B', '#1a2f5c':'#6B493B',
    '#0f2744':'#F1E1D8', '#4ADE80':'#71905E'
}
RGBA = {
    'rgba(37,99,235,0.3)':'rgba(184,102,75,0.25)',
    'rgba(5,150,105,0.3)':'rgba(113,132,94,0.25)',
    'rgba(124,58,237,0.3)':'rgba(165,102,85,0.25)',
    'rgba(37,99,235,0.15)':'rgba(184,102,75,0.12)',
    'rgba(124,58,237,0.1)':'rgba(165,102,85,0.10)',
    'rgba(37,99,235,0.08)':'rgba(184,102,75,0.08)',
    'rgba(37,99,235,0.06)':'rgba(184,102,75,0.07)',
    'rgba(74,222,128,0.07)':'rgba(113,144,94,0.09)',
}

# Keep all functionality and markup unchanged; only visual colour literals are adjusted.
files = [p for p in ROOT.rglob('*.py') if p.name != Path(__file__).name and '.venv' not in p.parts]
changed = []
for file in files:
    text = file.read_text(encoding='utf-8')
    new = text
    for old, fresh in RGBA.items():
        new = new.replace(old, fresh)
    for old, fresh in PALETTE.items():
        new = re.sub(re.escape(old), fresh, new, flags=re.IGNORECASE)
    # Light pages require dark readable inline text. Hero title is corrected immediately below.
    new = new.replace('color:white', 'color:#3E2D27').replace('color: white', 'color: #3E2D27')
    if new != text:
        saved = BACKUP / file.relative_to(ROOT)
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_text(text, encoding='utf-8')
        file.write_text(new, encoding='utf-8')
        changed.append(str(file.relative_to(ROOT)))

# Restore intentional light text only inside the dark home hero.
home = ROOT / 'pages' / 'home.py'
if home.exists():
    text = home.read_text(encoding='utf-8')
    text = text.replace('color: #3E2D27;\n            font-size: 2.8rem;', 'color: #FFF9F5;\n            font-size: 2.8rem;')
    home.write_text(text, encoding='utf-8')

# A reliable, accessible Streamlit shell: cream surfaces + cocoa text + terracotta actions.
styles = ROOT / 'styles.py'
if styles.exists() and not (BACKUP / 'styles.py').exists():
    (BACKUP / 'styles.py').write_text(styles.read_text(encoding='utf-8'), encoding='utf-8')
styles.write_text('''import streamlit as st

def load_css():
    st.markdown("""
    <style>
    .stApp { background: #F7EEE8; color: #3E2D27; }
    section[data-testid="stSidebar"] { background: #F1E4DC; border-right: 1px solid #DCCBC0; }
    section[data-testid="stSidebar"] * { color: #3E2D27; }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 { color: #3E2D27; }
    /* The home hero deliberately remains a dark cocoa panel with light text. */
    div[style*="linear-gradient"] h1 { color: #FFF9F5 !important; }
    .stApp p, .stApp label, .stApp span { color: #4A3932; }
    div[data-testid="stMetric"], div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFF9F5; border: 1px solid #DCCBC0; border-radius: 16px;
    }
    div[data-testid="stMetric"] { padding: 12px; }
    div[data-testid="stVerticalBlockBorderWrapper"] { padding: 15px; }
    .stButton > button { background: #B8664B; color: #FFF9F5; border: none; border-radius: 10px; font-weight: 600; height: 48px; }
    .stButton > button:hover { background: #914735; color: #FFF9F5; }
    div[data-baseweb="select"] > div, .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background: #FFF9F5 !important; color: #3E2D27 !important; border-color: #DCCBC0 !important;
    }
    .stAlert { background: #F5E5D6; color: #3E2D27; border-color: #DCCBC0; }
    hr { border-color: #DCCBC0; }
    </style>
    """, unsafe_allow_html=True)
''', encoding='utf-8')
if 'styles.py' not in changed: changed.append('styles.py')

print('Warm nude theme applied successfully.')
print('Updated colour-only files: ' + ', '.join(changed))
print('Your original files were backed up in: ' + BACKUP.name)
