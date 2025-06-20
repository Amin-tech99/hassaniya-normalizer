"""Gradio web interface for Hassaniya text normalization.

Provides a simple web UI for normalizing Hassaniya text with optional diff display.
"""

import gradio as gr
import sys
import json
import os
from pathlib import Path
from typing import Tuple, Dict, List

# Add parent directory to path to import normalizer
sys.path.insert(0, str(Path(__file__).parent.parent))

from normalizer import normalize_text, unknown_variants, clear_unknown_variants, reload_data


def load_variants_data() -> List[Dict[str, any]]:
    """Load all variant data from the JSONL file.
    
    Returns:
        List of dictionaries containing canonical and variants data.
    """
    variants_data = []
    try:
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        variants_file = os.path.join(current_dir, 'data', 'hassaniya_variants.jsonl')
        with open(variants_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    variants_data.append(json.loads(line))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return variants_data


def load_separation_data() -> List[Dict[str, str]]:
    """Load all word separation data from the JSONL file.
    
    Returns:
        List of dictionaries containing separated and linked word pairs.
    """
    separation_data = []
    try:
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        separation_file = os.path.join(current_dir, 'data', 'word_separation.jsonl')
        with open(separation_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    separation_data.append(json.loads(line))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return separation_data


def save_variants_data(variants_data: List[Dict[str, any]]) -> None:
    """Save variant data to the JSONL file.
    
    Args:
        variants_data: List of dictionaries containing canonical and variants data.
    """
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    variants_file = os.path.join(current_dir, 'data', 'hassaniya_variants.jsonl')
    with open(variants_file, 'w', encoding='utf-8') as f:
        for entry in variants_data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def save_separation_data(separation_data: List[Dict[str, str]]) -> None:
    """Save word separation data to the JSONL file.
    
    Args:
        separation_data: List of dictionaries containing separated and linked word pairs.
    """
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    separation_file = os.path.join(current_dir, 'data', 'word_separation.jsonl')
    with open(separation_file, 'w', encoding='utf-8') as f:
        for entry in separation_data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def check_word_exists(word: str, variants_data: List[Dict[str, any]]) -> Tuple[bool, str]:
    """Check if a word exists as canonical or variant.
    
    Args:
        word: Word to check.
        variants_data: List of variant entries.
        
    Returns:
        Tuple of (exists, message).
    """
    word = word.strip()
    if not word:
        return False, ""
    
    for entry in variants_data:
        if entry['canonical'] == word:
            return True, f"'{word}' already exists as a canonical word."
        if word in entry['variants']:
            return True, f"'{word}' already exists as a variant of '{entry['canonical']}'."
    
    return False, ""


def clear_normalizer_cache() -> None:
    """Clear the normalizer's variant cache to reload updated data."""
    try:
        from normalizer.normalizer import _variant_dict
        _variant_dict.clear()
    except ImportError:
        pass


def check_separation_exists(separated: str, linked: str, separation_data: List[Dict[str, str]]) -> Tuple[bool, str]:
    """Check if a word separation pair already exists.
    
    Args:
        separated: The separated form to check.
        linked: The linked form to check.
        separation_data: List of separation entries.
        
    Returns:
        Tuple of (exists, message).
    """
    separated = separated.strip()
    linked = linked.strip()
    
    if not separated or not linked:
        return False, ""
    
    for entry in separation_data:
        if entry['separated'] == separated:
            return True, f"'{separated}' already exists as a separated form."
        if entry['linked'] == linked:
            return True, f"'{linked}' already exists as a linked form."
        if entry['separated'] == linked:
            return True, f"'{linked}' already exists as a separated form."
        if entry['linked'] == separated:
            return True, f"'{separated}' already exists as a linked form."
    
    return False, ""


def add_new_separation(separated: str, linked: str) -> str:
    """Add a new word separation pair.
    
    Args:
        separated: The separated form of the word(s).
        linked: The linked (correct) form of the word(s).
        
    Returns:
        Status message.
    """
    separated = separated.strip()
    linked = linked.strip()
    
    if not separated:
        return "❌ Please enter the separated form."
    
    if not linked:
        return "❌ Please enter the linked form."
    
    if separated == linked:
        return "❌ Separated and linked forms cannot be the same."
    
    # Load current data
    separation_data = load_separation_data()
    
    # Check if either form already exists
    exists, message = check_separation_exists(separated, linked, separation_data)
    if exists:
        return f"❌ {message}"
    
    # Add new entry
    new_entry = {
        "separated": separated,
        "linked": linked
    }
    separation_data.append(new_entry)
    
    # Save to file
    try:
        save_separation_data(separation_data)
        return f"✅ Successfully added separation pair: '{separated}' → '{linked}'"
    except Exception as e:
        return f"❌ Error saving data: {str(e)}"


def add_new_variant(canonical: str, variants: str) -> str:
    """Add a new canonical word with its variants.
    
    Args:
        canonical: The canonical form of the word.
        variants: Comma-separated list of variants.
        
    Returns:
        Status message.
    """
    canonical = canonical.strip()
    if not canonical:
        return "❌ Please enter a canonical word."
    
    # Parse variants
    variant_list = [v.strip() for v in variants.split(',') if v.strip()]
    if not variant_list:
        return "❌ Please enter at least one variant."
    
    # Load current data
    variants_data = load_variants_data()
    
    # Check if canonical word already exists
    exists, message = check_word_exists(canonical, variants_data)
    if exists:
        return f"❌ {message}"
    
    # Check if any variant already exists
    for variant in variant_list:
        exists, message = check_word_exists(variant, variants_data)
        if exists:
            return f"❌ {message}"
    
    # Add new entry
    new_entry = {
        "canonical": canonical,
        "variants": variant_list
    }
    variants_data.append(new_entry)
    
    # Save to file
    try:
        save_variants_data(variants_data)
        # Clear the normalizer cache so it reloads the updated data
        clear_normalizer_cache()
        return f"✅ Successfully added '{canonical}' with variants: {', '.join(variant_list)}"
    except Exception as e:
        return f"❌ Error saving data: {str(e)}"


def highlight_changes(original: str, normalized: str) -> str:
    """Create HTML highlighting differences between original and normalized text.
    
    Args:
        original: The original text.
        normalized: The normalized text.
        
    Returns:
        HTML string with highlighted differences.
    """
    if original == normalized:
        return normalized
    
    # Simple word-by-word comparison for highlighting
    original_words = original.split()
    normalized_words = normalized.split()
    
    result_words = []
    max_len = max(len(original_words), len(normalized_words))
    
    for i in range(max_len):
        orig_word = original_words[i] if i < len(original_words) else ""
        norm_word = normalized_words[i] if i < len(normalized_words) else ""
        
        if orig_word != norm_word:
            if norm_word:
                result_words.append(f'<mark style="background-color: #ffeb3b;">{norm_word}</mark>')
        else:
            result_words.append(norm_word)
    
    return ' '.join(result_words)


def normalize_with_options(text: str, show_diff: bool) -> Tuple[str, str]:
    """Normalize text and optionally show differences.
    
    Args:
        text: Input text to normalize.
        show_diff: Whether to highlight differences.
        
    Returns:
        Tuple of (normalized_text, unknown_variants_info).
    """
    if not text.strip():
        return "", "No text provided."
    
    # Reload data to ensure we're using the latest files
    reload_data()
    
    # Clear previous unknown variants
    clear_unknown_variants()
    
    # Normalize the text
    normalized = normalize_text(text)
    
    # Prepare output
    if show_diff:
        output = highlight_changes(text, normalized)
    else:
        output = normalized
    
    # Prepare unknown variants info
    if unknown_variants:
        variants_info = f"Unknown variants found: {', '.join(unknown_variants[:10])}"
        if len(unknown_variants) > 10:
            variants_info += f" ... and {len(unknown_variants) - 10} more"
    else:
        variants_info = "No unknown variants found."
    
    return output, variants_info


def create_interface() -> gr.Interface:
    """Create and configure the Gradio interface.
    
    Returns:
        Configured Gradio interface.
    """
    with gr.Blocks(title="Hassaniya Text Normalizer") as interface:
        gr.Markdown(
            """
            # Hassaniya Text Normalizer
            
            This tool normalizes Hassaniya Arabic text using:
            - **Letter-level rules**: گ/ق → ك (with exceptions), final ة → ه
            - **Variant mappings**: Common word variants → canonical forms
            
            Enter your text below and click "Normalize" to process it.
            """
        )
        
        with gr.Tabs():
            with gr.TabItem("Text Normalizer"):
                with gr.Row():
                    with gr.Column():
                        input_text = gr.Textbox(
                            label="Input Text",
                            placeholder="Enter Hassaniya text to normalize...",
                            lines=5,
                            max_lines=10
                        )
                        
                        show_diff = gr.Radio(
                            choices=["No", "Yes"],
                            value="No",
                            label="Show differences (highlighted)"
                        )
                        
                        normalize_btn = gr.Button("Normalize", variant="primary")
                    
                    with gr.Column():
                        output_text = gr.HTML(
                            label="Normalized Text",
                            value="Normalized text will appear here..."
                        )
                        
                        variants_info = gr.Textbox(
                            label="Unknown Variants",
                            value="Unknown variants info will appear here...",
                            interactive=False,
                            lines=2
                        )
                
                # Examples
                gr.Markdown("### Examples")
                examples = [
                    ["هاذا النص يحتاج تطبيع", "No"],
                    ["الي يقول هاذا الكلام", "Yes"],
                    ["شنه رايك في هاذ الموضوع؟", "Yes"]
                ]
                
                gr.Examples(
                    examples=examples,
                    inputs=[input_text, show_diff],
                    outputs=[output_text, variants_info],
                    fn=lambda text, diff: normalize_with_options(text, diff == "Yes"),
                    cache_examples=False
                )
                
                # Connect the normalize button
                normalize_btn.click(
                    fn=lambda text, diff: normalize_with_options(text, diff == "Yes"),
                    inputs=[input_text, show_diff],
                    outputs=[output_text, variants_info]
                )
            
            with gr.TabItem("Variant Manager"):
                gr.Markdown(
                    """
                    ### Add New Word Variants
                    
                    Use this section to add new canonical words and their variants to the normalizer database.
                    The system will check for duplicates and prevent adding existing words.
                    """
                )
                
                with gr.Row():
                    with gr.Column():
                        canonical_input = gr.Textbox(
                            label="Canonical Word",
                            placeholder="Enter the canonical (standard) form of the word...",
                            lines=1
                        )
                        
                        variants_input = gr.Textbox(
                            label="Variants",
                            placeholder="Enter variants separated by commas (e.g., الي, ألي, إلي)...",
                            lines=2
                        )
                        
                        add_variant_btn = gr.Button("Add Variant", variant="primary")
                    
                    with gr.Column():
                        status_output = gr.Textbox(
                            label="Status",
                            value="Ready to add new variants...",
                            interactive=False,
                            lines=3
                        )
                
                # Connect the add variant button
                add_variant_btn.click(
                    fn=add_new_variant,
                    inputs=[canonical_input, variants_input],
                    outputs=[status_output]
                )
            
            with gr.TabItem("Word Separation Manager"):
                gr.Markdown(
                    """
                    ### Add Word Separation Pairs
                    
                    Use this section to add pairs of words that are sometimes written separately but should be linked together.
                    For example: "في ما" should be linked as "فيما".
                    The system will check for duplicates and prevent adding existing pairs.
                    """
                )
                
                with gr.Row():
                    with gr.Column():
                        separated_input = gr.Textbox(
                            label="Separated Form",
                            placeholder="Enter the separated form (e.g., في ما)...",
                            lines=1
                        )
                        
                        linked_input = gr.Textbox(
                            label="Linked Form",
                            placeholder="Enter the correct linked form (e.g., فيما)...",
                            lines=1
                        )
                        
                        add_separation_btn = gr.Button("Add Separation Pair", variant="primary")
                    
                    with gr.Column():
                        separation_status_output = gr.Textbox(
                            label="Status",
                            value="Ready to add new word separation pairs...",
                            interactive=False,
                            lines=3
                        )
                
                # Connect the add separation button
                add_separation_btn.click(
                    fn=add_new_separation,
                    inputs=[separated_input, linked_input],
                    outputs=[separation_status_output]
                )
    
    return interface


def main() -> None:
    """Main function for command line entry point."""
    print("🚀 Starting Hassaniya Text Normalizer Gradio Interface...")
    print("📱 Gradio interface will open automatically in your browser")
    print("Press Ctrl+C to stop the server")
    print()
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()