# hennge-auth

Solution to the **HENNGE Global Challenge** (Backend / Recursion track) — a real-world backend challenge that tests algorithmic thinking, secure API integration, and attention to specification details.

---

## Challenge overview

The challenge has two independent parts:

### Part 1 — Algorithmic problem (`solution.py`)
Given N test cases, each with a list of integers, compute the **sum of the 4th powers of all non-positive numbers** using only recursion (no loops allowed).

**Constraints enforced:**
- All processing via recursive functions
- Custom FIFO Queue implemented from scratch (no `collections.deque`)
- Input validation: if the declared count `X` doesn't match actual number of elements, output `-1`
- Results printed only after all input is consumed

**Data structures implemented from scratch:**
- `Node` — linked list node
- `Queue` — FIFO queue (enqueue / dequeue / is_empty)
- `NumberList` — encapsulates input numbers with recursive sum logic

### Part 2 — Secure API submission (`submit.py`)
Send the solution to HENNGE's API using:
- **RFC 6238-compliant TOTP** with HMAC-SHA-512, 10-digit output, 30s window
- **HTTP Basic Authentication** with the OTP as password
- **JSON payload** over HTTPS POST

---

## Project structure

```
hennge-auth/
├── solution.py        # Algorithmic solution (Part 1)
├── submit.py          # TOTP auth + API submission (Part 2)
├── requirements.txt   # Python dependencies
└── README.md
```

---

## Run locally

```bash
git clone https://github.com/Alexanderzero6is/hennge-auth
cd hennge-auth
pip install -r requirements.txt
```

### Run the algorithm

```bash
python solution.py
```

Input format:
```
3          ← number of test cases
4          ← expected count for case 1
-1 2 -3 4  ← numbers
2
5 5
3
0 -2 1
```

Expected output:
```
82
-1
16
```

### Run the submission (requires your own credentials)

```bash
python submit.py
```

> ⚠️ Update `github_url` and `contact_email` in `submit.py` before running.

---

## Authentication flow

```
email + "HENNGECHALLENGE004"
        ↓
    encode to ASCII
        ↓
    base32 encode  ←── required by pyotp
        ↓
TOTP(secret, digits=10, interval=30, digest=SHA-512)
        ↓
Basic Auth header: base64(email:otp)
        ↓
POST https://api.challenge.hennge.com/...
     Content-Type: application/json
     Authorization: Basic <token>
```

---

## Key concepts demonstrated

| Concept | Implementation |
|---|---|
| Recursion (no loops) | `process_cases`, `_recursive_sum`, `print_results` |
| Custom data structures | `Queue`, `Node`, `NumberList` from scratch |
| RFC 6238 TOTP | HMAC-SHA-512, 10 digits, 30s step via `pyotp` |
| HTTP Basic Auth | `base64(email:otp)` in Authorization header |
| HTTPS API communication | `urllib.request` with error handling |
| Input validation | Count mismatch → output `-1` |

---

## Environment

- Python 3.10+
- Linux (debugged DNS resolution and request failures in terminal)
- No external libraries for Part 1 (pure Python)
- `pyotp` for RFC 6238 TOTP generation (Part 2)
