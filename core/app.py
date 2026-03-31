import os
from flask import Flask, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

# Supabase සම්බන්ධ කිරීම
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route('/')
def health_check():
    return jsonify({"status": "Phylax Gateway Active"}), 200

# --- UNIT 1: BOT REGISTRATION API ---
@app.route('/api/register-bot', methods=['POST'])
def register_bot():
    data = request.json
    bot_name = data.get('bot_name')
    email = data.get('email')
    
    # නව API Key එකක් සෑදීම (Random hex string)
    new_key = f"sk-{os.urandom(8).hex()}"
    
    try:
        supabase.table("registered_bots").insert({
            "bot_name": bot_name,
            "owner_email": email,
            "api_key": new_key
        }).execute()
        return jsonify({"status": "Registered", "your_api_key": new_key}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- UNIT 2: SMART SECURE GATEWAY ---
@app.route('/api/pay', methods=['POST'], strict_slashes=False)
def process_payment():
    data = request.json
    api_key = data.get('api_key')
    site_url = data.get('site_url')

    if not api_key or not site_url:
        return jsonify({"error": "Missing parameters"}), 400

    # 1. පද්ධතියේ ලියාපදිංචි බොට් කෙනෙක්දැයි පරීක්ෂා කිරීම (Authentication)
    bot_check = supabase.table("registered_bots").select("*").eq("api_key", api_key).execute()
    
    if not bot_check.data:
        # හොර බොට් කෙනෙක් නම්, ඒ සිදුවීම සටහන් කරන්න (Security Logging)
        supabase.table("blocked_attempts").insert({
            "invalid_key": api_key,
            "target_site_url": site_url
        }).execute()
        
        print(f"⚠️ SECURITY ALERT: Blocked unauthorized access for key: {api_key}")
        return jsonify({"status": "blocked", "reason": "Invalid API Key - Unauthorized Bot"}), 403

    # 2. Key එක හරි නම්, සල්ලි කැපීමේ ගනුදෙනුව සිදු කිරීම (Transaction)
    try:
        # Supabase RPC (Process Payment Function) එක ඇමතීම
        response = supabase.rpc("process_phylax_payment", {
            "p_api_key": api_key,
            "p_site_url": site_url
        }).execute()

        if response.data == "SUCCESS":
            print(f"✅ SUCCESS: Payment processed for {site_url}")
            return jsonify({"status": "paid"}), 200
        else:
            print(f"❌ DENIED: {response.data} for {site_url}")
            return jsonify({"status": "denied", "reason": response.data}), 402

    except Exception as e:
        print(f"🔥 ERROR: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)