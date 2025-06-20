#!/usr/bin/env python3
"""
Flask web server for the Hassaniya Text Normalizer custom UI.
Provides API endpoints for text normalization and data management.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Add parent directory to path to import normalizer
sys.path.insert(0, str(Path(__file__).parent.parent))

from normalizer import normalize_text, unknown_variants, clear_unknown_variants

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
DATA_DIR = Path(os.environ.get('HASSANIYA_DATA_DIR', Path(__file__).parent.parent / 'data'))
VARIANTS_FILE = DATA_DIR / 'hassaniya_variants.jsonl'
WORD_SEPARATION_FILE = DATA_DIR / 'word_separation.jsonl'

# Get port from environment variable or use default
PORT = int(os.environ.get('HASSANIYA_PORT', 5000))


def load_variants_data() -> List[Dict[str, any]]:
    """Load all variant data from the JSONL file."""
    variants_data = []
    try:
        with open(VARIANTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    variants_data.append(json.loads(line))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return variants_data


def save_variants_data(variants_data: List[Dict[str, any]]) -> None:
    """Save variant data to the JSONL file."""
    with open(VARIANTS_FILE, 'w', encoding='utf-8') as f:
        for entry in variants_data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def load_separation_data() -> List[Dict[str, str]]:
    """Load all word separation data from the JSONL file."""
    separation_data = []
    try:
        with open(WORD_SEPARATION_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    separation_data.append(json.loads(line))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return separation_data


def save_separation_data(separation_data: List[Dict[str, str]]) -> None:
    """Save separation data to the JSONL file."""
    with open(WORD_SEPARATION_FILE, 'w', encoding='utf-8') as f:
        for entry in separation_data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def create_diff_html(original: str, normalized: str) -> str:
    """Create HTML with highlighted differences between original and normalized text."""
    if original == normalized:
        return normalized
    
    # Simple word-by-word diff
    original_words = original.split()
    normalized_words = normalized.split()
    
    result = []
    i = j = 0
    
    while i < len(original_words) and j < len(normalized_words):
        if original_words[i] == normalized_words[j]:
            result.append(original_words[i])
            i += 1
            j += 1
        else:
            # Find next matching word
            found_match = False
            for k in range(j + 1, min(j + 5, len(normalized_words))):
                if k < len(normalized_words) and i < len(original_words) and original_words[i] == normalized_words[k]:
                    # Add changed words
                    for l in range(j, k):
                        result.append(f'<span class="diff-added">{normalized_words[l]}</span>')
                    result.append(f'<span class="diff-removed">{original_words[i]}</span>')
                    result.append(normalized_words[k])
                    i += 1
                    j = k + 1
                    found_match = True
                    break
            
            if not found_match:
                # Simple replacement
                result.append(f'<span class="diff-removed">{original_words[i]}</span>')
                result.append(f'<span class="diff-added">{normalized_words[j]}</span>')
                i += 1
                j += 1
    
    # Add remaining words
    while i < len(original_words):
        result.append(f'<span class="diff-removed">{original_words[i]}</span>')
        i += 1
    
    while j < len(normalized_words):
        result.append(f'<span class="diff-added">{normalized_words[j]}</span>')
        j += 1
    
    return ' '.join(result)


@app.route('/')
def index():
    """Serve the main HTML page."""
    return send_from_directory('.', 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files (CSS, JS)."""
    return send_from_directory('.', filename)


@app.route('/api/normalize', methods=['POST'])
def api_normalize():
    """Normalize text and return results."""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        show_diff = data.get('show_diff', False)
        
        # Clear previous unknown variants
        clear_unknown_variants()
        
        # Normalize the text
        normalized = normalize_text(text)
        
        # Get unknown variants
        variants = list(unknown_variants) if unknown_variants else []
        
        response = {
            'normalized_text': normalized,
            'unknown_variants': variants
        }
        
        # Add diff HTML if requested
        if show_diff:
            response['diff_html'] = create_diff_html(text, normalized)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/add-variant', methods=['POST'])
def api_add_variant():
    """Add a new variant to the database."""
    try:
        data = request.get_json()
        if not data or 'canonical' not in data or 'variants' not in data:
            return jsonify({'success': False, 'message': 'Missing canonical word or variants'}), 400
        
        canonical = data['canonical'].strip()
        variants = [v.strip() for v in data['variants'] if v.strip()]
        
        if not canonical or not variants:
            return jsonify({'success': False, 'message': 'Canonical word and variants cannot be empty'})
        
        # Load existing data
        variants_data = load_variants_data()
        
        # Check for duplicates
        for entry in variants_data:
            if entry['canonical'] == canonical:
                return jsonify({'success': False, 'message': f'Canonical word "{canonical}" already exists'})
            
            # Check if any variant already exists
            for variant in variants:
                if variant in entry['variants'] or variant == entry['canonical']:
                    return jsonify({'success': False, 'message': f'Variant "{variant}" already exists'})
        
        # Add new entry
        new_entry = {'canonical': canonical, 'variants': variants}
        variants_data.append(new_entry)
        
        # Save to file
        save_variants_data(variants_data)
        
        # Clear normalizer cache
        clear_unknown_variants()
        
        return jsonify({
            'success': True, 
            'message': f'Successfully added canonical word "{canonical}" with {len(variants)} variant(s)'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/api/add-separation', methods=['POST'])
def api_add_separation():
    """Add a new word separation pair to the database."""
    try:
        data = request.get_json()
        if not data or 'separated' not in data or 'linked' not in data:
            return jsonify({'success': False, 'message': 'Missing separated or linked form'}), 400
        
        separated = data['separated'].strip()
        linked = data['linked'].strip()
        
        if not separated or not linked:
            return jsonify({'success': False, 'message': 'Separated and linked forms cannot be empty'})
        
        if separated == linked:
            return jsonify({'success': False, 'message': 'Separated and linked forms cannot be the same'})
        
        # Load existing data
        separation_data = load_separation_data()
        
        # Check for duplicates
        for entry in separation_data:
            if entry['separated'] == separated:
                return jsonify({'success': False, 'message': f'Separated form "{separated}" already exists'})
            if entry['linked'] == linked:
                return jsonify({'success': False, 'message': f'Linked form "{linked}" already exists as a linked form'})
            if entry['separated'] == linked:
                return jsonify({'success': False, 'message': f'Form "{linked}" already exists as a separated form'})
            if entry['linked'] == separated:
                return jsonify({'success': False, 'message': f'Form "{separated}" already exists as a linked form'})
        
        # Add new entry
        new_entry = {'separated': separated, 'linked': linked}
        separation_data.append(new_entry)
        
        # Save to file
        save_separation_data(separation_data)
        
        return jsonify({
            'success': True, 
            'message': f'Successfully added separation pair: "{separated}" → "{linked}"'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


def main():
    """Main function for command line entry point."""
    print("🚀 Starting Hassaniya Text Normalizer Web Interface...")
    print(f"📱 Web interface available at: http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    print()
    app.run(debug=True, host='0.0.0.0', port=PORT)


if __name__ == '__main__':
    # Ensure data directory exists
    DATA_DIR.mkdir(exist_ok=True)
    
    print("Starting Hassaniya Text Normalizer Web Server...")
    print(f"Data directory: {DATA_DIR}")
    print(f"Variants file: {VARIANTS_FILE}")
    print(f"Separation file: {WORD_SEPARATION_FILE}")
    print(f"\nServer will be available at: http://localhost:{PORT}")
    
    main()