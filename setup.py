"""
Setup script for Story Chat Interface
Run this script after installation to prepare the environment
"""

import os
import sys
from pathlib import Path
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_ollama():
    """Check if Ollama is installed and running"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✅ Ollama is installed and running")
            print("   Available models:")
            for line in result.stdout.split('\n')[1:]:
                if line.strip():
                    print(f"   - {line.split()[0]}")
            return True
        else:
            print("⚠️  Ollama is installed but not running")
            print("   Run: ollama serve")
            return False
    except FileNotFoundError:
        print("❌ Ollama is not installed")
        print("   Install from: https://ollama.ai")
        return False
    except Exception as e:
        print(f"⚠️  Could not check Ollama: {str(e)}")
        return False

def check_ollama_model(model_name="llama3.2"):
    """Check if required Ollama model is available"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if model_name in result.stdout:
            print(f"✅ Model '{model_name}' is available")
            return True
        else:
            print(f"⚠️  Model '{model_name}' not found")
            print(f"   Run: ollama pull {model_name}")
            return False
    except Exception as e:
        print(f"⚠️  Could not check model: {str(e)}")
        return False

def create_directories():
    """Create required directories"""
    dirs = [
        "data",
        "data/pdfs",
        "data/vectordb"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✅ Created data directories")
    return True

def check_pdf_files():
    """Check if any PDF files are present"""
    pdf_dir = Path("data/pdfs")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if pdf_files:
        print(f"✅ Found {len(pdf_files)} PDF file(s):")
        for pdf in pdf_files:
            print(f"   - {pdf.name}")
        return True
    else:
        print("⚠️  No PDF files found in data/pdfs/")
        print("   Please add your story PDF files to this directory")
        return False

def install_dependencies():
    """Install Python dependencies"""
    try:
        print("\n📦 Installing Python dependencies...")
        print("   This may take several minutes...\n")
        
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print("❌ Error installing dependencies")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Main setup routine"""
    print("=" * 60)
    print("📚 Story Chat Interface - Setup Script")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version()),
        ("Create Directories", create_directories()),
        ("Ollama Installation", check_ollama()),
        ("Ollama Model", check_ollama_model()),
        ("PDF Files", check_pdf_files())
    ]
    
    print("\n" + "=" * 60)
    print("Setup Summary:")
    print("=" * 60)
    
    all_passed = True
    for name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {name}")
        if not passed and name in ["Python Version", "Create Directories"]:
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("✅ Setup complete! You can now run the application:")
        print("   python main.py")
    else:
        print("⚠️  Some checks failed. Please resolve the issues above.")
        print("\nCommon fixes:")
        print("  • Ollama not installed → Visit https://ollama.ai")
        print("  • Ollama not running → Run: ollama serve")
        print("  • Model missing → Run: ollama pull llama3.2")
        print("  • No PDFs → Add PDF files to data/pdfs/")
    
    print("=" * 60)
    
    # Ask if user wants to install dependencies
    if all_passed:
        response = input("\nInstall Python dependencies now? (y/n): ")
        if response.lower() == 'y':
            install_dependencies()

if __name__ == "__main__":
    main()
