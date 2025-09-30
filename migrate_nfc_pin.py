#!/usr/bin/env python3
"""
Migration script to add PIN column to NFC cards table
This script adds the PIN field to existing NFC cards
"""

import sys
import os
from sqlalchemy import text

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def migrate_nfc_pin():
    """Add PIN column to NFC cards table"""
    print("🔄 Starting NFC PIN migration...")
    
    with app.app_context():
        try:
            # Check if PIN column already exists
            result = db.session.execute(text("PRAGMA table_info(nfc_cards)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'pin' in columns:
                print("✅ PIN column already exists in nfc_cards table")
                return True
            
            # Add PIN column
            db.session.execute(text("ALTER TABLE nfc_cards ADD COLUMN pin VARCHAR(4)"))
            db.session.commit()
            
            print("✅ Successfully added PIN column to nfc_cards table")
            print("📝 PIN column added with VARCHAR(4) type")
            print("🔒 PIN is required for payments over 500 credits")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during migration: {e}")
            db.session.rollback()
            return False

def main():
    """Run the migration"""
    print("🚀 NFC PIN Migration Script")
    print("=" * 40)
    
    success = migrate_nfc_pin()
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print("\n📋 What's new:")
        print("1. 🔒 PIN field added to NFC cards")
        print("2. 💳 PIN required for payments over 500 credits")
        print("3. 🛡️ Enhanced security for high-value transactions")
        print("\n🚀 Next steps:")
        print("1. Users can now set PINs for their NFC cards")
        print("2. Payments over 500 credits will require PIN verification")
        print("3. Existing cards will work without PIN for amounts ≤ 500")
    else:
        print("\n⚠️ Migration failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
