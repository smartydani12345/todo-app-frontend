from typing import Dict, List
import re

class LanguageDetectionService:
    """
    Service to detect the language of user input.
    Supports English, Urdu, Roman Urdu, and Roman English.
    """
    
    def __init__(self):
        # Define patterns for different languages
        self.language_patterns = {
            'en': {
                'name': 'English',
                'pattern': r'[a-zA-Z\s\d\W]+',  # Basic Latin characters
                'confidence_threshold': 0.8
            },
            'ur': {
                'name': 'Urdu',
                'pattern': r'[\u0600-\u06FF\s\d\W]+',  # Arabic/Persian script used for Urdu
                'confidence_threshold': 0.8
            },
            'roman_ur': {
                'name': 'Roman Urdu',
                'pattern': r'[a-zA-Z\s\d\W]+\s*[a-zA-Z\s\d\W]*',  # Mix of Latin characters with common Urdu words in Roman script
                'confidence_threshold': 0.6
            },
            'roman_en': {
                'name': 'Roman English',
                'pattern': r'[a-zA-Z\s\d\W]+',  # Same as English but contextually different
                'confidence_threshold': 0.7
            }
        }
        
        # Common Roman Urdu words for identification
        self.roman_urdu_words = {
            'hai', 'haiں', 'ho', 'kya', 'kiya', 'kaha', 'kehna', 'main', 'mein', 'tum', 
            'aap', 'hum', 'vo', 'wahan', 'yahan', 'kahan', 'kuch', 'koi', 'koi', 'na',
            'ji', 'han', 'haan', 'nahi', 'bilkul', 'jaroor', 'shukriya', 'khuda', 'allah'
        }
    
    def detect_language(self, text: str) -> Dict[str, any]:
        """
        Detect the language of the input text.
        
        Args:
            text: The input text to analyze
            
        Returns:
            Dictionary containing the detected language code and confidence score
        """
        if not text or not isinstance(text, str):
            return {'language': 'en', 'confidence': 1.0, 'message': 'Empty or invalid input defaulted to English'}
        
        text_lower = text.lower()
        
        # Check for Urdu (Arabic/Persian script)
        urdu_chars = len(re.findall(r'[\u0600-\u06FF]', text))
        total_chars = len(re.findall(r'[\w\u0600-\u06FF]', text))
        
        if total_chars > 0:
            urdu_ratio = urdu_chars / total_chars
            if urdu_ratio > 0.5:  # If more than half the characters are Urdu
                return {
                    'language': 'ur',
                    'confidence': urdu_ratio,
                    'message': f'Detected Urdu script with {urdu_ratio:.2%} confidence'
                }
        
        # Check for Roman Urdu patterns
        words = text_lower.split()
        roman_urdu_matches = sum(1 for word in words if word in self.roman_urdu_words)
        
        if len(words) > 0:
            roman_urdu_ratio = roman_urdu_matches / len(words)
            if roman_urdu_ratio > 0.3:  # If more than 30% of words are common Roman Urdu words
                return {
                    'language': 'roman_ur',
                    'confidence': roman_urdu_ratio,
                    'message': f'Detected Roman Urdu with {roman_urdu_ratio:.2%} confidence based on vocabulary'
                }
        
        # Default to English for Latin script
        latin_chars = len(re.findall(r'[a-zA-Z]', text))
        total_text_chars = len(re.findall(r'[a-zA-Z\u0600-\u06FF]', text))
        
        if total_text_chars > 0:
            english_ratio = latin_chars / total_text_chars
            if english_ratio > 0.7:
                # Check if it might be Roman English (more formal/structured)
                return {
                    'language': 'en',
                    'confidence': english_ratio,
                    'message': f'Detected English with {english_ratio:.2%} confidence'
                }
        
        # If we can't confidently determine, default to English
        return {
            'language': 'en',
            'confidence': 0.5,
            'message': 'Unable to confidently determine language, defaulted to English'
        }
    
    def get_supported_languages(self) -> List[Dict[str, str]]:
        """
        Get a list of supported languages.
        
        Returns:
            List of dictionaries containing language information
        """
        return [
            {'code': 'en', 'name': 'English'},
            {'code': 'ur', 'name': 'Urdu'},
            {'code': 'roman_ur', 'name': 'Roman Urdu'},
            {'code': 'roman_en', 'name': 'Roman English'}
        ]

# Global instance of the service
language_detection_service = LanguageDetectionService()

def get_language_detection_service() -> LanguageDetectionService:
    """
    Get the global instance of LanguageDetectionService.
    
    Returns:
        LanguageDetectionService instance
    """
    return language_detection_service