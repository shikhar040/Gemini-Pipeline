#!/usr/bin/env python3
"""
Project health checker script
"""

import json
import sys
from pathlib import Path
from src.project_analyzer import analyze_project_structure

def main():
    """Check project health and print report"""
    report = analyze_project_structure('.')
    
    print("🔍 PROJECT HEALTH REPORT")
    print("=" * 50)
    print(f"📁 Files: {report['file_count']}")
    print(f"📂 Directories: {report['directory_count']}")
    print(f"⚠️  Issues: {len(report['issues'])}")
    print(f"💡 Recommendations: {len(report['recommendations'])}")
    
    if report['issues']:
        print("\n❌ ISSUES FOUND:")
        for issue in report['issues'][:5]:  # Show first 5
            print(f"  - {issue}")
    
    if report['recommendations']:
        print("\n✅ RECOMMENDATIONS:")
        for rec in report['recommendations']:
            print(f"  - {rec}")
    
    # Exit with error code if issues found
    sys.exit(len(report['issues']))

if __name__ == "__main__":
    main()