import streamlit as st
from PIL import Image, ImageFilter, ImageStat
import io
import os
import hashlib
import struct
import math
import random
import numpy as np

st.set_page_config(page_title="LSB Stealth — Kelompok 4", layout="wide", page_icon="🔐")

# ─────────────────────────────────────────────
#  STYLE
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg: #06060a;
    --surface: #0e0e16;
    --surface2: #14141f;
    --border: rgba(255,255,255,0.07);
    --text: #f0f0f8;
    --muted: #6b6b80;
    --purple: #7c6af7;
    --purple-soft: rgba(124,106,247,0.15);
    --green: #10b981;
    --red: #ef4444;
    --amber: #f59e0b;
    --cyan: #38bdf8;
}

html, body, .stApp { background: var(--bg) !important; font-family: 'Instrument Sans', sans-serif; color: var(--text); }
header, footer, #MainMenu { visibility: hidden !important; }
.block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
section[data-testid="stMain"] > div { padding: 0 !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stAppViewBlockContainer"] { padding: 0 !important; max-width: 100% !important; }
div[data-testid="stVerticalBlockBorderWrapper"] { padding: 0 !important; }
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }

/* BG ORBS */
.bg-orbs { position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden; }
.orb { position:absolute;border-radius:50%;filter:blur(90px);animation:orbFloat ease-in-out infinite; }
.orb-1 { width:600px;height:600px;background:radial-gradient(circle,rgba(124,106,247,0.16) 0%,transparent 70%);top:-200px;left:-100px;animation-duration:10s; }
.orb-2 { width:500px;height:500px;background:radial-gradient(circle,rgba(192,132,252,0.12) 0%,transparent 70%);top:-100px;right:-150px;animation-duration:13s;animation-delay:-3s; }
.orb-3 { width:400px;height:400px;background:radial-gradient(circle,rgba(56,189,248,0.09) 0%,transparent 70%);bottom:20%;left:30%;animation-duration:15s;animation-delay:-6s; }
@keyframes orbFloat { 0%,100%{transform:translateY(0) scale(1);} 33%{transform:translateY(-30px) scale(1.05);} 66%{transform:translateY(20px) scale(0.97);} }
@keyframes fadeUp { from{opacity:0;transform:translateY(18px);} to{opacity:1;transform:translateY(0);} }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.3;} }

/* PAGE */
.page { position:relative;z-index:2;width:100%;max-width:900px;margin:0 auto;padding:0 32px 80px; }

/* HERO */
.hero { padding:80px 0 44px;text-align:center; }
.hero-pill { display:inline-flex;align-items:center;gap:8px;background:rgba(124,106,247,0.12);border:1px solid rgba(124,106,247,0.25);border-radius:100px;padding:8px 20px;font-size:0.75rem;font-weight:500;color:#a89bf8;margin-bottom:28px;animation:fadeUp 0.5s ease both; }
.pill-dot { width:6px;height:6px;background:var(--purple);border-radius:50%;box-shadow:0 0 10px var(--purple);animation:pulse 2s infinite; }
.hero-title { font-size:clamp(2.4rem,5vw,4.2rem);font-weight:700;line-height:1.05;letter-spacing:-2px;color:#fff;margin-bottom:16px;animation:fadeUp 0.5s 0.1s ease both; }
.grad { background:linear-gradient(135deg,#7c6af7 0%,#c084fc 50%,#38bdf8 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text; }
.grad-green { background:linear-gradient(135deg,#10b981,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text; }
.hero-sub { font-size:clamp(0.88rem,1.8vw,1rem);color:var(--muted);max-width:520px;margin:0 auto 20px;line-height:1.8;animation:fadeUp 0.5s 0.2s ease both;display:block;text-align:center !important; }
.hero-badges { display:flex;align-items:center;justify-content:center;gap:10px;margin:0 auto 44px;flex-wrap:wrap;animation:fadeUp 0.5s 0.25s ease both; }
.badge { display:inline-flex;align-items:center;gap:8px;padding:9px 18px;border-radius:10px;font-family:'JetBrains Mono',monospace;font-size:0.75rem;font-weight:500; }
.badge-main { background:linear-gradient(135deg,rgba(124,106,247,0.18),rgba(192,132,252,0.12));border:1px solid rgba(124,106,247,0.4);color:#c4b8ff;box-shadow:0 0 20px rgba(124,106,247,0.12); }
.badge-sec { background:rgba(255,255,255,0.04);border:1px solid var(--border);color:var(--muted); }
.badge-green { background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);color:#6ee7b7; }
.badge-dot { width:7px;height:7px;border-radius:50%; }
.dot-purple { background:var(--purple);box-shadow:0 0 8px var(--purple); }
.dot-green { background:var(--green);box-shadow:0 0 8px var(--green); }
.dot-cyan { background:var(--cyan);box-shadow:0 0 8px var(--cyan); }

/* STATS ROW */
.stats-row { display:flex;justify-content:center;flex-wrap:wrap;gap:1px;background:var(--border);border:1px solid var(--border);border-radius:16px;overflow:hidden;width:fit-content;margin:0 auto 52px;animation:fadeUp 0.5s 0.3s ease both; }
.stat { background:var(--surface);padding:15px 28px;text-align:center;transition:background 0.2s; }
.stat:hover { background:#1a1a28; }
.stat-val { font-size:1.3rem;font-weight:700;background:linear-gradient(135deg,#7c6af7,#c084fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1; }
.stat-lbl { font-size:0.63rem;color:var(--muted);margin-top:4px;letter-spacing:0.5px; }

/* TABS */
.stTabs [data-baseweb="tab-list"] { background:var(--surface) !important;border-radius:14px !important;padding:5px !important;gap:4px !important;border:1px solid var(--border) !important;width:fit-content !important;margin:0 auto !important;display:flex !important;justify-content:center !important;flex-wrap:wrap !important; }
.stTabs [data-baseweb="tab"] { background:transparent !important;border-radius:10px !important;color:var(--muted) !important;font-family:'Instrument Sans',sans-serif !important;font-weight:500 !important;font-size:0.82rem !important;padding:9px 20px !important;border:none !important;height:auto !important; }
.stTabs [data-baseweb="tab"]:hover { color:#d0d0e8 !important; }
.stTabs [aria-selected="true"] { background:linear-gradient(135deg,rgba(124,106,247,0.2),rgba(192,132,252,0.15)) !important;color:#fff !important;border:1px solid rgba(124,106,247,0.3) !important;box-shadow:0 2px 16px rgba(124,106,247,0.15) !important; }
.stTabs [data-baseweb="tab-highlight"] { display:none !important; }

/* FEATURE STRIP */
.feature-strip { display:block;width:100%;text-align:center;padding:36px 0 0;margin-bottom:32px; }
.feature-label { display:block;font-family:'JetBrains Mono',monospace;font-size:0.65rem;letter-spacing:3px;text-transform:uppercase;color:rgba(124,106,247,0.5);margin-bottom:10px; }
.feature-title { display:block;font-size:clamp(1.7rem,3.8vw,2.5rem);font-weight:700;color:#fff;letter-spacing:-1px;margin-bottom:12px;line-height:1.1; }
.feature-desc { display:block;font-size:0.88rem;color:var(--muted);max-width:480px;margin:0 auto 24px;line-height:1.75; }
.steps-row { display:flex;justify-content:center;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:20px; }
.step-pill { display:inline-flex;align-items:center;gap:10px;background:var(--surface);border:1px solid var(--border);border-radius:100px;padding:9px 16px;font-size:0.82rem;color:#8080a0;transition:all 0.2s;cursor:default; }
.step-pill:hover { border-color:rgba(124,106,247,0.35);color:#c0c0e0;transform:translateY(-2px); }
.step-num { width:22px;height:22px;min-width:22px;background:rgba(124,106,247,0.15);border:1px solid rgba(124,106,247,0.3);border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#a89bf8;font-weight:700; }
.tags-row { display:flex;justify-content:center;flex-wrap:wrap;gap:8px;margin-bottom:28px; }
.tag { background:rgba(124,106,247,0.08);border:1px solid rgba(124,106,247,0.2);border-radius:8px;padding:5px 12px;font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#a89bf8;letter-spacing:1px; }
.tag-green { background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);color:#6ee7b7; }
.tag-red { background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.2);color:#fca5a5; }

/* FORM CARD */
.form-card { background:var(--surface);border:1px solid var(--border);border-radius:24px;padding:36px 40px;position:relative;overflow:hidden;margin-bottom:8px; }
.form-card::before { content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(124,106,247,0.6) 30%,rgba(192,132,252,0.6) 70%,transparent); }
.form-card-red::before { background:linear-gradient(90deg,transparent,rgba(239,68,68,0.6) 30%,rgba(251,113,133,0.4) 70%,transparent); }
.form-card-green::before { background:linear-gradient(90deg,transparent,rgba(16,185,129,0.6) 30%,rgba(52,211,153,0.4) 70%,transparent); }

.sec-title { font-size:0.72rem;font-weight:600;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase;margin-bottom:16px;display:flex;align-items:center;gap:10px; }
.sec-title::after { content:'';flex:1;height:1px;background:var(--border); }

/* META */
.meta-box { background:var(--bg);border:1px solid var(--border);border-radius:14px;overflow:hidden;margin-top:8px; }
.meta-row { display:flex;justify-content:space-between;align-items:center;padding:11px 18px;border-bottom:1px solid var(--border); }
.meta-row:last-child { border-bottom:none; }
.meta-key { font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:var(--muted);letter-spacing:1px; }
.meta-val { font-family:'JetBrains Mono',monospace;font-size:0.85rem;font-weight:500;color:#a89bf8; }

/* CAP BAR */
.cap-wrap { margin:20px 0; }
.cap-header { display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:var(--muted);margin-bottom:8px; }
.cap-track { height:4px;background:rgba(255,255,255,0.05);border-radius:100px;overflow:hidden; }
.cap-fill { height:100%;border-radius:100px;transition:width 0.5s ease; }

/* FILE UPLOADER */
.stFileUploader section { background:var(--bg) !important;border:1.5px dashed rgba(124,106,247,0.25) !important;border-radius:16px !important;padding:28px !important;transition:all 0.2s !important; }
.stFileUploader section:hover { border-color:rgba(124,106,247,0.5) !important;background:rgba(124,106,247,0.03) !important; }
.stFileUploader section p,.stFileUploader section span { color:var(--muted) !important;font-family:'Instrument Sans',sans-serif !important; }
/* ── FIX: duplicate/stacked "upload" text in Streamlit file uploader ── */
/* Hide the drag-and-drop instruction text, keep only the browse button */
[data-testid="stFileUploaderDropzoneInstructions"] { display:none !important; }
/* Re-show the browse button which is inside the dropzone */
[data-testid="stFileUploaderDropzone"] button { display:inline-flex !important; }
/* Spacing fix so the button is centered */
[data-testid="stFileUploaderDropzone"] { display:flex !important; flex-direction:column !important; align-items:center !important; justify-content:center !important; gap:10px !important; min-height:80px !important; }

/* INPUTS */
.stTextArea textarea { background:var(--bg) !important;border:1.5px solid var(--border) !important;border-radius:14px !important;color:var(--text) !important;font-family:'Instrument Sans',sans-serif !important;font-size:0.95rem !important;padding:16px 18px !important;transition:border-color 0.2s !important; }
.stTextArea textarea:focus { border-color:rgba(124,106,247,0.5) !important;box-shadow:0 0 0 3px rgba(124,106,247,0.08) !important; }
.stTextArea textarea::placeholder { color:rgba(107,107,128,0.4) !important; }
.stTextArea label,.stFileUploader label { color:var(--muted) !important;font-family:'Instrument Sans',sans-serif !important;font-weight:600 !important;font-size:0.78rem !important;letter-spacing:0.5px !important; }
.stTextInput input { background:var(--bg) !important;border:1.5px solid var(--border) !important;border-radius:12px !important;color:var(--text) !important;font-family:'JetBrains Mono',monospace !important;font-size:0.9rem !important;padding:12px 16px !important;transition:border-color 0.2s !important; }
.stTextInput input:focus { border-color:rgba(124,106,247,0.5) !important;box-shadow:0 0 0 3px rgba(124,106,247,0.08) !important; }
.stTextInput label { color:var(--muted) !important;font-family:'Instrument Sans',sans-serif !important;font-weight:600 !important;font-size:0.78rem !important;letter-spacing:0.5px !important; }
.stCheckbox label span { color:var(--muted) !important;font-family:'Instrument Sans',sans-serif !important;font-size:0.88rem !important; }

/* BUTTONS */
.stButton > button { width:100% !important;background:linear-gradient(135deg,#7c6af7,#a855f7) !important;color:#fff !important;border:none !important;padding:15px 32px !important;border-radius:12px !important;font-family:'Instrument Sans',sans-serif !important;font-weight:600 !important;font-size:0.9rem !important;box-shadow:0 4px 24px rgba(124,106,247,0.3) !important;margin-top:10px !important;transition:all 0.25s ease !important; }
.stButton > button:hover { box-shadow:0 8px 32px rgba(124,106,247,0.45) !important;transform:translateY(-2px) !important; }
.stDownloadButton > button { width:100% !important;background:transparent !important;color:#a89bf8 !important;border:1px solid rgba(124,106,247,0.35) !important;padding:14px 32px !important;border-radius:12px !important;font-family:'Instrument Sans',sans-serif !important;font-weight:600 !important;font-size:0.9rem !important;margin-top:8px !important;transition:all 0.2s !important; }
.stDownloadButton > button:hover { background:rgba(124,106,247,0.1) !important;border-color:rgba(124,106,247,0.6) !important; }

/* ALERTS */
.stSuccess > div { background:rgba(16,185,129,0.08) !important;border:1px solid rgba(16,185,129,0.2) !important;border-radius:12px !important;color:#6ee7b7 !important; }
.stError > div { background:rgba(239,68,68,0.07) !important;border:1px solid rgba(239,68,68,0.2) !important;border-radius:12px !important;color:#fca5a5 !important; }
.stInfo > div { background:rgba(124,106,247,0.07) !important;border:1px solid rgba(124,106,247,0.2) !important;border-radius:12px !important;color:#c4b8ff !important; }
.stWarning > div { background:rgba(245,158,11,0.07) !important;border:1px solid rgba(245,158,11,0.2) !important;border-radius:12px !important;color:#fcd34d !important; }
.stImage > img { border-radius:14px !important;border:1px solid var(--border) !important; }

/* RESULT BOXES */
.result-box { background:var(--bg);border:1px solid var(--border);border-radius:14px;padding:22px 24px;font-family:'JetBrains Mono',monospace;font-size:0.85rem;color:#a89bf8;line-height:1.9;word-break:break-all;margin-top:12px; }
.result-box-red { background:rgba(239,68,68,0.04);border:1px solid rgba(239,68,68,0.2);color:#fca5a5; }
.result-box-green { background:rgba(16,185,129,0.04);border:1px solid rgba(16,185,129,0.2);color:#6ee7b7; }

/* HOW GRID */
.how-grid { display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:24px 0; }
.how-card { background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:26px 22px;transition:border-color 0.2s,transform 0.2s;position:relative;overflow:hidden; }
.how-card:hover { border-color:rgba(124,106,247,0.3);transform:translateY(-3px); }
.how-card::before { content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(124,106,247,0.4),transparent);opacity:0;transition:opacity 0.3s; }
.how-card:hover::before { opacity:1; }
.how-num { font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:rgba(124,106,247,0.4);letter-spacing:3px;margin-bottom:14px; }
.how-icon { font-size:1.6rem;margin-bottom:12px; }
.how-title { font-size:0.95rem;font-weight:700;color:#fff;margin-bottom:8px; }
.how-desc { font-size:0.8rem;color:var(--muted);line-height:1.7; }

/* BIT DEMO */
.bit-demo { background:#030308;border:1px solid var(--border);border-radius:18px;padding:28px 32px;margin:20px 0;font-family:'JetBrains Mono',monospace; }
.bit-demo-label { font-size:0.62rem;letter-spacing:2px;color:var(--muted);text-transform:uppercase;margin-bottom:22px; }
.bit-grid { display:grid;grid-template-columns:1fr 1fr;gap:32px; }
.bit-col-title { font-size:0.62rem;letter-spacing:2px;color:rgba(107,107,128,0.5);text-transform:uppercase;margin-bottom:14px; }
.bit-row { font-size:0.82rem;color:#3a3a55;line-height:2.4; }
.bit-body { color:#4a4a70; }
.lsb-old { color:#f87171;font-weight:700; }
.lsb-new { color:#7c6af7;font-weight:700; }
.bit-note { margin-top:18px;padding-top:14px;border-top:1px solid var(--border);font-size:0.72rem;color:var(--muted); }

/* ATTACK/DEFENSE CARDS */
.vuln-grid { display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:20px 0; }
.vuln-card { background:rgba(239,68,68,0.04);border:1px solid rgba(239,68,68,0.15);border-radius:18px;padding:22px 20px; }
.vuln-card-title { font-size:0.82rem;font-weight:700;color:#f87171;margin-bottom:10px;display:flex;align-items:center;gap:8px; }
.vuln-card-body { font-size:0.78rem;color:#8a5050;line-height:1.75; }
.mitig-card { background:rgba(16,185,129,0.04);border:1px solid rgba(16,185,129,0.18);border-radius:18px;padding:22px 20px; }
.mitig-card-title { font-size:0.82rem;font-weight:700;color:#6ee7b7;margin-bottom:10px;display:flex;align-items:center;gap:8px; }
.mitig-card-body { font-size:0.78rem;color:#3a7060;line-height:1.75; }

/* BEFORE/AFTER COMPARE */
.compare-wrap { display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border);border:1px solid var(--border);border-radius:18px;overflow:hidden;margin:20px 0; }
.compare-col { padding:22px 24px;background:var(--surface); }
.compare-title { font-family:'JetBrains Mono',monospace;font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:14px; }
.compare-title-bad { color:#f87171; }
.compare-title-good { color:#6ee7b7; }
.compare-item { display:flex;align-items:flex-start;gap:10px;font-size:0.8rem;color:var(--muted);margin-bottom:10px;line-height:1.6; }
.compare-icon-bad { color:#ef4444;font-size:0.9rem;margin-top:1px;flex-shrink:0; }
.compare-icon-good { color:#10b981;font-size:0.9rem;margin-top:1px;flex-shrink:0; }

/* MISC */
.warn-box { background:rgba(245,158,11,0.04);border:1px solid rgba(245,158,11,0.15);border-left:3px solid rgba(245,158,11,0.6);border-radius:14px;padding:20px 24px;margin-top:20px; }
.warn-title { font-weight:700;color:#fbbf24;font-size:0.9rem;margin-bottom:10px; }
.warn-box ul { padding-left:18px;color:#8a7040;font-size:0.82rem;line-height:2; }
.info-box { background:rgba(124,106,247,0.05);border:1px solid rgba(124,106,247,0.15);border-left:3px solid rgba(124,106,247,0.5);border-radius:14px;padding:18px 22px;font-size:0.88rem;color:#8080a0;line-height:1.8;margin-bottom:24px; }
.info-box strong { color:#a89bf8; }
.success-box { background:rgba(16,185,129,0.05);border:1px solid rgba(16,185,129,0.2);border-left:3px solid rgba(16,185,129,0.5);border-radius:14px;padding:18px 22px;font-size:0.88rem;color:#3a7060;line-height:1.8;margin-bottom:24px; }
.success-box strong { color:#6ee7b7; }
.sdiv { border:none;border-top:1px solid var(--border);margin:26px 0; }
.footer { text-align:center;padding:48px 0 16px;font-size:0.72rem;color:#2a2a3a;letter-spacing:0.5px; }
.footer span { margin:0 8px; }
h3 { font-family:'Instrument Sans',sans-serif !important;color:#fff !important;font-weight:700 !important; }

/* STEGANALYSIS METER */
.meter-wrap { margin:16px 0; }
.meter-label { display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:var(--muted);margin-bottom:6px; }
.meter-track { height:6px;background:rgba(255,255,255,0.05);border-radius:100px;overflow:hidden; }
.meter-fill-green { height:100%;border-radius:100px;background:linear-gradient(90deg,#10b981,#34d399);transition:width 0.6s ease; }
.meter-fill-amber { height:100%;border-radius:100px;background:linear-gradient(90deg,#f59e0b,#fbbf24);transition:width 0.6s ease; }
.meter-fill-red { height:100%;border-radius:100px;background:linear-gradient(90deg,#ef4444,#f87171);transition:width 0.6s ease; }

/* MOBILE */
@media (max-width:768px) {
    .page { padding:0 16px 60px; }
    .hero { padding:56px 0 36px; }
    .how-grid { grid-template-columns:1fr; }
    .vuln-grid { grid-template-columns:1fr; }
    .compare-wrap { grid-template-columns:1fr; }
    .bit-grid { grid-template-columns:1fr;gap:20px; }
    .stats-row { width:100%; }
    .stat { padding:12px 16px;flex:1; }
    .form-card { padding:24px 20px; }
    .step-pill { width:100%;max-width:300px;justify-content:flex-start; }
}
</style>

<div class="bg-orbs">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CRYPTO & STEGO CORE
# ─────────────────────────────────────────────

def xor_cipher(data: bytes, key: str) -> bytes:
    """XOR stream cipher — lightweight, runs without PyCryptodome."""
    key_bytes = hashlib.sha256(key.encode()).digest()  # 32-byte key from passphrase
    return bytes(b ^ key_bytes[i % 32] for i, b in enumerate(data))

def encrypt_message(text: str, passphrase: str) -> str:
    """Encrypt text using XOR cipher derived from passphrase, return hex string."""
    ciphertext = xor_cipher(text.encode('utf-8'), passphrase)
    return ciphertext.hex()

def decrypt_message(hex_text: str, passphrase: str) -> str:
    """Decrypt hex-encoded XOR ciphertext back to text."""
    try:
        ciphertext = bytes.fromhex(hex_text)
        plaintext = xor_cipher(ciphertext, passphrase)
        return plaintext.decode('utf-8')
    except Exception:
        return ""

def text_to_bin(text: str) -> str:
    return ''.join(format(ord(c), '08b') for c in text)

def max_capacity(img: Image.Image) -> int:
    img = img.convert('RGB')
    w, h = img.size
    return (w * h * 3 - 16) // 8

def encode_lsb(img: Image.Image, secret_data: str) -> Image.Image:
    binary_msg = text_to_bin(secret_data) + '1111111111111110'
    data_index = 0
    img = img.convert('RGB')
    pixels = list(img.getdata())
    new_pixels = []
    for pixel in pixels:
        pixel = list(pixel)
        for i in range(3):
            if data_index < len(binary_msg):
                pixel[i] = (pixel[i] & ~1) | int(binary_msg[data_index])
                data_index += 1
        new_pixels.append(tuple(pixel))
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    return new_img

def decode_lsb(img: Image.Image) -> str:
    img = img.convert('RGB')
    pixels = list(img.getdata())
    binary_msg = ""
    for pixel in pixels:
        for i in range(3):
            binary_msg += str(pixel[i] & 1)
    end_marker = "1111111111111110"
    if end_marker in binary_msg:
        binary_msg = binary_msg[:binary_msg.index(end_marker)]
    message = ""
    for i in range(0, len(binary_msg), 8):
        byte = binary_msg[i:i+8]
        if len(byte) < 8:
            break
        message += chr(int(byte, 2))
    return message

def compute_lsb_entropy(img: Image.Image) -> float:
    """Compute entropy of LSB plane — high entropy = likely stego."""
    img = img.convert('RGB')
    pixels = list(img.getdata())
    bits = []
    for px in pixels:
        for ch in px:
            bits.append(ch & 1)
    ones = sum(bits)
    total = len(bits)
    if total == 0:
        return 0.0
    p1 = ones / total
    p0 = 1 - p1
    if p0 == 0 or p1 == 0:
        return 0.0
    entropy = -(p0 * math.log2(p0) + p1 * math.log2(p1))
    return round(entropy, 4)

def compute_chi_square(img: Image.Image) -> float:
    """
    Simplified chi-square steganalysis on the LSB plane.
    Returns a suspicion score 0.0–1.0 (higher = more suspicious).
    """
    img = img.convert('RGB')
    pixels = np.array(img)
    r_lsb = pixels[:, :, 0] & 1
    ones = np.sum(r_lsb)
    total = r_lsb.size
    expected = total / 2
    if expected == 0:
        return 0.0
    chi = (ones - expected) ** 2 / expected + (total - ones - expected) ** 2 / expected
    # Normalize to 0–1 using logistic sigmoid
    score = 1 / (1 + math.exp(-0.001 * (chi - 500)))
    return round(score, 3)

def rs_analysis_score(img: Image.Image) -> float:
    """
    RS (Regular/Singular) Analysis — detects LSB steganography.
    Returns suspicion score 0.0–1.0.
    """
    img_gray = img.convert('L')
    arr = np.array(img_gray, dtype=np.int32)
    h, w = arr.shape
    block_size = 4
    R_count, S_count, R_inv, S_inv = 0, 0, 0, 0
    for i in range(0, h - block_size, block_size):
        for j in range(0, w - block_size, block_size):
            block = arr[i:i+block_size, j:j+block_size].flatten()
            if len(block) < 4:
                continue
            # Discrimination function: sum of abs differences
            def disc(b):
                return sum(abs(int(b[k+1]) - int(b[k])) for k in range(len(b)-1))
            d_orig = disc(block)
            # Flip LSB
            flipped = block.copy()
            for k in range(len(flipped)):
                flipped[k] = flipped[k] ^ 1
            d_flip = disc(flipped)
            if d_flip > d_orig:
                R_count += 1
            elif d_flip < d_orig:
                S_count += 1
            # Inverse flip (flip MSB as proxy)
            inv_block = block.copy()
            for k in range(len(inv_block)):
                inv_block[k] = inv_block[k] ^ 2
            d_inv = disc(inv_block)
            if d_inv > d_orig:
                R_inv += 1
            elif d_inv < d_orig:
                S_inv += 1
    total = R_count + S_count + 1
    # If R_count >> S_count -> suspicious
    imbalance = abs(R_count - R_inv) / (total + 1)
    score = min(1.0, imbalance * 3)
    return round(score, 3)


# ─────────────────────────────────────────────
#  HERO SECTION
# ─────────────────────────────────────────────
st.markdown("""
<div class="page">
<div class="hero">
    <div class="hero-pill"><div class="pill-dot"></div>Kelompok 4 &nbsp;·&nbsp; UTS Cybersecurity &nbsp;·&nbsp; Universitas Brawijaya</div>
    <div class="hero-title">Sembunyikan Pesan,<br><span class="grad">Lindungi Privasi.</span></div>
    <span class="hero-sub">Steganografi LSB + XOR Encryption — sisipkan pesan terenkripsi ke dalam piksel gambar tanpa mengubah tampilan visual sama sekali.</span>
    <div class="hero-badges">
        <div class="badge badge-main"><div class="badge-dot dot-purple"></div>LSB Steganography</div>
        <div class="badge badge-green"><div class="badge-dot dot-green"></div>XOR Encryption</div>
        <div class="badge badge-sec"><div class="badge-dot dot-cyan"></div>Steganalysis Detector</div>
        <div class="badge badge-sec">🔐 Before vs After Mitigation</div>
    </div>
</div>
<div class="stats-row">
    <div class="stat"><div class="stat-val">1 bit</div><div class="stat-lbl">per channel RGB</div></div>
    <div class="stat"><div class="stat-val">XOR</div><div class="stat-lbl">enkripsi pesan</div></div>
    <div class="stat"><div class="stat-val">SHA-256</div><div class="stat-lbl">key derivation</div></div>
    <div class="stat"><div class="stat-val">PNG</div><div class="stat-lbl">lossless output</div></div>
    <div class="stat"><div class="stat-val">RS+χ²</div><div class="stat-lbl">steganalysis</div></div>
</div>
""", unsafe_allow_html=True)

tab_enc, tab_dec, tab_stega, tab_info = st.tabs([
    "🔒  Encode + Enkripsi",
    "🔓  Decode + Dekripsi",
    "🔍  Steganalysis",
    "📖  Analisis & Mitigasi"
])


# ─────────────────────────────────────────────
#  TAB 1 — ENCODE + ENKRIPSI
# ─────────────────────────────────────────────
with tab_enc:
    st.markdown("""
    <div class="feature-strip">
        <span class="feature-label">// mode 01</span>
        <span class="feature-title">Encode &amp; <span class="grad">Sembunyikan</span></span>
        <span class="feature-desc">Upload gambar, tulis pesan, tambahkan passphrase untuk enkripsi XOR — pesan akan terenkripsi sebelum disisipkan ke piksel.</span>
        <div class="steps-row">
            <div class="step-pill"><div class="step-num">01</div>Upload gambar PNG/JPG</div>
            <div class="step-pill"><div class="step-num">02</div>Tulis pesan rahasia</div>
            <div class="step-pill"><div class="step-num">03</div>Set passphrase (opsional)</div>
            <div class="step-pill"><div class="step-num">04</div>Encode & unduh PNG</div>
        </div>
        <div class="tags-row">
            <span class="tag">INPUT: IMAGE + TEXT</span>
            <span class="tag tag-green">XOR ENCRYPTION</span>
            <span class="tag">OUTPUT: STEGO PNG</span>
            <span class="tag">LOSSLESS</span>
        </div>
    </div>
    <div class="form-card">
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Upload Gambar Sumber</div>', unsafe_allow_html=True)
    up_enc = st.file_uploader("Pilih gambar (PNG / JPG / JPEG)", type=["png","jpg","jpeg"], key="enc")

    if up_enc:
        img_obj = Image.open(up_enc)
        cap = max_capacity(img_obj)
        w, h = img_obj.size
        c1, c2 = st.columns([3, 2])
        with c1:
            st.image(up_enc, caption="Preview Gambar Asli", use_container_width=True)
        with c2:
            st.markdown(f"""
            <div class="meta-box">
                <div class="meta-row"><span class="meta-key">Resolusi</span><span class="meta-val">{w} × {h}</span></div>
                <div class="meta-row"><span class="meta-key">Format</span><span class="meta-val">{img_obj.format or 'PNG'}</span></div>
                <div class="meta-row"><span class="meta-key">Total piksel</span><span class="meta-val">{w*h:,}</span></div>
                <div class="meta-row"><span class="meta-key">Kapasitas maks (plaintext)</span><span class="meta-val">{cap:,} kar</span></div>
                <div class="meta-row"><span class="meta-key">Kapasitas maks (terenkripsi)</span><span class="meta-val">{cap//2:,} kar</span></div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<hr class="sdiv"><div class="sec-title">Pesan Rahasia</div>', unsafe_allow_html=True)
        msg = st.text_area("Tulis pesan yang ingin disembunyikan", placeholder="Ketik pesan di sini...", height=120)

        st.markdown('<hr class="sdiv"><div class="sec-title">Enkripsi (Opsional)</div>', unsafe_allow_html=True)
        use_enc = st.checkbox("🔐 Aktifkan enkripsi XOR sebelum disisiipkan ke gambar", value=True)
        passphrase = ""
        if use_enc:
            passphrase = st.text_input("Passphrase (kunci enkripsi)", type="password", placeholder="Masukkan passphrase rahasia...")
            if passphrase:
                st.markdown('<div class="success-box"><strong>Aktif:</strong> Pesan akan di-hash SHA-256 lalu dienkripsi XOR sebelum disisipkan. Hanya yang tahu passphrase yang bisa membaca pesan.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="info-box"><strong>Info:</strong> Masukkan passphrase untuk mengaktifkan enkripsi, atau kosongkan untuk LSB tanpa enkripsi.</div>', unsafe_allow_html=True)

        if msg:
            data_to_embed = encrypt_message(msg, passphrase) if (use_enc and passphrase) else msg
            used = len(data_to_embed)
            eff_cap = cap // 2 if (use_enc and passphrase) else cap
            pct = min(used / eff_cap * 100, 100) if eff_cap > 0 else 100
            color = "linear-gradient(90deg,#7c6af7,#a855f7)" if pct < 60 else ("linear-gradient(90deg,#f59e0b,#fbbf24)" if pct < 85 else "linear-gradient(90deg,#ef4444,#f87171)")
            st.markdown(f"""
            <div class="cap-wrap">
                <div class="cap-header"><span>Kapasitas terpakai</span><span>{used:,} / {eff_cap:,} karakter ({pct:.1f}%)</span></div>
                <div class="cap-track"><div class="cap-fill" style="width:{pct}%;background:{color};"></div></div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<hr class="sdiv"><div class="sec-title">Eksekusi</div>', unsafe_allow_html=True)
        if st.button("🔒  Encode & Sembunyikan Pesan", key="btn_enc"):
            if not msg:
                st.error("⚠️  Pesan tidak boleh kosong.")
            else:
                data_to_embed = encrypt_message(msg, passphrase) if (use_enc and passphrase) else msg
                eff_cap = cap // 2 if (use_enc and passphrase) else cap
                if len(data_to_embed) > eff_cap:
                    st.error(f"⚠️  Pesan terlalu panjang setelah enkripsi. Gunakan gambar lebih besar atau pesan lebih pendek.")
                else:
                    with st.spinner("Mengenkripsi & menyisipkan data ke piksel..."):
                        result = encode_lsb(img_obj, data_to_embed)
                        buf = io.BytesIO()
                        result.save(buf, format="PNG")
                    enc_label = "XOR-encrypted" if (use_enc and passphrase) else "plaintext"
                    st.success(f"✅  Pesan berhasil disembunyikan! ({enc_label})")
                    if use_enc and passphrase:
                        st.info("🔑  Simpan passphrase-mu! Tanpa passphrase yang benar, pesan tidak bisa didekripsi.")
                    st.download_button("⬇  Unduh Stego Image (PNG)", buf.getvalue(), "stego_output.png", mime="image/png")
    else:
        st.markdown('<div class="info-box"><strong>Tips:</strong> Gunakan gambar PNG beresolusi tinggi untuk kapasitas pesan yang lebih besar. Gambar 1000×1000 bisa menyimpan ±370.000 karakter.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TAB 2 — DECODE + DEKRIPSI
# ─────────────────────────────────────────────
with tab_dec:
    st.markdown("""
    <div class="feature-strip">
        <span class="feature-label">// mode 02</span>
        <span class="feature-title">Decode &amp; <span class="grad">Ekstrak</span></span>
        <span class="feature-desc">Upload stego image dan masukkan passphrase untuk mendekripsi pesan tersembunyi. Jika pesan tidak terenkripsi, kosongkan passphrase.</span>
        <div class="steps-row">
            <div class="step-pill"><div class="step-num">01</div>Upload stego image PNG</div>
            <div class="step-pill"><div class="step-num">02</div>Masukkan passphrase</div>
            <div class="step-pill"><div class="step-num">03</div>Decode & baca pesan</div>
        </div>
        <div class="tags-row">
            <span class="tag">INPUT: STEGO PNG</span>
            <span class="tag tag-green">XOR DECRYPTION</span>
            <span class="tag">OUTPUT: PLAINTEXT</span>
        </div>
    </div>
    <div class="form-card">
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Upload Stego Image</div>', unsafe_allow_html=True)
    up_dec = st.file_uploader("Upload gambar yang mengandung pesan", type=["png","jpg","jpeg"], key="dec")

    if up_dec:
        st.image(up_dec, caption="Stego Image", use_container_width=True)

        st.markdown('<hr class="sdiv"><div class="sec-title">Dekripsi</div>', unsafe_allow_html=True)
        dec_passphrase = st.text_input("Passphrase (kosongkan jika tidak terenkripsi)", type="password", placeholder="Masukkan passphrase...", key="dec_pass")

        st.markdown('<hr class="sdiv"><div class="sec-title">Ekstrak Pesan</div>', unsafe_allow_html=True)
        if st.button("🔓  Decode & Ekstrak Pesan", key="btn_dec"):
            with st.spinner("Membaca bit LSB dari piksel..."):
                raw = decode_lsb(Image.open(up_dec))
            if raw:
                if dec_passphrase:
                    with st.spinner("Mendekripsi pesan..."):
                        plaintext = decrypt_message(raw, dec_passphrase)
                    if plaintext and all(32 <= ord(c) <= 126 or c in '\n\r\t' for c in plaintext):
                        st.success(f"✅  Pesan berhasil didekripsi — {len(plaintext):,} karakter.")
                        st.markdown(f'<div class="result-box result-box-green">{plaintext}</div>', unsafe_allow_html=True)
                    else:
                        st.error("❌  Passphrase salah atau pesan tidak terenkripsi dengan passphrase ini.")
                        st.markdown(f'<div class="result-box result-box-red">Data raw (hex): {raw[:120]}...</div>', unsafe_allow_html=True)
                else:
                    st.success(f"✅  Pesan ditemukan (plaintext) — {len(raw):,} karakter.")
                    st.markdown(f'<div class="result-box">{raw}</div>', unsafe_allow_html=True)
            else:
                st.warning("⚠️  Tidak ada pesan ditemukan. Pastikan file ini stego image yang valid.")
    else:
        st.markdown('<div class="info-box"><strong>Penting:</strong> Hanya gunakan file PNG asli dari proses encode. Screenshot atau gambar terkompresi (JPG) akan merusak data LSB.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TAB 3 — STEGANALYSIS
# ─────────────────────────────────────────────
with tab_stega:
    st.markdown("""
    <div class="feature-strip">
        <span class="feature-label">// mode 03</span>
        <span class="feature-title">Steganalysis <span class="grad">Detector</span></span>
        <span class="feature-desc">Analisis gambar untuk mendeteksi apakah ada pesan tersembunyi menggunakan dua metode: Chi-Square Attack dan RS Analysis — teknik yang digunakan oleh security researcher.</span>
        <div class="steps-row">
            <div class="step-pill"><div class="step-num">01</div>Upload gambar yang dicurigai</div>
            <div class="step-pill"><div class="step-num">02</div>Jalankan analisis</div>
            <div class="step-pill"><div class="step-num">03</div>Lihat skor kecurigaan</div>
        </div>
        <div class="tags-row">
            <span class="tag tag-red">CHI-SQUARE ATTACK</span>
            <span class="tag tag-red">RS ANALYSIS</span>
            <span class="tag">LSB ENTROPY</span>
            <span class="tag">FORENSIC MODE</span>
        </div>
    </div>
    <div class="form-card form-card-red">
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Upload Gambar untuk Dianalisis</div>', unsafe_allow_html=True)
    up_stega = st.file_uploader("Upload gambar (PNG / JPG / JPEG)", type=["png","jpg","jpeg"], key="stega")

    if up_stega:
        img_stega = Image.open(up_stega)
        w, h = img_stega.size
        c1, c2 = st.columns([1, 1])
        with c1:
            st.image(up_stega, caption="Gambar Target", use_container_width=True)
        with c2:
            st.markdown(f"""
            <div class="meta-box">
                <div class="meta-row"><span class="meta-key">Resolusi</span><span class="meta-val">{w} × {h}</span></div>
                <div class="meta-row"><span class="meta-key">Total piksel</span><span class="meta-val">{w*h:,}</span></div>
                <div class="meta-row"><span class="meta-key">Mode</span><span class="meta-val">{img_stega.mode}</span></div>
            </div>
            <div style="height:12px"></div>
            <div class="info-box" style="margin-bottom:0"><strong>Cara kerja:</strong> Dua metode statistik berbeda digunakan untuk mendeteksi anomali pada LSB plane gambar.</div>
            """, unsafe_allow_html=True)

        st.markdown('<hr class="sdiv"><div class="sec-title">Jalankan Steganalysis</div>', unsafe_allow_html=True)
        if st.button("🔍  Analisis Gambar", key="btn_stega"):
            with st.spinner("Menghitung Chi-Square..."):
                chi_score = compute_chi_square(img_stega)
            with st.spinner("Menghitung RS Analysis..."):
                rs_score = rs_analysis_score(img_stega)
            with st.spinner("Menghitung LSB Entropy..."):
                entropy = compute_lsb_entropy(img_stega)

            # Verdict
            avg = (chi_score + rs_score) / 2
            if avg > 0.6:
                verdict = "🚨 SANGAT MENCURIGAKAN"
                v_color = "#f87171"
                v_bg = "rgba(239,68,68,0.08)"
                v_border = "rgba(239,68,68,0.3)"
            elif avg > 0.35:
                verdict = "⚠️ MENCURIGAKAN"
                v_color = "#fbbf24"
                v_bg = "rgba(245,158,11,0.08)"
                v_border = "rgba(245,158,11,0.3)"
            else:
                verdict = "✅ GAMBAR BERSIH"
                v_color = "#6ee7b7"
                v_bg = "rgba(16,185,129,0.08)"
                v_border = "rgba(16,185,129,0.3)"

            st.markdown(f"""
            <div style="background:{v_bg};border:1px solid {v_border};border-radius:16px;padding:20px 24px;text-align:center;margin:16px 0;">
                <div style="font-size:1.4rem;font-weight:700;color:{v_color};margin-bottom:4px">{verdict}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:var(--muted)">Skor rata-rata kecurigaan: {avg:.1%}</div>
            </div>
            """, unsafe_allow_html=True)

            # Meters
            chi_pct = chi_score * 100
            rs_pct = rs_score * 100
            ent_pct = entropy * 100
            chi_cls = "meter-fill-green" if chi_pct < 35 else ("meter-fill-amber" if chi_pct < 65 else "meter-fill-red")
            rs_cls  = "meter-fill-green" if rs_pct < 35  else ("meter-fill-amber" if rs_pct < 65  else "meter-fill-red")
            ent_cls = "meter-fill-green" if ent_pct < 70 else ("meter-fill-amber" if ent_pct < 85 else "meter-fill-red")

            st.markdown(f"""
            <div class="meter-wrap">
                <div class="meter-label"><span>Chi-Square Attack</span><span>{chi_pct:.1f}% kecurigaan</span></div>
                <div class="meter-track"><div class="{chi_cls}" style="width:{chi_pct:.1f}%"></div></div>
            </div>
            <div class="meter-wrap">
                <div class="meter-label"><span>RS Analysis</span><span>{rs_pct:.1f}% kecurigaan</span></div>
                <div class="meter-track"><div class="{rs_cls}" style="width:{rs_pct:.1f}%"></div></div>
            </div>
            <div class="meter-wrap">
                <div class="meter-label"><span>LSB Entropy</span><span>{entropy} (maks: 1.0)</span></div>
                <div class="meter-track"><div class="{ent_cls}" style="width:{ent_pct:.1f}%"></div></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="meta-box" style="margin-top:16px">
                <div class="meta-row"><span class="meta-key">Chi-Square Score</span><span class="meta-val">{chi_score}</span></div>
                <div class="meta-row"><span class="meta-key">RS Analysis Score</span><span class="meta-val">{rs_score}</span></div>
                <div class="meta-row"><span class="meta-key">LSB Entropy</span><span class="meta-val">{entropy} / 1.0</span></div>
                <div class="meta-row"><span class="meta-key">Verdict Skor Rata-rata</span><span class="meta-val">{avg:.3f}</span></div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box"><strong>Gunakan tab ini</strong> untuk mendeteksi apakah sebuah gambar mengandung pesan tersembunyi, sebagaimana yang dilakukan security analyst di dunia nyata.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TAB 4 — ANALISIS & MITIGASI
# ─────────────────────────────────────────────
with tab_info:
    st.markdown("""
    <div class="feature-strip">
        <span class="feature-label">// mode 04</span>
        <span class="feature-title">Analisis &amp; <span class="grad">Mitigasi</span></span>
        <span class="feature-desc">Pemahaman mendalam tentang cara kerja LSB, kelemahan yang dimiliki, serangan yang mungkin dilakukan, dan strategi mitigasi yang telah diterapkan.</span>
    </div>
    """, unsafe_allow_html=True)

    # Cara kerja
    st.markdown("""
    <div class="info-box"><strong>Apa itu Steganografi LSB?</strong><br>
    Steganografi menyembunyikan <em>keberadaan</em> pesan, bukan hanya isinya. Teknik <strong>Least Significant Bit (LSB)</strong> memanfaatkan bit paling kecil dari setiap channel warna piksel. Perubahan hanya ±1 sehingga tidak bisa dideteksi mata manusia. Dalam sistem ini, pesan terlebih dahulu <strong>dienkripsi XOR</strong> sebelum disisipkan — menjamin dua lapis keamanan.
    </div>
    <div class="how-grid">
        <div class="how-card"><div class="how-num">// 01</div><div class="how-icon">🔐</div><div class="how-title">XOR Enkripsi</div><div class="how-desc">Passphrase di-hash SHA-256 menjadi 32-byte key. Pesan dienkripsi XOR dengan key tersebut, menghasilkan ciphertext hex.</div></div>
        <div class="how-card"><div class="how-num">// 02</div><div class="how-icon">🔢</div><div class="how-title">Konversi ke Biner</div><div class="how-desc">Ciphertext hex dikonversi ke 8-bit biner per karakter. 'A' → 01000001, dst. End marker 16-bit ditambahkan.</div></div>
        <div class="how-card"><div class="how-num">// 03</div><div class="how-icon">🎨</div><div class="how-title">Modifikasi LSB Piksel</div><div class="how-desc">Bit LSB dari channel R, G, B setiap piksel diganti satu per satu. Perubahan nilai piksel hanya ±1, tidak terdeteksi mata.</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Bit demo
    st.markdown("""
    <div class="bit-demo">
        <div class="bit-demo-label">// simulasi piksel — sebelum & sesudah encode karakter 'H' (ASCII 72 = 01001000)</div>
        <div class="bit-grid">
            <div><div class="bit-col-title">// Sebelum (original)</div>
                <div class="bit-row">R = 200 → <span class="bit-body">1100100</span><span class="lsb-old">0</span></div>
                <div class="bit-row">G = 145 → <span class="bit-body">1001000</span><span class="lsb-old">1</span></div>
                <div class="bit-row">B = 78  → <span class="bit-body">0100111</span><span class="lsb-old">0</span></div>
            </div>
            <div><div class="bit-col-title">// Sesudah (encode '0','1','0' dari 'H')</div>
                <div class="bit-row">R = 200 → <span class="bit-body">1100100</span><span class="lsb-new">0</span></div>
                <div class="bit-row">G = 145 → <span class="bit-body">1001000</span><span class="lsb-new">1</span></div>
                <div class="bit-row">B = 78  → <span class="bit-body">0100111</span><span class="lsb-new">0</span></div>
            </div>
        </div>
        <div class="bit-note">Perubahan piksel maksimal ±1. Secara visual identik. Enkripsi XOR memastikan bit pattern terlihat acak di LSB plane.</div>
    </div>
    """, unsafe_allow_html=True)

    # Before vs After
    st.markdown("""
    <div class="sec-title" style="margin-top:32px">Analisis: Before vs After Mitigasi</div>
    <div class="compare-wrap">
        <div class="compare-col">
            <div class="compare-title compare-title-bad">// SEBELUM MITIGASI (LSB Plain)</div>
            <div class="compare-item"><span class="compare-icon-bad">✗</span>Pesan disisipkan langsung tanpa enkripsi</div>
            <div class="compare-item"><span class="compare-icon-bad">✗</span>Siapapun yang tahu teknik LSB bisa membaca pesan</div>
            <div class="compare-item"><span class="compare-icon-bad">✗</span>Chi-Square Attack mudah mendeteksi keberadaan pesan</div>
            <div class="compare-item"><span class="compare-icon-bad">✗</span>RS Analysis menunjukkan imbalance pattern yang jelas</div>
            <div class="compare-item"><span class="compare-icon-bad">✗</span>LSB Entropy terlalu tinggi (mendekati 1.0)</div>
        </div>
        <div class="compare-col">
            <div class="compare-title compare-title-good">// SESUDAH MITIGASI (LSB + XOR)</div>
            <div class="compare-item"><span class="compare-icon-good">✓</span>Pesan dienkripsi XOR dengan SHA-256 key derivation</div>
            <div class="compare-item"><span class="compare-icon-good">✓</span>Tanpa passphrase, ciphertext tidak dapat dibaca</div>
            <div class="compare-item"><span class="compare-icon-good">✓</span>Output XOR lebih random, menyulitkan steganalysis statistik</div>
            <div class="compare-item"><span class="compare-icon-good">✓</span>Dua lapis keamanan: sembunyi keberadaan + sembunyi isi</div>
            <div class="compare-item"><span class="compare-icon-good">✓</span>SHA-256 key derivation membuat brute-force sangat sulit</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Vulnerabilities
    st.markdown("""
    <div class="sec-title" style="margin-top:32px">Kelemahan yang Teridentifikasi</div>
    <div class="vuln-grid">
        <div class="vuln-card">
            <div class="vuln-card-title">⚠ Chi-Square Attack</div>
            <div class="vuln-card-body">Analisis statistik distribusi nilai piksel ganjil/genap pada LSB plane dapat mengungkap keberadaan data tersembunyi. Gambar stego menunjukkan distribusi yang lebih seragam dibanding gambar asli.</div>
        </div>
        <div class="vuln-card">
            <div class="vuln-card-title">⚠ RS Analysis</div>
            <div class="vuln-card-body">Regular-Singular analysis mendeteksi imbalance antara blok piksel yang bersifat "regular" vs "singular" setelah flipping LSB — indikasi kuat adanya data tersisip.</div>
        </div>
        <div class="vuln-card">
            <div class="vuln-card-title">⚠ Kompresi Lossy</div>
            <div class="vuln-card-body">Format JPG/WEBP menggunakan kompresi lossy yang mengubah nilai piksel secara agresif, menghancurkan bit LSB dan membuat pesan tidak bisa di-recover.</div>
        </div>
        <div class="vuln-card">
            <div class="vuln-card-title">⚠ XOR Weak Points</div>
            <div class="vuln-card-body">XOR cipher rentan terhadap known-plaintext attack jika passphrase pendek. Solusi: SHA-256 key stretching membuat key selalu 256-bit terlepas panjang passphrase asli.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Mitigasi
    st.markdown("""
    <div class="sec-title" style="margin-top:32px">Mitigasi yang Diterapkan</div>
    <div class="vuln-grid">
        <div class="mitig-card">
            <div class="mitig-card-title">✅ XOR + SHA-256 Key Derivation</div>
            <div class="mitig-card-body">Passphrase diproses melalui SHA-256 menghasilkan 256-bit key yang kuat. XOR dengan key ini memastikan ciphertext terlihat acak, menyulitkan analisis statistik.</div>
        </div>
        <div class="mitig-card">
            <div class="mitig-card-title">✅ End Marker 16-bit</div>
            <div class="mitig-card-body">Penanda akhir unik (16 bit bernilai 1) memastikan decode berhenti tepat di akhir pesan, mencegah pembacaan noise piksel yang tidak relevan.</div>
        </div>
        <div class="mitig-card">
            <div class="mitig-card-title">✅ PNG Lossless Output</div>
            <div class="mitig-card-body">Output selalu disimpan dalam format PNG yang menggunakan kompresi lossless — bit LSB terjaga 100% tanpa perubahan dari proses encode hingga decode.</div>
        </div>
        <div class="mitig-card">
            <div class="mitig-card-title">✅ Kapasitas Validasi</div>
            <div class="mitig-card-body">Sistem memvalidasi panjang pesan (setelah enkripsi) vs kapasitas gambar sebelum encode, mencegah data overflow yang bisa merusak struktur pesan.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warn-box" style="margin-top:24px">
        <div class="warn-title">⚠ Keterbatasan Sistem Saat Ini</div>
        <ul>
            <li>XOR cipher lebih lemah dari AES-GCM — untuk keamanan tinggi, rekomendasikan upgrade ke AES-256</li>
            <li>Enkripsi XOR tetap dapat terdeteksi steganalysis meski lebih sulit dibanding plaintext LSB</li>
            <li>Sistem ini adalah proof-of-concept edukasi, bukan untuk komunikasi rahasia produksi</li>
            <li>Passphrase tidak disimpan — user bertanggung jawab menyimpan passphrase dengan aman</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">LSB Stealth <span>·</span> Kelompok 4 <span>·</span> UTS Cybersecurity <span>·</span> Universitas Brawijaya <span>·</span> 2026</div>
</div>
""", unsafe_allow_html=True)