"""Command-line interface for Hassaniya text normalization.

Usage:
    python -m cli.normalize_text --in input.txt --out output.txt [--show-diff]
"""

import argparse
import difflib
import sys
from pathlib import Path
from typing import List

# Add parent directory to path to import normalizer
sys.path.insert(0, str(Path(__file__).parent.parent))

from normalizer import normalize_text, unknown_variants, clear_unknown_variants, reload_data


def highlight_diff(original: str, normalized: str) -> str:
    """Generate a highlighted diff between original and normalized text.
    
    Args:
        original: The original text.
        normalized: The normalized text.
        
    Returns:
        A string showing the differences with highlighting.
    """
    diff = list(difflib.unified_diff(
        original.splitlines(keepends=True),
        normalized.splitlines(keepends=True),
        fromfile='Original',
        tofile='Normalized',
        lineterm=''
    ))
    
    if not diff:
        return "No differences found."
    
    return ''.join(diff)


def main() -> None:
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description='Normalize Hassaniya Arabic text using letter rules and variant mappings.'
    )
    parser.add_argument(
        '--in', '--input',
        dest='input_file',
        required=True,
        help='Input text file to normalize'
    )
    parser.add_argument(
        '--out', '--output',
        dest='output_file',
        required=True,
        help='Output file for normalized text'
    )
    parser.add_argument(
        '--show-diff',
        action='store_true',
        help='Show differences between original and normalized text'
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    # Read input file
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            original_text = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Reload data to ensure we're using the latest files
    reload_data()
    
    # Clear previous unknown variants
    clear_unknown_variants()
    
    # Normalize text
    normalized_text = normalize_text(original_text)
    
    # Write output file
    output_path = Path(args.output_file)
    try:
        # Create parent directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(normalized_text)
        
        print(f"Normalized text written to '{output_path}'")
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Show diff if requested
    if args.show_diff:
        print("\n" + "="*50)
        print("DIFFERENCES:")
        print("="*50)
        diff_output = highlight_diff(original_text, normalized_text)
        print(diff_output)
    
    # Log unknown variants
    if unknown_variants:
        print("\n" + "="*50)
        print("UNKNOWN VARIANTS ENCOUNTERED:")
        print("="*50)
        for variant in unknown_variants:
            print(f"  - {variant}")
        print(f"\nTotal unknown variants: {len(unknown_variants)}")
    else:
        print("\nNo unknown variants encountered.")


if __name__ == '__main__':
    main()