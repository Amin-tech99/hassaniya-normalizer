#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Hassaniya Text Normalizer - PowerShell Interface

.DESCRIPTION
    This script provides easy access to the Hassaniya Text Normalizer tools.
    It can launch the web interface, normalize text files, or manage variants.

.PARAMETER Action
    The action to perform: 'web', 'normalize', 'gradio', or 'help'

.PARAMETER InputFile
    Input text file to normalize (for 'normalize' action)

.PARAMETER OutputFile
    Output file for normalized text (for 'normalize' action)

.PARAMETER ShowDiff
    Show differences between original and normalized text

.EXAMPLE
    .\hassaniya.ps1 web
    Launches the custom web interface

.EXAMPLE
    .\hassaniya.ps1 gradio
    Launches the Gradio interface

.EXAMPLE
    .\hassaniya.ps1 normalize -InputFile "input.txt" -OutputFile "output.txt" -ShowDiff
    Normalizes text from input.txt and saves to output.txt with diff display

.EXAMPLE
    .\hassaniya.ps1 help
    Shows this help information
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [ValidateSet('web', 'normalize', 'gradio', 'help', 'install')]
    [string]$Action,
    
    [Parameter(Mandatory=$false)]
    [string]$InputFile,
    
    [Parameter(Mandatory=$false)]
    [string]$OutputFile,
    
    [Parameter(Mandatory=$false)]
    [switch]$ShowDiff
)

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Function to check if Python is installed
function Test-PythonInstalled {
    try {
        $pythonVersion = python --version 2>$null
        if ($pythonVersion) {
            Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "[ERROR] Python not found. Please install Python 3.8+ from https://python.org" -ForegroundColor Red
        return $false
    }
    return $false
}

# Function to check if dependencies are installed
function Test-DependenciesInstalled {
    try {
        python -c "import gradio, flask, flask_cors" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Dependencies are installed" -ForegroundColor Green
            return $true
        } else {
            Write-Host "[WARNING] Some dependencies are missing" -ForegroundColor Yellow
            return $false
        }
    } catch {
        Write-Host "[ERROR] Error checking dependencies" -ForegroundColor Red
        return $false
    }
}

# Function to install dependencies
function Install-Dependencies {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    
    # Install main requirements
    python -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install main requirements" -ForegroundColor Red
        return $false
    }
    
    # Install web UI requirements
    python -m pip install -r web_ui/requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install web UI requirements" -ForegroundColor Red
        return $false
    }
    
    Write-Host "[OK] Dependencies installed successfully" -ForegroundColor Green
    return $true
}

# Function to show help
function Show-Help {
    Write-Host @"
Hassaniya Text Normalizer - PowerShell Interface

USAGE:
    .\hassaniya.ps1 <action> [options]

ACTIONS:
    web         Launch the custom web interface (recommended)
    gradio      Launch the Gradio interface
    normalize   Normalize a text file from command line
    install     Install/update dependencies
    help        Show this help message

EXAMPLES:
    .\hassaniya.ps1 web
    .\hassaniya.ps1 gradio
    .\hassaniya.ps1 normalize -InputFile "input.txt" -OutputFile "output.txt"
    .\hassaniya.ps1 normalize -InputFile "input.txt" -OutputFile "output.txt" -ShowDiff
    .\hassaniya.ps1 install

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

"@ -ForegroundColor Cyan
}

# Main script logic
switch ($Action) {
    'help' {
        Show-Help
        exit 0
    }
    
    'install' {
        if (-not (Test-PythonInstalled)) {
            exit 1
        }
        
        if (Install-Dependencies) {
            Write-Host "`n[OK] Installation complete! You can now run:" -ForegroundColor Green
            Write-Host "    .\hassaniya.ps1 web" -ForegroundColor Cyan
        } else {
            Write-Host "`n[ERROR] Installation failed" -ForegroundColor Red
            exit 1
        }
        exit 0
    }
    
    'web' {
        Write-Host "Starting Hassaniya Text Normalizer Web Interface..." -ForegroundColor Cyan
        
        if (-not (Test-PythonInstalled)) {
            exit 1
        }
        
        if (-not (Test-DependenciesInstalled)) {
            Write-Host "Installing missing dependencies..." -ForegroundColor Yellow
            if (-not (Install-Dependencies)) {
                exit 1
            }
        }
        
        Write-Host "`nWeb interface will open at: http://localhost:5000" -ForegroundColor Green
        Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
        Write-Host "" # Empty line
        
        python web_ui/server.py
    }
    
    'gradio' {
        Write-Host "Starting Hassaniya Text Normalizer Gradio Interface..." -ForegroundColor Cyan
        
        if (-not (Test-PythonInstalled)) {
            exit 1
        }
        
        if (-not (Test-DependenciesInstalled)) {
            Write-Host "Installing missing dependencies..." -ForegroundColor Yellow
            if (-not (Install-Dependencies)) {
                exit 1
            }
        }
        
        Write-Host "`nGradio interface will open automatically in your browser" -ForegroundColor Green
        Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
        Write-Host "" # Empty line
        
        python app/gradio_ui.py
    }
    
    'normalize' {
        if (-not $InputFile -or -not $OutputFile) {
            Write-Host "[ERROR] InputFile and OutputFile are required for normalize action" -ForegroundColor Red
            Write-Host "Usage: .\hassaniya.ps1 normalize -InputFile 'input.txt' -OutputFile 'output.txt'" -ForegroundColor Yellow
            exit 1
        }
        
        if (-not (Test-Path $InputFile)) {
            Write-Host "[ERROR] Input file '$InputFile' does not exist" -ForegroundColor Red
            exit 1
        }
        
        if (-not (Test-PythonInstalled)) {
            exit 1
        }
        
        Write-Host "Normalizing text from '$InputFile' to '$OutputFile'..." -ForegroundColor Cyan
        
        $args = @("--in", $InputFile, "--out", $OutputFile)
        if ($ShowDiff) {
            $args += "--show-diff"
        }
        
        python -m cli.normalize_text @args
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Text normalization completed successfully" -ForegroundColor Green
        } else {
            Write-Host "[ERROR] Text normalization failed" -ForegroundColor Red
            exit 1
        }
    }
    
    default {
        Write-Host "[ERROR] Unknown action: $Action" -ForegroundColor Red
        Show-Help
        exit 1
    }
}