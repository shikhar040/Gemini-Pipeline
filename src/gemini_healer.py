#!/usr/bin/env python3
"""
Enhanced Auto-Healer with Gemini AI
Fixes file names, directory structure, and code issues intelligently
"""

import os
import re
import json
import argparse
import requests
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GeminiAutoHealer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        
    def analyze_with_gemini(self, file_structure, issues):
        """Use Gemini AI to analyze and fix project structure"""
        
        prompt = f"""
        Analyze this web project structure and identify/fix issues for optimal Netlify deployment:

        CURRENT FILE STRUCTURE:
        {file_structure}

        DETECTED ISSUES:
        {issues}

        Provide specific fixes in JSON format:
        {{
            "fixes": [
                {{
                    "action": "rename|create|move|delete",
                    "from": "current_path",
                    "to": "new_path",
                    "reason": "explanation"
                }}
            ],
            "missing_files": ["file1", "file2"],
            "structure_advice": "general advice"
        }}

        Focus on:
        - Netlify deployment requirements
        - Web project best practices
        - File naming conventions
        - Directory organization
        """

        try:
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and result['candidates']:
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
            logger.error(f"API error: {response.status_code}")
            return None
                
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            return None
    
    def scan_project_structure(self, root_path):
        """Scan the project structure and identify issues"""
        issues = []
        file_structure = []
        
        for root, dirs, files in os.walk(root_path):
            if any(skip in root for skip in ['node_modules', '.git', '__pycache__']):
                continue
                
            level = root.replace(str(root_path), '').count(os.sep)
            indent = ' ' * 2 * level
            folder_name = os.path.basename(root) or root_path.name
            file_structure.append(f"{indent}{folder_name}/")
            
            sub_indent = ' ' * 2 * (level + 1)
            for file in files:
                if file in ['.DS_Store', 'Thumbs.db']:
                    continue
                file_path = os.path.join(root, file)
                file_structure.append(f"{sub_indent}{file}")
                issues.extend(self.detect_file_issues(file_path))
        
        return "\n".join(file_structure), issues
    
    def detect_file_issues(self, file_path):
        """Detect common file naming and structure issues"""
        issues = []
        filename = os.path.basename(file_path)
        
        # File naming issues
        if re.search(r'[!@#$%^&*()\s]', filename.replace(' ', '').replace('-', '').replace('_', '')):
            issues.append(f"Special characters in filename: {filename}")
        
        if ' ' in filename:
            issues.append(f"Spaces in filename: {filename}")
        
        if filename != filename.lower() and not any(filename.endswith(ext) for ext in ['.md', '.txt', '.json', '.gitignore']):
            issues.append(f"Uppercase letters in filename: {filename}")
        
        # Extension issues
        if filename.endswith(('.jx', '.htm', '.cssx')):
            issues.append(f"Suspicious file extension: {filename}")
        
        return issues
    
    def apply_fixes(self, fixes, root_path):
        """Apply the fixes recommended by Gemini"""
        applied_fixes = []
        
        for fix in fixes.get('fixes', []):
            try:
                action = fix.get('action')
                from_path = fix.get('from', '').lstrip('/')
                to_path = fix.get('to', '').lstrip('/')
                
                full_from = os.path.join(root_path, from_path)
                full_to = os.path.join(root_path, to_path)
                
                if action == 'rename' and os.path.exists(full_from) and full_from != full_to:
                    os.makedirs(os.path.dirname(full_to), exist_ok=True)
                    os.rename(full_from, full_to)
                    applied_fixes.append(f"Renamed: {from_path} → {to_path}")
                    
                elif action == 'create' and not os.path.exists(full_to):
                    os.makedirs(os.path.dirname(full_to), exist_ok=True)
                    if not to_path.endswith('/'):
                        with open(full_to, 'w') as f:
                            f.write(f"# Created by AI Auto-Healer\n")
                    applied_fixes.append(f"Created: {to_path}")
                    
            except Exception as e:
                logger.error(f"Failed to apply fix: {e}")
        
        return applied_fixes

def main():
    parser = argparse.ArgumentParser(description='Auto-Heal project structure with Gemini AI')
    parser.add_argument('--path', default='.', help='Project path to scan and fix')
    parser.add_argument('--api-key', required=True, help='Gemini API key')
    
    args = parser.parse_args()
    healer = GeminiAutoHealer(args.api_key)
    
    logger.info(f"Scanning project: {args.path}")
    file_structure, issues = healer.scan_project_structure(Path(args.path))
    
    if not issues:
        logger.info("✅ No issues found!")
        return
    
    logger.info(f"🔧 Found {len(issues)} issues")
    for issue in issues[:10]:  # Show first 10 issues
        logger.info(f"  - {issue}")
    
    logger.info("🤖 Consulting Gemini AI...")
    fixes = healer.analyze_with_gemini(file_structure, issues)
    
    if fixes:
        applied = healer.apply_fixes(fixes, args.path)
        logger.info(f"✅ Applied {len(applied)} fixes")
        for fix in applied:
            logger.info(f"  ✓ {fix}")
    else:
        logger.error("❌ Failed to get AI fixes")

if __name__ == "__main__":
    main()