#!/usr/bin/env python3
"""
Demo script for PlainClause: AI for Legal Assistance & Access
"""

import subprocess
import sys
import os

def run_demo():
    """Run a demonstration of PlainClause capabilities."""
    
    print("=" * 60)
    print("PLAINCLAUSE DEMO: AI for Legal Assistance & Access")
    print("=" * 60)
    print()
    
    # Check if sample files exist
    if not os.path.exists("sample_lease.txt"):
        print("Error: sample_lease.txt not found!")
        return 1
    
    print("1. Analyzing sample lease agreement as a tenant:")
    print("-" * 50)
    
    # Run the analysis
    result = subprocess.run([
        sys.executable, "main.py", 
        "--document", "sample_lease.txt",
        "--persona", "tenant"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"Error running analysis: {result.stderr}")
        return 1
    
    print("\n2. Analyzing sample lease agreement as a landlord (other persona):")
    print("-" * 50)
    
    result = subprocess.run([
        sys.executable, "main.py", 
        "--document", "sample_lease.txt",
        "--persona", "other"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"Error running analysis: {result.stderr}")
        return 1
        
    print("\n3. Verbose analysis showing detailed clause information:")
    print("-" * 50)
    
    result = subprocess.run([
        sys.executable, "main.py", 
        "--document", "sample_lease.txt",
        "--persona", "tenant",
        "--verbose"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"Error running analysis: {result.stderr}")
        return 1
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print()
    print("PlainClause successfully analyzed the lease agreement")
    print("from different perspectives, showing how the same")
    print("document presents different risks and considerations")
    print("depending on the user's role and concerns.")
    print()
    print("To try with your own documents:")
    print("  python main.py --document your_document.txt --persona tenant")
    print()
    print("Remember: This tool provides information and assistance,")
    print("not professional legal advice.")
    
    return 0

if __name__ == "__main__":
    sys.exit(run_demo())