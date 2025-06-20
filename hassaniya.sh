#!/bin/bash
# Hassaniya Text Normalizer - Unix/Linux Shell Interface
# This script provides easy access to the Hassaniya Text Normalizer tools

set -e  # Exit on any error

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to check if Python is installed
check_python() {
    if command -v python3 &> /dev/null; then
        echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"
        return 0
    elif command -v python &> /dev/null; then
        echo -e "${GREEN}✓ Python found: $(python --version)${NC}"
        return 0
    else
        echo -e "${RED}✗ Python not found. Please install Python 3.8+ from https://python.org${NC}"
        return 1
    fi
}

# Function to get Python command
get_python_cmd() {
    if command -v python3 &> /dev/null; then
        echo "python3"
    else
        echo "python"
    fi
}

# Function to check if dependencies are installed
check_deps() {
    local python_cmd=$(get_python_cmd)
    if $python_cmd -c "import gradio, flask, flask_cors" &> /dev/null; then
        echo -e "${GREEN}✓ Dependencies are installed${NC}"
        return 0
    else
        echo -e "${YELLOW}✗ Some dependencies are missing${NC}"
        return 1
    fi
}

# Function to install dependencies
install_deps() {
    echo -e "${YELLOW}Installing dependencies...${NC}"
    local python_cmd=$(get_python_cmd)
    
    # Install main requirements
    echo -e "${YELLOW}Installing main requirements...${NC}"
    $python_cmd -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Failed to install main requirements${NC}"
        return 1
    fi
    
    # Install web UI requirements
    echo -e "${YELLOW}Installing web UI requirements...${NC}"
    $python_cmd -m pip install -r web_ui/requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Failed to install web UI requirements${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
    return 0
}

# Function to show help
show_help() {
    echo -e "${CYAN}"
    cat << 'EOF'
🔤 Hassaniya Text Normalizer - Unix/Linux Shell Interface

USAGE:
    ./hassaniya.sh <action> [options]

ACTIONS:
    web         Launch the custom web interface (recommended)
    gradio      Launch the Gradio interface
    normalize   Normalize a text file from command line
    install     Install/update dependencies
    help        Show this help message

EXAMPLES:
    ./hassaniya.sh web
    ./hassaniya.sh gradio
    ./hassaniya.sh normalize input.txt output.txt
    ./hassaniya.sh normalize input.txt output.txt --show-diff
    ./hassaniya.sh install

WEB INTERFACE FEATURES:
    • Text Normalizer - Normalize Hassaniya Arabic text
    • Variant Manager - Add and manage word variants
    • Word Separation Manager - Manage word separation pairs
    • Dark theme interface
    • Real-time diff visualization

FILES:
    • data/hassaniya_variants.jsonl - Word variant mappings
    • data/word_separation.jsonl - Word separation pairs
    • data/exception_words_g_q.json - Exception words for گ/ق rules

EOF
    echo -e "${NC}"
}

# Main script logic
case "$1" in
    'help'|'-h'|'--help'|'')
        show_help
        exit 0
        ;;
    
    'install')
        if ! check_python; then
            exit 1
        fi
        
        if install_deps; then
            echo -e "\n${GREEN}✓ Installation complete! You can now run:${NC}"
            echo -e "${CYAN}    ./hassaniya.sh web${NC}"
        else
            echo -e "\n${RED}✗ Installation failed${NC}"
            exit 1
        fi
        exit 0
        ;;
    
    'web')
        echo -e "${CYAN}🚀 Starting Hassaniya Text Normalizer Web Interface...${NC}"
        
        if ! check_python; then
            exit 1
        fi
        
        if ! check_deps; then
            echo -e "${YELLOW}Installing missing dependencies...${NC}"
            if ! install_deps; then
                exit 1
            fi
        fi
        
        local python_cmd=$(get_python_cmd)
        echo -e "\n${GREEN}📱 Web interface will open at: http://localhost:5000${NC}"
        echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
        echo
        
        $python_cmd web_ui/server.py
        ;;
    
    'gradio')
        echo -e "${CYAN}🚀 Starting Hassaniya Text Normalizer Gradio Interface...${NC}"
        
        if ! check_python; then
            exit 1
        fi
        
        if ! check_deps; then
            echo -e "${YELLOW}Installing missing dependencies...${NC}"
            if ! install_deps; then
                exit 1
            fi
        fi
        
        local python_cmd=$(get_python_cmd)
        echo -e "\n${GREEN}📱 Gradio interface will open automatically in your browser${NC}"
        echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
        echo
        
        $python_cmd app/gradio_ui.py
        ;;
    
    'normalize')
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo -e "${RED}✗ Error: Input file and output file are required for normalize action${NC}"
            echo -e "${YELLOW}Usage: ./hassaniya.sh normalize input.txt output.txt [--show-diff]${NC}"
            exit 1
        fi
        
        if [ ! -f "$2" ]; then
            echo -e "${RED}✗ Error: Input file '$2' does not exist${NC}"
            exit 1
        fi
        
        if ! check_python; then
            exit 1
        fi
        
        local python_cmd=$(get_python_cmd)
        echo -e "${CYAN}🔤 Normalizing text from '$2' to '$3'...${NC}"
        
        if [ "$4" = "--show-diff" ]; then
            $python_cmd -m cli.normalize_text --in "$2" --out "$3" --show-diff
        else
            $python_cmd -m cli.normalize_text --in "$2" --out "$3"
        fi
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Text normalization completed successfully${NC}"
        else
            echo -e "${RED}✗ Text normalization failed${NC}"
            exit 1
        fi
        ;;
    
    *)
        echo -e "${RED}✗ Unknown action: $1${NC}"
        show_help
        exit 1
        ;;
esac