from typing import Dict, List
from services.phase3_language_detection import get_language_detection_service, LanguageDetectionService

class LanguageService:
    """
    Service to handle language-related functionality for the chatbot.
    This includes language detection, response translation, and language-specific processing.
    """
    
    def __init__(self):
        self.detection_service = get_language_detection_service()
        # Initialize a simple in-memory cache
        self.cache = {}
        self.cache_size_limit = 100  # Limit cache size to prevent memory issues
    
    def _get_cache_key(self, text: str) -> str:
        """Generate a cache key for the given text."""
        return f"lang_detect_{hash(text) % 10000}"
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cache entry is still valid (not too old)."""
        import time
        if cache_key in self.cache:
            cached_time, cached_result = self.cache[cache_key]
            # Cache is valid for 10 minutes (600 seconds)
            return (time.time() - cached_time) < 600
        return False
    
    def detect_language(self, text: str) -> Dict[str, any]:
        """
        Detect the language of the input text.
        
        Args:
            text: The input text to analyze
            
        Returns:
            Dictionary containing the detected language code and confidence score
        """
        cache_key = self._get_cache_key(text)
        
        # Check if result is in cache
        if self._is_cache_valid(cache_key):
            _, cached_result = self.cache[cache_key]
            return cached_result
        
        # Get result from detection service
        result = self.detection_service.detect_language(text)
        
        # Add to cache if cache is not full
        if len(self.cache) < self.cache_size_limit:
            import time
            self.cache[cache_key] = (time.time(), result)
        
        return result
    
    def get_response_in_language(self, text: str, target_language: str) -> str:
        """
        Get a response in the specified language.
        In a real implementation, this would involve translation or language-specific templates.
        For now, it returns the text as is, but in a real system, this would use translation APIs.
        
        Args:
            text: The original text
            target_language: The language code to translate to
            
        Returns:
            Text in the target language
        """
        # In a real implementation, this would call a translation service
        # For now, we'll just return the original text
        # This is a placeholder that would be replaced with actual translation logic
        return text
    
    def get_language_specific_templates(self, language_code: str) -> Dict[str, str]:
        """
        Get language-specific response templates.
        
        Args:
            language_code: The language code (en, ur, roman_ur, roman_en)
            
        Returns:
            Dictionary of response templates for the specified language
        """
        cache_key = f"templates_{language_code}"
        
        # Check if templates are in cache
        if cache_key in self.cache:
            cached_time, cached_result = self.cache[cache_key]
            import time
            # Templates don't expire as often since they're static
            if (time.time() - cached_time) < 3600:  # 1 hour
                return cached_result
        
        templates = {
            'en': {
                'greeting': 'Hello! How can I assist you today?',
                'task_created': 'I have created the task: {task}',
                'task_completed': 'I have marked the task as completed: {task}',
                'task_deleted': 'I have deleted the task: {task}',
                'task_edited': 'I have updated the task: {task}',
                'unknown_command': "I didn't understand that. Could you please rephrase?",
                'error': 'An error occurred while processing your request: {error}'
            },
            'ur': {
                'greeting': 'ہیلو! میں آج آپ کی کس طرح مدد کر سکتا ہوں؟',
                'task_created': 'میں نے کام بنایا ہے: {task}',
                'task_completed': 'میں نے کام مکمل کے بطور نشان زد کیا ہے: {task}',
                'task_deleted': 'میں نے کام حذف کر دیا ہے: {task}',
                'task_edited': 'میں نے کام کو اپ ڈیٹ کیا ہے: {task}',
                'unknown_command': 'مجھے یہ سمجھ نہیں آیا. کیا آپ الفاظ دوبارہ ترتیب دے سکتے ہیں؟',
                'error': 'آپ کی درخواست کو پروسیس کرتے وقت ایک خرابی پیش آگئی: {error}'
            },
            'roman_ur': {
                'greeting': 'Hello! Mein aaj apki kis tarhan madad kar sakta hun?',
                'task_created': 'Mein ne kam banaya hai: {task}',
                'task_completed': 'Mein ne kam complete ke tor par nishan zed kiya hai: {task}',
                'task_deleted': 'Mein ne kam delete kr diya hai: {task}',
                'task_edited': 'Mein ne kam update kiya hai: {task}',
                'unknown_command': 'Jhse mujhe samj nahi aya. Kya ap alfaz dobara tarteeb de sakte hain?',
                'error': 'Ap ki drukhat ko prosess krte waqt aik kharaabi pesh agyi: {error}'
            },
            'roman_en': {
                'greeting': 'Hello! How can I assist you today?',
                'task_created': 'I have created the task: {task}',
                'task_completed': 'I have marked the task as completed: {task}',
                'task_deleted': 'I have deleted the task: {task}',
                'task_edited': 'I have updated the task: {task}',
                'unknown_command': "I didn't understand that. Could you please rephrase?",
                'error': 'An error occurred while processing your request: {error}'
            }
        }
        
        result = templates.get(language_code, templates['en'])  # Default to English if language not found
        
        # Add to cache if cache is not full
        if len(self.cache) < self.cache_size_limit:
            import time
            self.cache[cache_key] = (time.time(), result)
        
        return result
    
    def validate_language_code(self, language_code: str) -> bool:
        """
        Validate if the provided language code is supported.
        
        Args:
            language_code: The language code to validate
            
        Returns:
            Boolean indicating if the language code is valid
        """
        supported_codes = ['en', 'ur', 'roman_ur', 'roman_en']
        return language_code in supported_codes

# Global instance of the service
language_service = LanguageService()

def get_language_service() -> LanguageService:
    """
    Get the global instance of LanguageService.
    
    Returns:
        LanguageService instance
    """
    return language_service