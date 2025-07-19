# File: conftest.py
# Path: Project_Startup/tests/conftest.py
# Standard: AIDEV-PascalCase-2.2
# Created: 2025-01-19
# Last Modified: 2025-01-19  09:13AM
"""
Description: Pytest configuration and shared fixtures for Project_Startup testing
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import json
import sys
import os

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.config_manager import ConfigManager
from core.project_creator import ProjectCreator


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def temp_project_dir(temp_dir):
    """Create a temporary project directory"""
    project_path = temp_dir / "TestProject"
    project_path.mkdir()
    yield project_path


@pytest.fixture
def mock_config():
    """Sample configuration for testing"""
    return {
        "project_info": {
            "name": "TestProject",
            "description": "A test project",
            "author": "Test Author",
            "email": "test@example.com",
            "license": "MIT"
        },
        "structure": {
            "directories": ["src", "tests", "docs"],
            "create_venv": False,  # Skip venv for tests
            "python_version": "3.11",
            "install_requirements": False
        },
        "files": [
            {
                "name": "README.md",
                "template": "README_template.md",
                "required": True
            },
            {
                "name": ".gitignore",
                "template": "gitignore_python.txt",
                "required": True
            }
        ],
        "symlinks": [],
        "github": {
            "check_repository": False,  # Skip GitHub for tests
            "initial_commit": False,
            "push_to_remote": False
        }
    }


@pytest.fixture
def mock_github_config():
    """Sample GitHub configuration for testing"""
    return {
        "account": {
            "username": "TestUser",
            "email": "test@example.com",
            "ssh_key_path": "~/.ssh/test_rsa",
            "personal_access_token": "",
            "api_base_url": "https://api.github.com"
        },
        "authentication": {
            "method": "ssh",
            "fallback_to_pat": True,
            "pat_token_env_var": "GITHUB_PAT"
        }
    }


@pytest.fixture
def config_manager(temp_dir, mock_config, mock_github_config):
    """Create a ConfigManager with test data"""
    
    # Create test config directory structure
    config_dir = temp_dir / "config"
    config_dir.mkdir()
    
    # Write test configs
    with open(config_dir / "default_config.json", "w") as f:
        json.dump(mock_config, f, indent=2)
    
    with open(config_dir / "github_config.json", "w") as f:
        json.dump(mock_github_config, f, indent=2)
    
    # Create ConfigManager with test directory
    manager = ConfigManager()
    manager.base_dir = temp_dir
    manager.config_dir = config_dir
    manager.project_configs_dir = temp_dir / "project_configs"
    manager.project_configs_dir.mkdir()
    
    return manager


@pytest.fixture
def project_creator(config_manager, temp_dir):
    """Create a ProjectCreator with test configuration"""
    creator = ProjectCreator(config_manager)
    creator.base_project_dir = temp_dir
    return creator


@pytest.fixture
def sample_template_files(temp_dir):
    """Create sample template files for testing"""
    templates_dir = temp_dir / "templates" / "files"
    templates_dir.mkdir(parents=True)
    
    # README template
    readme_content = """# File: README_template.md
# Path: Project_Startup/templates/files/README_template.md
# Standard: AIDEV-PascalCase-2.2
# Created: 2025-01-19
# Last Modified: 2025-01-19  09:13AM

# {{project_name}}

{{description}}

## Overview
This is a test project.
"""
    
    with open(templates_dir / "README_template.md", "w") as f:
        f.write(readme_content)
    
    # .gitignore template
    gitignore_content = """# File: gitignore_python.txt
# Standard: AIDEV-PascalCase-2.2

# Python
__pycache__/
*.py[cod]
*$py.class

# Special exclusion for directories starting with '..' (Herb's pattern)
..*/
"""
    
    with open(templates_dir / "gitignore_python.txt", "w") as f:
        f.write(gitignore_content)
    
    return templates_dir