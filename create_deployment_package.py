#!/usr/bin/env python3
"""
Create deployment package for Azure Web App
"""

import os
import zipfile
import shutil
from pathlib import Path

def create_deployment_package():
    """Create a deployment package for Azure Web App"""
    
    # Files to include in deployment
    include_files = [
        'app.py',
        'rag_client.py',
        'word_generator.py',
        'shared_config.py',
        'requirements.txt',
        'host.json',
        'function_app.py',
        'templates/',
        'static/',
        '.gitignore'
    ]
    
    # Files to exclude
    exclude_patterns = [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '.env',
        'reports/',
        'word_documents/',
        '*.log',
        '.git/',
        '.vscode/',
        '.idea/'
    ]
    
    print("📦 Creating deployment package...")
    
    # Create deployment directory
    deployment_dir = Path('deployment')
    if deployment_dir.exists():
        try:
            shutil.rmtree(deployment_dir)
        except PermissionError:
            print("  ⚠️ Could not remove existing deployment directory")
            print("  📁 Please manually delete the 'deployment' folder and try again")
            return
    deployment_dir.mkdir()
    
    # Copy files
    for item in include_files:
        src = Path(item)
        dst = deployment_dir / item
        
        if src.is_file():
            print(f"  📄 Copying file: {item}")
            shutil.copy2(src, dst)
        elif src.is_dir():
            print(f"  📁 Copying directory: {item}")
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*exclude_patterns))
    
    # Create necessary directories
    (deployment_dir / 'reports').mkdir(exist_ok=True)
    (deployment_dir / 'word_documents').mkdir(exist_ok=True)
    
    # Create .deployment file for Azure
    with open(deployment_dir / '.deployment', 'w') as f:
        f.write('[config]\n')
        f.write('SCM_DO_BUILD_DURING_DEPLOYMENT=true\n')
    
    # Create web.config for Azure
    web_config = '''<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="PythonHandler" path="*" verb="*" modules="httpPlatformHandler" resourceType="Unspecified"/>
    </handlers>
    <httpPlatform processPath="D:\\home\\Python39\\python.exe"
                  arguments="D:\\home\\site\\wwwroot\\app.py"
                  stdoutLogEnabled="true"
                  stdoutLogFile="D:\\home\\LogFiles\\python.log"
                  startupTimeLimit="60"
                  startupRetryCount="3">
    </httpPlatform>
  </system.webServer>
</configuration>'''
    
    with open(deployment_dir / 'web.config', 'w') as f:
        f.write(web_config)
    
    # Create deployment.zip
    zip_path = 'deployment.zip'
    if os.path.exists(zip_path):
        os.remove(zip_path)
    
    print(f"  📦 Creating {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deployment_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(deployment_dir)
                zipf.write(file_path, arc_path)
    
    # Clean up deployment directory (Windows-safe)
    try:
        shutil.rmtree(deployment_dir)
    except PermissionError:
        print("  ⚠️ Could not remove deployment directory (files may be in use)")
        print("  📁 You can manually delete the 'deployment' folder")
    
    # Get file size
    file_size = os.path.getsize(zip_path)
    size_mb = file_size / (1024 * 1024)
    
    print(f"✅ Deployment package created successfully!")
    print(f"📁 Package: {zip_path}")
    print(f"📊 Size: {size_mb:.2f} MB")
    print("")
    print("🚀 Ready for Azure deployment!")
    print("   Use: az webapp deployment source config-zip --src deployment.zip")

if __name__ == "__main__":
    create_deployment_package()
