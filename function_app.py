#!/usr/bin/env python3
"""
Azure Functions App for Temenos RAG AI System
"""

import azure.functions as func
import json
import os
from datetime import datetime
from rag_client import TemenosRAGClient
from word_generator import WordDocumentGenerator
from shared_config import API_CONFIG

# Initialize components
rag_client = TemenosRAGClient()
word_generator = WordDocumentGenerator()

app = func.FunctionApp()

@app.route(route="health", methods=["GET"])
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint"""
    return func.HttpResponse(
        json.dumps({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0"
        }),
        status_code=200,
        headers={"Content-Type": "application/json"}
    )

@app.route(route="test-connection", methods=["GET"])
def test_connection(req: func.HttpRequest) -> func.HttpResponse:
    """Test RAG API connection"""
    try:
        is_connected = rag_client.test_connection()
        return func.HttpResponse(
            json.dumps({
                "connected": is_connected,
                "timestamp": datetime.now().isoformat()
            }),
            status_code=200,
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({
                "connected": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }),
            status_code=500,
            headers={"Content-Type": "application/json"}
        )

@app.route(route="pillars", methods=["GET"])
def get_pillars(req: func.HttpRequest) -> func.HttpResponse:
    """Get available technology pillars"""
    try:
        pillars = rag_client.get_technology_pillars()
        return func.HttpResponse(
            json.dumps({
                "pillars": pillars,
                "count": len(pillars)
            }),
            status_code=200,
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            headers={"Content-Type": "application/json"}
        )

@app.route(route="analyze", methods=["POST"])
def analyze_pillar(req: func.HttpRequest) -> func.HttpResponse:
    """Analyze a technology pillar"""
    try:
        data = req.get_json()
        
        # Validate required fields
        required_fields = ['region', 'model_id', 'product_name', 'pillar']
        for field in required_fields:
            if field not in data:
                return func.HttpResponse(
                    json.dumps({"error": f"Missing required field: {field}"}),
                    status_code=400,
                    headers={"Content-Type": "application/json"}
                )
        
        # Perform analysis
        pillar_data = rag_client.analyze_pillar(
            region=data['region'],
            model_id=data['model_id'],
            product_name=data['product_name'],
            pillar=data['pillar']
        )
        
        # Save analysis
        filepath = rag_client.save_analysis(pillar_data)
        
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "analysis": pillar_data,
                "filepath": filepath,
                "timestamp": datetime.now().isoformat()
            }),
            status_code=200,
            headers={"Content-Type": "application/json"}
        )
        
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            headers={"Content-Type": "application/json"}
        )

@app.route(route="batch-analyze", methods=["POST"])
def batch_analyze(req: func.HttpRequest) -> func.HttpResponse:
    """Analyze multiple pillars in batch"""
    try:
        data = req.get_json()
        
        # Validate required fields
        required_fields = ['region', 'model_id', 'product_name', 'pillars']
        for field in required_fields:
            if field not in data:
                return func.HttpResponse(
                    json.dumps({"error": f"Missing required field: {field}"}),
                    status_code=400,
                    headers={"Content-Type": "application/json"}
                )
        
        results = []
        successful = 0
        failed = 0
        
        for pillar in data['pillars']:
            try:
                pillar_data = rag_client.analyze_pillar(
                    region=data['region'],
                    model_id=data['model_id'],
                    product_name=data['product_name'],
                    pillar=pillar
                )
                
                filepath = rag_client.save_analysis(pillar_data)
                results.append({
                    "pillar": pillar,
                    "success": True,
                    "filepath": filepath
                })
                successful += 1
                
            except Exception as e:
                results.append({
                    "pillar": pillar,
                    "success": False,
                    "error": str(e)
                })
                failed += 1
        
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "results": results,
                "summary": {
                    "total": len(data['pillars']),
                    "successful": successful,
                    "failed": failed
                },
                "timestamp": datetime.now().isoformat()
            }),
            status_code=200,
            headers={"Content-Type": "application/json"}
        )
        
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            headers={"Content-Type": "application/json"}
        )
