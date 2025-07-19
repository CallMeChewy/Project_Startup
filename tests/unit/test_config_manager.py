# File: test_config_manager.py
# Path: Project_Startup/tests/unit/test_config_manager.py
# Standard: AIDEV-PascalCase-2.2
# Created: 2025-01-19
# Last Modified: 2025-01-19  09:14AM
"""
Description: Unit tests for ConfigManager class functionality
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, mock_open

from core.config_manager import ConfigManager


class TestConfigManager:
    """Test suite for ConfigManager functionality"""
    
    def test_init(self):
        """Test ConfigManager initialization"""
        manager = ConfigManager()
        assert manager is not None
        assert hasattr(manager, 'config_dir')
    
    def test_load_base_config(self, config_manager, mock_config):
        """Test loading base configuration"""
        config = config_manager.load_base_config()
        
        assert config is not None
        assert config['project_info']['author'] == 'Test Author'
        assert config['structure']['directories'] == ['src', 'tests', 'docs']
        assert config['github']['check_repository'] == False
    
    def test_load_github_config(self, config_manager, mock_github_config):
        """Test loading GitHub configuration"""
        config = config_manager.load_github_config()
        
        assert config is not None
        assert config['account']['username'] == 'TestUser'
        assert config['authentication']['method'] == 'ssh'
        assert config['authentication']['fallback_to_pat'] == True
    
    def test_validate_config_valid(self, config_manager, mock_config):
        """Test configuration validation with valid config"""
        is_valid, errors = config_manager.validate_config(mock_config)
        
        assert is_valid == True
        assert len(errors) == 0
    
    def test_validate_config_missing_required(self, config_manager):
        """Test configuration validation with missing required fields"""
        invalid_config = {
            "project_info": {
                "name": "TestProject"
                # Missing required fields
            }
        }
        
        is_valid, errors = config_manager.validate_config(invalid_config)
        
        assert is_valid == False
        assert len(errors) > 0
        assert any("author" in error.lower() for error in errors)
    
    def test_save_project_config(self, config_manager, temp_dir, mock_config):
        """Test saving project-specific configuration"""
        project_name = "MyTestProject"
        
        success = config_manager.save_project_config(project_name, mock_config)
        
        assert success == True
        
        # Verify file was created
        config_file = config_manager.config_dir.parent / "project_configs" / f"{project_name}.json"
        assert config_file.exists()
        
        # Verify content
        with open(config_file) as f:
            saved_config = json.load(f)
        
        assert saved_config['project_info']['name'] == project_name
    
    def test_load_project_config(self, config_manager, temp_dir, mock_config):
        """Test loading project-specific configuration"""
        project_name = "MyTestProject"
        
        # First save a config
        config_manager.save_project_config(project_name, mock_config)
        
        # Then load it
        loaded_config = config_manager.load_project_config(project_name)
        
        assert loaded_config is not None
        assert loaded_config['project_info']['name'] == project_name
        assert loaded_config['project_info']['author'] == mock_config['project_info']['author']
    
    def test_load_project_config_not_exists(self, config_manager):
        """Test loading non-existent project configuration"""
        loaded_config = config_manager.load_project_config("NonExistentProject")
        
        # Should return base config when project config doesn't exist
        assert loaded_config is not None
        assert loaded_config['project_info']['author'] == 'Test Author'
    
    def test_get_available_templates(self, config_manager, temp_dir):
        """Test getting available project templates"""
        # Create some template files
        templates_dir = temp_dir / "templates" / "base_structure"
        templates_dir.mkdir(parents=True)
        
        template1 = {
            "name": "Python Basic",
            "description": "Basic Python project"
        }
        
        template2 = {
            "name": "Python GUI",
            "description": "GUI application"
        }
        
        with open(templates_dir / "python_basic.json", "w") as f:
            json.dump(template1, f)
        
        with open(templates_dir / "python_gui.json", "w") as f:
            json.dump(template2, f)
        
        config_manager.templates_dir = templates_dir
        templates = config_manager.get_available_templates()
        
        assert len(templates) == 2
        assert "python_basic" in templates
        assert "python_gui" in templates
        assert templates["python_basic"]["name"] == "Python Basic"
    
    def test_merge_configs(self, config_manager, mock_config):
        """Test merging configuration with overrides"""
        overrides = {
            "project_info": {
                "name": "OverriddenProject",
                "description": "New description"
            },
            "structure": {
                "create_venv": True
            }
        }
        
        merged = config_manager.merge_configs(mock_config, overrides)
        
        # Check overridden values
        assert merged['project_info']['name'] == 'OverriddenProject'
        assert merged['project_info']['description'] == 'New description'
        assert merged['structure']['create_venv'] == True
        
        # Check preserved values
        assert merged['project_info']['author'] == mock_config['project_info']['author']
        assert merged['structure']['directories'] == mock_config['structure']['directories']
    
    def test_load_config_invalid_json(self, config_manager, temp_dir):
        """Test handling of invalid JSON in config files"""
        # Create invalid JSON file
        invalid_file = temp_dir / "invalid.json"
        invalid_file.write_text('{"invalid": json}')
        
        # Should raise JSONDecodeError since we re-raise it in the code
        with pytest.raises(json.JSONDecodeError):
            config_manager._load_json_file(invalid_file)
    
    def test_config_file_not_found(self, config_manager):
        """Test handling of missing config files"""
        config = config_manager._load_json_file("nonexistent.json")
        assert config == {}