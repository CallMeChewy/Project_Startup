#!/usr/bin/env python3
# File: QuickLauncher.py
# Path: Scripts/QuickLauncher.py
# Standard: AIDEV-PascalCase-2.1
# Created: 2025-07-17
# Last Modified: 2025-07-17  10:25AM

"""
Ultra-simple script launcher for common tasks
Perfect for VS Code right-click execution
"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    """Quick launcher with most common scripts"""
    
    print("🚀 QUICK SCRIPT LAUNCHER")
    print("=" * 40)
    print("1. 📋 List files by date")
    print("2. 🌳 Show project tree")
    print("3. 🔍 Search for text")
    print("4. 💾 Backup project")
    print("5. 📊 Project summary")
    print("6. 🐙 GitHub auto-update")
    print("7. 🔧 Debug .gitignore")
    print("8. 📝 Full menu system")
    print("0. Exit")
    print("=" * 40)
    
    choice = input("Choose (0-8): ").strip()
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    scripts = {
        "1": "FinderDisplay/ListFilesByDate.py",
        "2": "FinderDisplay/SimpleTree.py", 
        "3": "FinderDisplay/FindText.py",
        "4": "System/BackupProject.py",
        "5": "System/CodebaseSum.py",
        "6": "GitHub/GitHubAutoUpdate.py",
        "7": "Tools/VerifyIgnore.py",
        "8": "ScriptMenu.py"
    }
    
    if choice == "0":
        print("👋 Done!")
        return
    
    if choice in scripts:
        script_path = script_dir / scripts[choice]
        
        if script_path.exists():
            print(f"🚀 Running {script_path.name}...")
            
            # Special handling for search
            if choice == "3":
                search_term = input("🔍 Search for: ").strip()
                if search_term:
                    subprocess.run([sys.executable, str(script_path), search_term], cwd=project_root)
            elif choice == "6":
                confirm = input("⚠️ This will commit/push to GitHub. Continue? (y/n): ")
                if confirm.lower() in ['y', 'yes']:
                    subprocess.run([sys.executable, str(script_path)], cwd=project_root)
            else:
                subprocess.run([sys.executable, str(script_path)], cwd=project_root)
        else:
            print(f"❌ Script not found: {script_path}")
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
