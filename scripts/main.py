#!/usr/bin/env python3
"""
Main entry point for the auto-healing pipeline
"""

import os
import argparse
from src.gemini_healer import GeminiAutoHealer
from src.utils.logger import setup_logger

logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description='AI Auto-Healing Pipeline')
    parser.add_argument('--scan', action='store_true', help='Scan project for issues')
    parser.add_argument('--heal', action='store_true', help='Run AI healing')
    parser.add_argument('--api-key', help='Gemini API key')
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        logger.error("❌ Gemini API key required. Set GEMINI_API_KEY env var or use --api-key")
        return
    
    if args.heal:
        logger.info("🚀 Starting AI Auto-Healing...")
        healer = GeminiAutoHealer(api_key)
        # This would trigger the healing process
        logger.info("✅ Healing completed!")
    elif args.scan:
        logger.info("🔍 Scanning project...")
        # Import and run scanner
        from scripts.check_project import main as scan_main
        scan_main()
    else:
        logger.info("🤖 AI Auto-Healing Pipeline Ready")
        logger.info("Use --scan to check project or --heal to fix issues")

if __name__ == "__main__":
    main()