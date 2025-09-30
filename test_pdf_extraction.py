#!/usr/bin/env python3
"""
Test script to debug PDF extraction issues
Run this script to test PDF extraction without going through the web interface
"""

import os
import sys
import re
import json

def test_pdf_extraction(pdf_path):
    """Test PDF extraction with detailed debugging"""
    print(f"Testing PDF extraction for: {pdf_path}")
    print("=" * 50)
    
    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF file not found: {pdf_path}")
        return
    
    print(f"File size: {os.path.getsize(pdf_path)} bytes")
    
    # Test different extraction methods
    methods = [
        ("pypdf", test_pypdf),
        ("PyPDF2", test_pypdf2),
        ("pdfminer", test_pdfminer),
    ]
    
    for method_name, method_func in methods:
        print(f"\n--- Testing {method_name} ---")
        try:
            text = method_func(pdf_path)
            if text:
                print(f"✓ {method_name} extracted {len(text)} characters")
                print(f"First 200 characters: {text[:200]}")
                
                # Test roll number extraction
                roll_numbers = extract_roll_numbers(text)
                print(f"Roll numbers found: {roll_numbers}")
            else:
                print(f"✗ {method_name} extracted no text")
        except Exception as e:
            print(f"✗ {method_name} failed: {e}")
    
    print("\n" + "=" * 50)

def test_pypdf(pdf_path):
    """Test pypdf extraction"""
    try:
        import pypdf
        text_parts = []
        with open(pdf_path, 'rb') as f:
            reader = pypdf.PdfReader(f)
            print(f"  PDF has {len(reader.pages)} pages")
            for page_num, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text_parts.append(page_text.strip())
                        print(f"  Page {page_num + 1}: {len(page_text)} chars")
                except Exception as e:
                    print(f"  Page {page_num + 1} error: {e}")
        return "\n".join(text_parts).strip()
    except ImportError:
        print("  pypdf not available")
        return ""

def test_pypdf2(pdf_path):
    """Test PyPDF2 extraction"""
    try:
        import PyPDF2
        text_parts = []
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            print(f"  PDF has {len(reader.pages)} pages")
            for page_num, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text_parts.append(page_text.strip())
                        print(f"  Page {page_num + 1}: {len(page_text)} chars")
                except Exception as e:
                    print(f"  Page {page_num + 1} error: {e}")
        return "\n".join(text_parts).strip()
    except ImportError:
        print("  PyPDF2 not available")
        return ""

def test_pdfminer(pdf_path):
    """Test pdfminer extraction"""
    try:
        from pdfminer.high_level import extract_text
        text = extract_text(pdf_path)
        if text and text.strip():
            print(f"  pdfminer extracted {len(text)} characters")
        return text.strip() if text else ""
    except ImportError:
        print("  pdfminer not available")
        return ""

def extract_roll_numbers(text):
    """Extract roll numbers from text using multiple patterns"""
    if not text:
        return []
    
    patterns = [
        r"\b[0-9A-Z]{8,12}\b",  # Original pattern
        r"\b[0-9]{2}[A-Z]{2}[0-9]{4}\b",  # Format: 22CS1234
        r"\b[A-Z]{2}[0-9]{6,8}\b",  # Format: CS123456
        r"\b[0-9]{6,10}\b",  # Numeric only
        r"\b[A-Z0-9]{6,12}\b"  # Alphanumeric
    ]
    
    roll_numbers = []
    for pattern in patterns:
        matches = re.findall(pattern, text.upper())
        if matches:
            roll_numbers.extend(matches)
            print(f"  Pattern '{pattern}' found {len(matches)} matches")
    
    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for r in roll_numbers:
        if r not in seen:
            seen.add(r)
            unique.append(r)
    
    return unique

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_pdf_extraction.py <path_to_pdf>")
        print("Example: python test_pdf_extraction.py static/uploads/results_1234567890.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    test_pdf_extraction(pdf_path)

if __name__ == "__main__":
    main()
