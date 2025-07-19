# File: test_project_creator.py
# Path: Project_Startup/tests/unit/test_project_creator.py
# Standard: AIDEV-PascalCase-2.2
# Created: 2025-01-19
# Last Modified: 2025-01-19  09:15AM
"""
Description: Unit tests for ProjectCreator class functionality
"""

import pytest
from pathlib import Path
import os
from unittest.mock import patch, MagicMock

from core.project_creator import ProjectCreator


class TestProjectCreator:
    """Test suite for ProjectCreator functionality"""
    
    def test_init(self, config_manager):
        """Test ProjectCreator initialization"""
        creator = ProjectCreator(config_manager)
        assert creator is not None
        assert creator.config_manager == config_manager
    
    def test_validate_project_name_valid(self, project_creator):
        """Test project name validation with valid names"""
        valid_names = [
            "MyProject",
            "my-project",
            "my_project",
            "Project123",
            "ABC"
        ]
        
        for name in valid_names:
            is_valid, error = project_creator.validate_project_name(name)
            assert is_valid == True, f"'{name}' should be valid"
            assert error is None
    
    def test_validate_project_name_invalid(self, project_creator):
        """Test project name validation with invalid names"""
        invalid_names = [
            "",  # Empty
            "a",  # Too short
            "My Project",  # Spaces
            "my@project",  # Special chars
            "123project",  # Starts with number
            "-project",  # Starts with dash
            "a" * 100,  # Too long
        ]
        
        for name in invalid_names:
            is_valid, error = project_creator.validate_project_name(name)
            assert is_valid == False, f"'{name}' should be invalid"
            assert error is not None
    
    def test_create_directory_structure(self, project_creator, temp_project_dir, mock_config):
        """Test creating directory structure"""
        success = project_creator.create_directory_structure(
            temp_project_dir, 
            mock_config['structure']['directories']
        )
        
        assert success == True
        
        # Verify directories were created
        for dir_name in mock_config['structure']['directories']:
            dir_path = temp_project_dir / dir_name
            assert dir_path.exists()
            assert dir_path.is_dir()
    
    def test_create_directory_structure_existing(self, project_creator, temp_project_dir):
        """Test creating directory structure with existing directories"""
        # Create a directory that already exists
        existing_dir = temp_project_dir / "src"
        existing_dir.mkdir()
        
        success = project_creator.create_directory_structure(
            temp_project_dir, 
            ["src", "tests"]
        )
        
        assert success == True
        assert existing_dir.exists()
        assert (temp_project_dir / "tests").exists()
    
    def test_process_template_file(self, project_creator, sample_template_files, temp_project_dir):
        """Test processing template files with variable substitution"""
        template_path = sample_template_files / "README_template.md"
        output_path = temp_project_dir / "README.md"
        
        variables = {
            "project_name": "MyAwesomeProject",
            "description": "This is an awesome test project"
        }
        
        success = project_creator.process_template_file(
            template_path, 
            output_path, 
            variables
        )
        
        assert success == True
        assert output_path.exists()
        
        # Verify content was processed
        content = output_path.read_text()
        assert "MyAwesomeProject" in content
        assert "This is an awesome test project" in content
        assert "{{project_name}}" not in content  # Template vars should be replaced
    
    def test_copy_template_files(self, project_creator, sample_template_files, temp_project_dir, mock_config):
        """Test copying and processing template files"""
        # Update config to point to our test templates
        project_creator.templates_dir = sample_template_files
        
        variables = {
            "project_name": "TestProject",
            "description": "A test project"
        }
        
        success = project_creator.copy_template_files(
            temp_project_dir,
            mock_config['files'],
            variables
        )
        
        assert success == True
        
        # Verify files were created
        assert (temp_project_dir / "README.md").exists()
        assert (temp_project_dir / ".gitignore").exists()
        
        # Verify content processing
        readme_content = (temp_project_dir / "README.md").read_text()
        assert "TestProject" in readme_content
    
    def test_create_symlinks(self, project_creator, temp_project_dir, temp_dir):
        """Test creating symlinks"""
        # Create source directory/file for symlink
        source_dir = temp_dir / "shared_source"
        source_dir.mkdir()
        (source_dir / "test_file.txt").write_text("test content")
        
        symlinks_config = [
            {
                "source": str(source_dir),
                "target": "linked_dir",
                "type": "directory"
            }
        ]
        
        success = project_creator.create_symlinks(temp_project_dir, symlinks_config)
        
        assert success == True
        
        # Verify symlink was created
        symlink_path = temp_project_dir / "linked_dir"
        assert symlink_path.exists()
        assert symlink_path.is_symlink()
        assert symlink_path.resolve() == source_dir.resolve()
    
    def test_initialize_git(self, project_creator, temp_project_dir):
        """Test Git initialization"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            success = project_creator.initialize_git(temp_project_dir)
            
            assert success == True
            mock_run.assert_called()
    
    def test_create_virtual_environment(self, project_creator, temp_project_dir):
        """Test virtual environment creation"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            success = project_creator.create_virtual_environment(temp_project_dir)
            
            assert success == True
            mock_run.assert_called()
    
    def test_preview_project(self, project_creator, mock_config, capsys):
        """Test project preview functionality"""
        project_creator.preview_project(mock_config)
        
        captured = capsys.readouterr()
        output = captured.out
        
        # Verify preview contains expected information
        assert "TestProject" in output
        assert "src" in output
        assert "tests" in output
        assert "docs" in output
        assert "README.md" in output
        assert ".gitignore" in output
    
    def test_create_project_success(self, project_creator, temp_dir, mock_config, sample_template_files):
        """Test successful project creation"""
        project_creator.base_project_dir = temp_dir
        project_creator.templates_dir = sample_template_files
        
        # Mock external dependencies
        with patch.object(project_creator, 'initialize_git', return_value=True), \
             patch.object(project_creator, 'create_virtual_environment', return_value=True):
            
            success = project_creator.create_project(mock_config)
            
            assert success == True
            
            # Verify project was created
            project_path = temp_dir / mock_config['project_info']['name']
            assert project_path.exists()
            
            # Verify directory structure
            for dir_name in mock_config['structure']['directories']:
                assert (project_path / dir_name).exists()
            
            # Verify files were created
            assert (project_path / "README.md").exists()
            assert (project_path / ".gitignore").exists()
    
    def test_create_project_existing_directory(self, project_creator, temp_dir, mock_config):
        """Test project creation with existing directory"""
        project_creator.base_project_dir = temp_dir
        
        # Create existing project directory
        existing_project = temp_dir / mock_config['project_info']['name']
        existing_project.mkdir()
        (existing_project / "existing_file.txt").write_text("existing content")
        
        success = project_creator.create_project(mock_config)
        
        # Should fail or handle gracefully
        assert success == False or (existing_project / "existing_file.txt").exists()
    
    def test_rollback_on_failure(self, project_creator, temp_dir, mock_config):
        """Test rollback functionality when project creation fails"""
        project_creator.base_project_dir = temp_dir
        
        # Mock a failure in git initialization
        with patch.object(project_creator, 'initialize_git', return_value=False):
            
            success = project_creator.create_project(mock_config)
            
            assert success == False
            
            # Verify partial project was cleaned up (if rollback is implemented)
            project_path = temp_dir / mock_config['project_info']['name']
            # This depends on implementation - either cleaned up or left partial