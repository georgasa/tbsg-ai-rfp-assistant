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
        self.api_calls_count = 0  # Track API calls
        
        # Technology pillars configuration for RFP responses (OPTIMIZED VERSION)
        self.technology_pillars = {
            "Architecture": {
                "description": "Overall system architecture, deployment options, cloud capabilities, and infrastructure design",
                "context": "Provide comprehensive architectural overview including design philosophy, components, deployment options, scalability, high availability, performance, architectural patterns, containerization, cloud-native features, data architecture, API management, and multi-tenancy capabilities",
                "questions": [
                    "Provide a comprehensive architectural overview of {product} including: 1) Overall design philosophy and approach, 2) Main architectural components and their interactions, 3) Deployment options (cloud, on-premises, hybrid) and characteristics, 4) Scalability mechanisms and performance design, 5) High availability and disaster recovery features, 6) Architectural patterns used (microservices, layered, event-driven), 7) Containerization and orchestration technologies, 8) Cloud-native features and capabilities, 9) Data architecture and flow patterns, 10) API management and gateway capabilities, 11) Multi-tenancy and tenant isolation support"
                ]
            },
            "Extensibility": {
                "description": "Extensibility features, customization capabilities, configuration tools, and developer frameworks",
                "context": "Provide comprehensive extensibility overview including customization capabilities, development tools, configuration options, plugin mechanisms, third-party integrations, low-code capabilities, and testing tools",
                "questions": [
                    "Provide a comprehensive extensibility overview of {product} including: 1) Customization capabilities and tailoring options, 2) Development tools, frameworks, and APIs for customization, 3) Configuration options without core code modification, 4) Plugin and extension mechanisms for new functionality, 5) Third-party integrations and custom adapters support, 6) Low-code and no-code development capabilities, 7) Configuration management and environment-specific settings, 8) Testing and validation tools for custom extensions"
                ]
            },
            "DevOps": {
                "description": "Deployment automation, CI/CD capabilities, testing frameworks, and operational tools",
                "context": "Provide comprehensive DevOps overview including deployment automation, CI/CD capabilities, testing frameworks, operational tools, infrastructure management, and monitoring capabilities",
                "questions": [
                    "Provide a comprehensive DevOps overview of {product} including: 1) Deployment automation capabilities and tools, 2) CI/CD pipeline features and automation, 3) Automated testing and quality assurance support, 4) Deployment strategies and rollback mechanisms, 5) Infrastructure management and provisioning capabilities, 6) Monitoring and alerting for operations, 7) Continuous integration and deployment support, 8) Operational tools and dashboards for system management"
                ]
            },
            "Security": {
                "description": "Security features, compliance standards, authentication, authorization, and data protection",
                "context": "Provide comprehensive security overview including built-in security features, authentication, authorization, encryption, compliance, monitoring, auditing, identity management, and incident response capabilities",
                "questions": [
                    "Provide a comprehensive security overview of {product} including: 1) Built-in security features and capabilities, 2) Authentication and user identity management, 3) Authorization and access control mechanisms, 4) Encryption and data protection features, 5) Compliance standards and regulatory requirements, 6) Security monitoring and threat detection, 7) Audit and logging for security events, 8) Security policies and governance support, 9) Identity and access management capabilities, 10) Multi-factor authentication and single sign-on, 11) Data encryption standards and key management, 12) Security auditing and compliance reporting, 13) Network security and firewall capabilities, 14) Vulnerability management and security scanning, 15) Incident response and security monitoring"
                ]
            },
            "Observability": {
                "description": "Monitoring capabilities, logging, metrics, dashboards, and operational visibility",
                "context": "Provide comprehensive observability overview including monitoring capabilities, logging, metrics, dashboards, alerting, tracing, analytics, and health monitoring",
                "questions": [
                    "Provide a comprehensive observability overview of {product} including: 1) Monitoring capabilities and operational visibility, 2) Logging and audit trail features, 3) Metrics collection and performance monitoring tools, 4) Dashboards and reporting capabilities for operations, 5) Alerting and notification management, 6) Tracing and debugging capabilities for troubleshooting, 7) Operational analytics and insights support, 8) Health monitoring and status reporting features"
                ]
            },
            "Integration": {
                "description": "API capabilities, integration patterns, data streaming, and connectivity options",
                "context": "Provide comprehensive integration overview including connectivity options, APIs, real-time streaming, messaging, data synchronization, protocol support, batch processing, and monitoring capabilities",
                "questions": [
                    "Provide a comprehensive integration overview of {product} including: 1) Integration capabilities and connectivity options, 2) APIs and web services for system integration, 3) Real-time data streaming and event processing support, 4) Messaging and queuing capabilities for integration, 5) Data synchronization and consistency handling, 6) Protocol support and communication standards, 7) Batch processing and file-based integration support, 8) Integration monitoring and error handling capabilities"
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
        # Increment API calls counter
        self.api_calls_count += 1
        
        # Check if demo mode is enabled
        if API_CONFIG.get("demo_mode", False):
            return self._get_demo_response(question, model_id, region, context)
            
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
        # Reset API calls counter for this analysis
        self.api_calls_count = 0
        
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
            "api_calls_made": 0,  # Will be updated after analysis
            "timestamp": datetime.now().isoformat()
        }
        
        # First API call - Get comprehensive overview
        base_questions = pillar_config["questions"]
        first_question = base_questions[0].format(product=product_name)
        
        response1 = self.query_rag(first_question, region, model_id, context)
        
        if not response1:
            raise Exception("RAG API is not available. Cannot proceed with analysis.")
        
        data1 = response1.get('data', {})
        first_answer = data1.get('answer', 'No answer received') if data1 else 'No answer received'
        
        if first_answer and first_answer.lower() not in ['no answer received', 'no answer', '']:
            pillar_data["questions_asked"].append(first_question)
            pillar_data["answers"].append(first_answer)
            pillar_data["conversation_flow"].append({
                "phase": "initial_overview",
                "question": first_question,
                "answer": first_answer,
                "timestamp": datetime.now().isoformat()
            })
            
            key_points = self._extract_key_points_from_answer(first_answer)
            pillar_data["key_points"].extend(key_points)
        
        # Second API call - Deep dive based on ALL key points from first response
        follow_up_question = f"Based on these {pillar.lower()} key points for {product_name}: '{first_answer[:800]}...', provide detailed technical analysis for EACH of these specific areas: 1) APIs and Web Services - technical implementation, performance metrics, security mechanisms, use cases, competitive advantages, 2) Real-Time Data Streaming - architecture details, event processing workflows, throughput capabilities, pub/sub integration, performance benchmarks, 3) Messaging and Queuing - protocol specifications, queue management, resilience patterns, fault tolerance, throughput optimization, 4) Data Synchronization - database architecture, CQRS implementation, consistency models, performance characteristics, scalability, 5) Protocol Support - supported protocols, transformation capabilities, compliance standards, interoperability, security protocols, 6) Batch Processing - file processing capabilities, ETL solutions, bulk data handling, integration patterns. For each area, provide specific technical details, implementation examples, performance metrics, competitive advantages, and business value propositions for RFP responses."
        
        response2 = self.query_rag(follow_up_question, region, model_id, context)
        
        print(f"DEBUG: Second API call response: {response2}")
        
        if response2:
            data2 = response2.get('data', {})
            second_answer = data2.get('answer', 'No answer received') if data2 else 'No answer received'
            
            print(f"DEBUG: Second answer length: {len(second_answer) if second_answer else 0}")
            print(f"DEBUG: Second answer preview: {second_answer[:200] if second_answer else 'None'}...")
            
            if second_answer and second_answer.lower() not in ['no answer received', 'no answer', '']:
                pillar_data["questions_asked"].append(follow_up_question)
                pillar_data["answers"].append(second_answer)
                pillar_data["conversation_flow"].append({
                    "phase": "detailed_insights",
                    "question": follow_up_question,
                    "answer": second_answer,
                    "timestamp": datetime.now().isoformat()
                })
                
                key_points = self._extract_key_points_from_answer(second_answer)
                pillar_data["key_points"].extend(key_points)
            else:
                print(f"DEBUG: Second answer is empty or invalid: '{second_answer}'")
        else:
            print("DEBUG: Second API call failed - no response")
        
        # Generate summary
        pillar_data["summary"] = self._generate_pillar_summary(pillar_data)
        
        # Update API calls count
        pillar_data["api_calls_made"] = self.api_calls_count
        
        # Debug: Print API calls count
        print(f"DEBUG: API calls made for {product_name} - {pillar}: {self.api_calls_count}")
        
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

    def _get_demo_response(self, question: str, model_id: str, region: str, context: str = "") -> Dict:
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
                "context_used": bool(context) if context else False,
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
