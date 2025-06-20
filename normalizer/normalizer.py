"""Core normalization algorithms for Hassaniya text.

This module provides the main normalization functions that combine
variant lookups with letter-level rules.
"""

import json
from typing import Dict, List
from importlib import resources
from .rules import apply_letter_rules

# Global variables for caching
_variant_dict: Dict[str, str] = {}
unknown_variants: List[str] = []


def load_variants() -> Dict[str, str]:
    """Load variant mappings from JSONL file.
    
    Returns:
        Dictionary mapping variant words to their canonical forms.
    """
    global _variant_dict
    if not _variant_dict:
        try:
            # Try to load from package data first
            try:
                with resources.open_text('data', 'hassaniya_variants.jsonl') as f:
                    lines = f.readlines()
            except (FileNotFoundError, ModuleNotFoundError):
                # Fallback to relative path
                import os
                current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                variants_file = os.path.join(current_dir, 'data', 'hassaniya_variants.jsonl')
                with open(variants_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if line:
                    entry = json.loads(line)
                    canonical = entry['canonical']
                    for variant in entry['variants']:
                        _variant_dict[variant] = canonical
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is malformed, use empty dict
            _variant_dict = {}
    
    return _variant_dict


def normalize_word(word: str) -> str:
    """Normalize a single word using variant lookup and letter rules.
    
    Workflow:
    1. Check if word exists in variant dictionary
    2. If found, return canonical form
    3. If not found, apply letter-level rules
    4. Track unknown variants for logging
    
    Args:
        word: The word to normalize.
        
    Returns:
        The normalized word.
    """
    if not word:
        return word
    
    # Remove punctuation for lookup but preserve it
    punctuation = '.,!?;:()[]{}"\'\''
    clean_word = word.strip(punctuation)
    prefix = word[:len(word) - len(word.lstrip(punctuation))]
    suffix = word[len(clean_word) + len(prefix):]
    
    if not clean_word:
        return word
    
    variants = load_variants()
    
    # Step 1: Check variant dictionary
    if clean_word in variants:
        return prefix + variants[clean_word] + suffix
    
    # Step 2: Apply letter rules
    normalized = apply_letter_rules(clean_word)
    
    # Step 3: Track unknown variants (words that weren't in dictionary)
    if clean_word not in unknown_variants and clean_word != normalized:
        unknown_variants.append(clean_word)
    
    return prefix + normalized + suffix


def normalize_text(text: str) -> str:
    """Normalize a complete text by processing each word.
    
    Args:
        text: The text to normalize.
        
    Returns:
        The normalized text.
    """
    if not text:
        return text
    
    # Split on whitespace and normalize each word
    words = text.split()
    normalized_words = [normalize_word(word) for word in words]
    
    return ' '.join(normalized_words)


def clear_unknown_variants() -> None:
    """Clear the list of unknown variants.
    
    Useful for resetting the tracking between different normalization sessions.
    """
    global unknown_variants
    unknown_variants.clear()