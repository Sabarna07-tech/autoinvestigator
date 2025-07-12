# server/tools/financial_data.py

import yfinance as yf

class FinancialDataTool:
    """
    Fetches key financial data for a given company using Yahoo Finance.
    """

    def run(self, ticker: str) -> str:
        """
        This function extracts the financial data from the web using Yahoo Finance
        
        Args:
            ticker : Ticker of the app.
        """
        print(f"[FinancialDataTool] Fetching financials for {ticker}")
        stock = yf.Ticker(ticker)
        try:
            info = stock.info
        except Exception:
            return f"Failed to fetch data for {ticker}."

        name = info.get("longName", "N/A")
        sector = info.get("sector", "N/A")
        market_cap = info.get("marketCap", "N/A")
        pe_ratio = info.get("trailingPE", "N/A")
        revenue = info.get("totalRevenue", "N/A")
        summary = info.get("longBusinessSummary", "")

        return f"""
Company: {name}
Sector: {sector}
Market Cap: {market_cap}
P/E Ratio: {pe_ratio}
Revenue: {revenue}

Summary:
{summary}
"""
