import pyotp
import json 
import base64
import hashlib
import urllib.request
import urllib.error

# Challenge endpoint
URL = "https://api.challenge.hennge.com/challenges/backend-recursion/004"


def TOTP(email: str) -> str:
    """
    Generate RFC6238-compliant TOTP using:
    - HMAC-SHA-512
    - 30-second time step
    - 10-digit output

    Shared secret is defined by the challenge specification as:
    email + "HENNGECHALLENGE004"
    """
    secret_ascii = (email + "HENNGECHALLENGE004").encode("ascii")
    secret_base32 = base64.b32encode(secret_ascii).decode("ascii")

    totp = pyotp.TOTP(
        secret_base32,
        digits=10,
        interval=30,
        digest=hashlib.sha512
    )
    return totp.now()


def basic_auth_header(email: str, otp: str) -> str:
    """
    Build HTTP Basic Authentication header.
    Format: Authorization: Basic base64(email:otp)
    """
    token = base64.b64encode(f"{email}:{otp}".encode("ascii")).decode("ascii")
    return f"Basic {token}"


def post_solution(github_url: str, contact_email: str, solution_language: str) -> None:
    """
    Send POST request with solution metadata and TOTP-based authentication.
    """
    json_data = {
        "github_url": github_url,
        "contact_email": contact_email,
        "solution_language": solution_language
    }

    body = json.dumps(json_data).encode("ascii")

    otp = TOTP(contact_email)
    auth = basic_auth_header(contact_email, otp)

    req = urllib.request.Request(
        URL,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": auth
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            print(response.status)
            print(response.read().decode("ascii"))

    except urllib.error.HTTPError as e:
        # Server responded but returned an HTTP error
        print(e.code)
        print(e.read().decode("ascii"))

    except Exception as e:
        # Network or unexpected runtime error
        print("Error:", e)


if __name__ == "__main__":
    github_url = "https://gist.github.com/Alexanderzero6is/b52fe3c9a2a8b1e7b0c2330a880bf1e9"
    contact_email = "alexander.cisneros@unmsm.edu.pe"
    solution_language = "python"

    post_solution(github_url, contact_email, solution_language)
