from bs4 import BeautifulSoup
import requests

def analyze_url(url, html, headers):
    findings = []
    h = {k.lower(): v for k, v in headers.items()}
    soup = BeautifulSoup(html or "", "html.parser")

    if "content-security-policy" not in h:
        findings.append({
            "severity": "Medium",
            "type": "Missing Security Header",
            "url": url,
            "evidence": "Content-Security-Policy header was not observed.",
            "action": "Add a suitable Content-Security-Policy policy."
        })

    if "x-content-type-options" not in h:
        findings.append({
            "severity": "Low",
            "type": "Missing Security Header",
            "url": url,
            "evidence": "X-Content-Type-Options was not observed.",
            "action": "Set X-Content-Type-Options: nosniff."
        })

    if "x-frame-options" not in h and "content-security-policy" not in h:
        findings.append({
            "severity": "Low",
            "type": "Clickjacking Protection",
            "url": url,
            "evidence": "No X-Frame-Options or CSP frame-ancestors protection observed.",
            "action": "Use X-Frame-Options or CSP frame-ancestors where appropriate."
        })

    for form in soup.find_all("form"):
        method = (form.get("method") or "get").lower()
        if method == "get" and form.find("input", {"type": "password"}):
            findings.append({
                "severity": "Medium",
                "type": "Password Form Uses GET",
                "url": url,
                "evidence": "A password input was found inside a GET form.",
                "action": "Use POST for credential submission and HTTPS in production."
            })

    if "server" in h:
        findings.append({
            "severity": "Info",
            "type": "Server Banner",
            "url": url,
            "evidence": f"Server header exposed: {h['server']}",
            "action": "Consider minimizing unnecessary server version disclosure."
        })

    return findings

def security_headers(target):
    try:
        r = requests.get(target, timeout=5, allow_redirects=True)
        checks = []
        expected = [
            ("Content-Security-Policy", "Medium"),
            ("X-Content-Type-Options", "Low"),
            ("X-Frame-Options", "Low"),
            ("Referrer-Policy", "Low"),
        ]
        for name, severity in expected:
            present = name.lower() in {k.lower() for k in r.headers}
            checks.append({"header": name, "present": present, "severity": severity})
        return {"url": r.url, "status": r.status_code, "checks": checks}
    except requests.RequestException as e:
        return {"error": str(e)}
