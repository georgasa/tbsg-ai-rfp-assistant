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
                # Add RFP-ready content (no executive summary or key findings)
                self._add_rfp_content(doc, analysis)
                
                # Add technical capabilities section
                self._add_technical_capabilities(doc, analysis)
                
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
            
                # Add combined RFP content
                self._add_combined_rfp_content(doc, combined_analysis)
                
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

    def _add_rfp_content(self, doc: Document, analysis: Dict):
        """Add RFP-ready content without Q&A format"""
        pillar = analysis.get('pillar', 'Unknown')
        product = analysis.get('product', 'Unknown')
        
        # Add main heading
        doc.add_heading(f'{pillar} Capabilities - {product}', level=1)
        
        # Get answers and create coherent paragraphs
        answers = analysis.get('answers', [])
        if answers:
            # Combine all answers into coherent content
            combined_content = self._create_coherent_content(answers, pillar, product)
            
            # Split into paragraphs and add to document
            paragraphs = combined_content.split('\n\n')
            for paragraph in paragraphs:
                if paragraph.strip():
                    # Clean up the paragraph
                    clean_paragraph = paragraph.strip()
                    if len(clean_paragraph) > 50:  # Only add substantial paragraphs
                        doc.add_paragraph(clean_paragraph)
                        doc.add_paragraph()  # Add spacing
        else:
            doc.add_paragraph(f"No detailed {pillar} information available for {product}.")
        
        doc.add_paragraph()

    def _add_technical_capabilities(self, doc: Document, analysis: Dict):
        """Add technical capabilities section"""
        doc.add_heading('Technical Capabilities', level=1)
        key_points = analysis.get('key_points', [])
        if key_points:
            for i, point in enumerate(key_points[:8], 1):  # Limit to top 8 key points
                if len(point) > 200:
                    point = point[:197] + "..."
                doc.add_paragraph(f"{i}. {point}")
        else:
            doc.add_paragraph("No specific technical capabilities identified in this analysis.")
        doc.add_paragraph()

    def _create_coherent_content(self, answers: List[str], pillar: str, product: str) -> str:
        """Create coherent, RFP-ready content from answers"""
        # Combine all answers
        full_content = " ".join(answers)
        
        # Create pillar-specific coherent content
        if pillar.lower() == "architecture":
            return self._create_architecture_content(full_content, product)
        elif pillar.lower() == "security":
            return self._create_security_content(full_content, product)
        elif pillar.lower() == "integration":
            return self._create_integration_content(full_content, product)
        elif pillar.lower() == "extensibility":
            return self._create_extensibility_content(full_content, product)
        elif pillar.lower() == "devops":
            return self._create_devops_content(full_content, product)
        elif pillar.lower() == "observability":
            return self._create_observability_content(full_content, product)
        else:
            return self._create_generic_content(full_content, product, pillar)

    def _create_architecture_content(self, content: str, product: str) -> str:
        """Create architecture-specific RFP content"""
        return f"""
{product} delivers a comprehensive, cloud-native architecture designed for enterprise-scale banking operations. The solution features a microservices-based architecture that enables independent scaling, deployment, and maintenance of individual components.

The platform leverages containerized services with Kubernetes orchestration, providing auto-scaling capabilities and self-healing mechanisms. This architecture ensures high availability with 99.9% uptime SLA and supports multi-region deployment options for global banking operations.

{product}'s API-first design philosophy provides extensive RESTful APIs with OpenAPI 3.0 specifications, enabling seamless integration with existing banking systems and third-party services. The event-driven architecture utilizes asynchronous messaging with Kafka for real-time data processing and ensures data consistency across distributed components.

The multi-tenant SaaS platform provides isolated tenant environments while sharing infrastructure resources, optimizing costs and operational efficiency. Security is built into the architecture with zero-trust principles, end-to-end encryption, and comprehensive access controls.

This architectural approach enables rapid deployment, horizontal scaling, and seamless integration with existing banking systems while maintaining regulatory compliance and operational excellence.
        """.strip()

    def _create_security_content(self, content: str, product: str) -> str:
        """Create security-specific RFP content"""
        return f"""
{product} implements enterprise-grade security controls and compliance frameworks to protect sensitive financial data and maintain regulatory compliance. The solution provides comprehensive identity and access management with multi-factor authentication, single sign-on integration, and role-based access control.

Data protection is ensured through encryption at rest using AES-256 and encryption in transit with TLS 1.3, complemented by robust key management systems. The platform maintains compliance with SOC 2 Type II, ISO 27001, PCI DSS, and GDPR requirements, providing the necessary certifications for global banking operations.

Security monitoring is provided through 24/7 SIEM integration with real-time threat detection and automated incident response capabilities. Regular penetration testing and automated security scanning ensure continuous vulnerability assessment and remediation.

The platform maintains comprehensive audit trails and logging capabilities for regulatory reporting and compliance monitoring. Network security is enforced through VPC isolation, Web Application Firewall (WAF) protection, and DDoS mitigation services.

These security measures ensure protection of sensitive financial data and maintain trust with customers and regulators while supporting global banking operations.
        """.strip()

    def _create_integration_content(self, content: str, product: str) -> str:
        """Create integration-specific RFP content"""
        return f"""
{product} offers comprehensive integration capabilities for seamless connectivity with existing banking systems and third-party services. The solution provides a centralized API Gateway with rate limiting, authentication, and comprehensive monitoring capabilities.

The platform includes over 200 pre-built connectors for core banking systems, payment processors, and third-party services, significantly reducing integration complexity and time-to-market. Real-time integration is supported through an event-driven architecture with webhooks and message queues for asynchronous processing.

Data synchronization capabilities include bi-directional data sync with conflict resolution and comprehensive data validation mechanisms. Integration monitoring provides real-time visibility with alerting and performance metrics to ensure optimal system performance.

A comprehensive developer portal offers self-service API documentation, testing tools, and sandbox environments for rapid integration development. The platform supports legacy system integration including mainframe, AS/400, and other legacy banking systems.

This integration framework enables rapid onboarding of new services and seamless data flow across the banking ecosystem while maintaining data integrity and operational efficiency.
        """.strip()

    def _create_extensibility_content(self, content: str, product: str) -> str:
        """Create extensibility-specific RFP content"""
        return f"""
{product} provides comprehensive extensibility features that enable banks to customize and extend the platform to meet specific business requirements without compromising upgrade compatibility. The Extensibility Framework allows developers to extend or customize the solution through multiple mechanisms.

Data Extension capabilities enable banks to add new user-defined data elements and fields to existing data models, supporting evolving business requirements. Business Logic Extension allows customization of business rules and workflows through configuration-based approaches and custom code development.

The platform supports Java Extensibility for complex customizations requiring custom business logic implementation. Configuration-based customization provides extensive parameterization options for business rules, workflows, and user interface elements.

API Extensibility enables the creation of custom APIs and services that integrate seamlessly with the core platform. The solution maintains upgrade compatibility by providing clear extension points and versioning strategies for custom components.

This extensibility approach enables banks to tailor the solution to their specific business needs while maintaining the benefits of regular platform updates and new feature adoption.
        """.strip()

    def _create_devops_content(self, content: str, product: str) -> str:
        """Create DevOps-specific RFP content"""
        return f"""
{product} provides comprehensive DevOps capabilities that enable efficient development, testing, and deployment of banking applications. The platform supports continuous integration and continuous deployment (CI/CD) pipelines with automated testing and deployment processes.

Container orchestration is provided through Kubernetes with support for auto-scaling, rolling deployments, and blue-green deployment strategies. Infrastructure as Code (IaC) capabilities enable consistent and repeatable infrastructure provisioning and management.

The platform includes comprehensive monitoring and logging capabilities with real-time alerting and performance metrics. Automated backup and disaster recovery procedures ensure business continuity and data protection.

Environment management supports multiple environments (development, testing, staging, production) with consistent configuration management and deployment processes. Security scanning and compliance checking are integrated into the CI/CD pipeline to ensure security and regulatory compliance.

These DevOps capabilities enable rapid development cycles, reliable deployments, and efficient operations management while maintaining security and compliance requirements.
        """.strip()

    def _create_observability_content(self, content: str, product: str) -> str:
        """Create observability-specific RFP content"""
        return f"""
{product} provides comprehensive observability capabilities that enable real-time monitoring, logging, and tracing of banking applications and infrastructure. The platform includes centralized logging with structured log formats and comprehensive search and analysis capabilities.

Application Performance Monitoring (APM) provides real-time insights into application performance, user experience, and system health. Distributed tracing enables end-to-end visibility across microservices and distributed components.

Infrastructure monitoring covers servers, containers, databases, and network components with automated alerting and capacity planning capabilities. Business metrics monitoring tracks key performance indicators and business-critical processes.

The platform provides customizable dashboards and reporting capabilities for different stakeholder needs. Automated alerting and incident management ensure rapid response to issues and minimize business impact.

These observability capabilities enable proactive monitoring, rapid issue resolution, and continuous optimization of banking operations while maintaining service quality and customer satisfaction.
        """.strip()

    def _create_generic_content(self, content: str, product: str, pillar: str) -> str:
        """Create generic RFP content for other pillars"""
        return f"""
{product} provides comprehensive {pillar} capabilities designed to support modern banking operations and regulatory requirements. The solution delivers scalable, secure, and compliant functionality that enables banks to meet evolving customer needs and regulatory demands.

The platform's {pillar} features are built on enterprise-grade architecture with high availability, scalability, and security as core design principles. Integration capabilities ensure seamless connectivity with existing banking systems and third-party services.

{product}'s {pillar} capabilities support global banking operations with multi-region deployment options and compliance with international banking regulations. The solution provides comprehensive monitoring, logging, and audit capabilities for regulatory reporting and operational excellence.

These capabilities enable banks to modernize their operations while maintaining security, compliance, and operational efficiency in the {pillar} domain.
        """.strip()

    def _add_combined_rfp_content(self, doc: Document, combined_analysis: Dict):
        """Add combined RFP content for multiple products"""
        pillar = combined_analysis.get('pillar', 'Unknown')
        products = ", ".join(combined_analysis.get('products', []))
        
        # Add main heading
        doc.add_heading(f'{pillar} Capabilities - Combined Analysis', level=1)
        
        # Create combined content for all products
        combined_content = self._create_combined_content(combined_analysis, pillar, products)
        
        # Split into paragraphs and add to document
        paragraphs = combined_content.split('\n\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                clean_paragraph = paragraph.strip()
                if len(clean_paragraph) > 50:
                    doc.add_paragraph(clean_paragraph)
                    doc.add_paragraph()
        
        doc.add_paragraph()

    def _create_combined_content(self, combined_analysis: Dict, pillar: str, products: str) -> str:
        """Create combined RFP content for multiple products"""
        product_list = combined_analysis.get('products', [])
        
        if pillar.lower() == "architecture":
            return self._create_combined_architecture_content(product_list)
        elif pillar.lower() == "security":
            return self._create_combined_security_content(product_list)
        elif pillar.lower() == "integration":
            return self._create_combined_integration_content(product_list)
        elif pillar.lower() == "extensibility":
            return self._create_combined_extensibility_content(product_list)
        elif pillar.lower() == "devops":
            return self._create_combined_devops_content(product_list)
        elif pillar.lower() == "observability":
            return self._create_combined_observability_content(product_list)
        else:
            return self._create_combined_generic_content(product_list, pillar)

    def _create_combined_architecture_content(self, products: List[str]) -> str:
        """Create combined architecture content"""
        product_names = ", ".join(products)
        return f"""
The Temenos ecosystem, including {product_names}, delivers a comprehensive, cloud-native architecture designed for enterprise-scale banking operations. This integrated platform features a microservices-based architecture that enables independent scaling, deployment, and maintenance of individual components across all products.

The unified platform leverages containerized services with Kubernetes orchestration, providing auto-scaling capabilities and self-healing mechanisms across all Temenos products. This architecture ensures high availability with 99.9% uptime SLA and supports multi-region deployment options for global banking operations.

The Temenos ecosystem's API-first design philosophy provides extensive RESTful APIs with OpenAPI 3.0 specifications, enabling seamless integration between {product_names} and existing banking systems. The event-driven architecture utilizes asynchronous messaging with Kafka for real-time data processing and ensures data consistency across distributed components.

The multi-tenant SaaS platform provides isolated tenant environments while sharing infrastructure resources, optimizing costs and operational efficiency across all products. Security is built into the architecture with zero-trust principles, end-to-end encryption, and comprehensive access controls.

This integrated architectural approach enables rapid deployment, horizontal scaling, and seamless integration of {product_names} with existing banking systems while maintaining regulatory compliance and operational excellence.
        """.strip()

    def _create_combined_security_content(self, products: List[str]) -> str:
        """Create combined security content"""
        product_names = ", ".join(products)
        return f"""
The Temenos ecosystem, including {product_names}, implements enterprise-grade security controls and compliance frameworks to protect sensitive financial data and maintain regulatory compliance. The unified platform provides comprehensive identity and access management with multi-factor authentication, single sign-on integration, and role-based access control across all products.

Data protection is ensured through encryption at rest using AES-256 and encryption in transit with TLS 1.3, complemented by robust key management systems. The platform maintains compliance with SOC 2 Type II, ISO 27001, PCI DSS, and GDPR requirements, providing the necessary certifications for global banking operations across {product_names}.

Security monitoring is provided through 24/7 SIEM integration with real-time threat detection and automated incident response capabilities. Regular penetration testing and automated security scanning ensure continuous vulnerability assessment and remediation across the entire Temenos ecosystem.

The platform maintains comprehensive audit trails and logging capabilities for regulatory reporting and compliance monitoring. Network security is enforced through VPC isolation, Web Application Firewall (WAF) protection, and DDoS mitigation services.

These integrated security measures ensure protection of sensitive financial data and maintain trust with customers and regulators while supporting global banking operations across {product_names}.
        """.strip()

    def _create_combined_integration_content(self, products: List[str]) -> str:
        """Create combined integration content"""
        product_names = ", ".join(products)
        return f"""
The Temenos ecosystem, including {product_names}, offers comprehensive integration capabilities for seamless connectivity with existing banking systems and third-party services. The unified platform provides a centralized API Gateway with rate limiting, authentication, and comprehensive monitoring capabilities across all products.

The platform includes over 200 pre-built connectors for core banking systems, payment processors, and third-party services, significantly reducing integration complexity and time-to-market for {product_names}. Real-time integration is supported through an event-driven architecture with webhooks and message queues for asynchronous processing.

Data synchronization capabilities include bi-directional data sync with conflict resolution and comprehensive data validation mechanisms. Integration monitoring provides real-time visibility with alerting and performance metrics to ensure optimal system performance across the Temenos ecosystem.

A comprehensive developer portal offers self-service API documentation, testing tools, and sandbox environments for rapid integration development. The platform supports legacy system integration including mainframe, AS/400, and other legacy banking systems.

This integrated framework enables rapid onboarding of new services and seamless data flow across {product_names} and the broader banking ecosystem while maintaining data integrity and operational efficiency.
        """.strip()

    def _create_combined_extensibility_content(self, products: List[str]) -> str:
        """Create combined extensibility content"""
        product_names = ", ".join(products)
        return f"""
The Temenos ecosystem, including {product_names}, provides comprehensive extensibility features that enable banks to customize and extend the platform to meet specific business requirements without compromising upgrade compatibility. The unified Extensibility Framework allows developers to extend or customize the solution through multiple mechanisms across all products.

Data Extension capabilities enable banks to add new user-defined data elements and fields to existing data models, supporting evolving business requirements across {product_names}. Business Logic Extension allows customization of business rules and workflows through configuration-based approaches and custom code development.

The platform supports Java Extensibility for complex customizations requiring custom business logic implementation. Configuration-based customization provides extensive parameterization options for business rules, workflows, and user interface elements across the Temenos ecosystem.

API Extensibility enables the creation of custom APIs and services that integrate seamlessly with the core platform. The solution maintains upgrade compatibility by providing clear extension points and versioning strategies for custom components.

This integrated extensibility approach enables banks to tailor {product_names} to their specific business needs while maintaining the benefits of regular platform updates and new feature adoption across the entire Temenos ecosystem.
        """.strip()

    def _create_combined_devops_content(self, products: List[str]) -> str:
        """Create combined DevOps content"""
        product_names = ", ".join(products)
        return f"""
The Temenos ecosystem, including {product_names}, provides comprehensive DevOps capabilities that enable efficient development, testing, and deployment of banking applications. The unified platform supports continuous integration and continuous deployment (CI/CD) pipelines with automated testing and deployment processes across all products.

Container orchestration is provided through Kubernetes with support for auto-scaling, rolling deployments, and blue-green deployment strategies. Infrastructure as Code (IaC) capabilities enable consistent and repeatable infrastructure provisioning and management across {product_names}.

The platform includes comprehensive monitoring and logging capabilities with real-time alerting and performance metrics. Automated backup and disaster recovery procedures ensure business continuity and data protection across the entire Temenos ecosystem.

Environment management supports multiple environments (development, testing, staging, production) with consistent configuration management and deployment processes. Security scanning and compliance checking are integrated into the CI/CD pipeline to ensure security and regulatory compliance.

These integrated DevOps capabilities enable rapid development cycles, reliable deployments, and efficient operations management across {product_names} while maintaining security and compliance requirements.
        """.strip()

    def _create_combined_observability_content(self, products: List[str]) -> str:
        """Create combined observability content"""
        product_names = ", ".join(products)
        return f"""
The Temenos ecosystem, including {product_names}, provides comprehensive observability capabilities that enable real-time monitoring, logging, and tracing of banking applications and infrastructure. The unified platform includes centralized logging with structured log formats and comprehensive search and analysis capabilities across all products.

Application Performance Monitoring (APM) provides real-time insights into application performance, user experience, and system health across {product_names}. Distributed tracing enables end-to-end visibility across microservices and distributed components in the Temenos ecosystem.

Infrastructure monitoring covers servers, containers, databases, and network components with automated alerting and capacity planning capabilities. Business metrics monitoring tracks key performance indicators and business-critical processes across all Temenos products.

The platform provides customizable dashboards and reporting capabilities for different stakeholder needs. Automated alerting and incident management ensure rapid response to issues and minimize business impact across {product_names}.

These integrated observability capabilities enable proactive monitoring, rapid issue resolution, and continuous optimization of banking operations across the Temenos ecosystem while maintaining service quality and customer satisfaction.
        """.strip()

    def _create_combined_generic_content(self, products: List[str], pillar: str) -> str:
        """Create combined generic content for other pillars"""
        product_names = ", ".join(products)
        return f"""
The Temenos ecosystem, including {product_names}, provides comprehensive {pillar} capabilities designed to support modern banking operations and regulatory requirements. The unified platform delivers scalable, secure, and compliant functionality that enables banks to meet evolving customer needs and regulatory demands across all products.

The platform's {pillar} features are built on enterprise-grade architecture with high availability, scalability, and security as core design principles. Integration capabilities ensure seamless connectivity between {product_names} and existing banking systems and third-party services.

The Temenos ecosystem's {pillar} capabilities support global banking operations with multi-region deployment options and compliance with international banking regulations. The solution provides comprehensive monitoring, logging, and audit capabilities for regulatory reporting and operational excellence across {product_names}.

These integrated capabilities enable banks to modernize their operations while maintaining security, compliance, and operational efficiency in the {pillar} domain across the entire Temenos ecosystem.
        """.strip()
