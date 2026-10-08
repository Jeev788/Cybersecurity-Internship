from flask import Flask, render_template, request, jsonify, send_file
from crawler import crawl_site
from scanner import analyze_url
from datetime import datetime
import json, os

app = Flask(__name__)
REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/demo")
def demo():
    return render_template("demo.html")

@app.route("/api/scan", methods=["POST"])
def scan():
    data = request.get_json(silent=True) or {}
    target = (data.get("target") or "").strip()
    authorized = bool(data.get("authorized"))

    if not authorized:
        return jsonify({"error": "Confirm that you own the target or have explicit permission to test it."}), 400

    try:
        max_pages = max(1, min(int(data.get("max_pages", 20)), 50))
        max_depth = max(0, min(int(data.get("max_depth", 2)), 4))
        delay = float(data.get("delay", 0.4))
        delay = max(0.2, min(delay, 2.0))
    except Exception:
        max_pages, max_depth, delay = 20, 2, 0.4

    try:
        result = crawl_site(target, max_pages=max_pages, max_depth=max_depth, delay=delay)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    findings = []
    for item in result["pages"]:
        findings.extend(analyze_url(item["url"], item.get("html", ""), item.get("headers", {})))

    # De-duplicate identical finding type + URL pairs.
    unique = {}
    for f in findings:
        unique[(f["type"], f["url"])] = f
    findings = list(unique.values())

    summary = {"high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        summary[f["severity"].lower()] += 1

    scan_result = {
        "target": target,
        "authorized": True,
        "started_at": result["started_at"],
        "finished_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pages_crawled": len(result["pages"]),
        "urls_discovered": len(result["urls"]),
        "forms_found": result["forms_found"],
        "max_pages": max_pages,
        "max_depth": max_depth,
        "endpoints": result["urls"],
        "pages": [
            {"url": x["url"], "depth": x["depth"], "status": x["status"], "content_type": x["content_type"]}
            for x in result["pages"]
        ],
        "crawl_errors": result["errors"],
        "findings": findings,
        "summary": summary,
    }

    with open(os.path.join(REPORT_DIR, "latest_report.json"), "w", encoding="utf-8") as f:
        json.dump(scan_result, f, indent=2)

    return jsonify(scan_result)

@app.route("/report")
def report():
    path = os.path.join(REPORT_DIR, "latest_report.json")
    if not os.path.exists(path):
        return "No report generated yet. Run a scan first.", 404
    return send_file(path, as_attachment=True, download_name="CyberRecon_Report.json")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
