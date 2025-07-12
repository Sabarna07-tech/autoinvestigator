# server/tools/sec_filings.py

import requests

class SECFilingsTool:
    """
    Fetches the latest 10-K or 10-Q filings from the SEC EDGAR system for a company.
    """

    def run(self, cik: str) -> str:
        print(f"[SECFilingsTool] Fetching SEC filings for CIK: {cik}")
        url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
        headers = {"User-Agent": "AutoInvestigator/1.0 contact@example.com"}

        try:
            res = requests.get(url, headers=headers)
            data = res.json()
        except Exception:
            return "Unable to retrieve filings."

        items = data.get("filings", {}).get("recent", {})
        docs = [
            f"{form} | {date} | https://www.sec.gov/Archives/{link}"
            for form, date, link in zip(items.get("form", []), items.get("filingDate", []), items.get("primaryDocument", []))
            if form in ["10-K", "10-Q"]
        ]

        return "\n".join(docs[:3]) if docs else "No recent filings found."
