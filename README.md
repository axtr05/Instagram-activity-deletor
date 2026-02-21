```
█████╗ ██╗  ██╗████████╗██████╗ 
██╔══██╗╚██╗██╔╝╚══██╔══╝██╔══██╗
███████║ ╚███╔╝    ██║   ██████╔╝
██╔══██║ ██╔██╗    ██║   ██╔══██╗
██║  ██║██╔╝ ██╗   ██║   ██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
```            

📱 InstaDel — Instagram Activity Cleaner
======================================

🧹 InstaDel is a Python-based automation tool designed to help you **clean and
manage your Instagram activity**. It allows you to remove **comments, likes,
reels, and posts** through a real browser session using **Selenium and
ChromeDriver**.

────────────────────────────────────────────────────────────

✨ FEATURES
----------
📝 Delete comments  
❤️ Remove likes  
🎬 Remove reels  
🖼️ Delete posts  
🔐 Manual login (no credentials stored)  
⚙️ Configurable batch deletion  
🔄 Graceful handling of Instagram rate limits  

────────────────────────────────────────────────────────────

⚙️ REQUIREMENTS
---------------
🐍 Python 3.x  
🌐 Google Chrome  
🧩 ChromeDriver (must match your Chrome version)  
🤖 Selenium  

────────────────────────────────────────────────────────────

📦 INSTALLATION
---------------
1️⃣ Install Selenium:
    pip install selenium

2️⃣ Download ChromeDriver:
    https://sites.google.com/chromium.org/driver/

3️⃣ Make sure `chromedriver` is available in your system PATH.

────────────────────────────────────────────────────────────

🚀 USAGE
--------
1️⃣ Run the script:
    python instdel.py

2️⃣ A Chrome browser window will open automatically.

3️⃣ Log in to Instagram **manually**.

4️⃣ If prompted, click **"Not now"** when asked to save login info.

5️⃣ Choose the desired option from the menu and let InstaDel do the work 🧹

────────────────────────────────────────────────────────────

🗑️ DELETION SETTINGS
--------------------
You can control how many items are deleted per batch by editing:

    AT_ONCE_DELETE = 20

Increase or decrease this value depending on your comfort level and rate limits.

────────────────────────────────────────────────────────────

⚠️ DISCLAIMER
-------------
🚨 This tool is intended **for educational purposes only**.

Automating Instagram actions **may violate Instagram’s Terms of Service** and
could result in temporary restrictions or permanent account bans.

⚠️ **Use at your own risk.**
The author is **not responsible** for any actions taken by Instagram against
your account.

────────────────────────────────────────────────────────────

📄 LICENSE
----------
MIT License

See the LICENSE file for full license text.

────────────────────────────────────────────────────────────

© 2026 Akshay Krishna

