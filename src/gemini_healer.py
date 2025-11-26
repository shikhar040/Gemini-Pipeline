#!/usr/bin/env python3
"""
Enhanced Auto-Healer with Gemini AI - Fixed version
"""

import os
import re
import json
import argparse
import requests
from pathlib import Path
import logging
import shutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GeminiAutoHealer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        
    def analyze_with_gemini(self, file_structure, issues):
        """Use Gemini AI to analyze and fix project structure"""
        
        prompt = f"""
        CRITICAL: Fix this web project for Netlify deployment.
        
        FILE STRUCTURE:
        {file_structure}

        DETECTED ISSUES:
        {issues}

        URGENT FIXES NEEDED:
        - Change index.htm to index.html (Netlify requires index.html)
        - Fix any other file naming issues
        - Ensure proper web file extensions

        Return JSON with specific file fixes:
        {{
            "fixes": [
                {{
                    "action": "rename",
                    "from": "current/file.htm",
                    "to": "current/file.html",
                    "reason": "Netlify requires .html extension for main file"
                }}
            ]
        }}
        """
        
        try:
            headers = {'Content-Type': 'application/json'}
            data = {"contents": [{"parts": [{"text": prompt}]}]}
            
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
                    logger.info(f"Gemini response: {content}")
                    
                    # Extract JSON from response
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                    else:
                        # If no JSON, create automatic fixes
                        return self.create_automatic_fixes(issues)
            logger.error(f"API error: {response.status_code} - {response.text}")
            return self.create_automatic_fixes(issues)
                
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            return self.create_automatic_fixes(issues)
    
    def create_automatic_fixes(self, issues):
        """Create automatic fixes when Gemini fails"""
        fixes = {"fixes": []}
        
        # Auto-fix common issues without AI
        for issue in issues:
            if "index.htm" in issue and "should be" in issue:
                fixes["fixes"].append({
                    "action": "rename",
                    "from": "public/index.htm",
                    "to": "public/index.html",
                    "reason": "Netlify requires .html extension for main file"
                })
            elif ".htm" in issue and "should be" in issue:
                original_file = issue.split(": ")[1].split(" should be")[0]
                new_file = original_file + "l"  # .htm -> .html
                fixes["fixes"].append({
                    "action": "rename", 
                    "from": original_file,
                    "to": new_file,
                    "reason": "Fix HTML file extension"
                })
                
        return fixes
    
    def scan_project_structure(self, root_path):
        """Scan the project structure and identify issues"""
        issues = []
        file_structure = []
        
        for root, dirs, files in os.walk(root_path):
            if any(skip in root for skip in ['.git', '__pycache__', 'node_modules']):
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
        file_dir = os.path.dirname(file_path)
        
        # CRITICAL: Check for .htm extension (should be .html)
        if filename == 'index.htm':
            issues.append(f"CRITICAL: index.htm should be index.html for Netlify deployment")
        
        if filename.endswith('.htm') and not filename.endswith('.html'):
            issues.append(f"Incorrect extension: {filename} should be {filename}l")
        
        # File naming issues
        if re.search(r'[!@#$%^&*()\s]', filename.replace(' ', '').replace('-', '').replace('_', '')):
            issues.append(f"Special characters in filename: {filename}")
        
        if ' ' in filename:
            issues.append(f"Spaces in filename: {filename}")
        
        if filename != filename.lower() and not filename.endswith(('.md', '.txt', '.json', '.gitignore')):
            issues.append(f"Uppercase letters in filename: {filename}")
        
        # Extension issues
        if filename.endswith(('.jx', '.cssx')):
            issues.append(f"Suspicious file extension: {filename}")
        
        # Netlify specific checks
        if filename == 'index.html' and 'public' not in file_dir:
            issues.append(f"index.html should be in public/ directory for Netlify")
        
        return issues
    
    def apply_fixes(self, fixes, root_path):
        """Apply the fixes recommended by Gemini"""
        applied_fixes = []
        
        # FIRST: Apply critical .htm to .html fixes automatically
        self.apply_critical_fixes(root_path, applied_fixes)
        
        # THEN: Apply AI-suggested fixes
        for fix in fixes.get('fixes', []):
            try:
                action = fix.get('action')
                from_path = fix.get('from', '').lstrip('/')
                to_path = fix.get('to', '').lstrip('/')
                reason = fix.get('reason', 'No reason provided')
                
                full_from = os.path.join(root_path, from_path)
                full_to = os.path.join(root_path, to_path)
                
                if action == 'rename' and os.path.exists(full_from) and full_from != full_to:
                    os.makedirs(os.path.dirname(full_to), exist_ok=True)
                    os.rename(full_from, full_to)
                    applied_fixes.append(f"Renamed: {from_path} → {to_path}")
                    logger.info(f"✅ Renamed: {from_path} → {to_path} ({reason})")
                
                elif action == 'create' and not os.path.exists(full_to):
                    os.makedirs(os.path.dirname(full_to), exist_ok=True)
                    if not to_path.endswith('/'):
                        with open(full_to, 'w') as f:
                            f.write(f"<!-- Created by AI Auto-Healer -->\n<!-- {reason} -->\n")
                    applied_fixes.append(f"Created: {to_path}")
                    
            except Exception as e:
                logger.error(f"❌ Failed to apply fix {fix}: {e}")
        
        return applied_fixes
    
    def apply_critical_fixes(self, root_path, applied_fixes):
        """Apply critical fixes that must happen regardless of AI"""
        critical_fixes = [
            # .htm to .html fixes
            ("public/index.htm", "public/index.html", "Netlify requires .html extension"),
            ("index.htm", "public/index.html", "Move and fix extension for Netlify"),
        ]
        
        for from_rel, to_rel, reason in critical_fixes:
            full_from = os.path.join(root_path, from_rel)
            full_to = os.path.join(root_path, to_rel)
            
            if os.path.exists(full_from):
                try:
                    os.makedirs(os.path.dirname(full_to), exist_ok=True)
                    shutil.move(full_from, full_to)
                    applied_fixes.append(f"CRITICAL: {from_rel} → {to_rel}")
                    logger.info(f"🚨 CRITICAL FIX: {from_rel} → {to_rel} ({reason})")
                except Exception as e:
                    logger.error(f"Failed critical fix {from_rel} → {to_rel}: {e}")
    
    def run_auto_heal(self, root_path):
        """Main healing function"""
        logger.info("🔍 Scanning project structure...")
        file_structure, issues = self.scan_project_structure(root_path)
        
        if not issues:
            logger.info("✅ No issues found! Project structure is clean.")
            return True
        
        logger.info(f"❌ Found {len(issues)} issues:")
        for issue in issues:
            logger.info(f"  - {issue}")
        
        logger.info("🤖 Consulting Gemini AI for fixes...")
        fixes = self.analyze_with_gemini(file_structure, issues)
        
        logger.info("🔧 Applying fixes...")
        applied_fixes = self.apply_fixes(fixes, root_path)
        
        # Summary
        logger.info("📊 HEALING SUMMARY:")
        logger.info(f"✅ Applied {len(applied_fixes)} fixes:")
        for fix in applied_fixes:
            logger.info(f"  ✓ {fix}")
        
        return len(applied_fixes) > 0

def main():
    parser = argparse.ArgumentParser(description='Auto-Heal project structure with Gemini AI')
    parser.add_argument('--path', default='.', help='Project path to scan and fix')
    parser.add_argument('--api-key', required=True, help='Gemini API key')
    
    args = parser.parse_args()
    
    if not args.api_key or args.api_key == "YOUR_GEMINI_API_KEY":
        logger.error("❌ Gemini API key is required!")
        logger.info("💡 Get your API key from: https://makersuite.google.com/app/apikey")
        logger.info("💡 Add it to GitHub Secrets as GEMINI_API_KEY")
        return
    
    healer = GeminiAutoHealer(args.api_key)
    success = healer.run_auto_heal(Path(args.path))
    
    if success:
        logger.info("🎉 Auto-healing completed successfully!")
    else:
        logger.info("💤 No changes were made.")

if __name__ == "__main__":
    main()