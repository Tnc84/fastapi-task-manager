#!/usr/bin/env python3
"""
Simple database setup script
Runs Alembic migrations and initializes the database
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Task Manager Database")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("alembic.ini"):
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Run Alembic migrations
    if not run_command("alembic upgrade head", "Running database migrations"):
        print("❌ Migration failed. Please check your database configuration.")
        sys.exit(1)
    
    # Initialize database with sample data
    if not run_command("python init_db.py", "Initializing database with sample data"):
        print("❌ Database initialization failed.")
        sys.exit(1)
    
    print("\n🎉 Database setup completed successfully!")
    print("\n📝 Next steps:")
    print("   1. Start the server: python run.py")
    print("   2. Open Swagger UI: http://localhost:8000/docs")
    print("   3. Test the API endpoints")

if __name__ == "__main__":
    main()
