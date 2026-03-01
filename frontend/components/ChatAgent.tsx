'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { FiSend, FiMic, FiVolume2, FiVolumeX, FiSettings, FiX } from 'react-icons/fi';
import { motion, AnimatePresence } from 'framer-motion';
import * as chatService from '@/lib/chatService';

interface Message {
  id?: number;
  conversation_id: number;
  sender_type: 'user' | 'ai';
  content: string;
  timestamp?: string;
  language: string;
}

interface Conversation {
  id?: number;
  title: string;
  user_id: string;
  language: string;
  created_at?: string;
  updated_at?: string;
}

interface ChatAgentProps {
  userId: string;
  isOpen: boolean;
  onClose: () => void;
}

const ChatAgent = ({ userId, isOpen, onClose }: ChatAgentProps) => {
  const [currentConversation, setCurrentConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [language, setLanguage] = useState<'en' | 'ur' | 'roman_ur' | 'roman_en'>('en');
  const [selectedGender, setSelectedGender] = useState<'male' | 'female'>('male'); // User manually selects gender
  const [voiceSettings, setVoiceSettings] = useState({
    rate: 1.0,
    pitch: 1.0,
    autoSpeak: true
  });
  const [detectedLanguage, setDetectedLanguage] = useState<string>('en');
  const [availableVoices, setAvailableVoices] = useState<SpeechSynthesisVoice[]>([]);

  // Load voice settings from localStorage on mount
  useEffect(() => {
    const savedSettings = localStorage.getItem('voiceSettings');
    if (savedSettings) {
      try {
        const parsed = JSON.parse(savedSettings);
        setVoiceSettings(prev => ({ ...prev, ...parsed }));
      } catch (e) {
        console.error('Error loading voice settings:', e);
      }
    }
  }, []);

  // Save voice settings to localStorage when changed
  useEffect(() => {
    localStorage.setItem('voiceSettings', JSON.stringify(voiceSettings));
  }, [voiceSettings]);

  // Load available voices on mount
  useEffect(() => {
    const loadVoices = () => {
      const voices = chatService.getAvailableVoices();
      setAvailableVoices(voices);
    };
    
    loadVoices();
    
    // Some browsers load voices asynchronously
    if (typeof window !== 'undefined' && window.speechSynthesis) {
      window.speechSynthesis.onvoiceschanged = loadVoices;
    }
    
    return () => {
      if (typeof window !== 'undefined' && window.speechSynthesis) {
        window.speechSynthesis.onvoiceschanged = null;
      }
    };
  }, []);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const stopRecognitionRef = useRef<(() => void) | null>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Load conversations on mount (create if none exist)
  useEffect(() => {
    if (isOpen && userId) {
      createNewConversation();
    }
  }, [isOpen, userId]);

  // Language detection from input (for display purposes only)
  useEffect(() => {
    if (inputMessage.trim()) {
      const detected = chatService.detectLanguage(inputMessage);
      setDetectedLanguage(detected);
    }
  }, [inputMessage]);

  const createNewConversation = async () => {
    try {
      const newConversation = await chatService.createConversation(
        `Chat ${new Date().toLocaleDateString()}`,
        language
      );

      setCurrentConversation(newConversation);
      setMessages([]);
    } catch (error) {
      console.error('Error creating conversation:', error);
      const mockConversation: Conversation = {
        id: Date.now(),
        title: 'Offline Chat',
        user_id: userId,
        language: language
      };
      setCurrentConversation(mockConversation);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || !currentConversation || isLoading) return;

    const userMessage: Message = {
      conversation_id: currentConversation.id!,
      sender_type: 'user',
      content: inputMessage,
      language: language
    };

    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await chatService.sendMessage(
        inputMessage,
        language,
        currentConversation.id
      );

      const aiMessage: Message = {
        conversation_id: currentConversation.id!,
        sender_type: 'ai',
        content: response.response,
        language: response.language
      };

      setMessages([...updatedMessages, aiMessage]);

      // Dispatch custom event if a task was created (for task list refresh)
      if (response.task_data && response.task_data.operation === 'create') {
        window.dispatchEvent(new CustomEvent('task-created', {
          detail: response.task_data
        }));
      }

      // Auto-speak response if enabled
      if (voiceSettings.autoSpeak) {
        speakResponse(response.response);
      }
    } catch (error: any) {
      console.error('Error sending message:', error);

      const errorMessage: Message = {
        conversation_id: currentConversation.id!,
        sender_type: 'ai',
        content: 'Sorry, I encountered an error processing your message. Please try again.',
        language: language
      };

      setMessages([...updatedMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const startListening = useCallback(() => {
    if (isListening) {
      stopRecognitionRef.current?.();
      setIsListening(false);
      return;
    }

    const langCode = chatService.getLanguageCode(language);

    stopRecognitionRef.current = chatService.startSpeechRecognition(
      (transcript) => {
        setInputMessage(transcript);
        setIsListening(false);
        // Auto-send after voice input
        setTimeout(() => sendMessage(), 500);
      },
      (error) => {
        console.error('Speech recognition error:', error);
        setIsListening(false);
      },
      () => {
        setIsListening(false);
      },
      langCode
    );

    setIsListening(true);
  }, [isListening, language, inputMessage, currentConversation]);

  const speakResponse = (text: string) => {
    const langCode = chatService.getLanguageCode(language);
    const isUrduScript = chatService.isUrduScript(text);

    // Adjust pitch based on selected gender for better distinction
    const pitch = selectedGender === 'female' ? 1.2 : 0.9;
    const rate = voiceSettings.rate;

    chatService.speakText(text, {
      voiceType: selectedGender,
      rate: rate,
      pitch: pitch,
      lang: langCode,
      isUrdu: isUrduScript  // Pass Urdu flag
    });
  };

  const toggleSpeech = () => {
    if (window.speechSynthesis.speaking) {
      window.speechSynthesis.cancel();
    } else if (messages.length > 0) {
      const lastAiMessage = messages.filter(m => m.sender_type === 'ai').pop();
      if (lastAiMessage) {
        speakResponse(lastAiMessage.content);
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const getLanguageName = (lang: string) => {
    const names: Record<string, string> = {
      'en': 'English',
      'ur': 'اردو',
      'roman_ur': 'Roman Urdu',
      'roman_en': 'Roman English'
    };
    return names[lang] || lang;
  };

  const getLanguageIcon = (lang: string) => {
    const icons: Record<string, string> = {
      'en': '🇺🇸',
      'ur': '🇵🇰',
      'roman_ur': '🇵🇰',
      'roman_en': '🇬🇧'
    };
    return icons[lang] || '🌐';
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ x: 400, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: 400, opacity: 0 }}
          transition={{ type: 'spring', damping: 25, stiffness: 200 }}
          className="fixed right-0 top-0 h-full w-96 bg-gray-800 border-l border-gray-700 shadow-2xl z-50 flex flex-col"
        >
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
              <h2 className="text-lg font-bold text-white">ChatAgent</h2>
            </div>
            <button
              onClick={onClose}
              className="p-2 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
              title="Close"
            >
              <FiX size={18} />
            </button>
          </div>

          {/* Language & Voice Selector */}
          <div className="bg-gray-900 p-3 border-b border-gray-700">
            {/* Language Selection */}
            <div className="mb-3">
              <span className="text-xs text-gray-400 block mb-2">Language</span>
              <div className="flex space-x-2">
                {(['en', 'ur', 'roman_ur', 'roman_en'] as const).map((lang) => (
                  <button
                    key={lang}
                    onClick={() => setLanguage(lang)}
                    className={`flex items-center px-3 py-1.5 rounded-lg text-sm transition-colors ${
                      language === lang
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                    }`}
                  >
                    <span className="mr-1">{getLanguageIcon(lang)}</span>
                    {lang === 'en' ? 'EN' : lang === 'ur' ? 'UR' : lang === 'roman_ur' ? 'R-UR' : 'R-EN'}
                  </button>
                ))}
              </div>
            </div>

            {/* Voice Gender Selection */}
            <div className="border-t border-gray-700 pt-3">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs text-gray-400">
                  Voice: {selectedGender === 'male' ? '👨 Male' : '👩 Female'}
                </span>
              </div>

              {/* Gender Selection Buttons */}
              <div className="grid grid-cols-2 gap-2">
                <button
                  onClick={() => setSelectedGender('male')}
                  className={`px-3 py-2 rounded-lg text-sm transition-colors ${
                    selectedGender === 'male'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  👨 Male Voice
                </button>
                <button
                  onClick={() => setSelectedGender('female')}
                  className={`px-3 py-2 rounded-lg text-sm transition-colors ${
                    selectedGender === 'female'
                      ? 'bg-pink-600 text-white'
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  👩 Female Voice
                </button>
              </div>
              
              <p className="text-xs text-gray-500 mt-2">
                {selectedGender === 'male' 
                  ? 'Using Microsoft David (lower pitch)' 
                  : 'Using Microsoft Zira (higher pitch)'}
              </p>
            </div>
          </div>

          {/* Messages Container */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-900/30">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-gray-500">
                <div className="text-4xl mb-4">🤖</div>
                <p className="text-center mb-2">Start a conversation with ChatAgent</p>
                <p className="text-sm text-center text-gray-400">
                  Ask about tasks, features, or get help with the app
                </p>
                <div className="mt-4 flex flex-wrap gap-2 justify-center">
                  <button
                    onClick={() => setInputMessage('Add a task to buy groceries')}
                    className="text-xs bg-gray-700 hover:bg-gray-600 px-3 py-1.5 rounded-full transition-colors"
                  >
                    Add a task
                  </button>
                  <button
                    onClick={() => setInputMessage('Show my tasks')}
                    className="text-xs bg-gray-700 hover:bg-gray-600 px-3 py-1.5 rounded-full transition-colors"
                  >
                    List tasks
                  </button>
                  <button
                    onClick={() => setInputMessage('Help me use this app')}
                    className="text-xs bg-gray-700 hover:bg-gray-600 px-3 py-1.5 rounded-full transition-colors"
                  >
                    Get help
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                {messages.map((msg, index) => (
                  <motion.div
                    key={`${msg.id || 'msg'}-${index}-${msg.timestamp || Date.now()}`}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.2 }}
                    className={`flex ${msg.sender_type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[85%] rounded-2xl p-3 ${
                        msg.sender_type === 'user'
                          ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-tr-sm'
                          : 'bg-gray-700 text-gray-100 rounded-tl-sm'
                      }`}
                    >
                      {msg.sender_type === 'ai' && (
                        <div className="flex items-center space-x-2 mb-1">
                          <span className="text-xs text-gray-400">ChatAgent</span>
                          <button
                            onClick={() => speakResponse(msg.content)}
                            className="text-gray-400 hover:text-white transition-colors"
                            title="Listen"
                          >
                            <FiVolume2 size={12} />
                          </button>
                        </div>
                      )}
                      <p className="whitespace-pre-wrap text-sm">{msg.content}</p>
                      {msg.timestamp && (
                        <p className="text-xs text-gray-400 mt-1">
                          {new Date(msg.timestamp).toLocaleTimeString()}
                        </p>
                      )}
                    </div>
                  </motion.div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-700 rounded-2xl rounded-tl-sm p-3">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-700 p-4 bg-gray-900">
            <div className="flex items-end space-x-2">
              <button
                onClick={toggleSpeech}
                disabled={isLoading || messages.length === 0}
                className="p-2.5 rounded-xl bg-gray-700 text-gray-300 hover:bg-gray-600 disabled:opacity-50 transition-colors"
                title={window?.speechSynthesis?.speaking ? 'Stop speaking' : 'Listen to response'}
              >
                {window?.speechSynthesis?.speaking ? <FiVolumeX size={18} /> : <FiVolume2 size={18} />}
              </button>

              <div className="flex-1 relative">
                <textarea
                  ref={inputRef}
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask about tasks, features, or get help..."
                  className="w-full bg-gray-700 text-white rounded-xl py-3 px-4 pr-10 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 max-h-24 text-sm"
                  rows={1}
                  disabled={isLoading}
                />
              </div>

              <button
                onClick={startListening}
                disabled={isLoading}
                className={`p-2.5 rounded-xl transition-colors ${
                  isListening
                    ? 'bg-red-600 text-white animate-pulse'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                } disabled:opacity-50`}
                title={isListening ? 'Stop listening' : 'Voice input'}
              >
                <FiMic size={18} />
              </button>

              <button
                onClick={sendMessage}
                disabled={!inputMessage.trim() || isLoading}
                className="p-2.5 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 transition-all"
                title="Send message"
              >
                <FiSend size={18} />
              </button>
            </div>

            <div className="text-xs text-gray-500 mt-2 text-center">
              {isListening ? (
                <span className="text-red-400">🔴 Listening... Speak now</span>
              ) : (
                'Press Enter to send, Shift+Enter for new line'
              )}
            </div>
          </div>

          {/* Islamic Values Note */}
          <div className="bg-gray-900/80 px-4 py-2 text-center border-t border-gray-700">
            <p className="text-xs text-gray-500">
              بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ - All praise is due to ALLAH
            </p>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default ChatAgent;
