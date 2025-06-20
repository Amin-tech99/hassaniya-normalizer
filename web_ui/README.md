# Hassaniya Text Normalizer - Custom Web UI

This is a custom web interface for the Hassaniya Text Normalizer, built with HTML, CSS, JavaScript, and Flask. It provides a modern, responsive alternative to the Gradio interface.

## Features

### 🎯 Text Normalizer
- Normalize Hassaniya Arabic text using letter-level rules and variant mappings
- Optional diff highlighting to show changes
- Real-time unknown variants detection
- Keyboard shortcuts (Ctrl+Enter to normalize)

### 📝 Variant Manager
- Add new canonical words and their variants
- Duplicate detection and prevention
- Automatic cache refresh after additions
- Form validation and error handling

### 🔗 Word Separation Manager
- Manage words that should be linked but are sometimes separated
- Add pairs like "في ما" → "فيما"
- Comprehensive duplicate checking
- Real-time status feedback

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   python server.py
   ```

3. **Open your browser:**
   Navigate to `http://localhost:5000`

## Usage

### Text Normalization
1. Go to the "Text Normalizer" tab
2. Enter your Hassaniya text in the input area
3. Optionally check "Show differences" for highlighted changes
4. Click "Normalize" or press Ctrl+Enter
5. View the normalized text and any unknown variants found

### Adding Variants
1. Go to the "Variant Manager" tab
2. Enter the canonical (standard) form of the word
3. Enter variants separated by commas
4. Click "Add Variant"
5. The system will check for duplicates and save if valid

### Adding Word Separations
1. Go to the "Word Separation Manager" tab
2. Enter the separated form (e.g., "في ما")
3. Enter the correct linked form (e.g., "فيما")
4. Click "Add Separation Pair"
5. The system will validate and save the pair

## API Endpoints

The Flask server provides the following REST API endpoints:

- `POST /api/normalize` - Normalize text
- `POST /api/add-variant` - Add new variant
- `POST /api/add-separation` - Add new separation pair

## File Structure

```
web_ui/
├── index.html          # Main HTML interface
├── styles.css          # CSS styling
├── script.js           # JavaScript functionality
├── server.py           # Flask backend server
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Features

### 🎨 Modern Design
- Responsive layout that works on desktop and mobile
- Beautiful gradient backgrounds and smooth animations
- Clean, professional interface with intuitive navigation
- Loading states and visual feedback

### 🚀 Performance
- Fast, lightweight interface
- Efficient API communication
- Real-time validation and feedback
- Keyboard shortcuts for power users

### 🛡️ Robust Error Handling
- Comprehensive input validation
- Duplicate detection and prevention
- Clear error messages and status updates
- Graceful handling of network errors

### 📱 User Experience
- Tab-based navigation
- Form auto-focus and Enter key support
- Visual diff highlighting
- Status indicators and success messages

## Keyboard Shortcuts

- **Ctrl+Enter** in text area: Normalize text
- **Enter** in canonical word field: Move to variants field
- **Ctrl+Enter** in variants field: Add variant
- **Enter** in separated form field: Move to linked form field
- **Enter** in linked form field: Add separation pair

## Troubleshooting

### Server won't start
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that port 5000 is not in use by another application
- Ensure you're in the correct directory when running `python server.py`

### API errors
- Check the server console for error messages
- Ensure the normalizer module is properly installed
- Verify that data files are accessible and writable

### Interface not loading
- Clear your browser cache
- Check browser console for JavaScript errors
- Ensure the server is running and accessible

## Development

To modify the interface:

1. **HTML structure**: Edit `index.html`
2. **Styling**: Modify `styles.css`
3. **Functionality**: Update `script.js`
4. **Backend logic**: Change `server.py`

The server runs in debug mode by default, so changes to Python files will automatically reload the server.

## Comparison with Gradio

| Feature | Custom UI | Gradio UI |
|---------|-----------|----------|
| Performance | ⚡ Fast | 🐌 Slower |
| Customization | 🎨 Full control | 🔒 Limited |
| Dependencies | 📦 Minimal | 📚 Heavy |
| Mobile support | 📱 Responsive | 📱 Basic |
| Loading speed | 🚀 Instant | ⏳ Slower |
| UI flexibility | ✅ Complete | ❌ Restricted |

This custom interface provides better performance, more flexibility, and a superior user experience compared to the Gradio-based interface.