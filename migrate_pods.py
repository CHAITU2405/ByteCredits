#!/usr/bin/env python3
"""
Database migration script for Learning Pods feature
Creates all necessary tables for the learning pods functionality
"""

import os
import sys
from datetime import datetime

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import (LearningPod, PodMembership, StudentProfile, PodTask, 
                   TaskSubmission, MeritBadge, CollaborationEvent)

def create_pods_tables():
    """Create all learning pods related tables"""
    try:
        print("Creating learning pods tables...")
        
        with app.app_context():
            # Create all tables
            db.create_all()
            
            print("✅ Successfully created learning pods tables:")
            print("   - learning_pods")
            print("   - pod_memberships") 
            print("   - student_profiles")
            print("   - pod_tasks")
            print("   - task_submissions")
            print("   - merit_badges")
            print("   - collaboration_events")
            
            print("\n🎉 Learning Pods feature is ready to use!")
            print("\nNext steps:")
            print("1. Start the Flask application: python app.py")
            print("2. Login as teacher/admin to create learning pods")
            print("3. Students can access pods from their dashboard")
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    
    return True

def verify_tables():
    """Verify that all tables were created successfully"""
    try:
        with app.app_context():
            # Check if tables exist
            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            required_tables = [
                'learning_pods',
                'pod_memberships', 
                'student_profiles',
                'pod_tasks',
                'task_submissions',
                'merit_badges',
                'collaboration_events'
            ]
            
            missing_tables = [table for table in required_tables if table not in existing_tables]
            
            if missing_tables:
                print(f"❌ Missing tables: {missing_tables}")
                return False
            else:
                print("✅ All learning pods tables verified successfully!")
                return True
                
    except Exception as e:
        print(f"❌ Error verifying tables: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Learning Pods Database Migration")
    print("=" * 50)
    
    if create_pods_tables():
        if verify_tables():
            print("\n✨ Migration completed successfully!")
        else:
            print("\n⚠️  Migration completed with warnings.")
    else:
        print("\n💥 Migration failed!")
        sys.exit(1)
