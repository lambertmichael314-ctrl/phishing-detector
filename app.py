import os
import sys
import re
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse

VERSION = "1.0.0"

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    template_folder = os.path.join(base_path, 'templates')
    static_folder = os.path.join(base_path, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

def analyze_url(url):
    scores = []
    risk_score = 0
    
    parsed = urlparse(url)
    # Get the hostname (the domain) and the full path
    hostname = parsed.hostname if parsed.hostname else parsed.netloc
    
    # 1. Check for @ symbol (Immediate High Risk)
    if "@" in url:
        scores.append("🔴 Contains '@' symbol - likely domain spoofing (High Risk)")
        risk_score += 40

    # 2. Check for IP address in hostname
    ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    if hostname and re.match(ip_pattern, hostname):
        scores.append("🔴 Uses raw IP address instead of domain (High Risk)")
        risk_score += 50

    # 3. Check for suspicious keywords anywhere in the URL
    # (Checking the full URL catches them in the domain AND the path)
    suspicious_keywords = ['login', 'verify', 'update', 'secure', 'account', 'banking', 'signin', 'confirm']
    found_keywords = [word for word in suspicious_keywords if word in url.lower()]
    if found_keywords:
        scores.append(f"🟡 Suspicious keywords detected: {', '.join(found_keywords)}")
        risk_score += 25

    # 4. Check for subdomain count
    if hostname and hostname.count('.') > 3:
        scores.append("🟡 Excessive subdomains detected (Medium Risk)")
        risk_score += 20

    # 5. Length Check
    if len(url) > 75:
        scores.append("🔵 URL is unusually long")
        risk_score += 10

    # --- UPDATED SOC THRESHOLDS ---
    # We want anything 30 or above to be flagged as Suspicious
    if risk_score >= 65:
        level = "MALICIOUS"
    elif risk_score >= 30:
        level = "SUSPICIOUS"
    else:
        level = "SAFE"

    return {
        "score": risk_score,
        "level": level,
        "findings": scores if scores else ["✅ No obvious heuristics triggered."]
    }

@app.route('/')
def index():
    return render_template('index.html', version=VERSION)

@app.route('/scan', methods=['POST'])
def scan():
    url = request.json.get('url', '')
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    result = analyze_url(url)
    return jsonify(result)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5002/')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(host='127.0.0.1', port=5002, debug=False)
