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
        raise FileNotFoundError(f"{name} was not found in the outputs folder.")
    return pd.read_csv(path)

def load_raw_csv(name):
    path = RAW_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"{name} was not found in the data folder.")
    return pd.read_csv(path)

def build_raw_audit(raw_tables):
    descriptions = {
        "pelanggan": "Master data pelanggan sebelum filter transaksi valid",
        "orders": "Raw order records sebelum filtering status",
        "detil_order": "Transaction details or line items before preprocessing",
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
            "description": descriptions.get(name, "Raw data before preprocessing")
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
CATEGORY_DISPLAY_NAMES = {
    "Makanan": "Food",
    "Minuman": "Beverage",
    "Alat Tulis": "Stationery",
    "Bayi": "Baby",
    "Perawatan Tubuh": "Personal Care",
    "Rokok": "Cigarettes"
}
STATUS_DISPLAY_NAMES = {
    "selesai": "Completed",
    "dikirim": "Shipped",
    "dibayar": "Paid",
    "dibatalkan": "Cancelled"
}
SEGMENT_DISPLAY_NAMES = {
    "At Risk": "At Risk",
    "Big Spenders": "Big Spenders",
    "Hibernating": "Hibernating",
    "Potential Loyalist": "Potential Loyalist",
    "Champions": "Champions",
    "Loyal Customers": "Loyal Customers"
}

def display_category_map(series):
    return series.map(CATEGORY_DISPLAY_NAMES).fillna(series)

def display_segment_map(series):
    return series.map(SEGMENT_DISPLAY_NAMES).fillna(series)

def display_status_map(series):
    return series.map(STATUS_DISPLAY_NAMES).fillna(series)

SPARSE_BASKET_THRESHOLD = 4
EXTREME_LIFT_THRESHOLD = 10

def clean_empty(value, empty_text="Not available"):
    if pd.isna(value): return empty_text
    value = str(value).strip()
    return value if value else empty_text

def short_reliability_flag(row):
    flag = str(row.get("reliability_flag", "")).lower()
    rule_level = str(row.get("rule_level", "")).lower()
    lift = pd.to_numeric(row.get("lift"), errors="coerce")
    basket_count = pd.to_numeric(row.get("basket_count"), errors="coerce")
    if "stable" in flag and rule_level == "category": return "Stable"
    if ("product" in rule_level) or (pd.notna(lift) and lift > EXTREME_LIFT_THRESHOLD) or (pd.notna(basket_count) and basket_count <= SPARSE_BASKET_THRESHOLD): return "Exploratory"
    return "Needs Validation"

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
        st.info("No province data matches the current filters.")
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
            highest_at_risk["provinsi"] if highest_at_risk is not None else "Not available",
            f"{fmt_int(highest_at_risk['customers'])} pelanggan"
            if highest_at_risk is not None else "No province is dominated by At Risk customers"
        ),
        (
            "🎯 Big Spenders Terbesar",
            highest_big_spenders["provinsi"] if highest_big_spenders is not None else "Not available",
            f"{fmt_int(highest_big_spenders['customers'])} pelanggan"
            if highest_big_spenders is not None else "No province is dominated by Big Spenders customers"
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
    st.error("The dashboard could not read the output data.")
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
st.sidebar.caption("Filters are applied to Customer RFM and Next Best Action.")
segments = sorted(rfm["segment"].dropna().unique())
selected_segments = st.sidebar.multiselect("Segment", segments, default=segments)
provinces = sorted(rfm["provinsi"].dropna().unique()) if "provinsi" in rfm.columns else []
selected_provinces = st.sidebar.multiselect("Province", provinces, default=provinces) if provinces else []
rfm_view = rfm[rfm["segment"].isin(selected_segments)].copy()
if selected_provinces: rfm_view = rfm_view[rfm_view["provinsi"].isin(selected_provinces)]
nba_view = nba[nba["segment"].isin(selected_segments)].copy()
if selected_provinces and "provinsi" in nba_view.columns: nba_view = nba_view[nba_view["provinsi"].isin(selected_provinces)]

st.sidebar.divider()
st.sidebar.markdown("### Ringkasan Data")
st.sidebar.write(f"""
Initial customers: **{fmt_int(summary.get('raw_customers', 0))}**  
Analyzed customers: **{fmt_int(summary.get('analyzed_customers', 0))}**  
Valid orders: **{fmt_int(summary.get('valid_non_cancelled_orders', 0))}**  
Valid line items: **{fmt_int(summary.get('valid_line_items', len(line_items) if 'line_items' in globals() else 0))}**
""")

# Header
st.markdown("""
<div class="hero">
<h1>🛒 Customer ID Recommendation Dashboard</h1>
<p>This dashboard presents customer analysis using <b>Customer RFM</b>, <b>Association Rule Mining</b>, dan <b>Nudge Framework</b> to support data-driven marketing strategy recommendations.</p>
<span class="pill">Customer RFM</span><span class="pill">Association Rule Mining</span><span class="pill">Next Best Action</span><span class="pill">Digital Nudging</span><span class="pill">Business KPI</span>
</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4,c5 = st.columns(5)
with c1: metric_card("Raw Customers", fmt_int(summary["raw_customers"]), "Total pelanggan awal pada dataset.")
with c2: metric_card("Analyzed Customers", fmt_int(summary["analyzed_customers"]), "Number of customers included in the analysis.")
with c3: metric_card("Audit Customers", fmt_int(summary["excluded_customers_without_valid_orders"]), "Number of customers recorded in the data audit.")
with c4: metric_card("Valid Orders", fmt_int(summary["valid_non_cancelled_orders"]), "Order berstatus dibayar, dikirim, dan selesai.")
with c5: metric_card("Relevance Rate", f"{summary['recommendation_relevance_rate_pct']}%", "Rekomendasi sesuai kategori favorit pelanggan aktif.")

tabs = st.tabs(["🏠 Executive Overview", "🧹 Data Validation", "👥 Customer RFM", "📦 Product & Revenue", "🔗 Association Rule Validation", "🎯 Next Best Action", "🧠 Nudge Framework", "📈 KPI & Decision Support", "📋 Data Explorer", "📖 Dashboard Guide", "📥 Raw Data Audit", "🎯 Marketing Decision Center"])

with tabs[0]:
    section("Executive Overview", "Main dashboard summary based on customer data, transactions, RFM segmentation, and marketing recommendations.")
    st.subheader("Raw Data Before Preprocessing")
    rc1, rc2, rc3, rc4 = st.columns(4)
    with rc1: metric_card("Raw Customers", fmt_int(raw_tables["pelanggan"].shape[0]), f"{raw_tables['pelanggan'].shape[1]} fields before preprocessing")
    with rc2: metric_card("Raw Orders", fmt_int(raw_tables["orders"].shape[0]), f"{raw_tables['orders'].shape[1]} fields before status filtering")
    with rc3: metric_card("Raw Order Details", fmt_int(raw_tables["detil_order"].shape[0]), f"{raw_tables['detil_order'].shape[1]} fields before joining and filtering")
    with rc4: metric_card("Raw Products", fmt_int(raw_tables["produk"].shape[0]), f"{raw_tables['produk'].shape[1]} product master fields")
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
        fig = px.bar(segment_summary, x="segment", y="customers", color="segment", text="customers", title="Active Customers by Segment", color_discrete_map=SEGMENT_COLORS)
        fig.update_layout(showlegend=False)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col2:
        segment_chart = segment_summary.copy(); segment_chart["segment_display"] = display_segment_map(segment_chart["segment"]); fig = px.pie(segment_chart, names="segment_display", values="total_revenue", hole=.45, title="Revenue Share by Segment", color="segment_display", color_discrete_map=display_seg_colors)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    col3,col4 = st.columns(2)
    with col3:
        monthly_chart = monthly.copy(); monthly_chart["segment_display"] = display_segment_map(monthly_chart["segment"]); fig = px.line(monthly_chart, x="month", y="revenue", color="segment_display", markers=True, title="Monthly Revenue by Segment", color_discrete_map=display_seg_colors)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col4:
        status_chart = status_summary.copy(); status_chart["status_display"] = display_status_map(status_chart["status_clean"]); fig = px.bar(status_chart, x="status_display", y="orders", color="valid_for_analysis", text="orders", title="Order Status Distribution", color_discrete_map=STATUS_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)


    # === REGIONAL CUSTOMER MARKET MAP ===
    section(
        "Indonesia Customer Market Map",
        "Distribution of active customers by province. Use the metric selector to view customer, revenue, order, or average transaction concentration."
    )

    province_map_data = build_province_map_data(rfm_view)

    if province_map_data.empty:
        st.info("Province data is not available for the current filters.")
    else:
        map_metric_label = st.selectbox(
            "Map Metric",
            ["Customer Count", "Revenue", "Orders", "Average Order Value"],
            key="executive_map_metric"
        )

        metric_config = {
            "Customer Count": ("customers", "Customers"),
            "Revenue": ("revenue", "Revenue"),
            "Orders": ("orders", "Orders"),
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
                "Hover over a province to view customers, revenue, orders, "
                "Average Order Value, and dominant customer segment."
            )

            st.subheader("Regional Marketing Opportunity")
            regional_opportunity_cards(province_map_data)

        except Exception as e:
            st.warning(
                "The province map could not be loaded. Please ensure the application has internet access "
                "to retrieve Indonesia province boundaries."
            )
            st.caption(f"Detail: {e}")
            st.dataframe(
                province_map_data.sort_values("customers", ascending=False),
                use_container_width=True,
                height=300
            )


with tabs[1]:
    section("Data Validation", "Summary of data validation, transaction quality, preprocessing audit, and recency validation.")
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
        fig = px.histogram(rfm, x="recency_days", color="segment", title="Recency Distribution of Active Customers", color_discrete_map=SEGMENT_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)

with tabs[2]:
    section("Customer RFM", "Customer segmentation based on Recency, Frequency, and Monetary, with customer profiles and segment explanations.")
    col1,col2,col3 = st.columns(3)
    with col1:
        rfm_chart = rfm_view.copy(); rfm_chart["segment_display"] = display_segment_map(rfm_chart["segment"]); fig = px.histogram(rfm_chart, x="recency_days", color="segment_display", title="Recency Distribution", color_discrete_map=display_seg_colors)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col2:
        rfm_chart = rfm_view.copy(); rfm_chart["segment_display"] = display_segment_map(rfm_chart["segment"]); fig = px.histogram(rfm_chart, x="frequency", color="segment_display", title="Frequency Distribution", color_discrete_map=display_seg_colors)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col3:
        rfm_chart = rfm_view.copy(); rfm_chart["segment_display"] = display_segment_map(rfm_chart["segment"]); fig = px.histogram(rfm_chart, x="monetary", color="segment_display", title="Monetary Distribution", color_discrete_map=display_seg_colors)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    rfm_scatter = rfm_view.copy(); rfm_scatter["segment_display"] = display_segment_map(rfm_scatter["segment"]); fig = px.scatter(rfm_scatter, x="recency_days", y="monetary", size="frequency", color="segment_display", hover_data=[c for c in ["customer_id","customer_name","favorite_category","favorite_product","rfm_score"] if c in rfm_view.columns], title="Customer RFM Map: Recency vs Monetary", color_discrete_map=display_seg_colors)
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
    section("Product & Revenue", "Visualization of category, product, revenue, and customer purchase contributions.")
    col1,col2 = st.columns(2)
    with col1:
        cat_rev = line_items.groupby("kategori").agg(revenue=("subtotal","sum"), quantity=("quantity","sum"), orders=("order_id","nunique")).reset_index().sort_values("revenue", ascending=False)
        cat_rev["category_display"] = display_category_map(cat_rev["kategori"]); display_cat_colors = {CATEGORY_DISPLAY_NAMES.get(k,k):v for k,v in CATEGORY_COLORS.items()}; fig = px.bar(cat_rev, x="category_display", y="revenue", color="category_display", text="quantity", title="Revenue by Category", color_discrete_map=display_cat_colors)
        fig.update_layout(showlegend=False)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col2:
        top_products_chart = top_products.head(15).copy(); top_products_chart["category_display"] = display_category_map(top_products_chart["kategori"]); fig = px.bar(top_products_chart, x="product_name", y="revenue", color="category_display", title="Top 15 Products by Revenue", color_discrete_map=display_cat_colors)
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    col3,col4 = st.columns(2)
    with col3:
        fav_cat = rfm["favorite_category"].value_counts().reset_index(); fav_cat.columns = ["favorite_category","customers"]
        fav_cat["category_display"] = display_category_map(fav_cat["favorite_category"]); fig = px.bar(fav_cat, x="customers", y="category_display", color="category_display", orientation="h", title="Favorite Category Distribution", color_discrete_map=display_cat_colors)
        fig.update_layout(showlegend=False)
        st.plotly_chart(plotly_common_layout(fig, height=460), use_container_width=True, theme=None)
    with col4:
        product_pattern = customer_product.copy(); product_pattern["category_display"] = display_category_map(product_pattern["kategori"]); fig = px.scatter(product_pattern, x="quantity", y="revenue", color="category_display", hover_data=[c for c in ["customer_id","product_name","segment"] if c in product_pattern.columns], title="Customer Product Purchase Pattern", color_discrete_map=display_cat_colors)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)


with tabs[4]:
    section("Association Rule Validation", "Validation of co-purchase patterns using support, confidence, lift, basket count, and reliability flags.")
    st.markdown(f'<div class="warn-box"><b>Methodological note:</b> category rules are used as the main insight. Rule produk dengan basket count ≤ {SPARSE_BASKET_THRESHOLD} atau lift &gt; {EXTREME_LIFT_THRESHOLD} are interpreted as exploratory findings.</div>', unsafe_allow_html=True)
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
                st.warning("This rule should be interpreted as an exploratory insight because of sparse basket size / extreme lift.")
            else:
                st.success("This rule meets the dashboard reliability label for stronger interpretation.")

    st.subheader("Market Basket Rules")
    level_filter = st.multiselect("Rule level", sorted(rules_plot["rule_level"].unique()), default=sorted(rules_plot["rule_level"].unique()))
    rel_filter = st.multiselect("Reliability label", sorted(rules_plot["reliability_label"].unique()), default=sorted(rules_plot["reliability_label"].unique()))
    rules_view = rules_plot[rules_plot["rule_level"].isin(level_filter) & rules_plot["reliability_label"].isin(rel_filter)]
    st.dataframe(rules_view, use_container_width=True, height=520)

with tabs[5]:
    section("Next Best Action per Active Customer", "Primary recommendations for active customers, with campaign targeting and recommendation rationale.")
    segment_reco = st.selectbox("Recommendation Segment", ["All"] + sorted(nba_view["segment"].dropna().unique()))
    nba_filtered = nba_view[nba_view["segment"] == segment_reco].copy() if segment_reco != "All" else nba_view.copy()
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
        target = st.selectbox("Target Segment", target_segments if target_segments else ["Not available"], key="campaign_target")
        target_df = nba_view[nba_view["segment"] == target].copy() if target_segments else nba_view.copy()
        action_map = {"At Risk":"Win-back campaign", "Big Spenders":"Premium / value expansion", "Potential Loyalist":"Cross-sell / loyalty", "Hibernating":"Re-engagement campaign"}
        action = action_map.get(target, "Targeted marketing")
        coverage = len(target_df) / len(nba_view) * 100 if len(nba_view) else 0
        c1,c2,c3 = st.columns(3)
        with c1: metric_card("Target Customers", fmt_int(len(target_df)), "Customers in selected target segment")
        with c2: metric_card("Recommended Action", action, "Strategy mapped from the dashboard framework")
        with c3: metric_card("Target Share", f"{coverage:.1f}%", "Share of filtered active customers")
        st.markdown(f'<div class="info-box"><b>Campaign direction:</b> {action}. Use the category/product recommendations from NBA as the target message without claiming untested conversion uplift.</div>', unsafe_allow_html=True)
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
    section("Nudge Framework", "Nudges are mapped as communication strategies by active customer segment; the simulator provides recommendations, not evidence of causal effects.")
    st.dataframe(nudge_framework, use_container_width=True, height=300)
    fig = px.bar(nudge_framework, x="customers", y="segment", color="nudge_type", orientation="h", text="customers", title="Customers by Segment and Recommended Nudge")
    st.plotly_chart(plotly_common_layout(fig, height=430), use_container_width=True, theme=None)

    with st.expander("🧠 Nudge Simulator", expanded=True):
        segs = sorted(nudge_framework["segment"].dropna().unique()) if "segment" in nudge_framework.columns else []
        selected_seg = st.selectbox("Select Segment", segs if segs else ["Not available"], key="nudge_segment")
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
        st.caption("This simulator does not claim that a specific nudge increases conversion because the dataset contains no treatment-control experiment.")

    with st.expander("🌳 Nudge Decision Tree"):
        st.markdown("""
        **Customer Segment** → **Marketing Objective** → **Recommended Nudge**

        **At Risk** → Retention → Win-back / Reminder  
        **Big Spenders** → Value Expansion → Premium / Personalized Recommendation  
        **Potential Loyalist** → Growth → Cross-sell / Personalized Recommendation  
        **Hibernating** → Re-engagement → Reminder
        """)

with tabs[7]:
    section("KPI & Decision Support", "KPI and decision frameworks for translating analytical results into marketing decisions.")
    st.subheader("KPI Framework"); st.dataframe(kpi_framework, use_container_width=True, height=300)
    st.subheader("Decision-Support Framework"); st.dataframe(decision_framework, use_container_width=True, height=260)
    st.subheader("Recommendation Evaluation"); st.dataframe(recommendation_evaluation, use_container_width=True, height=260)
    eval_chart = recommendation_evaluation.copy(); eval_chart["value"] = pd.to_numeric(eval_chart["value"], errors="coerce")
    fig = px.bar(eval_chart.dropna(subset=["value"]), x="metric", y="value", color="evaluation_area", title="Evaluation Metrics")
    fig.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)


with tabs[8]:
    section("Data Explorer", "Access processed datasets, including the customer audit table excluded from the main analysis.")
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
    selected_table = st.selectbox("Select table", list(tables.keys()))
    st.markdown(f"<div class='info-box'><b>Table Function:</b> {table_info.get(selected_table, 'Tabel output pengolahan data untuk mendukung visualisasi dashboard.')}</div>", unsafe_allow_html=True)
    st.dataframe(tables[selected_table], use_container_width=True, height=580)
    st.download_button(f"Download {selected_table}.csv", tables[selected_table].to_csv(index=False).encode("utf-8"), file_name=f"{selected_table}.csv", mime="text/csv")


with tabs[9]:
    section("Dashboard Guide Dashboard", "A brief guide to using each menu and understanding the analytical results.")
    steps = [
        ("1", "Validate Data", "Start with Data Validation to review data quality, preprocessing audit, and recency validation."),
        ("2", "Understand Customers", "Use Customer RFM to review segmentation, RFM distributions, and the Customer 360° Profile."),
        ("3", "Understand Products", "Use Product & Revenue to review category and product contributions and customer purchase patterns."),
        ("4", "Validate Product Relationships", "Use Association Rule Validation to review support, confidence, lift, reliability, and Rule Explorer."),
        ("5", "Select Marketing Action", "Use Next Best Action to select a target segment, campaign target, and recommendation rationale."),
        ("6", "Choose Nudge", "Use Nudge Framework to review nudges by segment, try the Nudge Simulator, and read the decision tree."),
        ("7", "Evaluate Decisions", "Use KPI & Decision Support to review the KPI framework, decision framework, and evaluation metrics."),
        ("8", "Make Marketing Decision", "Use Marketing Decision Center to combine segments, actions, rule-linked customers, and recommended nudges."),
        ("9", "Explore Data", "Use Data Explorer and Raw Data Audit to view and download the tables used in the dashboard.")
    ]
    for num, title, desc in steps:
        st.markdown(f"### {num}. {title}")
        st.markdown(desc)

    st.info("Main dashboard flow: **Data Validation → Customer Analysis → Product Analysis → Association Rules → Next Best Action → Digital Nudge → Decision Support**.")

with tabs[10]:
    section("Raw Data Audit", "Summary of the structure and condition of raw data tables before analysis.")
    c_raw1, c_raw2, c_raw3, c_raw4 = st.columns(4)
    with c_raw1: metric_card("Customers", fmt_int(raw_tables["pelanggan"].shape[0]), f"{raw_tables['pelanggan'].shape[1]} fields in Customer data")
    with c_raw2: metric_card("Orders", fmt_int(raw_tables["orders"].shape[0]), f"{raw_tables['orders'].shape[1]} fields in Orders data")
    with c_raw3: metric_card("Order Details", fmt_int(raw_tables["detil_order"].shape[0]), f"{raw_tables['detil_order'].shape[1]} fields in Order Detail data")
    with c_raw4: metric_card("Products", fmt_int(raw_tables["produk"].shape[0]), f"{raw_tables['produk'].shape[1]} fields in Product data")

    st.subheader("Raw Data Summary")
    st.dataframe(raw_data_summary, use_container_width=True, height=190)
    st.subheader("Raw Field Summary")
    st.dataframe(raw_field_summary, use_container_width=True, height=320)
    raw_choice = st.selectbox("Select raw table to display", list(raw_tables.keys()))
    st.dataframe(raw_tables[raw_choice], use_container_width=True, height=430)
    st.download_button(
        f"Download raw_{raw_choice}.csv",
        raw_tables[raw_choice].to_csv(index=False).encode("utf-8"),
        file_name=f"raw_{raw_choice}.csv",
        mime="text/csv"
    )

with tabs[11]:
    section("Marketing Decision Center", "A single decision layer combining RFM, NBA, Association Rules, and Nudges into an easy-to-read marketing decision.")
    target_segments = sorted(rfm_view["segment"].dropna().unique()) if "segment" in rfm_view.columns else []
    selected_target = st.selectbox("Who should we target?", target_segments if target_segments else ["Not available"], key="decision_target")
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


