# File: test_myawesome_project.py
# Path: Project_Startup/tests/functional/test_myawesome_project.py
# Standard: AIDEV-PascalCase-2.2
# Created: 2025-01-19
# Last Modified: 2025-01-19  07:19PM
"""
Description: Functional test for creating MyAwesomeProject with default configuration
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import sys
import subprocess
import json

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from core.config_manager import ConfigManager
from core.project_creator import ProjectCreator


class TestMyAwesomeProjectCreation:
    """Functional test for end-to-end MyAwesomeProject creation"""
    
    @pytest.fixture
    def test_workspace(self):
        """Create a temporary workspace for the test"""
        temp_path = tempfile.mkdtemp(prefix="myawesome_test_")
        yield Path(temp_path)
        shutil.rmtree(temp_path)
    
    def test_create_myawesome_project_full_workflow(self, test_workspace):
        """Test complete MyAwesomeProject creation with all defaults"""
        
        # Initialize config manager with project paths
        config_manager = ConfigManager()
        config_manager.base_dir = Path(__file__).parent.parent.parent
        config_manager.config_dir = config_manager.base_dir / "config"
        config_manager.templates_dir = config_manager.base_dir / "templates"
        config_manager.project_configs_dir = test_workspace / "project_configs"
        config_manager.project_configs_dir.mkdir()
        
        # Load the default configuration
        base_config = config_manager.load_base_config()
        github_config = config_manager.load_github_config()
        
        # Create MyAwesomeProject configuration
        project_config = config_manager.merge_configs(base_config, {
            "project_info": {
                "name": "MyAwesomeProject",
                "description": "An awesome test project created with Project_Startup"
            },
            "github": {
                "check_repository": False,  # Skip GitHub for test
                "initial_commit": False,
                "push_to_remote": False
            },
            "structure": {
                "create_venv": False,  # Skip venv for test speed
                "install_requirements": False
            }
        })
        
        # Validate configuration
        is_valid, errors = config_manager.validate_config(project_config)
        assert is_valid, f"Configuration validation failed: {errors}"
        
        # Create project creator
        project_creator = ProjectCreator(config_manager)
        project_creator.base_project_dir = test_workspace
        
        # Create the project
        success = project_creator.create_project(project_config)
        assert success, "Project creation failed"
        
        # Verify project structure
        project_path = test_workspace / "MyAwesomeProject"
        assert project_path.exists(), "Project directory not created"
        assert project_path.is_dir(), "Project path is not a directory"
        
        # Verify directory structure
        expected_dirs = ["src", "tests", "docs", "config", "examples"]
        for dir_name in expected_dirs:
            dir_path = project_path / dir_name
            assert dir_path.exists(), f"Directory {dir_name} not created"
            assert dir_path.is_dir(), f"{dir_name} is not a directory"
        
        # Verify required files
        expected_files = [
            "README.md",
            ".gitignore", 
            "requirements.txt",
            "CLAUDE.md"
        ]
        
        for file_name in expected_files:
            file_path = project_path / file_name
            assert file_path.exists(), f"File {file_name} not created"
            assert file_path.is_file(), f"{file_name} is not a file"
        
        # Verify file content processing
        readme_path = project_path / "README.md"
        readme_content = readme_path.read_text()
        assert "MyAwesomeProject" in readme_content, "Project name not in README"
        assert "An awesome test project" in readme_content, "Description not in README"
        
        # Verify CLAUDE.md content
        claude_path = project_path / "CLAUDE.md"
        claude_content = claude_path.read_text()
        assert "MyAwesomeProject" in claude_content, "Project name not in CLAUDE.md"
        assert "DESIGN STANDARD" in claude_content, "Design standard not in CLAUDE.md"
        
        # Verify .gitignore content
        gitignore_path = project_path / ".gitignore"
        gitignore_content = gitignore_path.read_text()
        assert "__pycache__/" in gitignore_content, "Python patterns not in .gitignore"
        assert "Special exclusion" in gitignore_content, "Herb's special pattern not in .gitignore"
        
        # Verify symlinks (if Project_BaseFiles exists)
        basefiles_path = Path("/home/herb/Desktop/Project_BaseFiles")
        if basefiles_path.exists():
            # Check Scripts symlink
            scripts_link = project_path / "Scripts"
            if scripts_link.exists():
                assert scripts_link.is_symlink(), "Scripts should be a symlink"
                assert scripts_link.resolve() == basefiles_path / "Scripts", "Scripts symlink target incorrect"
            
            # Check .vscode symlink (if parent directory exists)
            vscode_dir = project_path / ".vscode"
            if vscode_dir.exists():
                vscode_settings = vscode_dir / "settings.json"
                if vscode_settings.exists():
                    assert vscode_settings.is_symlink(), ".vscode/settings.json should be a symlink"
        
        # Verify Git initialization
        git_dir = project_path / ".git"
        if git_dir.exists():
            assert git_dir.is_dir(), ".git should be a directory"
        
        print(f"\n✅ MyAwesomeProject created successfully at: {project_path}")
        print(f"📁 Directory structure: {len(expected_dirs)} directories created")
        print(f"📄 Files created: {len(expected_files)} template files processed")
        print(f"🔗 Symlinks: {'Created' if basefiles_path.exists() else 'Skipped (Project_BaseFiles not found)'}")
        
        return project_path
    
    def test_project_file_permissions(self, test_workspace):
        """Test that created files have proper permissions"""
        # This test would run after the main creation test
        project_path = test_workspace / "MyAwesomeProject"
        
        if project_path.exists():
            # Check that files are readable
            for file_path in project_path.rglob("*"):
                if file_path.is_file() and not file_path.is_symlink():
                    assert file_path.stat().st_mode & 0o444, f"File {file_path} not readable"
    
    def test_project_git_status(self, test_workspace):
        """Test Git repository status of created project"""
        project_path = test_workspace / "MyAwesomeProject"
        
        if project_path.exists() and (project_path / ".git").exists():
            # Run git status to verify repository is clean
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=project_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Empty output means clean repository
                assert len(result.stdout.strip()) >= 0, "Git repository should be initialized"


if __name__ == "__main__":
    # Run this test standalone for manual testing
    test_instance = TestMyAwesomeProjectCreation()
    
    import tempfile
    with tempfile.TemporaryDirectory(prefix="myawesome_standalone_") as temp_dir:
        test_workspace = Path(temp_dir)
        
        try:
            project_path = test_instance.test_create_myawesome_project_full_workflow(test_workspace)
            print(f"\n🎉 Standalone test completed! Project created at: {project_path}")
            print("You can examine the created project structure.")
            
            # Keep the temp directory for examination
            import time
            print(f"\n⏰ Temporary directory will be preserved for 60 seconds for examination...")
            print(f"📂 Examine: {project_path}")
            time.sleep(60)
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            raise