#!/usr/bin/env python3
"""
Database Migration Script for ByteCredits Mock Exam Feature
This script adds the missing columns to the mock_exams table
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Add missing columns to the mock_exams table"""
    
    db_path = 'byte_credits.db'
    
    if not os.path.exists(db_path):
        print(f"Database file {db_path} not found!")
        return False
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Connected to database successfully!")
        
        # Check if mock_exams table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mock_exams'")
        if not cursor.fetchone():
            print("mock_exams table does not exist. Creating it...")
            # Create the table with all columns
            cursor.execute('''
                CREATE TABLE mock_exams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exam_id VARCHAR(50) UNIQUE NOT NULL,
                    student_username VARCHAR(50) NOT NULL,
                    subject_name VARCHAR(100) NOT NULL,
                    syllabus TEXT NOT NULL,
                    question_format VARCHAR(50) NOT NULL,
                    total_questions INTEGER NOT NULL,
                    total_marks INTEGER NOT NULL,
                    time_limit INTEGER NOT NULL,
                    difficulty_level VARCHAR(20) DEFAULT 'medium',
                    format_description TEXT,
                    questions TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'created'
                )
            ''')
            print("Created mock_exams table successfully!")
        else:
            print("mock_exams table exists. Checking for missing columns...")
            
            # Get current table schema
            cursor.execute("PRAGMA table_info(mock_exams)")
            columns = [column[1] for column in cursor.fetchall()]
            print(f"Current columns: {columns}")
            
            # Add missing columns
            missing_columns = []
            
            if 'total_marks' not in columns:
                missing_columns.append(('total_marks', 'INTEGER NOT NULL DEFAULT 50'))
            
            if 'difficulty_level' not in columns:
                missing_columns.append(('difficulty_level', "VARCHAR(20) DEFAULT 'medium'"))
            
            if 'format_description' not in columns:
                missing_columns.append(('format_description', 'TEXT'))
            
            # Add each missing column
            for column_name, column_def in missing_columns:
                try:
                    alter_sql = f"ALTER TABLE mock_exams ADD COLUMN {column_name} {column_def}"
                    print(f"Adding column: {alter_sql}")
                    cursor.execute(alter_sql)
                    print(f"Successfully added column: {column_name}")
                except sqlite3.OperationalError as e:
                    if "duplicate column name" in str(e):
                        print(f"Column {column_name} already exists, skipping...")
                    else:
                        print(f"Error adding column {column_name}: {e}")
                        raise
        
        # Check if exam_attempts table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='exam_attempts'")
        if not cursor.fetchone():
            print("Creating exam_attempts table...")
            cursor.execute('''
                CREATE TABLE exam_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    attempt_id VARCHAR(50) UNIQUE NOT NULL,
                    exam_id VARCHAR(50) NOT NULL,
                    student_username VARCHAR(50) NOT NULL,
                    answers TEXT NOT NULL,
                    time_taken INTEGER,
                    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (exam_id) REFERENCES mock_exams (exam_id)
                )
            ''')
            print("Created exam_attempts table successfully!")
        
        # Check if exam_results table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='exam_results'")
        if not cursor.fetchone():
            print("Creating exam_results table...")
            cursor.execute('''
                CREATE TABLE exam_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    result_id VARCHAR(50) UNIQUE NOT NULL,
                    exam_id VARCHAR(50) NOT NULL,
                    attempt_id VARCHAR(50) NOT NULL,
                    student_username VARCHAR(50) NOT NULL,
                    marks_obtained INTEGER NOT NULL,
                    total_marks INTEGER NOT NULL,
                    percentage REAL NOT NULL,
                    grade VARCHAR(10) NOT NULL,
                    detailed_feedback TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (exam_id) REFERENCES mock_exams (exam_id),
                    FOREIGN KEY (attempt_id) REFERENCES exam_attempts (attempt_id)
                )
            ''')
            print("Created exam_results table successfully!")
        
        # Commit all changes
        conn.commit()
        print("Database migration completed successfully!")
        
        # Verify the final schema
        cursor.execute("PRAGMA table_info(mock_exams)")
        final_columns = [column[1] for column in cursor.fetchall()]
        print(f"Final mock_exams columns: {final_columns}")
        
        return True
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    print("Starting ByteCredits Database Migration...")
    print("=" * 50)
    
    success = migrate_database()
    
    print("=" * 50)
    if success:
        print("✅ Migration completed successfully!")
        print("You can now use the mock exam feature.")
    else:
        print("❌ Migration failed!")
        print("Please check the error messages above and try again.")
