from server.tools.web_search import WebSearchTool
from server.tools.ticker_manager import TickerManager
from server.tools.financial_data import FinancialDataTool
from server.tools.sec_filings import SECFilingsTool
from server.tools.news_scanner import NewsScannerTool
from server.tools.mail_sender import MailSender
from server.tools.gemini import GeminiAgent
from server.tools.pdf_reader import analyze_pdf_report

class UTIL:
    def __init__(self):
        self.web_search = WebSearchTool()
        self.ticker_manager = TickerManager()
        self.financial = FinancialDataTool()
        self.sectool = SECFilingsTool()
        self.news = NewsScannerTool()
        self.mail_sender = MailSender()
        self.llm = GeminiAgent()
        
    def get_web_search(self,query:str):
        result = self.web_search.run(query)
        return result
    
    def get_news(self,name:str):
        result = self.news.run(name)
        return result
        
    def get_financial_data(self,ticker:str, cik:str):
        fin = "No data"
        if ticker!="Unknown":
            fin = self.financial.run(ticker)
        sec = "Not found"
        if cik!="Unknown":
            sec = self.sectool.run(cik)
        return fin+"\n\n"+sec
        
    def send_mail(self, subject:str, message:str, receiver:str):
        return self.mail_sender.sendMail(subject=subject, message=message, dest=receiver)       
            
    def analyze_pdf(self, file_input, analysis_type="comprehensive"):
        """
        Analyze uploaded PDF report
        
        Args:
            file_input: Flask FileStorage object
            analysis_type: 'comprehensive', 'financial', or 'summary'
        """
        try:
            result = analyze_pdf_report(file_input, analysis_type)
            return result
        except Exception as e:
            return {
                'success': False,
                'error': f"PDF analysis failed: {str(e)}",
                'analysis': None
            }
