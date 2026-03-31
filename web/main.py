import streamlit as st
import base64

# පේජ් එකේ සැකසුම්
st.set_page_config(page_title="Phylax Gateway | AI Data Monetization", layout="centered", page_icon="🛡️")

# --- CUSTOM CSS FOR PROFESSIONAL LOOK ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #0062ff;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #004ecc; border: none; color: white; }
    .login-container {
        padding: 30px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    h1 { color: #1e293b; text-align: center; font-family: 'Inter', sans-serif; }
    .subtitle { text-align: center; color: #64748b; margin-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN / SESSION LOGIC ---
if "auth_status" not in st.session_state:
    st.session_state.auth_status = False
    st.session_state.user_role = None

def login(role):
    # Investorsලට පෙන්වන්න සරල ලොජික් එකක් (පස්සේ Supabase Auth දාමු)
    st.session_state.auth_status = True
    st.session_state.user_role = role
    st.rerun()

# --- UI RENDERING ---
if not st.session_state.auth_status:
    st.markdown("<h1>🛡️ Phylax Gateway</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>The Secure Protocol for AI-to-Web Transactions</p>", unsafe_allow_html=True)

    with st.container():
        # Login Form එක මැදට ගැනීම සඳහා columns පාවිච්චි කරමු
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["Sign In", "Create Account"])
            
            with tab1:
                email = st.text_input("Work Email", placeholder="name@company.com")
                password = st.text_input("Password", type="password")
                role = st.selectbox("I am a...", ["AI Developer", "Website Owner", "Phylax Admin"])
                
                if st.button("Access Dashboard"):
                    if email and password:
                        login(role)
                    else:
                        st.error("Please enter credentials")
            
            with tab2:
                st.info("Join the ecosystem to monetize or access data.")
                new_email = st.text_input("Full Name")
                st.selectbox("Select Role", ["AI Agency", "Data Publisher", "Researcher"])
                if st.button("Start 14-Day Free Trial"):
                    st.success("Welcome aboard! Please Sign In.")
            
            st.markdown('</div>', unsafe_allow_html=True)
else:
    # Login වුණාට පස්සේ පේන Sidebar එක
    st.sidebar.title("🛡️ Phylax Portal")
    st.sidebar.success(f"Connected: {st.session_state.user_role}")
    
    if st.sidebar.button("Log Out"):
        st.session_state.auth_status = False
        st.rerun()

    # --- ROLE ROUTING ---
    if st.session_state.user_role == "AI Developer":
        st.title("🤖 Developer Terminal")
        st.info("Manage your AI Bot instances and API usage.")
        # මෙතනට අපි කලින් හදපු ai_portal එකේ logic ටික ලස්සන කරලා දාමු
        
    elif st.session_state.user_role == "Website Owner":
        st.title("🌐 Publisher Dashboard")
        st.info("Monetize your web traffic from AI crawlers.")
        
    elif st.session_state.user_role == "Phylax Admin":
        st.title("👑 System Governance")
        st.warning("Global Oversight: Monitoring all network transactions.")