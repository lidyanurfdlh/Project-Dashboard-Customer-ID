from pathlib import Path
import json
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# === DASHBOARD CUSTOMER ID RECOMMENDATION ===
px.defaults.template = "plotly_white"
px.defaults.color_continuous_scale = "Blues"

st.set_page_config(
    page_title="Customer ID Recommendation Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# MULTI-LANGUAGE (i18n) DICTIONARY & SETUP
# ==========================================
if "lang" not in st.session_state:
    st.session_state.lang = "en"  # Default English untuk kebutuhan figure/screenshot

st.sidebar.markdown("### 🌐 Language / Bahasa")
lang_choice = st.sidebar.radio(
    "Select Language / Pilih Bahasa",
    options=["English", "Bahasa Indonesia"],
    index=0 if st.session_state.lang == "en" else 1,
    label_visibility="collapsed"
)
st.session_state.lang = "en" if lang_choice == "English" else "id"

TRANSLATIONS = {
    # Headers & Hero
    "title_hero": {
        "id": "🛒 Customer ID Recommendation Dashboard",
        "en": "🛒 Customer ID Recommendation Dashboard"
    },
    "hero_desc": {
        "id": "Dashboard ini menyajikan analisis pelanggan berbasis Customer RFM, Association Rule Mining, dan Nudge Framework untuk mendukung rekomendasi strategi pemasaran berbasis data transaksi.",
        "en": "This dashboard presents customer analytics based on Customer RFM, Association Rule Mining, and Nudge Framework to support data-driven marketing strategy recommendations."
    },
    # Metrics
    "m_raw_cust": {"id": "Raw Customers", "en": "Raw Customers"},
    "m_raw_cust_help": {"id": "Total pelanggan awal pada dataset.", "en": "Initial total customers in dataset."},
    "m_analyzed_cust": {"id": "Analyzed Customers", "en": "Analyzed Customers"},
    "m_analyzed_cust_help": {"id": "Jumlah pelanggan yang masuk proses analisis.", "en": "Number of customers processed for analysis."},
    "m_audit_cust": {"id": "Audit Customers", "en": "Audit Customers"},
    "m_audit_cust_help": {"id": "Jumlah pelanggan yang tercatat pada audit data.", "en": "Number of customers recorded in data audit."},
    "m_valid_orders": {"id": "Valid Orders", "en": "Valid Orders"},
    "m_valid_orders_help": {"id": "Order berstatus dibayar, dikirim, dan selesai.", "en": "Orders with paid, shipped, and completed status."},
    "m_relevance": {"id": "Relevance Rate", "en": "Relevance Rate"},
    "m_relevance_help": {"id": "Rekomendasi sesuai kategori favorit pelanggan aktif.", "en": "Recommendations matching active customers' favorite category."},

    # Tabs Title
    "tab_exec": {"id": "🏠 Executive Overview", "en": "🏠 Executive Overview"},
    "tab_val": {"id": "🧹 Data Validation", "en": "🧹 Data Validation"},
    "tab_rfm": {"id": "👥 Customer RFM", "en": "👥 Customer RFM"},
    "tab_prod": {"id": "📦 Product & Revenue", "en": "📦 Product & Revenue"},
    "tab_assoc": {"id": "🔗 Association Rule Validation", "en": "🔗 Association Rule Validation"},
    "tab_nba": {"id": "🎯 Next Best Action", "en": "🎯 Next Best Action"},
    "tab_nudge": {"id": "🧠 Nudge Framework", "en": "🧠 Nudge Framework"},
    "tab_kpi": {"id": "📈 KPI & Decision Support", "en": "📈 KPI & Decision Support"},
    "tab_exp": {"id": "📋 Data Explorer", "en": "📋 Data Explorer"},
    "tab_guide": {"id": "📖 Panduan Baca", "en": "📖 User Guide"},
    "tab_raw": {"id": "📥 Raw Data Audit", "en": "📥 Raw Data Audit"},

    # Chart Titles & Section Headers
    "sec_exec_title": {"id": "Executive Overview", "en": "Executive Overview"},
    "sec_exec_desc": {
        "id": "Ringkasan utama dashboard berdasarkan data pelanggan, transaksi, segmentasi RFM, dan rekomendasi pemasaran.",
        "en": "Executive summary based on customer, transaction, RFM segmentation, and marketing recommendation data."
    },
    "sec_val_title": {"id": "Data Validation", "en": "Data Validation"},
    "sec_val_desc": {
        "id": "Ringkasan validasi data, status transaksi, pelanggan audit, dan recency sebelum digunakan dalam analisis.",
        "en": "Summary of data validation, transaction status, audit customers, and recency prior to analysis."
    },
    "sec_rfm_title": {"id": "Customer RFM", "en": "Customer RFM"},
    "sec_rfm_desc": {
        "id": "Segmentasi pelanggan berdasarkan Recency, Frequency, dan Monetary.",
        "en": "Customer segmentation based on Recency, Frequency, and Monetary metrics."
    },
    "sec_prod_title": {"id": "Product & Revenue", "en": "Product & Revenue"},
    "sec_prod_desc": {
        "id": "Visualisasi kontribusi kategori, produk, dan pola pembelian pelanggan.",
        "en": "Visualization of category contribution, products, and customer purchasing patterns."
    },
    "sec_assoc_title": {"id": "Association Rule Validation", "en": "Association Rule Validation"},
    "sec_assoc_desc": {
        "id": "Validasi pola pembelian bersama menggunakan support, confidence, lift, dan basket count.",
        "en": "Validation of co-purchase patterns using support, confidence, lift, and basket count."
    },
    "sec_nba_title": {"id": "Next Best Action per Active Customer", "en": "Next Best Action per Active Customer"},
    "sec_nba_desc": {
        "id": "Rekomendasi utama hanya diberikan untuk pelanggan aktif dengan kategori favorit yang valid.",
        "en": "Primary recommendations provided exclusively for active customers with valid favorite categories."
    },
    "sec_nudge_title": {"id": "Nudge Framework", "en": "Nudge Framework"},
    "sec_nudge_desc": {
        "id": "Nudge ditampilkan sebagai strategi per segmen pelanggan aktif, bukan sebagai grafik kategori numerik.",
        "en": "Nudges displayed as strategies per active customer segment rather than numerical category charts."
    },
    "sec_kpi_title": {"id": "KPI & Decision Support", "en": "KPI & Decision Support"},
    "sec_kpi_desc": {
        "id": "KPI dan kerangka keputusan untuk mengevaluasi strategi rekomendasi pada pelanggan aktif.",
        "en": "KPIs and decision-support framework to evaluate recommendation strategies on active customers."
    },
    "sec_exp_title": {"id": "Data Explorer", "en": "Data Explorer"},
    "sec_exp_desc": {
        "id": "Akses dataset hasil pengolahan, termasuk tabel audit pelanggan yang dikeluarkan dari analisis utama.",
        "en": "Access processed datasets, including customer audit tables excluded from primary analysis."
    },
    "sec_guide_title": {"id": "Panduan Baca Dashboard", "en": "Dashboard User Guide"},
    "sec_guide_desc": {
        "id": "Panduan singkat untuk membaca setiap menu utama pada dashboard.",
        "en": "A brief guide to understanding each primary menu on the dashboard."
    },
    "sec_raw_title": {"id": "Raw Data Audit", "en": "Raw Data Audit"},
    "sec_raw_desc": {
        "id": "Ringkasan jumlah record dan jumlah field dari setiap tabel data mentah.",
        "en": "Summary of total records and field counts for each raw data table."
    },

    # Specific Chart Titles
    "chart_raw_before": {"id": "Raw Data Sebelum Preprocessing", "en": "Raw Data Before Preprocessing"},
    "chart_raw_fields": {"id": "Jumlah Field pada Setiap Tabel Mentah", "en": "Number of Fields in Each Raw Table"},
    "chart_cust_per_seg": {"id": "Jumlah Pelanggan Aktif per Segmen", "en": "Number of Active Customers per Segment"},
    "chart_rev_share": {"id": "Pangsa Pendapatan per Segmen", "en": "Revenue Share by Segment"},
    "chart_monthly_rev": {"id": "Pendapatan Bulanan per Segmen", "en": "Monthly Revenue by Segment"},
    "chart_order_status": {"id": "Distribusi Status Pesanan", "en": "Order Status Distribution"},
    "chart_recency_dist": {"id": "Distribusi Recency Pelanggan Aktif", "en": "Active Customer Recency Distribution"},
    "chart_freq_dist": {"id": "Distribusi Frekuensi", "en": "Frequency Distribution"},
    "chart_monetary_dist": {"id": "Distribusi Monetary", "en": "Monetary Distribution"},
    "chart_rfm_map": {"id": "Customer RFM Map: Recency vs Monetary", "en": "Customer RFM Map: Recency vs Monetary"},
    "chart_rev_cat": {"id": "Pendapatan per Kategori", "en": "Revenue by Category"},
    "chart_top_prod": {"id": "Top 15 Produk Berdasarkan Pendapatan", "en": "Top 15 Products by Revenue"},
    "chart_fav_cat": {"id": "Distribusi Kategori Favorit", "en": "Favorite Category Distribution"},
    "chart_cust_prod_pattern": {"id": "Pola Pembelian Produk Pelanggan", "en": "Customer Product Purchase Pattern"},
    "chart_supp_conf": {"id": "Support vs Confidence berdasarkan Keandalan", "en": "Support vs Confidence by Reliability"},
    "chart_rule_rel": {"id": "Distribusi Keandalan Rule", "en": "Rule Reliability Distribution"},
    "chart_rec_cat_dist": {"id": "Distribusi Kategori Rekomendasi", "en": "Recommended Category Distribution"},
    "chart_nudge_dist": {"id": "Distribusi Tipe Nudge", "en": "Nudge Type Distribution"},
    "chart_nudge_segment": {"id": "Jumlah Customer per Segment dan Recommended Nudge", "en": "Number of Customers per Segment and Recommended Nudge"},
    "chart_eval_metrics": {"id": "Metrik Evaluasi", "en": "Evaluation Metrics"},
    "chart_raw_rec_table": {"id": "Jumlah Record per Tabel Mentah", "en": "Raw Records by Table"},
    "chart_raw_field_table": {"id": "Jumlah Field per Tabel Mentah", "en": "Raw Fields by Table"}
}

def t(key):
    return TRANSLATIONS.get(key, {}).get(st.session_state.lang, key)

# === STYLES ===
st.markdown("""
<style>
html, body, .stApp, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #F8FAFC 0%, #EEF6FF 45%, #F7FBFF 100%) !important;
    color: #1E293B !important;
}
.block-container {padding-top: 1.3rem; padding-bottom: 2.2rem; max-width: 1450px;}
[data-testid="stHeader"] {background: rgba(248,250,252,.75) !important; backdrop-filter: blur(10px);}
[data-testid="stSidebar"] {background: linear-gradient(180deg,#FFFFFF 0%,#EFF6FF 55%,#ECFEFF 100%) !important; border-right:1px solid #DBEAFE !important;}
[data-testid="stSidebar"] * {color:#1E293B !important;}
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 {color:#0F172A !important;}
[data-testid="stSidebar"] small,[data-testid="stSidebar"] .stCaptionContainer {color:#64748B !important;}
div[data-baseweb="select"] > div {background-color:#FFFFFF !important; border:1px solid #BFDBFE !important; border-radius:14px !important; box-shadow:0 6px 16px rgba(37,99,235,.08) !important; padding-left:8px !important; overflow:visible !important;}
.stMultiSelect [data-baseweb="tag"], span[data-baseweb="tag"] {background:linear-gradient(135deg,#DBEAFE 0%,#CCFBF1 100%) !important; color:#0F172A !important; border-radius:999px !important; border:1px solid #93C5FD !important; font-weight:700 !important; margin-left:4px !important; padding-left:10px !important; overflow:visible !important; max-width:none !important;}
.stMultiSelect [data-baseweb="tag"] span {overflow:visible !important; text-overflow:clip !important; white-space:nowrap !important;}
input, textarea {background-color:#FFFFFF !important; color:#0F172A !important;}
.hero {background:linear-gradient(135deg,#2563EB 0%,#0EA5E9 48%,#14B8A6 100%); color:white; padding:32px 34px; border-radius:30px; margin-bottom:22px; box-shadow:0 18px 45px rgba(37,99,235,.22); border:1px solid rgba(255,255,255,.28);}
.hero h1 {font-size:38px; margin:0 0 10px; letter-spacing:-.6px; font-weight:900; color:#FFFFFF !important;}
.hero p {font-size:15px; color:#EFF6FF !important; line-height:1.65; max-width:1120px;}
.pill {display:inline-block; padding:8px 14px; border-radius:999px; margin:12px 7px 0 0; background:rgba(255,255,255,.20); border:1px solid rgba(255,255,255,.38); color:#FFFFFF !important; font-weight:800; font-size:12px; box-shadow:0 5px 14px rgba(15,23,42,.12);}
.metric-card {background:rgba(255,255,255,.92); border:1px solid #DBEAFE; border-radius:24px; padding:20px 22px; box-shadow:0 14px 30px rgba(37,99,235,.10); min-height:136px; transition:all .25s ease; margin-bottom:14px;}
.metric-card:hover {transform:translateY(-3px); box-shadow:0 18px 38px rgba(37,99,235,.16);}
.metric-label {color:#64748B !important; font-size:12px; font-weight:900; letter-spacing:.8px; text-transform:uppercase; margin-bottom:8px;}
.metric-value {color:#0F172A !important; font-size:31px; font-weight:950; margin-bottom:6px;}
.metric-help {color:#64748B !important; font-size:12px; line-height:1.5;}
.section {background:rgba(255,255,255,.94); border:1px solid #DBEAFE; border-radius:24px; padding:22px 24px; box-shadow:0 12px 28px rgba(37,99,235,.09); margin:18px 0 18px;}
.section h2 {font-size:24px; margin:0 0 8px; color:#0F172A !important; font-weight:900;}
.section p {font-size:14px; color:#64748B !important; line-height:1.7; margin:0;}
.info-box {background:linear-gradient(135deg,#EFF6FF 0%,#F8FAFC 100%); border-left:6px solid #3B82F6; border-radius:18px; padding:15px 18px; color:#1E3A8A !important; line-height:1.65; margin:12px 0 16px; box-shadow:0 8px 20px rgba(59,130,246,.08);}
.warn-box {background:linear-gradient(135deg,#FFF7ED 0%,#FFFBEB 100%); border-left:6px solid #F97316; border-radius:18px; padding:15px 18px; color:#7C2D12 !important; line-height:1.65; margin:12px 0 16px; box-shadow:0 8px 20px rgba(249,115,22,.08);}
.success-box {background:linear-gradient(135deg,#ECFDF5 0%,#F0FDFA 100%); border-left:6px solid #10B981; border-radius:18px; padding:15px 18px; color:#064E3B !important; line-height:1.65; margin:12px 0 16px; box-shadow:0 8px 20px rgba(16,185,129,.08);}
.stTabs [data-baseweb="tab-list"] {gap:10px; flex-wrap:wrap; border-bottom:1px solid #DBEAFE; padding-bottom:12px; margin-top:10px;}
.stTabs [data-baseweb="tab"] {background-color:#FFFFFF; border-radius:999px; padding:10px 17px; color:#334155 !important; font-weight:800; border:1px solid #DBEAFE; box-shadow:0 6px 15px rgba(37,99,235,.07);}
.stTabs [aria-selected="true"] {background:linear-gradient(135deg,#2563EB 0%,#14B8A6 100%) !important; color:white !important; border:1px solid transparent !important;}
div[data-testid="stDataFrame"] {border:1px solid #DBEAFE; border-radius:18px; overflow:hidden; background:#FFFFFF !important; box-shadow:0 10px 24px rgba(37,99,235,.08); color:#0F172A !important;}
.stDownloadButton button,.stButton button {background:linear-gradient(135deg,#2563EB 0%,#14B8A6 100%) !important; color:white !important; border:none !important; border-radius:999px !important; padding:.65rem 1.2rem !important; font-weight:800 !important; box-shadow:0 10px 20px rgba(37,99,235,.18);}
h1,h2,h3,h4,h5,h6 {color:#0F172A !important;}
p,li,label {color:#334155;} [data-testid="stMarkdownContainer"] {color:#334155;} [data-baseweb="select"] span {color:#0F172A !important;} hr {border-color:#DBEAFE !important;}
</style>
""", unsafe_allow_html=True)

BASE = Path(__file__).resolve().parent
OUT = BASE / "outputs"
RAW_DIR = BASE / "data"

def load_csv(name):
    path = OUT / name
    if not path.exists():
        raise FileNotFoundError(f"{name} tidak ditemukan di folder outputs.")
    return pd.read_csv(path)

def load_raw_csv(name):
    path = RAW_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"{name} tidak ditemukan di folder data.")
    return pd.read_csv(path)

def build_raw_audit(raw_tables):
    descriptions = {
        "pelanggan": "Master data pelanggan sebelum filter transaksi valid",
        "orders": "Raw order records sebelum filtering status",
        "detil_order": "Detail transaksi atau line items sebelum preprocessing",
        "produk": "Master data produk dan kategori sebelum join"
    }
    primary_keys = {"pelanggan":"pelanggan_id", "orders":"order_id", "detil_order":"detil_id", "produk":"produk_id"}
    rows = []
    field_rows = []
    for name, df in raw_tables.items():
        display_name = name
        if st.session_state.lang == "en":
            table_map = {"pelanggan": "customers", "detil_order": "order_details", "produk": "products", "orders": "orders"}
            display_name = table_map.get(name, name)

        rows.append({
            "table_name": display_name,
            "raw_records": int(len(df)),
            "fields": int(len(df.columns)),
            "primary_key": primary_keys.get(name, "-"),
            "description": descriptions.get(name, "Raw data sebelum preprocessing")
        })
        for col in df.columns:
            field_rows.append({
                "table_name": display_name,
                "field_name": col,
                "dtype": str(df[col].dtype),
                "missing_values": int(df[col].isna().sum()),
                "unique_values": int(df[col].nunique(dropna=True))
            })
    return pd.DataFrame(rows), pd.DataFrame(field_rows)

def fmt_int(x):
    try: return f"{int(float(x)):,}".replace(",", ".")
    except Exception: return str(x)

def metric_card(label, value, help_text):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-help">{help_text}</div>
    </div>
    """, unsafe_allow_html=True)

def section(title, desc):
    st.markdown(f"""
    <div class="section"><h2>{title}</h2><p>{desc}</p></div>
    """, unsafe_allow_html=True)

SEGMENT_COLORS = {
    "At Risk": "#7DD3FC",
    "Big Spenders": "#1D4ED8",
    "Hibernating": "#FDE68A",
    "Potential Loyalist": "#22C55E",
    "Champions": "#8B5CF6",
    "Loyal Customers": "#14B8A6"
}
CATEGORY_COLORS = {
    "Makanan": "#2563EB",
    "Minuman": "#16A34A",
    "Alat Tulis": "#F97316",
    "Bayi": "#8B5CF6",
    "Perawatan Tubuh": "#EF4444",
    "Rokok": "#6B7280"
}
STATUS_COLORS = {True: "#10B981", False: "#EF4444"}
SPARSE_BASKET_THRESHOLD = 4
EXTREME_LIFT_THRESHOLD = 10

def clean_empty(value, empty_text="Tidak tersedia"):
    if pd.isna(value): return empty_text
    value = str(value).strip()
    return value if value else empty_text

def short_reliability_flag(row):
    flag = str(row.get("reliability_flag", "")).lower()
    rule_level = str(row.get("rule_level", "")).lower()
    lift = pd.to_numeric(row.get("lift"), errors="coerce")
    basket_count = pd.to_numeric(row.get("basket_count"), errors="coerce")
    if "stable" in flag and rule_level == "category": return "Stabil" if st.session_state.lang == "id" else "Stable"
    if ("product" in rule_level) or (pd.notna(lift) and lift > EXTREME_LIFT_THRESHOLD) or (pd.notna(basket_count) and basket_count <= SPARSE_BASKET_THRESHOLD): 
        return "Eksploratif" if st.session_state.lang == "id" else "Exploratory"
    return "Perlu Validasi" if st.session_state.lang == "id" else "Needs Validation"

def plotly_common_layout(fig, height=430):
    fig.update_layout(
        template="plotly_white", height=height, margin=dict(l=25,r=25,t=72,b=55), legend_title_text="",
        paper_bgcolor="rgba(255,255,255,0)", plot_bgcolor="#FFFFFF",
        font=dict(family="Inter, Segoe UI, Arial, sans-serif", size=12, color="#1E293B"),
        title=dict(font=dict(size=17,color="#0F172A"), x=0.02, xanchor="left"),
        legend=dict(bgcolor="rgba(255,255,255,.85)", bordercolor="#E2E8F0", borderwidth=1, font=dict(color="#334155")),
        hoverlabel=dict(bgcolor="#FFFFFF", font_size=12, font_color="#0F172A", bordercolor="#CBD5E1")
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E2E8F0", zeroline=False, linecolor="#CBD5E1", tickfont=dict(color="#475569"), title_font=dict(color="#334155"))
    fig.update_yaxes(showgrid=True, gridcolor="#E2E8F0", zeroline=False, linecolor="#CBD5E1", tickfont=dict(color="#475569"), title_font=dict(color="#334155"))
    return fig

@st.cache_data
def load_all_data():
    data = {name: load_csv(file) for name, file in {
        "customer_rfm":"customer_rfm.csv", "segment_summary":"segment_summary.csv", "monthly":"customer_monthly_summary.csv",
        "customer_product":"customer_product_summary.csv", "rules":"market_basket_rules.csv", "nba":"next_best_action.csv",
        "top_products":"top_products.csv", "line_items":"transaction_line_items.csv", "status_summary":"status_summary.csv",
        "preprocessing_audit":"preprocessing_audit.csv", "excluded_customers":"excluded_customers.csv", "recency_validation":"recency_validation.csv",
        "association_validation":"association_rule_validation.csv", "recommendation_evaluation":"recommendation_evaluation.csv",
        "nudge_framework":"nudge_framework.csv", "kpi_framework":"kpi_framework.csv", "decision_framework":"dashboard_decision_framework.csv",
        "data_dictionary":"data_dictionary.csv"}.items()}
    raw_tables = {
        "pelanggan": load_raw_csv("pelanggan.csv"),
        "orders": load_raw_csv("orders.csv"),
        "detil_order": load_raw_csv("detil_order.csv"),
        "produk": load_raw_csv("produk.csv"),
    }
    raw_data_summary, raw_field_summary = build_raw_audit(raw_tables)
    data["raw_tables"] = raw_tables
    data["raw_data_summary"] = raw_data_summary
    data["raw_field_summary"] = raw_field_summary
    with open(OUT / "project_summary.json", "r", encoding="utf-8") as f:
        data["summary_json"] = json.load(f)
    return data

try:
    data = load_all_data()
except Exception as e:
    st.error("Dashboard gagal membaca data output.")
    st.exception(e)
    st.stop()

rfm = data["customer_rfm"]; segment_summary = data["segment_summary"]; monthly = data["monthly"]; customer_product = data["customer_product"]
rules = data["rules"]; nba = data["nba"]; top_products = data["top_products"]; line_items = data["line_items"]; status_summary = data["status_summary"]
preprocessing_audit = data["preprocessing_audit"]; excluded_customers = data["excluded_customers"]; recency_validation = data["recency_validation"]
association_validation = data["association_validation"]; recommendation_evaluation = data["recommendation_evaluation"]; nudge_framework = data["nudge_framework"]
kpi_framework = data["kpi_framework"]; decision_framework = data["decision_framework"]; summary = data["summary_json"]
raw_tables = data["raw_tables"]; raw_data_summary = data["raw_data_summary"]; raw_field_summary = data["raw_field_summary"]

for df in [rfm, segment_summary, monthly, rules, nba, top_products, line_items, nudge_framework]:
    for col in df.columns:
        if col in ["recency_days","frequency","monetary","revenue","quantity","orders","support","confidence","lift","basket_count","priority_score","customers"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

# Sidebar Filter
st.sidebar.title("🧭 Filter Dashboard" if st.session_state.lang == "id" else "🧭 Dashboard Filters")
st.sidebar.caption("Filter diterapkan pada Customer RFM dan Next Best Action." if st.session_state.lang == "id" else "Filters applied to Customer RFM and Next Best Action.")
segments = sorted(rfm["segment"].dropna().unique())
selected_segments = st.sidebar.multiselect("Segment", segments, default=segments)
provinces = sorted(rfm["provinsi"].dropna().unique()) if "provinsi" in rfm.columns else []
selected_provinces = st.sidebar.multiselect("Provinsi" if st.session_state.lang == "id" else "Province", provinces, default=provinces) if provinces else []
rfm_view = rfm[rfm["segment"].isin(selected_segments)].copy()
if selected_provinces: rfm_view = rfm_view[rfm_view["provinsi"].isin(selected_provinces)]
nba_view = nba[nba["segment"].isin(selected_segments)].copy()
if selected_provinces and "provinsi" in nba_view.columns: nba_view = nba_view[nba_view["provinsi"].isin(selected_provinces)]

st.sidebar.divider()
st.sidebar.markdown("### Ringkasan Data" if st.session_state.lang == "id" else "### Data Summary")
st.sidebar.write(f"""
Total pelanggan awal: **{fmt_int(summary.get('raw_customers', 0))}**  
Pelanggan dianalisis: **{fmt_int(summary.get('analyzed_customers', 0))}**  
Valid orders: **{fmt_int(summary.get('valid_non_cancelled_orders', 0))}**  
Valid line items: **{fmt_int(summary.get('valid_line_items', len(line_items) if 'line_items' in globals() else 0))}**
""")

# Header Hero
st.markdown(f"""
<div class="hero">
<h1>{t('title_hero')}</h1>
<p>{t('hero_desc')}</p>
<span class="pill">Customer RFM</span><span class="pill">Association Rule Mining</span><span class="pill">Next Best Action</span><span class="pill">Digital Nudging</span><span class="pill">Business KPI</span>
</div>
""", unsafe_allow_html=True)

# Metric Cards
c1,c2,c3,c4,c5 = st.columns(5)
with c1: metric_card(t("m_raw_cust"), fmt_int(summary["raw_customers"]), t("m_raw_cust_help"))
with c2: metric_card(t("m_analyzed_cust"), fmt_int(summary["analyzed_customers"]), t("m_analyzed_cust_help"))
with c3: metric_card(t("m_audit_cust"), fmt_int(summary["excluded_customers_without_valid_orders"]), t("m_audit_cust_help"))
with c4: metric_card(t("m_valid_orders"), fmt_int(summary["valid_non_cancelled_orders"]), t("m_valid_orders_help"))
with c5: metric_card(t("m_relevance"), f"{summary['recommendation_relevance_rate_pct']}%", t("m_relevance_help"))

# Tabs Initialization
tabs = st.tabs([
    t("tab_exec"), t("tab_val"), t("tab_rfm"), t("tab_prod"), 
    t("tab_assoc"), t("tab_nba"), t("tab_nudge"), t("tab_kpi"), 
    t("tab_exp"), t("tab_guide"), t("tab_raw")
])

# === TAB 0: EXECUTIVE OVERVIEW ===
with tabs[0]:
    section(t("sec_exec_title"), t("sec_exec_desc"))
    
    st.subheader(t("chart_raw_before"))
    rc1, rc2, rc3, rc4 = st.columns(4)
    with rc1: metric_card("Raw Customers" if st.session_state.lang == "en" else "Raw Pelanggan", fmt_int(raw_tables["pelanggan"].shape[0]), f"{raw_tables['pelanggan'].shape[1]} fields")
    with rc2: metric_card("Raw Orders", fmt_int(raw_tables["orders"].shape[0]), f"{raw_tables['orders'].shape[1]} fields")
    with rc3: metric_card("Raw Order Details" if st.session_state.lang == "en" else "Raw Detil Order", fmt_int(raw_tables["detil_order"].shape[0]), f"{raw_tables['detil_order'].shape[1]} fields")
    with rc4: metric_card("Raw Products" if st.session_state.lang == "en" else "Raw Produk", fmt_int(raw_tables["produk"].shape[0]), f"{raw_tables['produk'].shape[1]} fields")
    
    raw_col1, raw_col2 = st.columns(2)
    with raw_col1:
        fig = px.bar(raw_data_summary, x="table_name", y="raw_records", color="table_name", text="raw_records", title=t("chart_raw_before"))
        fig.update_layout(showlegend=False)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with raw_col2:
        fig = px.bar(raw_data_summary, x="table_name", y="fields", color="table_name", text="fields", title=t("chart_raw_fields"))
        fig.update_layout(showlegend=False)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)

    col1,col2 = st.columns(2)
    with col1:
        fig = px.bar(segment_summary, x="segment", y="customers", color="segment", text="customers", title=t("chart_cust_per_seg"), color_discrete_map=SEGMENT_COLORS)
        fig.update_layout(showlegend=False)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col2:
        fig = px.pie(segment_summary, names="segment", values="total_revenue", hole=.45, title=t("chart_rev_share"), color="segment", color_discrete_map=SEGMENT_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
        
    col3,col4 = st.columns(2)
    with col3:
        fig = px.line(monthly, x="month", y="revenue", color="segment", markers=True, title=t("chart_monthly_rev"), color_discrete_map=SEGMENT_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col4:
        fig = px.bar(status_summary, x="status_clean", y="orders", color="valid_for_analysis", text="orders", title=t("chart_order_status"), color_discrete_map=STATUS_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)

# === TAB 1: DATA VALIDATION ===
with tabs[1]:
    section(t("sec_val_title"), t("sec_val_desc"))
    st.subheader("Raw Data Audit Before Preprocessing" if st.session_state.lang == "en" else "Audit Data Mentah Sebelum Preprocessing")
    st.dataframe(raw_data_summary, use_container_width=True, height=180)
    st.subheader("Preprocessing Audit")
    st.dataframe(preprocessing_audit, use_container_width=True, height=360)
    st.subheader("Excluded Customers Audit")
    st.dataframe(excluded_customers, use_container_width=True, height=260)
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Recency Validation")
        st.dataframe(recency_validation, use_container_width=True)
    with col2:
        fig = px.histogram(rfm, x="recency_days", color="segment", title=t("chart_recency_dist"), color_discrete_map=SEGMENT_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)

# === TAB 2: CUSTOMER RFM ===
with tabs[2]:
    section(t("sec_rfm_title"), t("sec_rfm_desc"))
    col1,col2,col3 = st.columns(3)
    with col1:
        fig = px.histogram(rfm_view, x="recency_days", color="segment", title=t("chart_recency_dist"), color_discrete_map=SEGMENT_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col2:
        fig = px.histogram(rfm_view, x="frequency", color="segment", title=t("chart_freq_dist"), color_discrete_map=SEGMENT_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col3:
        fig = px.histogram(rfm_view, x="monetary", color="segment", title=t("chart_monetary_dist"), color_discrete_map=SEGMENT_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    fig = px.scatter(rfm_view, x="recency_days", y="monetary", size="frequency", color="segment", hover_data=["customer_id","customer_name","favorite_category","favorite_product","rfm_score"], title=t("chart_rfm_map"), color_discrete_map=SEGMENT_COLORS)
    st.plotly_chart(plotly_common_layout(fig, height=520), use_container_width=True, theme=None)
    st.subheader("Customer RFM Table")
    st.dataframe(rfm_view.sort_values("rfm_total", ascending=False), use_container_width=True, height=520)

# === TAB 3: PRODUCT & REVENUE ===
with tabs[3]:
    section(t("sec_prod_title"), t("sec_prod_desc"))
    col1,col2 = st.columns(2)
    with col1:
        cat_rev = line_items.groupby("kategori").agg(revenue=("subtotal","sum"), quantity=("quantity","sum"), orders=("order_id","nunique")).reset_index().sort_values("revenue", ascending=False)
        fig = px.bar(cat_rev, x="kategori", y="revenue", color="kategori", text="quantity", title=t("chart_rev_cat"), color_discrete_map=CATEGORY_COLORS)
        fig.update_layout(showlegend=False)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col2:
        fig = px.bar(top_products.head(15), x="product_name", y="revenue", color="kategori", title=t("chart_top_prod"), color_discrete_map=CATEGORY_COLORS)
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    col3,col4 = st.columns(2)
    with col3:
        fav_cat = rfm["favorite_category"].value_counts().reset_index()
        fav_cat.columns = ["favorite_category","customers"]
        fig = px.bar(fav_cat, x="customers", y="favorite_category", color="favorite_category", orientation="h", title=t("chart_fav_cat"), color_discrete_map=CATEGORY_COLORS)
        fig.update_layout(showlegend=False, yaxis_title="favorite_category", xaxis_title="customers")
        st.plotly_chart(plotly_common_layout(fig, height=460), use_container_width=True, theme=None)
    with col4:
        fig = px.scatter(customer_product, x="quantity", y="revenue", color="kategori", hover_data=["customer_id","product_name","segment"], title=t("chart_cust_prod_pattern"), color_discrete_map=CATEGORY_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)

# === TAB 4: ASSOCIATION RULE VALIDATION ===
with tabs[4]:
    section(t("sec_assoc_title"), t("sec_assoc_desc"))
    st.markdown(f"""
    <div class="warn-box"><b>Methodological note:</b> Category rules are used as primary insights. Product rules with basket count ≤ {SPARSE_BASKET_THRESHOLD} or lift &gt; {EXTREME_LIFT_THRESHOLD} are interpreted as exploratory findings.</div>
    """ if st.session_state.lang == "en" else f"""
    <div class="warn-box"><b>Catatan metodologis:</b> rule kategori digunakan sebagai insight utama. Rule produk dengan basket count ≤ {SPARSE_BASKET_THRESHOLD} atau lift &gt; {EXTREME_LIFT_THRESHOLD} dibaca sebagai temuan eksploratif.</div>
    """, unsafe_allow_html=True)
    rules_plot = rules.copy(); rules_plot["reliability_label"] = rules_plot.apply(short_reliability_flag, axis=1)
    st.subheader("Association Rule Validation Summary")
    st.dataframe(association_validation, use_container_width=True)
    col1,col2 = st.columns(2)
    with col1:
        fig = px.scatter(rules_plot, x="support", y="confidence", size="basket_count", color="reliability_label", hover_data=["rule_level","antecedent","consequent","lift","basket_count"], title=t("chart_supp_conf"))
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col2:
        rel = rules_plot["reliability_label"].value_counts().reset_index(); rel.columns=["reliability_label","rules"]
        fig = px.bar(rel, x="rules", y="reliability_label", color="reliability_label", orientation="h", text="rules", title=t("chart_rule_rel"))
        fig.update_layout(yaxis_title="", xaxis_title="Rules Count" if st.session_state.lang == "en" else "Jumlah Rule")
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    st.subheader("Market Basket Rules")
    level_filter = st.multiselect("Rule level", sorted(rules_plot["rule_level"].unique()), default=sorted(rules_plot["rule_level"].unique()))
    rel_filter = st.multiselect("Reliability label", sorted(rules_plot["reliability_label"].unique()), default=sorted(rules_plot["reliability_label"].unique()))
    rules_view = rules_plot[rules_plot["rule_level"].isin(level_filter) & rules_plot["reliability_label"].isin(rel_filter)]
    st.dataframe(rules_view, use_container_width=True, height=520)

# === TAB 5: NEXT BEST ACTION ===
with tabs[5]:
    section(t("sec_nba_title"), t("sec_nba_desc"))
    segment_reco = st.selectbox("Recommended Segment" if st.session_state.lang == "en" else "Segment rekomendasi", ["All" if st.session_state.lang == "en" else "Semua"] + sorted(nba_view["segment"].dropna().unique()))
    nba_filtered = nba_view[nba_view["segment"] == segment_reco].copy() if segment_reco not in ["Semua", "All"] else nba_view.copy()
    col1,col2 = st.columns(2)
    with col1:
        rec_cat = nba_filtered["recommended_category"].value_counts().reset_index(); rec_cat.columns=["recommended_category","customers"]
        fig = px.bar(rec_cat, x="recommended_category", y="customers", color="recommended_category", title=t("chart_rec_cat_dist"), color_discrete_map=CATEGORY_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col2:
        nudge_count = nba_filtered["nudge_type"].value_counts().reset_index(); nudge_count.columns=["nudge_type","customers"]
        fig = px.pie(nudge_count, names="nudge_type", values="customers", hole=.45, title=t("chart_nudge_dist"))
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    st.subheader("Next Best Action Table")
    nba_display = nba_filtered.copy()
    for col in ["cross_sell_product_from_rule", "cross_sell_category_from_rule"]:
        if col in nba_display.columns: nba_display[col] = nba_display[col].apply(clean_empty)
    st.dataframe(nba_display, use_container_width=True, height=560)

# === TAB 6: NUDGE FRAMEWORK ===
with tabs[6]:
    section(t("sec_nudge_title"), t("sec_nudge_desc"))
    st.dataframe(nudge_framework, use_container_width=True, height=360)
    fig = px.bar(nudge_framework, x="customers", y="segment", color="nudge_type", orientation="h", text="customers", title=t("chart_nudge_segment"))
    fig.update_layout(yaxis_title="Segment", xaxis_title="Active Customers Count" if st.session_state.lang == "en" else "Jumlah customer aktif")
    st.plotly_chart(plotly_common_layout(fig, height=430), use_container_width=True, theme=None)

# === TAB 7: KPI & DECISION SUPPORT ===
with tabs[7]:
    section(t("sec_kpi_title"), t("sec_kpi_desc"))
    st.subheader("KPI Framework"); st.dataframe(kpi_framework, use_container_width=True, height=330)
    st.subheader("Decision-Support Framework"); st.dataframe(decision_framework, use_container_width=True, height=280)
    st.subheader("Recommendation Evaluation"); st.dataframe(recommendation_evaluation, use_container_width=True, height=280)
    eval_chart = recommendation_evaluation.copy(); eval_chart["value"] = pd.to_numeric(eval_chart["value"], errors="coerce")
    fig = px.bar(eval_chart.dropna(subset=["value"]), x="metric", y="value", color="evaluation_area", title=t("chart_eval_metrics"))
    fig.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)

# === TAB 8: DATA EXPLORER ===
with tabs[8]:
    section(t("sec_exp_title"), t("sec_exp_desc"))
    tables = {"raw_data_summary":raw_data_summary, "raw_field_summary":raw_field_summary, "raw_pelanggan":raw_tables["pelanggan"], "raw_orders":raw_tables["orders"], "raw_detil_order":raw_tables["detil_order"], "raw_produk":raw_tables["produk"], "customer_rfm":rfm, "excluded_customers":excluded_customers, "segment_summary":segment_summary, "customer_monthly_summary":monthly, "customer_product_summary":customer_product, "market_basket_rules":rules, "next_best_action":nba, "top_products":top_products, "transaction_line_items":line_items, "status_summary":status_summary, "preprocessing_audit":preprocessing_audit, "recency_validation":recency_validation, "association_rule_validation":association_validation, "recommendation_evaluation":recommendation_evaluation, "nudge_framework":nudge_framework, "kpi_framework":kpi_framework, "dashboard_decision_framework":decision_framework, "data_dictionary":data["data_dictionary"]}
    selected_table = st.selectbox("Select Table" if st.session_state.lang == "en" else "Pilih tabel", list(tables.keys()))
    st.markdown(f"<div class='info-box'><b>Table Function:</b> Data processing output table to support dashboard visualization.</div>" if st.session_state.lang == "en" else f"<div class='info-box'><b>Fungsi Tabel:</b> Tabel output pengolahan data untuk mendukung visualisasi dashboard.</div>", unsafe_allow_html=True)
    st.dataframe(tables[selected_table], use_container_width=True, height=580)
    st.download_button(f"Download {selected_table}.csv", tables[selected_table].to_csv(index=False).encode("utf-8"), file_name=f"{selected_table}.csv", mime="text/csv")

# === TAB 9: USER GUIDE ===
with tabs[9]:
    section(t("sec_guide_title"), t("sec_guide_desc"))
    if st.session_state.lang == "en":
        st.markdown("""
        ### Dashboard Menu Summary

        **Executive Overview** displays high-level summary metrics for data counts, customers, orders, segmentation, and key recommendations.

        **Data Validation** displays initial data validation results prior to analytical processing.

        **Customer RFM** presents customer segmentation based on Recency, Frequency, and Monetary metrics.

        **Product & Revenue** displays category and product contributions toward total sales.

        **Association Rule Validation** presents product/category co-purchase patterns derived from transaction data.

        **Next Best Action** provides personalized marketing action recommendations per customer.

        **Nudge Framework** outlines communication approaches tailored to each customer segment.

        **KPI & Decision Support** displays strategic key performance indicators to support decision-making.

        **Data Explorer** allows users to view and download processed data tables.

        **Raw Data Audit** summarizes raw dataset tables prior to preprocessing.
        """)
    else:
        st.markdown("""
        ### Ringkasan Menu Dashboard

        **Executive Overview** menampilkan ringkasan jumlah data, pelanggan, order, segmentasi, dan rekomendasi utama.

        **Data Validation** digunakan untuk melihat hasil validasi data sebelum masuk ke tahap analisis.

        **Customer RFM** menampilkan segmentasi pelanggan berdasarkan Recency, Frequency, dan Monetary.

        **Product & Revenue** menampilkan kontribusi kategori dan produk terhadap penjualan.

        **Association Rule Validation** menampilkan pola hubungan antarproduk atau antarkategori berdasarkan transaksi.

        **Next Best Action** menampilkan rekomendasi tindakan pemasaran untuk setiap pelanggan.

        **Nudge Framework** menampilkan pendekatan komunikasi yang sesuai dengan segmen pelanggan.

        **KPI & Decision Support** menampilkan indikator yang dapat digunakan untuk mendukung keputusan pemasaran.

        **Data Explorer** digunakan untuk membuka dan mengunduh tabel data.

        **Raw Data Audit** menampilkan ringkasan tabel mentah sebelum diproses.
        """)

# === TAB 10: RAW DATA AUDIT ===
with tabs[10]:
    section(t("sec_raw_title"), t("sec_raw_desc"))
    c_raw1, c_raw2, c_raw3, c_raw4 = st.columns(4)
    with c_raw1: metric_card("Customers" if st.session_state.lang == "en" else "Pelanggan", fmt_int(raw_tables["pelanggan"].shape[0]), f"{raw_tables['pelanggan'].shape[1]} fields pada pelanggan.csv")
    with c_raw2: metric_card("Orders", fmt_int(raw_tables["orders"].shape[0]), f"{raw_tables['orders'].shape[1]} fields pada orders.csv")
    with c_raw3: metric_card("Order Details" if st.session_state.lang == "en" else "Detil Order", fmt_int(raw_tables["detil_order"].shape[0]), f"{raw_tables['detil_order'].shape[1]} fields pada detil_order.csv")
    with c_raw4: metric_card("Products" if st.session_state.lang == "en" else "Produk", fmt_int(raw_tables["produk"].shape[0]), f"{raw_tables['produk'].shape[1]} fields pada produk.csv")

    col_a, col_b = st.columns(2)
    with col_a:
        fig = px.bar(raw_data_summary, x="table_name", y="raw_records", color="table_name", text="raw_records", title=t("chart_raw_rec_table"))
        fig.update_layout(showlegend=False, xaxis_title="Raw table", yaxis_title="Records")
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col_b:
        fig = px.bar(raw_data_summary, x="table_name", y="fields", color="table_name", text="fields", title=t("chart_raw_field_table"))
        fig.update_layout(showlegend=False, xaxis_title="Raw table", yaxis_title="Fields")
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)

    st.subheader("Raw Data Summary")
    st.dataframe(raw_data_summary, use_container_width=True, height=190)
    st.subheader("Raw Field Summary")
    st.dataframe(raw_field_summary, use_container_width=True, height=320)

    raw_choice = st.selectbox("Select raw table to view" if st.session_state.lang == "en" else "Pilih raw table untuk ditampilkan", list(raw_tables.keys()))
    st.dataframe(raw_tables[raw_choice], use_container_width=True, height=430)
    st.download_button(f"Download raw_{raw_choice}.csv", raw_tables[raw_choice].to_csv(index=False).encode("utf-8"), file_name=f"raw_{raw_choice}.csv", mime="text/csv")
