'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { FiSend, FiMic, FiX, FiMaximize, FiMinimize, FiVolume2 } from 'react-icons/fi';
import apiClient from '@/lib/api-client';

// Define TypeScript interfaces
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

interface ChatbotProps {
  userId: string;
  isOpen: boolean;
  onClose: () => void;
  onToggle: () => void;
}

// Voice options for selection
interface VoiceOption {
  id: string;
  name: string;
  gender: 'male' | 'female';
  description: string;
}

const VOICE_OPTIONS: VoiceOption[] = [
  // Male Voices (20-26 years old)
  { id: 'zain', name: 'Zain', gender: 'male', description: 'Deep, confident tone' },
  { id: 'jordan', name: 'Jordan', gender: 'male', description: 'Energetic, smooth tone' },
  { id: 'ali', name: 'Ali', gender: 'male', description: 'Friendly, calm tone' },
  { id: 'rayyan', name: 'Rayyan', gender: 'male', description: 'Playful, clear tone' },
  { id: 'omar', name: 'Omar', gender: 'male', description: 'Warm, mature tone' },
  // Female Voices (20-26 years old)
  { id: 'lucy', name: 'Lucy', gender: 'female', description: 'Sweet, bright tone' },
  { id: 'kiran', name: 'Kiran', gender: 'female', description: 'Gentle, clear tone' },
  { id: 'sara', name: 'Sara', gender: 'female', description: 'Lively, fun tone' },
  { id: 'noor', name: 'Noor', gender: 'female', description: 'Soothing, soft tone' },
  { id: 'amina', name: 'Amina', gender: 'female', description: 'Playful, warm tone' },
];

const Chatbot = ({ userId, isOpen, onClose, onToggle }: ChatbotProps) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversation, setCurrentConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [language, setLanguage] = useState<'en' | 'ur' | 'roman_ur' | 'roman_en'>('en');
  const [selectedVoice, setSelectedVoice] = useState<string>('zain'); // Default voice
  const [showVoiceSelector, setShowVoiceSelector] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<any>(null);

  // Initialize speech recognition
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      
      if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = getLanguageCode(language);
        
        recognition.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          setInputMessage(transcript);
          setIsListening(false);
        };
        
        recognition.onerror = (event: any) => {
          console.error('Speech recognition error', event.error);
          setIsListening(false);
        };
        
        recognition.onend = () => {
          setIsListening(false);
        };
        
        recognitionRef.current = recognition;
      }
    }
  }, [language]);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Load conversations for the user
  useEffect(() => {
    if (isOpen && userId) {
      loadConversations();
    }
  }, [isOpen, userId]);

  const loadConversations = async () => {
    try {
      const response = await apiClient.get('/chat/conversations');
      const conversationsData = response.data as Conversation[];
      setConversations(conversationsData);

      // Load the most recent conversation if available
      if (conversationsData.length > 0) {
        const latestConversation = conversationsData[conversationsData.length - 1];
        setCurrentConversation(latestConversation);
        loadMessages(latestConversation.id);
      }
    } catch (error) {
      console.error('Error loading conversations:', error);
      // Create a new conversation if loading fails
      createNewConversation();
    }
  };

  const loadMessages = async (conversationId: number) => {
    try {
      const response = await apiClient.get(`/chat/conversations/${conversationId}/messages`);
      setMessages(response.data as Message[]);
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const createNewConversation = async () => {
    try {
      const newConversationData = {
        title: `Chat ${new Date().toLocaleDateString()}`,
        user_id: userId,
        language: language
      };

      const response = await apiClient.post('/chat/conversations', newConversationData);
      const newConversation = response.data as Conversation;

      // Add to conversations list
      setConversations([...conversations, newConversation]);

      // Set as current conversation
      setCurrentConversation(newConversation);
      setMessages([]);
    } catch (error) {
      console.error('Error creating conversation:', error);
      // Set a mock conversation for offline mode
      const mockConversation: Conversation = {
        id: Date.now(),
        title: 'Offline Chat',
        user_id: userId,
        language: language
      };
      setCurrentConversation(mockConversation);
    }
  };

  const switchConversation = async (conversation: Conversation) => {
    setCurrentConversation(conversation);
    setLanguage(conversation.language as 'en' | 'ur' | 'roman_ur' | 'roman_en');
    loadMessages(conversation.id!);
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || !currentConversation || isLoading) return;

    const userMessage: Message = {
      conversation_id: currentConversation.id!,
      sender_type: 'user',
      content: inputMessage,
      language: language
    };

    // Add user message to UI immediately
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Send message to backend
      const response = await apiClient.post(`/chat/conversations/${currentConversation.id}/messages`, userMessage);

      // Add AI response to messages
      setMessages([...updatedMessages, response.data as Message]);
    } catch (error: any) {
      console.error('Error sending message:', error);

      // Silent error handling - don't show technical errors to user
      // Just show a friendly message and continue
      
      // If error is 403 or 500, try creating a new conversation silently
      if (error.response?.status === 403 || error.response?.status === 500) {
        console.log('Creating new conversation due to error...');
        await createNewConversation();
      }

      // Show a friendly, human-like error message
      const friendlyErrorMessages = [
        "Oops! I had a little glitch there. Try asking me again?",
        "Hmm, that didn't quite work. Let's try that one more time!",
        "I'm having a tiny brain freeze! Can you repeat that?",
        "Sorry about that! Sometimes I need a second try. What did you want to ask?"
      ];
      
      const randomErrorMessage = friendlyErrorMessages[Math.floor(Math.random() * friendlyErrorMessages.length)];
      
      const errorMessage: Message = {
        conversation_id: currentConversation.id!,
        sender_type: 'ai',
        content: randomErrorMessage,
        language: language
      };

      setMessages([...updatedMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const startListening = () => {
    if (!recognitionRef.current) {
      alert('Speech recognition is not supported in your browser.');
      return;
    }

    try {
      // Stop if already listening
      if (isListening) {
        recognitionRef.current.stop();
        setIsListening(false);
        return;
      }

      // Set language and start listening
      recognitionRef.current.lang = getLanguageCode(language);
      recognitionRef.current.start();
      setIsListening(true);
    } catch (error: any) {
      console.error('Speech recognition error:', error);
      // Handle "already started" error
      if (error.name === 'InvalidStateError') {
        // Recognition already started, stop it
        try {
          recognitionRef.current.stop();
        } catch (e) {
          console.error('Error stopping recognition:', e);
        }
        setIsListening(false);
      } else {
        alert('Speech recognition error: ' + (error.message || 'Unknown error'));
      }
    }
  };

  const getLanguageCode = (lang: string) => {
    switch (lang) {
      case 'ur': return 'ur-PK'; // Urdu Pakistan
      case 'en': return 'en-US'; // English US
      case 'roman_ur': return 'ur-PK'; // Roman Urdu still uses Urdu locale
      case 'roman_en': return 'en-US'; // Roman English uses English locale
      default: return 'en-US';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const speakResponse = (text: string) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = getLanguageCode(language);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      speechSynthesis.speak(utterance);
    }
  };

  // Render the chatbot UI
  return (
    <div className={`fixed bottom-4 right-4 z-50 transition-all duration-300 ease-in-out ${isOpen ? 'translate-y-0' : 'translate-y-full'}`}>
      {/* Chatbot Window */}
      <div className="w-80 h-[500px] flex flex-col bg-gray-800 border border-gray-700 rounded-lg shadow-lg overflow-hidden">
        {/* Chat Header */}
        <div className="bg-gray-900 p-3 flex items-center justify-between border-b border-gray-700">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
            <h3 className="font-semibold text-white">AI Assistant</h3>
          </div>
          
          <div className="flex space-x-2">
            <button 
              onClick={onToggle}
              className="text-gray-400 hover:text-white"
            >
              {isOpen ? <FiMinimize /> : <FiMaximize />}
            </button>
            <button 
              onClick={onClose}
              className="text-gray-400 hover:text-white"
            >
              <FiX />
            </button>
          </div>
        </div>
        
        {/* Conversation Selector */}
        <div className="bg-gray-800 p-2 border-b border-gray-700 overflow-x-auto">
          <div className="flex space-x-2">
            <button
              onClick={createNewConversation}
              className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded text-sm whitespace-nowrap"
            >
              + New Chat
            </button>
            
            {conversations.map(conv => (
              <button
                key={conv.id}
                onClick={() => switchConversation(conv)}
                className={`px-3 py-1 rounded text-sm whitespace-nowrap truncate max-w-[120px] ${
                  currentConversation?.id === conv.id 
                    ? 'bg-indigo-600 text-white' 
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                {conv.title || `Chat ${conv.id}`}
              </button>
            ))}
          </div>
        </div>
        
        {/* Language Selector */}
        <div className="bg-gray-800 p-2 border-b border-gray-700">
          <div className="flex space-x-2">
            {(['en', 'ur', 'roman_ur', 'roman_en'] as const).map(lang => (
              <button
                key={lang}
                onClick={() => setLanguage(lang)}
                className={`px-2 py-1 rounded text-xs ${
                  language === lang
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                {lang === 'en' ? 'EN' :
                 lang === 'ur' ? 'UR' :
                 lang === 'roman_ur' ? 'RUR' : 'REN'}
              </button>
            ))}
          </div>
        </div>

        {/* Voice Selector */}
        <div className="bg-gray-800 p-2 border-b border-gray-700">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-gray-400">Voice: {VOICE_OPTIONS.find(v => v.id === selectedVoice)?.name}</span>
            <button
              onClick={() => setShowVoiceSelector(!showVoiceSelector)}
              className="text-xs text-blue-400 hover:text-blue-300"
            >
              {showVoiceSelector ? '▼' : '▶'}
            </button>
          </div>
          
          {showVoiceSelector && (
            <div className="grid grid-cols-2 gap-2 max-h-48 overflow-y-auto">
              {/* Male Voices */}
              <div className="col-span-2">
                <p className="text-xs text-gray-500 mb-1">Male Voices</p>
              </div>
              {VOICE_OPTIONS.filter(v => v.gender === 'male').map(voice => (
                <button
                  key={voice.id}
                  onClick={() => {
                    setSelectedVoice(voice.id);
                    setShowVoiceSelector(false);
                  }}
                  className={`px-2 py-1 rounded text-xs text-left ${
                    selectedVoice === voice.id
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                  title={voice.description}
                >
                  {voice.name}
                </button>
              ))}
              
              {/* Female Voices */}
              <div className="col-span-2 mt-2">
                <p className="text-xs text-gray-500 mb-1">Female Voices</p>
              </div>
              {VOICE_OPTIONS.filter(v => v.gender === 'female').map(voice => (
                <button
                  key={voice.id}
                  onClick={() => {
                    setSelectedVoice(voice.id);
                    setShowVoiceSelector(false);
                  }}
                  className={`px-2 py-1 rounded text-xs text-left ${
                    selectedVoice === voice.id
                      ? 'bg-pink-600 text-white'
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                  title={voice.description}
                >
                  {voice.name}
                </button>
              ))}
            </div>
          )}
        </div>
        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-3 bg-gray-900/50">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-gray-500">
              <p className="text-center mb-4">Start a conversation with the AI assistant</p>
              <p className="text-sm text-center">Ask about tasks, features, or get help with the app</p>
            </div>
          ) : (
            <div className="space-y-3">
              {messages.map((msg, index) => (
                <div 
                  key={msg.id || index} 
                  className={`flex ${msg.sender_type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div 
                    className={`max-w-[80%] rounded-lg p-3 ${
                      msg.sender_type === 'user' 
                        ? 'bg-blue-600 text-white rounded-tr-none' 
                        : 'bg-gray-700 text-gray-100 rounded-tl-none'
                    }`}
                  >
                    <div className="flex items-start">
                      {msg.sender_type === 'ai' && (
                        <button 
                          onClick={() => speakResponse(msg.content)}
                          className="mr-2 text-gray-300 hover:text-white"
                          title="Listen to response"
                        >
                          <FiVolume2 size={14} />
                        </button>
                      )}
                      <p className="whitespace-pre-wrap">{msg.content}</p>
                    </div>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-gray-700 text-gray-100 rounded-lg p-3 rounded-tl-none max-w-[80%]">
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
        <div className="border-t border-gray-700 p-2 bg-gray-800">
          <div className="flex items-end space-x-2">
            <div className="flex-1 relative">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about tasks, features, or get help..."
                className="w-full bg-gray-700 text-white rounded-lg py-2 px-3 pr-10 resize-none focus:outline-none focus:ring-1 focus:ring-blue-500 max-h-24"
                rows={1}
                disabled={isLoading}
              />
            </div>
            
            <button
              onClick={startListening}
              disabled={isLoading}
              className={`p-2 rounded-full ${
                isListening 
                  ? 'bg-red-600 text-white' 
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
              title={isListening ? "Stop listening" : "Voice input"}
            >
              <FiMic />
            </button>
            
            <button
              onClick={sendMessage}
              disabled={!inputMessage.trim() || isLoading}
              className="p-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 disabled:opacity-50"
              title="Send message"
            >
              <FiSend />
            </button>
          </div>
          
          <div className="text-xs text-gray-500 mt-1 text-center">
            {isListening ? "Listening..." : "Press Enter to send, Shift+Enter for new line"}
          </div>
        </div>
      </div>
      
      {/* Islamic Values Note */}
      <div className="text-xs text-gray-500 mt-1 text-center bg-black/30 px-2 py-1 rounded-b">
        بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ - All praise is due to ALLAH, Lord of all worlds
      </div>
    </div>
  );
};

export default Chatbot;