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

.stMultiSelect [data-baseweb="value-container"] {
    overflow:visible !important;
    flex-wrap:wrap !important;
}

.stMultiSelect [data-baseweb="select"] {
    overflow:visible !important;
}
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
p,li,label {color:#334155;} [data-testid="stMarkdownContainer"] {color:#334155;} hr {border-color:#DBEAFE !important;}
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

# === ENGLISH DISPLAY LABELS FOR FIGURES ===
# These mappings only change labels shown in charts.
# Original dataset values and analytical logic remain unchanged.
TABLE_DISPLAY_NAMES = {
    "pelanggan": "Customer",
    "orders": "Orders",
    "detil_order": "Order Detail",
    "produk": "Product"
}

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
    raw_data_summary_display = raw_data_summary.copy()
    raw_data_summary_display["table_name"] = raw_data_summary_display["table_name"].map(TABLE_DISPLAY_NAMES).fillna(raw_data_summary_display["table_name"])
    raw_field_summary_display = raw_field_summary.copy()
    raw_field_summary_display["table_name"] = raw_field_summary_display["table_name"].map(TABLE_DISPLAY_NAMES).fillna(raw_field_summary_display["table_name"])
    data["raw_tables"] = raw_tables
    data["raw_data_summary"] = raw_data_summary
    data["raw_field_summary"] = raw_field_summary
    data["raw_data_summary_display"] = raw_data_summary_display
    data["raw_field_summary_display"] = raw_field_summary_display
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
raw_tables = data["raw_tables"]; raw_data_summary = data["raw_data_summary"]; raw_field_summary = data["raw_field_summary"]; raw_data_summary_display = data["raw_data_summary_display"]; raw_field_summary_display = data["raw_field_summary_display"]

for df in [rfm, segment_summary, monthly, rules, nba, top_products, line_items, nudge_framework]:
    for col in df.columns:
        if col in ["recency_days","frequency","monetary","revenue","quantity","orders","support","confidence","lift","basket_count","priority_score","customers"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

# === PERBAIKAN FINAL V4 02: FILTER HANYA PELANGGAN AKTIF ===
st.sidebar.title("🧭 Dashboard Filters")
st.sidebar.caption("Filters are applied to Customer RFM and Next Best Action.")
segments = sorted(rfm["segment"].dropna().unique())
selected_segments = st.sidebar.multiselect("Segment", segments, default=segments)
provinces = sorted(rfm["provinsi"].dropna().unique()) if "provinsi" in rfm.columns else []
selected_provinces = st.sidebar.multiselect("Provinsi", provinces, default=provinces) if provinces else []
rfm_view = rfm[rfm["segment"].isin(selected_segments)].copy()
if selected_provinces: rfm_view = rfm_view[rfm_view["provinsi"].isin(selected_provinces)]
nba_view = nba[nba["segment"].isin(selected_segments)].copy()
if selected_provinces and "provinsi" in nba_view.columns: nba_view = nba_view[nba_view["provinsi"].isin(selected_provinces)]

st.sidebar.divider()
st.sidebar.markdown("### Data Summary")
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
<p>This dashboard presents customer analysis using <b>Customer RFM</b>, <b>Association Rule Mining</b>, and <b>Nudge Framework</b> to support data-driven marketing strategy recommendations.</p>
<span class="pill">Customer RFM</span><span class="pill">Association Rule Mining</span><span class="pill">Next Best Action</span><span class="pill">Digital Nudging</span><span class="pill">Business KPI</span>
</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4,c5 = st.columns(5)
with c1: metric_card("Raw Customers", fmt_int(summary["raw_customers"]), "Total customers in the original dataset.")
with c2: metric_card("Analyzed Customers", fmt_int(summary["analyzed_customers"]), "Number of customers included in the analysis.")
with c3: metric_card("Audit Customers", fmt_int(summary["excluded_customers_without_valid_orders"]), "Number of customers recorded in the data audit.")
with c4: metric_card("Valid Orders", fmt_int(summary["valid_non_cancelled_orders"]), "Orders with paid, shipped, and completed status.")
with c5: metric_card("Relevance Rate", f"{summary['recommendation_relevance_rate_pct']}%", "Recommendations aligned with active customers’ favorite categories.")

tabs = st.tabs(["🏠 Executive Overview", "🧹 Data Validation", "👥 Customer RFM", "📦 Product & Revenue", "🔗 Association Rule Validation", "🎯 Next Best Action", "🧠 Nudge Framework", "📈 KPI & Decision Support", "📋 Data Explorer", "📖 Dashboard Guide", "📥 Raw Data Audit"])

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
        raw_chart = raw_data_summary.copy()
        raw_chart["table_name_display"] = raw_chart["table_name"].map(TABLE_DISPLAY_NAMES).fillna(raw_chart["table_name"])
        fig = px.bar(
            raw_chart, x="table_name_display", y="raw_records",
            color="table_name_display", text="raw_records",
            title="Raw Data Records Before Preprocessing"
        )
        fig.update_layout(showlegend=False, xaxis_title="Raw Table", yaxis_title="Records")
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with raw_col2:
        raw_chart = raw_data_summary.copy()
        raw_chart["table_name_display"] = raw_chart["table_name"].map(TABLE_DISPLAY_NAMES).fillna(raw_chart["table_name"])
        fig = px.bar(
            raw_chart, x="table_name_display", y="fields",
            color="table_name_display", text="fields",
            title="Number of Fields in Each Raw Table"
        )
        fig.update_layout(showlegend=False, xaxis_title="Raw Table", yaxis_title="Fields")
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)

    col1,col2 = st.columns(2)
    with col1:
        fig = px.bar(segment_summary, x="segment", y="customers", color="segment", text="customers", title="Active Customers by Segment", color_discrete_map=SEGMENT_COLORS)
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
        status_chart = status_summary.copy()
        status_chart["status_display"] = status_chart["status_clean"].map(STATUS_DISPLAY_NAMES).fillna(status_chart["status_clean"])
        fig = px.bar(
            status_chart, x="status_display", y="orders",
            color="valid_for_analysis", text="orders",
            title="Order Status Distribution",
            color_discrete_map=STATUS_COLORS
        )
        fig.update_layout(xaxis_title="Order Status", yaxis_title="Orders")
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)

with tabs[1]:
    section("Data Validation", "Summary of data validation, transaction status, audited customers, and recency before analysis.")
    st.subheader("Raw Data Audit Before Preprocessing")
    st.dataframe(raw_data_summary_display, use_container_width=True, height=180)
    st.subheader("Preprocessing Audit")
    st.dataframe(preprocessing_audit, use_container_width=True, height=360)
    st.subheader("Excluded Customers Audit")
    st.dataframe(excluded_customers, use_container_width=True, height=260)
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Recency Validation")
        st.dataframe(recency_validation, use_container_width=True)
    with col2:
        fig = px.histogram(rfm, x="recency_days", color="segment", title="Recency Distribution of Active Customers", color_discrete_map=SEGMENT_COLORS)
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)

with tabs[2]:
    section("Customer RFM", "Segmentasi pelanggan berdasarkan Recency, Frequency, dan Monetary.")
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
    fig = px.scatter(rfm_view, x="recency_days", y="monetary", size="frequency", color="segment", hover_data=["customer_id","customer_name","favorite_category","favorite_product","rfm_score"], title="Customer RFM Map: Recency vs Monetary", color_discrete_map=SEGMENT_COLORS)
    st.plotly_chart(plotly_common_layout(fig, height=520), use_container_width=True, theme=None)
    st.subheader("Customer RFM Table")
    st.dataframe(rfm_view.sort_values("rfm_total", ascending=False), use_container_width=True, height=520)

with tabs[3]:
    section("Product & Revenue", "Visualization of category and product contributions and customer purchase patterns.")
    col1,col2 = st.columns(2)
    with col1:
        cat_rev = line_items.groupby("kategori").agg(
            revenue=("subtotal","sum"),
            quantity=("quantity","sum"),
            orders=("order_id","nunique")
        ).reset_index().sort_values("revenue", ascending=False)
        cat_rev["category_display"] = cat_rev["kategori"].map(CATEGORY_DISPLAY_NAMES).fillna(cat_rev["kategori"])
        display_category_colors = {
            CATEGORY_DISPLAY_NAMES.get(k, k): v for k, v in CATEGORY_COLORS.items()
        }
        fig = px.bar(
            cat_rev, x="category_display", y="revenue",
            color="category_display", text="quantity",
            title="Revenue by Category",
            color_discrete_map=display_category_colors
        )
        fig.update_layout(showlegend=False, xaxis_title="Category", yaxis_title="Revenue")
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col2:
        top_products_chart = top_products.head(15).copy()
        top_products_chart["category_display"] = top_products_chart["kategori"].map(CATEGORY_DISPLAY_NAMES).fillna(top_products_chart["kategori"])
        fig = px.bar(
            top_products_chart,
            x="product_name",
            y="revenue",
            color="category_display",
            title="Top 15 Products by Revenue",
            color_discrete_map=display_category_colors,
            hover_data={"category_display": True, "kategori": False}
        )
        fig.update_layout(
            xaxis_tickangle=-35,
            xaxis_title="Product",
            yaxis_title="Revenue"
        )
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Category=%{customdata[0]}<br>Revenue=%{y:$,.0f}<extra></extra>"
        )
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    col3,col4 = st.columns(2)
    with col3:
        fav_cat = rfm["favorite_category"].value_counts().reset_index()
        fav_cat.columns = ["favorite_category","customers"]
        fav_cat["category_display"] = fav_cat["favorite_category"].map(CATEGORY_DISPLAY_NAMES).fillna(fav_cat["favorite_category"])
        fig = px.bar(
            fav_cat, x="customers", y="category_display",
            color="category_display", orientation="h",
            title="Favorite Category Distribution",
            color_discrete_map=display_category_colors
        )
        fig.update_layout(showlegend=False, yaxis_title="Category", xaxis_title="Customers")
        st.plotly_chart(plotly_common_layout(fig, height=460), use_container_width=True, theme=None)
    with col4:
        product_pattern = customer_product.copy()
        product_pattern["category_display"] = product_pattern["kategori"].map(CATEGORY_DISPLAY_NAMES).fillna(product_pattern["kategori"])
        fig = px.scatter(
            product_pattern, x="quantity", y="revenue",
            color="category_display",
            hover_data=["customer_id","product_name","segment"],
            title="Customer Product Purchase Pattern",
            color_discrete_map=display_category_colors
        )
        fig.update_layout(xaxis_title="Quantity", yaxis_title="Revenue")
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)

with tabs[4]:
    section("Association Rule Validation", "Validation of co-purchase patterns using support, confidence, lift, and basket count.")
    st.markdown(f"""
    <div class="warn-box"><b>Methodological note:</b> category rules are used as the main insight. Product rules with basket count ≤ {SPARSE_BASKET_THRESHOLD} or lift &gt; {EXTREME_LIFT_THRESHOLD} dibaca sebagai temuan eksploratif.</div>
    """, unsafe_allow_html=True)
    rules_plot = rules.copy(); rules_plot["reliability_label"] = rules_plot.apply(short_reliability_flag, axis=1)
    st.subheader("Association Rule Validation Summary")
    st.dataframe(association_validation, use_container_width=True)
    col1,col2 = st.columns(2)
    with col1:
        fig = px.scatter(rules_plot, x="support", y="confidence", size="basket_count", color="reliability_label", hover_data=["rule_level","antecedent","consequent","lift","basket_count"], title="Support vs Confidence by Reliability")
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col2:
        rel = rules_plot["reliability_label"].value_counts().reset_index(); rel.columns=["reliability_label","rules"]
        fig = px.bar(rel, x="rules", y="reliability_label", color="reliability_label", orientation="h", text="rules", title="Rule Reliability Distribution")
        fig.update_layout(yaxis_title="", xaxis_title="Number of Rules")
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    st.subheader("Market Basket Rules")
    level_filter = st.multiselect("Rule level", sorted(rules_plot["rule_level"].unique()), default=sorted(rules_plot["rule_level"].unique()))
    rel_filter = st.multiselect("Reliability label", sorted(rules_plot["reliability_label"].unique()), default=sorted(rules_plot["reliability_label"].unique()))
    rules_view = rules_plot[rules_plot["rule_level"].isin(level_filter) & rules_plot["reliability_label"].isin(rel_filter)]
    st.dataframe(rules_view, use_container_width=True, height=520)

with tabs[5]:
    section("Next Best Action per Active Customer", "Primary recommendations are provided only for active customers with valid favorite categories.")
    segment_reco = st.selectbox("Recommendation segment", ["All"] + sorted(nba_view["segment"].dropna().unique()))
    nba_filtered = nba_view[nba_view["segment"] == segment_reco].copy() if segment_reco != "All" else nba_view.copy()
    col1,col2 = st.columns(2)
    with col1:
        rec_cat = nba_filtered["recommended_category"].value_counts().reset_index()
        rec_cat.columns=["recommended_category","customers"]
        rec_cat["category_display"] = rec_cat["recommended_category"].map(CATEGORY_DISPLAY_NAMES).fillna(rec_cat["recommended_category"])
        fig = px.bar(
            rec_cat, x="category_display", y="customers",
            color="category_display",
            title="Recommended Category Distribution",
            color_discrete_map=display_category_colors
        )
        fig.update_layout(xaxis_title="Recommended Category", yaxis_title="Customers")
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col2:
        nudge_count = nba_filtered["nudge_type"].value_counts().reset_index(); nudge_count.columns=["nudge_type","customers"]
        fig = px.pie(nudge_count, names="nudge_type", values="customers", hole=.45, title="Nudge Type Distribution")
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    st.subheader("Next Best Action Table")
    nba_display = nba_filtered.copy()
    for col in ["cross_sell_product_from_rule", "cross_sell_category_from_rule"]:
        if col in nba_display.columns: nba_display[col] = nba_display[col].apply(clean_empty)
    st.dataframe(nba_display, use_container_width=True, height=560)

with tabs[6]:
    section("Nudge Framework", "Nudges are presented as segment-based strategies rather than numerical category charts.")
    st.dataframe(nudge_framework, use_container_width=True, height=360)
    fig = px.bar(nudge_framework, x="customers", y="segment", color="nudge_type", orientation="h", text="customers", title="Customers by Segment and Recommended Nudge")
    fig.update_layout(yaxis_title="Segment", xaxis_title="Active Customers")
    st.plotly_chart(plotly_common_layout(fig, height=430), use_container_width=True, theme=None)

with tabs[7]:
    section("KPI & Decision Support", "KPI and decision framework for evaluating recommendation strategies for active customers.")
    st.subheader("KPI Framework"); st.dataframe(kpi_framework, use_container_width=True, height=330)
    st.subheader("Decision-Support Framework"); st.dataframe(decision_framework, use_container_width=True, height=280)
    st.subheader("Recommendation Evaluation"); st.dataframe(recommendation_evaluation, use_container_width=True, height=280)
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
    st.markdown(f"<div class='info-box'><b>Table Function:</b> {table_info.get(selected_table, 'Processed data table used to support dashboard visualizations.')}</div>", unsafe_allow_html=True)
    st.dataframe(tables[selected_table], use_container_width=True, height=580)
    st.download_button(f"Download {selected_table}.csv", tables[selected_table].to_csv(index=False).encode("utf-8"), file_name=f"{selected_table}.csv", mime="text/csv")

with tabs[9]:
    section("Dashboard Guide Dashboard", "A brief guide to reading each main dashboard module.")

    st.markdown("""
    ### Dashboard Menu Summary

    **Executive Overview** shows a summary of data volume, customers, orders, segmentation, and key recommendations.

    **Data Validation** is used to review data validation results before analysis.

    **Customer RFM** shows customer segmentation based on Recency, Frequency, and Monetary.

    **Product & Revenue** shows category and product contributions to sales.

    **Association Rule Validation** shows relationships among products or categories based on transactions.

    **Next Best Action** shows recommended marketing actions for each customer.

    **Nudge Framework** shows communication approaches appropriate for each customer segment.

    **KPI & Decision Support** shows indicators that can support marketing decisions.

    **Data Explorer** is used to open and download data tables.

    **Raw Data Audit** shows a summary of raw tables before processing.
    """)


with tabs[10]:
    section("Raw Data Audit", "Summary of records and fields in each raw data table.")
    c_raw1, c_raw2, c_raw3, c_raw4 = st.columns(4)
    with c_raw1: metric_card("Customers", fmt_int(raw_tables["pelanggan"].shape[0]), f"{raw_tables['pelanggan'].shape[1]} fields in pelanggan.csv")
    with c_raw2: metric_card("Orders", fmt_int(raw_tables["orders"].shape[0]), f"{raw_tables['orders'].shape[1]} fields in orders.csv")
    with c_raw3: metric_card("Order Details", fmt_int(raw_tables["detil_order"].shape[0]), f"{raw_tables['detil_order'].shape[1]} fields in detil_order.csv")
    with c_raw4: metric_card("Products", fmt_int(raw_tables["produk"].shape[0]), f"{raw_tables['produk'].shape[1]} fields in produk.csv")

    col_a, col_b = st.columns(2)
    with col_a:
        raw_audit_chart = raw_data_summary.copy()
        raw_audit_chart["table_name_display"] = raw_audit_chart["table_name"].map(TABLE_DISPLAY_NAMES).fillna(raw_audit_chart["table_name"])
        fig = px.bar(
            raw_audit_chart, x="table_name_display", y="raw_records",
            color="table_name_display", text="raw_records",
            title="Raw Records by Table"
        )
        fig.update_layout(showlegend=False, xaxis_title="Raw Table", yaxis_title="Records")
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)
    with col_b:
        raw_audit_chart = raw_data_summary.copy()
        raw_audit_chart["table_name_display"] = raw_audit_chart["table_name"].map(TABLE_DISPLAY_NAMES).fillna(raw_audit_chart["table_name"])
        fig = px.bar(
            raw_audit_chart, x="table_name_display", y="fields",
            color="table_name_display", text="fields",
            title="Raw Fields by Table"
        )
        fig.update_layout(showlegend=False, xaxis_title="Raw Table", yaxis_title="Fields")
        st.plotly_chart(plotly_common_layout(fig), use_container_width=True, theme=None)

    st.subheader("Raw Data Summary")
    st.dataframe(raw_data_summary_display, use_container_width=True, height=190)
    st.subheader("Raw Field Summary")
    st.dataframe(raw_field_summary_display, use_container_width=True, height=320)

    raw_choice = st.selectbox("Select raw table to display", list(raw_tables.keys()))
    st.dataframe(raw_tables[raw_choice], use_container_width=True, height=430)
    st.download_button(f"Download raw_{raw_choice}.csv", raw_tables[raw_choice].to_csv(index=False).encode("utf-8"), file_name=f"raw_{raw_choice}.csv", mime="text/csv")




