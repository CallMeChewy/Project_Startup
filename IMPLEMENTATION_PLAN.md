# File: IMPLEMENTATION_PLAN.md
# Path: /home/herb/Desktop/Project_Startup/IMPLEMENTATION_PLAN.md
# Standard: AIDEV-PascalCase-2.1
# Created: 2025-01-19
# Last Modified: 2025-01-19  08:53AM

# Project_Startup - Comprehensive Implementation Plan

## 🎯 Project Vision

**Ultimate Goal**: Create a robust, GUI-driven project initialization system that integrates with GitHub, manages configurations, and creates standardized project structures with symlink-based shared resources.

**Command**: `newproj --projectname` or `newproj` (GUI prompt)
**Interface**: PySide6 GUI with CLI launcher
**Integration**: GitHub API, Project_BaseFiles ecosystem, JSON configurations

---

## 🏗️ Architecture Overview

### Core Components

```
Project_Startup/
├── src/                           # Main application code
│   ├── main.py                   # Entry point & CLI argument handling
│   ├── gui/                      # PySide6 GUI components
│   │   ├── __init__.py
│   │   ├── main_window.py        # Primary GUI interface
│   │   ├── project_wizard.py     # Step-by-step project setup
│   │   ├── config_editor.py      # Configuration management UI
│   │   └── dialogs/              # Confirmation dialogs, popups
│   ├── core/                     # Business logic
│   │   ├── __init__.py
│   │   ├── project_creator.py    # Core project creation engine
│   │   ├── github_manager.py     # GitHub integration
│   │   ├── config_manager.py     # Configuration handling
│   │   ├── symlink_manager.py    # Symlink creation/management
│   │   └── template_engine.py    # Template processing
│   └── utils/                    # Utilities
│       ├── __init__.py
│       ├── file_operations.py    # File/directory operations
│       ├── validation.py         # Input validation
│       └── logging_config.py     # Logging setup
├── config/                       # Configuration files
│   ├── default_config.json       # Base configuration
│   ├── github_config.json        # GitHub account settings
│   └── app_settings.json         # Application preferences
├── templates/                    # Project templates
│   ├── base_structure/           # Directory structures
│   │   ├── python_basic.json    # Basic Python project
│   │   ├── python_web.json      # Web application
│   │   └── python_ml.json       # Machine learning project
│   ├── files/                   # Template files
│   │   ├── README_template.md
│   │   ├── gitignore_python.txt
│   │   ├── requirements_basic.txt
│   │   └── license_mit.txt
│   └── symlinks/                # Symlink targets
│       ├── shared_scripts/      # Common scripts
│       ├── shared_configs/      # Common configurations
│       └── shared_docs/         # Common documentation
├── project_configs/             # Per-project saved configurations
├── shared_resources/            # Shared files for symlinking
├── scripts/                     # Installation and utility scripts
│   ├── install.sh              # Install newproj command
│   └── newproj                 # CLI launcher script
├── requirements.txt
├── setup.py
└── README.md
```

---

## 🚀 Feature Specifications

### 1. Command Line Interface

#### Primary Command
```bash
newproj --projectname MyProject    # Direct project creation
newproj                           # GUI with project name prompt
newproj --help                    # Show help
newproj --config                  # Open configuration editor
```

#### Bash Integration
```bash
# Install creates alias in ~/.bashrc
alias newproj='/home/herb/Desktop/Project_Startup/scripts/newproj'
```

### 2. GitHub Integration

#### Repository Detection
- Check if `CallMeChewy/projectname` exists on GitHub
- Display status: "Repository exists" or "Repository not found"
- Determine available setup options based on existence

#### Repository States
1. **Repo doesn't exist**: Full setup, no GitHub operations
2. **Repo exists, no commits**: Setup + initial commit/push option
3. **Repo exists, has commits**: Show warning, offer "redo" option

#### Dangerous "Redo" Operation
```
If repo has commits:
1. Popup: "Repository has existing commits!"
2. Input box: "Type 'redo' to recreate repository"
3. Confirmation: "Type 'YES' to delete all history and recreate"
4. Action: Delete repo history, push new initial commit
```

### 3. Configuration Management

#### Configuration Hierarchy
1. **Base Configuration**: Default settings for all projects
2. **Template Configurations**: Pre-configured for specific project types
3. **Per-Project Configurations**: Custom settings saved as JSON
4. **User Override**: Real-time modifications during setup

#### Configuration Schema
```json
{
  "project_info": {
    "name": "",
    "description": "",
    "author": "Herb Bowers",
    "email": "HimalayaProject1@gmail.com",
    "license": "MIT"
  },
  "structure": {
    "directories": ["src", "tests", "docs", "config"],
    "create_venv": true,
    "python_version": "3.11"
  },
  "files": [
    {"name": "README.md", "template": "README_template.md"},
    {"name": ".gitignore", "template": "gitignore_python.txt"},
    {"name": "requirements.txt", "template": "requirements_basic.txt"}
  ],
  "symlinks": [
    {"source": "shared_scripts", "target": "scripts", "type": "directory"},
    {"source": "shared_configs/.vscode", "target": ".vscode", "type": "directory"}
  ],
  "github": {
    "create_repo": false,
    "initial_commit": true,
    "push_to_remote": true
  },
  "integrations": {
    "link_to_project_basefiles": true,
    "inherit_design_standards": true
  }
}
```

### 4. GUI Design (PySide6)

#### Main Window Layout
```
┌─────────────────────────────────────────────────────┐
│ Project Startup - New Project Wizard               │
├─────────────────────────────────────────────────────┤
│ Project Name: [_______________] [Check GitHub]     │
│ GitHub Status: ● Repository not found              │
├─────────────────────────────────────────────────────┤
│ Configuration:                                      │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Base Configuration          ▼ │ [Edit] [Save]  │ │
│ └─────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────┤
│ ┌─ Project Structure ─────┐ ┌─ Files & Templates ─┐ │
│ │ ☑ src/                 │ │ ☑ README.md        │ │
│ │ ☑ tests/               │ │ ☑ .gitignore       │ │
│ │ ☑ docs/                │ │ ☑ requirements.txt │ │
│ │ ☑ config/              │ │ ☑ LICENSE          │ │
│ │ ☑ .venv (create venv)  │ │ ☐ setup.py         │ │
│ └────────────────────────┘ └────────────────────┘ │
├─────────────────────────────────────────────────────┤
│ ┌─ Symlinks ─────────────────────────────────────┐ │
│ │ ☑ scripts/ → shared_scripts/               │ │
│ │ ☑ .vscode/ → shared_configs/.vscode/       │ │
│ │ ☑ docs/standards/ → Project_BaseFiles/...  │ │
│ └───────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────┤
│ GitHub Options: ☑ Initial Commit ☑ Push to Remote │
├─────────────────────────────────────────────────────┤
│              [Cancel]  [Create Project]            │
└─────────────────────────────────────────────────────┘
```

#### Special Features
- **Configuration Dropdown**: Select from saved configurations
- **"***" Admin Mode**: Hidden option to edit default configurations
- **Real-time GitHub Status**: Live checking of repository existence
- **Preview Mode**: Show what will be created before execution

### 5. Integration with Project_BaseFiles

#### Symlink Integration
```python
# Link to existing Project_BaseFiles infrastructure
symlinks = {
    "scripts": "~/Desktop/Project_BaseFiles/Scripts",
    ".vscode/settings.json": "~/Desktop/Project_BaseFiles/Config/VSCode/settings.json",
    "docs/standards": "~/Desktop/Project_BaseFiles/Docs/Standards"
}
```

#### Template Inheritance
- Copy templates from Project_BaseFiles/Docs/Templates/
- Inherit design standards and file headers
- Maintain consistency across project ecosystem

---

## 💻 Technical Implementation

### Phase 1: Core Infrastructure (Week 1)

#### 1.1 Project Structure & Basic CLI
```python
# src/main.py
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--projectname', help='Project name')
    parser.add_argument('--config', action='store_true', help='Open config editor')
    
    if args.projectname:
        # Direct creation
        create_project_direct(args.projectname)
    else:
        # Launch GUI
        launch_gui()
```

#### 1.2 Configuration System
```python
# src/core/config_manager.py
class ConfigManager:
    def load_base_config(self) -> dict
    def load_project_config(self, project_name: str) -> dict
    def save_project_config(self, project_name: str, config: dict)
    def get_available_templates(self) -> list
    def validate_config(self, config: dict) -> bool
```

#### 1.3 Basic GUI Framework
```python
# src/gui/main_window.py
class MainWindow(QMainWindow):
    def __init__(self):
        # Setup UI components
        self.setup_project_info_section()
        self.setup_configuration_section()
        self.setup_structure_section()
        self.setup_github_section()
```

### Phase 2: Core Functionality (Week 2)

#### 2.1 Project Creation Engine
```python
# src/core/project_creator.py
class ProjectCreator:
    def create_project(self, config: dict) -> bool:
        self.create_directory_structure(config['structure'])
        self.copy_template_files(config['files'])
        self.create_symlinks(config['symlinks'])
        self.setup_virtual_environment(config)
        self.initialize_git(config)
        return True
```

#### 2.2 GitHub Integration
```python
# src/core/github_manager.py
class GitHubManager:
    def check_repository_exists(self, repo_name: str) -> RepoStatus
    def get_repository_info(self, repo_name: str) -> dict
    def create_initial_commit(self, project_path: str)
    def push_to_remote(self, project_path: str)
    def recreate_repository(self, repo_name: str)  # Dangerous operation
```

#### 2.3 Template Engine
```python
# src/core/template_engine.py
class TemplateEngine:
    def process_template(self, template_path: str, variables: dict) -> str
    def copy_template_file(self, source: str, destination: str, variables: dict)
    def generate_from_template(self, template_name: str, output_path: str)
```

### Phase 3: Advanced Features (Week 3)

#### 3.1 Symlink Management
```python
# src/core/symlink_manager.py
class SymlinkManager:
    def create_symlink(self, source: str, target: str, link_type: str)
    def validate_symlink_targets(self, symlinks: list) -> bool
    def update_symlinks(self, project_path: str, new_symlinks: list)
    def remove_broken_symlinks(self, project_path: str)
```

#### 3.2 Advanced GUI Features
- Configuration editor with live preview
- Project wizard with step-by-step guidance
- Admin mode for template management
- Progress bars and status indicators

#### 3.3 Error Handling & Validation
- Input validation for project names
- GitHub connectivity checks
- Symlink target validation
- Configuration schema validation

---

## 🔧 Installation & Setup

### Bash Integration Script
```bash
#!/bin/bash
# scripts/install.sh

# Install newproj command
echo "Installing Project_Startup..."

# Create launcher script
cat > /home/herb/Desktop/Project_Startup/scripts/newproj << 'EOF'
#!/bin/bash
cd /home/herb/Desktop/Project_Startup
python src/main.py "$@"
EOF

chmod +x /home/herb/Desktop/Project_Startup/scripts/newproj

# Add to bashrc if not already there
if ! grep -q "alias newproj=" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# Project_Startup alias" >> ~/.bashrc
    echo "alias newproj='/home/herb/Desktop/Project_Startup/scripts/newproj'" >> ~/.bashrc
    echo "newproj command installed! Restart terminal or run: source ~/.bashrc"
else
    echo "newproj alias already exists in ~/.bashrc"
fi
```

### Requirements
```txt
PySide6>=6.6.0
requests>=2.31.0
GitPython>=3.1.40
pathspec>=0.11.2
Jinja2>=3.1.2
```

---

## 🛡️ Safety & Security

### Dangerous Operations
1. **Repository Recreation**: Multiple confirmations, clear warnings
2. **Symlink Creation**: Validate targets exist and are safe
3. **File Overwrites**: Backup existing files before replacement

### Configuration Validation
- Schema validation for all JSON configs
- Path validation for symlink targets
- GitHub credentials validation

### Error Recovery
- Rollback mechanism for failed project creation
- Backup original files before modification
- Clear error messages with suggested fixes

---

## 🧪 Testing Strategy

### Unit Tests
- Configuration loading/saving
- Template processing
- GitHub API integration
- Symlink creation

### Integration Tests
- Full project creation workflow
- GitHub repository interaction
- Configuration inheritance

### User Acceptance Tests
- GUI workflow testing
- Command-line interface testing
- Error scenario handling

---

## 📈 Future Enhancements

### Version 2.0 Features
- Plugin system for custom project types
- Integration with other version control systems
- Team configuration sharing
- Automated dependency updates

### Integration Opportunities
- VS Code extension for project creation
- GitHub Actions workflow templates
- Docker container setup options
- CI/CD pipeline initialization

---

## 🎯 Success Metrics

### Functional Requirements
- ✅ Create projects via `newproj --projectname`
- ✅ GUI interface for configuration
- ✅ GitHub repository detection and integration
- ✅ Symlink-based shared resource system
- ✅ Configuration inheritance and customization

### Quality Requirements
- ✅ Sub-10 second project creation
- ✅ Zero data loss during repository recreation
- ✅ 100% Design Standard v2.1 compliance
- ✅ Intuitive GUI requiring no documentation

### User Experience
- ✅ Single command project creation
- ✅ Visual feedback for all operations
- ✅ Clear error messages and recovery
- ✅ Seamless integration with existing workflow

---

This implementation plan leverages everything valuable from Project_BaseFiles while creating a completely new, robust system for project initialization. The architecture supports extensibility, maintains safety, and provides an excellent user experience through both CLI and GUI interfaces.

Ready to begin implementation phase by phase!