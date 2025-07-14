"""
PDF Reader Tool for AutoInvestigator
Analyzes uploaded PDF reports and extracts key financial information
"""

import PyPDF2
import pdfplumber
import fitz  # PyMuPDF
import io
import re
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import tempfile
import os
import logging
from werkzeug.datastructures import FileStorage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PDFAnalysisResult:
    """Structure for PDF analysis results"""
    filename: str
    total_pages: int
    extracted_text: str
    financial_data: Dict[str, Any]
    key_metrics: Dict[str, Any]
    tables: List[Dict[str, Any]]
    sections: Dict[str, str]
    summary: str
    analysis_type: str

class PDFReader:
    """
    Advanced PDF reader and analyzer for financial reports
    """
    
    def __init__(self):
        self.financial_keywords = [
            'revenue', 'profit', 'loss', 'ebitda', 'operating income',
            'net income', 'gross margin', 'cash flow', 'assets', 'liabilities',
            'equity', 'debt', 'earnings per share', 'eps', 'return on equity',
            'roe', 'return on assets', 'roa', 'current ratio', 'quick ratio',
            'debt to equity', 'price to earnings', 'p/e ratio', 'market cap',
            'dividend', 'yield', 'book value', 'working capital'
        ]
        
        self.section_patterns = {
            'executive_summary': r'executive\s+summary|management\s+summary',
            'financial_highlights': r'financial\s+highlights|key\s+metrics',
            'revenue_analysis': r'revenue\s+analysis|sales\s+analysis',
            'profitability': r'profitability|profit\s+analysis',
            'balance_sheet': r'balance\s+sheet|statement\s+of\s+financial\s+position',
            'cash_flow': r'cash\s+flow|statement\s+of\s+cash\s+flows',
            'income_statement': r'income\s+statement|profit\s+and\s+loss',
            'risks': r'risk\s+factors|risks\s+and\s+uncertainties',
            'outlook': r'outlook|forward\s+looking|guidance',
            'management_discussion': r'management\s+discussion|md&a'
        }

    def analyze_pdf(self, file_input: FileStorage, analysis_type: str = "comprehensive") -> PDFAnalysisResult:
        """
        Main method to analyze a PDF file
        
        Args:
            file_input: Flask FileStorage object or file path
            analysis_type: Type of analysis ('comprehensive', 'financial', 'summary')
        """
        try:
            # Save uploaded file temporarily
            temp_path = self._save_temp_file(file_input)
            
            # Extract text and metadata
            text_content = self._extract_text_multiple_methods(temp_path)
            tables = self._extract_tables(temp_path)
            
            # Analyze content
            financial_data = self._extract_financial_data(text_content)
            key_metrics = self._extract_key_metrics(text_content, tables)
            sections = self._identify_sections(text_content)
            
            # Generate summary based on analysis type
            summary = self._generate_summary(text_content, financial_data, analysis_type)
            
            # Get total pages
            total_pages = self._get_page_count(temp_path)
            
            # Clean up temp file
            self._cleanup_temp_file(temp_path)
            
            return PDFAnalysisResult(
                filename=file_input.filename,
                total_pages=total_pages,
                extracted_text=text_content[:5000],  # Limit for response size
                financial_data=financial_data,
                key_metrics=key_metrics,
                tables=tables,
                sections=sections,
                summary=summary,
                analysis_type=analysis_type
            )
            
        except Exception as e:
            logger.error(f"Error analyzing PDF: {str(e)}")
            raise Exception(f"PDF analysis failed: {str(e)}")

    def _save_temp_file(self, file_input: FileStorage) -> str:
        """Save uploaded file to temporary location"""
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"pdf_analysis_{file_input.filename}")
        file_input.save(temp_path)
        return temp_path

    def _cleanup_temp_file(self, temp_path: str):
        """Clean up temporary file"""
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception as e:
            logger.warning(f"Could not clean up temp file: {e}")

    def _extract_text_multiple_methods(self, file_path: str) -> str:
        """Extract text using multiple methods for better accuracy"""
        text_content = ""
        
        # Method 1: pdfplumber (best for structured text)
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n"
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed: {e}")
        
        # Method 2: PyMuPDF (fallback)
        if not text_content.strip():
            try:
                doc = fitz.open(file_path)
                for page_num in range(doc.page_count):
                    page = doc[page_num]
                    text_content += page.get_text() + "\n"
                doc.close()
            except Exception as e:
                logger.warning(f"PyMuPDF extraction failed: {e}")
        
        # Method 3: PyPDF2 (last resort)
        if not text_content.strip():
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text_content += page.extract_text() + "\n"
            except Exception as e:
                logger.warning(f"PyPDF2 extraction failed: {e}")
        
        return text_content

    def _extract_tables(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract tables from PDF"""
        tables = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_tables = page.extract_tables()
                    for table_num, table in enumerate(page_tables):
                        if table and len(table) > 1:  # Skip empty or single-row tables
                            table_dict = {
                                'page': page_num + 1,
                                'table_number': table_num + 1,
                                'headers': table[0] if table else [],
                                'data': table[1:] if len(table) > 1 else [],
                                'row_count': len(table) - 1,
                                'column_count': len(table[0]) if table else 0
                            }
                            tables.append(table_dict)
        except Exception as e:
            logger.warning(f"Table extraction failed: {e}")
        
        return tables

    def _extract_financial_data(self, text: str) -> Dict[str, Any]:
        """Extract financial data using pattern matching"""
        financial_data = {}
        
        # Common financial patterns
        patterns = {
            'revenue': r'(?:revenue|sales|total\s+revenue)[\s:]+\$?([0-9,]+(?:\.[0-9]+)?)\s*(?:million|billion|m|b)?',
            'net_income': r'(?:net\s+income|net\s+profit)[\s:]+\$?([0-9,]+(?:\.[0-9]+)?)\s*(?:million|billion|m|b)?',
            'ebitda': r'ebitda[\s:]+\$?([0-9,]+(?:\.[0-9]+)?)\s*(?:million|billion|m|b)?',
            'eps': r'(?:earnings\s+per\s+share|eps)[\s:]+\$?([0-9]+(?:\.[0-9]+)?)',
            'total_assets': r'(?:total\s+assets)[\s:]+\$?([0-9,]+(?:\.[0-9]+)?)\s*(?:million|billion|m|b)?',
            'total_debt': r'(?:total\s+debt|long.term\s+debt)[\s:]+\$?([0-9,]+(?:\.[0-9]+)?)\s*(?:million|billion|m|b)?',
            'cash': r'(?:cash|cash\s+and\s+equivalents)[\s:]+\$?([0-9,]+(?:\.[0-9]+)?)\s*(?:million|billion|m|b)?'
        }
        
        for key, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    # Take the first match and clean it
                    value = matches[0].replace(',', '')
                    financial_data[key] = float(value)
                except (ValueError, IndexError):
                    continue
        
        return financial_data

    def _extract_key_metrics(self, text: str, tables: List[Dict]) -> Dict[str, Any]:
        """Extract key financial metrics and ratios"""
        metrics = {}
        
        # Extract ratios and percentages
        ratio_patterns = {
            'gross_margin': r'gross\s+margin[\s:]+([0-9]+(?:\.[0-9]+)?)%',
            'operating_margin': r'operating\s+margin[\s:]+([0-9]+(?:\.[0-9]+)?)%',
            'net_margin': r'net\s+margin[\s:]+([0-9]+(?:\.[0-9]+)?)%',
            'roe': r'(?:return\s+on\s+equity|roe)[\s:]+([0-9]+(?:\.[0-9]+)?)%',
            'roa': r'(?:return\s+on\s+assets|roa)[\s:]+([0-9]+(?:\.[0-9]+)?)%',
            'current_ratio': r'current\s+ratio[\s:]+([0-9]+(?:\.[0-9]+)?)',
            'debt_to_equity': r'debt.to.equity[\s:]+([0-9]+(?:\.[0-9]+)?)'
        }
        
        for key, pattern in ratio_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    metrics[key] = float(matches[0])
                except (ValueError, IndexError):
                    continue
        
        # Extract from tables if available
        for table in tables:
            if table.get('headers'):
                headers = [str(h).lower() if h else '' for h in table['headers']]
                for row in table.get('data', []):
                    if row and len(row) >= 2:
                        key = str(row[0]).lower().strip() if row[0] else ''
                        value_str = str(row[1]).strip() if len(row) > 1 and row[1] else ''
                        
                        # Look for financial keywords in the key
                        for keyword in self.financial_keywords:
                            if keyword in key:
                                try:
                                    # Extract numeric value
                                    numeric_value = re.search(r'([0-9,]+(?:\.[0-9]+)?)', value_str)
                                    if numeric_value:
                                        metrics[keyword.replace(' ', '_')] = float(numeric_value.group(1).replace(',', ''))
                                except (ValueError, AttributeError):
                                    continue
        
        return metrics

    def _identify_sections(self, text: str) -> Dict[str, str]:
        """Identify and extract different sections of the report"""
        sections = {}
        
        for section_name, pattern in self.section_patterns.items():
            matches = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                start_pos = matches.start()
                # Extract ~1000 characters from the start of the section
                section_text = text[start_pos:start_pos + 1000]
                sections[section_name] = section_text.strip()
        
        return sections

    def _generate_summary(self, text: str, financial_data: Dict, analysis_type: str) -> str:
        """Generate summary based on analysis type"""
        if analysis_type == "financial":
            return self._generate_financial_summary(financial_data)
        elif analysis_type == "summary":
            return self._generate_executive_summary(text)
        else:  # comprehensive
            return self._generate_comprehensive_summary(text, financial_data)

    def _generate_financial_summary(self, financial_data: Dict) -> str:
        """Generate focused financial summary"""
        summary_parts = ["📊 Financial Analysis Summary:"]
        
        if 'revenue' in financial_data:
            summary_parts.append(f"• Revenue: ${financial_data['revenue']:,.0f}")
        
        if 'net_income' in financial_data:
            summary_parts.append(f"• Net Income: ${financial_data['net_income']:,.0f}")
        
        if 'ebitda' in financial_data:
            summary_parts.append(f"• EBITDA: ${financial_data['ebitda']:,.0f}")
        
        if len(summary_parts) == 1:
            summary_parts.append("• No specific financial metrics were automatically extracted from this report.")
            summary_parts.append("• Manual review may be required for detailed financial analysis.")
        
        return "\n".join(summary_parts)

    def _generate_executive_summary(self, text: str) -> str:
        """Generate executive summary"""
        # Look for executive summary section
        exec_pattern = r'(?:executive\s+summary|management\s+summary)(.*?)(?=\n\s*\n|\n[A-Z])'
        match = re.search(exec_pattern, text, re.IGNORECASE | re.DOTALL)
        
        if match:
            return f"📋 Executive Summary:\n{match.group(1)[:800]}..."
        else:
            # Extract first few paragraphs as summary
            paragraphs = text.split('\n\n')[:3]
            return f"📋 Document Summary:\n{' '.join(paragraphs)[:800]}..."

    def _generate_comprehensive_summary(self, text: str, financial_data: Dict) -> str:
        """Generate comprehensive analysis summary"""
        summary_parts = ["🔍 Comprehensive Analysis:"]
        
        # Document overview
        word_count = len(text.split())
        summary_parts.append(f"• Document contains ~{word_count:,} words")
        
        # Financial highlights
        if financial_data:
            summary_parts.append("• Key Financial Data Extracted:")
            for key, value in list(financial_data.items())[:5]:
                summary_parts.append(f"  - {key.replace('_', ' ').title()}: ${value:,.0f}")
        
        # Key topics (basic keyword analysis)
        keywords = ['growth', 'profit', 'loss', 'risk', 'strategy', 'market', 'competition']
        found_keywords = [kw for kw in keywords if kw in text.lower()]
        if found_keywords:
            summary_parts.append(f"• Key Topics Identified: {', '.join(found_keywords)}")
        
        return "\n".join(summary_parts)

    def _get_page_count(self, file_path: str) -> int:
        """Get total page count"""
        try:
            with pdfplumber.open(file_path) as pdf:
                return len(pdf.pages)
        except:
            try:
                doc = fitz.open(file_path)
                count = doc.page_count
                doc.close()
                return count
            except:
                return 0

    def get_supported_formats(self) -> List[str]:
        """Return list of supported file formats"""
        return ['.pdf']

    def validate_file(self, file_input: FileStorage) -> Tuple[bool, str]:
        """Validate uploaded file"""
        if not file_input:
            return False, "No file provided"
        
        if not file_input.filename:
            return False, "No filename provided"
        
        if not file_input.filename.lower().endswith('.pdf'):
            return False, "Only PDF files are supported"
        
        # Check file size (limit to 50MB)
        file_input.seek(0, 2)  # Seek to end
        file_size = file_input.tell()
        file_input.seek(0)  # Reset to beginning
        
        if file_size > 50 * 1024 * 1024:  # 50MB
            return False, "File size too large (max 50MB)"
        
        return True, "Valid file"

# Utility function for integration with the main server
def analyze_pdf_report(file_input: FileStorage, analysis_type: str = "comprehensive") -> Dict[str, Any]:
    """
    Main function to be called from the server interface
    """
    reader = PDFReader()
    
    # Validate file
    is_valid, message = reader.validate_file(file_input)
    if not is_valid:
        return {
            'success': False,
            'error': message,
            'analysis': None
        }
    
    try:
        result = reader.analyze_pdf(file_input, analysis_type)
        return {
            'success': True,
            'error': None,
            'analysis': {
                'filename': result.filename,
                'pages': result.total_pages,
                'financial_data': result.financial_data,
                'key_metrics': result.key_metrics,
                'tables_found': len(result.tables),
                'sections_identified': list(result.sections.keys()),
                'summary': result.summary,
                'analysis_type': result.analysis_type,
                'preview_text': result.extracted_text[:500] + "..." if len(result.extracted_text) > 500 else result.extracted_text
            }
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'analysis': None
        }

if __name__ == "__main__":
    # Test the PDF reader
    print("PDF Reader Tool - Ready for integration")
    print("Supported formats:", PDFReader().get_supported_formats())