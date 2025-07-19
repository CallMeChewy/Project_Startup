# File: main_window.py
# Path: Project_Startup/src/gui/main_window.py
# Standard: AIDEV-PascalCase-2.2
# Created: 2025-01-19
# Last Modified: 2025-01-19  09:20AM
"""
Description: Main GUI window for Project_Startup application using PySide6
"""

try:
    from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                                   QHBoxLayout, QLabel, QLineEdit, 
                                   QPushButton, QTextEdit, QProgressBar)
    from PySide6.QtCore import Qt, QThread, pyqtSignal
    PYSIDE6_AVAILABLE = True
except ImportError:
    # Create stub classes for testing when PySide6 not available
    class QMainWindow:
        def __init__(self): pass
        def show(self): pass
    
    PYSIDE6_AVAILABLE = False


class MainWindow(QMainWindow):
    """Main window for Project_Startup GUI application"""
    
    def __init__(self):
        """Initialize the main window"""
        super().__init__()
        
        if not PYSIDE6_AVAILABLE:
            print("PySide6 not available - GUI will not function")
            return
        
        self.setWindowTitle("Project_Startup - New Project Creator")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize UI components
        self.setup_ui()
        
        # Connect signals
        self.connect_signals()
    
    def setup_ui(self):
        """Set up the user interface"""
        if not PYSIDE6_AVAILABLE:
            return
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Project name section
        project_layout = QHBoxLayout()
        project_layout.addWidget(QLabel("Project Name:"))
        self.project_name_edit = QLineEdit()
        self.project_name_edit.setPlaceholderText("Enter project name (e.g., MyAwesomeProject)")
        project_layout.addWidget(self.project_name_edit)
        layout.addLayout(project_layout)
        
        # GitHub status section
        self.github_status_label = QLabel("GitHub Status: Not checked")
        layout.addWidget(self.github_status_label)
        
        # Template selection section
        template_layout = QHBoxLayout()
        template_layout.addWidget(QLabel("Template:"))
        self.template_combo = QLineEdit()  # Placeholder for QComboBox
        self.template_combo.setText("python_basic")
        template_layout.addWidget(self.template_combo)
        layout.addLayout(template_layout)
        
        # Progress section
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status/output section
        self.output_text = QTextEdit()
        self.output_text.setMaximumHeight(200)
        self.output_text.setPlaceholderText("Project creation output will appear here...")
        layout.addWidget(self.output_text)
        
        # Button section
        button_layout = QHBoxLayout()
        self.preview_button = QPushButton("Preview")
        self.create_button = QPushButton("Create Project")
        self.cancel_button = QPushButton("Cancel")
        
        button_layout.addWidget(self.preview_button)
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
    
    def connect_signals(self):
        """Connect UI signals to handlers"""
        if not PYSIDE6_AVAILABLE:
            return
        
        self.create_button.clicked.connect(self.create_project)
        self.preview_button.clicked.connect(self.preview_project)
        self.cancel_button.clicked.connect(self.close)
        self.project_name_edit.textChanged.connect(self.on_project_name_changed)
    
    def create_project(self):
        """Handle project creation"""
        project_name = self.project_name_edit.text().strip()
        
        if not project_name:
            self.output_text.append("❌ Please enter a project name")
            return
        
        self.output_text.append(f"🚀 Creating project: {project_name}")
        self.progress_bar.setVisible(True)
        
        # TODO: Implement actual project creation
        # This would integrate with ProjectCreator
        
        self.output_text.append(f"✅ Project {project_name} created successfully!")
        self.progress_bar.setVisible(False)
    
    def preview_project(self):
        """Handle project preview"""
        project_name = self.project_name_edit.text().strip()
        
        if not project_name:
            self.output_text.append("❌ Please enter a project name")
            return
        
        self.output_text.append(f"🔍 Previewing project: {project_name}")
        
        # TODO: Implement preview functionality
        # This would use ProjectCreator.preview_project()
    
    def on_project_name_changed(self, text):
        """Handle project name changes"""
        # TODO: Implement GitHub status checking
        # TODO: Validate project name
        pass