import streamlit as st
import os
from supabase import create_client, Client
import pandas as pd
import time
from dotenv import load_dotenv

load_dotenv()

# Supabase Setup
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Phylax Gateway Control Center", layout="wide")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🛡️ Phylax Control Center")
user_role = st.sidebar.radio("Select View:", ["Admin Control", "AI Developer Portal", "Website Creator Portal"])

# දත්ත ලබා ගැනීම (Database Fetch functions)
def get_ledger_logs():
    res = supabase.table("phylax_ledger").select("*, registered_sites(url), ai_partners(company_name)").order("timestamp", desc=True).limit(15).execute()
    return res.data

def get_blocked_logs():
    res = supabase.table("blocked_attempts").select("*").order("attempted_at", desc=True).limit(10).execute()
    return res.data

def get_registered_bots():
    res = supabase.table("registered_bots").select("*").execute()
    return res.data

# --- 1. ADMIN CONTROL VIEW ---
if user_role == "Admin Control":
    st.title("🛡️ Phylax Global Administration")
    st.markdown("Centralized security and bot management.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 Registered AI Bots")
        bots = get_registered_bots()
        if bots:
            df_bots = pd.DataFrame(bots)
            st.dataframe(df_bots[['bot_name', 'api_key', 'created_at']], use_container_width=True)
        else:
            st.write("No bots registered yet.")

    with col2:
        st.subheader("🚨 Blocked Fraudulent Attempts")
        blocks = get_blocked_logs()
        if blocks:
            st.error("Unauthorized bot access detected and blocked:")
            df_blocks = pd.DataFrame(blocks)
            st.table(df_blocks[['attempted_at', 'invalid_key', 'target_site_url']])
        else:
            st.success("No unauthorized attempts detected. System secure.")

# --- 2. AI DEVELOPER PORTAL ---
elif user_role == "AI Developer Portal":
    st.title("🤖 AI Developer Dashboard")
    st.info("Monitoring AI data spending and API usage.")
    
    col1, col2, col3 = st.columns(3)
    
    # OpenAI ලෙස උපකල්පනය කර දත්ත පෙන්වීම
    res_wallet = supabase.table("ai_partners").select("balance").eq("company_name", "OpenAI").execute()
    wallet_balance = res_wallet.data[0]['balance'] if res_wallet.data else 0
    
    with col1:
        st.metric("My Wallet Balance", f"${wallet_balance:.4f}", delta="-0.005 / req")
    
    with col2:
        logs = get_ledger_logs()
        total_spent = sum(float(item['amount']) for item in logs if item.get('ai_partners') and item['ai_partners']['company_name'] == 'OpenAI')
        st.metric("Total Spent Today", f"${total_spent:.4f}")
        
    with col3:
        st.metric("API Status", "Active", delta_color="normal")

    st.subheader("My Data Acquisition Logs")
    if logs:
        df = pd.DataFrame(logs)
        # OpenAI ට අදාළ දත්ත විතරක් Filter කිරීම
        df = df[df['ai_partners'].apply(lambda x: x['company_name'] == 'OpenAI' if x else False)]
        if not df.empty:
            df['Target Site'] = df['registered_sites'].apply(lambda x: x['url'] if x else "Unknown")
            st.table(df[['timestamp', 'Target Site', 'amount']])
        else:
            st.write("No recent transactions found.")


# --- 3. WEBSITE CREATOR PORTAL ---
else:
    st.title("🌐 Website Creator Dashboard")
    st.success("Monitoring revenue earned from AI bots.")
    
    # මෙතනදී logs සහ total_earned අලුතින් ගන්න ඕනේ Error එක නැති වෙන්න
    logs = get_ledger_logs()
    
    # පද්ධතියේ මුළු ආදායම ගණනය කිරීම
    if logs:
        total_earned = sum(float(item['amount']) for item in logs)
    else:
        total_earned = 0.0

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Revenue Earned", f"${total_earned:.4f}", delta="Income")
    
    with col2:
        # ලියාපදිංචි වෙබ් අඩවි ගණන
        res_sites = supabase.table("registered_sites").select("id", count="exact").execute()
        st.metric("Monetized Sites", res_sites.count if res_sites.count else 0)
        
    with col3:
        st.metric("Security Level", "High (Bot Shield Active)")

    st.subheader("Incoming Revenue Stream")
    if logs:
        df = pd.DataFrame(logs)
        # දත්ත ප්‍රසන්නව පෙන්වීමට column names සකසමු
        df['Payer (Bot)'] = df['ai_partners'].apply(lambda x: x['company_name'] if x else "Unknown")
        df['My Site'] = df['registered_sites'].apply(lambda x: x['url'] if x else "Unknown")
        st.table(df[['timestamp', 'Payer (Bot)', 'My Site', 'amount']])
    else:
        st.write("No earnings yet. Waiting for AI traffic...")