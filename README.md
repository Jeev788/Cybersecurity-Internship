# CyberRecon V2

CyberRecon V2 is a student web reconnaissance and defensive security analysis platform inspired by the general endpoint-discovery workflow of tools such as Katana.

## V2 features

- Accepts `http://` and `https://` targets
- Requires an authorization confirmation
- Same-origin crawling
- Configurable maximum pages
- Configurable crawl depth
- Small request delay/rate limiting
- Blocks localhost/private/reserved network targets
- URL and endpoint discovery
- HTML form discovery
- Status/content-type collection
- Basic defensive security-header checks
- Severity classification
- Professional dashboard
- Crawl result view
- JSON report export
- Included local college-fee training target

## Run

CMD 1:
```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python demo_target.py
```

CMD 2:
```bat
venv\Scripts\activate
python app.py
```

Open:
`http://127.0.0.1:8000`

## Test public crawling

Use a website you own or have explicit authorization to test.

For a simple public demonstration, `https://example.com` can be used as a basic connectivity/crawling example. Tick the authorization checkbox and click Start Crawl & Scan.

Do not use the project against websites without permission.

## How to explain it

"CyberRecon has two stages. First, reconnaissance discovers the application's same-origin attack surface by crawling links and collecting pages, forms and response metadata. Second, the defensive analysis engine evaluates basic security controls such as response security headers and form configuration. The results are classified by severity and presented through the dashboard."

## Difference from Katana

"Katana is a dedicated high-performance web crawler. CyberRecon is an educational web application that implements a smaller crawler independently and combines reconnaissance with defensive security analysis, visualization and reporting."

## Project title

CyberRecon: Web Application Reconnaissance and Defensive Security Analysis Platform
