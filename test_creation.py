#!/usr/bin/env python3
# Test script to create MyAwesomeProject

import sys
import os
import json
import shutil
from pathlib import Path

def create_test_project():
    """Create test project manually based on config"""
    
    # Project setup
    project_name = "MyAwesomeProject"
    project_path = Path("/home/herb/Desktop") / project_name
    
    # Remove existing project if it exists
    if project_path.exists():
        print(f"Removing existing project: {project_path}")
        shutil.rmtree(project_path)
    
    # Create project directory
    print(f"Creating project directory: {project_path}")
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Create PascalCase directories
    directories = ["Src", "Tests", "Docs", "Config", "Examples"]
    for dir_name in directories:
        dir_path = project_path / dir_name
        print(f"Creating directory: {dir_path}")
        dir_path.mkdir(exist_ok=True)
    
    # Copy requirements.txt (runtime only)
    req_src = Path("/home/herb/Desktop/Project_Startup/templates/files/requirements_basic.txt")
    req_dst = project_path / "requirements.txt"
    if req_src.exists():
        print(f"Copying requirements.txt from {req_src}")
        shutil.copy2(req_src, req_dst)
    
    # Copy requirements-dev.txt (development tools)
    req_dev_src = Path("/home/herb/Desktop/Project_Startup/templates/files/requirements_dev.txt")
    req_dev_dst = project_path / "requirements-dev.txt"
    if req_dev_src.exists():
        print(f"Copying requirements-dev.txt from {req_dev_src}")
        shutil.copy2(req_dev_src, req_dev_dst)
    
    # Initialize git repository
    try:
        os.chdir(project_path)
        os.system("git init")
        print("Git repository initialized")
    except Exception as e:
        print(f"Failed to initialize git: {e}")
    
    # Create virtual environment
    try:
        os.system("python3 -m venv .venv")
        print("Virtual environment created")
    except Exception as e:
        print(f"Failed to create virtual environment: {e}")
    
    print(f"✅ Project {project_name} created successfully!")
    return True

if __name__ == "__main__":
    create_test_project()