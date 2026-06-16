**# SOC // Phishing URL Heuristic Analyzer**



A defensive security tool designed to identify common indicators of phishing and malicious redirection in URLs. This tool uses a weighted scoring engine to categorize links into Safe, Suspicious, or Malicious threat levels.



**## Project Structure**

```text

phish-detector/

├── app.py                # Scoring Engine (Python Heuristics)

├── requirements.txt      # Dependencies

├── static/

│   ├── css/style.css     # SOC-inspired UI (Dark Cyber Theme)

│   └── js/main.js        # API Handler \& UI State Management

└── templates/

&nbsp;   └── index.html        # Scanning Dashboard



**Heuristic Detection Logic**



The analyzer evaluates URLs against five primary risk indicators:



* **IP-Hostname Verification**: Detection of raw IPv4 addresses used instead of registered domains (High Risk).



* **User-Info Obfuscation**: Identification of the @ symbol, frequently used to spoof legitimate domains (High Risk).



* **Subdomain Chain Analysis**: Detection of "domain stacking" (more than 3 subdomains), often used to mimic corporate structures.



* **Keyword Intelligence**: Scanning the URL path for high-value targets (e.g., login, verify, banking).



* **Length Analysis**: Identifying unusually long URLs (>75 characters) often used to conceal malicious parameters.



**Deployment \& Installation**



Prepare Environment:

├── python -m venv venv

├── source venv/bin/activate  # Windows: venv\\Scripts\\activate

├── pip install -r requirements.txt



Run Scanner:

├── python app.py

&nbsp;	├── *The system defaults to Port 5002 for isolated SOC operations.*



**Creating the SOC Executable**



To package the analyzer into a standalone diagnostic tool:



**Windows Command**: pyinstaller --onefile --noconsole --add-data "templates;templates" --add-data "static;static" app.py

