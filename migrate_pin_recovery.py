#!/usr/bin/env python3
"""
Migration script to add PinRecoveryOTP table for forgot PIN functionality
"""

import sqlite3
import os
from datetime import datetime

def migrate_pin_recovery():
    """Add PinRecoveryOTP table for PIN recovery functionality"""
    
    # Database path
    db_path = 'byte_credits.db'
    
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if table already exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='pin_recovery_otp'
        """)
        
        if cursor.fetchone():
            print("PinRecoveryOTP table already exists!")
            return True
        
        # Create PinRecoveryOTP table
        cursor.execute("""
            CREATE TABLE pin_recovery_otp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) NOT NULL,
                email VARCHAR(120) NOT NULL,
                otp_code VARCHAR(6) NOT NULL,
                card_id VARCHAR(100) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME NOT NULL,
                is_used BOOLEAN DEFAULT 0
            )
        """)
        
        # Create index for better performance
        cursor.execute("""
            CREATE INDEX idx_pin_recovery_card_id ON pin_recovery_otp(card_id)
        """)
        
        cursor.execute("""
            CREATE INDEX idx_pin_recovery_username ON pin_recovery_otp(username)
        """)
        
        cursor.execute("""
            CREATE INDEX idx_pin_recovery_expires ON pin_recovery_otp(expires_at)
        """)
        
        conn.commit()
        print("✅ PinRecoveryOTP table created successfully!")
        print("✅ Indexes created for better performance!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating PinRecoveryOTP table: {e}")
        return False
        
    finally:
        if conn:
            conn.close()

def main():
    print("🔄 Starting PIN recovery migration...")
    
    if migrate_pin_recovery():
        print("✅ Migration completed successfully!")
    else:
        print("❌ Migration failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
