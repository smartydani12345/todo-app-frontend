"""
Urdu to Roman Urdu Transliteration Service

This service converts Urdu script text to Roman Urdu for TTS compatibility.
Example: "میرا کام یاد رکھو" → "mera kaam yaad rakho"
"""

import re
from typing import Dict, List

# Urdu to Roman Urdu mapping
URDU_TO_ROMAN = {
    # Urdu letters
    'ا': 'a',
    'ب': 'b',
    'پ': 'p',
    'ت': 't',
    'ٹ': 't',
    'ث': 's',
    'ج': 'j',
    'چ': 'ch',
    'ح': 'h',
    'خ': 'kh',
    'د': 'd',
    'ڈ': 'd',
    'ذ': 'z',
    'ر': 'r',
    'ڑ': 'r',
    'ز': 'z',
    'ژ': 'zh',
    'س': 's',
    'ش': 'sh',
    'ص': 's',
    'ض': 'z',
    'ط': 't',
    'ظ': 'z',
    'ع': 'a',
    'غ': 'gh',
    'ف': 'f',
    'ق': 'q',
    'ک': 'k',
    'گ': 'g',
    'ل': 'l',
    'م': 'm',
    'ن': 'n',
    'ں': 'n',
    'و': 'o',
    'ہ': 'h',
    'ھ': 'h',
    'ی': 'y',
    'ے': 'ay',
    'ئ': 'a',
    'ؤ': 'o',
    
    # Urdu numerals
    '۰': '0',
    '۱': '1',
    '۲': '2',
    '۳': '3',
    '۴': '4',
    '۵': '5',
    '۶': '6',
    '۷': '7',
    '۸': '8',
    '۹': '9',
}

# Common Urdu words and their Roman equivalents (for better accuracy)
COMMON_WORDS = {
    'میرا': 'mera',
    'میری': 'meri',
    'ہمارا': 'hamara',
    'ہماری': 'hamari',
    'تمہارا': 'tumhara',
    'تمہاری': 'tumhari',
    'آپ کا': 'aap ka',
    'آپ کی': 'aap ki',
    'کا': 'ka',
    'کی': 'ki',
    'کے': 'ke',
    'کو': 'ko',
    'سے': 'se',
    'میں': 'main',
    'پر': 'par',
    'اور': 'aur',
    'یا': 'ya',
    'لیکن': 'lekin',
    'اگر': 'agar',
    'تو': 'to',
    'ہے': 'hai',
    'ہیں': 'hain',
    'تھا': 'tha',
    'تھی': 'thi',
    'تھے': 'the',
    'ہوں': 'hoon',
    'ہو': 'ho',
    'ہوں': 'hain',
    'نہیں': 'nahin',
    'نا': 'na',
    'مت': 'mat',
    'کیا': 'kya',
    'کب': 'kab',
    'کہاں': 'kahan',
    'کیوں': 'kyun',
    'کس': 'kis',
    'کون': 'kaun',
    'کتن': 'kitna',
    'کتنی': 'kitni',
    'کتنے': 'kitne',
    'یہ': 'yeh',
    'وہ': 'woh',
    'یہاں': 'yahan',
    'وہاں': 'wahan',
    'اب': 'ab',
    'پھر': 'phir',
    'بھی': 'bhi',
    'ہی': 'hi',
    'تک': 'tak',
    'والا': 'wala',
    'والی': 'wali',
    'والے': 'wale',
    'کرن': 'karna',
    'کرو': 'karo',
    'کرتا': 'karta',
    'کرتی': 'karti',
    'کرتے': 'karte',
    'کیا': 'kiya',
    'کی': 'ki',
    'کے': 'ke',
    'جا': 'ja',
    'جاؤ': 'jao',
    'جاتا': 'jata',
    'جاتی': 'jati',
    'جاتے': 'jate',
    'آ': 'aa',
    'آؤ': 'aao',
    'آتا': 'aata',
    'آتی': 'aati',
    'آتے': 'aate',
    'دیکھ': 'dekh',
    'دیکھو': 'dekho',
    'دیکھتا': 'dekhta',
    'دیکھتی': 'dekhti',
    'دیکھتے': 'dekhte',
    'سن': 'sun',
    'سنو': 'suno',
    'سنتا': 'sunta',
    'سنتی': 'sunti',
    'سنتے': 'sunte',
    'بول': 'bol',
    'بولو': 'bolo',
    'بولتا': 'bolta',
    'بولتی': 'bolti',
    'بولتے': 'bolte',
    'کھا': 'kha',
    'کھاؤ': 'khao',
    'کھاتا': 'khata',
    'کھاتی': 'khati',
    'کھاتے': 'khate',
    'پڑھ': 'parh',
    'پڑھو': 'parho',
    'پڑھتا': 'parhta',
    'پڑھتی': 'parhti',
    'پڑھتے': 'parhte',
    'لکھ': 'likh',
    'لکھو': 'likho',
    'لکھتا': 'likhta',
    'لکھتی': 'likhti',
    'لکھتے': 'likhte',
    'سو': 'so',
    'سوؤ': 'soo',
    'سوتا': 'sota',
    'سوتی': 'soti',
    'سوتے': 'sote',
    'اٹھ': 'uth',
    'اٹھو': 'utho',
    'اٹھتا': 'uthta',
    'اٹھتی': 'uthti',
    'اٹھتے': 'uthte',
    'بیٹھ': 'baith',
    'بیٹھو': 'baitho',
    'بیٹھتا': 'baithta',
    'بیٹھتی': 'baithti',
    'بیٹھتے': 'baithte',
    'چل': 'chal',
    'چلو': 'chalo',
    'چلتا': 'chalta',
    'چلتی': 'chalti',
    'چلتے': 'chalte',
    'روک': 'rok',
    'روکو': 'roko',
    'روکتا': 'rokta',
    'روکتی': 'rokti',
    'روکتے': 'rokte',
    'چاہ': 'chah',
    'چاہو': 'chaho',
    'چاہتا': 'chahta',
    'چاہتی': 'chahti',
    'چاہتے': 'chahte',
    'جان': 'jaan',
    'جانو': 'jaano',
    'جانتا': 'jaanta',
    'جانتی': 'jaanti',
    'جانتے': 'jaante',
}


def is_urdu_text(text: str) -> bool:
    """
    Check if text contains Urdu script
    
    Args:
        text: Input text
        
    Returns:
        True if text contains Urdu script
    """
    urdu_pattern = re.compile(r'[\u0600-\u06FF]')
    return bool(urdu_pattern.search(text))


def transliterate_urdu_to_roman(text: str) -> str:
    """
    Transliterate Urdu text to Roman Urdu
    
    Args:
        text: Urdu text to transliterate
        
    Returns:
        Roman Urdu text
    """
    if not text:
        return text
    
    # Check if text is actually Urdu
    if not is_urdu_text(text):
        return text
    
    # Try to match common words first
    words = text.split()
    roman_words = []
    
    for word in words:
        # Remove punctuation for matching
        clean_word = re.sub(r'[^\w\s\u0600-\u06FF]', '', word)
        
        # Check if we have this word in our common words dictionary
        if clean_word in COMMON_WORDS:
            roman_words.append(COMMON_WORDS[clean_word])
        else:
            # Transliterate character by character
            roman_word = ''
            for char in clean_word:
                roman_word += URDU_TO_ROMAN.get(char, char)
            
            # Apply some basic rules for better pronunciation
            roman_word = apply_pronunciation_rules(roman_word, clean_word)
            roman_words.append(roman_word)
    
    return ' '.join(roman_words)


def apply_pronunciation_rules(roman_word: str, original_word: str) -> str:
    """
    Apply pronunciation rules to improve Roman Urdu output
    
    Args:
        roman_word: Transliterated word
        original_word: Original Urdu word
        
    Returns:
        Improved Roman Urdu word
    """
    # Basic rules for better pronunciation
    rules = [
        # Double vowels at the end
        (r'aa$', 'aa'),
        (r'ee$', 'ee'),
        (r'oo$', 'oo'),
        
        # Consonant clusters
        (r'kh', 'kh'),
        (r'gh', 'gh'),
        (r'sh', 'sh'),
        (r'ch', 'ch'),
        
        # Nasal sounds
        (r'n$', 'n'),
        (r'm$', 'm'),
    ]
    
    result = roman_word
    for pattern, replacement in rules:
        result = re.sub(pattern, replacement, result)
    
    return result


def process_mixed_text(text: str) -> str:
    """
    Process text that may contain both Urdu and English
    
    Args:
        text: Mixed language text
        
    Returns:
        Text with Urdu portions converted to Roman Urdu
    """
    if not text:
        return text
    
    # Split by whitespace and process each word
    words = text.split()
    processed_words = []
    
    for word in words:
        if is_urdu_text(word):
            processed_words.append(transliterate_urdu_to_roman(word))
        else:
            processed_words.append(word)
    
    return ' '.join(processed_words)


# Global instance
class UrduTransliterationService:
    """Service class for Urdu transliteration"""
    
    def transliterate(self, text: str) -> str:
        """
        Transliterate Urdu text to Roman Urdu
        
        Args:
            text: Input text (may be Urdu, Roman Urdu, or English)
            
        Returns:
            Roman Urdu text
        """
        if not text:
            return text
        
        # Check if text is Urdu
        if is_urdu_text(text):
            return transliterate_urdu_to_roman(text)
        
        # Already Roman Urdu or English
        return text
    
    def is_urdu(self, text: str) -> bool:
        """Check if text is Urdu script"""
        return is_urdu_text(text)
    
    def process(self, text: str) -> str:
        """Process mixed language text"""
        return process_mixed_text(text)


# Singleton instance
urdu_service = UrduTransliterationService()


def get_urdu_service() -> UrduTransliterationService:
    """Get the Urdu transliteration service instance"""
    return urdu_service
