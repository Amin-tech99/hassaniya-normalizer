"""Hassaniya text normalizer package.

This package provides functionality to normalize Hassaniya Arabic text using
letter-level rules and variant mappings.
"""

from .normalizer import normalize_text, normalize_word, unknown_variants, clear_unknown_variants

__version__ = "0.1.0"
__all__ = ["normalize_text", "normalize_word", "unknown_variants", "clear_unknown_variants"]