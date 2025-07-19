# File: test_create_myawesomeproject.py
# Path: Project_Startup/tests/functional/test_create_myawesomeproject.py
# Standard: AIDEV-PascalCase-2.2
# Created: 2025-01-19
# Last Modified: 2025-01-19  09:16AM
"""
Description: Functional test for creating 'MyAwesomeProject' end-to-end
"""

import pytest
import subprocess
import sys
from pathlib import Path
import json
import shutil


class TestCreateMyAwesomeProject:
    """Functional test suite for complete project creation workflow"""
    
    def test_create_myawesomeproject_cli(self, temp_dir):
        """Test creating MyAwesomeProject via CLI interface"""
        
        # Setup test environment
        project_name = "MyAwesomeProject"
        expected_project_path = temp_dir / project_name
        
        # Create test configuration
        test_config = {
            "project_info": {
                "name": project_name,
                "description": "An awesome test project created by Project_Startup",
                "author": "Herb Bowers",
                "email": "HimalayaProject1@gmail.com",
                "license": "MIT"
            },
            "structure": {
                "directories": [
                    "src",
                    "tests", 
                    "docs",
                    "config",
                    "examples"
                ],
                "create_venv": False,  # Skip for testing
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
                },
                {
                    "name": "requirements.txt",
                    "template": "requirements_basic.txt", 
                    "required": True
                },
                {
                    "name": "CLAUDE.md",
                    "template": "claude_template.md",
                    "required": True
                }
            ],
            "symlinks": [],
            "github": {
                "check_repository": False,  # Skip for testing
                "initial_commit": False,
                "push_to_remote": False
            },
            "integrations": {
                "link_to_project_basefiles": False,  # Skip for testing
                "inherit_design_standards": True
            }
        }
        
        # Create test templates
        self._create_test_templates(temp_dir)
        
        # Mock the main.py execution
        from src.main import create_project_direct
        from core.config_manager import ConfigManager
        from core.project_creator import ProjectCreator
        
        # Setup test config manager
        config_manager = ConfigManager()
        config_manager.config_dir = temp_dir / "config"
        config_manager.config_dir.mkdir()
        
        # Save test config
        with open(config_manager.config_dir / "default_config.json", "w") as f:
            json.dump(test_config, f, indent=2)
        
        # Create project creator with test settings
        project_creator = ProjectCreator(config_manager)
        project_creator.base_project_dir = temp_dir
        project_creator.templates_dir = temp_dir / "templates" / "files"
        
        # Execute project creation
        result = project_creator.create_project(test_config)
        
        # Verify project creation succeeded
        assert result == True, "Project creation should succeed"
        
        # Verify project directory exists
        assert expected_project_path.exists(), f"Project directory should exist at {expected_project_path}"
        assert expected_project_path.is_dir(), "Project path should be a directory"
        
        # Verify directory structure
        expected_dirs = test_config["structure"]["directories"]
        for dir_name in expected_dirs:
            dir_path = expected_project_path / dir_name
            assert dir_path.exists(), f"Directory '{dir_name}' should exist"
            assert dir_path.is_dir(), f"'{dir_name}' should be a directory"
        
        # Verify files were created
        expected_files = [file_config["name"] for file_config in test_config["files"]]
        for file_name in expected_files:
            file_path = expected_project_path / file_name
            assert file_path.exists(), f"File '{file_name}' should exist"
            assert file_path.is_file(), f"'{file_name}' should be a file"
        
        # Verify file contents
        self._verify_file_contents(expected_project_path, project_name)
        
        # Verify Design Standard v2.2 compliance
        self._verify_design_standard_compliance(expected_project_path)
    
    def test_create_myawesomeproject_with_git(self, temp_dir):
        """Test creating MyAwesomeProject with Git initialization"""
        
        project_name = "MyAwesomeProject"
        expected_project_path = temp_dir / project_name
        
        # Create test configuration with Git enabled
        test_config = self._get_base_config(project_name)
        test_config["github"]["initial_commit"] = True
        
        # Setup test environment
        self._create_test_templates(temp_dir)
        config_manager = self._setup_config_manager(temp_dir, test_config)
        
        # Create project creator
        project_creator = ProjectCreator(config_manager)
        project_creator.base_project_dir = temp_dir
        project_creator.templates_dir = temp_dir / "templates" / "files"
        
        # Mock Git operations for testing
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            result = project_creator.create_project(test_config)
            
            assert result == True
            assert expected_project_path.exists()
            
            # Verify Git commands were called
            git_calls = [call for call in mock_run.call_args_list 
                        if 'git' in str(call)]
            assert len(git_calls) > 0, "Git commands should have been executed"
    
    def test_create_myawesomeproject_with_venv(self, temp_dir):
        """Test creating MyAwesomeProject with virtual environment"""
        
        project_name = "MyAwesomeProject"
        expected_project_path = temp_dir / project_name
        
        # Create test configuration with venv enabled
        test_config = self._get_base_config(project_name)
        test_config["structure"]["create_venv"] = True
        
        # Setup test environment
        self._create_test_templates(temp_dir)
        config_manager = self._setup_config_manager(temp_dir, test_config)
        
        # Create project creator
        project_creator = ProjectCreator(config_manager)
        project_creator.base_project_dir = temp_dir
        project_creator.templates_dir = temp_dir / "templates" / "files"
        
        # Mock venv creation for testing
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            result = project_creator.create_project(test_config)
            
            assert result == True
            assert expected_project_path.exists()
            
            # Verify venv directory would be created
            # (Actual venv creation mocked to avoid test environment issues)
            venv_calls = [call for call in mock_run.call_args_list 
                         if 'venv' in str(call) or 'virtualenv' in str(call)]
            assert len(venv_calls) > 0, "Virtual environment commands should have been executed"
    
    def test_create_myawesomeproject_error_handling(self, temp_dir):
        """Test error handling during MyAwesomeProject creation"""
        
        project_name = "MyAwesomeProject"
        
        # Create test configuration
        test_config = self._get_base_config(project_name)
        
        # Setup test environment
        self._create_test_templates(temp_dir)
        config_manager = self._setup_config_manager(temp_dir, test_config)
        
        # Create project creator
        project_creator = ProjectCreator(config_manager)
        project_creator.base_project_dir = temp_dir
        project_creator.templates_dir = temp_dir / "templates" / "files"
        
        # Test with invalid project directory (read-only)
        readonly_dir = temp_dir / "readonly"
        readonly_dir.mkdir()
        readonly_dir.chmod(0o444)  # Read-only
        
        project_creator.base_project_dir = readonly_dir
        
        try:
            result = project_creator.create_project(test_config)
            # Should handle the error gracefully
            assert result == False, "Should return False when unable to create project"
        finally:
            # Restore permissions for cleanup
            readonly_dir.chmod(0o755)
    
    def test_myawesomeproject_compliance_check(self, temp_dir):
        """Test that MyAwesomeProject meets all Design Standard v2.2 requirements"""
        
        project_name = "MyAwesomeProject"
        expected_project_path = temp_dir / project_name
        
        # Create project
        test_config = self._get_base_config(project_name)
        self._create_test_templates(temp_dir)
        config_manager = self._setup_config_manager(temp_dir, test_config)
        
        project_creator = ProjectCreator(config_manager)
        project_creator.base_project_dir = temp_dir
        project_creator.templates_dir = temp_dir / "templates" / "files"
        
        result = project_creator.create_project(test_config)
        assert result == True
        
        # Comprehensive compliance check
        compliance_issues = []
        
        # Check all Python files for proper headers
        for py_file in expected_project_path.rglob("*.py"):
            issues = self._check_file_compliance(py_file)
            compliance_issues.extend(issues)
        
        # Check all Markdown files for proper headers
        for md_file in expected_project_path.rglob("*.md"):
            issues = self._check_file_compliance(md_file)
            compliance_issues.extend(issues)
        
        # Report compliance issues
        if compliance_issues:
            pytest.fail(f"Design Standard v2.2 compliance issues found:\n" + 
                       "\n".join(compliance_issues))
    
    # Helper methods
    
    def _get_base_config(self, project_name):
        """Get base configuration for testing"""
        return {
            "project_info": {
                "name": project_name,
                "description": "An awesome test project created by Project_Startup",
                "author": "Herb Bowers",
                "email": "HimalayaProject1@gmail.com",
                "license": "MIT"
            },
            "structure": {
                "directories": ["src", "tests", "docs", "config", "examples"],
                "create_venv": False,
                "python_version": "3.11",
                "install_requirements": False
            },
            "files": [
                {"name": "README.md", "template": "README_template.md", "required": True},
                {"name": ".gitignore", "template": "gitignore_python.txt", "required": True},
                {"name": "requirements.txt", "template": "requirements_basic.txt", "required": True},
                {"name": "CLAUDE.md", "template": "claude_template.md", "required": True}
            ],
            "symlinks": [],
            "github": {"check_repository": False, "initial_commit": False, "push_to_remote": False}
        }
    
    def _create_test_templates(self, temp_dir):
        """Create test template files"""
        templates_dir = temp_dir / "templates" / "files"
        templates_dir.mkdir(parents=True)
        
        # README template
        readme_template = '''# File: README_template.md
# Path: Project_Startup/templates/files/README_template.md
# Standard: AIDEV-PascalCase-2.2
# Created: 2025-01-19
# Last Modified: 2025-01-19  09:16AM
"""
Description: Template for generating README.md files in new projects created by Project_Startup
"""

# {{project_name}}

{{description}}

## Overview

This project was created using Project_Startup and follows the AIDEV-PascalCase-2.2 design standard.

## Author

{{author}}
{{email}}
'''
        
        with open(templates_dir / "README_template.md", "w") as f:
            f.write(readme_template)
        
        # .gitignore template
        gitignore_template = '''# File: gitignore_python.txt
# Path: Project_Startup/templates/files/gitignore_python.txt
# Standard: AIDEV-PascalCase-2.2
# Created: 2025-01-19
# Last Modified: 2025-01-19  09:16AM

# Python
__pycache__/
*.py[cod]
*$py.class

# Special exclusion for directories starting with '..' (Herb's pattern)
..*/
'''
        
        with open(templates_dir / "gitignore_python.txt", "w") as f:
            f.write(gitignore_template)
        
        # Requirements template
        requirements_template = '''# File: requirements_basic.txt
# Path: Project_Startup/templates/files/requirements_basic.txt
# Standard: AIDEV-PascalCase-2.2
# Created: 2025-01-19
# Last Modified: 2025-01-19  09:16AM

# Core dependencies
pathlib
requests
pytest
'''
        
        with open(templates_dir / "requirements_basic.txt", "w") as f:
            f.write(requirements_template)
        
        # CLAUDE.md template
        claude_template = '''# File: claude_template.md
# Path: Project_Startup/templates/files/claude_template.md
# Standard: AIDEV-PascalCase-2.2
# Created: 2025-01-19
# Last Modified: 2025-01-19  09:16AM

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚨 DESIGN STANDARD v2.2 COMPLIANCE ACKNOWLEDGED 🚨

## Project Overview

{{description}}

## Author

{{author}}
'''
        
        with open(templates_dir / "claude_template.md", "w") as f:
            f.write(claude_template)
    
    def _setup_config_manager(self, temp_dir, test_config):
        """Setup ConfigManager with test configuration"""
        from core.config_manager import ConfigManager
        
        config_manager = ConfigManager()
        config_manager.config_dir = temp_dir / "config"
        config_manager.config_dir.mkdir()
        
        with open(config_manager.config_dir / "default_config.json", "w") as f:
            json.dump(test_config, f, indent=2)
        
        return config_manager
    
    def _verify_file_contents(self, project_path, project_name):
        """Verify that generated files have correct content"""
        
        # Check README.md
        readme_path = project_path / "README.md"
        readme_content = readme_path.read_text()
        assert project_name in readme_content
        assert "Herb Bowers" in readme_content
        assert "AIDEV-PascalCase-2.2" in readme_content
        
        # Check .gitignore
        gitignore_path = project_path / ".gitignore"
        gitignore_content = gitignore_path.read_text()
        assert "__pycache__/" in gitignore_content
        assert "../*" in gitignore_content  # Herb's pattern
        
        # Check CLAUDE.md
        claude_path = project_path / "CLAUDE.md"
        claude_content = claude_path.read_text()
        assert "DESIGN STANDARD v2.2 COMPLIANCE" in claude_content
        assert "Herb Bowers" in claude_content
    
    def _verify_design_standard_compliance(self, project_path):
        """Verify Design Standard v2.2 compliance"""
        
        # Check for proper file headers in generated files
        for file_path in project_path.rglob("*.md"):
            content = file_path.read_text()
            lines = content.split('\n')
            
            # Should have proper header format
            if len(lines) > 5:
                assert lines[0].startswith("# File:")
                assert lines[1].startswith("# Path:")
                assert lines[2].startswith("# Standard:")
                assert "AIDEV-PascalCase-2.2" in lines[2]
                assert lines[3].startswith("# Created:")
                assert lines[4].startswith("# Last Modified:")
    
    def _check_file_compliance(self, file_path):
        """Check individual file for Design Standard compliance"""
        issues = []
        
        try:
            content = file_path.read_text()
            lines = content.split('\n')
            
            if len(lines) < 5:
                issues.append(f"{file_path}: File too short for proper header")
                return issues
            
            # Check header format
            if not lines[0].startswith("# File:"):
                issues.append(f"{file_path}: Missing '# File:' header line")
            
            if not lines[1].startswith("# Path:"):
                issues.append(f"{file_path}: Missing '# Path:' header line")
            
            if not lines[2].startswith("# Standard:"):
                issues.append(f"{file_path}: Missing '# Standard:' header line")
            
            if "AIDEV-PascalCase-2.2" not in lines[2]:
                issues.append(f"{file_path}: Incorrect standard version")
            
            # Check for placeholder timestamps
            header_text = '\n'.join(lines[:10])
            if "HH:MM" in header_text or "XX:XX" in header_text:
                issues.append(f"{file_path}: Contains placeholder timestamps")
            
        except Exception as e:
            issues.append(f"{file_path}: Error reading file - {e}")
        
        return issues


# Import required for mocking
from unittest.mock import patch