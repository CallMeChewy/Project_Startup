# Common Scripts Repository Design

**File:** CommonScriptsRepository.md  
**Path:** Docs/CommonScriptsRepository.md  
**Standard:** AIDEV-PascalCase-2.1  
**Created:** 2025-07-17  
**Last Modified:** 2025-07-17  10:30AM

---

## 🎯 **The Problem**

You have scripts that:
- Migrate between projects and get modified
- Are hard to remember and access
- Sometimes become outdated or dangerous
- Need parameters but you forget what they are

## 💡 **The Solution: Common Scripts Repository**

### **Recommended Structure:**
```
~/Development/CommonScripts/
├── Scripts/                    # All your common scripts
│   ├── ScriptMenu.py          # Main menu system
│   ├── QuickLauncher.py       # Simple launcher
│   ├── System/
│   ├── GitHub/
│   ├── Tools/
│   └── ...
├── Docs/                      # Shared documentation
│   ├── Standards/             # Design standards for all projects
│   ├── Templates/             # Common file templates
│   └── ScriptHelp/           # Individual script documentation
└── Config/                    # Common configuration files
    ├── .gitignore-templates/
    ├── vscode-settings/
    └── script-configs/
```

### **In Each Project:**
```
YourProject/
├── Scripts/                   # Symlinks to common scripts
│   ├── ScriptMenu.py -> ~/Development/CommonScripts/Scripts/ScriptMenu.py
│   ├── QuickLauncher.py -> ~/Development/CommonScripts/Scripts/QuickLauncher.py
│   └── System/ -> ~/Development/CommonScripts/Scripts/System/
├── Docs/
│   └── Standards/ -> ~/Development/CommonScripts/Docs/Standards/
└── .vscode/
    └── settings.json -> ~/Development/CommonScripts/Config/vscode-settings/settings.json
```

## 🔧 **Implementation Steps**

### **Phase 1: Create Common Repository**
```bash
# Create the structure
mkdir -p ~/Development/CommonScripts/{Scripts,Docs,Config}
mkdir -p ~/Development/CommonScripts/Scripts/{System,GitHub,Tools,DataBase,FinderDisplay,Deployment,CurrentApp}
mkdir -p ~/Development/CommonScripts/Docs/{Standards,Templates,ScriptHelp}
mkdir -p ~/Development/CommonScripts/Config/{gitignore-templates,vscode-settings,script-configs}

# Move current scripts
cp -r /home/herb/Desktop/CSM/Scripts/* ~/Development/CommonScripts/Scripts/
cp -r /home/herb/Desktop/CSM/Docs/Standards/* ~/Development/CommonScripts/Docs/Standards/
```

### **Phase 2: Create Project Setup Script**
```python
# ~/Development/CommonScripts/SetupProject.py
# This script creates symlinks in new projects
```

### **Phase 3: Modify Existing Projects**
```bash
# For each existing project:
cd /path/to/project
rm -rf Scripts/  # Remove local copies
ln -s ~/Development/CommonScripts/Scripts Scripts
ln -s ~/Development/CommonScripts/Docs/Standards Docs/Standards
```

## 🎯 **Benefits**

1. **Single Source of Truth** - Scripts exist in one place
2. **Consistent Updates** - Fix once, fixed everywhere
3. **No More Forgetting** - Menu system helps you remember
4. **Safety First** - Dangerous scripts have warnings
5. **Parameter Help** - Menu prompts for required parameters
6. **Easy Access** - Right-click → Run in VS Code

## 🔄 **Workflow**

### **Daily Use:**
1. Right-click `Scripts/QuickLauncher.py` → Run
2. Choose from most common scripts
3. Or use `Scripts/ScriptMenu.py` for full menu

### **New Project Setup:**
1. Run `~/Development/CommonScripts/SetupProject.py`
2. Creates all necessary symlinks
3. Copies project-specific templates

### **Script Maintenance:**
1. Update scripts in `~/Development/CommonScripts/Scripts/`
2. Changes automatically available in all projects
3. No need to copy/update individual projects

## 📝 **Script Categories for Common Repo**

### **Universal Scripts** (should be in common repo):
```
✅ System/BackupProject.py
✅ System/CodebaseSum.py
✅ FinderDisplay/ListFilesByDate.py
✅ FinderDisplay/SimpleTree.py
✅ FinderDisplay/FindText.py
✅ Tools/VerifyIgnore.py
✅ Tools/MarkdownToText.py
✅ GitHub/GitHubAutoUpdate.py
✅ GitHub/GitHubInitialCommit.py
✅ Deployment/UpdateFiles.py
```

### **Project-Specific Scripts** (keep local):
```
❌ CurrentApp/WebAppDiagnostic.py (Anderson's Library specific)
❌ Tools/GPUOCRSpeedTest.py (very specific use case)
❌ Tests/* (project-specific testing)
```

### **Maybe Common** (decide per project):
```
🤔 DataBase/SQLiteToMySQL_*.py (useful for multiple projects)
🤔 GitHub/GitHubTimeMachine.py (useful for any git project)
🤔 FinderDisplay/AdvancedFileSearcher.py (useful for any project)
```

## 🚀 **Next Steps**

1. **Create the common repository structure**
2. **Test with one project first** (CSM)
3. **Create SetupProject.py script**
4. **Migrate other projects gradually**
5. **Add version control to common scripts**

## 📋 **Migration Script Template**

```python
#!/usr/bin/env python3
# MigrateToCommonScripts.py
import os
import shutil
from pathlib import Path

def migrate_project(project_path):
    """Migrate a project to use common scripts"""
    # Remove local Scripts directory
    # Create symlinks to common scripts
    # Update documentation links
    # Create project-specific config
```

This approach gives you:
- **One place to maintain scripts**
- **Consistent experience across projects**
- **No more "where did I put that script?"**
- **Easy parameter handling**
- **Safety warnings for dangerous operations**

Perfect for your VS Code workflow! 🎯