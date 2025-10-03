#!/usr/bin/env python3
"""
Database initialization script
Creates the database tables and populates with sample data
"""

import sys
import os
from datetime import datetime, timedelta

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.models.task import Task
from app.core.security import get_password_hash

# Create database engine directly with SQLite
DATABASE_URL = "sqlite:///./task_manager.db"
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize the database with sample data"""
    print("🚀 Initializing database...")
    
    # Create all tables (this is handled by Alembic migrations, but we can ensure they exist)
    from app.core.database import Base
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_users = db.query(User).first()
        if existing_users:
            print("✅ Database already contains data. Skipping initialization.")
            return
        
        print("📝 Creating sample users...")
        
        # Create sample users
        users_data = [
            {
                "email": "admin@taskmanager.com",
                "username": "admin",
                "hashed_password": get_password_hash("admin123"),
                "full_name": "Administrator",
                "is_active": True,
                "is_superuser": True
            },
            {
                "email": "john.doe@example.com",
                "username": "johndoe",
                "hashed_password": get_password_hash("password123"),
                "full_name": "John Doe",
                "is_active": True,
                "is_superuser": False
            },
            {
                "email": "jane.smith@example.com",
                "username": "janesmith",
                "hashed_password": get_password_hash("password123"),
                "full_name": "Jane Smith",
                "is_active": True,
                "is_superuser": False
            }
        ]
        
        created_users = []
        for user_data in users_data:
            user = User(**user_data)
            db.add(user)
            db.flush()  # Flush to get the ID
            created_users.append(user)
        
        db.commit()
        print(f"✅ Created {len(created_users)} users")
        
        print("📋 Creating sample tasks...")
        
        # Create sample tasks
        tasks_data = [
            {
                "title": "Complete project documentation",
                "description": "Write comprehensive documentation for the Task Manager API project",
                "is_completed": False,
                "priority": "high",
                "due_date": datetime.now() + timedelta(days=7),
                "owner_id": created_users[0].id  # Admin user
            },
            {
                "title": "Review code changes",
                "description": "Review all recent code changes and provide feedback",
                "is_completed": True,
                "priority": "medium",
                "due_date": datetime.now() - timedelta(days=1),
                "owner_id": created_users[0].id  # Admin user
            },
            {
                "title": "Setup development environment",
                "description": "Configure local development environment for new team members",
                "is_completed": False,
                "priority": "high",
                "due_date": datetime.now() + timedelta(days=3),
                "owner_id": created_users[1].id  # John Doe
            },
            {
                "title": "Design user interface mockups",
                "description": "Create wireframes and mockups for the frontend application",
                "is_completed": False,
                "priority": "medium",
                "due_date": datetime.now() + timedelta(days=14),
                "owner_id": created_users[2].id  # Jane Smith
            },
            {
                "title": "Write unit tests",
                "description": "Add comprehensive unit tests for all API endpoints",
                "is_completed": False,
                "priority": "high",
                "due_date": datetime.now() + timedelta(days=5),
                "owner_id": created_users[1].id  # John Doe
            },
            {
                "title": "Database optimization",
                "description": "Optimize database queries and add proper indexing",
                "is_completed": False,
                "priority": "low",
                "due_date": datetime.now() + timedelta(days=21),
                "owner_id": created_users[2].id  # Jane Smith
            }
        ]
        
        for task_data in tasks_data:
            task = Task(**task_data)
            db.add(task)
        
        db.commit()
        print(f"✅ Created {len(tasks_data)} tasks")
        
        print("\n🎉 Database initialization completed successfully!")
        print("\n📊 Sample data created:")
        print(f"   👥 Users: {len(created_users)}")
        print(f"   📋 Tasks: {len(tasks_data)}")
        print("\n🔑 Default credentials:")
        print("   Admin: admin@taskmanager.com / admin123")
        print("   User: john.doe@example.com / password123")
        print("   User: jane.smith@example.com / password123")
        print("\n🌐 You can now test the API at: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def reset_db():
    """Reset the database (drop all tables and recreate)"""
    print("⚠️  Resetting database...")
    
    # Drop all tables
    from app.core.database import Base
    Base.metadata.drop_all(bind=engine)
    print("🗑️  Dropped all tables")
    
    # Recreate tables
    Base.metadata.create_all(bind=engine)
    print("🔨 Recreated all tables")
    
    # Initialize with sample data
    init_db()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database initialization script")
    parser.add_argument(
        "--reset", 
        action="store_true", 
        help="Reset the database (drop and recreate all tables)"
    )
    
    args = parser.parse_args()
    
    if args.reset:
        reset_db()
    else:
        init_db()
