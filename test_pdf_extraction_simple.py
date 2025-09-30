#!/usr/bin/env python3
"""
Simple test script for PDF roll number extraction
Run this to test PDF extraction without needing web interface
"""

import sys
import os
import re

# Add the current directory to Python path so we can import from app.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def _validate_roll_number(roll: str) -> bool:
    """Validate if a string looks like a valid roll number"""
    if not roll or len(roll) < 4 or len(roll) > 15:
        return False
    
    # Skip if all zeros or too many zeros
    if roll.count('0') > len(roll) * 0.8:  # Skip if more than 80% zeros
        return False
    
    # Skip if too many repeated digits/characters
    if len(set(roll)) < 3:  # Skip if less than 3 unique characters
        return False
    
    # Skip common non-roll-number patterns
    invalid_patterns = [
        'HTTP', 'HTML', 'PDF', 'XML', 'CSS', 'JS', 'PHP', 'SQL',
        'WWW', 'COM', 'ORG', 'NET', 'GOV', 'EDU',
        'COPYRIGHT', 'ALLRIGHTS', 'RESERVED'
    ]
    
    if roll in invalid_patterns:
        return False
    
    # Skip if it's mostly punctuation or special characters
    if sum(1 for c in roll if c.isalnum()) < len(roll) * 0.7:
        return False
    
    return True

def extract_text_from_pdf_simple(pdf_path: str) -> str:
    """Extract text from PDF using multiple methods"""
    if not os.path.exists(pdf_path):
        print(f"PDF file not found: {pdf_path}")
        return ""
    
    # Try pypdf first
    try:
        import pypdf
        text_parts = []
        with open(pdf_path, 'rb') as f:
            reader = pypdf.PdfReader(f)
            print(f"PDF has {len(reader.pages)} pages")
            for page_num, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text_parts.append(page_text.strip())
                        print(f"Page {page_num + 1}: Extracted {len(page_text)} characters")
                    else:
                        print(f"Page {page_num + 1}: No text extracted")
                except Exception as e:
                    print(f"Error extracting page {page_num + 1}: {e}")
                    continue
        collected = "\n".join(text_parts).strip()
        if collected:
            print(f"Total extracted text length: {len(collected)} characters")
            return collected
        else:
            print("No text collected from any page")
    except Exception as e:
        print(f"pypdf extraction failed: {e}")
    
    # Try pdfminer
    try:
        from pdfminer.high_level import extract_text
        text = extract_text(pdf_path)
        if text and text.strip():
            print(f"pdfminer extracted {len(text)} characters")
        return text.strip() if text else ""
    except Exception as e:
        print(f"pdfminer extraction failed: {e}")
    
    print(f"All PDF extraction methods failed for: {pdf_path}")
    return ""

def extract_roll_numbers_from_text(text: str) -> list:
    """Extract roll numbers from text using multiple patterns"""
    if not text:
        return []
    
    patterns = [
        # Common roll number patterns
        r"\b[0-9]{2}[A-Z]{2}[0-9]{4}\b",  # Format: 22CS1234
        r"\b[A-Z]{2}[0-9]{4,6}\b",  # Format: CS1234, CS123456
        r"\b[0-9]{4}[A-Z]{2}[0-9]{2}\b",  # Format: 2024CS01
        r"\b[A-Z]{3}[0-9]{4,6}\b",  # Format: CSE1234
        r"\b[0-9]{2}[A-Z]{3}[0-9]{3}\b",  # Format: 22CSE123
        
        # More flexible patterns
        r"\b[0-9]{6,10}\b",  # Numeric only (6-10 digits)
        r"\b[A-Z0-9]{6,12}\b",  # Alphanumeric (6-12 chars)
        r"\b[0-9]{2,4}[A-Z]{1,3}[0-9]{2,6}\b",  # Flexible format
        r"\b[A-Z]{1,3}[0-9]{3,8}\b",  # Letter(s) + numbers
        
        # Patterns without word boundaries (in case of formatting issues)
        r"(?<![A-Z0-9])[0-9]{2}[A-Z]{2}[0-9]{4}(?![A-Z0-9])",  # 22CS1234
        r"(?<![A-Z0-9])[A-Z]{2}[0-9]{4,6}(?![A-Z0-9])",  # CS1234
        r"(?<![A-Z0-9])[0-9]{6,8}(?![A-Z0-9])",  # Numeric
    ]
    
    roll_numbers = []
    for pattern in patterns:
        matches = re.findall(pattern, text.upper())
        if matches:
            # Validate matches before adding
            valid_matches = [m for m in matches if _validate_roll_number(m)]
            if valid_matches:
                roll_numbers.extend(valid_matches)
                print(f"Found {len(valid_matches)} valid roll numbers with pattern: {pattern}")
                print(f"Sample matches: {valid_matches[:5]}")
                break
    
    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for r in roll_numbers:
        if r not in seen:
            seen.add(r)
            unique.append(r)
    
    return unique

def test_pdf_extraction(pdf_path: str):
    """Test PDF extraction with detailed output"""
    print(f"Testing PDF extraction for: {pdf_path}")
    print("=" * 60)
    
    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF file not found: {pdf_path}")
        return
    
    print(f"File size: {os.path.getsize(pdf_path)} bytes")
    print()
    
    # Extract text
    print("--- Extracting Text ---")
    text = extract_text_from_pdf_simple(pdf_path)
    
    if not text:
        print("ERROR: No text could be extracted from PDF")
        print("This might be a scanned PDF or image-based PDF")
        print("Try using OCR tools or provide the roll numbers manually")
        return
    
    print(f"Successfully extracted {len(text)} characters")
    print()
    
    # Show sample text
    print("--- Sample Extracted Text (first 500 chars) ---")
    print(text[:500])
    print("...")
    print()
    
    # Extract roll numbers
    print("--- Extracting Roll Numbers ---")
    roll_numbers = extract_roll_numbers_from_text(text)
    
    print(f"Found {len(roll_numbers)} roll numbers:")
    for i, roll in enumerate(roll_numbers, 1):
        print(f"{i:3d}. {roll}")
    
    if not roll_numbers:
        print("No roll numbers found. This could be because:")
        print("1. The PDF format doesn't match expected patterns")
        print("2. The roll numbers are in a different format")
        print("3. The text extraction didn't work properly")
        print()
        print("You can manually provide roll numbers in the admin interface")
    
    print("=" * 60)

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_pdf_extraction_simple.py <path_to_pdf>")
        print("Example: python test_pdf_extraction_simple.py static/uploads/results_1234567890.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    test_pdf_extraction(pdf_path)

if __name__ == "__main__":
    main()
