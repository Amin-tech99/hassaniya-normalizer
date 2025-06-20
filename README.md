# Hassaniya Normalizer

A production-ready Python package for normalizing Hassaniya Arabic text using letter-level rules and variant mappings.

## Features

- **Letter-level normalization**: Converts گ/ق → ك (with exception handling) and final ة → ه
- **Variant mappings**: Maps common Hassaniya variants to their canonical forms
- **CLI interface**: Command-line tool for batch text processing
- **Web interface**: Gradio-based demo with diff visualization
- **Extensible**: Easy to add new variants and exception words

## Installation

### Quick Start with PowerShell (Windows)

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/yourusername/hassaniya-normalizer.git
   cd hassaniya-normalizer
   ```

2. **Install dependencies and launch:**
   ```powershell
   .\hassaniya.ps1 install
   .\hassaniya.ps1 web
   ```

### Quick Start with Batch (Windows)

1. **Clone the repository:**
   ```cmd
   git clone https://github.com/yourusername/hassaniya-normalizer.git
   cd hassaniya-normalizer
   ```

2. **Install dependencies and launch:**
   ```cmd
   hassaniya.bat install
   hassaniya.bat web
   ```

### From Source (Manual)

```bash
git clone https://github.com/yourusername/hassaniya-normalizer.git
cd hassaniya-normalizer
pip install -r requirements.txt
pip install -r web_ui/requirements.txt
```

### As a Package

```bash
pip install git+https://github.com/yourusername/hassaniya-normalizer.git
```

## Usage

### Python API

```python
from normalizer import normalize_text, normalize_word

# Normalize a single word
word = normalize_word("هاذا")
print(word)  # Output: هذا

# Normalize full text
text = "الي يقول هاذا الكلام گتير"
normalized = normalize_text(text)
print(normalized)  # Output: اللي يكول هذا الكلام كتير

# Check unknown variants encountered
from normalizer import unknown_variants
print(unknown_variants)  # List of words not found in variant dictionary
```

### Command Line Interface

#### PowerShell (Windows - Recommended)

```powershell
# Launch web interface
.\hassaniya.ps1 web

# Launch Gradio interface
.\hassaniya.ps1 gradio

# Normalize a text file
.\hassaniya.ps1 normalize -InputFile "input.txt" -OutputFile "output.txt"

# Show differences between original and normalized text
.\hassaniya.ps1 normalize -InputFile "input.txt" -OutputFile "output.txt" -ShowDiff

# Install/update dependencies
.\hassaniya.ps1 install

# Show help
.\hassaniya.ps1 help
```

#### Batch (Windows)

```cmd
# Launch web interface
hassaniya.bat web

# Launch Gradio interface
hassaniya.bat gradio

# Normalize a text file
hassaniya.bat normalize input.txt output.txt

# Show differences
hassaniya.bat normalize input.txt output.txt --show-diff

# Install dependencies
hassaniya.bat install
```

#### Direct Python Commands

```bash
# Normalize a text file
python -m cli.normalize_text --in input.txt --out output.txt

# Show differences between original and normalized text
python -m cli.normalize_text --in input.txt --out output.txt --show-diff

# Launch web interface
python web_ui/server.py

# Launch Gradio interface
python app/gradio_ui.py
```

### Web Interface

```bash
# Launch Gradio demo
python -m app.gradio_ui
```

Then open your browser to `http://localhost:7860`

## Data Files

### Variant Mappings (`data/hassaniya_variants.jsonl`)

Contains mappings from Hassaniya variants to canonical forms:

```json
{"canonical": "هذا", "variants": ["هاذ", "هاذا"]}
{"canonical": "الآن", "variants": ["الان"]}
```

### Exception Words (`data/exception_words_g_q.json`)

List of words that should NOT have گ/ق replaced with ك:

```json
[
  "قرآن",
  "قاموس",
  "گتاب"
]
```

## Normalization Rules

### Letter-Level Rules

1. **گ/ق → ك**: Replace گ and ق with ك, unless the word is in the exception list
2. **Final ة → ه**: Replace word-final ة with ه

### Variant Lookup

1. Check if word exists in variant dictionary
2. If found, return canonical form
3. If not found, apply letter-level rules
4. Track unknown variants for analysis

## Development

### Setup Development Environment

```bash
git clone https://github.com/<user>/hassaniya-normalizer.git
cd hassaniya-normalizer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_normalizer.py -v

# Run with coverage
pytest tests/ --cov=normalizer
```

### Code Quality

```bash
# Lint code
ruff check .

# Format code
ruff format .

# Type checking (optional)
mypy normalizer/
```

### Adding New Variants

1. Edit `data/hassaniya_variants.jsonl`
2. Add new entries in JSONL format:
   ```json
   {"canonical": "canonical_form", "variants": ["variant1", "variant2"]}
   ```
3. Run tests to ensure everything works

### Adding Exception Words

1. Edit `data/exception_words_g_q.json`
2. Add words that should preserve گ/ق:
   ```json
   [
     "existing_word",
     "new_exception_word"
   ]
   ```

## Project Structure

```
hassaniya-normalizer/
│
├── data/
│   ├── hassaniya_variants.jsonl        # Variant mappings
│   └── exception_words_g_q.json        # Exception words for گ/ق rules
│
├── normalizer/                         # Core package
│   ├── __init__.py                     # Package exports
│   ├── rules.py                        # Letter-level rules
│   └── normalizer.py                   # Main normalization logic
│
├── cli/
│   └── normalize_text.py               # Command-line interface
│
├── app/
│   └── gradio_ui.py                    # Web interface
│
├── tests/
│   └── test_normalizer.py              # Test suite
│
├── .github/
│   └── workflows/
│       └── ci.yml                      # GitHub Actions CI
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests and linting: `pytest && ruff check .`
5. Commit your changes: `git commit -m "Add feature"`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## Development Commands Cheatsheet

```bash
# Initialize repository
git init
git add . && git commit -m "🎉 initial Hassaniya normalizer"
gh repo create hassaniya-normalizer --public --source=. --remote=origin
git push -u origin main

# Development workflow
pytest tests/ -v                        # Run tests
ruff check .                            # Lint code
ruff format .                           # Format code
python -m cli.normalize_text --help     # Test CLI
python -m app.gradio_ui                 # Launch web demo
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for the Hassaniya Arabic language community
- Inspired by modern NLP text normalization practices
- Uses Gradio for the web interface