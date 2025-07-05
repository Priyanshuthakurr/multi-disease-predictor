#!/usr/bin/env python3
"""
Setup script for Smart Health Companion
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["data", "model", "utils"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")

def train_model():
    """Train the ML model"""
    print("🤖 Training machine learning model...")
    try:
        subprocess.check_call([sys.executable, "model/train_model.py"])
        print("✅ Model trained successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error training model: {e}")
        return False

def create_env_file():
    """Create .env file from example"""
    if not os.path.exists(".env"):
        if os.path.exists("env_example.txt"):
            shutil.copy("env_example.txt", ".env")
            print("📝 Created .env file from template")
            print("⚠️  Please edit .env file with your API keys")
        else:
            print("⚠️  No env_example.txt found, please create .env manually")
    else:
        print("✅ .env file already exists")

def main():
    """Main setup function"""
    print("🏥 Smart Health Companion - Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Train model
    if not train_model():
        print("⚠️  Model training failed, but you can still run the app")
    
    # Create environment file
    create_env_file()
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: streamlit run app.py")
    print("3. Open http://localhost:8501 in your browser")
    
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main() 