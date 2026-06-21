import time
import requests
import json
import re
import os
import sys
from datetime import datetime, date, timedelta
from urllib.parse import quote_plus
from pathlib import Path
import sqlite3
import telebot
from telebot import types
import threading
import random
import itertools
import firebase_admin
from firebase_admin import credentials, firestore, auth
import hashlib
import secrets

# ======================
# 🚫 إخفاء جميع مخرجات الطرفية
# ======================
class NullWriter:
    def write(self, *args, **kwargs):
        pass
    def flush(self, *args, **kwargs):
        pass

original_stdout = sys.stdout
original_stderr = sys.stderr
sys.stdout = NullWriter()
sys.stderr = NullWriter()

# ======================
# 🔥 تهيئة Firebase
# ======================
try:
    # قراءة ملف credentials من JSON
    firebase_cred = {
        "type": "service_account",
        "project_id": "us-bot-b073b",
        "private_key_id": "d2c9f772c21b60b37a8f79f1e61d01c99a8ac7be",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDhFEc6RoxW6N9k\n18lSNLXoxL+RTDDUjWsplUQaGU5Tsj75utC7Z2XRxRTPaF7SY53j2r//s9NaTBrD\nlb2RneCR321CJYtnQmJhNziX8LVn7d3wQ7UwS6VzlZ4Or5XkLKyrb9Sq0fK+JiDa\nu7zOezU3sZk54mBZCMaXM5JPHc0nMg/cogsEJB5Ba70EiVuHHqaiAL/xlUyo1TSl\nhBXEAZVNnyxzLI6nUxgD927TTYYIfaBk4tzubpSI0xbMwTIjq0hpVb7j6Zdipm8l\nADOOxsZvjkYDWLeRf25LVeknGjCZWK0zcmVxFxPTYlcm3f1p72Trsr4HLJf4dR/Y\nwXRpb5n/AgMBAAECggEABks53qnmwyHJ6Jj8ITDy8UPz+c0mngFb8/kfj8p4KgqV\nWW7Ds90LuAm8/KIpHKFg4rE7czWesF5QCHrhQF3CaaUH+hrwqTEhbSFNLNQagbVH\nr0mrzfwfiUbixfuOkA3YjW0YH+eB1GPE9J9Eg7jNEsMD/nfGqyN94iNOcQ+FRnyo\nPZYnXO3PqK/+xM7DgNshY9l84jc5Kwv/JT6KuOuAvOhMxi4mWkiO+XPa3Mqib88R\njSLhvnfR8h15bfIUnbTHTPfrrGE5bH3FF2vyEZ0YtjOzEDLuRx/hho+CDpX/TSfp\nxGqV/UdYr5eKWuofatq9mLjndnZaedJLGFEKyzXtwQKBgQD92RrScF+L+R9lcHAk\n1dkeHRxjn+gyNy92cNk9gcV2PBC/dlJaAfYpuhPqmxxqNlNVrgTAUY8mJuW2Pzn1\nhZgI3jRdUx1EspvzAixseapmkkqtye0HYr+4oKLwytkxNNxg42zDomyjpVsMzoVP\nEmONFl5VfI5W25O0yHEjR0vW4QKBgQDi/L1tu4ci7xVLpf0Qaf70TvW/Zvpwbb2v\n847+qlugur8OIB8OK4ktX0Hur7oWQVFMq1o0ARfPHU7AGXwJ8GHzKsuwJHeVzr8G\ni1b97mvCDeAYwV62y9o+gOYC4UoJmLp4zOnVHwaVisfLMIXzaLTSWT2yTbzwfGgJ\njqHalUjs3wKBgQCW9M2ziSn4tkxKaaP288j1Ir2X7iYbCLof1Fg91Qy7KNVCIsO\nhY4a4FJJuLYcH3RNRnAC4j2LhaQjTdQswqZX17QyL2P/X2vIBmnelDeWSbbpRGSV\neM7kf3qGUUr5rSLE51nduTB73LCZnBLApAHZfAzbL3gCBRAAeRZ20UYzYQKBgQC0\nVX2dx4XmcDHoBvjV6JBAwtak+Qhw+A7i0krB8tCXEqalb0mc9WOno217VystcTlJ\nAz3H4TJsPumI3vZX4x2+ljp7N422fCnx5hP37Eq6QlHO+Rnpem1qiPe0RA6RL0C+\npnYD9wFBH5/5wxQ4vPAjyfilRvOb0ArLxQC76yyj2wKBgQCMwB0JDuTDMn7F5I2y\np1iNL0iBWh+ADRjICS3SvgVoJJCmk2idSCGTpOGZp4dKMrgZDVaEqmSAZmx+ahS+\nrKaFb9ryXiLK/4ZWsBqfypqAn/NSy79Dozm5Tq6Z564np9yjsTHquQoHqHnYVfqp\nyuPR95M6zLUsZuvonmK46MsVZg==\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-fbsvc@us-bot-b073b.iam.gserviceaccount.com",
        "client_id": "100089972966089282489",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40us-bot-b073b.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }
    
    cred = credentials.Certificate(firebase_cred)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase initialized successfully")
except Exception as e:
    sys.stdout = original_stdout
    sys.stderr = original_stderr
    print(f"❌ Firebase initialization failed: {e}")
    sys.exit(1)

# ======================
# 🖥️ لوحة واحدة فقط
# ======================
DASHBOARD_CONFIGS = [
    {
        "name": "alone234100",
        "base": "http://51.210.208.26",
        "ajax_path": "/ints/agent/res/data_smscdr.php",
        "login_page": "/ints/login",
        "login_post": "/ints/signin",
        "username": "alone234100",
        "password": "alone234100",
        "session": requests.Session(),
        "is_logged_in": False
    }
]

COMMON_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8"
}

for dash in DASHBOARD_CONFIGS:
    dash["session"].headers.update(COMMON_HEADERS)
    login_page_url = dash["base"] + dash["login_page"]
    dash["login_page_url"] = login_page_url
    dash["login_post_url"] = dash["base"] + dash["login_post"]
    dash["ajax_url"] = dash["base"] + dash["ajax_path"]

USERNAME = "alone234100"
PASSWORD = "alone234100"
BOT_TOKEN = "8552862910:AAFmCRhJPTAZ0kAnSOPvPdS2NntS5fy6sfQ"
CHAT_IDS = ["-1003270581564"]
REFRESH_INTERVAL = 10
TIMEOUT = 100
MAX_RETRIES = 5
RETRY_DELAY = 5
IDX_DATE = 0
IDX_NUMBER = 2
IDX_SMS = 5
SENT_MESSAGES_FILE = "sent_messages.json"

ADMIN_IDS = [7023416185]
DB_PATH = "bot.db"

if not BOT_TOKEN:
    sys.stdout = original_stdout
    sys.stderr = original_stderr
    raise SystemExit("❌ BOT_TOKEN must be set")

# ======================
# 📋 دوال Firebase
# ======================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user_in_firebase(telegram_id, username, email, password, first_name="", last_name=""):
    """إنشاء مستخدم جديد في Firebase"""
    try:
        user_data = {
            "telegram_id": telegram_id,
            "telegram_username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password_hash": hash_password(password),
            "created_at": datetime.now().isoformat(),
            "is_banned": False,
            "is_admin": False,
            "is_logged_in": False
        }
        doc_ref = db.collection('users').document(str(telegram_id))
        doc_ref.set(user_data)
        return True, "User created successfully"
    except Exception as e:
        return False, str(e)

def get_user_from_firebase(telegram_id):
    """جلب بيانات المستخدم من Firebase"""
    try:
        doc_ref = db.collection('users').document(str(telegram_id))
        doc = doc_ref.get()
        if doc.exists:
            return True, doc.to_dict()
        return False, "User not found"
    except Exception as e:
        return False, str(e)

def authenticate_user(email, password):
    """مصادقة المستخدم"""
    try:
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', email).limit(1)
        results = query.get()
        
        for doc in results:
            user_data = doc.to_dict()
            if user_data.get('password_hash') == hash_password(password):
                return True, user_data, doc.id
        return False, "Invalid credentials", None
    except Exception as e:
        return False, str(e), None

def update_user_login_status(telegram_id, is_logged_in):
    """تحديث حالة تسجيل الدخول"""
    try:
        doc_ref = db.collection('users').document(str(telegram_id))
        doc_ref.update({'is_logged_in': is_logged_in})
        return True
    except Exception as e:
        return False

def ban_user_firebase(telegram_id):
    """حظر المستخدم في Firebase"""
    try:
        doc_ref = db.collection('users').document(str(telegram_id))
        doc_ref.update({'is_banned': True})
        return True
    except Exception as e:
        return False

def unban_user_firebase(telegram_id):
    """إلغاء حظر المستخدم في Firebase"""
    try:
        doc_ref = db.collection('users').document(str(telegram_id))
        doc_ref.update({'is_banned': False})
        return True
    except Exception as e:
        return False

def is_user_banned_firebase(telegram_id):
    """التحقق من حالة الحظر"""
    success, user_data = get_user_from_firebase(telegram_id)
    if success:
        return user_data.get('is_banned', False)
    return False

def is_admin_firebase(telegram_id):
    """التحقق من صلاحيات الأدمن"""
    # الأدمن الرئيسي
    if telegram_id in ADMIN_IDS:
        return True
    
    success, user_data = get_user_from_firebase(telegram_id)
    if success:
        return user_data.get('is_admin', False)
    return False

def set_admin_firebase(telegram_id, is_admin):
    """تعيين مستخدم كأدمن"""
    try:
        doc_ref = db.collection('users').document(str(telegram_id))
        doc_ref.update({'is_admin': is_admin})
        return True
    except Exception as e:
        return False

def get_user_email(telegram_id):
    """جلب الإيميل الخاص بالمستخدم"""
    success, user_data = get_user_from_firebase(telegram_id)
    if success:
        return user_data.get('email')
    return None

def log_user_action(telegram_id, action, details=""):
    """تسجيل أنشطة المستخدم"""
    try:
        log_data = {
            "telegram_id": telegram_id,
            "action": action,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        db.collection('logs').add(log_data)
        return True
    except Exception as e:
        return False

# ======================
# 🧰 دوال إدارة قاعدة البيانات المحلية (للتوافق)
# ======================
def get_setting(key):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT value FROM bot_settings WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def set_setting(key, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("REPLACE INTO bot_settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            country_code TEXT,
            assigned_number TEXT,
            is_banned INTEGER DEFAULT 0,
            private_combo_country TEXT DEFAULT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS combos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_code TEXT UNIQUE,
            numbers TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS otp_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT,
            otp TEXT,
            full_message TEXT,
            timestamp TEXT,
            assigned_to INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS dashboards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            base_url TEXT,
            ajax_path TEXT,
            login_page TEXT,
            login_post TEXT,
            username TEXT,
            password TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS bot_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS private_combos (
            user_id INTEGER,
            country_code TEXT,
            numbers TEXT,
            PRIMARY KEY (user_id, country_code)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS force_sub_channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_url TEXT UNIQUE NOT NULL,
            description TEXT DEFAULT '',
            enabled INTEGER DEFAULT 1
        )
    ''')
    c.execute("INSERT OR IGNORE INTO bot_settings (key, value) VALUES ('force_sub_channel', '')")
    c.execute("INSERT OR IGNORE INTO bot_settings (key, value) VALUES ('force_sub_enabled', '0')")
    
    c.execute("SELECT value FROM bot_settings WHERE key = 'force_sub_channel'")
    old_channel = c.fetchone()
    if old_channel and old_channel[0].strip():
        channel = old_channel[0].strip()
        c.execute("SELECT 1 FROM force_sub_channels WHERE channel_url = ?", (channel,))
        if not c.fetchone():
            enabled = 1 if get_setting("force_sub_enabled") == "1" else 0
            c.execute("INSERT INTO force_sub_channels (channel_url, description, enabled) VALUES (?, ?, ?)",
                      (channel, "القناة الأساسية", enabled))
    
    conn.commit()
    conn.close()

init_db()

# ======================
# 🧰 دوال إدارة المستخدمين المحلية (للتخزين المؤقت)
# ======================
def get_user_local(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row

def save_user_local(user_id, username="", first_name="", last_name="", country_code=None, assigned_number=None, private_combo_country=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    existing_data = get_user_local(user_id)
    if existing_data:
        if country_code is None:
            country_code = existing_data[4]
        if assigned_number is None:
            assigned_number = existing_data[5]
        if private_combo_country is None:
            private_combo_country = existing_data[7]
    
    c.execute("""
        REPLACE INTO users (user_id, username, first_name, last_name, country_code, assigned_number, is_banned, private_combo_country)
        VALUES (?, ?, ?, ?, ?, ?, COALESCE((SELECT is_banned FROM users WHERE user_id=?), 0), ?)
    """, (
        user_id,
        username,
        first_name,
        last_name,
        country_code,
        assigned_number,
        user_id,
        private_combo_country
    ))
    conn.commit()
    conn.close()

def get_all_users_local():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE is_banned=0")
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users

def get_combo(country_code, user_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if user_id:
        c.execute("SELECT numbers FROM private_combos WHERE user_id=? AND country_code=?", (user_id, country_code))
        row = c.fetchone()
        if row:
            conn.close()
            return json.loads(row[0])
    c.execute("SELECT numbers FROM combos WHERE country_code=?", (country_code,))
    row = c.fetchone()
    conn.close()
    return json.loads(row[0]) if row else []

def save_combo(country_code, numbers, user_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if user_id:
        c.execute("REPLACE INTO private_combos (user_id, country_code, numbers) VALUES (?, ?, ?)",
                  (user_id, country_code, json.dumps(numbers)))
    else:
        c.execute("REPLACE INTO combos (country_code, numbers) VALUES (?, ?)",
                  (country_code, json.dumps(numbers)))
    conn.commit()
    conn.close()

def delete_combo(country_code, user_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if user_id:
        c.execute("DELETE FROM private_combos WHERE user_id=? AND country_code=?", (user_id, country_code))
    else:
        c.execute("DELETE FROM combos WHERE country_code=?", (country_code,))
    conn.commit()
    conn.close()

def get_all_combos():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT country_code FROM combos")
    combos = [row[0] for row in c.fetchall()]
    conn.close()
    return combos

def assign_number_to_user(user_id, number):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET assigned_number=? WHERE user_id=?", (number, user_id))
    conn.commit()
    conn.close()

def get_user_by_number(number):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE assigned_number=?", (number,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def log_otp(number, otp, full_message, assigned_to=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO otp_logs (number, otp, full_message, timestamp, assigned_to) VALUES (?, ?, ?, ?, ?)",
              (number, otp, full_message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), assigned_to))
    conn.commit()
    conn.close()

def release_number(old_number):
    if not old_number:
        return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET assigned_number=NULL WHERE assigned_number=?", (old_number,))
    conn.commit()
    conn.close()

def get_otp_logs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM otp_logs")
    logs = c.fetchall()
    conn.close()
    return logs

def get_user_info_local(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row

def get_all_force_sub_channels(enabled_only=True):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if enabled_only:
        c.execute("SELECT id, channel_url, description FROM force_sub_channels WHERE enabled = 1 ORDER BY id")
    else:
        c.execute("SELECT id, channel_url, description FROM force_sub_channels ORDER BY id")
    rows = c.fetchall()
    conn.close()
    return rows

def add_force_sub_channel(channel_url, description=""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO force_sub_channels (channel_url, description, enabled) VALUES (?, ?, 1)",
                  (channel_url.strip(), description.strip()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def delete_force_sub_channel(channel_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM force_sub_channels WHERE id = ?", (channel_id,))
    changed = c.rowcount > 0
    conn.commit()
    conn.close()
    return changed

def toggle_force_sub_channel(channel_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE force_sub_channels SET enabled = 1 - enabled WHERE id = ?", (channel_id,))
    conn.commit()
    conn.close()

# ======================
# 🤖 إنشاء بوت Telegram
# ======================
bot = telebot.TeleBot(BOT_TOKEN)

# ======================
# 🔐 دوال الاشتراك الإجباري
# ======================
def force_sub_check(user_id):
    channels = get_all_force_sub_channels(enabled_only=True)
    if not channels:
        return True
    
    for _, url, _ in channels:
        try:
            if url.startswith("https://t.me/"):
                ch = "@" + url.split("/")[-1]
            elif url.startswith("@"):
                ch = url
            else:
                continue
            member = bot.get_chat_member(ch, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception:
            return False
    return True

def force_sub_markup():
    channels = get_all_force_sub_channels(enabled_only=True)
    if not channels:
        return None
    
    markup = types.InlineKeyboardMarkup()
    for _, url, desc in channels:
        text = f"📢 {desc}" if desc else "📢 اشترك في القناة"
        markup.add(types.InlineKeyboardButton(text, url=url))
    markup.add(types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_sub"))
    return markup

# ======================
# 🎮 دوال المصادقة
# ======================
def is_user_logged_in(telegram_id):
    """التحقق من حالة تسجيل الدخول"""
    success, user_data = get_user_from_firebase(telegram_id)
    if success:
        return user_data.get('is_logged_in', False)
    return False

def get_auth_markup():
    """أزرار المصادقة"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔐 تسجيل الدخول", callback_data="auth_login"),
        types.InlineKeyboardButton("📝 إنشاء حساب", callback_data="auth_register")
    )
    return markup

def get_logged_in_markup():
    """أزرار المستخدم المسجل دخوله"""
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🚪 تسجيل خروج", callback_data="auth_logout"))
    return markup

# ======================
# 🎮 دوال البوت الرئيسية
# ======================
user_states = {}

def is_admin(user_id):
    return is_admin_firebase(user_id)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    telegram_id = message.from_user.id
    
    # التحقق من الاشتراك الإجباري
    if not force_sub_check(telegram_id):
        markup = force_sub_markup()
        if markup:
            bot.send_message(message.chat.id, "🔒 يجب الاشتراك في القناة لاستخدام البوت.", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "🔒 الاشتراك الإجباري مفعل لكن لم يتم تحديد قناة!")
        return
    
    # التحقق من الحظر
    if is_user_banned_firebase(telegram_id):
        bot.reply_to(message, "🚫 You are banned.")
        return
    
    # التحقق من وجود المستخدم في Firebase
    success, user_data = get_user_from_firebase(telegram_id)
    
    if not success:
        # مستخدم جديد
        bot.send_message(
            message.chat.id, 
            "👋 Welcome! Please login or create an account:\n\n"
            "🔐 Login if you already have an account\n"
            "📝 Register to create a new account",
            reply_markup=get_auth_markup()
        )
        return
    
    # مستخدم موجود - التحقق من حالة تسجيل الدخول
    if not user_data.get('is_logged_in', False):
        bot.send_message(
            message.chat.id,
            "🔒 Please login to continue:",
            reply_markup=get_auth_markup()
        )
        return
    
    # ✅ مستخدم مسجل دخوله
    # حفظ بيانات المستخدم محلياً (للتوافق مع الكود القديم)
    save_user_local(
        telegram_id,
        username=message.from_user.username or "",
        first_name=message.from_user.first_name or "",
        last_name=message.from_user.last_name or ""
    )
    
    # إرسال إشعار للأدمن عند أول استخدام (مرة واحدة)
    if not get_user_local(telegram_id):
        email = user_data.get('email', 'N/A')
        for admin in ADMIN_IDS:
            try:
                caption = f"🆕 مستخدم جديد دخل البوت:\n"
                caption += f"🆔: `{telegram_id}`\n"
                caption += f"👤: @{message.from_user.username or 'None'}\n"
                caption += f"📧: `{email}`\n"
                caption += f"الاسم: {message.from_user.first_name or ''} {message.from_user.last_name or ''}\n"
                caption += f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                bot.send_message(admin, caption, parse_mode="Markdown")
            except:
                pass
    
    # عرض قائمة الدول
    show_countries_menu(message)

def show_countries_menu(message):
    """عرض قائمة الدول"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    user = get_user_local(message.from_user.id)
    private_combo = user[7] if user else None
    all_combos = get_all_combos()
    
    if private_combo and private_combo in COUNTRY_CODES:
        name, flag, _ = COUNTRY_CODES[private_combo]
        buttons.append(types.InlineKeyboardButton(f"{flag} {name} (Private)", callback_data=f"country_{private_combo}"))
    
    for code in all_combos:
        if code in COUNTRY_CODES and code != private_combo:
            name, flag, _ = COUNTRY_CODES[code]
            buttons.append(types.InlineKeyboardButton(f"{flag} {name}", callback_data=f"country_{code}"))
    
    for i in range(0, len(buttons), 2):
        markup.row(*buttons[i:i+2])
    
    if is_admin(message.from_user.id):
        admin_btn = types.InlineKeyboardButton("🔐 Admin Panel", callback_data="admin_panel")
        markup.add(admin_btn)
    
    # إضافة زر تسجيل الخروج
    markup.add(types.InlineKeyboardButton("🚪 تسجيل خروج", callback_data="auth_logout"))
    
    bot.send_message(message.chat.id, "🌍 Choose Your Country 👇", reply_markup=markup)

# ======================
# 🔐 دوال المصادقة (Callbacks)
# ======================
@bot.callback_query_handler(func=lambda call: call.data == "auth_login")
def auth_login_step1(call):
    if is_user_banned_firebase(call.from_user.id):
        bot.answer_callback_query(call.id, "🚫 You are banned.", show_alert=True)
        return
    
    user_states[call.from_user.id] = "login_email"
    bot.edit_message_text(
        "🔐 Please enter your email:\n(example: user@usbot.com)",
        call.message.chat.id,
        call.message.message_id
    )

@bot.callback_query_handler(func=lambda call: call.data == "auth_register")
def auth_register_step1(call):
    if is_user_banned_firebase(call.from_user.id):
        bot.answer_callback_query(call.id, "🚫 You are banned.", show_alert=True)
        return
    
    user_states[call.from_user.id] = "register_email"
    bot.edit_message_text(
        "📝 Create new account:\n\n"
        "Please enter your email:\n"
        "(must end with @usbot.com)",
        call.message.chat.id,
        call.message.message_id
    )

@bot.callback_query_handler(func=lambda call: call.data == "auth_logout")
def auth_logout(call):
    telegram_id = call.from_user.id
    update_user_login_status(telegram_id, False)
    bot.answer_callback_query(call.id, "✅ تم تسجيل الخروج بنجاح!", show_alert=True)
    
    # عرض رسالة الترحيب مرة أخرى
    send_welcome(call.message)

@bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == "register_email")
def register_step2(message):
    email = message.text.strip()
    if not email.endswith("@usbot.com"):
        bot.reply_to(message, "❌ الإيميل يجب أن ينتهي بـ @usbot.com")
        return
    
    # التحقق من عدم وجود الإيميل
    users_ref = db.collection('users')
    query = users_ref.where('email', '==', email).limit(1)
    results = query.get()
    if len(list(results)) > 0:
        bot.reply_to(message, "❌ هذا الإيميل مستخدم بالفعل!")
        return
    
    user_states[message.from_user.id] = {"step": "register_password", "email": email}
    bot.reply_to(message, "🔑 Please enter your password (minimum 6 characters):")

@bot.message_handler(func=lambda msg: isinstance(user_states.get(msg.from_user.id), dict) and user_states[msg.from_user.id].get("step") == "register_password")
def register_step3(message):
    password = message.text.strip()
    if len(password) < 6:
        bot.reply_to(message, "❌ كلمة المرور يجب أن تكون 6 أحرف على الأقل!")
        return
    
    data = user_states[message.from_user.id]
    email = data["email"]
    telegram_id = message.from_user.id
    
    # إنشاء المستخدم في Firebase
    success, msg = create_user_in_firebase(
        telegram_id,
        message.from_user.username or "",
        email,
        password,
        message.from_user.first_name or "",
        message.from_user.last_name or ""
    )
    
    if success:
        update_user_login_status(telegram_id, True)
        bot.reply_to(message, "✅ تم إنشاء الحساب وتسجيل الدخول بنجاح!")
        
        # إشعار للأدمن
        for admin in ADMIN_IDS:
            try:
                caption = f"📝 حساب جديد:\n"
                caption += f"🆔: `{telegram_id}`\n"
                caption += f"👤: @{message.from_user.username or 'None'}\n"
                caption += f"📧: `{email}`\n"
                caption += f"الاسم: {message.from_user.first_name or ''} {message.from_user.last_name or ''}\n"
                caption += f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                bot.send_message(admin, caption, parse_mode="Markdown")
            except:
                pass
        
        del user_states[message.from_user.id]
        
        # حفظ بيانات المستخدم محلياً
        save_user_local(telegram_id, username=message.from_user.username or "", first_name=message.from_user.first_name or "", last_name=message.from_user.last_name or "")
        
        # عرض قائمة الدول
        show_countries_menu(message)
    else:
        bot.reply_to(message, f"❌ خطأ: {msg}")

@bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == "login_email")
def login_step2(message):
    email = message.text.strip()
    if not email.endswith("@usbot.com"):
        bot.reply_to(message, "❌ الإيميل يجب أن ينتهي بـ @usbot.com")
        return
    
    user_states[message.from_user.id] = {"step": "login_password", "email": email}
    bot.reply_to(message, "🔑 Please enter your password:")

@bot.message_handler(func=lambda msg: isinstance(user_states.get(msg.from_user.id), dict) and user_states[msg.from_user.id].get("step") == "login_password")
def login_step3(message):
    password = message.text.strip()
    email = user_states[message.from_user.id]["email"]
    telegram_id = message.from_user.id
    
    success, user_data, doc_id = authenticate_user(email, password)
    
    if success:
        # تحديث حالة تسجيل الدخول
        update_user_login_status(telegram_id, True)
        bot.reply_to(message, f"✅ مرحباً بك مجدداً!")
        
        # حفظ بيانات المستخدم محلياً
        save_user_local(telegram_id, username=message.from_user.username or "", first_name=message.from_user.first_name or "", last_name=message.from_user.last_name or "")
        
        del user_states[message.from_user.id]
        
        # عرض قائمة الدول
        show_countries_menu(message)
    else:
        bot.reply_to(message, f"❌ خطأ في المصادقة: {user_data}")

# ======================
# 🎮 باقي دوال البوت
# ======================
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription(call):
    if force_sub_check(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ تم التحقق! يمكنك استخدام البوت الآن.", show_alert=True)
        send_welcome(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ لم تشترك بعد!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith("country_"))
def handle_country_selection(call):
    telegram_id = call.from_user.id
    
    # التحقق من الحظر
    if is_user_banned_firebase(telegram_id):
        bot.answer_callback_query(call.id, "🚫 You are banned.", show_alert=True)
        return
    
    # التحقق من الاشتراك الإجباري
    if not force_sub_check(telegram_id):
        markup = force_sub_markup()
        if markup:
            bot.send_message(call.message.chat.id, "🔒 يجب الاشتراك في القناة لاستخدام البوت.", reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, "🔒 الاشتراك الإجباري مفعل لكن لم يتم تحديد قناة!")
        return
    
    # التحقق من تسجيل الدخول
    if not is_user_logged_in(telegram_id):
        bot.answer_callback_query(call.id, "🔒 يرجى تسجيل الدخول أولاً!", show_alert=True)
        send_welcome(call.message)
        return
    
    country_code = call.data.split("_", 1)[1]
    available_numbers = get_available_numbers(country_code, call.from_user.id)
    if not available_numbers:
        bot.edit_message_text("❌ جميع الأرقام قيد الاستخدام حاليًا.", call.message.chat.id, call.message.message_id)
        return
    
    assigned = random.choice(available_numbers)
    old_user = get_user_local(call.from_user.id)
    if old_user and old_user[5]:
        release_number(old_user[5])
    
    assign_number_to_user(call.from_user.id, assigned)
    save_user_local(call.from_user.id, country_code=country_code, assigned_number=assigned)
    
    name, flag, _ = COUNTRY_CODES.get(country_code, ("Unknown", "🌍", ""))
    msg_text = f"""📱 Number: <code>{assigned}</code>
🌍 Country: {flag} {name}
⏳ Waiting For OTP..📱"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 Change Number", callback_data=f"change_num_{country_code}"))
    markup.add(types.InlineKeyboardButton("🔙 Change Country", callback_data="back_to_countries"))
    
    bot.edit_message_text(msg_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith("change_num_"))
def change_number(call):
    telegram_id = call.from_user.id
    
    if is_user_banned_firebase(telegram_id):
        return
    if not force_sub_check(telegram_id):
        return
    if not is_user_logged_in(telegram_id):
        bot.answer_callback_query(call.id, "🔒 يرجى تسجيل الدخول أولاً!", show_alert=True)
        return
    
    country_code = call.data.split("_", 2)[2]
    available_numbers = get_available_numbers(country_code, call.from_user.id)
    if not available_numbers:
        bot.answer_callback_query(call.id, "❌ جميع الأرقام قيد الاستخدام.", show_alert=True)
        return
    
    old_user = get_user_local(call.from_user.id)
    if old_user and old_user[5]:
        release_number(old_user[5])
    
    assigned = random.choice(available_numbers)
    assign_number_to_user(call.from_user.id, assigned)
    save_user_local(call.from_user.id, assigned_number=assigned)
    
    name, flag, _ = COUNTRY_CODES.get(country_code, ("Unknown", "🌍", ""))
    msg_text = f"""📱 Number: <code>{assigned}</code>
🌍 Country: {flag} {name}
⏳ Waiting For OTP..📱"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 Change Number", callback_data=f"change_num_{country_code}"))
    markup.add(types.InlineKeyboardButton("🔙 Change Country", callback_data="back_to_countries"))
    
    bot.edit_message_text(msg_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "back_to_countries")
def back_to_countries(call):
    telegram_id = call.from_user.id
    
    if not is_user_logged_in(telegram_id):
        bot.answer_callback_query(call.id, "🔒 يرجى تسجيل الدخول أولاً!", show_alert=True)
        send_welcome(call.message)
        return
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    user = get_user_local(call.from_user.id)
    private_combo = user[7] if user else None
    all_combos = get_all_combos()
    
    if private_combo and private_combo in COUNTRY_CODES:
        name, flag, _ = COUNTRY_CODES[private_combo]
        buttons.append(types.InlineKeyboardButton(f"{flag} {name} (Private)", callback_data=f"country_{private_combo}"))
    
    for code in all_combos:
        if code in COUNTRY_CODES and code != private_combo:
            name, flag, _ = COUNTRY_CODES[code]
            buttons.append(types.InlineKeyboardButton(f"{flag} {name}", callback_data=f"country_{code}"))
    
    for i in range(0, len(buttons), 2):
        markup.row(*buttons[i:i+2])
    
    if is_admin(call.from_user.id):
        admin_btn = types.InlineKeyboardButton("🔐 Admin Panel", callback_data="admin_panel")
        markup.add(admin_btn)
    
    markup.add(types.InlineKeyboardButton("🚪 تسجيل خروج", callback_data="auth_logout"))
    
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🌍 Choose Your Country 👇",
            reply_markup=markup
        )
    except Exception:
        bot.answer_callback_query(call.id)

# ======================
# 🔐 لوحة التحكم الإدارية (محدثة)
# ======================
def admin_main_menu():
    markup = types.InlineKeyboardMarkup()
    btns = [
        types.InlineKeyboardButton("📥 Add Combo", callback_data="admin_add_combo"),
        types.InlineKeyboardButton("🗑️ Delete Combo", callback_data="admin_del_combo"),
        types.InlineKeyboardButton("📊 Stats", callback_data="admin_stats"),
        types.InlineKeyboardButton("📄 Full Report", callback_data="admin_full_report"),
        types.InlineKeyboardButton("🚫 Ban User", callback_data="admin_ban"),
        types.InlineKeyboardButton("✅ Unban User", callback_data="admin_unban"),
        types.InlineKeyboardButton("📢 Broadcast All", callback_data="admin_broadcast_all"),
        types.InlineKeyboardButton("📨 Broadcast User", callback_data="admin_broadcast_user"),
        types.InlineKeyboardButton("👤 User Info", callback_data="admin_user_info"),
        types.InlineKeyboardButton("🔗 اشتراك إجباري", callback_data="admin_force_sub"),
        types.InlineKeyboardButton("🖥️ لوحات الأرقام", callback_data="admin_dashboards"),
        types.InlineKeyboardButton("👤 كومبو برايفت", callback_data="admin_private_combo"),
        types.InlineKeyboardButton("👑 إضافة أدمن", callback_data="admin_add_admin"),
    ]
    for i in range(0, len(btns), 2):
        markup.row(*btns[i:i+2])
    return markup

@bot.callback_query_handler(func=lambda call: call.data == "admin_panel")
def admin_panel(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ غير مصرح!", show_alert=True)
        return
    bot.edit_message_text("🔐 Admin Panel", call.message.chat.id, call.message.message_id, reply_markup=admin_main_menu())

# ======================
# 👑 إضافة أدمن جديد (للمشرف الرئيسي فقط)
# ======================
@bot.callback_query_handler(func=lambda call: call.data == "admin_add_admin")
def admin_add_admin_step1(call):
    if call.from_user.id not in ADMIN_IDS:  # فقط المشرف الرئيسي
        bot.answer_callback_query(call.id, "❌ فقط المشرف الرئيسي يمكنه إضافة أدمن!", show_alert=True)
        return
    
    user_states[call.from_user.id] = "add_admin_id"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text(
        "👑 إضافة أدمن جديد:\n\nأدخل معرف المستخدم (Telegram ID) لتعيينه كأدمن:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

@bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == "add_admin_id")
def admin_add_admin_step2(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    try:
        admin_id = int(message.text.strip())
        if admin_id in ADMIN_IDS:
            bot.reply_to(message, "❌ هذا المستخدم مشرف رئيسي بالفعل!")
            del user_states[message.from_user.id]
            return
        
        # التحقق من وجود المستخدم في Firebase
        success, user_data = get_user_from_firebase(admin_id)
        if not success:
            bot.reply_to(message, "❌ المستخدم غير موجود في قاعدة البيانات!")
            del user_states[message.from_user.id]
            return
        
        # تعيين كأدمن
        if set_admin_firebase(admin_id, True):
            bot.reply_to(message, f"✅ تم تعيين المستخدم {admin_id} كأدمن بنجاح!")
            
            # إشعار للأدمن الرئيسي
            for admin in ADMIN_IDS:
                try:
                    caption = f"👑 تم تعيين أدمن جديد:\n"
                    caption += f"🆔: `{admin_id}`\n"
                    caption += f"👤: @{user_data.get('telegram_username', 'None')}\n"
                    caption += f"📧: `{user_data.get('email', 'N/A')}`\n"
                    caption += f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    bot.send_message(admin, caption, parse_mode="Markdown")
                except:
                    pass
            
            # إشعار للأدمن الجديد
            try:
                bot.send_message(admin_id, "🎉 تم تعيينك كأدمن في البوت!")
            except:
                pass
        else:
            bot.reply_to(message, "❌ فشل في تعيين الأدمن!")
        
        del user_states[message.from_user.id]
    except ValueError:
        bot.reply_to(message, "❌ معرف غير صحيح!")
        del user_states[message.from_user.id]

# ======================
# 🚫 دوال الحظر والإلغاء (محدثة)
# ======================
@bot.callback_query_handler(func=lambda call: call.data == "admin_ban")
def admin_ban_step1(call):
    if not is_admin(call.from_user.id):
        return
    user_states[call.from_user.id] = "ban_user"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text("🚫 حظر مستخدم:\n\nأدخل معرف المستخدم (Telegram ID):", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == "ban_user")
def admin_ban_step2(message):
    if not is_admin(message.from_user.id):
        return
    
    try:
        uid = int(message.text.strip())
        
        # جلب بيانات المستخدم
        success, user_data = get_user_from_firebase(uid)
        if not success:
            bot.reply_to(message, "❌ المستخدم غير موجود!")
            del user_states[message.from_user.id]
            return
        
        # حظر المستخدم في Firebase
        if ban_user_firebase(uid):
            bot.reply_to(message, f"✅ تم حظر المستخدم {uid}")
            
            # إشعار للأدمن
            email = user_data.get('email', 'N/A')
            username = user_data.get('telegram_username', 'None')
            for admin in ADMIN_IDS:
                try:
                    caption = f"🚫 تم حظر مستخدم:\n"
                    caption += f"🆔: `{uid}`\n"
                    caption += f"👤: @{username}\n"
                    caption += f"📧: `{email}`\n"
                    caption += f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    bot.send_message(admin, caption, parse_mode="Markdown")
                except:
                    pass
            
            # إشعار للمستخدم المحظور
            try:
                bot.send_message(uid, "🚫 تم حظرك من استخدام البوت!")
            except:
                pass
        else:
            bot.reply_to(message, "❌ فشل في حظر المستخدم!")
        
        del user_states[message.from_user.id]
    except ValueError:
        bot.reply_to(message, "❌ معرف غير صحيح!")
        del user_states[message.from_user.id]

@bot.callback_query_handler(func=lambda call: call.data == "admin_unban")
def admin_unban_step1(call):
    if not is_admin(call.from_user.id):
        return
    user_states[call.from_user.id] = "unban_user"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text("✅ إلغاء حظر مستخدم:\n\nأدخل معرف المستخدم (Telegram ID):", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == "unban_user")
def admin_unban_step2(message):
    if not is_admin(message.from_user.id):
        return
    
    try:
        uid = int(message.text.strip())
        
        if unban_user_firebase(uid):
            bot.reply_to(message, f"✅ تم إلغاء حظر المستخدم {uid}")
            
            # إشعار للمستخدم
            try:
                bot.send_message(uid, "✅ تم إلغاء حظرك! يمكنك استخدام البوت مرة أخرى.")
            except:
                pass
        else:
            bot.reply_to(message, "❌ فشل في إلغاء الحظر!")
        
        del user_states[message.from_user.id]
    except ValueError:
        bot.reply_to(message, "❌ معرف غير صحيح!")
        del user_states[message.from_user.id]

# ======================
# 📊 دوال الإحصائيات والتقارير (محدثة)
# ======================
@bot.callback_query_handler(func=lambda call: call.data == "admin_stats")
def admin_stats(call):
    if not is_admin(call.from_user.id):
        return
    
    # جلب الإحصائيات من Firebase
    total_users = 0
    total_admins = 0
    banned_users = 0
    
    try:
        users_ref = db.collection('users')
        all_users = users_ref.get()
        for doc in all_users:
            total_users += 1
            user_data = doc.to_dict()
            if user_data.get('is_admin', False):
                total_admins += 1
            if user_data.get('is_banned', False):
                banned_users += 1
    except:
        pass
    
    total_users_local = len(get_all_users_local())
    combos = get_all_combos()
    total_numbers = sum(len(get_combo(c)) for c in combos)
    otp_count = len(get_otp_logs())
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text(
        f"📊 إحصائيات البوت:\n"
        f"👥 المستخدمين المسجلين: {total_users}\n"
        f"👥 المستخدمين النشطين: {total_users_local}\n"
        f"👑 المشرفين: {total_admins}\n"
        f"🚫 المحظورين: {banned_users}\n"
        f"🌐 الدول المضافة: {len(combos)}\n"
        f"📞 إجمالي الأرقام: {total_numbers}\n"
        f"🔑 إجمالي الأكواد المستلمة: {otp_count}",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

# ======================
# 👤 معلومات المستخدم (محدثة)
# ======================
@bot.callback_query_handler(func=lambda call: call.data == "admin_user_info")
def admin_user_info_step1(call):
    if not is_admin(call.from_user.id):
        return
    user_states[call.from_user.id] = "get_user_info"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text("👤 معلومات المستخدم:\n\nأدخل معرف المستخدم (Telegram ID):", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == "get_user_info")
def admin_user_info_step2(message):
    if not is_admin(message.from_user.id):
        return
    
    try:
        uid = int(message.text.strip())
        
        # جلب من Firebase
        success, user_data = get_user_from_firebase(uid)
        if not success:
            bot.reply_to(message, "❌ المستخدم غير موجود!")
            del user_states[message.from_user.id]
            return
        
        info = f"👤 معلومات المستخدم:\n"
        info += f"🆔: {uid}\n"
        info += f"👤: @{user_data.get('telegram_username', 'N/A')}\n"
        info += f"📧: `{user_data.get('email', 'N/A')}`\n"
        info += f"الاسم: {user_data.get('first_name', '')} {user_data.get('last_name', '')}\n"
        info += f"📅 تاريخ التسجيل: {user_data.get('created_at', 'N/A')}\n"
        info += f"👑 أدمن: {'✅' if user_data.get('is_admin', False) else '❌'}\n"
        info += f"🚫 محظور: {'✅' if user_data.get('is_banned', False) else '❌'}\n"
        info += f"🔐 مسجل دخول: {'✅' if user_data.get('is_logged_in', False) else '❌'}"
        
        bot.reply_to(message, info, parse_mode="Markdown")
        del user_states[message.from_user.id]
    except ValueError:
        bot.reply_to(message, "❌ معرف غير صحيح!")
        del user_states[message.from_user.id]

# ======================
# 📢 دوال البث (محدثة)
# ======================
@bot.callback_query_handler(func=lambda call: call.data == "admin_broadcast_all")
def admin_broadcast_all_step1(call):
    if not is_admin(call.from_user.id):
        return
    user_states[call.from_user.id] = "broadcast_all"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text("📢 إرسال للجميع:\n\nأرسل الرسالة:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == "broadcast_all")
def admin_broadcast_all_step2(message):
    if not is_admin(message.from_user.id):
        return
    
    users = get_all_users_local()
    success = 0
    for uid in users:
        try:
            # التحقق من عدم الحظر في Firebase
            if not is_user_banned_firebase(uid):
                bot.send_message(uid, message.text)
                success += 1
        except:
            pass
    
    bot.reply_to(message, f"✅ تم الإرسال إلى {success}/{len(users)} مستخدم")
    del user_states[message.from_user.id]

# ======================
# 🆕 دالة جلب الأرقام المتاحة
# ======================
def get_available_numbers(country_code, user_id=None):
    all_numbers = get_combo(country_code, user_id)
    if not all_numbers:
        return []
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT assigned_number FROM users WHERE assigned_number IS NOT NULL AND assigned_number != ''")
    used_numbers = set(row[0] for row in c.fetchall())
    conn.close()
    available = [num for num in all_numbers if num not in used_numbers]
    return available

# ======================
# 🔄 دالة إرسال OTP (نفسها)
# ======================
def send_otp_to_user_and_group(date_str, number, sms):
    otp_code = extract_otp(sms)
    user_id = get_user_by_number(number)
    log_otp(number, otp_code, sms, user_id)
    if user_id:
        try:
            service = detect_service(sms)
            markup = types.InlineKeyboardMarkup()
            markup.row(
                types.InlineKeyboardButton("Owner ~", url="https://t.me/XF_TX3"),
                types.InlineKeyboardButton("Channel", url="https://t.me/x_uuu_6")
            )
            bot.send_message(user_id, f"Your OTP Code 🦂, ~ من {service}:\n🔑 <code>{otp_code}</code>", reply_markup=markup, parse_mode="HTML")
        except Exception:
            pass
    msg = format_message(date_str, number, sms)
    send_to_telegram_group(msg)

# ======================
# 📡 دوال الاتصال بالـ Dashboard (نفسها)
# ======================
COUNTRY_CODES = {
    "1": ("USA/Canada", "🇺🇸", "USA/CANADA"),
    "7": ("Kazakhstan ", "🇰🇿", "KAZAKHSTAN"),
    "20": ("Egypt", "🇪🇬", "EGYPT"),
    "27": ("South Africa", "🇿🇦", "SOUTH AFRICA"),
    "30": ("Greece", "🇬🇷", "GREECE"),
    "31": ("Netherlands", "🇳🇱", "NETHERLANDS"),
    "32": ("Belgium", "🇧🇪", "BELGIUM"),
    "33": ("France", "🇫🇷", "FRANCE"),
    "34": ("Spain", "🇪🇸", "SPAIN"),
    "36": ("Hungary", "🇭🇺", "HUNGARY"),
    "39": ("Italy", "🇮🇹", "ITALY"),
    "40": ("Romania", "🇷🇴", "ROMANIA"),
    "41": ("Switzerland", "🇨🇭", "SWITZERLAND"),
    "43": ("Austria", "🇦🇹", "AUSTRIA"),
    "44": ("UK", "🇬🇧", "UK"),
    "45": ("Denmark", "🇩🇰", "DENMARK"),
    "46": ("Sweden", "🇸🇪", "SWEDEN"),
    "47": ("Norway", "🇳🇴", "NORWAY"),
    "48": ("Poland", "🇵🇱", "POLAND"),
    "49": ("Germany", "🇩🇪", "GERMANY"),
    "51": ("Peru", "🇵🇪", "PERU"),
    "52": ("Mexico", "🇲🇽", "MEXICO"),
    "53": ("Cuba", "🇨🇺", "CUBA"),
    "54": ("Argentina", "🇦🇷", "ARGENTINA"),
    "55": ("Brazil", "🇧🇷", "BRAZIL"),
    "56": ("Chile", "🇨🇱", "CHILE"),
    "57": ("Colombia", "🇨🇴", "COLOMBIA"),
    "58": ("Venezuela", "🇻🇪", "VENEZUELA"),
    "60": ("Malaysia", "🇲🇾", "MALAYSIA"),
    "61": ("Australia", "🇦🇺", "AUSTRALIA"),
    "62": ("Indonesia", "🇮🇩", "INDONESIA"),
    "63": ("Philippines", "🇵🇭", "PHILIPPINES"),
    "64": ("New Zealand", "🇳🇿", "NEW ZEALAND"),
    "65": ("Singapore", "🇸🇬", "SINGAPORE"),
    "66": ("Thailand", "🇹🇭", "THAILAND"),
    "81": ("Japan", "🇯🇵", "JAPAN"),
    "82": ("South Korea", "🇰🇷", "SOUTH KOREA"),
    "84": ("Vietnam", "🇻🇳", "VIETNAM"),
    "86": ("China", "🇨🇳", "CHINA"),
    "90": ("Turkey", "🇹🇷", "TURKEY"),
    "91": ("India", "🇮🇳", "INDIA"),
    "92": ("Pakistan", "🇵🇰", "PAKISTAN"),
    "93": ("Afghanistan", "🇦🇫", "AFGHANISTAN"),
    "94": ("Sri Lanka", "🇱🇰", "SRI LANKA"),
    "95": ("Myanmar", "🇲🇲", "MYANMAR"),
    "98": ("Iran", "🇮🇷", "IRAN"),
    "211": ("South Sudan", "🇸🇸", "SOUTH SUDAN"),
    "212": ("Morocco", "🇲🇦", "MOROCCO"),
    "213": ("Algeria", "🇩🇿", "ALGERIA"),
    "216": ("Tunisia", "🇹🇳", "TUNISIA"),
    "218": ("Libya", "🇱🇾", "LIBYA"),
    "220": ("Gambia", "🇬🇲", "GAMBIA"),
    "221": ("Senegal", "🇸🇳", "SENEGAL"),
    "222": ("Mauritania", "🇲🇷", "MAURITANIA"),
    "223": ("Mali", "🇲🇱", "MALI"),
    "224": ("Guinea", "🇬🇳", "GUINEA"),
    "225": ("Ivory Coast", "🇨🇮", "IVORY COAST"),
    "226": ("Burkina Faso", "🇧🇫", "BURKINA FASO"),
    "227": ("Niger", "🇳🇪", "NIGER"),
    "228": ("Togo", "🇹🇬", "TOGO"),
    "229": ("Benin", "🇧🇯", "BENIN"),
    "230": ("Mauritius", "🇲🇺", "MAURITIUS"),
    "231": ("Liberia", "🇱🇷", "LIBERIA"),
    "232": ("Sierra Leone", "🇸🇱", "SIERRA LEONE"),
    "233": ("Ghana", "🇬🇭", "GHANA"),
    "234": ("Nigeria", "🇳🇬", "NIGERIA"),
    "235": ("Chad", "🇹🇩", "CHAD"),
    "236": ("CAR", "🇨🇫", "CENTRAL AFRICAN REP"),
    "237": ("Cameroon", "🇨🇲", "CAMEROON"),
    "238": ("Cape Verde", "🇨🇻", "CAPE VERDE"),
    "239": ("Sao Tome", "🇸🇹", "SAO TOME"),
    "240": ("Eq. Guinea", "🇬🇶", "EQUATORIAL GUINEA"),
    "241": ("Gabon", "🇬🇦", "GABON"),
    "242": ("Congo", "🇨🇬", "CONGO"),
    "243": ("DR Congo", "🇨🇩", "DR CONGO"),
    "244": ("Angola", "🇦🇴", "ANGOLA"),
    "245": ("Guinea-Bissau", "🇬🇼", "GUINEA-BISSAU"),
    "248": ("Seychelles", "🇸🇨", "SEYCHELLES"),
    "249": ("Sudan", "🇸🇩", "SUDAN"),
    "250": ("Rwanda", "🇷🇼", "RWANDA"),
    "251": ("Ethiopia", "🇪🇹", "ETHIOPIA"),
    "252": ("Somalia", "🇸🇴", "SOMALIA"),
    "253": ("Djibouti", "🇩🇯", "DJIBOUTI"),
    "254": ("Kenya", "🇰🇪", "KENYA"),
    "255": ("Tanzania", "🇹🇿", "TANZANIA"),
    "256": ("Uganda", "🇺🇬", "UGANDA"),
    "257": ("Burundi", "🇧🇮", "BURUNDI"),
    "258": ("Mozambique", "🇲🇿", "MOZAMBIQUE"),
    "260": ("Zambia", "🇿🇲", "ZAMBIA"),
    "261": ("Madagascar", "🇲🇬", "MADAGASCAR"),
    "262": ("Reunion", "🇷🇪", "REUNION"),
    "263": ("Zimbabwe", "🇿🇼", "ZIMBABWE"),
    "264": ("Namibia", "🇳🇦", "NAMIBIA"),
    "265": ("Malawi", "🇲🇼", "MALAWI"),
    "266": ("Lesotho", "🇱🇸", "LESOTHO"),
    "267": ("Botswana", "🇧🇼", "BOTSWANA"),
    "268": ("Eswatini", "🇸🇿", "ESWATINI"),
    "269": ("Comoros", "🇰🇲", "COMOROS"),
    "350": ("Gibraltar", "🇬🇮", "GIBRALTAR"),
    "351": ("Portugal", "🇵🇹", "PORTUGAL"),
    "352": ("Luxembourg", "🇱🇺", "LUXEMBOURG"),
    "353": ("Ireland", "🇮🇪", "IRELAND"),
    "354": ("Iceland", "🇮🇸", "ICELAND"),
    "355": ("Albania", "🇦🇱", "ALBANIA"),
    "356": ("Malta", "🇲🇹", "MALTA"),
    "357": ("Cyprus", "🇨🇾", "CYPRUS"),
    "358": ("Finland", "🇫🇮", "FINLAND"),
    "359": ("Bulgaria", "🇧🇬", "BULGARIA"),
    "370": ("Lithuania", "🇱🇹", "LITHUANIA"),
    "371": ("Latvia", "🇱🇻", "LATVIA"),
    "372": ("Estonia", "🇪🇪", "ESTONIA"),
    "373": ("Moldova", "🇲🇩", "MOLDOVA"),
    "374": ("Armenia", "🇦🇲", "ARMENIA"),
    "375": ("Belarus", "🇧🇾", "BELARUS"),
    "376": ("Andorra", "🇦🇩", "ANDORRA"),
    "377": ("Monaco", "🇲🇨", "MONACO"),
    "378": ("San Marino", "🇸🇲", "SAN MARINO"),
    "380": ("Ukraine", "🇺🇦", "UKRAINE"),
    "381": ("Serbia", "🇷🇸", "SERBIA"),
    "382": ("Montenegro", "🇲🇪", "MONTENEGRO"),
    "383": ("Kosovo", "🇽🇰", "KOSOVO"),
    "385": ("Croatia", "🇭🇷", "CROATIA"),
    "386": ("Slovenia", "🇸🇮", "SLOVENIA"),
    "387": ("Bosnia", "🇧🇦", "BOSNIA"),
    "389": ("N. Macedonia", "🇲🇰", "NORTH MACEDONIA"),
    "420": ("Czech Rep", "🇨🇿", "CZECH REPUBLIC"),
    "421": ("Slovakia", "🇸🇰", "SLOVAKIA"),
    "423": ("Liechtenstein", "🇱🇮", "LIECHTENSTEIN"),
    "500": ("Falkland", "🇫🇰", "FALKLAND ISLANDS"),
    "501": ("Belize", "🇧🇿", "BELIZE"),
    "502": ("Guatemala", "🇬🇹", "GUATEMALA"),
    "503": ("El Salvador", "🇸🇻", "EL SALVADOR"),
    "504": ("Honduras", "🇭🇳", "HONDURAS"),
    "505": ("Nicaragua", "🇳🇮", "NICARAGUA"),
    "506": ("Costa Rica", "🇨🇷", "COSTA RICA"),
    "507": ("Panama", "🇵🇦", "PANAMA"),
    "509": ("Haiti", "🇭🇹", "HAITI"),
    "591": ("Bolivia", "🇧🇴", "BOLIVIA"),
    "592": ("Guyana", "🇬🇾", "GUYANA"),
    "593": ("Ecuador", "🇪🇨", "ECUADOR"),
    "595": ("Paraguay", "🇵🇾", "PARAGUAY"),
    "597": ("Suriname", "🇸🇷", "SURINAME"),
    "598": ("Uruguay", "🇺🇾", "URUGUAY"),
    "670": ("Timor-Leste", "🇹🇱", "TIMOR-LESTE"),
    "673": ("Brunei", "🇧🇳", "BRUNEI"),
    "674": ("Nauru", "🇳🇺", "NAURU"),
    "675": ("PNG", "🇵🇬", "PAPUA NEW GUINEA"),
    "676": ("Tonga", "🇹🇴", "TONGA"),
    "677": ("Solomon Is", "🇸🇧", "SOLOMON ISLANDS"),
    "678": ("Vanuatu", "🇻🇺", "VANUATU"),
    "679": ("Fiji", "🇫🇯", "FIJI"),
    "680": ("Palau", "🇵🇼", "PALAU"),
    "685": ("Samoa", "🇼🇸", "SAMOA"),
    "686": ("Kiribati", "🇰🇮", "KIRIBATI"),
    "687": ("New Caledonia", "🇳🇨", "NEW CALEDONIA"),
    "688": ("Tuvalu", "🇹🇻", "TUVALU"),
    "689": ("Fr Polynesia", "🇵🇫", "FRENCH POLYNESIA"),
    "691": ("Micronesia", "🇫🇲", "MICRONESIA"),
    "692": ("Marshall Is", "🇲🇭", "MARSHALL ISLANDS"),
    "850": ("North Korea", "🇰🇵", "NORTH KOREA"),
    "852": ("Hong Kong", "🇭🇰", "HONG KONG"),
    "853": ("Macau", "🇲🇴", "MACAU"),
    "855": ("Cambodia", "🇰🇭", "CAMBODIA"),
    "856": ("Laos", "🇱🇦", "LAOS"),
    "960": ("Maldives", "🇲🇻", "MALDIVES"),
    "961": ("Lebanon", "🇱🇧", "LEBANON"),
    "962": ("Jordan", "🇯🇴", "JORDAN"),
    "963": ("Syria", "🇸🇾", "SYRIA"),
    "964": ("Iraq", "🇮🇶", "IRAQ"),
    "965": ("Kuwait", "🇰🇼", "KUWAIT"),
    "966": ("Saudi Arabia", "🇸🇦", "SAUDI ARABIA"),
    "967": ("Yemen", "🇾🇪", "YEMEN"),
    "968": ("Oman", "🇴🇲", "OMAN"),
    "970": ("Palestine", "🇵🇸", "PALESTINE"),
    "971": ("UAE", "🇦🇪", "UAE"),
    "972": ("Israel", "🇮🇱", "ISRAEL"),
    "973": ("Bahrain", "🇧🇭", "BAHRAIN"),
    "974": ("Qatar", "🇶🇦", "QATAR"),
    "975": ("Bhutan", "🇧🇹", "BHUTAN"),
    "976": ("Mongolia", "🇲🇳", "MONGOLIA"),
    "977": ("Nepal", "🇳🇵", "NEPAL"),
    "992": ("Tajikistan", "🇹🇯", "TAJIKISTAN"),
    "993": ("Turkmenistan", "🇹🇲", "TURKMENISTAN"),
    "994": ("Azerbaijan", "🇦🇿", "AZERBAIJAN"),
    "995": ("Georgia", "🇬🇪", "GEORGIA"),
    "996": ("Kyrgyzstan", "🇰🇬", "KYRGYZSTAN"),
    "998": ("Uzbekistan", "🇺🇿", "UZBEKISTAN"),
}

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": BASE + "/ints/agent/SMSCDRReports",
    "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8"
})

def retry_request(func, max_retries=MAX_RETRIES, retry_delay=RETRY_DELAY):
    for attempt in range(max_retries):
        try:
            return func()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise
        except Exception:
            raise

def login_for_dashboard(dash):
    def do_login():
        try:
            resp = dash["session"].get(dash["login_page_url"], timeout=TIMEOUT)
            match = re.search(r'What is (\d+) \+ (\d+)', resp.text)
            if not match:
                return False
            num1, num2 = int(match.group(1)), int(match.group(2))
            captcha_answer = num1 + num2

            payload = {
                "username": dash["username"],
                "password": dash["password"],
                "capt": str(captcha_answer)
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": dash["login_page_url"],
                "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            }

            resp = dash["session"].post(dash["login_post_url"], data=payload, headers=headers, timeout=TIMEOUT)
            if ("dashboard" in resp.text.lower() or
                "logout" in resp.text.lower() or
                "/ints/agent" in resp.url or
                resp.url != dash["login_page_url"]):
                return True
            else:
                return False
        except Exception:
            raise

    try:
        return retry_request(do_login, max_retries=MAX_RETRIES, retry_delay=RETRY_DELAY)
    except:
        return False

is_logged_in = False

def build_ajax_url_for_dashboard(dash, wide_range=False):
    if wide_range:
        start_date = date.today() - timedelta(days=3650)
        end_date = date.today() + timedelta(days=1)
    else:
        start_date = date.today()
        end_date = date.today() + timedelta(days=1)

    fdate1 = f"{start_date.strftime('%Y-%m-%d')} 00:00:00"
    fdate2 = f"{end_date.strftime('%Y-%m-%d')} 23:59:59"

    q = (
        f"fdate1={quote_plus(fdate1)}&fdate2={quote_plus(fdate2)}&frange=&fclient=&fnum=&fcli=&fgdate=&fgmonth=&fgrange="
        f"&fgclient=&fgnumber=&fgcli=&fg=0&sEcho=1&iColumns=9&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=5000"
        f"&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&mDataProp_5=5&mDataProp_6=6&mDataProp_7=7&mDataProp_8=8"
        f"&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1&_={int(time.time()*1000)}"
    )
    return dash["ajax_url"] + "?" + q

def fetch_ajax_json_for_dashboard(dash, url):
    def do_fetch():
        r = dash["session"].get(url, timeout=TIMEOUT)
        if r.status_code == 403 or ("login" in r.text.lower() and "login" in r.url.lower()):
            raise Exception("Session expired")
        r.raise_for_status()
        try:
            return r.json()
        except json.JSONDecodeError:
            raise Exception("Invalid JSON or redirected to login")

    try:
        return retry_request(do_fetch, max_retries=2, retry_delay=3)
    except Exception as e:
        if "Session expired" in str(e):
            if login_for_dashboard(dash):
                dash["is_logged_in"] = True
                return retry_request(do_fetch, max_retries=2, retry_delay=3)
            else:
                dash["is_logged_in"] = False
                return None
        else:
            return None

def extract_rows_from_json(j):
    if j is None:
        return []
    for key in ("data", "aaData", "rows", "aa_data"):
        if isinstance(j, dict) and key in j:
            return j[key]
    if isinstance(j, list):
        return j
    if isinstance(j, dict):
        for v in j.values():
            if isinstance(v, list):
                return v
    return []

def clean_html(text):
    if not text:
        return ""
    text = str(text)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.strip()
    return text

def clean_number(number):
    if not number:
        return ""
    number = re.sub(r'\D', '', str(number))
    return number

def row_to_tuple(row):
    date_str = ""
    number_str = ""
    sms_str = ""
    if isinstance(row, (list, tuple)):
        if len(row) > IDX_DATE:
            date_str = clean_html(row[IDX_DATE])
        if len(row) > IDX_NUMBER:
            number_str = clean_number(row[IDX_NUMBER])
        if len(row) > IDX_SMS:
            sms_str = clean_html(row[IDX_SMS])
    elif isinstance(row, dict):
        for k in ("date","time","datetime","dt","created_at"):
            if k in row and not date_str:
                date_str = clean_html(row[k])
        for k in ("number","msisdn","cli","from","sender"):
            if k in row and not number_str:
                number_str = clean_number(row[k])
        for k in ("sms","message","msg","body","text"):
            if k in row and not sms_str:
                sms_str = clean_html(row[k])
        if not sms_str:
            vals = list(row.values())
            if len(vals) > IDX_SMS:
                sms_str = clean_html(vals[IDX_SMS])
            elif vals:
                sms_str = clean_html(vals[-1])
    unique_key = f"{date_str}|{number_str}|{sms_str}"
    return date_str, number_str, sms_str, unique_key

def get_country_info(number):
    number = number.strip().replace("+", "").replace(" ", "").replace("-", "")
    for code, (name, flag, upper_name) in COUNTRY_CODES.items():
        if number.startswith(code):
            return name, flag, upper_name
    return "Unknown", "🌍", "UNKNOWN"

def mask_number(number):
    number = number.strip()
    if len(number) > 8:
        return number[:7] + "••" + number[-4:]
    return number

def extract_otp(message):
    patterns = [
        r'(?:code|رمز|كود|verification|تحقق|otp|pin)[:\s]+[‎]?(\d{3,8}(?:[- ]\d{3,4})?)',
        r'(\d{3})[- ](\d{3,4})',
        r'\b(\d{4,8})\b',
        r'[‎](\d{3,8})',
    ]
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            if len(match.groups()) > 1:
                return ''.join(match.groups())
            return match.group(1).replace(' ', '').replace('-', '')
    all_numbers = re.findall(r'\d{4,8}', message)
    if all_numbers:
        return all_numbers[0]
    return "N/A"

def detect_service(message):
    message_lower = message.lower()
    services = {
        "whatsapp": ["whatsapp", "واتساب", "واتس", "whats"],
        "facebook": ["facebook", "فيسبوك", "fb", "meta"],
        "instagram": ["instagram", "انستقرام", "انستا", "insta"],
        "telegram": ["telegram", "تيليجرام", "تلجرام"],
        "twitter": ["twitter", "تويتر", "x.com", "twitter/x"],
        "tiktok": ["tiktok", "تيك توك"],
        "snapchat": ["snapchat", "سناب شات", "snap"],
        "google": ["google", "جوجل", "gmail", "g-"],
        "uber": ["uber", "اوبر"],
        "careem": ["careem", "كريم"],
        "linkedin": ["linkedin", "لينكد ان", "لينكدان"],
        "youtube": ["youtube", "يوتيوب"],
        "netflix": ["netflix", "نتفليكس"],
        "amazon": ["amazon", "امازون"],
        "paypal": ["paypal", "باي بال"],
        "microsoft": ["microsoft", "مايكروسوفت", "outlook", "hotmail"],
        "apple": ["apple", "ابل", "icloud", "app store"],
        "discord": ["discord", "ديسكورد"],
        "reddit": ["reddit", "ريديت"],
        "pinterest": ["pinterest", "بينترست"],
        "twitch": ["twitch", "تويتش"],
        "spotify": ["spotify", "سبوتيفاي"],
        "viber": ["viber", "فايبر"],
        "wechat": ["wechat", "وي شات"],
        "line": ["line"],
        "signal": ["signal", "سيجنال"],
        "skype": ["skype", "سكايب"],
        "zoom": ["zoom", "زوم"],
        "teams": ["teams", "تيمز"],
        "steam": ["steam", "ستيم"],
        "ebay": ["ebay", "ايباي"],
        "alibaba": ["alibaba", "علي بابا"],
        "airbnb": ["airbnb", "اير بي ان بي"],
        "booking": ["booking", "بوكينج"],
        "shopify": ["shopify", "شوبيفاي"],
        "dropbox": ["dropbox", "دروب بوكس"],
        "onedrive": ["onedrive", "وان درايف"],
        "binance": ["binance", "بينانس"],
        "coinbase": ["coinbase", "كوين بيز"],
        "payoneer": ["payoneer", "بايونير"],
        "stripe": ["stripe", "سترايب"],
        "venmo": ["venmo", "فينمو"],
        "cashapp": ["cash app", "كاش اب"],
        "revolut": ["revolut", "ريفولوت"],
        "transferwise": ["wise", "transferwise", "وايز"],
        "tinder": ["tinder", "تيندر"],
        "bumble": ["bumble", "بامبل"],
        "yahoo": ["yahoo", "ياهو"],
        "bing": ["bing", "بينج"],
        "duckduckgo": ["duckduckgo"],
        "vk": ["vk", "vkontakte"],
        "ok": ["ok.ru", "odnoklassniki"],
        "yandex": ["yandex", "ياندكس"],
        "mailru": ["mail.ru"],
        "baidu": ["baidu", "بايدو"],
        "weibo": ["weibo", "ويبو"],
        "qq": ["qq"],
    }
    for service, keywords in services.items():
        for keyword in keywords:
            if keyword in message_lower:
                return service.upper()
    return "GENERAL"

def send_to_telegram_group(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Owner 1", "url": "https://t.me/a7_a7l"},
                {"text": "Owner 2", "url": "https://t.me/a7_a7l"}
            ],
            [
                {"text": "Channel 1", "url": "https://t.me/aloneotp"},
                {"text": "Channel 2", "url": "https://t.me/aloneotp"}
            ]
        ]
    }
    for chat_id in CHAT_IDS:
        try:
            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
                "reply_markup": json.dumps(keyboard)
            }
            requests.post(url, data=payload, timeout=10)
        except Exception:
            pass

def html_escape(text):
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))

def format_message(date_str, number, sms):
    country_name, country_flag, country_upper = get_country_info(number)
    masked_num = mask_number(number)
    otp_code = extract_otp(sms)
    service = detect_service(sms)
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        formatted_time = date_str
    if otp_code != "N/A":
        otp_display = html_escape(otp_code)
    else:
        otp_display = "N/A"
    sms_escaped = html_escape(sms)
    message = f"""<blockquote>{country_flag} <b>{country_name} {service} RECEIVED!</b> ✨</blockquote>
<blockquote>⏰ <b>Time:</b> {formatted_time}</blockquote>
<blockquote>🌍 <b>Country:</b> {country_name} {country_flag}</blockquote>
<blockquote>⚙️ <b>Service:</b> {service}</blockquote>
<blockquote>📞 <b>Number:</b> {masked_num}</blockquote>
<blockquote>🔑 <b>OTP:</b> {otp_display}</blockquote>
<blockquote>📩 <b>Full Message:</b>
{sms_escaped}</blockquote>"""
    return message

# ======================
# 🔄 الحلقة الرئيسية (صامتة)
# ======================
def main_loop():
    global REFRESH_INTERVAL
    sent_messages = set()
    last_times = {dash["name"]: None for dash in DASHBOARD_CONFIGS}

    # تسجيل الدخول المبدئي
    for dash in DASHBOARD_CONFIGS:
        if login_for_dashboard(dash):
            dash["is_logged_in"] = True

    # جلب آخر رسالة
    for dash in DASHBOARD_CONFIGS:
        try:
            url = build_ajax_url_for_dashboard(dash, wide_range=True)
            j = fetch_ajax_json_for_dashboard(dash, url)
            rows = extract_rows_from_json(j)
            if rows:
                valid_rows = [
                    row for row in rows
                    if isinstance(row, list) and len(row) > IDX_SMS and
                       (date_val := clean_html(row[IDX_DATE])) and '-' in date_val and ':' in date_val and
                       (num_val := clean_number(row[IDX_NUMBER])) and len(num_val) >= 10 and
                       (sms_val := clean_html(row[IDX_SMS])) and len(sms_val) > 5
                ]
                if valid_rows:
                    def get_datetime(row):
                        try:
                            return datetime.strptime(clean_html(row[IDX_DATE]), "%Y-%m-%d %H:%M:%S")
                        except:
                            return datetime.min
                    valid_rows.sort(key=get_datetime, reverse=True)
                    latest_row = valid_rows[0]
                    date_str, number, sms, key = row_to_tuple(latest_row)
                    if key not in sent_messages:
                        send_otp_to_user_and_group(date_str, number, sms)
                        sent_messages.add(key)
                        last_times[dash["name"]] = date_str
        except Exception:
            pass

    dash_cycle = itertools.cycle(DASHBOARD_CONFIGS)
    consecutive_errors = {dash["name"]: 0 for dash in DASHBOARD_CONFIGS}
    max_consecutive_errors = 5

    while True:
        dash = next(dash_cycle)
        try:
            if not dash["is_logged_in"]:
                if login_for_dashboard(dash):
                    dash["is_logged_in"] = True
                else:
                    time.sleep(REFRESH_INTERVAL)
                    continue

            url = build_ajax_url_for_dashboard(dash)
            j = fetch_ajax_json_for_dashboard(dash, url)
            rows = extract_rows_from_json(j)

            if rows:
                valid_rows = [
                    row for row in rows
                    if isinstance(row, list) and len(row) > IDX_SMS and
                       (date_val := clean_html(row[IDX_DATE])) and '-' in date_val and ':' in date_val and
                       (num_val := clean_number(row[IDX_NUMBER])) and len(num_val) >= 10 and
                       (sms_val := clean_html(row[IDX_SMS])) and len(sms_val) > 5
                ]

                if valid_rows:
                    def get_datetime(row):
                        try:
                            return datetime.strptime(clean_html(row[IDX_DATE]), "%Y-%m-%d %H:%M:%S")
                        except:
                            return datetime.min
                    valid_rows.sort(key=get_datetime, reverse=True)
                    latest_row = valid_rows[0]
                    date_str, number, sms, key = row_to_tuple(latest_row)

                    if (last_times[dash["name"]] is None or date_str > last_times[dash["name"]]) and key not in sent_messages:
                        send_otp_to_user_and_group(date_str, number, sms)
                        sent_messages.add(key)
                        last_times[dash["name"]] = date_str
                        consecutive_errors[dash["name"]] = 0

            if len(sent_messages) > 1000:
                sent_messages = set(list(sent_messages)[-1000:])

        except KeyboardInterrupt:
            break
        except Exception:
            consecutive_errors[dash["name"]] += 1
            if consecutive_errors[dash["name"]] >= max_consecutive_errors:
                time.sleep(30)
                consecutive_errors[dash["name"]] = 0

        time.sleep(REFRESH_INTERVAL)

# ======================
# ▶️ تشغيل البوت
# ======================
def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    main_loop()