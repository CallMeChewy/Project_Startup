# CSM Project Python Scripts Inventory

**File:** ScriptInventory.md  
**Path:** Docs/ScriptInventory.md  
**Standard:** AIDEV-PascalCase-2.1  
**Created:** 2025-07-17  
**Last Modified:** 2025-07-17  10:10AM

---

## 📋 **Overview**

This document provides a comprehensive inventory of all Python scripts in the Claude Session Manager (CSM) project. The scripts are organized by functional directory and include detailed information about their purpose, capabilities, dependencies, and integration within the CSM ecosystem.

---

## 🎯 **Main Application**

### `enhanced_claude_monitor.py`
**Location:** `/home/herb/Desktop/CSM/enhanced_claude_monitor.py`  
**Primary Purpose:** Core session monitoring script that provides multi-session support for Claude CLI processes with project isolation

**Key Features:**
- Multi-session Claude process detection and isolation
- Project-aware monitoring with automatic context inference
- Conversation history capture and routing
- Real-time MCP log monitoring
- Session restoration with project context
- Automatic archiving and compression
- Emergency capture for rate limits and crashes

**Dependencies:** `psutil`, `watchdog`, `pathlib`, `json`, `dataclasses`

**Usage Scenarios:**
- Monitoring simultaneous GitUp and CSM development sessions
- Capturing conversation history for session continuity
- Emergency recovery from Claude CLI crashes
- Session restoration after interruptions

**Integration:** Central component of CSM ecosystem, designed to work with GitUp and other Project Himalaya tools

---

## 📁 **Scripts Directory Structure**

### `Scripts/CurrentApp/`

#### `WebAppDiagnostic.py`
**Purpose:** Diagnostic tool for Anderson's Library web application setup verification

**Key Features:**
- Web application health checks
- API endpoint validation
- Database connectivity testing
- File existence verification
- Detailed diagnostic reporting

**Dependencies:** `requests`, `json`, `pathlib`

**Usage:** Verifying web application setup and identifying configuration issues

**Integration:** Part of Anderson's Library project diagnostic suite

---

### `Scripts/DataBase/`

#### `SQLiteToMySQL_DataDump.py`
**Purpose:** Converts SQLite databases to MySQL-compatible SQL scripts

**Key Features:**
- Schema and data migration
- Automatic database naming from filename
- Type mapping (SQLite to MySQL)
- Complete data export without MySQL connection

**Dependencies:** `sqlite3`, `argparse`

**Usage:** Creating MySQL import scripts from SQLite databases

#### `SQLiteToMySQL_GenericPort.py`
**Purpose:** Direct SQLite to MySQL migration utility

**Key Features:**
- Live database migration
- Schema recreation
- Data transfer with batch processing
- Connection-based migration

**Dependencies:** `sqlite3`, `mysql.connector`

**Usage:** Direct database migration for development/testing

#### `SQLiteToMySQL_GenericPort_Hardened.py`
**Purpose:** Production-ready SQLite to MySQL migration tool

**Key Features:**
- JSON configuration file support
- Command-line argument parsing
- Enhanced error handling
- Configurable connection parameters

**Dependencies:** `sqlite3`, `mysql.connector`, `json`

**Usage:** Production database migrations with configuration management

---

### `Scripts/Deployment/`

#### `UpdateFiles.py`
**Purpose:** Himalaya-standard file deployment utility with PascalCase enforcement

**Key Features:**
- Header path parsing for deployment locations
- Base directory stripping and path normalization
- PascalCase naming convention enforcement
- Automatic archiving of existing files
- Comprehensive audit trail generation

**Dependencies:** `shutil`, `re`, `logging`

**Usage:** Automated file deployment from Updates directory

**Integration:** Core deployment tool for Project Himalaya ecosystem

---

### `Scripts/FinderDisplay/`

#### `NewPyDump.py`
**Purpose:** Generate CSV reports of Python files with metadata

**Key Features:**
- .gitignore-aware file discovery
- Size, line count, and modification date tracking
- CSV output with headers
- Date filtering capabilities

**Dependencies:** `pathspec`, `csv`

**Usage:** Project analysis and code inventory generation

#### `ListNewPy.py`
**Purpose:** Terminal-based Python file listing utility

**Key Features:**
- Sorted file listing by modification date
- Size and line count display
- .gitignore pattern respect
- Console-friendly output

**Dependencies:** `pathspec`

**Usage:** Quick Python file overview in terminal

#### `FindText.py`
**Purpose:** Simple text search utility for documentation

**Key Features:**
- Multi-file text search
- Line number reporting
- Case-insensitive matching
- Markdown/text file focus

**Usage:** Finding specific content in documentation

#### `FindTextTwo.py`
**Purpose:** Advanced text search with multiple query support

**Key Features:**
- Dual-phrase search capability
- Same-line matching requirement
- Enhanced search precision

**Usage:** Complex text pattern matching

#### `AdvancedFileSearcher.py`
**Purpose:** GUI-based file search application

**Key Features:**
- PySide6 GUI interface
- Multi-threaded search processing
- Include/exclude pattern support
- Real-time search results
- File type filtering

**Dependencies:** `PySide6`, `threading`

**Usage:** Advanced file content searching with GUI

#### `ListFilesByDate.py`
**Purpose:** Simple file listing by modification date

**Key Features:**
- Date-sorted file listing
- Modification timestamp display
- Current directory focus

**Usage:** Quick file timeline analysis

#### `SimpleTree.py`
**Purpose:** .gitignore-aware directory tree generator

**Key Features:**
- Pathspec-based .gitignore parsing
- Directory tree visualization
- Content-only pattern handling
- Clean tree output format

**Dependencies:** `pathspec`

**Usage:** Project structure visualization

---

### `Scripts/GitHub/`

#### `GitHubTimeMachine.py`
**Purpose:** Git commit navigation tool with GUI

**Key Features:**
- PySide6 GUI interface
- Commit history browsing
- Branch creation for time travel
- GitHub integration links

**Dependencies:** `PySide6`, `subprocess`

**Usage:** Git repository time travel and exploration

#### `TimeTraveiGitHub.py`
**Purpose:** Advanced Git time travel with file comparison

**Key Features:**
- Enhanced commit navigation
- File-specific tracking
- Side-by-side diff viewer
- Fullscreen comparison mode
- Web file filtering (.py, .js, .css, .html)

**Dependencies:** `PySide6`, `subprocess`, `difflib`

**Usage:** Advanced git history exploration with file comparison

#### `GitHubAutoUpdate.py`
**Purpose:** Automated GitHub repository updates

**Key Features:**
- Automated add/commit/push workflow
- Watch mode for continuous updates
- Custom commit message support
- Configuration file management
- Library-specific update methods

**Dependencies:** `subprocess`, `json`, `pathlib`

**Usage:** Automated GitHub Pages deployment

**Integration:** Core tool for BowersWorld.com and library updates

#### `GitHubUpdateSite.py`
**Purpose:** Simple GitHub Pages update utility

**Key Features:**
- Interactive update menu
- Automatic commit messages
- Quick update functions
- Command-line interface

**Dependencies:** `subprocess`

**Usage:** Simple GitHub Pages site updates

#### `GitHubInitialCommit.py`
**Purpose:** New repository initialization and first commit

**Key Features:**
- Repository initialization
- GitHub CLI integration
- Initial commit creation
- Remote setup and push

**Dependencies:** `subprocess` (requires GitHub CLI)

**Usage:** Setting up new GitHub repositories

---

### `Scripts/System/`

#### `BackupTemp.py`
**Purpose:** Temporary backup utility for specific directories

**Key Features:**
- Selective directory backup
- Timestamp-based naming
- File extension filtering
- Quick backup functionality

**Dependencies:** `shutil`

**Usage:** Quick project backups

#### `BackupProject.py`
**Purpose:** Comprehensive project backup with .gitignore support

**Key Features:**
- .gitignore pattern parsing
- Negation pattern support
- Recursive directory copying
- Desktop backup location

**Dependencies:** `shutil`, `pathlib`

**Usage:** Full project backup with git-aware filtering

#### `CodebaseSum.py`
**Purpose:** Comprehensive codebase analysis and documentation

**Key Features:**
- .gitignore-aware file discovery
- PDF content extraction
- Tree structure generation
- File content compilation
- Complete project snapshot

**Dependencies:** `pathspec`, `PyPDF2`

**Usage:** Project documentation and analysis

**Integration:** Key tool for project analysis and documentation

---

### `Scripts/Tools/`

#### `MarkdownToText.py`
**Purpose:** Markdown to plain text conversion utility

**Key Features:**
- Comprehensive Markdown syntax removal
- Batch directory processing
- Structure preservation
- PascalCase naming enforcement
- Detailed logging and audit trail

**Dependencies:** `re`, `logging`

**Usage:** Converting documentation to plain text

#### `GPUOCRSpeedTest.py`
**Purpose:** GPU-accelerated OCR performance testing

**Key Features:**
- CUDA availability testing
- Multiple OCR engine comparison (EasyOCR, PaddleOCR, Tesseract)
- Performance benchmarking
- Speedup analysis

**Dependencies:** `torch`, `easyocr`, `paddleocr`, `pytesseract`, `pdf2image`

**Usage:** OCR performance optimization testing

#### `VerifyIgnore.py`
**Purpose:** .gitignore pattern verification and visualization

**Key Features:**
- Robust .gitignore parsing
- Pattern matching verification
- Tree visualization with debug output
- Negation pattern support

**Dependencies:** `pathlib`, `fnmatch`

**Usage:** Debugging .gitignore patterns and project structure

---

### `Tests/`

#### `test_multi_session.py`
**Purpose:** Comprehensive multi-session testing with dependencies

**Key Features:**
- Full dependency testing with psutil/watchdog
- Multi-session scenario testing
- Integration test validation
- Performance testing

**Dependencies:** `psutil`, `watchdog`, `pathlib`

**Usage:** Comprehensive CSM testing

#### `validate_multi_session.py`
**Purpose:** Dependency-free multi-session architecture validation

**Key Features:**
- Core logic validation without external dependencies
- Critical requirements testing
- Architecture verification
- Quick validation testing

**Dependencies:** `json`, `pathlib`, `datetime`, `dataclasses`

**Usage:** Quick architecture validation

---

## 🗂️ **Script Categories by Function**

### **Core CSM Functionality**
- **enhanced_claude_monitor.py** - Main application
- **WebAppDiagnostic.py** - Application diagnostics
- **test_multi_session.py** - Comprehensive testing
- **validate_multi_session.py** - Quick validation

### **Database Operations**
- **SQLiteToMySQL_DataDump.py** - SQL export
- **SQLiteToMySQL_GenericPort.py** - Direct migration
- **SQLiteToMySQL_GenericPort_Hardened.py** - Production migration

### **File Management & Deployment**
- **UpdateFiles.py** - Automated deployment
- **BackupProject.py** - Project backup
- **BackupTemp.py** - Quick backup

### **Git & Version Control**
- **GitHubAutoUpdate.py** - Automated updates
- **GitHubUpdateSite.py** - Simple updates
- **GitHubInitialCommit.py** - Repository setup
- **GitHubTimeMachine.py** - Commit navigation
- **TimeTraveiGitHub.py** - Advanced git exploration

### **File Search & Analysis**
- **AdvancedFileSearcher.py** - GUI search
- **FindText.py** - Simple text search
- **FindTextTwo.py** - Multi-phrase search
- **NewPyDump.py** - Python file analysis
- **ListNewPy.py** - File listing
- **ListFilesByDate.py** - Date-sorted listing

### **Project Analysis & Documentation**
- **CodebaseSum.py** - Comprehensive analysis
- **SimpleTree.py** - Directory visualization
- **VerifyIgnore.py** - .gitignore verification

### **Text Processing & Utilities**
- **MarkdownToText.py** - Markdown conversion
- **GPUOCRSpeedTest.py** - OCR performance testing

---

## 🔗 **Integration Points**

### **CSM Ecosystem Integration**
- **enhanced_claude_monitor.py** works with GitUp for multi-session monitoring
- **CodebaseSum.py** provides project analysis for documentation
- **BackupProject.py** ensures project safety during development

### **Project Himalaya Integration**
- **UpdateFiles.py** enforces PascalCase naming standards
- **GitHubAutoUpdate.py** supports BowersWorld.com deployment
- All scripts follow AIDEV-PascalCase-2.1 standard

### **Anderson's Library Integration**
- **WebAppDiagnostic.py** validates library web application
- **SQLiteToMySQL_*.py** scripts support database migration
- **GPUOCRSpeedTest.py** optimizes OCR performance

---

## 🔄 **Usage Patterns**

### **Development Workflow**
1. Use **enhanced_claude_monitor.py** for session monitoring
2. Use **GitHubAutoUpdate.py** for automated deployments
3. Use **BackupProject.py** for safety backups
4. Use **CodebaseSum.py** for documentation

### **Analysis & Debugging**
1. Use **VerifyIgnore.py** for .gitignore debugging
2. Use **FindText.py** for content searching
3. Use **ListNewPy.py** for file inventory
4. Use **SimpleTree.py** for structure visualization

### **Deployment & Maintenance**
1. Use **UpdateFiles.py** for file deployment
2. Use **GitHubInitialCommit.py** for new repositories
3. Use **WebAppDiagnostic.py** for application health checks

---

## 📊 **Script Statistics**

- **Total Scripts:** 26
- **Core CSM:** 4 scripts
- **Database Operations:** 3 scripts
- **File Management:** 3 scripts
- **Git Operations:** 5 scripts
- **Search & Analysis:** 6 scripts
- **Project Analysis:** 3 scripts
- **Text Processing:** 2 scripts

---

## 🎯 **Key Insights**

This inventory demonstrates the comprehensive nature of the CSM project's script ecosystem, with tools covering:

1. **Monitoring & Session Management** - The core CSM functionality
2. **Database Migration** - Complete SQLite to MySQL ecosystem
3. **File & Project Management** - Backup, deployment, and analysis
4. **Version Control Integration** - GitHub automation and exploration
5. **Search & Discovery** - Multiple search and analysis tools
6. **Project Analysis** - Documentation and structure tools
7. **Utility Functions** - Text processing and performance testing

The scripts work together to provide a complete development ecosystem supporting the Project Himalaya vision of integrated AI-assisted development tools.

---

**Next Steps:**
1. Verify all scripts have proper Design Standard v2.1 headers
2. Test integration points between scripts
3. Document dependency installation requirements
4. Create usage examples for each script category
5. Integrate with CSM session monitoring for script usage tracking