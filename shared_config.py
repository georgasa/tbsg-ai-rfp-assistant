#!/usr/bin/env python3
"""
Shared Configuration for Temenos RAG AI System
Centralized configuration for both Python and web applications.
"""

import os
from typing import Dict, List, Optional

# API Configuration
API_CONFIG = {
    "base_url": "https://tbsg.temenos.com/api/v1.0",
    "jwt_token": os.getenv("TEMENOS_JWT_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYXBvc3RvbG9zLmdlb3JnYXMiLCJlbWFpbCI6ImFwb3N0b2xvcy5nZW9yZ2FzQHRlbWVub3MuY29tIiwiZXhwIjoxNzYyMDcxNjIzLCJpYXQiOjE3NTk0Nzk2MjMsImlzcyI6InRic2cudGVtZW5vcy5jb20iLCJhdWQiOiJ0ZW1lbm9zLWFwaSJ9.8VuKANbWATjEg24yJU7sxrtilmeJNJEfZ-wUIZ1Y8q0"),
    "timeout": 30,
    "max_retries": 3,
    "demo_mode": os.getenv("DEMO_MODE", "false").lower() == "true"
}

# Category to Model Mapping
CATEGORY_TO_MODEL = {
    # Generic
    "Temenos Annual Reports": "InvestorRelations",
    "Policies": "TemenosPolicies",
    # Technology
    "Analytics": "Analytics",
    "Payments Hub": "FuncPaymentsHub",
    "Transact": "TechnologyOverview",
    "TAP": "TechTAP",
    "Digital": "digital_model",
    "Modular Banking": "ModularBanking",
    "Data Hub": "DataHub",
    "Data Source": "DataSource",
    "Extensibility Framework": "ExtensibilityAdvisor",
    "Security": "SecurityFramework",
    "SaaS": "SaaSUniformTerms",
    # Functionality
    "Transact Wealth": "FuncTransactWealth",
    "FCM": "FuncFCM",
    "TAP Wealth": "funcWealthTAP",
    "Payments": "Payments",
    "Transact Generic": "FuncTransactGeneric"
}

# Available Categories
CATEGORIES = list(CATEGORY_TO_MODEL.keys())

# Models by Region
MODELS_BY_REGION = {
    "GLOBAL": list(CATEGORY_TO_MODEL.values()),
    "EMEA": list(CATEGORY_TO_MODEL.values()),
    "AMERICAS": list(CATEGORY_TO_MODEL.values()),
    "APAC": list(CATEGORY_TO_MODEL.values())
}

# UI Configuration
UI_CONFIG = {
    "app_name": "RFP Assistant",
    "version": "2.0.0",
    "theme": {
        "primary_color": "#283593",
        "secondary_color": "#E0EBF7",
        "accent_color": "#1976D2",
        "text_color": "#333333",
        "background_color": "#F5F5F5"
    },
    "features": {
        "pillar_analysis": True,
        "word_generation": True,
        "api_access": True,
        "batch_processing": True
    }
}

def get_available_categories_for_region(region: str) -> List[str]:
    """Get available categories for a specific region"""
    return CATEGORIES

def get_model_for_category(category: str, region: str = "GLOBAL") -> Optional[str]:
    """Get model ID for a category and region"""
    return CATEGORY_TO_MODEL.get(category)

def get_category_number_mapping() -> Dict[str, int]:
    """Get mapping of category names to numbers"""
    return {category: i+1 for i, category in enumerate(CATEGORIES)}

def validate_category_selection(selection: str) -> bool:
    """Validate if category selection is valid"""
    try:
        num = int(selection)
        return 1 <= num <= len(CATEGORIES)
    except ValueError:
        return selection in CATEGORIES
