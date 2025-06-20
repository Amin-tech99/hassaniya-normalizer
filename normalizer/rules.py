"""Letter-level normalization rules for Hassaniya text.

This module handles the application of letter-level transformation rules,
including exception handling for specific words.
"""

import json
from typing import Set
from importlib import resources

# Global variable to store exception words
_exception_words: Set[str] = set()


def load_exceptions(force_reload: bool = False) -> Set[str]:
    """Load exception words from the JSON file.
    
    Args:
        force_reload: If True, reload data even if already cached.
    
    Returns:
        Set of words that should not have گ/ق replaced with ك.
    """
    global _exception_words
    if not _exception_words or force_reload:
        try:
            # Try to load from package data first
            try:
                with resources.open_text('data', 'exception_words_g_q.json') as f:
                    _exception_words = set(json.load(f))
            except (FileNotFoundError, ModuleNotFoundError):
                # Fallback to relative path
                import os
                current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                exception_file = os.path.join(current_dir, 'data', 'exception_words_g_q.json')
                with open(exception_file, 'r', encoding='utf-8') as f:
                    _exception_words = set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is malformed, use empty set
            _exception_words = set()
    
    return _exception_words


def apply_letter_rules(word: str) -> str:
    """Apply letter-level normalization rules to a word.
    
    Rules:
    1. Replace گ and ق with ك (unless word is in exception list)
    2. Replace final ة with ه
    
    Args:
        word: The word to normalize.
        
    Returns:
        The normalized word.
    """
    if not word:
        return word
    
    exceptions = load_exceptions()
    result = word
    
    # Rule 1: Replace گ and ق with ك (unless in exceptions)
    if word not in exceptions:
        result = result.replace('گ', 'ك')
        result = result.replace('ق', 'ك')
    
    # Rule 2: Replace final ة with ه
    if result.endswith('ة'):
        result = result[:-1] + 'ه'
    
    return result


def reload_exceptions() -> None:
    """Force reload of exception words from the JSON file.
    
    This clears the cache and reloads data from files.
    Useful when exception words file has been updated.
    """
    global _exception_words
    _exception_words = set()
    load_exceptions(force_reload=True)