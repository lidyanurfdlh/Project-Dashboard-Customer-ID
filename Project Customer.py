from pathlib import Path
import json
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import requests

# === DASHBOARD CUSTOMER ID RECOMMENDATION ===
px.defaults.template = "plotly_white"
px.defaults.color_continuous_scale = "Blues"

st.set_page_config(
    page_title="Customer ID Recommendation Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

/* === MULTISELECT FIX: VERSION F, INDONESIAN DASHBOARD === */
[data-testid="stMultiSelect"] [data-baseweb="tag"] {
    position: relative !important;
    z-index: 5 !important;
}
[data-testid="stMultiSelect"] [data-baseweb="tag"] button,
[data-testid="stMultiSelect"] [data-baseweb="tag"] [role="button"] {
    position: relative !important;
    z-index: 20 !important;
    pointer-events: auto !important;
    cursor: pointer !important;
}
[data-testid="stMultiSelect"] [data-baseweb="popover"],
[data-testid="stMultiSelect"] [role="listbox"] {
    z-index: 1000 !important;
}
[data-testid="stMultiSelect"] [role="option"] {
    pointer-events: auto !important;
    cursor: pointer !important;
}

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
        rows.append({
            "table_name": name,
            "raw_records": int(len(df)),
            "fields": int(len(df.columns)),
            "primary_key": primary_keys.get(name, "-"),
            "description": descriptions.get(name, "Raw data sebelum preprocessing")
        })
        for col in df.columns:
            field_rows.append({
                "table_name": name,
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

# === PERBAIKAN FINAL V4 01: WARNA KONSISTEN TANPA NO VALID PURCHASE ===
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
    if "stable" in flag and rule_level == "category": return "Stabil"
    if ("product" in rule_level) or (pd.notna(lift) and lift > EXTREME_LIFT_THRESHOLD) or (pd.notna(basket_count) and basket_count <= SPARSE_BASKET_THRESHOLD): return "Eksploratif"
    return "Perlu Validasi"

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


@st.cache_data(ttl=86400, show_spinner=False)
def load_indonesia_province_geojson():
    """Load the 38-province Indonesia GeoJSON used by the Executive Overview map."""
    url = "https://raw.githubusercontent.com/denyherianto/indonesia-geojson-topojson-maps-with-38-provinces/main/GeoJSON/indonesia-38-provinces.geojson"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.json()


def build_province_map_data(rfm_data):
    """Aggregate the active customer RFM data by province for map metrics."""
    if rfm_data.empty or "provinsi" not in rfm_data.columns:
        return pd.DataFrame()

    work = rfm_data.copy()
    work["monetary"] = pd.to_numeric(work.get("monetary"), errors="coerce").fillna(0)
    work["frequency"] = pd.to_numeric(work.get("frequency"), errors="coerce").fillna(0)

    province = (
        work.groupby("provinsi", dropna=False)
        .agg(
            customers=("customer_id", "nunique"),
            revenue=("monetary", "sum"),
            orders=("frequency", "sum"),
        )
        .reset_index()
    )

    province["aov"] = np.where(
        province["orders"] > 0,
        province["revenue"] / province["orders"],
        0
    )

    dominant = (
        work.dropna(subset=["provinsi"])
        .groupby(["provinsi", "segment"])
        .size()
        .reset_index(name="segment_customers")
        .sort_values(
            ["provinsi", "segment_customers", "segment"],
            ascending=[True, False, True]
        )
        .drop_duplicates("provinsi")
        .rename(columns={"segment": "dominant_segment"})
        [["provinsi", "dominant_segment"]]
    )

    province = province.merge(dominant, on="provinsi", how="left")
    return province


def fmt_currency_short(x):
    try:
        x = float(x)
        if abs(x) >= 1_000_000_000:
            return f"Rp {x/1_000_000_000:.1f} M"
        if abs(x) >= 1_000_000:
            return f"Rp {x/1_000_000:.1f} jt"
        if abs(x) >= 1_000:
            return f"Rp {x/1_000:.1f} rb"
        return f"Rp {x:,.0f}".replace(",", ".")
    except Exception:
        return "Rp 0"


def regional_opportunity_cards(province_data):
    """Show compact regional decision-support highlights below the map."""
    if province_data.empty:
        st.info("Belum ada data provinsi yang sesuai dengan filter saat ini.")
        return

    highest_customers = province_data.loc[province_data["customers"].idxmax()]
    highest_revenue = province_data.loc[province_data["revenue"].idxmax()]

    at_risk = province_data[
        province_data["dominant_segment"].eq("At Risk")
    ]
    big_spenders = province_data[
        province_data["dominant_segment"].eq("Big Spenders")
    ]

    highest_at_risk = (
        at_risk.loc[at_risk["customers"].idxmax()]
        if not at_risk.empty
        else None
    )
    highest_big_spenders = (
        big_spenders.loc[big_spenders["customers"].idxmax()]
        if not big_spenders.empty
        else None
    )

    cards = [
        (
            "👥 Basis Pelanggan Tertinggi",
            highest_customers["provinsi"],
            f"{fmt_int(highest_customers['customers'])} pelanggan"
        ),
        (
            "💰 Revenue Tertinggi",
            highest_revenue["provinsi"],
            fmt_currency_short(highest_revenue["revenue"])
        ),
        (
            "⚠️ At Risk Terbesar",
            highest_at_risk["provinsi"] if highest_at_risk is not None else "Tidak tersedia",
            f"{fmt_int(highest_at_risk['customers'])} pelanggan"
            if highest_at_risk is not None else "Tidak ada provinsi dominan At Risk"
        ),
        (
            "🎯 Big Spenders Terbesar",
            highest_big_spenders["provinsi"] if highest_big_spenders is not None else "Tidak tersedia",
            f"{fmt_int(highest_big_spenders['customers'])} pelanggan"
            if highest_big_spenders is not None else "Tidak ada provinsi dominan Big Spenders"
        ),
    ]

    cols = st.columns(4)
    for col, (label, value, detail) in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div class="metric-card" style="min-height:118px;">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value" style="font-size:22px;">{value}</div>
                    <div class="metric-help">{detail}</div>
                </div>
                """,
                unsafe_allow_html=True
            )



def safe_numeric(df, col, default=0):
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce").fillna(default)
    return pd.Series(default, index=df.index)

def fmt_rupiah(x):
    try:
        return f"Rp {float(x):,.0f}".replace(",", ".")
    except Exception:
        return "Rp 0"

def segment_explanation(row):
    """Rule-of-thumb explanation based only on the available RFM scores."""
    parts = []
    for score, label in [("r_score", "recency"), ("f_score", "frequency"), ("m_score", "monetary")]:
        if score in row.index and pd.notna(row[score]):
            try:
                v = float(row[score])
                parts.append(f"{label.title()} score {v:.0f}/5")
            except Exception:
                pass
    return parts

def build_customer_profile(rfm_data, customer_id):
    if rfm_data.empty or "customer_id" not in rfm_data.columns:
        return None
    hit = rfm_data[rfm_data["customer_id"].astype(str) == str(customer_id)]
    return hit.iloc[0] if not hit.empty else None

def build_segment_priority(rfm_data, nba_data):
    if rfm_data.empty or "segment" not in rfm_data.columns:
        return pd.DataFrame()
    g = rfm_data.groupby("segment", dropna=False).agg(
        customers=("customer_id", "nunique"),
        revenue=("monetary", "sum"),
        avg_recency=("recency_days", "mean"),
        avg_frequency=("frequency", "mean")
    ).reset_index()
    g["revenue_share"] = g["revenue"] / g["revenue"].sum() * 100 if g["revenue"].sum() else 0
    # Transparent prioritization heuristic for dashboard exploration, not a model prediction.
    max_rev = g["revenue"].max() or 1
    max_cust = g["customers"].max() or 1
    g["priority_score"] = ((g["revenue"] / max_rev) * 0.55 + (g["customers"] / max_cust) * 0.45) * 100
    action_map = {
        "At Risk": "Retention / Win-back",
        "Big Spenders": "Value Expansion / Premium",
        "Potential Loyalist": "Cross-sell / Loyalty",
        "Hibernating": "Re-engagement"
    }
    g["recommended_focus"] = g["segment"].map(action_map).fillna("Targeted Marketing")
    return g.sort_values("priority_score", ascending=False)

def build_product_matrix(line_items_data):
    if line_items_data.empty or "product_name" not in line_items_data.columns:
        return pd.DataFrame()
    g = line_items_data.groupby(["product_name", "kategori"], dropna=False).agg(
        revenue=("subtotal", "sum"),
        quantity=("quantity", "sum"),
        orders=("order_id", "nunique")
    ).reset_index()
    return g

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

# === PERBAIKAN FINAL V4 02: FILTER HANYA PELANGGAN AKTIF ===
st.sidebar.title("🧭 Filter Dashboard")
st.sidebar.caption("Filter diterapkan pada Customer RFM dan Next Best Action.")
segments = sorted(rfm["segment"].dropna().unique())
selected_segments = st.sidebar.multiselect("Segment", segments, default=segments)
provinces = sorted(rfm["provinsi"].dropna().unique()) if "provinsi" in rfm.columns else []
selected_provinces = st.sidebar.multiselect("Provinsi", provinces, default=provinces) if provinces else []
rfm_view = rfm[rfm["segment"].isin(selected_segments)].copy()
if selected_provinces: rfm_view = rfm_view[rfm_view["provinsi"].isin(selected_provinces)]
nba_view = nba[nba["segment"].isin(selected_segments)].copy()
if selected_provinces and "provinsi" in nba_view.columns: nba_view = nba_view[nba_view["provinsi"].isin(selected_provinces)]

st.sidebar.divider()
st.sidebar.markdown("### Ringkasan Data")
st.sidebar.write(f"""
Total pelanggan awal: **{fmt_int(summary.get('raw_customers', 0))}**  
Pelanggan dianalisis: **{fmt_int(summary.get('analyzed_customers', 0))}**  
Valid orders: **{fmt_int(summary.get('valid_non_cancelled_orders', 0))}**  
Valid line items: **{fmt_int(summary.get('valid_line_items', len(line_items) if 'line_items' in globals() else 0))}**
""")

# Header
st.markdown("""
<div class="hero">
<h1>🛒 Customer ID Recommendation Dashboard</h1>
<p>Dashboard ini menyajikan analisis pelanggan berbasis <b>Customer RFM</b>, <b>Association Rule Mining</b>, dan <b>Nudge Framework</b> untuk mendukung rekomendasi strategi pemasaran berbasis data transaksi.</p>
<span class="pill">Customer RFM</span><span class="pill">Association Rule Mining</span><span class="pill">Next Best Action</span><span class="pill">Digital Nudging</span><span class="pill">Business KPI</span>
</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4,c5 = st.columns(5)
with c1: metric_card("Raw Customers", fmt_int(summary["raw_customers"]), "Total pelanggan awal pada dataset.")
with c2: metric_card("Analyzed Customers", fmt_int(summary["analyzed_customers"]), "Jumlah pelanggan yang masuk proses analisis.")
with c3: metric_card("Audit Customers", fmt_int(summary["excluded_customers_without_valid_orders"]), "Jumlah pelanggan yang tercatat pada audit data.")
with c4: metric_card("Valid Orders", fmt_int(summary["valid_non_cancelled_orders"]), "Order berstatus dibayar, dikirim, dan selesai.")
with c5: metric_card("Relevance Rate", f"{summary['recommendation_relevance_rate_pct']}%", "Rekomendasi sesuai kategori favorit pelanggan aktif.")

tabs = st.tabs(["🏠 Executive Overview", "🧹 Data Validation", "👥 Customer RFM", "📦 Product & Revenue", "🔗 Association Rule Validation", "🎯 Next Best Action", "🧠 Nudge Framework", "📈 KPI & Decision Support", "📋 Data Explorer", "📖 Panduan Baca", "📥 Raw Data Audit", "🎯 Marketing Decision Center"])

with tabs[0]:
    section("Executive Overview", "Ringkasan utama dashboard berdasarkan data pelanggan, transaksi, segmentasi RFM, dan rekomendasi pemasaran.")
    st.subheader("Raw Data Sebelum Preprocessing")
    rc1, rc2, rc3, rc4 = st.columns(4)
    with rc1: metric_card("Raw Pelanggan", fmt_int(raw_tables["pelanggan"].shape[0]), f"{raw_tables['pelanggan'].shape[1]} fields sebelum preprocessing")
    with rc2: metric_card("Raw Orders", fmt_int(raw_tables["orders"].shape[0]), f"{raw_tables['orders'].shape[1]} fields sebelum filter status")
    with rc3: metric_card("Raw Detil Order", fmt_int(raw_tables["detil_order"].shape[0]), f"{raw_tables['detil_order'].shape[1]} fields sebelum join dan filter")
    with rc4: metric_card("Raw Produk", fmt_int(raw_tables["produk"].shape[0]), f"{raw_tables['produk'].shape[1]} fields master produk")
    raw_col1, raw_col2 = st.columns(2)
    with raw_col1:
        fig = px.bar(raw_data_summary, x="table_name", y="raw_records", color="table_name", text="raw_records", title="Raw Data Records Before Preprocessing")
        fig.update_layout(showlegend=False)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with raw_col2:
        fig = px.bar(raw_data_summary, x="table_name", y="fields", color="table_name", text="fields", title="Number of Fields in Each Raw Table")
        fig.update_layout(showlegend=False)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)

    col1,col2 = st.columns(2)
    with col1:
        fig = px.bar(segment_summary, x="segment", y="customers", color="segment", text="customers", title="Jumlah Pelanggan Aktif per Segmen", color_discrete_map=SEGMENT_COLORS)
        fig.update_layout(showlegend=False)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col2:
        fig = px.pie(segment_summary, names="segment", values="total_revenue", hole=.45, title="Revenue Share by Segment", color="segment", color_discrete_map=SEGMENT_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    col3,col4 = st.columns(2)
    with col3:
        fig = px.line(monthly, x="month", y="revenue", color="segment", markers=True, title="Monthly Revenue by Segment", color_discrete_map=SEGMENT_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col4:
        fig = px.bar(status_summary, x="status_clean", y="orders", color="valid_for_analysis", text="orders", title="Order Status Distribution", color_discrete_map=STATUS_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)


    # === REGIONAL CUSTOMER MARKET MAP ===
    section(
        "Indonesia Customer Market Map",
        "Distribusi pelanggan aktif berdasarkan provinsi. Gunakan pilihan metrik untuk melihat konsentrasi pelanggan, revenue, order, atau nilai transaksi rata-rata."
    )

    province_map_data = build_province_map_data(rfm_view)

    if province_map_data.empty:
        st.info("Data provinsi tidak tersedia pada filter saat ini.")
    else:
        map_metric_label = st.selectbox(
            "Metric Peta",
            ["Customer Count", "Revenue", "Orders", "Average Order Value"],
            key="executive_map_metric"
        )

        metric_config = {
            "Customer Count": ("customers", "Jumlah Pelanggan"),
            "Revenue": ("revenue", "Revenue"),
            "Orders": ("orders", "Jumlah Order"),
            "Average Order Value": ("aov", "Average Order Value"),
        }
        map_column, map_title = metric_config[map_metric_label]

        try:
            indonesia_geojson = load_indonesia_province_geojson()

            # Real geographic basemap + province-level analytical overlay.
            # This gives the dashboard a map-like appearance while keeping the
            # choropleth tied to the actual customer data.
            fig_map = px.choropleth_map(
                province_map_data,
                geojson=indonesia_geojson,
                locations="provinsi",
                featureidkey="properties.PROVINSI",
                color=map_column,
                hover_name="provinsi",
                hover_data={
                    "customers": ":,.0f",
                    "revenue": ":,.0f",
                    "orders": ":,.0f",
                    "aov": ":,.0f",
                    "dominant_segment": True,
                },
                color_continuous_scale="YlGnBu",
                opacity=0.58,
                map_style="open-street-map",
                center={"lat": -2.5, "lon": 118.0},
                zoom=3.75,
                labels={
                    "customers": "Customers",
                    "revenue": "Revenue",
                    "orders": "Orders",
                    "aov": "Average Order Value",
                    "dominant_segment": "Dominant Segment",
                },
            )

            fig_map.update_traces(
                marker_line_color="#173B63",
                marker_line_width=0.8,
                hovertemplate=(
                    "<b>%{hovertext}</b><br>"
                    "Customers: %{customdata[0]:,.0f}<br>"
                    "Revenue: Rp %{customdata[1]:,.0f}<br>"
                    "Orders: %{customdata[2]:,.0f}<br>"
                    "AOV: Rp %{customdata[3]:,.0f}<br>"
                    "Dominant Segment: %{customdata[4]}<extra></extra>"
                )
            )

            fig_map.update_layout(
                height=650,
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor="rgba(255,255,255,0)",
                map=dict(
                    center={"lat": -2.5, "lon": 118.0},
                    zoom=3.75,
                ),
                coloraxis_colorbar=dict(
                    title=map_title,
                    thickness=14,
                    len=0.62,
                    x=0.985,
                    xanchor="right",
                    bgcolor="rgba(255,255,255,.92)",
                    bordercolor="#CBD5E1",
                    borderwidth=1,
                ),
            )

            st.plotly_chart(
                fig_map,
                use_container_width=True,
                theme=None
            )

            st.caption(
                "Hover pada provinsi untuk melihat jumlah pelanggan, revenue, order, "
                "Average Order Value, dan segmen pelanggan dominan."
            )

            st.subheader("Regional Marketing Opportunity")
            regional_opportunity_cards(province_map_data)

        except Exception as e:
            st.warning(
                "Peta provinsi belum dapat dimuat. Pastikan aplikasi memiliki akses internet "
                "untuk mengambil data batas wilayah Indonesia."
            )
            st.caption(f"Detail: {e}")
            st.dataframe(
                province_map_data.sort_values("customers", ascending=False),
                use_container_width=True,
                height=300
            )


with tabs[1]:
    section("Data Validation", "Ringkasan validasi data, kualitas transaksi, preprocessing audit, dan validasi recency.")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Raw Data Audit Before Preprocessing")
        st.dataframe(raw_data_summary, use_container_width=True, height=190)
    with c2:
        st.subheader("Preprocessing Audit")
        st.dataframe(preprocessing_audit, use_container_width=True, height=190)

    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Recency Validation")
        st.dataframe(recency_validation, use_container_width=True)
    with col2:
        fig = px.histogram(rfm, x="recency_days", color="segment", title="Distribusi Recency Pelanggan Aktif", color_discrete_map=SEGMENT_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)

with tabs[2]:
    section("Customer RFM", "Segmentasi pelanggan berdasarkan Recency, Frequency, dan Monetary, dilengkapi customer profile dan alasan segmentasi.")
    col1,col2,col3 = st.columns(3)
    with col1:
        fig = px.histogram(rfm_view, x="recency_days", color="segment", title="Recency Distribution", color_discrete_map=SEGMENT_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col2:
        fig = px.histogram(rfm_view, x="frequency", color="segment", title="Frequency Distribution", color_discrete_map=SEGMENT_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col3:
        fig = px.histogram(rfm_view, x="monetary", color="segment", title="Monetary Distribution", color_discrete_map=SEGMENT_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    fig = px.scatter(rfm_view, x="recency_days", y="monetary", size="frequency", color="segment", hover_data=[c for c in ["customer_id","customer_name","favorite_category","favorite_product","rfm_score"] if c in rfm_view.columns], title="Customer RFM Map: Recency vs Monetary", color_discrete_map=SEGMENT_COLORS)
    st.plotly_chart(plotly_common_layout(fig, height=520), use_container_width=True, theme=None)

    with st.expander("👤 Customer 360° Profile", expanded=True):
        ids = sorted(rfm_view["customer_id"].astype(str).unique()) if "customer_id" in rfm_view.columns else []
        if ids:
            selected_customer = st.selectbox("Select Customer", ids, key="customer360")
            profile = build_customer_profile(rfm_view, selected_customer)
            if profile is not None:
                c1,c2,c3,c4 = st.columns(4)
                with c1: metric_card("Segment", clean_empty(profile.get("segment")), "Current RFM segment")
                with c2: metric_card("Recency", f"{float(profile.get('recency_days',0)):.0f} days", "Days since last valid purchase")
                with c3: metric_card("Frequency", f"{float(profile.get('frequency',0)):.0f} orders", "Valid order frequency")
                with c4: metric_card("Monetary", fmt_rupiah(profile.get("monetary",0)), "Total customer monetary value")
                c5,c6 = st.columns(2)
                with c5:
                    st.markdown(f"**Favorite Category:** {clean_empty(profile.get('favorite_category'))}")
                    st.markdown(f"**Favorite Product:** {clean_empty(profile.get('favorite_product'))}")
                with c6:
                    st.markdown(f"**RFM Score:** {clean_empty(profile.get('rfm_score'))}")
                    reasons = segment_explanation(profile)
                    st.markdown("**Why this segment?** " + ("; ".join(reasons) if reasons else "Based on the calculated RFM profile."))
        else:
            st.info("Tidak ada customer yang tersedia pada filter saat ini.")

    st.subheader("Customer RFM Table")
    st.dataframe(rfm_view.sort_values("rfm_total", ascending=False), use_container_width=True, height=520)

with tabs[3]:
    section("Product & Revenue", "Visualisasi kontribusi kategori, produk, revenue, dan pola pembelian pelanggan.")
    col1,col2 = st.columns(2)
    with col1:
        cat_rev = line_items.groupby("kategori").agg(revenue=("subtotal","sum"), quantity=("quantity","sum"), orders=("order_id","nunique")).reset_index().sort_values("revenue", ascending=False)
        fig = px.bar(cat_rev, x="kategori", y="revenue", color="kategori", text="quantity", title="Revenue by Category", color_discrete_map=CATEGORY_COLORS)
        fig.update_layout(showlegend=False)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col2:
        fig = px.bar(top_products.head(15), x="product_name", y="revenue", color="kategori", title="Top 15 Products by Revenue", color_discrete_map=CATEGORY_COLORS)
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    col3,col4 = st.columns(2)
    with col3:
        fav_cat = rfm["favorite_category"].value_counts().reset_index(); fav_cat.columns = ["favorite_category","customers"]
        fig = px.bar(fav_cat, x="customers", y="favorite_category", color="favorite_category", orientation="h", title="Favorite Category Distribution", color_discrete_map=CATEGORY_COLORS)
        fig.update_layout(showlegend=False)
        st.plotly_chart(plotly_common_layout(fig, height=460), use_container_width=True, theme=None)
    with col4:
        fig = px.scatter(customer_product, x="quantity", y="revenue", color="kategori", hover_data=[c for c in ["customer_id","product_name","segment"] if c in customer_product.columns], title="Customer Product Purchase Pattern", color_discrete_map=CATEGORY_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)


with tabs[4]:
    section("Association Rule Validation", "Validasi pola pembelian bersama menggunakan support, confidence, lift, basket count, dan reliability flag.")
    st.markdown(f'<div class="warn-box"><b>Catatan metodologis:</b> rule kategori digunakan sebagai insight utama. Rule produk dengan basket count ≤ {SPARSE_BASKET_THRESHOLD} atau lift &gt; {EXTREME_LIFT_THRESHOLD} dibaca sebagai temuan eksploratif.</div>', unsafe_allow_html=True)
    rules_plot = rules.copy(); rules_plot["reliability_label"] = rules_plot.apply(short_reliability_flag, axis=1)
    st.subheader("Association Rule Validation Summary")
    st.dataframe(association_validation, use_container_width=True)
    col1,col2 = st.columns(2)
    with col1:
        fig = px.scatter(rules_plot, x="support", y="confidence", size="basket_count", color="reliability_label", hover_data=[c for c in ["rule_level","antecedent","consequent","lift","basket_count"] if c in rules_plot.columns], title="Support vs Confidence by Reliability")
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col2:
        rel = rules_plot["reliability_label"].value_counts().reset_index(); rel.columns=["reliability_label","rules"]
        fig = px.bar(rel, x="rules", y="reliability_label", color="reliability_label", orientation="h", text="rules", title="Rule Reliability Distribution")
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)

    with st.expander("🔎 Rule Explorer", expanded=True):
        if not rules_plot.empty:
            rule_labels = [f"{i}: {r.get('antecedent','?')} → {r.get('consequent','?')}" for i, (_,r) in enumerate(rules_plot.iterrows())]
            idx = st.selectbox("Select Rule", list(range(len(rule_labels))), format_func=lambda i: rule_labels[i], key="rule_explorer")
            row = rules_plot.iloc[idx]
            c1,c2,c3,c4 = st.columns(4)
            with c1: metric_card("Support", f"{float(row.get('support',0))*100:.2f}%", "Share of valid baskets containing the rule")
            with c2: metric_card("Confidence", f"{float(row.get('confidence',0))*100:.2f}%", "Conditional purchase probability")
            with c3: metric_card("Lift", f"{float(row.get('lift',0)):.2f}", "Strength relative to independence")
            with c4: metric_card("Reliability", str(row.get('reliability_label','Needs Validation')), "Dashboard interpretation flag")
            if row.get("reliability_label") == "Eksploratif":
                st.warning("Rule ini sebaiknya dibaca sebagai exploratory insight karena keterbatasan basket size / lift ekstrem.")
            else:
                st.success("Rule ini memenuhi label reliability dashboard untuk interpretasi yang lebih kuat.")

    st.subheader("Market Basket Rules")
    level_filter = st.multiselect("Rule level", sorted(rules_plot["rule_level"].unique()), default=sorted(rules_plot["rule_level"].unique()))
    rel_filter = st.multiselect("Reliability label", sorted(rules_plot["reliability_label"].unique()), default=sorted(rules_plot["reliability_label"].unique()))
    rules_view = rules_plot[rules_plot["rule_level"].isin(level_filter) & rules_plot["reliability_label"].isin(rel_filter)]
    st.dataframe(rules_view, use_container_width=True, height=520)

with tabs[5]:
    section("Next Best Action per Active Customer", "Rekomendasi utama untuk pelanggan aktif, dilengkapi campaign targeting dan alasan rekomendasi.")
    segment_reco = st.selectbox("Segment rekomendasi", ["Semua"] + sorted(nba_view["segment"].dropna().unique()))
    nba_filtered = nba_view[nba_view["segment"] == segment_reco].copy() if segment_reco != "Semua" else nba_view.copy()
    col1,col2 = st.columns(2)
    with col1:
        rec_cat = nba_filtered["recommended_category"].value_counts().reset_index(); rec_cat.columns=["recommended_category","customers"]
        fig = px.bar(rec_cat, x="recommended_category", y="customers", color="recommended_category", title="Recommended Category Distribution", color_discrete_map=CATEGORY_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col2:
        nudge_count = nba_filtered["nudge_type"].value_counts().reset_index(); nudge_count.columns=["nudge_type","customers"]
        fig = px.pie(nudge_count, names="nudge_type", values="customers", hole=.45, title="Nudge Type Distribution")
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)

    with st.expander("🎯 Campaign Builder", expanded=True):
        target_segments = sorted(nba_view["segment"].dropna().unique())
        target = st.selectbox("Target Segment", target_segments if target_segments else ["Tidak tersedia"], key="campaign_target")
        target_df = nba_view[nba_view["segment"] == target].copy() if target_segments else nba_view.copy()
        action_map = {"At Risk":"Win-back campaign", "Big Spenders":"Premium / value expansion", "Potential Loyalist":"Cross-sell / loyalty", "Hibernating":"Re-engagement campaign"}
        action = action_map.get(target, "Targeted marketing")
        coverage = len(target_df) / len(nba_view) * 100 if len(nba_view) else 0
        c1,c2,c3 = st.columns(3)
        with c1: metric_card("Target Customers", fmt_int(len(target_df)), "Customers in selected target segment")
        with c2: metric_card("Recommended Action", action, "Strategy mapped from the dashboard framework")
        with c3: metric_card("Target Share", f"{coverage:.1f}%", "Share of filtered active customers")
        st.markdown(f'<div class="info-box"><b>Campaign direction:</b> {action}. Gunakan rekomendasi kategori/produk dari NBA sebagai target message, tanpa mengklaim conversion uplift yang belum diuji.</div>', unsafe_allow_html=True)
        campaign_cols = [c for c in ["customer_id","segment","provinsi","favorite_category","favorite_product","recommended_category","recommended_product","nudge_type"] if c in target_df.columns]
        if campaign_cols:
            st.dataframe(target_df[campaign_cols], use_container_width=True, height=320)
            st.download_button("Download Campaign Target", target_df[campaign_cols].to_csv(index=False).encode("utf-8"), file_name=f"campaign_{target.replace(' ','_').lower()}.csv", mime="text/csv")

    with st.expander("💡 Why This Recommendation?"):
        if not nba_filtered.empty:
            sample = nba_filtered.iloc[0]
            st.markdown(f"**Customer:** {clean_empty(sample.get('customer_id'))}")
            st.markdown(f"**Segment:** {clean_empty(sample.get('segment'))}")
            st.markdown(f"**Recommended Category:** {clean_empty(sample.get('recommended_category'))}")
            st.markdown(f"**Recommended Product:** {clean_empty(sample.get('recommended_product'))}")
            st.markdown(f"**Nudge:** {clean_empty(sample.get('nudge_type'))}")
            st.markdown("**Rationale:** recommendation follows the customer's RFM segment and available favorite-category / association-rule information in the processed NBA output.")

    st.subheader("Next Best Action Table")
    nba_display = nba_filtered.copy()
    for col in ["cross_sell_product_from_rule", "cross_sell_category_from_rule"]:
        if col in nba_display.columns: nba_display[col] = nba_display[col].apply(clean_empty)
    st.dataframe(nba_display, use_container_width=True, height=560)

with tabs[6]:
    section("Nudge Framework", "Nudge dipetakan sebagai strategi komunikasi per segmen pelanggan aktif; simulator hanya memberi rekomendasi, bukan bukti efek kausal.")
    st.dataframe(nudge_framework, use_container_width=True, height=300)
    fig = px.bar(nudge_framework, x="customers", y="segment", color="nudge_type", orientation="h", text="customers", title="Jumlah Customer per Segment dan Recommended Nudge")
    st.plotly_chart(plotly_common_layout(fig, height=430), use_container_width=True, theme=None)

    with st.expander("🧠 Nudge Simulator", expanded=True):
        segs = sorted(nudge_framework["segment"].dropna().unique()) if "segment" in nudge_framework.columns else []
        selected_seg = st.selectbox("Select Segment", segs if segs else ["Tidak tersedia"], key="nudge_segment")
        nudge_options = sorted(nudge_framework["nudge_type"].dropna().unique()) if "nudge_type" in nudge_framework.columns else []
        selected_nudge = st.selectbox("Select Nudge", nudge_options if nudge_options else ["Personalized Recommendation"], key="nudge_type_sim")
        rationale_map = {
            "At Risk":"Focus on re-engagement and reduce the risk of customer inactivity.",
            "Big Spenders":"Emphasize value, premium offers, and relevant complementary products.",
            "Potential Loyalist":"Encourage deeper engagement through relevant cross-sell or loyalty-oriented recommendations.",
            "Hibernating":"Use a simple reminder or re-engagement message to bring attention back to the store."
        }
        c1,c2 = st.columns(2)
        with c1:
            st.markdown(f"### {selected_seg}")
            st.markdown(rationale_map.get(selected_seg, "Use a targeted communication strategy based on the available customer segment profile."))
        with c2:
            st.markdown(f"### {selected_nudge}")
            st.markdown("**Suggested communication:** Personalized and relevant message based on the customer's available purchase history.")
        st.caption("Simulator ini tidak menyatakan bahwa nudge tertentu meningkatkan conversion karena tidak ada eksperimen treatment-control pada dataset.")

    with st.expander("🌳 Nudge Decision Tree"):
        st.markdown("""
        **Customer Segment** → **Marketing Objective** → **Recommended Nudge**

        **At Risk** → Retention → Win-back / Reminder  
        **Big Spenders** → Value Expansion → Premium / Personalized Recommendation  
        **Potential Loyalist** → Growth → Cross-sell / Personalized Recommendation  
        **Hibernating** → Re-engagement → Reminder
        """)

with tabs[7]:
    section("KPI & Decision Support", "KPI dan kerangka keputusan untuk membantu menerjemahkan hasil analisis menjadi keputusan pemasaran.")
    st.subheader("KPI Framework"); st.dataframe(kpi_framework, use_container_width=True, height=300)
    st.subheader("Decision-Support Framework"); st.dataframe(decision_framework, use_container_width=True, height=260)
    st.subheader("Recommendation Evaluation"); st.dataframe(recommendation_evaluation, use_container_width=True, height=260)
    eval_chart = recommendation_evaluation.copy(); eval_chart["value"] = pd.to_numeric(eval_chart["value"], errors="coerce")
    fig = px.bar(eval_chart.dropna(subset=["value"]), x="metric", y="value", color="evaluation_area", title="Evaluation Metrics")
    fig.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)


with tabs[8]:
    section("Data Explorer", "Akses dataset hasil pengolahan, termasuk tabel audit pelanggan yang dikeluarkan dari analisis utama.")
    tables = {"raw_data_summary":raw_data_summary, "raw_field_summary":raw_field_summary, "raw_pelanggan":raw_tables["pelanggan"], "raw_orders":raw_tables["orders"], "raw_detil_order":raw_tables["detil_order"], "raw_produk":raw_tables["produk"], "customer_rfm":rfm, "excluded_customers":excluded_customers, "segment_summary":segment_summary, "customer_monthly_summary":monthly, "customer_product_summary":customer_product, "market_basket_rules":rules, "next_best_action":nba, "top_products":top_products, "transaction_line_items":line_items, "status_summary":status_summary, "preprocessing_audit":preprocessing_audit, "recency_validation":recency_validation, "association_rule_validation":association_validation, "recommendation_evaluation":recommendation_evaluation, "nudge_framework":nudge_framework, "kpi_framework":kpi_framework, "dashboard_decision_framework":decision_framework, "data_dictionary":data["data_dictionary"]}
    table_info = {
        "customer_rfm": "Berisi hasil segmentasi pelanggan berdasarkan RFM.",
        "excluded_customers": "Berisi tabel audit pelanggan.",
        "next_best_action": "Berisi rekomendasi produk dan nudge untuk pelanggan.",
        "market_basket_rules": "Berisi aturan asosiasi kategori dan produk berdasarkan transaksi valid.",
        "raw_data_summary": "Ringkasan jumlah record dan jumlah field pada setiap tabel mentah sebelum preprocessing.",
        "raw_field_summary": "Daftar nama field, tipe data, missing value, dan unique value pada tabel mentah.",
        "raw_orders": "Tabel orders mentah sebelum status dibersihkan dan sebelum valid-order filtering.",
        "raw_detil_order": "Tabel detail order mentah sebelum join dengan orders dan produk.",
        "raw_pelanggan": "Tabel pelanggan mentah sebelum pemilihan active customers.",
        "raw_produk": "Tabel produk mentah sebelum join ke detail order.",
    }
    selected_table = st.selectbox("Pilih tabel", list(tables.keys()))
    st.markdown(f"<div class='info-box'><b>Fungsi Tabel:</b> {table_info.get(selected_table, 'Tabel output pengolahan data untuk mendukung visualisasi dashboard.')}</div>", unsafe_allow_html=True)
    st.dataframe(tables[selected_table], use_container_width=True, height=580)
    st.download_button(f"Download {selected_table}.csv", tables[selected_table].to_csv(index=False).encode("utf-8"), file_name=f"{selected_table}.csv", mime="text/csv")


with tabs[9]:
    section("Panduan Baca Dashboard", "Panduan singkat untuk menggunakan setiap menu dan memahami hasil analisis.")
    steps = [
        ("1", "Validate Data", "Mulai dari Data Validation untuk melihat kualitas data, preprocessing audit, dan validasi recency."),
        ("2", "Understand Customers", "Gunakan Customer RFM untuk melihat segmentasi, distribusi RFM, dan Customer 360° Profile."),
        ("3", "Understand Products", "Gunakan Product & Revenue untuk melihat kontribusi kategori, produk, dan pola pembelian pelanggan."),
        ("4", "Validate Product Relationships", "Gunakan Association Rule Validation untuk melihat support, confidence, lift, reliability, dan Rule Explorer."),
        ("5", "Select Marketing Action", "Gunakan Next Best Action untuk memilih target segment, campaign target, dan alasan rekomendasi."),
        ("6", "Choose Nudge", "Gunakan Nudge Framework untuk melihat nudge per segmen, mencoba Nudge Simulator, dan membaca decision tree."),
        ("7", "Evaluate Decisions", "Gunakan KPI & Decision Support untuk melihat KPI framework, decision framework, dan evaluation metrics."),
        ("8", "Make Marketing Decision", "Gunakan Marketing Decision Center untuk menggabungkan segment, action, rule-linked customers, dan recommended nudge."),
        ("9", "Explore Data", "Gunakan Data Explorer dan Raw Data Audit untuk melihat serta mengunduh tabel yang digunakan dalam dashboard.")
    ]
    for num, title, desc in steps:
        st.markdown(f"### {num}. {title}")
        st.markdown(desc)

    st.info("Alur utama dashboard: **Data Validation → Customer Analysis → Product Analysis → Association Rules → Next Best Action → Digital Nudge → Decision Support**.")

with tabs[10]:
    section("Raw Data Audit", "Ringkasan struktur dan kondisi tabel data mentah sebelum digunakan dalam analisis.")
    c_raw1, c_raw2, c_raw3, c_raw4 = st.columns(4)
    with c_raw1: metric_card("Customers", fmt_int(raw_tables["pelanggan"].shape[0]), f"{raw_tables['pelanggan'].shape[1]} fields pada pelanggan.csv")
    with c_raw2: metric_card("Orders", fmt_int(raw_tables["orders"].shape[0]), f"{raw_tables['orders'].shape[1]} fields pada orders.csv")
    with c_raw3: metric_card("Order Details", fmt_int(raw_tables["detil_order"].shape[0]), f"{raw_tables['detil_order'].shape[1]} fields pada detil_order.csv")
    with c_raw4: metric_card("Products", fmt_int(raw_tables["produk"].shape[0]), f"{raw_tables['produk'].shape[1]} fields pada produk.csv")

    st.subheader("Raw Data Summary")
    st.dataframe(raw_data_summary, use_container_width=True, height=190)
    st.subheader("Raw Field Summary")
    st.dataframe(raw_field_summary, use_container_width=True, height=320)
    raw_choice = st.selectbox("Pilih raw table untuk ditampilkan", list(raw_tables.keys()))
    st.dataframe(raw_tables[raw_choice], use_container_width=True, height=430)
    st.download_button(
        f"Download raw_{raw_choice}.csv",
        raw_tables[raw_choice].to_csv(index=False).encode("utf-8"),
        file_name=f"raw_{raw_choice}.csv",
        mime="text/csv"
    )

with tabs[11]:
    section("Marketing Decision Center", "Tempat menggabungkan RFM, NBA, Association Rule, dan Nudge menjadi satu keputusan pemasaran yang mudah dibaca.")
    target_segments = sorted(rfm_view["segment"].dropna().unique()) if "segment" in rfm_view.columns else []
    selected_target = st.selectbox("Who should we target?", target_segments if target_segments else ["Tidak tersedia"], key="decision_target")
    target_rfm = rfm_view[rfm_view["segment"] == selected_target].copy() if target_segments else rfm_view.copy()
    target_nba = nba_view[nba_view["segment"] == selected_target].copy() if "segment" in nba_view.columns else nba_view.copy()
    action_map = {"At Risk":"Win-back / Retention", "Big Spenders":"Premium / Value Expansion", "Potential Loyalist":"Cross-sell / Loyalty", "Hibernating":"Re-engagement"}
    action = action_map.get(selected_target, "Targeted Marketing")
    recommended_nudge = "Personalized Recommendation"
    if not nudge_framework.empty and "segment" in nudge_framework.columns:
        n = nudge_framework[nudge_framework["segment"].astype(str) == str(selected_target)]
        if not n.empty and "nudge_type" in n.columns:
            recommended_nudge = str(n.iloc[0]["nudge_type"])
    relevant_rule_count = 0
    if not target_nba.empty:
        for col in ["cross_sell_product_from_rule", "cross_sell_category_from_rule"]:
            if col in target_nba.columns:
                relevant_rule_count = max(relevant_rule_count, int(target_nba[col].notna().sum()))
    c1,c2,c3,c4 = st.columns(4)
    with c1: metric_card("Target Customers", fmt_int(len(target_rfm)), "Customers in selected RFM segment")
    with c2: metric_card("Marketing Action", action, "Recommended action mapped from segment")
    with c3: metric_card("Rule-linked Customers", fmt_int(relevant_rule_count), "Customers with available cross-sell rule information")
    with c4: metric_card("Recommended Nudge", recommended_nudge, "Nudge mapped from the framework")

    st.subheader("Why this decision?")
    reasons = {
        "At Risk": "Prioritize retention because customers are in a risk-oriented RFM segment.",
        "Big Spenders": "Prioritize value expansion because this segment contributes relatively high monetary value.",
        "Potential Loyalist": "Prioritize cross-sell and loyalty because customers show promising engagement.",
        "Hibernating": "Prioritize re-engagement because customers have low recent activity."
    }
    st.markdown(reasons.get(selected_target, "Decision is based on the available customer segment profile and processed recommendation outputs."))

    if not target_nba.empty:
        display_cols = [c for c in ["customer_id","favorite_category","favorite_product","recommended_category","recommended_product","nudge_type"] if c in target_nba.columns]
        st.subheader("Target Customer Actions")
        if display_cols:
            st.dataframe(target_nba[display_cols], use_container_width=True, height=360)
    st.warning("Decision Center is a descriptive decision-support layer. It does not predict campaign conversion or causal treatment effects.")

