# File: project_creator.py
# Path: Project_Startup/src/core/project_creator.py
# Standard: AIDEV-PascalCase-2.2
# Created: 2025-01-19
# Last Modified: 2025-01-19  09:19AM
"""
Description: Project creation engine for Project_Startup - handles all aspects of creating new projects
"""

import os
import shutil
import subprocess
import re
from pathlib import Path
from typing import Dict, Any, Tuple, List
from datetime import datetime

from .config_manager import ConfigManager


class ProjectCreator:
    """Handles the creation of new projects with all necessary files and structure"""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize ProjectCreator with configuration manager"""
        self.config_manager = config_manager
        self.base_project_dir = Path.home() / "Desktop"
        self.templates_dir = config_manager.base_dir / "templates" / "files"
        self.shared_resources_dir = config_manager.base_dir / "shared_resources"
    
    def validate_project_name(self, name: str) -> Tuple[bool, str]:
        """Validate project name according to standards"""
        if not name:
            return False, "Project name cannot be empty"
        
        if len(name) < 2:
            return False, "Project name must be at least 2 characters long"
        
        if len(name) > 50:
            return False, "Project name must be 50 characters or less"
        
        # Check for valid characters (letters, numbers, hyphens, underscores)
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', name):
            return False, "Project name must start with a letter and contain only letters, numbers, hyphens, and underscores"
        
        return True, None
    
    def create_project(self, config: Dict[str, Any]) -> bool:
        """Create a complete project based on configuration"""
        try:
            project_name = config["project_info"]["name"]
            project_path = self.base_project_dir / project_name
            
            print(f"🚀 Creating project: {project_name}")
            print(f"📁 Location: {project_path}")
            
            # Validate project name
            is_valid, error = self.validate_project_name(project_name)
            if not is_valid:
                print(f"❌ Invalid project name: {error}")
                return False
            
            # Check if project already exists
            if project_path.exists():
                print(f"⚠️ Project directory already exists: {project_path}")
                return False
            
            # Create project directory
            project_path.mkdir(parents=True)
            print(f"✅ Created project directory")
            
            # Create directory structure
            if not self.create_directory_structure(project_path, config["structure"]["directories"]):
                return False
            
            # Process template variables
            template_vars = self._prepare_template_variables(config)
            
            # Copy and process template files
            if not self.copy_template_files(project_path, config["files"], template_vars):
                return False
            
            # Create symlinks
            if "symlinks" in config and config["symlinks"]:
                if not self.create_symlinks(project_path, config["symlinks"]):
                    return False
            
            # Initialize Git if requested
            if config.get("git", {}).get("initialize", False):
                if not self.initialize_git(project_path):
                    print("⚠️ Git initialization failed, but continuing...")
                    
            # Create initial commit if requested
            if config.get("git", {}).get("initial_commit", False) or config.get("github", {}).get("initial_commit", False):
                if not self.create_initial_commit(project_path):
                    print("⚠️ Initial commit failed, but continuing...")
            
            # Create virtual environment if requested
            if config["structure"].get("create_venv", False):
                if not self.create_virtual_environment(project_path):
                    print("⚠️ Virtual environment creation failed, but continuing...")
            
            # Install requirements if requested
            if config["structure"].get("install_requirements", False):
                if not self.install_requirements(project_path):
                    print("⚠️ Requirements installation failed, but continuing...")
            
            print(f"🎉 Project {project_name} created successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error creating project: {e}")
            return False
    
    def preview_project(self, config: Dict[str, Any]) -> None:
        """Preview what would be created without actually creating it"""
        project_name = config["project_info"]["name"]
        project_path = self.base_project_dir / project_name
        
        print(f"🔍 PREVIEW: Project '{project_name}'")
        print(f"📁 Would be created at: {project_path}")
        print()
        
        print("📂 Directory structure:")
        for directory in config["structure"]["directories"]:
            print(f"  📁 {directory}/")
        print()
        
        print("📄 Files to be created:")
        for file_config in config["files"]:
            required = "✅" if file_config.get("required", False) else "⭕"
            print(f"  {required} {file_config['name']} (from {file_config['template']})")
        print()
        
        if "symlinks" in config and config["symlinks"]:
            print("🔗 Symlinks to be created:")
            for symlink in config["symlinks"]:
                print(f"  🔗 {symlink['target']} -> {symlink['source']}")
            print()
        
        print("⚙️ Configuration:")
        print(f"  🐍 Python version: {config['structure'].get('python_version', 'default')}")
        print(f"  📦 Create venv: {config['structure'].get('create_venv', False)}")
        print(f"  🔧 Install requirements: {config['structure'].get('install_requirements', False)}")
        print(f"  🌐 GitHub integration: {config.get('github', {}).get('initial_commit', False)}")
    
    def create_directory_structure(self, project_path: Path, directories: List[str]) -> bool:
        """Create the directory structure for the project"""
        try:
            print("📂 Creating directory structure...")
            
            for directory in directories:
                dir_path = project_path / directory
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"  📁 Created: {directory}/")
            
            return True
        except Exception as e:
            print(f"❌ Error creating directories: {e}")
            return False
    
    def copy_template_files(self, project_path: Path, files_config: List[Dict[str, Any]], template_vars: Dict[str, str]) -> bool:
        """Copy and process template files"""
        try:
            print("📄 Processing template files...")
            
            for file_config in files_config:
                file_name = file_config["name"]
                template_name = file_config["template"]
                
                template_path = self.templates_dir / template_name
                output_path = project_path / file_name
                
                if not template_path.exists():
                    print(f"⚠️ Template not found: {template_name}")
                    if file_config.get("required", False):
                        return False
                    continue
                
                if not self.process_template_file(template_path, output_path, template_vars):
                    if file_config.get("required", False):
                        return False
                
                print(f"  📄 Created: {file_name}")
            
            return True
        except Exception as e:
            print(f"❌ Error processing template files: {e}")
            return False
    
    def process_template_file(self, template_path: Path, output_path: Path, variables: Dict[str, str]) -> bool:
        """Process a single template file with variable substitution"""
        try:
            # Read template content
            content = template_path.read_text()
            
            # Replace template variables
            for var_name, var_value in variables.items():
                placeholder = f"{{{{{var_name}}}}}"
                content = content.replace(placeholder, var_value)
            
            # Update header with current timestamp if it's a template header
            if content.startswith("# File:"):
                lines = content.split('\n')
                if len(lines) > 4 and "Last Modified:" in lines[4]:
                    current_time = datetime.now().strftime("%Y-%m-%d  %I:%M%p")
                    lines[4] = f"# Last Modified: {current_time}"
                    content = '\n'.join(lines)
            
            # Write processed content
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(content)
            
            return True
        except Exception as e:
            print(f"❌ Error processing template {template_path}: {e}")
            return False
    
    def create_symlinks(self, project_path: Path, symlinks_config: List[Dict[str, Any]]) -> bool:
        """Create symlinks to shared resources"""
        try:
            print("🔗 Creating symlinks...")
            
            for symlink_config in symlinks_config:
                source = symlink_config["source"]
                target = symlink_config["target"]
                
                # Resolve source path
                if not source.startswith("/"):
                    source_path = self.shared_resources_dir / source
                else:
                    source_path = Path(source)
                
                target_path = project_path / target
                
                if not source_path.exists():
                    print(f"⚠️ Symlink source not found: {source}")
                    continue
                
                # Create parent directories if needed
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Remove existing file/link if it exists
                if target_path.exists() or target_path.is_symlink():
                    if target_path.is_dir() and not target_path.is_symlink():
                        shutil.rmtree(target_path)
                    else:
                        target_path.unlink()
                
                # Create symlink
                os.symlink(source_path, target_path)
                print(f"  🔗 Linked: {target} -> {source}")
            
            return True
        except Exception as e:
            print(f"❌ Error creating symlinks: {e}")
            return False
    
    def initialize_git(self, project_path: Path) -> bool:
        """Initialize Git repository"""
        try:
            print("🌐 Initializing Git repository...")
            
            # Initialize git repo
            result = subprocess.run(
                ["git", "init"],
                cwd=project_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"❌ Git init failed: {result.stderr}")
                return False
            
            print("  ✅ Git repository initialized")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing Git: {e}")
            return False
    
    def create_initial_commit(self, project_path: Path) -> bool:
        """Create initial Git commit"""
        try:
            print("📝 Creating initial commit...")
            
            # Add all files
            result = subprocess.run(
                ["git", "add", "."],
                cwd=project_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"❌ Git add failed: {result.stderr}")
                return False
            
            # Create initial commit
            result = subprocess.run(
                ["git", "commit", "-m", "Initial commit - Project created with Project_Startup"],
                cwd=project_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"❌ Git commit failed: {result.stderr}")
                return False
                
            print("  ✅ Initial commit created")
            return True
            
        except Exception as e:
            print(f"❌ Error creating initial commit: {e}")
            return False
    
    def create_virtual_environment(self, project_path: Path) -> bool:
        """Create Python virtual environment"""
        try:
            print("🐍 Creating virtual environment...")
            
            venv_path = project_path / ".venv"
            
            result = subprocess.run(
                ["python", "-m", "venv", str(venv_path)],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"❌ Virtual environment creation failed: {result.stderr}")
                return False
            
            print("  ✅ Virtual environment created")
            return True
            
        except Exception as e:
            print(f"❌ Error creating virtual environment: {e}")
            return False
    
    def install_requirements(self, project_path: Path) -> bool:
        """Install requirements from requirements.txt"""
        try:
            requirements_file = project_path / "requirements.txt"
            
            if not requirements_file.exists():
                print("⚠️ No requirements.txt found, skipping installation")
                return True
            
            print("📦 Installing requirements...")
            
            # Use venv pip if available, otherwise system pip
            venv_pip = project_path / ".venv" / "bin" / "pip"
            pip_command = str(venv_pip) if venv_pip.exists() else "pip"
            
            result = subprocess.run(
                [pip_command, "install", "-r", str(requirements_file)],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"❌ Requirements installation failed: {result.stderr}")
                return False
            
            print("  ✅ Requirements installed")
            return True
            
        except Exception as e:
            print(f"❌ Error installing requirements: {e}")
            return False
    
    def _prepare_template_variables(self, config: Dict[str, Any]) -> Dict[str, str]:
        """Prepare template variables for substitution"""
        project_info = config["project_info"]
        
        variables = {
            "project_name": project_info["name"],
            "description": project_info.get("description", ""),
            "author": project_info.get("author", ""),
            "email": project_info.get("email", ""),
            "license": project_info.get("license", "MIT"),
            "creation_date": datetime.now().strftime("%Y-%m-%d"),
            "github_username": config.get("github", {}).get("username", ""),
            "project_type": config.get("project_type", "Python Application")
        }
        
        return variables