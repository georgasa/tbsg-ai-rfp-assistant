#!/usr/bin/env python3
"""
Temenos RAG AI Web Application
Flask-based web application with Temenos Explorer look and feel.
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from flask_cors import CORS
import os
import json
import glob
from datetime import datetime
from rag_client import TemenosRAGClient
from word_generator import WordDocumentGenerator
from shared_config import UI_CONFIG, API_CONFIG

app = Flask(__name__)
CORS(app)

# Initialize components
rag_client = TemenosRAGClient()
word_generator = WordDocumentGenerator()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', config=UI_CONFIG)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": UI_CONFIG["version"]
    })

@app.route('/api/test-connection')
def test_connection():
    """Test RAG API connection"""
    try:
        is_connected = rag_client.test_connection()
        return jsonify({
            "connected": is_connected,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "connected": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/pillars')
def get_pillars():
    """Get available technology pillars"""
    try:
        pillars = rag_client.get_technology_pillars()
        return jsonify({
            "pillars": pillars,
            "count": len(pillars)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/models')
def get_models():
    """Get available models"""
    try:
        models = rag_client.get_available_models()
        return jsonify({
            "models": models,
            "count": len(models)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_pillar():
    """Analyze a technology pillar"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['region', 'model_id', 'products', 'pillar']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Map product name to model ID
        product_to_model = {
            "Transact": "TechnologyOverview",
            "Wealth": "FuncTransactWealth", 
            "Digital": "digital_model",
            "TAP": "TechTAP",
            "Payments": "Payments",
            "Analytics": "Analytics",
            "DataHub": "DataHub",
            "ModularBanking": "ModularBanking",
            "SaaS": "SaaSUniformTerms",
            "FCM": "FuncFCM",
            "TransactWealth": "FuncTransactWealth",
            "TAPWealth": "funcWealthTAP",
            "TransactGeneric": "FuncTransactGeneric"
        }
        
        # Handle multiple products - combine analysis into single document
        combined_analysis = {
            "pillar": data['pillar'],
            "region": data['region'],
            "products": data['products'],
            "combined_answers": [],
            "combined_key_points": [],
            "product_analyses": [],
            "total_api_calls": 0,  # Track total API calls
            "timestamp": datetime.now().isoformat()
        }
        
        # Analyze each product and combine results
        for product_name in data['products']:
            model_id = product_to_model.get(product_name, "TechnologyOverview")
            
            try:
                # Perform analysis for this product
                pillar_data = rag_client.analyze_pillar(
                    region=data['region'],
                    model_id=model_id,
                    product_name=product_name,
                    pillar=data['pillar']
                )
            except Exception as e:
                # RAG API is not available
                return jsonify({
                    "success": False,
                    "error": "RAG API is not available. Please check your connection and try again.",
                    "details": str(e)
                }), 503
            
            # Add product-specific analysis
            combined_analysis["product_analyses"].append({
                "product": product_name,
                "analysis": pillar_data
            })
            
            # Add API calls count
            if 'api_calls_made' in pillar_data:
                combined_analysis["total_api_calls"] += pillar_data['api_calls_made']
            
            # Combine answers and key points
            if 'answers' in pillar_data:
                for answer in pillar_data['answers']:
                    combined_analysis["combined_answers"].append(f"[{product_name}] {answer}")
            
            if 'key_points' in pillar_data:
                for point in pillar_data['key_points']:
                    combined_analysis["combined_key_points"].append(f"[{product_name}] {point}")
        
        # Save combined analysis
        combined_filepath = rag_client.save_combined_analysis(combined_analysis)
        
        # Generate single Word document for all products
        word_filepath = None
        word_filename = None
        if word_generator:
            try:
                word_filepath = word_generator.create_combined_document(combined_analysis)
                if word_filepath:
                    word_filename = os.path.basename(word_filepath)
                    print(f"Combined Word document generated: {word_filepath}")
                else:
                    print(f"Combined Word document generation failed")
            except Exception as e:
                print(f"Error generating combined Word document: {e}")
                word_filepath = None
                word_filename = None
        
        # Return combined results
        return jsonify({
            "success": True,
            "combined_analysis": combined_analysis,
            "filepath": combined_filepath,
            "word_filepath": word_filepath,
            "word_filename": word_filename,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-word', methods=['POST'])
def generate_word_document():
    """Generate Word document from analysis"""
    try:
        data = request.get_json()
        
        if 'analysis' not in data:
            return jsonify({"error": "Missing analysis data"}), 400
        
        # Create Word document
        filepath = word_generator.create_document(data)
        
        if filepath:
            return jsonify({
                "success": True,
                "filepath": filepath,
                "filename": os.path.basename(filepath),
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({"error": "Failed to create Word document"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-combined-word', methods=['POST'])
def generate_combined_word_document():
    """Generate combined Word document from multiple products analysis"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Missing combined analysis data"}), 400
        
        # Create combined Word document
        filepath = word_generator.create_combined_document(data)
        
        if filepath:
            return jsonify({
                "success": True,
                "filepath": filepath,
                "filename": os.path.basename(filepath),
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({"error": "Failed to create combined Word document"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    """Download generated file"""
    try:
        # Security check - only allow files from specific directories
        if filename.endswith('.docx'):
            filepath = os.path.join('word_documents', filename)
        elif filename.endswith('.json'):
            filepath = os.path.join('reports', filename)
        else:
            return jsonify({"error": "Invalid file type"}), 400
        
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({"error": "File not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/reports')
def list_reports():
    """List available reports"""
    try:
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            return jsonify({"reports": []})
        
        files = glob.glob(os.path.join(reports_dir, "*.json"))
        reports = []
        
        for filepath in files:
            filename = os.path.basename(filepath)
            stat = os.stat(filepath)
            reports.append({
                "filename": filename,
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        
        # Sort by modification time (newest first)
        reports.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({"reports": reports})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/word-documents')
def list_word_documents():
    """List available Word documents"""
    try:
        word_docs_dir = "word_documents"
        if not os.path.exists(word_docs_dir):
            return jsonify({"documents": []})
        
        files = glob.glob(os.path.join(word_docs_dir, "*.docx"))
        documents = []
        
        for filepath in files:
            filename = os.path.basename(filepath)
            stat = os.stat(filepath)
            documents.append({
                "filename": filename,
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        
        # Sort by modification time (newest first)
        documents.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({"documents": documents})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear all reports and word documents"""
    try:
        import shutil
        
        cleared_files = []
        
        # Clear reports directory
        reports_dir = "reports"
        if os.path.exists(reports_dir):
            for filename in os.listdir(reports_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(reports_dir, filename)
                    try:
                        os.remove(file_path)
                        cleared_files.append(f"reports/{filename}")
                    except PermissionError:
                        print(f"Could not remove {file_path} - file may be in use")
        
        # Clear word documents directory
        word_docs_dir = "word_documents"
        if os.path.exists(word_docs_dir):
            for filename in os.listdir(word_docs_dir):
                if filename.endswith('.docx'):
                    file_path = os.path.join(word_docs_dir, filename)
                    try:
                        os.remove(file_path)
                        cleared_files.append(f"word_documents/{filename}")
                    except PermissionError:
                        print(f"Could not remove {file_path} - file may be in use")
        
        return jsonify({
            "success": True,
            "cleared_files": cleared_files,
            "count": len(cleared_files),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/batch-analyze', methods=['POST'])
def batch_analyze():
    """Analyze multiple pillars in batch"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['region', 'model_id', 'products', 'pillars']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        results = []
        successful = 0
        failed = 0
        
        # Map product name to model ID
        product_to_model = {
            "Transact": "TechnologyOverview",
            "Wealth": "FuncTransactWealth", 
            "Digital": "digital_model",
            "TAP": "TechTAP",
            "Payments": "Payments",
            "Analytics": "Analytics",
            "DataHub": "DataHub",
            "ModularBanking": "ModularBanking",
            "SaaS": "SaaSUniformTerms",
            "FCM": "FuncFCM",
            "TransactWealth": "FuncTransactWealth",
            "TAPWealth": "funcWealthTAP",
            "TransactGeneric": "FuncTransactGeneric"
        }
        
        # Handle multiple products and pillars
        for product_name in data['products']:
            model_id = product_to_model.get(product_name, "TechnologyOverview")
            
            for pillar in data['pillars']:
                try:
                    pillar_data = rag_client.analyze_pillar(
                        region=data['region'],
                        model_id=model_id,
                        product_name=product_name,
                        pillar=pillar
                    )
                    
                    filepath = rag_client.save_analysis(pillar_data)
                    
                    # Generate Word document
                    word_filepath = None
                    word_filename = None
                    if word_generator:
                        try:
                            word_filepath = word_generator.convert_json_to_word(filepath)
                            if word_filepath:
                                word_filename = os.path.basename(word_filepath)
                        except Exception as e:
                            print(f"Error generating Word document: {e}")
                    
                    results.append({
                        "product": product_name,
                        "pillar": pillar,
                        "success": True,
                        "filepath": filepath,
                        "word_filepath": word_filepath,
                        "word_filename": word_filename
                    })
                    successful += 1
                    
                except Exception as e:
                    # RAG API is not available
                    if "RAG API is not available" in str(e):
                        return jsonify({
                            "success": False,
                            "error": "RAG API is not available. Please check your connection and try again.",
                            "details": str(e)
                        }), 503
                    
                    results.append({
                        "product": product_name,
                        "pillar": pillar,
                        "success": False,
                        "error": str(e)
                    })
                    failed += 1
        
        return jsonify({
            "success": True,
            "results": results,
            "summary": {
                "total": len(data['pillars']),
                "successful": successful,
                "failed": failed
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('reports', exist_ok=True)
    os.makedirs('word_documents', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
