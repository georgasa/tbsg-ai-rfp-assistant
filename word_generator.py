#!/usr/bin/env python3
"""
Word Document Generator for Temenos RAG AI System
Converts JSON pillar analysis files into well-formatted Word documents for RFP responses.
"""

import json
import os
import glob
from datetime import datetime
from typing import Dict, List, Optional

try:
    from docx import Document
    from docx.shared import Inches, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.style import WD_STYLE_TYPE
    DOCX_AVAILABLE = True
except ImportError:
    Document = None
    Inches = None
    Pt = None
    WD_ALIGN_PARAGRAPH = None
    WD_STYLE_TYPE = None
    DOCX_AVAILABLE = False

class WordDocumentGenerator:
    """Generate Word documents from pillar analysis JSON files"""
    
    def __init__(self):
        self.docx_available = DOCX_AVAILABLE
        
    def create_document(self, data: Dict) -> Optional[str]:
        """Create a Word document from pillar analysis data"""
        if not self.docx_available:
            return None
        
        try:
            # Extract data with error handling
            metadata = data.get("metadata", {})
            analysis = data.get("analysis", {})
            
            if not metadata:
                return None
            
            # Create document
            doc = Document()
            
            # Set up styles
            self._setup_styles(doc)
            
            # Add content
            if analysis:
                # Add executive summary first
                self._add_executive_summary(doc, analysis)
                
                # Add key findings
                self._add_key_findings(doc, analysis)
                
                # Add detailed technical analysis
                self._add_detailed_analysis(doc, analysis)
                
                # Add author information at the end
                self._add_author_info(doc, metadata)
            else:
                doc.add_paragraph("No analysis data available.")
            
            # Save document
            word_docs_dir = "word_documents"
            if not os.path.exists(word_docs_dir):
                os.makedirs(word_docs_dir)
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pillar = metadata.get('pillar', 'Unknown')
            product = metadata.get('product', 'Unknown')
            pillar_name = pillar.lower().replace(" ", "_")
            product_name = product.lower().replace(" ", "_").replace("temenos_", "")
            filename = f"{pillar_name}_analysis_{product_name}_{timestamp}.docx"
            filepath = os.path.join(word_docs_dir, filename)
            
            doc.save(filepath)
            return filepath
            
        except Exception as e:
            print(f"Error creating Word document: {e}")
            return None
    
    def _setup_styles(self, doc: Document):
        """Set up document styles"""
        try:
            # Title style
            title_style = doc.styles.add_style('CustomTitle', WD_STYLE_TYPE.PARAGRAPH)
            title_style.font.name = 'Calibri'
            title_style.font.size = Pt(16)
            title_style.font.bold = True
            
            # Heading style
            heading_style = doc.styles.add_style('CustomHeading', WD_STYLE_TYPE.PARAGRAPH)
            heading_style.font.name = 'Calibri'
            heading_style.font.size = Pt(14)
            heading_style.font.bold = True
            
        except Exception:
            pass  # Use default styles if custom styles fail
    
    def _add_executive_summary(self, doc: Document, analysis: Dict):
        """Add executive summary section"""
        doc.add_heading('Executive Summary', level=1)
        
        pillar = analysis.get('pillar', 'Unknown')
        product = analysis.get('product', 'Unknown')
        region = analysis.get('region', 'Unknown')
        
        summary_text = f"""
This document provides a comprehensive analysis of {pillar} capabilities for {product} in the {region} region. 
The analysis focuses on key technical capabilities and business value propositions suitable for RFP response preparation.

Key findings include {len(analysis.get('key_points', []))} identified technical capabilities and business benefits that demonstrate 
{product}'s competitive advantages in the {pillar} domain. This analysis supports strategic decision-making 
and provides detailed insights for client presentations and proposal development.
        """.strip()
        
        doc.add_paragraph(summary_text)
        doc.add_paragraph()  # Add spacing

    def _add_detailed_analysis(self, doc: Document, analysis: Dict):
        """Add detailed questions and answers section with integrated business benefits"""
        doc.add_heading('Technical Analysis', level=1)
        
        # Check if conversation_flow exists and is not empty
        if 'conversation_flow' not in analysis or not analysis['conversation_flow']:
            doc.add_paragraph("No conversation flow data available.")
            return
        
        # Add questions in compact format - limit to 3 pages
        questions_per_page = 3  # Approximately 3 questions per page for 3-page limit
        max_questions = min(len(analysis['conversation_flow']), questions_per_page * 3)
        
        for i, q_data in enumerate(analysis['conversation_flow'][:max_questions], 1):
            question = q_data.get('question', 'No question available')
            answer = q_data.get('answer', 'No answer available')
            
            # Shorten question for compactness
            if len(question) > 80:
                question = question[:77] + "..."
            
            # Add question as bold
            q_para = doc.add_paragraph()
            q_run = q_para.add_run(f"Q{i}: {question}")
            q_run.bold = True
            
            # Add answer with integrated business benefit - keep concise
            if len(answer) > 200:
                answer = answer[:197] + "..."
            answer_para = doc.add_paragraph(answer)
            answer_para.style = 'Normal'
            
            # Add minimal spacing between questions
            if i < max_questions:
                doc.add_paragraph()

    def _add_key_findings(self, doc: Document, analysis: Dict):
        """Add key findings section"""
        doc.add_heading('Key Findings', level=1)
        
        key_points = analysis.get('key_points', [])
        if key_points:
            # Limit to top 5 key points for compactness
            top_points = key_points[:5]
            for i, point in enumerate(top_points, 1):
                if len(point) > 150:
                    point = point[:147] + "..."
                doc.add_paragraph(f"{i}. {point}")
        else:
            doc.add_paragraph("No specific key findings identified in this analysis.")
        
        doc.add_paragraph()  # Add spacing
    
    def _add_author_info(self, doc: Document, metadata: Dict):
        """Add author information at the end"""
        # Add author section without page break to keep within 3 pages
        doc.add_heading('Document Information', level=1)
        
        # Get API key from shared_config
        try:
            from shared_config import API_CONFIG
            api_key = API_CONFIG.get('jwt_token', 'N/A')
            # Show only first 10 and last 10 characters for security
            if len(api_key) > 20:
                masked_key = f"{api_key[:10]}...{api_key[-10:]}"
            else:
                masked_key = "N/A"
        except:
            masked_key = "N/A"
        
        # Add author info
        doc.add_paragraph(f"Generated by: Temenos RAG AI System")
        doc.add_paragraph(f"API Key: {masked_key}")
        doc.add_paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        doc.add_paragraph(f"Product: {metadata.get('product', 'Unknown')}")
        doc.add_paragraph(f"Pillar: {metadata.get('pillar', 'Unknown')}")
        doc.add_paragraph(f"Region: {metadata.get('region', 'Unknown')}")
    
    def convert_json_to_word(self, json_filepath: str) -> Optional[str]:
        """Convert JSON analysis file to Word document"""
        try:
            with open(json_filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return self.create_document(data)
            
        except Exception as e:
            print(f"Error converting JSON to Word: {e}")
            return None

    def create_combined_document(self, combined_analysis: Dict) -> Optional[str]:
        """Create a combined Word document from multiple products analysis"""
        if not self.docx_available:
            return None
        
        try:
            # Create document
            doc = Document()
            
            # Set up styles
            self._setup_styles(doc)
            
            # Add title
            products = ", ".join(combined_analysis.get('products', []))
            pillar = combined_analysis.get('pillar', 'Unknown')
            doc.add_heading(f'Combined RFP Analysis Report - {pillar}', 0)
            doc.add_paragraph(f'Products: {products}')
            doc.add_paragraph()
            
            # Add executive summary for combined analysis
            self._add_combined_executive_summary(doc, combined_analysis)
            
            # Add combined key findings
            self._add_combined_key_findings(doc, combined_analysis)
            
            # Add product-specific sections
            self._add_product_sections(doc, combined_analysis)
            
            # Add author info
            self._add_author_info(doc, {
                'pillar': pillar,
                'product': products,
                'region': combined_analysis.get('region', 'Unknown'),
                'timestamp': combined_analysis.get('timestamp', '')
            })
            
            # Save document
            word_docs_dir = "word_documents"
            if not os.path.exists(word_docs_dir):
                os.makedirs(word_docs_dir)
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pillar_clean = pillar.lower().replace(" ", "_")
            products_clean = "_".join([p.lower().replace(" ", "_").replace("temenos_", "") for p in combined_analysis.get('products', [])])
            
            filename = f"combined_{pillar_clean}_analysis_{products_clean}_{timestamp}.docx"
            filepath = os.path.join(word_docs_dir, filename)
            
            doc.save(filepath)
            return filepath
            
        except Exception as e:
            print(f"Error creating combined Word document: {e}")
            return None

    def _add_combined_executive_summary(self, doc: Document, combined_analysis: Dict):
        """Add executive summary for combined analysis"""
        doc.add_heading('Executive Summary', level=1)
        pillar = combined_analysis.get('pillar', 'Unknown')
        products = ", ".join(combined_analysis.get('products', []))
        region = combined_analysis.get('region', 'Unknown')
        
        summary_text = f"""
This document provides a comprehensive combined analysis of {pillar} capabilities across multiple Temenos products: {products} in the {region} region.
The analysis consolidates insights from each product to provide a unified view of {pillar} capabilities suitable for RFP response preparation.

The combined analysis identifies {len(combined_analysis.get('combined_key_points', []))} key technical capabilities and business benefits across all selected products,
demonstrating the comprehensive {pillar} coverage and competitive advantages of the Temenos ecosystem.
        """.strip()
        doc.add_paragraph(summary_text)
        doc.add_paragraph()

    def _add_combined_key_findings(self, doc: Document, combined_analysis: Dict):
        """Add combined key findings section"""
        doc.add_heading('Key Findings', level=1)
        key_points = combined_analysis.get('combined_key_points', [])
        if key_points:
            # Limit to top 8 key points for combined analysis
            top_points = key_points[:8]
            for i, point in enumerate(top_points, 1):
                if len(point) > 200:
                    point = point[:197] + "..."
                doc.add_paragraph(f"{i}. {point}")
        else:
            doc.add_paragraph("No specific key findings identified in this combined analysis.")
        doc.add_paragraph()

    def _add_product_sections(self, doc: Document, combined_analysis: Dict):
        """Add product-specific analysis sections"""
        doc.add_heading('Product-Specific Analysis', level=1)
        
        product_analyses = combined_analysis.get('product_analyses', [])
        for product_data in product_analyses:
            product_name = product_data.get('product', 'Unknown')
            analysis = product_data.get('analysis', {})
            
            doc.add_heading(f'{product_name} - {analysis.get("pillar", "Unknown")} Analysis', level=2)
            
            # Add key points for this product
            key_points = analysis.get('key_points', [])
            if key_points:
                doc.add_heading('Key Capabilities', level=3)
                for i, point in enumerate(key_points[:5], 1):  # Limit to top 5 per product
                    if len(point) > 150:
                        point = point[:147] + "..."
                    doc.add_paragraph(f"{i}. {point}")
            
            # Add conversation flow if available
            if 'conversation_flow' in analysis and analysis['conversation_flow']:
                doc.add_heading('Technical Details', level=3)
                for i, q_data in enumerate(analysis['conversation_flow'][:3], 1):  # Limit to 3 questions per product
                    question = q_data.get('question', 'No question available')
                    answer = q_data.get('answer', 'No answer available')
                    
                    if len(question) > 80:
                        question = question[:77] + "..."
                    if len(answer) > 200:
                        answer = answer[:197] + "..."
                    
                    q_para = doc.add_paragraph()
                    q_run = q_para.add_run(f"Q{i}: {question}")
                    q_run.bold = True
                    
                    doc.add_paragraph(answer)
            
            doc.add_paragraph()  # Add spacing between products
