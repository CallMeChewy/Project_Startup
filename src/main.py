#!/usr/bin/env python3
# File: main.py
# Path: /home/herb/Desktop/Project_Startup/src/main.py
# Standard: AIDEV-PascalCase-2.1
# Created: 2025-01-19
# Last Modified: 2025-01-19  09:09AM
"""
Description: Main entry point for Project_Startup - handles CLI arguments and launches GUI
"""

import sys
import argparse
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from PySide6.QtWidgets import QApplication
    from gui.main_window import MainWindow
    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False
    print("⚠️ PySide6 not installed. GUI features disabled.")
    print("Install with: pip install PySide6")

from core.project_creator import ProjectCreator
from core.config_manager import ConfigManager


def main():
    """Main entry point for Project_Startup application"""
    
    parser = argparse.ArgumentParser(
        description="Project_Startup - Comprehensive project initialization system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  newproj MyProject                 Create project directly (preferred)
  newproj --projectname MyProject    Create project with explicit flag
  newproj                           Open GUI to enter project name  
  newproj --config                  Open configuration editor
  python Project_Startup            Direct Python execution
  Project_Startup MyProject         Python with project name

For more information, see: /home/herb/Desktop/Project_Startup/README.md
        """
    )
    
    parser.add_argument(
        'projectname',
        nargs='?',
        type=str,
        help='Name of the project to create'
    )
    
    parser.add_argument(
        '--config',
        action='store_true',
        help='Open configuration editor GUI'
    )
    
    parser.add_argument(
        '--template',
        type=str,
        default='python_basic',
        help='Project template to use (default: python_basic)'
    )
    
    parser.add_argument(
        '--no-github',
        action='store_true',
        help='Skip GitHub integration'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be created without actually creating it'
    )
    
    args = parser.parse_args()
    
    # Handle configuration editor
    if args.config:
        if not PYSIDE6_AVAILABLE:
            print("❌ Configuration editor requires PySide6")
            print("Install with: pip install PySide6")
            return 1
        
        launch_config_editor()
        return 0
    
    # Determine project name from positional or flag argument
    project_name = args.projectname
    
    # Handle direct project creation
    if project_name:
        return create_project_direct(
            project_name,
            args.template,
            not args.no_github,
            args.dry_run
        )
    
    # Launch GUI for interactive project creation
    if not PYSIDE6_AVAILABLE:
        print("❌ GUI requires PySide6. Use --projectname for CLI mode.")
        print("Install PySide6 with: pip install PySide6")
        return 1
    
    return launch_gui()


def create_project_direct(project_name, template, github_integration, dry_run):
    """Create project directly from command line"""
    
    print(f"🚀 Creating project: {project_name}")
    print(f"📋 Template: {template}")
    print(f"🌐 GitHub integration: {'enabled' if github_integration else 'disabled'}")
    
    if dry_run:
        print("🔍 DRY RUN MODE - No files will be created")
    
    try:
        # Initialize managers
        config_manager = ConfigManager()
        project_creator = ProjectCreator(config_manager)
        
        # Load configuration
        config = config_manager.load_template_config(template)
        config['project_info']['name'] = project_name
        config['github']['enabled'] = github_integration
        
        # Create project
        if dry_run:
            project_creator.preview_project(config)
        else:
            success = project_creator.create_project(config)
            if success:
                print(f"✅ Project {project_name} created successfully!")
                print(f"📁 Location: ~/Desktop/{project_name}")
                return 0
            else:
                print(f"❌ Failed to create project {project_name}")
                return 1
                
    except Exception as e:
        print(f"❌ Error creating project: {e}")
        return 1
    
    return 0


def launch_gui():
    """Launch the GUI interface"""
    
    print("🖥️ Launching Project_Startup GUI...")
    
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Project_Startup")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Project Himalaya")
    app.setOrganizationDomain("HimalayaProject1@gmail.com")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    return app.exec()


def launch_config_editor():
    """Launch the configuration editor"""
    
    print("⚙️ Launching Configuration Editor...")
    
    app = QApplication(sys.argv)
    
    # Set application properties  
    app.setApplicationName("Project_Startup Config Editor")
    app.setApplicationVersion("1.0")
    
    # TODO: Create configuration editor window
    # from gui.config_editor import ConfigEditor
    # editor = ConfigEditor()
    # editor.show()
    
    print("⚠️ Configuration editor not yet implemented")
    print("📝 Manually edit files in: /home/herb/Desktop/Project_Startup/config/")
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)