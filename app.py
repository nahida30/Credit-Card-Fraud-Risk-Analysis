import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# ---------------------------------------------------------
# 1. Page Configuration & Custom Theme Layer
# ---------------------------------------------------------
st.set_page_config(
    page_title="Credit Card Fraud Risk Analysis Dashboard", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Dark theme visual layout mimicking the original Power BI styling
st.markdown("""
    <style>
    body { background-color: #121212; color: #FFFFFF; }
    .stApp { background-color: #131314; }
    
    /* Style KPI Cards */
    .metric-container {
        background-color: #1e1e1f;
        padding: 18px 22px;
        border-radius: 12px;
        border: 1px solid #2a2a2b;
        margin-bottom: 12px;
        min-height: 105px;
    }
    .metric-header {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #9aa0a6;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #f1f3f4;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💳 Credit Card Fraud Risk Analysis")
st.markdown("---")

# ---------------------------------------------------------
# 2. Optimized Data Ingestion & Transformation Engine
# ---------------------------------------------------------
@st.cache_data
def load_and_sanitize_data():
    try:
        df = pd.read_csv("Credit Card Fraud Risk Analysis.csv")
    except FileNotFoundError:
        st.error("Target missing: Please verify 'Credit Card Fraud Risk Analysis.csv' is in this directory.")
        st.stop()
        
    # Standardize spaces and object text entries
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        
    # Correct date types and extract Month calendar values
    if 'Transaction Date' in df.columns:
        df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors='coerce')
        df['Month'] = df['Transaction Date'].dt.strftime('%B')
    else:
        df['Month'] = 'Unknown'
        
    return df

df_raw = load_and_sanitize_data()

# ---------------------------------------------------------
# 3. Sidebar Filter Panel Configuration
# ---------------------------------------------------------
st.sidebar.header("Filter Panel")

fraud_types = ["All"] + sorted(list(df_raw['Fraud Type'].dropna().unique()))
selected_fraud = st.sidebar.selectbox("Fraud Type", fraud_types)

states = ["All"] + sorted(list(df_raw['State'].dropna().unique()))
selected_state = st.sidebar.selectbox("State", states)

merchants = ["All"] + sorted(list(df_raw['Merchant Name'].dropna().unique()))
selected_merchant = st.sidebar.selectbox("Merchant Name", merchants)

# Reactive sub-setting logic
df = df_raw.copy()
if selected_fraud != "All":
    df = df[df['Fraud Type'] == selected_fraud]
if selected_state != "All":
    df = df[df['State'] == selected_state]
if selected_merchant != "All":
    df = df[df['Merchant Name'] == selected_merchant]

# ---------------------------------------------------------
# 4. Top KPI Blocks Matrix Layer
# ---------------------------------------------------------
total_records = len(df)
fraud_cases = df[df['IsFraud'] == 1].shape[0] if 'IsFraud' in df.columns else 0

# Calculations
fraud_rate = (fraud_cases / total_records * 100) if total_records > 0 else 0.0
total_fraud_volume_m = (df[df['IsFraud'] == 1]['Transaction Amount (INR)'].sum() / 1_000_000) if 'IsFraud' in df.columns else 0.0

if 'Fraud Risk' in df.columns and total_records > 0:
    critical_cases = df[df['Fraud Risk'] == 'Critical'].shape[0]
    critical_ratio = (critical_cases / total_records * 100)
else:
    critical_ratio = 0.0

top_fraud_type = df['Fraud Type'].value_counts().index[0] if not df.empty and 'Fraud Type' in df.columns else "N/A"

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
with kpi1:
    st.markdown(f'<div class="metric-container"><div class="metric-header">Fraud Rate %</div><div class="metric-value">{fraud_rate:.2f}%</div></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown(f'<div class="metric-container"><div class="metric-header">Fraudulent Transaction</div><div class="metric-value">{fraud_cases}</div></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown(f'<div class="metric-container"><div class="metric-header">Critical Risk Transaction</div><div class="metric-value">{critical_ratio:.2f}%</div></div>', unsafe_allow_html=True)
with kpi4:
    st.markdown(f'<div class="metric-container"><div class="metric-header">Fraudulent Trans. Vol</div><div class="metric-value">₹{total_fraud_volume_m:.2f}M</div></div>', unsafe_allow_html=True)
with kpi5:
    st.markdown(f'<div class="metric-container"><div class="metric-header">Top Fraud Type</div><div class="metric-value" style="font-size:15px; margin-top:5px;">{top_fraud_type}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. Requirement 1 & 2: Stacked Bars & Donut Charts
# ---------------------------------------------------------
mid_col1, mid_col2 = st.columns([3, 2])

with mid_col1:
    st.subheader("Total Transaction Amount by Fraud Type and Transaction Category")
    # Groups correctly via 'Transaction Amount (INR)' column
    bar_agg = df.groupby(['Fraud Type', 'Transaction Category'])['Transaction Amount (INR)'].sum().reset_index()
    bar_agg['Amount (Millions)'] = bar_agg['Transaction Amount (INR)'] / 1_000_000
    
    fig_bar = px.bar(
        bar_agg,
        y='Fraud Type',
        x='Amount (Millions)',
        color='Transaction Category',
        orientation='h',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_bar.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Total Transaction Amount (In Millions)",
        yaxis_title=None
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with mid_col2:
    st.subheader("Total Transaction Amount by Fraud Risk")
    donut_agg = df.groupby('Fraud Risk')['Transaction Amount (INR)'].sum().reset_index()
    
    fig_donut = px.pie(
        donut_agg,
        values='Transaction Amount (INR)',
        names='Fraud Risk',
        hole=0.6,
        color='Fraud Risk',
        color_discrete_map={'Low': '#a020f0', 'Medium': '#e6c319', 'High': '#d9383a', 'Critical': '#1ca3ec'}
    )
    fig_donut.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# ---------------------------------------------------------
# 6. Requirement 3: Bottom Row State Bars & Trend Lines
# ---------------------------------------------------------
bot_col1, bot_col2 = st.columns(2)

with bot_col1:
    st.subheader("Fraudulent Transaction by State")
    state_agg = df[df['IsFraud'] == 1]['State'].value_counts().reset_index()
    state_agg.columns = ['State', 'Count']
    
    fig_state = px.bar(
        state_agg,
        x='State',
        y='Count',
        color_discrete_sequence=['#bf55ec']
    )
    fig_state.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title=None,
        yaxis_title="Count of Fraud Cases"
    )
    st.plotly_chart(fig_state, use_container_width=True)

with bot_col2:
    st.subheader("Fraudulent Transaction by Month")
    # Sorting explicitly by proper calendar chronology
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_agg = df[df['IsFraud'] == 1]['Month'].value_counts().reindex(month_order, fill_value=0).reset_index()
    month_agg.columns = ['Month', 'Count']
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=month_agg['Month'],
        y=month_agg['Count'],
        mode='lines+markers',
        line=dict(color='#e6c319', width=3),
        marker=dict(size=8, color='#ffffff', line=dict(color='#e6c319', width=2)),
        fill='tozeroy',
        fillcolor='rgba(230, 195, 25, 0.08)'
    ))
    fig_line.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title=None,
        yaxis_title="Count of Fraud Cases"
    )
    st.plotly_chart(fig_line, use_container_width=True)
