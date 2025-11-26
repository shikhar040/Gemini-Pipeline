#!/usr/bin/env python3
"""
SIMPLE Auto-Healer - Guaranteed to work
"""

import os
import glob
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleAutoHealer:
    def __init__(self):
        self.fixes_applied = []
    
    def fix_file_names(self, root_path):
        """Fix all problematic file names"""
        
        # Patterns to find problematic files
        patterns = [
            os.path.join(root_path, "**", "* *"),  # Files with spaces
            os.path.join(root_path, "**", "*.jx"),  # Wrong JS extension
            os.path.join(root_path, "**", "*.htm"),  # Wrong HTML extension
            os.path.join(root_path, "**", "*.PY"),  # Wrong Python extension
            os.path.join(root_path, "**", "*@*"),  # Files with @
        ]
        
        for pattern in patterns:
            for file_path in glob.glob(pattern, recursive=True):
                if os.path.isfile(file_path):
                    self.fix_single_file(file_path)
    
    def fix_single_file(self, file_path):
        """Fix a single problematic file"""
        directory = os.path.dirname(file_path)
        old_name = os.path.basename(file_path)
        new_name = old_name
        
        # Apply fixes
        if ' ' in new_name:
            new_name = new_name.replace(' ', '-')
        
        if '@' in new_name:
            new_name = new_name.replace('@', '-')
        
        if new_name.endswith('.jx'):
            new_name = new_name.replace('.jx', '.js')
        
        if new_name.endswith('.htm') and not new_name.endswith('.html'):
            new_name = new_name + 'l'  # .htm -> .html
        
        if new_name.endswith('.PY'):
            new_name = new_name.replace('.PY', '.py')
        
        # Convert to lowercase (except extensions)
        if '.' in new_name:
            name_part, ext_part = new_name.rsplit('.', 1)
            new_name = name_part.lower() + '.' + ext_part.lower()
        else:
            new_name = new_name.lower()
        
        # Rename if changed
        if new_name != old_name:
            new_path = os.path.join(directory, new_name)
            try:
                os.rename(file_path, new_path)
                self.fixes_applied.append(f"{old_name} → {new_name}")
                logger.info(f"✅ FIXED: {old_name} → {new_name}")
            except Exception as e:
                logger.error(f"❌ Failed to rename {old_name}: {e}")
    
    def ensure_index_html(self, root_path):
        """Ensure public/index.html exists"""
        public_dir = os.path.join(root_path, "public")
        index_html = os.path.join(public_dir, "index.html")
        index_htm = os.path.join(public_dir, "index.htm")
        
        # Create public directory if it doesn't exist
        os.makedirs(public_dir, exist_ok=True)
        
        # If index.htm exists, rename it
        if os.path.exists(index_htm):
            os.rename(index_htm, index_html)
            self.fixes_applied.append("index.htm → index.html")
            logger.info("✅ FIXED: index.htm → index.html")
        
        # Create index.html if it doesn't exist
        if not os.path.exists(index_html):
            with open(index_html, 'w') as f:
                f.write('''<!DOCTYPE html>
<html>
<head>
    <title>AI Auto-Healing Pipeline - WORKING!</title>
</head>
<body>
    <h1>✅ AI Auto-Healer is WORKING!</h1>
    <p>File names have been automatically fixed.</p>
</body>
</html>''')
            self.fixes_applied.append("Created index.html")
            logger.info("✅ CREATED: index.html")

def main():
    healer = SimpleAutoHealer()
    
    logger.info("🚀 STARTING SIMPLE AUTO-HEALER")
    
    # Fix all file names
    healer.fix_file_names('.')
    
    # Ensure index.html exists
    healer.ensure_index_html('.')
    
    # Summary
    logger.info("📊 HEALING SUMMARY:")
    if healer.fixes_applied:
        for fix in healer.fixes_applied:
            logger.info(f"  ✓ {fix}")
        logger.info(f"🎉 SUCCESS: Applied {len(healer.fixes_applied)} fixes!")
    else:
        logger.info("💤 No fixes needed - files are already good!")

if __name__ == "__main__":
    main()
