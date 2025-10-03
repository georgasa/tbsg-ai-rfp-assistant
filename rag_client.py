#!/usr/bin/env python3
"""
Temenos RAG AI Client
Core functionality for interacting with Temenos RAG API and generating RFP responses.
"""

import requests
import json
import re
import os
import glob
from datetime import datetime
from typing import Dict, List, Optional, Any
from shared_config import API_CONFIG, CATEGORY_TO_MODEL

class TemenosRAGClient:
    """Main client for Temenos RAG AI operations"""
    
    def __init__(self, jwt_token: str = None):
        self.jwt_token = jwt_token or API_CONFIG['jwt_token']
        self.base_url = API_CONFIG['base_url']
        self.timeout = API_CONFIG['timeout']
        
        # Technology pillars configuration for RFP responses
        self.technology_pillars = {
            "Architecture": {
                "description": "Overall system architecture, deployment options, cloud capabilities, and infrastructure design",
                "context": "focus on architectural overview, deployment options, cloud capabilities, and infrastructure design",
                "questions": [
                    "What is the overall architectural approach and design philosophy of {product}?",
                    "What are the main architectural components and how do they interact with each other?",
                    "What deployment options are available (cloud, on-premises, hybrid) and their characteristics?",
                    "How does {product} handle scalability and what are the scaling mechanisms?",
                    "What are the high availability and disaster recovery architectural features?",
                    "How is {product} designed for performance and what are the key performance characteristics?",
                    "What architectural patterns are used (microservices, layered, event-driven) and why?",
                    "How does the architecture support different deployment environments and configurations?",
                    "What containerization and orchestration technologies are used in {product}?",
                    "How does {product} implement event-driven architecture and messaging patterns?",
                    "What are the specific cloud-native features and capabilities of {product}?",
                    "How does {product} handle data consistency and transaction management across distributed components?",
                    "What are the specific API management and gateway capabilities in {product}?",
                    "What are the data architecture and data flow patterns in {product}?",
                    "How does {product} support multi-tenancy and tenant isolation?"
                ]
            },
            "Extensibility": {
                "description": "Extensibility features, customization capabilities, configuration tools, and developer frameworks",
                "context": "focus on extensibility features, customization capabilities, configuration tools, and developer frameworks",
                "questions": [
                    "What extensibility and customization capabilities are available for tailoring {product}?",
                    "What development tools, frameworks, and APIs are provided for customization?",
                    "How can {product} be configured and customized without modifying core code?",
                    "What plugin and extension mechanisms are available for adding new functionality?",
                    "How does {product} support third-party integrations and custom adapters?",
                    "What low-code or no-code development capabilities are available?",
                    "How does {product} handle configuration management and environment-specific settings?",
                    "What testing and validation tools are available for custom extensions?"
                ]
            },
            "DevOps": {
                "description": "Deployment automation, CI/CD capabilities, testing frameworks, and operational tools",
                "context": "focus on deployment automation, CI/CD capabilities, testing frameworks, and operational tools",
                "questions": [
                    "What DevOps and deployment automation capabilities are available in {product}?",
                    "What CI/CD pipeline features and automation tools are provided?",
                    "How does {product} support automated testing and quality assurance?",
                    "What deployment strategies and rollback mechanisms are available?",
                    "How does {product} handle infrastructure management and provisioning?",
                    "What monitoring and alerting capabilities are available for operations?",
                    "How does {product} support continuous integration and continuous deployment?",
                    "What operational tools and dashboards are available for system management?"
                ]
            },
            "Security": {
                "description": "Security features, compliance standards, authentication, authorization, and data protection",
                "context": "focus on security features, compliance standards, authentication, authorization, and data protection",
                "questions": [
                    "What security features and capabilities are built into {product}?",
                    "How does {product} handle authentication and user identity management?",
                    "What authorization and access control mechanisms are available?",
                    "What encryption and data protection features are provided?",
                    "What compliance standards and regulatory requirements are supported?",
                    "How does {product} handle security monitoring and threat detection?",
                    "What audit and logging capabilities are available for security events?",
                    "How does {product} support security policies and governance?",
                    "What are the specific identity and access management capabilities in {product}?",
                    "How does {product} implement multi-factor authentication and single sign-on?",
                    "What are the data encryption standards and key management practices in {product}?",
                    "How does {product} handle security auditing and compliance reporting?",
                    "What are the network security and firewall capabilities in {product}?",
                    "How does {product} implement vulnerability management and security scanning?",
                    "What are the incident response and security monitoring capabilities in {product}?"
                ]
            },
            "Observability": {
                "description": "Monitoring capabilities, logging, metrics, dashboards, and operational visibility",
                "context": "focus on monitoring capabilities, logging, metrics, dashboards, and operational visibility",
                "questions": [
                    "What observability and monitoring capabilities are available in {product}?",
                    "What logging and audit trail features are provided?",
                    "What metrics collection and performance monitoring tools are available?",
                    "What dashboards and reporting capabilities are provided for operations?",
                    "How does {product} handle alerting and notification management?",
                    "What tracing and debugging capabilities are available for troubleshooting?",
                    "How does {product} support operational analytics and insights?",
                    "What health monitoring and status reporting features are available?"
                ]
            },
            "Integration": {
                "description": "API capabilities, integration patterns, data streaming, and connectivity options",
                "context": "focus on API capabilities, integration patterns, data streaming, and connectivity options",
                "questions": [
                    "What integration capabilities and connectivity options are available in {product}?",
                    "What APIs and web services are provided for system integration?",
                    "How does {product} support real-time data streaming and event processing?",
                    "What messaging and queuing capabilities are available for integration?",
                    "How does {product} handle data synchronization and consistency?",
                    "What protocol support and communication standards are available?",
                    "How does {product} support batch processing and file-based integration?",
                    "What integration monitoring and error handling capabilities are provided?"
                ]
            }
        }
    
    def test_connection(self) -> bool:
        """Test connection to Temenos RAG API"""
        # Check if demo mode is enabled
        if API_CONFIG.get("demo_mode", False):
            return True
            
        try:
            headers = {
                "Authorization": f"Bearer {self.jwt_token}",
                "Content-Type": "application/json"
            }
            # Test with health endpoint first
            response = requests.get(f"{self.base_url}/health", headers=headers, timeout=self.timeout)
            # Return True if we get any response that indicates the API is reachable
            # 200 = success, 400/401/403 = API is reachable but auth/request issues
            return response.status_code in [200, 400, 401, 403]
        except requests.exceptions.ConnectionError:
            # Connection error means API is not reachable (network issue)
            return False
        except requests.exceptions.Timeout:
            # Timeout means API is not reachable
            return False
        except Exception:
            # Other exceptions mean API is not reachable
            return False
    
    def query_rag(self, question: str, region: str, model_id: str, context: str = "") -> Optional[Dict]:
        """Query the RAG API with a question"""
        # Check if demo mode is enabled
        if API_CONFIG.get("demo_mode", False):
            return self._get_demo_response(question, model_id, region)
            
        try:
            headers = {
                "Authorization": f"Bearer {self.jwt_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "question": question,
                "region": region.lower(),  # API expects lowercase regions
                "RAGmodelId": model_id,    # API uses RAGmodelId instead of model_id
                "context": context
            }
            
            response = requests.post(
                f"{self.base_url}/query",
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                response_data = response.json()
                # Handle the new API response format
                if response_data.get("status") == "success" and "data" in response_data:
                    return response_data
                else:
                    print(f"API returned error: {response_data}")
                    return None
            elif response.status_code in [400, 401, 403]:
                # API is reachable but request has issues - try to get response anyway
                try:
                    return response.json()
                except:
                    # If we can't parse JSON, return None
                    print(f"API request failed with status {response.status_code}: {response.text}")
                    return None
            else:
                print(f"API request failed with status {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error querying RAG API: {e}")
            return None
    
    def analyze_pillar(self, region: str, model_id: str, product_name: str, pillar: str) -> Dict:
        """Analyze a specific technology pillar"""
        pillar_config = self.technology_pillars[pillar]
        context = pillar_config["context"]
        
        # Prepare analysis data
        pillar_data = {
            "pillar": pillar,
            "product": product_name,
            "region": region,
            "model_id": model_id,
            "questions_asked": [],
            "answers": [],
            "conversation_flow": [],
            "key_points": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Ask base questions
        base_questions = pillar_config["questions"]
        for i, question_template in enumerate(base_questions, 1):
            question = question_template.format(product=product_name)
            
            response = self.query_rag(question, region, model_id, context)
            
            if response:
                data = response.get('data', {})
                answer = data.get('answer', 'No answer received') if data else 'No answer received'
                
                if answer and answer.lower() not in ['no answer received', 'no answer', '']:
                    pillar_data["questions_asked"].append(question)
                    pillar_data["answers"].append(answer)
                    pillar_data["conversation_flow"].append({
                        "phase": "base",
                        "question": question,
                        "answer": answer,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    key_points = self._extract_key_points_from_answer(answer)
                    pillar_data["key_points"].extend(key_points)
            else:
                # RAG API is not available - stop analysis
                raise Exception("RAG API is not available. Cannot proceed with analysis.")
        
        # Generate summary
        pillar_data["summary"] = self._generate_pillar_summary(pillar_data)
        
        return pillar_data
    
    def _extract_key_points_from_answer(self, answer: str) -> List[str]:
        """Extract key points from an answer"""
        # Simple key point extraction - split by sentences and filter
        sentences = re.split(r'[.!?]+', answer)
        key_points = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and not sentence.startswith(('I cannot', 'I don\'t', 'I\'m not')):
                key_points.append(sentence)
        
        return key_points[:3]  # Limit to 3 key points per answer
    
    def _generate_pillar_summary(self, pillar_data: Dict) -> str:
        """Generate a summary for the pillar analysis"""
        pillar = pillar_data['pillar']
        product = pillar_data['product']
        key_points_count = len(pillar_data['key_points'])
        
        return f"Comprehensive {pillar} analysis for {product} completed. Identified {key_points_count} key technical capabilities and business value propositions suitable for RFP response preparation."
    
    def save_analysis(self, pillar_data: Dict) -> str:
        """Save pillar analysis to JSON file"""
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pillar = pillar_data['pillar'].lower().replace(" ", "_")
        product = pillar_data['product'].lower().replace(" ", "_").replace("temenos_", "")
        
        filename = f"pillar_analysis_{product}_{pillar}_{timestamp}.json"
        filepath = os.path.join(reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(pillar_data, f, indent=2, ensure_ascii=False)
        
        return filepath

    def save_combined_analysis(self, combined_analysis: Dict) -> str:
        """Save combined analysis data to JSON file"""
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pillar = combined_analysis.get('pillar', 'unknown').lower().replace(" ", "_")
        products = "_".join([p.lower().replace(" ", "_").replace("temenos_", "") for p in combined_analysis.get('products', ['unknown'])])
        
        filename = f"combined_analysis_{products}_{pillar}_{timestamp}.json"
        filepath = os.path.join(reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(combined_analysis, f, indent=2, ensure_ascii=False)
        
        return filepath

    def _get_demo_response(self, question: str, model_id: str, region: str) -> Dict:
        """Generate realistic demo response for testing purposes"""
        # Extract key terms from question for context-aware response
        question_lower = question.lower()
        
        if "architecture" in question_lower:
            answer = f"""Temenos {model_id} provides a comprehensive, cloud-native architecture designed for scalability and resilience. The solution features:

• **Microservices Architecture**: Containerized services with independent scaling and deployment capabilities
• **API-First Design**: RESTful APIs with OpenAPI 3.0 specifications for seamless integration
• **Event-Driven Architecture**: Asynchronous messaging with Kafka for real-time data processing
• **Multi-Tenant SaaS Platform**: Isolated tenant environments with shared infrastructure
• **Cloud-Native Deployment**: Kubernetes orchestration with auto-scaling and self-healing capabilities
• **High Availability**: 99.9% uptime SLA with multi-region deployment options
• **Security by Design**: Zero-trust architecture with end-to-end encryption

This architecture enables rapid deployment, horizontal scaling, and seamless integration with existing banking systems while maintaining regulatory compliance and operational excellence."""
        
        elif "security" in question_lower:
            answer = f"""Temenos {model_id} implements enterprise-grade security controls and compliance frameworks:

• **Identity & Access Management**: Multi-factor authentication, SSO integration, and role-based access control
• **Data Protection**: Encryption at rest (AES-256) and in transit (TLS 1.3) with key management
• **Regulatory Compliance**: SOC 2 Type II, ISO 27001, PCI DSS, and GDPR compliance
• **Security Monitoring**: 24/7 SIEM integration with real-time threat detection
• **Vulnerability Management**: Regular penetration testing and automated security scanning
• **Audit Trail**: Comprehensive logging and audit capabilities for regulatory reporting
• **Network Security**: VPC isolation, WAF protection, and DDoS mitigation

These security measures ensure protection of sensitive financial data and maintain trust with customers and regulators."""
        
        elif "integration" in question_lower:
            answer = f"""Temenos {model_id} offers comprehensive integration capabilities for seamless connectivity:

• **API Gateway**: Centralized API management with rate limiting, authentication, and monitoring
• **Pre-built Connectors**: 200+ connectors for core banking, payment systems, and third-party services
• **Real-time Integration**: Event-driven architecture with webhooks and message queues
• **Data Synchronization**: Bi-directional data sync with conflict resolution and data validation
• **Integration Monitoring**: Real-time monitoring with alerting and performance metrics
• **Developer Portal**: Self-service API documentation and testing tools
• **Legacy System Integration**: Support for mainframe, AS/400, and other legacy systems

This integration framework enables rapid onboarding of new services and seamless data flow across the banking ecosystem."""
        
        else:
            answer = f"""Temenos {model_id} provides comprehensive capabilities for modern banking operations:

• **Scalable Platform**: Cloud-native architecture supporting millions of transactions
• **Real-time Processing**: Sub-second response times for critical banking operations
• **Regulatory Compliance**: Built-in compliance with international banking regulations
• **API-First Design**: Extensive API library for seamless third-party integrations
• **Advanced Analytics**: AI-powered insights for risk management and customer experience
• **Multi-Channel Support**: Unified platform for digital, mobile, and branch operations
• **Global Deployment**: Multi-region support with local data residency options

This solution enables banks to modernize their operations while maintaining security, compliance, and operational excellence."""
        
        return {
            "status": "success",
            "data": {
                "question": question,
                "region": region,
                "model_ids": [model_id],
                "answer": answer,
                "context_used": bool(context),
                "models_queried": 1
            },
            "metadata": {
                "api_version": "v1.0",
                "timestamp": datetime.now().isoformat(),
                "response_length": len(answer),
                "query_type": "single_model"
            }
        }
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        return list(CATEGORY_TO_MODEL.values())
    
    def get_technology_pillars(self) -> List[str]:
        """Get list of available technology pillars"""
        return list(self.technology_pillars.keys())
