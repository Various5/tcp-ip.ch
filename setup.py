#!/usr/bin/env python3
"""
NetworkHub.ch Setup Script
Automated setup for the comprehensive networking compendium
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def print_banner():
    """Display the NetworkHub.ch banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              🌐 NetworkHub.ch Setup 🌐                    ║
    ║                                                           ║
    ║        The Ultimate Networking Compendium                 ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible!")
    return True


def create_project_structure():
    """Create the required project directory structure"""
    print("📁 Creating project structure...")

    directories = [
        "templates",
        "static/css",
        "static/js",
        "static/images",
        "logs",
        "config"
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created: {directory}/")

    print("✅ Project structure created successfully!")


def setup_virtual_environment():
    """Set up Python virtual environment"""
    print("🐍 Setting up virtual environment...")

    venv_name = "networkenv"

    if os.path.exists(venv_name):
        print(f"   ℹ️  Virtual environment '{venv_name}' already exists")
        return True

    try:
        subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)
        print(f"   ✅ Virtual environment '{venv_name}' created")
        return True
    except subprocess.CalledProcessError:
        print("   ❌ Failed to create virtual environment")
        return False


def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")

    # Determine pip command based on platform
    if platform.system() == "Windows":
        pip_cmd = ["networkenv\\Scripts\\pip.exe"]
    else:
        pip_cmd = ["networkenv/bin/pip"]

    try:
        # Upgrade pip first
        subprocess.run(pip_cmd + ["install", "--upgrade", "pip"], check=True)

        # Install requirements
        subprocess.run(pip_cmd + ["install", "-r", "requirements.txt"], check=True)
        print("   ✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("   ❌ Failed to install dependencies")
        print("   💡 Try installing manually: pip install -r requirements.txt")
        return False


def create_env_file():
    """Create environment configuration file"""
    print("⚙️  Creating environment configuration...")

    env_content = """# NetworkHub.ch Environment Configuration
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
HOST=0.0.0.0
PORT=5000

# Production settings (uncomment for production)
# FLASK_ENV=production
# FLASK_DEBUG=False
# SECRET_KEY=your-production-secret-key

# Optional: Database configuration
# DATABASE_URL=sqlite:///networkHub.db

# Optional: External API keys
# MONITORING_API_KEY=your-api-key
# ANALYTICS_API_KEY=your-api-key
"""

    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("   ✅ Environment file (.env) created")
        return True
    except Exception as e:
        print(f"   ❌ Failed to create .env file: {e}")
        return False


def create_run_script():
    """Create convenient run scripts for different platforms"""
    print("🚀 Creating run scripts...")

    # Windows batch script
    windows_script = """@echo off
echo Starting NetworkHub.ch...
call networkenv\\Scripts\\activate
python app.py
pause
"""

    # Unix shell script
    unix_script = """#!/bin/bash
echo "Starting NetworkHub.ch..."
source networkenv/bin/activate
python app.py
"""

    try:
        # Create Windows script
        with open("run_networkHub.bat", "w") as f:
            f.write(windows_script)

        # Create Unix script
        with open("run_networkHub.sh", "w") as f:
            f.write(unix_script)

        # Make Unix script executable
        if platform.system() != "Windows":
            os.chmod("run_networkHub.sh", 0o755)

        print("   ✅ Run scripts created:")
        print("      - run_networkHub.bat (Windows)")
        print("      - run_networkHub.sh (Linux/Mac)")
        return True
    except Exception as e:
        print(f"   ❌ Failed to create run scripts: {e}")
        return False


def create_dockerfile():
    """Create Dockerfile for containerized deployment"""
    print("🐳 Creating Docker configuration...")

    dockerfile_content = """# NetworkHub.ch Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash networkuser
RUN chown -R networkuser:networkuser /app
USER networkuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \\
    CMD curl -f http://localhost:5000/ || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
"""

    docker_compose_content = """version: '3.8'

services:
  networkhub:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  # Optional: Add nginx reverse proxy
  # nginx:
  #   image: nginx:alpine
  #   ports:
  #     - "80:80"
  #   volumes:
  #     - ./nginx.conf:/etc/nginx/nginx.conf
  #   depends_on:
  #     - networkhub
"""

    try:
        with open("Dockerfile", "w") as f:
            f.write(dockerfile_content)

        with open("docker-compose.yml", "w") as f:
            f.write(docker_compose_content)

        print("   ✅ Docker configuration created:")
        print("      - Dockerfile")
        print("      - docker-compose.yml")
        return True
    except Exception as e:
        print(f"   ❌ Failed to create Docker files: {e}")
        return False


def display_success_message():
    """Display setup completion message with next steps"""
    print("\n" + "=" * 60)
    print("🎉 NetworkHub.ch Setup Complete! 🎉")
    print("=" * 60)
    print()
    print("📋 Next Steps:")
    print("   1. Activate virtual environment:")

    if platform.system() == "Windows":
        print("      networkenv\\Scripts\\activate")
    else:
        print("      source networkenv/bin/activate")

    print("   2. Start the application:")
    print("      python app.py")
    print("      OR use run script:")
    if platform.system() == "Windows":
        print("      run_networkHub.bat")
    else:
        print("      ./run_networkHub.sh")

    print("   3. Open your browser to:")
    print("      http://localhost:5000")
    print()
    print("🌐 Welcome to your comprehensive networking compendium!")
    print("📚 Explore 8 major sections covering every aspect of networking")
    print("🔧 Use 15+ interactive tools for hands-on learning")
    print("📊 Monitor real-time network statistics and performance")
    print()
    print("💡 For production deployment:")
    print("   - Update SECRET_KEY in .env file")
    print("   - Set FLASK_ENV=production")
    print("   - Use Docker: docker-compose up")
    print()
    print("📖 Check README.md for comprehensive documentation")
    print("🚀 Happy networking!")


def main():
    """Main setup function"""
    print_banner()

    # Check prerequisites
    if not check_python_version():
        sys.exit(1)

    # Setup steps
    steps = [
        ("Creating project structure", create_project_structure),
        ("Setting up virtual environment", setup_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Creating environment configuration", create_env_file),
        ("Creating run scripts", create_run_script),
        ("Creating Docker configuration", create_dockerfile)
    ]

    failed_steps = []

    for step_name, step_function in steps:
        try:
            if not step_function():
                failed_steps.append(step_name)
        except Exception as e:
            print(f"❌ Error in {step_name}: {e}")
            failed_steps.append(step_name)

    # Show results
    if failed_steps:
        print(f"\n⚠️  Setup completed with {len(failed_steps)} warnings:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\n💡 You can continue with manual setup for failed steps")

    display_success_message()


if __name__ == "__main__":
    main()