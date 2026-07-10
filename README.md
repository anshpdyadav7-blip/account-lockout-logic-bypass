Markdown
# Authentication Oracle: Account Lockout Logic Flaw Exploit Framework

A modular, high-performance Python security toolset engineered to identify and exploit flawed authentication state handlers. This framework demonstrates how poorly implemented anti-brute-force rate limits (specifically, sequential account lockout thresholds) can be weaponized as an **Information Oracle** to systematically isolate valid usernames and bypass account lockout controls to extract passwords.

## 🔍 Vulnerability & Methodology Overview

Defensive mechanisms often implement localized account lockouts after a fixed threshold of consecutive failed login attempts (e.g., locking an account for 1 minute after 5 failures). If the application evaluates this failure tracker sequentially per-user and returns a distinct application state—such as unique error strings (`"Too many incorrect login attempts"`), changes in response size, or specific HTTP status codes—it introduces a logical side-channel.

This framework breaks the exploitation vector into two specialized, automated phases:

1. **Phase 1: Enumeration Oracle (`solve_usernames.py`)** Iterates through a directory of target entities and injects an exact payload block of failed authentication events per user. By monitoring state shifts dynamically, it filters out non-existent accounts and maps the precise perimeter of valid usernames.

2. **Phase 2: Authentication Bypass (`solve_passwords.py`)** Utilizes the discovered username to execute automated password spraying. To neutralize the application's lock counter, the engine maps a candidate password immediately followed by $N-1$ deliberate dummy failures (where $N$ is the lockout threshold). If the cluster fails to lock the account, the engine mathematically infers that the first password cleared the internal session failure counter, verifying a successful match without triggering a persistent lockout denial of service.

## 📁 Repository Architecture

```text
account-lockout-logic-bypass/
├── .gitignore               # Weaponized wordlist isolation controls
├── requirements.txt         # Core dependencies
├── README.md                # Technical documentation
├── solve_usernames.py       # Phase 1: User enumeration framework
└── solve_passwords.py       # Phase 2: Password extraction framework
🛠️ Engineering Features
Extensible Configuration: Built for rapid adaptation. By modifying the HTTP POST payload dictionaries and target parameter arrays, the code scales across custom enterprise login API endpoints (JSON, application/x-www-form-urlencoded).

Inline Routing Interception: Integrated default upstream proxying (127.0.0.1:8080) for seamless debugging, session inspection, and downstream analysis via Burp Suite Professional.

Robust Error Handling: Features defensive try/except exception wrappers to handle broken pipes, connection dropping, and missing wordlists gracefully without stack-trace leakage.

Persistent Connection Management: Built on top of requests.Session() architecture to track application cookie tracking and state synchronization cleanly.

🚀 Getting Started & Deployment
1. Environment Installation
Ensure Python 3.x is configured on your environment. Pull down operational requirements via pip:

Bash
pip install -r requirements.txt
2. Operational Wordlist Positioning (Required)
Massive fuzzing directories are explicitly stripped via .gitignore to prevent repository bloating. Populate your own dictionary sets in the root workspace prior to runtime execution.

For testing, generate localized diagnostic dictionaries directly via the CLI:

Bash
echo -e "admin\nguest\ninfo\nuser" > usernames.txt
echo -e "password123\n123456\nsecret" > passwords.txt
3. Target Customization & Parameters
Open the relevant script files to align the parameters with your target infrastructure. If testing against a PortSwigger Web Security Academy sandbox, capture your ephemeral lab ID and update the configuration variables at the top of the file:

Python
# --- TARGET CONFIGURATION BLOCK ---
LAB_URL = "[https://YOUR-DYNAMIC-TARGET-ID.web-security-academy.net/](https://YOUR-DYNAMIC-TARGET-ID.web-security-academy.net/)"
LOGIN_URL = f"{LAB_URL}login"
USERNAME_FILE = "usernames.txt"
PASSWORD_FILE = "passwords.txt"
Note: For deployment against corporate environments or bug bounty targets, adjust the data={} dictionary parameter arrays in the code to map precisely to the target application's parameter names (e.g., user, email, passwd).

4. Execution Pipeline
Step 1: Isolate Valid Corporate Targets

Bash
python3 solve_usernames.py
Step 2: Weaponize the Account Oracle against Target Credentials

Bash
python3 solve_passwords.py
⚠️ Disclaimer
This toolset is developed exclusively for authorized security audits, penetration testing engagements, and educational research within controlled training sandboxes. Execution against external infrastructure without an explicit, legally binding Rules of Engagement (RoE) agreement signed by system owners is strictly prohibited. The author accepts no liability for actions or damages caused by this code framework.
