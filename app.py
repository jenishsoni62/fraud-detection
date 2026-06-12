import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
import os
from dotenv import load_dotenv
import json

load_dotenv()

st.set_page_config(page_title="AI Fraud Detection", page_icon="🔍", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }

p, h1, h2, h3, h4, h5, label, .stMarkdown { color: #ffffff !important; }
[data-testid="stMetricLabel"] { color: #f87171 !important; font-size: 0.9rem !important; }
[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 2.2rem !important; font-weight: 800 !important; }

.stApp {
    background: radial-gradient(ellipse at top, #1a0505 0%, #0a0a0f 50%, #050510 100%);
}

div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(248,113,113,0.1), rgba(220,38,38,0.05));
    border: 1px solid rgba(248,113,113,0.2);
    border-radius: 16px;
    padding: 20px;
}

.stButton>button {
    background: linear-gradient(90deg, #dc2626 0%, #f87171 50%, #dc2626 100%);
    background-size: 200% auto;
    color: white;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    padding: 14px 30px;
    width: 100%;
    font-size: 1.1rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.stTextArea textarea {
    background: rgba(248,113,113,0.05) !important;
    border: 1px solid rgba(248,113,113,0.2) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
}

.stFileUploader {
    background: rgba(248,113,113,0.05);
    border: 2px dashed rgba(248,113,113,0.3);
    border-radius: 12px;
    padding: 20px;
}

.hero-section {
    text-align: center;
    padding: 2rem 0;
    margin-bottom: 1rem;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(90deg, #ff4444, #ff8888, #ffaa00, #ff8888, #ff4444);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    letter-spacing: -1px;
}

.hero-subtitle {
    color: rgba(255,255,255,0.5) !important;
    font-size: 1.1rem;
    font-weight: 300;
}

.hero-badge {
    display: inline-block;
    background: rgba(248,113,113,0.15);
    border: 1px solid rgba(248,113,113,0.3);
    color: #f87171 !important;
    padding: 4px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 1rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.section-header {
    font-size: 1.3rem;
    font-weight: 700;
    color: #f87171 !important;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(248,113,113,0.2);
    display: flex;
    align-items: center;
    gap: 8px;
}

.transaction-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px;
    margin: 12px 0;
    word-wrap: break-word;
    overflow-wrap: break-word;
    transition: all 0.3s ease;
}

.high-risk {
    border-left: 5px solid #f87171;
    background: linear-gradient(135deg, rgba(248,113,113,0.08), rgba(220,38,38,0.03));
}

.medium-risk {
    border-left: 5px solid #fbbf24;
    background: linear-gradient(135deg, rgba(251,191,36,0.08), rgba(217,119,6,0.03));
}

.low-risk {
    border-left: 5px solid #34d399;
    background: linear-gradient(135deg, rgba(52,211,153,0.08), rgba(16,185,129,0.03));
}

.stat-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    margin: 8px 0;
}

.feature-card {
    background: linear-gradient(135deg, rgba(248,113,113,0.08), rgba(220,38,38,0.03));
    border: 1px solid rgba(248,113,113,0.15);
    border-radius: 16px;
    padding: 28px 20px;
    text-align: center;
    height: 100%;
}

.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 2rem 0;
}

.alert-banner {
    background: linear-gradient(90deg, rgba(248,113,113,0.15), rgba(220,38,38,0.1));
    border: 1px solid rgba(248,113,113,0.3);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 16px 0;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-section">
    <p class="hero-badge">🛡️ AI Powered Security</p>
    <p class="hero-title">Fraud Detection System</p>
    <p class="hero-subtitle">Real-time transaction monitoring powered by advanced AI</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

def analyze_transactions(df):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    transactions_text = df.to_string(index=False)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "You are an expert fraud detection analyst. Analyze these financial transactions and identify suspicious ones. Respond ONLY with a JSON array, no other text.\n\nTransactions:\n" + transactions_text + "\n\nFor each transaction respond with exactly this JSON format:\n[{\"id\": \"T001\", \"risk_level\": \"High\", \"risk_score\": 85, \"reason\": \"Unusually large amount at odd hours\", \"recommendation\": \"Block and investigate immediately\"}, ...]\n\nRisk levels: High (score 70-100), Medium (score 40-69), Low (score 0-39)"
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

def create_sample_data():
    data = {
        'Transaction_ID': ['T001', 'T002', 'T003', 'T004', 'T005', 'T006', 'T007', 'T008', 'T009', 'T010'],
        'Amount': [150.00, 45000.00, 23.50, 8900.00, 12.00, 150000.00, 450.00, 89.99, 25000.00, 5.50],
        'Merchant': ['Grocery Store', 'Unknown Merchant', 'Coffee Shop', 'Electronics Store', 'Fast Food', 'Offshore Account', 'Restaurant', 'Online Shopping', 'Wire Transfer', 'Convenience Store'],
        'Location': ['Mumbai', 'Unknown', 'Mumbai', 'Delhi', 'Mumbai', 'Cayman Islands', 'Mumbai', 'Online', 'Dubai', 'Mumbai'],
        'Time': ['10:30 AM', '3:15 AM', '12:45 PM', '2:30 PM', '8:00 AM', '4:45 AM', '7:30 PM', '11:00 AM', '1:15 AM', '9:00 AM'],
        'Card_Type': ['Debit', 'Credit', 'Debit', 'Credit', 'Debit', 'Credit', 'Debit', 'Credit', 'Credit', 'Debit'],
        'Status': ['Completed', 'Pending', 'Completed', 'Completed', 'Completed', 'Pending', 'Completed', 'Completed', 'Pending', 'Completed']
    }
    return pd.DataFrame(data)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<p class="section-header">📁 Transaction Data</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload CSV file with transaction data",
        type=["csv"],
        help="Upload a CSV file containing transaction data"
    )
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ {len(df)} transactions loaded successfully!")
    else:
        st.markdown("""
        <div class="alert-banner">
            <p style="margin:0; color:rgba(255,255,255,0.7);">📋 No file uploaded - Using sample transaction data</p>
        </div>
        """, unsafe_allow_html=True)
        df = create_sample_data()

with col2:
    st.markdown('<p class="section-header">👁️ Data Preview</p>', unsafe_allow_html=True)
    st.dataframe(df.head(5), use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

if st.button("🔍 SCAN FOR FRAUD"):
    with st.spinner("🤖 AI is scanning transactions for suspicious activity..."):
        try:
            result_text = analyze_transactions(df)
            result_text = result_text.strip()
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
            results = json.loads(result_text)

            high_risk = [r for r in results if r.get("risk_level") == "High"]
            medium_risk = [r for r in results if r.get("risk_level") == "Medium"]
            low_risk = [r for r in results if r.get("risk_level") == "Low"]

            if high_risk:
                st.markdown(f"""
                <div class="alert-banner">
                    <p style="margin:0; color:#f87171; font-weight:700; font-size:1.1rem;">
                        🚨 ALERT: {len(high_risk)} HIGH RISK TRANSACTION(S) DETECTED!
                    </p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<p class="section-header">📊 Risk Overview</p>', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Scanned", len(results))
            with col2:
                st.metric("🔴 High Risk", len(high_risk))
            with col3:
                st.metric("🟡 Medium Risk", len(medium_risk))
            with col4:
                st.metric("🟢 Low Risk", len(low_risk))

            st.markdown('<hr class="divider">', unsafe_allow_html=True)

            col_chart1, col_chart2 = st.columns(2)

            with col_chart1:
                st.markdown('<p class="section-header">🥧 Risk Distribution</p>', unsafe_allow_html=True)
                risk_counts = {"High Risk": len(high_risk), "Medium Risk": len(medium_risk), "Low Risk": len(low_risk)}
                fig1 = px.pie(
                    values=list(risk_counts.values()),
                    names=list(risk_counts.keys()),
                    color=list(risk_counts.keys()),
                    color_discrete_map={"High Risk": "#f87171", "Medium Risk": "#fbbf24", "Low Risk": "#34d399"},
                    template="plotly_dark",
                    hole=0.4
                )
                fig1.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    legend=dict(font=dict(color='white'))
                )
                st.plotly_chart(fig1, use_container_width=True)

            with col_chart2:
                st.markdown('<p class="section-header">📊 Risk Scores</p>', unsafe_allow_html=True)
                scores_df = pd.DataFrame([
                    {"Transaction": r.get("id", ""), "Score": r.get("risk_score", 0), "Risk": r.get("risk_level", "")}
                    for r in results
                ])
                fig2 = px.bar(
                    scores_df, x="Transaction", y="Score",
                    color="Risk",
                    color_discrete_map={"High": "#f87171", "Medium": "#fbbf24", "Low": "#34d399"},
                    template="plotly_dark"
                )
                fig2.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    legend=dict(font=dict(color='white'))
                )
                st.plotly_chart(fig2, use_container_width=True)

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown('<p class="section-header">🚨 Detailed Transaction Analysis</p>', unsafe_allow_html=True)

            for r in results:
                risk = r.get("risk_level", "Low")
                score = r.get("risk_score", 0)
                if risk == "High":
                    card_class = "transaction-card high-risk"
                    emoji = "🔴"
                    color = "#f87171"
                elif risk == "Medium":
                    card_class = "transaction-card medium-risk"
                    emoji = "🟡"
                    color = "#fbbf24"
                else:
                    card_class = "transaction-card low-risk"
                    emoji = "🟢"
                    color = "#34d399"

                row = df[df.iloc[:, 0] == r.get("id", "")]
                amount = row['Amount'].values[0] if len(row) > 0 and 'Amount' in df.columns else "N/A"
                merchant = row['Merchant'].values[0] if len(row) > 0 and 'Merchant' in df.columns else "N/A"
                location = row['Location'].values[0] if len(row) > 0 and 'Location' in df.columns else "N/A"
                time = row['Time'].values[0] if len(row) > 0 and 'Time' in df.columns else "N/A"

                st.markdown(f"""
                <div class="{card_class}">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                        <div>
                            <span style="font-size:1.3rem; font-weight:800;">{emoji} {r.get("id", "")}</span>
                            <span style="background:rgba(255,255,255,0.08); padding:2px 12px; border-radius:20px; font-size:0.85rem; margin-left:10px; color:rgba(255,255,255,0.6);">{risk} Risk</span>
                        </div>
                        <span style="background:rgba(255,255,255,0.08); padding:8px 20px; border-radius:20px; font-weight:800; color:{color}; font-size:1.2rem;">
                            {score}/100
                        </span>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:12px; margin-bottom:16px;">
                        <div style="background:rgba(255,255,255,0.04); border-radius:8px; padding:10px;">
                            <p style="color:rgba(255,255,255,0.4); font-size:0.8rem; margin-bottom:4px;">AMOUNT</p>
                            <p style="font-weight:700; margin:0;">₹{amount}</p>
                        </div>
                        <div style="background:rgba(255,255,255,0.04); border-radius:8px; padding:10px;">
                            <p style="color:rgba(255,255,255,0.4); font-size:0.8rem; margin-bottom:4px;">MERCHANT</p>
                            <p style="font-weight:600; margin:0; font-size:0.9rem;">{merchant}</p>
                        </div>
                        <div style="background:rgba(255,255,255,0.04); border-radius:8px; padding:10px;">
                            <p style="color:rgba(255,255,255,0.4); font-size:0.8rem; margin-bottom:4px;">LOCATION</p>
                            <p style="font-weight:600; margin:0;">{location}</p>
                        </div>
                        <div style="background:rgba(255,255,255,0.04); border-radius:8px; padding:10px;">
                            <p style="color:rgba(255,255,255,0.4); font-size:0.8rem; margin-bottom:4px;">TIME</p>
                            <p style="font-weight:600; margin:0;">{time}</p>
                        </div>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                        <div style="background:rgba(248,113,113,0.08); border-radius:8px; padding:12px; border:1px solid rgba(248,113,113,0.15);">
                            <p style="color:{color}; font-weight:600; margin-bottom:6px; font-size:0.9rem;">⚠️ FRAUD REASON</p>
                            <p style="margin:0; font-size:0.95rem;">{r.get("reason", "N/A")}</p>
                        </div>
                        <div style="background:rgba(96,165,250,0.08); border-radius:8px; padding:12px; border:1px solid rgba(96,165,250,0.15);">
                            <p style="color:#60a5fa; font-weight:600; margin-bottom:6px; font-size:0.9rem;">💡 RECOMMENDATION</p>
                            <p style="margin:0; font-size:0.95rem;">{r.get("recommendation", "N/A")}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {str(e)}")

else:
    st.markdown('<p class="section-header">🛡️ System Capabilities</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <p style="font-size:3rem; margin-bottom:1rem;">🔍</p>
            <p style="font-weight:800; font-size:1.2rem; margin-bottom:0.5rem;">AI Detection</p>
            <p style="color:rgba(255,255,255,0.5); font-size:0.95rem;">Advanced AI analyzes each transaction for suspicious patterns and anomalies</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <p style="font-size:3rem; margin-bottom:1rem;">⚡</p>
            <p style="font-weight:800; font-size:1.2rem; margin-bottom:0.5rem;">Real-time Scoring</p>
            <p style="color:rgba(255,255,255,0.5); font-size:0.95rem;">Instant risk scores from 0-100 with High, Medium, and Low risk classification</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <p style="font-size:3rem; margin-bottom:1rem;">🚨</p>
            <p style="font-weight:800; font-size:1.2rem; margin-bottom:0.5rem;">Instant Alerts</p>
            <p style="color:rgba(255,255,255,0.5); font-size:0.95rem;">Immediate alerts for high-risk transactions with detailed recommendations</p>
        </div>
        """, unsafe_allow_html=True)