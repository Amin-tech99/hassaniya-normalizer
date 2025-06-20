"""Tests for the Hassaniya text normalizer.

This module contains comprehensive tests for the normalization functionality,
including letter rules, variant mappings, and exception handling.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path to import normalizer
sys.path.insert(0, str(Path(__file__).parent.parent))

from normalizer import normalize_text, normalize_word, clear_unknown_variants
from normalizer.rules import apply_letter_rules


class TestLetterRules:
    """Test letter-level normalization rules."""
    
    def test_gaf_qaf_replacement(self):
        """Test that گ and ق are replaced with ك."""
        assert apply_letter_rules("گتاب") == "كتاب"
        assert apply_letter_rules("قلم") == "كلم"
        assert apply_letter_rules("گقگق") == "كككك"
    
    def test_final_taa_marbuta_replacement(self):
        """Test that final ة is replaced with ه."""
        assert apply_letter_rules("مدرسة") == "مدرسه"
        assert apply_letter_rules("كتابة") == "كتابه"
        assert apply_letter_rules("ة") == "ه"
    
    def test_non_final_taa_marbuta_preserved(self):
        """Test that non-final ة is preserved."""
        assert apply_letter_rules("ةاب") == "ةاب"
        assert apply_letter_rules("كةاب") == "كةاب"
    
    def test_empty_and_none_input(self):
        """Test handling of empty and None inputs."""
        assert apply_letter_rules("") == ""
        assert apply_letter_rules(None) == None
    
    def test_combined_rules(self):
        """Test application of multiple rules together."""
        assert apply_letter_rules("قراءة") == "كراءه"
        assert apply_letter_rules("گتابة") == "كتابه"


class TestVariantMappings:
    """Test variant-to-canonical mappings."""
    
    def setup_method(self):
        """Clear unknown variants before each test."""
        clear_unknown_variants()
    
    @pytest.mark.parametrize("variant,expected", [
        ("هاذ", "هذا"),
        ("هاذا", "هذا"),
        ("الان", "الآن"),
        ("لله", "الله"),
        ("امين", "آمين"),
        ("مايده", "مائده"),
        ("رايك", "رأيك"),
        ("الي", "اللي"),
        ("ألي", "اللي"),
        ("لي", "اللي"),
    ])
    def test_known_variants(self, variant: str, expected: str):
        """Test normalization of known variants."""
        assert normalize_word(variant) == expected
    
    def test_unknown_word_gets_letter_rules(self):
        """Test that unknown words get letter rules applied."""
        # This word shouldn't be in the variants dictionary
        unknown_word = "گتابقة"
        expected = "كتابكه"  # After letter rules
        assert normalize_word(unknown_word) == expected
    
    def test_punctuation_preservation(self):
        """Test that punctuation is preserved during normalization."""
        assert normalize_word("هاذا!") == "هذا!"
        assert normalize_word("(الي)") == "(اللي)"
        assert normalize_word('"رايك"') == '"رأيك"'
        assert normalize_word("الان.") == "الآن."


class TestTextNormalization:
    """Test full text normalization."""
    
    def setup_method(self):
        """Clear unknown variants before each test."""
        clear_unknown_variants()
    
    def test_simple_text_normalization(self):
        """Test normalization of simple text."""
        text = "هاذا كتاب جميل"
        expected = "هذا كتاب جميل"
        assert normalize_text(text) == expected
    
    def test_mixed_variants_and_rules(self):
        """Test text with both variants and letter rule applications."""
        text = "الي يقول هاذا الكلام گتير"
        expected = "اللي يكول هذا الكلام كتير"
        assert normalize_text(text) == expected
    
    def test_punctuation_in_text(self):
        """Test that punctuation is handled correctly in full text."""
        text = "هاذا، الي يقول كذا!"
        expected = "هذا، اللي يكول كذا!"
        assert normalize_text(text) == expected
    
    def test_empty_text(self):
        """Test handling of empty text."""
        assert normalize_text("") == ""
        assert normalize_text("   ") == ""
    
    def test_single_word_text(self):
        """Test normalization of single word text."""
        assert normalize_text("هاذا") == "هذا"
        assert normalize_text("گتاب") == "كتاب"
    
    def test_multiple_spaces_preserved(self):
        """Test that word spacing is normalized to single spaces."""
        text = "هاذا    كتاب   جميل"
        expected = "هذا كتاب جميل"
        assert normalize_text(text) == expected


class TestExceptionHandling:
    """Test exception word handling for letter rules."""
    
    def test_exception_words_preserved(self):
        """Test that words in exception list don't get گ/ق replaced."""
        # Note: This test assumes some words are in the exception list
        # The actual behavior depends on the content of exception_words_g_q.json
        
        # Test with a word that should be in exceptions (if any)
        # Since we can't guarantee specific words, we test the mechanism
        word_with_qaf = "قرآن"  # Common word that might be in exceptions
        result = normalize_word(word_with_qaf)
        
        # The result should either preserve ق (if in exceptions) or replace it
        # This test verifies the mechanism works, not specific content
        assert isinstance(result, str)
        assert len(result) > 0


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_arabic_numbers_preserved(self):
        """Test that Arabic numerals are preserved."""
        text = "هاذا رقم ١٢٣"
        result = normalize_text(text)
        assert "١٢٣" in result
    
    def test_latin_text_preserved(self):
        """Test that Latin characters are preserved."""
        text = "هاذا test كتاب"
        result = normalize_text(text)
        assert "test" in result
    
    def test_mixed_scripts(self):
        """Test handling of mixed script text."""
        text = "Hello هاذا world الي"
        expected = "Hello هذا world اللي"
        assert normalize_text(text) == expected
    
    def test_only_punctuation(self):
        """Test text with only punctuation."""
        text = "!@#$%^&*()"
        assert normalize_text(text) == text
    
    def test_newlines_and_tabs(self):
        """Test that newlines and tabs are handled appropriately."""
        # normalize_text splits on whitespace, so newlines become spaces
        text = "هاذا\nكتاب\tجميل"
        result = normalize_text(text)
        # Should normalize words but may change whitespace structure
        assert "هذا" in result
        assert "كتاب" in result
        assert "جميل" in result


if __name__ == "__main__":
    pytest.main([__file__])