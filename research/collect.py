"""Read-only source collector for hackathon planning. Never executes fetched code."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import sys
import requests
from html.parser import HTMLParser

class PageText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self.links, self.anchor = [], [], None
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"script", "style"}:
            self.hidden += 1
        if tag == "a" and attrs.get("href"):
            self.anchor = {"label": "", "href": attrs["href"]}
        if tag in {"p", "div", "br", "li", "h1", "h2", "h3", "tr", "pre"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.hidden = max(0, self.hidden - 1)
        if tag == "a" and self.anchor:
            self.links.append(self.anchor)
            self.anchor = None

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)
            if self.anchor:
                self.anchor["label"] += data

ROOT = Path(__file__).resolve().parent / "sources"
ROOT.mkdir(exist_ok=True)

def fetch(item):
    label, url = item
    key = label + "-" + hashlib.sha256(url.encode()).hexdigest()[:8]
    try:
        response = requests.get(url, timeout=35, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github+json"} if "api.github.com" in url else {"User-Agent": "Mozilla/5.0"})
        raw = response.text
        (ROOT / (key + ".raw")).write_text(raw)
        if "html" in response.headers.get("Content-Type", ""):
            parser = PageText()
            parser.feed(raw)
            body = "\n".join(line.strip() for line in "".join(parser.parts).splitlines() if line.strip())
            (ROOT / (key + ".links.json")).write_text(json.dumps(parser.links, indent=2))
        else:
            body = raw
        (ROOT / (key + ".txt")).write_text(f"URL: {url}\nHTTP: {response.status_code}\n\n{body}")
        return {"label": label, "url": url, "status": response.status_code, "file": key + ".txt", "chars": len(body), "preview": body[:350]}
    except Exception as error:
        return {"label": label, "url": url, "error": str(error)}

if __name__ == "__main__":
    items = json.load(sys.stdin)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for result in pool.map(fetch, items):
            print(json.dumps(result), flush=True)
