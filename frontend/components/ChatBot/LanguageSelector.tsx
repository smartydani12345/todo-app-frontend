import React, { useState, useEffect } from 'react';

interface LanguageSelectorProps {
  onLanguageChange: (language: string) => void;
  initialLanguage?: string;
}

const LANGUAGE_PREFERENCE_KEY = 'chatbot-preferred-language';

const LanguageSelector: React.FC<LanguageSelectorProps> = ({ 
  onLanguageChange, 
  initialLanguage = 'en' 
}) => {
  const [selectedLanguage, setSelectedLanguage] = useState(() => {
    // Check for saved language preference in localStorage
    const savedLanguage = localStorage.getItem(LANGUAGE_PREFERENCE_KEY);
    return savedLanguage || initialLanguage;
  });
  const [isOpen, setIsOpen] = useState(false);
  
  const languages = [
    { code: 'en', name: 'English', flag: '🇺🇸' },
    { code: 'ur', name: 'Urdu', flag: '🇵🇰' },
    { code: 'roman_ur', name: 'Roman Urdu', flag: '🇵🇰' },
    { code: 'roman_en', name: 'Roman English', flag: '🇬🇧' }
  ];

  useEffect(() => {
    // Initialize with the initial language or saved preference
    const savedLanguage = localStorage.getItem(LANGUAGE_PREFERENCE_KEY);
    const initialLang = savedLanguage || initialLanguage;
    setSelectedLanguage(initialLang);
    onLanguageChange(initialLang);
  }, [initialLanguage, onLanguageChange]);

  // Save language preference to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem(LANGUAGE_PREFERENCE_KEY, selectedLanguage);
    onLanguageChange(selectedLanguage);
  }, [selectedLanguage, onLanguageChange]);

  const handleSelect = (languageCode: string) => {
    setSelectedLanguage(languageCode);
    onLanguageChange(languageCode);
    setIsOpen(false);
  };

  const selectedLanguageInfo = languages.find(lang => lang.code === selectedLanguage);

  return (
    <div className="language-selector relative">
      <button
        type="button"
        className="language-select-btn flex items-center justify-between w-full px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        onClick={() => setIsOpen(!isOpen)}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
      >
        <span className="flex items-center">
          <span className="mr-2">{selectedLanguageInfo?.flag}</span>
          <span>{selectedLanguageInfo?.name} ({selectedLanguageInfo?.code})</span>
        </span>
        <svg
          className={`ml-2 h-5 w-5 text-gray-400 transform ${isOpen ? 'rotate-180' : ''}`}
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
          aria-hidden="true"
        >
          <path
            fillRule="evenodd"
            d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
            clipRule="evenodd"
          />
        </svg>
      </button>

      {isOpen && (
        <div className="language-dropdown absolute z-10 mt-1 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm">
          <ul
            tabIndex={-1}
            role="listbox"
            className="language-options-list"
          >
            {languages.map((language) => (
              <li
                key={language.code}
                className={`relative py-2 pl-3 pr-9 cursor-pointer select-none hover:bg-gray-100 ${
                  selectedLanguage === language.code ? 'text-indigo-600 bg-indigo-50' : 'text-gray-900'
                }`}
                id={`language-option-${language.code}`}
                onClick={() => handleSelect(language.code)}
                role="option"
                aria-selected={selectedLanguage === language.code}
              >
                <div className="flex items-center">
                  <span className="mr-2">{language.flag}</span>
                  <span className={`block font-normal truncate ${selectedLanguage === language.code ? 'font-semibold' : ''}`}>
                    {language.name} ({language.code})
                  </span>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default LanguageSelector;