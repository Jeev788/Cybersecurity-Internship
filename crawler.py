import requests
import socket
import ipaddress
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
from collections import deque
from datetime import datetime

HEADERS = {"User-Agent": "CyberRecon-Student-Lab/2.0"}
TIMEOUT = 7

def validate_public_target(start_url):
    parsed = urlparse(start_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("Enter a valid http:// or https:// website.")

    host = parsed.hostname
    if not host:
        raise ValueError("Invalid hostname.")

    # Prevent the demo crawler from being used against local/private network targets.
    try:
        addresses = socket.getaddrinfo(host, None)
        for item in addresses:
            ip = ipaddress.ip_address(item[4][0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
                raise ValueError("Private, loopback or reserved network targets are blocked. Use a public website you own or are authorized to test.")
    except socket.gaierror:
        raise ValueError("Could not resolve the target hostname.")

    return True

def same_origin(base, candidate):
    b = urlparse(base)
    c = urlparse(candidate)
    return c.netloc.lower() == b.netloc.lower() and c.scheme in ("http", "https")

def crawl_site(start_url, max_pages=20, max_depth=2, delay=0.4):
    validate_public_target(start_url)

    queue = deque([(start_url, 0)])
    discovered = set()
    visited = set()
    pages = []
    forms_found = 0
    errors = []
    started = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    while queue and len(pages) < max_pages:
        url, depth = queue.popleft()
        url, _ = urldefrag(url)

        if url in visited or depth > max_depth:
            continue

        visited.add(url)

        try:
            r = requests.get(
                url,
                headers=HEADERS,
                timeout=TIMEOUT,
                allow_redirects=True
            )

            final_url, _ = urldefrag(r.url)
            discovered.add(final_url)

            content_type = r.headers.get("Content-Type", "")
            html = r.text if "text/html" in content_type.lower() else ""

            soup = BeautifulSoup(html, "html.parser")
            page_forms = len(soup.find_all("form"))
            forms_found += page_forms

            pages.append({
                "url": final_url,
                "depth": depth,
                "status": r.status_code,
                "content_type": content_type,
                "html": html,
                "headers": dict(r.headers),
            })

            if depth < max_depth and html:
                for a in soup.find_all("a", href=True):
                    nxt = urljoin(final_url, a["href"].strip())
                    nxt, _ = urldefrag(nxt)

                    if same_origin(start_url, nxt) and nxt not in discovered:
                        discovered.add(nxt)
                        queue.append((nxt, depth + 1))

        except requests.RequestException as exc:
            errors.append({"url": url, "error": str(exc)})

        time.sleep(max(0.0, min(delay, 2.0)))

    return {
        "started_at": started,
        "pages": pages,
        "urls": sorted(discovered),
        "forms_found": forms_found,
        "errors": errors,
    }
