# File: test_main.py
# Path: Project_Startup/tests/unit/test_main.py
# Standard: AIDEV-PascalCase-2.2
# Created: 2025-01-19
# Last Modified: 2025-01-19  09:17AM
"""
Description: Unit tests for main.py argument parsing and CLI functionality
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from main import main, create_project_direct, launch_gui


class TestMainArgumentParsing:
    """Test suite for main.py argument parsing and CLI interface"""
    
    def test_main_with_positional_project_name(self):
        """Test main function with positional project name argument"""
        test_args = ["main.py", "MyTestProject"]
        
        with patch('sys.argv', test_args), \
             patch('main.create_project_direct', return_value=0) as mock_create:
            
            result = main()
            
            assert result == 0
            mock_create.assert_called_once()
            args = mock_create.call_args[0]
            assert args[0] == "MyTestProject"  # project name
            assert args[1] == "python_basic"  # default template
            assert args[2] == True  # github integration enabled
            assert args[3] == False  # not dry run
    
    def test_main_with_template_option(self):
        """Test main function with custom template"""
        test_args = ["main.py", "GuiProject", "--template", "python_gui"]
        
        with patch('sys.argv', test_args), \
             patch('main.create_project_direct', return_value=0) as mock_create:
            
            result = main()
            
            assert result == 0
            args = mock_create.call_args[0]
            assert args[0] == "GuiProject"
            assert args[1] == "python_gui"
    
    def test_main_with_no_github(self):
        """Test main function with --no-github flag"""
        test_args = ["main.py", "NoGitProject", "--no-github"]
        
        with patch('sys.argv', test_args), \
             patch('main.create_project_direct', return_value=0) as mock_create:
            
            result = main()
            
            assert result == 0
            args = mock_create.call_args[0]
            assert args[0] == "NoGitProject"
            assert args[2] == False  # github integration disabled
    
    def test_main_with_dry_run(self):
        """Test main function with --dry-run flag"""
        test_args = ["main.py", "DryRunProject", "--dry-run"]
        
        with patch('sys.argv', test_args), \
             patch('main.create_project_direct', return_value=0) as mock_create:
            
            result = main()
            
            assert result == 0
            args = mock_create.call_args[0]
            assert args[0] == "DryRunProject"
            assert args[3] == True  # dry run enabled
    
    def test_main_config_mode(self):
        """Test main function with --config flag"""
        test_args = ["main.py", "--config"]
        
        with patch('sys.argv', test_args), \
             patch('main.launch_config_editor', return_value=0) as mock_config, \
             patch('main.PYSIDE6_AVAILABLE', True):
            
            result = main()
            
            assert result == 0
            mock_config.assert_called_once()
    
    def test_main_config_mode_no_pyside6(self):
        """Test main function with --config flag when PySide6 not available"""
        test_args = ["main.py", "--config"]
        
        with patch('sys.argv', test_args), \
             patch('main.PYSIDE6_AVAILABLE', False), \
             patch('builtins.print') as mock_print:
            
            result = main()
            
            assert result == 1
            mock_print.assert_called()
            # Should print error about PySide6 requirement
    
    def test_main_gui_mode(self):
        """Test main function launching GUI when no project name provided"""
        test_args = ["main.py"]
        
        with patch('sys.argv', test_args), \
             patch('main.launch_gui', return_value=0) as mock_gui, \
             patch('main.PYSIDE6_AVAILABLE', True):
            
            result = main()
            
            assert result == 0
            mock_gui.assert_called_once()
    
    def test_main_gui_mode_no_pyside6(self):
        """Test main function GUI mode when PySide6 not available"""
        test_args = ["main.py"]
        
        with patch('sys.argv', test_args), \
             patch('main.PYSIDE6_AVAILABLE', False), \
             patch('builtins.print') as mock_print:
            
            result = main()
            
            assert result == 1
            mock_print.assert_called()
            # Should print error about PySide6 requirement
    
    def test_main_help_argument(self):
        """Test main function with --help argument"""
        test_args = ["main.py", "--help"]
        
        with patch('sys.argv', test_args):
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            # argparse exits with code 0 for help
            assert exc_info.value.code == 0


class TestCreateProjectDirect:
    """Test suite for create_project_direct function"""
    
    @patch('main.ProjectCreator')
    @patch('main.ConfigManager')
    def test_create_project_direct_success(self, mock_config_manager, mock_project_creator):
        """Test successful direct project creation"""
        # Setup mocks
        mock_config_instance = MagicMock()
        mock_config_manager.return_value = mock_config_instance
        
        mock_creator_instance = MagicMock()
        mock_creator_instance.create_project.return_value = True
        mock_project_creator.return_value = mock_creator_instance
        
        mock_config_instance.load_template_config.return_value = {
            "project_info": {"name": ""},
            "github": {"enabled": False}
        }
        
        # Test function
        result = create_project_direct("TestProject", "python_basic", True, False)
        
        assert result == 0
        mock_creator_instance.create_project.assert_called_once()
    
    @patch('main.ProjectCreator')
    @patch('main.ConfigManager')
    def test_create_project_direct_failure(self, mock_config_manager, mock_project_creator):
        """Test failed direct project creation"""
        # Setup mocks for failure
        mock_config_instance = MagicMock()
        mock_config_manager.return_value = mock_config_instance
        
        mock_creator_instance = MagicMock()
        mock_creator_instance.create_project.return_value = False
        mock_project_creator.return_value = mock_creator_instance
        
        mock_config_instance.load_template_config.return_value = {
            "project_info": {"name": ""},
            "github": {"enabled": False}
        }
        
        # Test function
        result = create_project_direct("TestProject", "python_basic", True, False)
        
        assert result == 1
    
    @patch('main.ProjectCreator')
    @patch('main.ConfigManager')
    def test_create_project_direct_dry_run(self, mock_config_manager, mock_project_creator):
        """Test dry run mode"""
        # Setup mocks
        mock_config_instance = MagicMock()
        mock_config_manager.return_value = mock_config_instance
        
        mock_creator_instance = MagicMock()
        mock_project_creator.return_value = mock_creator_instance
        
        mock_config_instance.load_template_config.return_value = {
            "project_info": {"name": ""},
            "github": {"enabled": False}
        }
        
        # Test dry run
        result = create_project_direct("TestProject", "python_basic", True, True)
        
        assert result == 0
        mock_creator_instance.preview_project.assert_called_once()
        mock_creator_instance.create_project.assert_not_called()
    
    @patch('main.ProjectCreator')
    @patch('main.ConfigManager')
    def test_create_project_direct_exception(self, mock_config_manager, mock_project_creator):
        """Test exception handling in direct project creation"""
        # Setup mocks to raise exception
        mock_config_manager.side_effect = Exception("Test error")
        
        with patch('builtins.print') as mock_print:
            result = create_project_direct("TestProject", "python_basic", True, False)
            
            assert result == 1
            mock_print.assert_called()


class TestLaunchGui:
    """Test suite for launch_gui function"""
    
    @patch('main.QApplication')
    @patch('main.MainWindow')
    def test_launch_gui_success(self, mock_main_window, mock_qapp):
        """Test successful GUI launch"""
        # Setup mocks
        mock_app_instance = MagicMock()
        mock_app_instance.exec.return_value = 0
        mock_qapp.return_value = mock_app_instance
        
        mock_window_instance = MagicMock()
        mock_main_window.return_value = mock_window_instance
        
        # Test function
        result = launch_gui()
        
        assert result == 0
        mock_qapp.assert_called_once()
        mock_main_window.assert_called_once()
        mock_window_instance.show.assert_called_once()
        mock_app_instance.exec.assert_called_once()
    
    @patch('main.QApplication')
    def test_launch_gui_app_properties(self, mock_qapp):
        """Test that GUI application properties are set correctly"""
        mock_app_instance = MagicMock()
        mock_app_instance.exec.return_value = 0
        mock_qapp.return_value = mock_app_instance
        
        with patch('main.MainWindow'):
            launch_gui()
            
            # Verify application properties were set
            mock_app_instance.setApplicationName.assert_called_with("Project_Startup")
            mock_app_instance.setApplicationVersion.assert_called_with("1.0")
            mock_app_instance.setOrganizationName.assert_called_with("Project Himalaya")
            mock_app_instance.setOrganizationDomain.assert_called_with("HimalayaProject1@gmail.com")


class TestCommandLineIntegration:
    """Integration tests for command line usage"""
    
    def test_help_message_content(self, capsys):
        """Test that help message contains expected information"""
        test_args = ["main.py", "--help"]
        
        with patch('sys.argv', test_args):
            with pytest.raises(SystemExit):
                main()
        
        captured = capsys.readouterr()
        help_output = captured.out
        
        # Verify help contains key information
        assert "Project_Startup" in help_output
        assert "newproj MyProject" in help_output
        assert "python Project_Startup" in help_output
        assert "--config" in help_output
        assert "--template" in help_output
        assert "--no-github" in help_output
        assert "--dry-run" in help_output
    
    def test_argument_parsing_edge_cases(self):
        """Test edge cases in argument parsing"""
        
        # Test with empty project name
        test_args = ["main.py", ""]
        
        with patch('sys.argv', test_args), \
             patch('main.create_project_direct', return_value=0) as mock_create:
            
            main()
            
            # Should still call create_project_direct with empty string
            mock_create.assert_called_once()
            assert mock_create.call_args[0][0] == ""
    
    def test_multiple_argument_combinations(self):
        """Test various argument combinations"""
        combinations = [
            (["main.py", "Project1", "--template", "python_gui", "--no-github"], 
             "Project1", "python_gui", False),
            (["main.py", "Project2", "--dry-run", "--template", "python_basic"], 
             "Project2", "python_basic", True),
        ]
        
        for test_args, expected_name, expected_template, expected_dry_run in combinations:
            with patch('sys.argv', test_args), \
                 patch('main.create_project_direct', return_value=0) as mock_create:
                
                main()
                
                args = mock_create.call_args[0]
                assert args[0] == expected_name
                assert args[1] == expected_template
                assert args[3] == expected_dry_run