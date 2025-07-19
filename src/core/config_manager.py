# File: config_manager.py
# Path: Project_Startup/src/core/config_manager.py
# Standard: AIDEV-PascalCase-2.2
# Created: 2025-01-19
# Last Modified: 2025-01-19  09:18AM
"""
Description: Configuration management for Project_Startup - handles loading, saving, and validating project configurations
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple, List


class ConfigManager:
    """Manages configuration loading, saving, and validation for Project_Startup"""
    
    def __init__(self):
        """Initialize ConfigManager with default paths"""
        self.base_dir = Path(__file__).parent.parent.parent
        self.config_dir = self.base_dir / "config"
        self.templates_dir = self.base_dir / "templates" / "base_structure"
        self.project_configs_dir = self.base_dir / "project_configs"
        
        # Ensure directories exist
        self.project_configs_dir.mkdir(exist_ok=True)
    
    def load_base_config(self) -> Dict[str, Any]:
        """Load the base configuration template"""
        return self._load_json_file(self.config_dir / "default_config.json")
    
    def load_github_config(self) -> Dict[str, Any]:
        """Load GitHub configuration"""
        return self._load_json_file(self.config_dir / "github_config.json")
    
    def load_app_settings(self) -> Dict[str, Any]:
        """Load application settings"""
        return self._load_json_file(self.config_dir / "app_settings.json")
    
    def load_template_config(self, template_name: str) -> Dict[str, Any]:
        """Load a specific project template configuration"""
        template_file = self.templates_dir / f"{template_name}.json"
        
        if template_file.exists():
            template_config = self._load_json_file(template_file)
            base_config = self.load_base_config()
            return self.merge_configs(base_config, template_config)
        else:
            return self.load_base_config()
    
    def load_project_config(self, project_name: str) -> Dict[str, Any]:
        """Load saved configuration for a specific project"""
        config_file = self.project_configs_dir / f"{project_name}.json"
        
        if config_file.exists():
            return self._load_json_file(config_file)
        else:
            # Return base config if project config doesn't exist
            return self.load_base_config()
    
    def save_project_config(self, project_name: str, config: Dict[str, Any]) -> bool:
        """Save configuration for a specific project"""
        try:
            config_file = self.project_configs_dir / f"{project_name}.json"
            
            # Ensure project name is set in config
            if "project_info" not in config:
                config["project_info"] = {}
            config["project_info"]["name"] = project_name
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving project config: {e}")
            return False
    
    def get_available_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get list of available project templates"""
        templates = {}
        
        if not self.templates_dir.exists():
            return templates
        
        for template_file in self.templates_dir.glob("*.json"):
            template_name = template_file.stem
            template_config = self._load_json_file(template_file)
            templates[template_name] = template_config
        
        return templates
    
    def validate_config(self, config: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate configuration against required schema"""
        errors = []
        
        # Check required top-level sections
        required_sections = ["project_info", "structure", "files"]
        for section in required_sections:
            if section not in config:
                errors.append(f"Missing required section: {section}")
        
        # Validate project_info section
        if "project_info" in config:
            project_info = config["project_info"]
            required_fields = ["name", "author", "email"]
            
            for field in required_fields:
                if field not in project_info or not project_info[field]:
                    errors.append(f"Missing required project_info field: {field}")
        
        # Validate structure section
        if "structure" in config:
            structure = config["structure"]
            if "directories" not in structure:
                errors.append("Missing directories in structure section")
            elif not isinstance(structure["directories"], list):
                errors.append("Directories must be a list")
        
        # Validate files section
        if "files" in config:
            files = config["files"]
            if not isinstance(files, list):
                errors.append("Files section must be a list")
            else:
                for i, file_config in enumerate(files):
                    if not isinstance(file_config, dict):
                        errors.append(f"File config {i} must be a dictionary")
                    elif "name" not in file_config:
                        errors.append(f"File config {i} missing 'name' field")
        
        return len(errors) == 0, errors
    
    def merge_configs(self, base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge configuration with overrides"""
        merged = base_config.copy()
        
        for key, value in override_config.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self.merge_configs(merged[key], value)
            else:
                merged[key] = value
        
        return merged
    
    def _load_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Load JSON file with error handling"""
        try:
            if not file_path.exists():
                return {}
            
            with open(file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file {file_path}: {e}")
            raise
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return {}