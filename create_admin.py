from app import app, db
from models import Credentials
from werkzeug.security import generate_password_hash

def create_admin_user():
    with app.app_context():
        # Check if admin user already exists
        admin = db.session.execute(db.select(Credentials).filter_by(username='admin')).scalar()
        
        if admin:
            print("Admin user already exists!")
        else:
            # Create admin user
            admin_user = Credentials(
                username='admin',
                email='admin@bytecredits.com',
                password=generate_password_hash('admin123'),
                role='admin',
                credits=0
            )
            
            db.session.add(admin_user)
            print("Admin user created successfully!")
            print("Username: admin")
            print("Password: admin123")
        
        # Check if college user already exists
        college = db.session.execute(db.select(Credentials).filter_by(username='college')).scalar()
        
        if college:
            print("College user already exists!")
        else:
            # Create college user
            college_user = Credentials(
                username='college',
                email='college@bytecredits.com',
                password=generate_password_hash('college123'),
                role='college',
                credits=0
            )
            
            db.session.add(college_user)
            print("College user created successfully!")
            print("Username: college")
            print("Password: college123")
        
        db.session.commit()

if __name__ == '__main__':
    create_admin_user() 