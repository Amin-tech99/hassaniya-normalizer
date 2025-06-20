# GitHub Deployment Guide

This guide explains how to deploy the Hassaniya Text Normalizer to GitHub and make it accessible to anyone via PowerShell commands.

## 🚀 Quick Deployment Steps

### 1. Prepare Your Repository

1. **Initialize Git (if not already done):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Hassaniya Text Normalizer with PowerShell interface"
   ```

2. **Create a GitHub repository:**
   - Go to [GitHub](https://github.com) and create a new repository
   - Name it `hassaniya-normalizer` (or your preferred name)
   - Don't initialize with README (since you already have one)

3. **Connect and push to GitHub:**
   ```bash
   git remote add origin https://github.com/yourusername/hassaniya-normalizer.git
   git branch -M main
   git push -u origin main
   ```

### 2. Update Repository URLs

After creating your GitHub repository, update the following files with your actual GitHub username:

- `README.md` - Replace `yourusername` with your GitHub username
- `setup.py` - Update the `url` field with your repository URL

### 3. Test the Deployment

Once pushed to GitHub, anyone can use your normalizer by:

```powershell
# Clone the repository
git clone https://github.com/yourusername/hassaniya-normalizer.git
cd hassaniya-normalizer

# Install and run
.\hassaniya.ps1 install
.\hassaniya.ps1 web
```

## 📋 What Users Get

### Easy PowerShell Commands

Users can access all functionality through simple commands:

```powershell
# Launch web interface for adding variants
.\hassaniya.ps1 web

# Launch Gradio interface
.\hassaniya.ps1 gradio

# Normalize text files
.\hassaniya.ps1 normalize -InputFile "input.txt" -OutputFile "output.txt"

# Install dependencies automatically
.\hassaniya.ps1 install
```

### Web Interface Features

- **Text Normalizer**: Normalize Hassaniya Arabic text with real-time preview
- **Variant Manager**: Add new word variants easily
- **Word Separation Manager**: Manage word separation pairs
- **Dark Theme**: Modern, eye-friendly interface
- **Diff Visualization**: See exactly what changes were made

### Data Management

Users can easily add new words and variants through:

1. **Web Interface**: User-friendly forms for adding variants
2. **Direct File Editing**: Edit JSON/JSONL files directly
3. **API Endpoints**: Programmatic access for bulk operations

## 🔧 Advanced Configuration

### Environment Variables

Users can customize behavior with environment variables:

```powershell
# Set custom data directory
$env:HASSANIYA_DATA_DIR = "C:\MyCustomData"

# Set custom port for web interface
$env:HASSANIYA_PORT = "8080"
```

### Custom Data Files

Users can provide their own data files:

- `data/hassaniya_variants.jsonl` - Word variant mappings
- `data/word_separation.jsonl` - Word separation pairs
- `data/exception_words_g_q.json` - Exception words for گ/ق rules

## 📊 Usage Analytics

### File Structure After Installation

```
hassaniya-normalizer/
├── hassaniya.ps1          # PowerShell interface
├── hassaniya.bat          # Batch interface
├── setup.py               # Package installation
├── requirements.txt       # Dependencies
├── data/                  # Data files
│   ├── hassaniya_variants.jsonl
│   ├── word_separation.jsonl
│   └── exception_words_g_q.json
├── web_ui/               # Custom web interface
├── app/                  # Gradio interface
├── cli/                  # Command-line tools
├── normalizer/           # Core library
└── tests/                # Test suite
```

### User Workflow

1. **Clone repository** from GitHub
2. **Run installation** with `hassaniya.ps1 install`
3. **Launch web interface** with `hassaniya.ps1 web`
4. **Add new variants** through the web interface
5. **Normalize text** via web UI or command line
6. **Share improvements** by contributing back to the repository

## 🤝 Contributing Guidelines

### For Repository Maintainers

1. **Accept Pull Requests**: Review and merge variant additions
2. **Update Documentation**: Keep README and guides current
3. **Release Management**: Tag versions and create releases
4. **Issue Management**: Help users with problems

### For Users Contributing Variants

1. **Fork the repository**
2. **Add variants** through the web interface or direct file editing
3. **Test your changes** with the provided test suite
4. **Submit a pull request** with your improvements

## 🔒 Security Considerations

- **No sensitive data**: The repository contains only linguistic data
- **Safe execution**: PowerShell scripts include input validation
- **Local operation**: All processing happens locally on user's machine
- **Open source**: All code is transparent and auditable

## 📈 Scaling and Performance

- **Lightweight**: Minimal dependencies and fast startup
- **Efficient**: Optimized for large text processing
- **Extensible**: Easy to add new languages or rules
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🆘 Support and Troubleshooting

### Common Issues

1. **Python not found**: Install Python 3.8+ from python.org
2. **Dependencies missing**: Run `hassaniya.ps1 install`
3. **Port conflicts**: Change port in web_ui/server.py
4. **Permission errors**: Run PowerShell as administrator

### Getting Help

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check README.md and DEPLOYMENT.md
- **Community**: Engage with other users in discussions

---

**Ready to deploy?** Follow the steps above and share your Hassaniya Text Normalizer with the world! 🌍