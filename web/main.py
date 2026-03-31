import streamlit as st
from core.database import supabase

# --- UI SETTINGS ---
st.set_page_config(page_title="Phylax | Onboarding", layout="centered")

if "step" not in st.session_state:
    st.session_state.step = "auth" # auth -> role_selection -> form -> dashboard

# --- 1. AUTH STEP (Login/Signup) ---
if st.session_state.step == "auth":
    st.title("🛡️ Welcome to Phylax")
    tab1, tab2 = st.tabs(["Login", "Create Account"])
    
    with tab2:
        email = st.text_input("Email Address")
        password = st.text_input("Choose Password", type="password")
        if st.button("Sign Up"):
            # මෙතනදී අපි සරලව Step එක මාරු කරමු (Demo එකක් නිසා)
            st.session_state.temp_email = email
            st.session_state.step = "role_selection"
            st.rerun()

# --- 2. ROLE SELECTION ---
elif st.session_state.step == "role_selection":
    st.title("Identify Your Role")
    st.write(f"Setting up account for: **{st.session_state.temp_email}**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🤖 I am an AI Developer"):
            st.session_state.user_role = "AI Developer"
            st.session_state.step = "form"
            st.rerun()
    with col2:
        if st.button("🌐 I am a Website Owner"):
            st.session_state.user_role = "Website Owner"
            st.session_state.step = "form"
            st.rerun()

# --- 3. ROLE-SPECIFIC FORM ---
elif st.session_state.step == "form":
    st.title(f"Complete {st.session_state.user_role} Profile")
    
    if st.session_state.user_role == "AI Developer":
        bot_name = st.text_input("Bot Name (e.g. GPT-Crawler)")
        bot_url = st.text_input("Bot / API URL (Optional)")
        bot_ip = st.text_input("Primary Server IP (for Security)")
        use_case = st.selectbox("Intended Use", ["LLM Training", "Price Monitoring", "Academic Research"])
        
        if st.button("Complete Setup & Get $10 Credits"):
            # Database එකට Save කිරීම (ai_partners)
            new_key = f"sk_phylax_{bot_name[:3]}_demo"
            supabase.table("ai_partners").insert({
                "company_name": bot_name, "api_key": new_key, "balance": 10.00,
                "bot_url": bot_url, "bot_ip": bot_ip, "use_case": use_case
            }).execute()
            st.session_state.step = "dashboard"
            st.rerun()

    else: # Website Owner
        site_name = st.text_input("Website Name")
        site_url = st.text_input("Website URL (https://...)")
        category = st.selectbox("Content Niche", ["News", "E-commerce", "Blog", "Scientific Data"])
        price = st.number_input("Target Price per Request ($)", value=0.005, format="%.4f")
        
        if st.button("Verify Website & Start Earning"):
            # Database එකට Save කිරීම (registered_sites)
            supabase.table("registered_sites").insert({
                "url": site_url, "site_name": site_name, 
                "category": category, "price_per_request": price
            }).execute()
            st.session_state.step = "dashboard"
            st.rerun()

# --- 4. THE DASHBOARD (Final View) ---
elif st.session_state.step == "dashboard":
    st.sidebar.title("🛡️ Phylax Gateway")
    st.sidebar.write(f"Logged as: {st.session_state.user_role}")
    
    if st.session_state.user_role == "AI Developer":
        st.header("🤖 Developer Control Panel")
        st.success("Your bot is active. Use your API key to access data.")
        # මෙතනට පස්සේ Spending charts දාමු
    else:
        st.header("🌐 Publisher Revenue Dashboard")
        st.success("Monetization active. Monitoring incoming bot traffic.")
        # මෙතනට පස්සේ Earnings charts දාමු

    if st.sidebar.button("Log Out"):
        st.session_state.step = "auth"
        st.rerun()