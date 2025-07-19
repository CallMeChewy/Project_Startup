# File: README.md

# Path: /home/herb/Desktop/Project_Startup/README.md

# Standard: AIDEV-PascalCase-2.1

# Created: 2025-01-19

# Last Modified: 2025-01-19  09:04AM

"""
Description: Main documentation for Project_Startup - comprehensive project initialization system
"""

# Project_Startup

**Comprehensive project initialization system with GUI interface, GitHub integration, and symlink-based shared resources.**

*A Product of the Project Himalaya Ecosystem*

## 🏔️ Project Himalaya

**Project_Startup** is proudly developed by the **Project Himalaya** team - pioneers in AI-assisted software development. This tool embodies our commitment to bridging human creativity with artificial intelligence to create enterprise-grade development solutions.

## 🎯 Overview

Project_Startup revolutionizes project creation by providing:

- **CLI + GUI Interface**: `newproj --projectname` or interactive GUI
- **GitHub Integration**: Smart repository detection and management
- **Configuration Management**: JSON-based templates with inheritance
- **Symlink Architecture**: Shared resources across projects
- **Design Standard Compliance**: Automatic AIDEV-PascalCase-2.1 enforcement

## 🚀 Quick Start

### Installation

```bash
# Install from any terminal (hardcoded path in bashrc)
bash /home/herb/Desktop/Project_Startup/scripts/install.sh
```

### Usage

```bash
# Primary usage patterns
newproj MyAwesomeProject             # Direct project creation (preferred)
newproj MyAwesomeProject             # Alternative syntax
newproj --projectname MyAwesomeProject  # Explicit flag syntax

# GUI and configuration
newproj                              # Open GUI to enter project name
newproj --help                       # Show help
newproj --config                     # Open configuration editor

# Python direct startup alternatives
python Project_Startup              # Direct Python execution
Project_Startup MyAwesomeProject    # Python with project name
```

## 🏗️ Architecture

### Core Components

- **Src/**: Main application code (GUI, CoreLogic, Utilities)
- **Config/**: Configuration files (defaults, GitHub, app settings)
- **Templates/**: Project templates (structures, files, symlinks)
- **ProjectConfigs/**: Saved per-project configurations
- **SharedResources/**: Files for symlinking to projects
- **Scripts/**: Installation and utility scripts

### Project Creation Flow

1. **GitHub Check**: Verify repository existence and status
2. **Configuration**: Select/customize project template
3. **Structure Creation**: Build directory tree and copy files
4. **Symlink Setup**: Link to shared resources
5. **Git Initialization**: Setup version control
6. **Virtual Environment**: Create and configure Python venv
7. **GitHub Integration**: Initial commit and push (optional)

## 🎛️ Configuration System

### Configuration Hierarchy

1. **Base Configuration**: `config/default_config.json`
2. **Template Configurations**: `templates/base_structure/*.json`  
3. **Per-Project Configs**: `project_configs/{project_name}.json`
4. **User Override**: Real-time GUI modifications

### Special Features

- **"***" Admin Mode**: Hidden option to edit default configurations
- **GitHub Repository States**: Smart handling of existing repos
- **Dangerous "Redo" Operation**: Repository recreation with confirmations

## 🔗 GitHub Integration

### Repository Detection

- Checks if `CallMeChewy/{projectname}` exists
- Displays status and determines available options
- Handles three states: non-existent, exists without commits, exists with commits

### Dangerous Operations

```
If repo has commits:
1. Popup: "Repository has existing commits!"
2. Input: "Type 'redo' to recreate repository"  
3. Confirmation: "Type 'YES' to delete all history"
4. Action: Complete repository recreation
```

## 🎨 GUI Interface (PySide6)

### Main Window Features

- **Project Name Entry** with real-time GitHub checking
- **Configuration Dropdown** with template selection
- **Project Structure** checkboxes for directories/files
- **Symlink Management** with shared resource linking
- **GitHub Options** for commit/push operations
- **Progress Indicators** for all operations

### Safety Features

- **Input Validation** for project names and paths
- **Confirmation Dialogs** for dangerous operations
- **Progress Feedback** with detailed status updates
- **Error Recovery** with rollback capabilities

## 🔧 Templates

### Available Templates

- **python_basic.json**: Standard Python project
- **python_gui.json**: PySide6 GUI application
- **Custom Templates**: Add your own project types

### Template Components

- **Directory Structure**: Configurable folder hierarchy
- **File Templates**: README, .gitignore, requirements.txt, CLAUDE.md
- **Symlink Targets**: Connections to shared resources
- **Settings**: Python version, venv creation, dependencies

### File Generation Rules
- **Missing README**: User can craft one interactively with optional AI assistance
- **Existing Files**: Never replace unless they are symlinks
- **Symlinked Files**: Can be replaced/updated as they point to shared resources

## 🔗 Integration with Project_BaseFiles

### Symlink Connections

```bash
# Typical project links to shared infrastructure
{project}/scripts/ -> ~/Desktop/Project_BaseFiles/Scripts/
{project}/.vscode/ -> ~/Desktop/Project_BaseFiles/Config/VSCode/
{project}/docs/standards/ -> ~/Desktop/Project_BaseFiles/Docs/Standards/
```

### Design Standard Enforcement

- All generated files include proper AIDEV-PascalCase-2.1 headers
- Progressive timestamps across all created files
- Path verification matching deployment reality
- Automatic compliance with Project Himalaya ecosystem

## 🛡️ Safety & Security

### File Operations

- **Backup Before Changes**: Preserve existing files
- **Path Validation**: Prevent directory traversal
- **Symlink Verification**: Ensure target existence
- **Configuration Validation**: JSON schema compliance

### GitHub Operations

- **SSH Key Management**: Secure authentication with SSH keys
- **Personal Access Token (PAT)**: Alternative authentication when SSH unavailable
- **Repository Verification**: Existence checking
- **Commit Validation**: Proper message formatting
- **Push Confirmation**: User approval required

## 📋 Development Commands

### Testing

```bash
# Run from Project_Startup directory
python -m pytest tests/

# Run with coverage
python -m pytest --cov=src tests/
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/
```

### Manual Testing

```bash
# Test CLI directly
python src/main.py --projectname TestProject

# Test GUI
python src/main.py
```

## 🔄 Workflow Integration

### VS Code Integration

- Projects automatically get shared VS Code settings
- Tasks for common operations pre-configured
- Extensions and formatting rules inherited

### Project Himalaya Ecosystem

- Seamless integration with existing toolchain
- Shared script access via symlinks
- Consistent design standards across all projects

## 🚨 Design Standard v2.1 Compliance

**This project strictly follows Design Standard v2.1:**

- ✅ All files have proper headers with actual timestamps
- ✅ Progressive timestamps showing creation sequence  
- ✅ File paths match actual deployment locations
- ✅ PascalCase naming for Python files and directories
- ✅ Specific descriptions (no generic text)

## 📈 Future Enhancements

### Planned Features

- **Plugin System**: Custom project type extensions
- **Team Templates**: Shared configuration repositories
- **CI/CD Integration**: Automated pipeline setup
- **Docker Support**: Container-based development
- **Multi-Language**: Support for non-Python projects

### Integration Opportunities

- **VS Code Extension**: Direct IDE integration
- **GitHub Actions**: Workflow template generation
- **Cloud Deployment**: Automated hosting setup

## 🎯 Success Metrics

### Functional Goals

- ✅ Sub-10 second project creation
- ✅ Zero manual file copying
- ✅ 100% Design Standard compliance
- ✅ Seamless GitHub integration

### User Experience

- ✅ Single command operation
- ✅ Visual progress feedback
- ✅ Clear error messages
- ✅ No documentation required

---

## 🏔️ Project Himalaya Team

### Core Contributors
- **Herb Bowers** - Lead Architect & Vision  
  *HimalayaProject1@gmail.com*
- **Claude (Anthropic)** - AI Development Partner
- **Project Himalaya Community** - Contributors & Innovation

### Our Mission
*"Bridging the gap between human creativity and artificial intelligence to build the future of software development."*

### Recognition
Project_Startup exemplifies the Project Himalaya philosophy of:
- **Human-AI Collaboration**: Purpose-built for AI-assisted development
- **Standards Excellence**: AIDEV-PascalCase-2.1 compliance
- **Developer Productivity**: Eliminating repetitive setup tasks
- **Ecosystem Integration**: Seamless shared resource management

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Project Himalaya Development Team

---

*Created with Project_Startup following Design Standard v2.2*  
*Generated by the Project Himalaya AI-Human Collaborative Development System*