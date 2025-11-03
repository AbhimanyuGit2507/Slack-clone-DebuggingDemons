"""
Complete setup: Install dependencies, create database, seed data, and show results
"""
import subprocess
import sys
import os

print("="*80)
print("🚀 SLACK CLONE - COMPLETE SETUP")
print("="*80)
print()

# Change to project directory
project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)
print(f"📁 Working directory: {project_dir}")
print()

# Step 1: Install dependencies
print("="*80)
print("📦 STEP 1: Installing Dependencies")
print("="*80)
try:
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"], check=True)
    print("✅ Dependencies installed successfully")
except Exception as e:
    print(f"⚠️  Warning: {e}")
    print("Continuing anyway...")
print()

# Step 2: Run the seed script
print("="*80)
print("🌱 STEP 2: Creating and Seeding Database")
print("="*80)
try:
    subprocess.run([sys.executable, "test_seed.py"], check=True)
except Exception as e:
    print(f"❌ Error seeding database: {e}")
    sys.exit(1)
print()

# Step 3: Show database location
print("="*80)
print("✅ SETUP COMPLETE!")
print("="*80)
print()
print("📍 Database Location: data/slack_rl.db")
print()
print("📊 To view the database:")
print("   1. In VS Code Explorer, navigate to: slack-rl-clone/data/")
print("   2. Right-click on: slack_rl.db")
print("   3. Select: 'Open with SQLite Viewer'")
print()
print("🚀 To start the backend server:")
print("   Run: python -m uvicorn backend.main:app --reload --port 8000")
print()
print("📖 API Documentation will be at:")
print("   http://localhost:8000/docs")
print()
print("🔑 Test Login Credentials:")
print("   Email: sarah.johnson@company.com")
print("   Password: password123")
print()
print("="*80)
