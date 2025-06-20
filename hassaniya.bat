@echo off
REM Hassaniya Text Normalizer - Windows Batch Interface
REM This script provides easy access to the Hassaniya Text Normalizer tools

setlocal enabledelayedexpansion

REM Get the script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check if action is provided
if "%1"=="" (
    call :show_help
    exit /b 1
)

REM Parse the action
set "ACTION=%1"

if /i "%ACTION%"=="help" (
    call :show_help
    exit /b 0
)

if /i "%ACTION%"=="install" (
    call :install_deps
    exit /b !errorlevel!
)

if /i "%ACTION%"=="web" (
    call :start_web
    exit /b !errorlevel!
)

if /i "%ACTION%"=="gradio" (
    call :start_gradio
    exit /b !errorlevel!
)

if /i "%ACTION%"=="normalize" (
    call :normalize_text %2 %3 %4
    exit /b !errorlevel!
)

echo [ERROR] Unknown action: %ACTION%
call :show_help
exit /b 1

:show_help
echo.
echo 🔤 Hassaniya Text Normalizer - Windows Batch Interface
echo.
echo USAGE:
echo     hassaniya.bat ^<action^> [options]
echo.
echo ACTIONS:
echo     web         Launch the custom web interface (recommended)
echo     gradio      Launch the Gradio interface
echo     normalize   Normalize a text file from command line
echo     install     Install/update dependencies
echo     help        Show this help message
echo.
echo EXAMPLES:
echo     hassaniya.bat web
echo     hassaniya.bat gradio
echo     hassaniya.bat normalize input.txt output.txt
echo     hassaniya.bat normalize input.txt output.txt --show-diff
echo     hassaniya.bat install
echo.
echo WEB INTERFACE FEATURES:
echo     • Text Normalizer - Normalize Hassaniya Arabic text
echo     • Variant Manager - Add and manage word variants
echo     • Word Separation Manager - Manage word separation pairs
echo     • Dark theme interface
echo     • Real-time diff visualization
echo.
echo FILES:
echo     • data/hassaniya_variants.jsonl - Word variant mappings
echo     • data/word_separation.jsonl - Word separation pairs
echo     • data/exception_words_g_q.json - Exception words for گ/ق rules
echo.
goto :eof

:check_python
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8+ from https://python.org
    exit /b 1
)
echo [INFO] Python found
goto :eof

:check_deps
python -c "import gradio, flask, flask_cors" >nul 2>&1
if !errorlevel! neq 0 (
    echo [WARNING] Some dependencies are missing
    exit /b 1
)
echo [INFO] Dependencies are installed
goto :eof

:install_deps
echo [INFO] Installing dependencies...

call :check_python
if !errorlevel! neq 0 exit /b 1

REM Install main requirements
echo [INFO] Installing main requirements...
python -m pip install -r requirements.txt
if !errorlevel! neq 0 (
    echo [ERROR] Failed to install main requirements
    exit /b 1
)

REM Install web UI requirements
echo [INFO] Installing web UI requirements...
python -m pip install -r web_ui/requirements.txt
if !errorlevel! neq 0 (
    echo [ERROR] Failed to install web UI requirements
    exit /b 1
)

echo [SUCCESS] Dependencies installed successfully
echo.
echo [INFO] Installation complete! You can now run:
echo     hassaniya.bat web
exit /b 0

:start_web
echo 🚀 Starting Hassaniya Text Normalizer Web Interface...

call :check_python
if !errorlevel! neq 0 exit /b 1

call :check_deps
if !errorlevel! neq 0 (
    echo [INFO] Installing missing dependencies...
    call :install_deps
    if !errorlevel! neq 0 exit /b 1
)

echo.
echo [INFO] Web interface will open at: http://localhost:5000
echo [INFO] Press Ctrl+C to stop the server
echo.

python web_ui/server.py
exit /b !errorlevel!

:start_gradio
echo 🚀 Starting Hassaniya Text Normalizer Gradio Interface...

call :check_python
if !errorlevel! neq 0 exit /b 1

call :check_deps
if !errorlevel! neq 0 (
    echo [INFO] Installing missing dependencies...
    call :install_deps
    if !errorlevel! neq 0 exit /b 1
)

echo.
echo [INFO] Gradio interface will open automatically in your browser
echo [INFO] Press Ctrl+C to stop the server
echo.

python app/gradio_ui.py
exit /b !errorlevel!

:normalize_text
set "INPUT_FILE=%1"
set "OUTPUT_FILE=%2"
set "SHOW_DIFF=%3"

if "%INPUT_FILE%"=="" (
    echo [ERROR] Input file is required
    echo Usage: hassaniya.bat normalize input.txt output.txt [--show-diff]
    exit /b 1
)

if "%OUTPUT_FILE%"=="" (
    echo [ERROR] Output file is required
    echo Usage: hassaniya.bat normalize input.txt output.txt [--show-diff]
    exit /b 1
)

if not exist "%INPUT_FILE%" (
    echo [ERROR] Input file '%INPUT_FILE%' does not exist
    exit /b 1
)

call :check_python
if !errorlevel! neq 0 exit /b 1

echo 🔤 Normalizing text from '%INPUT_FILE%' to '%OUTPUT_FILE%'...

if /i "%SHOW_DIFF%"=="--show-diff" (
    python -m cli.normalize_text --in "%INPUT_FILE%" --out "%OUTPUT_FILE%" --show-diff
) else (
    python -m cli.normalize_text --in "%INPUT_FILE%" --out "%OUTPUT_FILE%"
)

if !errorlevel! equ 0 (
    echo [SUCCESS] Text normalization completed successfully
) else (
    echo [ERROR] Text normalization failed
    exit /b 1
)

exit /b 0