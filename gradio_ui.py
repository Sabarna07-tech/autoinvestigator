#!/usr/bin/env python3
"""
Interactive Gradio UI for AutoInvestigator
This provides a user-friendly web interface for all AutoInvestigator functionalities.
"""

import gradio as gr
import json
import asyncio
import logging
from typing import Tuple, Optional, Dict, Any
from datetime import datetime
import traceback

from client.agent import AutoInvestigatorAgent
from client.config import SERVER_URL, GEMINI_API_KEY

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutoInvestigatorUI:
    """
    Gradio UI wrapper for AutoInvestigator agent functionality
    """
    
    def __init__(self):
        """Initialize the UI with agent"""
        self.agent = None
        self.agent_error = None
        try:
            self.agent = AutoInvestigatorAgent()
            logger.info("AutoInvestigator agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            self.agent_error = str(e)
            self.agent = None

    def analyze_company(self, 
                       company_query: str, 
                       analysis_type: str, 
                       email_recipient: str = "") -> Tuple[str, str, str, str]:
        """
        Main analysis function that processes company queries
        
        Args:
            company_query: Company name or query to analyze
            analysis_type: Type of analysis to perform
            email_recipient: Optional email to send results to
            
        Returns:
            Tuple of (status, web_search_results, financial_data, news_analysis)
        """
        if not self.agent:
            error_msg = "❌ Error: Agent not initialized"
            if self.agent_error:
                error_msg += f"\n\nDetails: {self.agent_error}"
                if "GEMINI_API_KEY" in self.agent_error:
                    error_msg += "\n\n🔑 Please set your GEMINI_API_KEY in the environment variables or .env file."
                    error_msg += "\n📝 See .env.example for template."
            return (error_msg, "", "", "")
            
        if not company_query.strip():
            return ("⚠️ Please enter a company name or query", "", "", "")
        
        try:
            # Customize query based on analysis type
            if analysis_type == "Full Analysis":
                query = f"Provide a comprehensive risk analysis for {company_query} including company profile, financial data, recent news, and potential risks"
            elif analysis_type == "Financial Only":
                query = f"Provide detailed financial analysis and data for {company_query}"
            elif analysis_type == "News & Risk Only":
                query = f"Analyze recent news and potential risks for {company_query}"
            elif analysis_type == "Company Profile":
                query = f"Provide detailed company profile and background information for {company_query}"
            else:
                query = company_query
            
            # Update status
            status = f"🔍 Analyzing {company_query}...\n"
            
            # Run the agent analysis
            logger.info(f"Starting analysis for query: {query}")
            
            # Capture the agent output
            original_query = query
            main_prompt = self.agent._get_main_prompt()
            status += "✅ Retrieved analysis template\n"
            
            llm_request_str = self.agent._get_llm_request_json(main_prompt, original_query)
            status += "✅ Generated tool invocation plan\n"
            
            request_json = self.agent._parse_llm_output(llm_request_str)
            status += "✅ Parsed analysis plan\n"
            
            server_response = self.agent._execute_server_request(request_json)
            status += "✅ Executed analysis tools\n"
            
            final_answer = self.agent._get_final_response(original_query, server_response)
            status += "✅ Generated final analysis report\n"
            
            # Parse results for better display
            web_results, financial_results, news_results = self._parse_server_results(server_response)
            
            # Send email if recipient provided
            if email_recipient and email_recipient.strip():
                try:
                    self._send_email_report(company_query, final_answer, email_recipient)
                    status += f"📧 Report sent to {email_recipient}\n"
                except Exception as e:
                    status += f"⚠️ Email sending failed: {str(e)}\n"
            
            status += f"\n🎯 Analysis completed for {company_query}"
            
            return (
                status,
                web_results or "No web search results available",
                financial_results or "No financial data available", 
                news_results or final_answer
            )
            
        except Exception as e:
            error_msg = f"❌ Error during analysis: {str(e)}"
            logger.error(f"Analysis error: {e}")
            logger.error(traceback.format_exc())
            return (error_msg, "", "", "")

    def _parse_server_results(self, server_response: Dict[str, Any]) -> Tuple[str, str, str]:
        """Parse server response into categorized results"""
        web_results = ""
        financial_results = ""
        news_results = ""
        
        try:
            if 'results' in server_response:
                for result in server_response['results']:
                    method = result.get('method', '')
                    results_data = result.get('results', [])
                    
                    if 'websearch' in method:
                        web_results = "\n".join(str(r) for r in results_data) if results_data else ""
                    elif 'financial_descriptor' in method:
                        financial_results = "\n".join(str(r) for r in results_data) if results_data else ""
                    elif 'news' in method:
                        news_results = "\n".join(str(r) for r in results_data) if results_data else ""
                        
        except Exception as e:
            logger.error(f"Error parsing server results: {e}")
            
        return web_results, financial_results, news_results

    def _send_email_report(self, company: str, report: str, recipient: str):
        """Send analysis report via email"""
        try:
            # Use the mail sender tool
            import requests
            import uuid
            
            payload = {
                "id": f"email-request-{uuid.uuid4()}",
                "requests": [
                    {
                        "id": f"email-{uuid.uuid4()}",
                        "method": "tools/send_mail",
                        "params": {
                            "subject": f"AutoInvestigator Analysis Report - {company}",
                            "message": f"Analysis Report for {company}\n\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{report}",
                            "receiver": recipient
                        }
                    }
                ]
            }
            
            response = requests.post(SERVER_URL, json=payload)
            response.raise_for_status()
            logger.info(f"Email sent successfully to {recipient}")
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise

    def get_tool_list(self) -> str:
        """Get list of available tools"""
        try:
            import requests
            import uuid
            
            payload = {
                "id": f"tools-list-{uuid.uuid4()}",
                "requests": [
                    {
                        "id": f"tools-{uuid.uuid4()}",
                        "method": "tools/list"
                    }
                ]
            }
            
            response = requests.post(SERVER_URL, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if 'results' in result and result['results']:
                return result['results'][0].get('results', ['No tools available'])[0]
            return "Unable to fetch tools list"
            
        except Exception as e:
            return f"Error fetching tools: {str(e)}"

def create_interface():
    """Create and configure the Gradio interface"""
    
    ui_handler = AutoInvestigatorUI()
    
    # Custom CSS for better styling
    css = """
    .container {
        max-width: 1200px;
        margin: auto;
    }
    .gradio-button {
        background: linear-gradient(90deg, #4CAF50, #45a049);
        color: white;
    }
    .analysis-output {
        font-family: 'Courier New', monospace;
        font-size: 12px;
    }
    """
    
    with gr.Blocks(css=css, title="AutoInvestigator - Corporate Risk Intelligence") as interface:
        
        # Header
        gr.Markdown("""
        # 🕵️ AutoInvestigator - Corporate Risk Intelligence
        
        **Multi-Agent AI System for Corporate Risk Analysis**
        
        Automate corporate risk analysis through coordinated agents that perform web research, 
        financial analysis, sentiment tracking, and risk reporting.
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # Input Section
                gr.Markdown("## 📝 Analysis Configuration")
                
                company_input = gr.Textbox(
                    label="Company Name or Query",
                    placeholder="e.g., Apple Inc., Tesla, Microsoft Corp...",
                    lines=2
                )
                
                analysis_type = gr.Dropdown(
                    choices=[
                        "Full Analysis",
                        "Company Profile", 
                        "Financial Only",
                        "News & Risk Only",
                        "Custom Query"
                    ],
                    value="Full Analysis",
                    label="Analysis Type"
                )
                
                email_input = gr.Textbox(
                    label="Email (Optional)",
                    placeholder="your.email@domain.com",
                    lines=1
                )
                
                analyze_btn = gr.Button(
                    "🔍 Start Analysis", 
                    variant="primary",
                    size="lg"
                )
                
            with gr.Column(scale=1):
                # Tools Information
                gr.Markdown("## 🛠️ Available Tools")
                tools_info = gr.Textbox(
                    value=ui_handler.get_tool_list(),
                    label="System Tools",
                    lines=10,
                    interactive=False
                )
        
        # Results Section
        gr.Markdown("## 📊 Analysis Results")
        
        with gr.Row():
            status_output = gr.Textbox(
                label="🔄 Analysis Status",
                lines=8,
                interactive=False
            )
        
        with gr.Tabs():
            with gr.TabItem("🌐 Web Research"):
                web_output = gr.Textbox(
                    label="Company Information & Profile",
                    lines=10,
                    interactive=False,
                    elem_classes=["analysis-output"]
                )
                
            with gr.TabItem("💰 Financial Data"):
                financial_output = gr.Textbox(
                    label="Financial Analysis & Reports",
                    lines=10,
                    interactive=False,
                    elem_classes=["analysis-output"]
                )
                
            with gr.TabItem("📰 News & Risk Analysis"):
                news_output = gr.Textbox(
                    label="Recent News & Risk Assessment",
                    lines=10,
                    interactive=False,
                    elem_classes=["analysis-output"]
                )
        
        # Example Section
        gr.Markdown("""
        ## 💡 Example Queries
        
        - **Full Company Analysis**: "Tesla Inc" with "Full Analysis"
        - **Risk Assessment**: "WeWork recent controversies and financial risks"
        - **Financial Deep Dive**: "Microsoft" with "Financial Only"
        - **News Monitoring**: "Facebook Meta recent legal issues" with "News & Risk Only"
        """)
        
        # Footer
        gr.Markdown("""
        ---
        **AutoInvestigator** - Powered by Multi-Agent AI | 
        Server: `{}` | 
        Built with Gradio
        """.format(SERVER_URL))
        
        # Event handlers
        analyze_btn.click(
            fn=ui_handler.analyze_company,
            inputs=[company_input, analysis_type, email_input],
            outputs=[status_output, web_output, financial_output, news_output]
        )
        
        # Example inputs on click
        examples = gr.Examples(
            examples=[
                ["Apple Inc", "Full Analysis", ""],
                ["Tesla lawsuit risks", "News & Risk Only", ""],
                ["Microsoft Corporation", "Financial Only", ""],
                ["Amazon.com Inc", "Company Profile", ""]
            ],
            inputs=[company_input, analysis_type, email_input]
        )
    
    return interface

def main():
    """Main function to launch the Gradio interface"""
    
    print("🚀 Starting AutoInvestigator UI...")
    print(f"📡 Server URL: {SERVER_URL}")
    
    try:
        # Create the interface
        interface = create_interface()
        
        # Launch the interface
        interface.launch(
            server_name="0.0.0.0",  # Allow external access
            server_port=7860,       # Default Gradio port
            share=False,            # Set to True for public sharing
            debug=True,
            show_error=True
        )
        
    except Exception as e:
        logger.error(f"Failed to launch UI: {e}")
        logger.error(traceback.format_exc())
        print(f"❌ Error launching UI: {e}")

if __name__ == "__main__":
    main()