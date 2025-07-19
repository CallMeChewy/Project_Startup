#!/bin/bash
# File: install.sh
# Path: /home/herb/Desktop/Project_Startup/scripts/install.sh
# Standard: AIDEV-PascalCase-2.1
# Created: 2025-01-19
# Last Modified: 2025-01-19  09:10AM

echo "🚀 Installing Project_Startup..."

# Hardcoded project directory for bashrc alias
PROJECT_DIR="/home/herb/Desktop/Project_Startup"

echo "📁 Project directory: $PROJECT_DIR"

# Verify project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Project directory not found: $PROJECT_DIR"
    echo "Please ensure Project_Startup is installed at /home/herb/Desktop/Project_Startup"
    exit 1
fi

# Create launcher script
cat > "$PROJECT_DIR/scripts/newproj" << EOF
#!/bin/bash
# File: newproj
# Path: /home/herb/Desktop/Project_Startup/scripts/newproj
# Standard: AIDEV-PascalCase-2.1
# Created: 2025-01-19
# Last Modified: 2025-01-19  08:47AM

cd "$PROJECT_DIR"
python src/main.py "\$@"
EOF

chmod +x "$PROJECT_DIR/scripts/newproj"
echo "✅ Created launcher script"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd "$PROJECT_DIR"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "⚠️ No requirements.txt found"
fi

# Add to bashrc if not already there
if ! grep -q "alias newproj=" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# Project_Startup alias" >> ~/.bashrc
    echo "alias newproj='$PROJECT_DIR/scripts/newproj'" >> ~/.bashrc
    echo "✅ Added newproj alias to ~/.bashrc"
    echo ""
    echo "🎉 Installation complete!"
    echo "📝 Restart your terminal or run: source ~/.bashrc"
    echo "🚀 Then use: newproj --projectname MyProject"
else
    echo "✅ newproj alias already exists in ~/.bashrc"
    echo "🎉 Installation complete!"
fi

echo ""
echo "📋 Usage:"
echo "  newproj --projectname MyProject  # Create project directly"
echo "  newproj                         # Open GUI to enter project name"
echo "  newproj --help                  # Show help"