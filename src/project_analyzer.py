#!/usr/bin/env python3
"""
Project structure analyzer for the auto-healing pipeline
"""

import os
import json
from pathlib import Path

def analyze_project_structure(root_path):
    """Analyze project structure and return health report"""
    
    analysis = {
        'issues': [],
        'recommendations': [],
        'file_count': 0,
        'directory_count': 0
    }
    
    for root, dirs, files in os.walk(root_path):
        # Skip unnecessary directories
        if any(skip in root for skip in ['.git', '__pycache__', 'node_modules']):
            continue
            
        analysis['directory_count'] += 1
        
        for file in files:
            analysis['file_count'] += 1
            file_path = Path(root) / file
            
            # Check for common issues
            if ' ' in file:
                analysis['issues'].append(f"Space in filename: {file_path}")
                
            if file != file.lower() and not file.startswith('README'):
                analysis['issues'].append(f"Uppercase in filename: {file_path}")
                
            if file.endswith(('.jx', '.htm')):
                analysis['issues'].append(f"Non-standard extension: {file_path}")
    
    # Generate recommendations
    if not (Path(root_path) / 'public' / 'index.html').exists():
        analysis['recommendations'].append("Create public/index.html for Netlify")
        
    if not (Path(root_path) / 'netlify.toml').exists():
        analysis['recommendations'].append("Add netlify.toml for deployment config")
    
    return analysis

if __name__ == "__main__":
    report = analyze_project_structure('.')
    print(json.dumps(report, indent=2))