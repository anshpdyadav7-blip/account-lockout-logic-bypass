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

