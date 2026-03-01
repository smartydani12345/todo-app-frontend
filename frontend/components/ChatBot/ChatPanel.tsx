import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

const ChatPanel: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showProactiveHelp, setShowProactiveHelp] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Toggle chat panel open/closed
  const toggleChatPanel = () => {
    setIsOpen(!isOpen);
  };

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Proactive help detection
  useEffect(() => {
    // Simple heuristic: if the user hasn't sent a message in 60 seconds and has at least one message
    if (messages.length > 0 && inputValue === '') {
      const lastMessage = messages[messages.length - 1];
      if (lastMessage.role === 'user') {
        const timeSinceLastMessage = Date.now() - new Date(lastMessage.timestamp).getTime();
        if (timeSinceLastMessage > 60000) { // 60 seconds
          setShowProactiveHelp(true);
        }
      }
    }
  }, [messages, inputValue]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Dismiss proactive help
  const dismissProactiveHelp = () => {
    setShowProactiveHelp(false);
  };

  // Offer proactive help
  const offerProactiveHelp = () => {
    const helpMessage: Message = {
      id: Date.now(),
      role: 'assistant',
      content: "Hi there! It looks like you might need some help. I can explain how to create tasks, set priorities, use tags, or troubleshoot common issues. What would you like to know?",
      timestamp: new Date().toISOString(),
    };
    
    setMessages(prev => [...prev, helpMessage]);
    setShowProactiveHelp(false);
  };
  
  // Function to ask about the developer
  const askAboutDeveloper = () => {
    const developerMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: "Tell me about the developer of this application",
      timestamp: new Date().toISOString(),
    };
    
    setMessages(prev => [...prev, developerMessage]);
    setInputValue("Tell me about the developer of this application");
  };

  // Handle sending a message
  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    // Add user message to the chat
    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the backend API to get AI response
      const response = await axios.post('/api/chat', {
        message: inputValue,
        language: 'en', // Default to English, could be dynamic
      });

      // Add AI response to the chat
      const aiMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: (response.data as any).response || 'Sorry, I could not process that.',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message to the chat
      const errorMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className={`fixed inset-y-0 right-0 flex ${isOpen ? 'w-full md:w-96' : 'w-0'} transition-all duration-300 z-50`}>
      {/* Chat Panel */}
      <div className={`${isOpen ? 'flex' : 'hidden'} flex-col w-full bg-white border-l shadow-lg h-full`}>
        {/* Chat Header */}
        <div className="bg-blue-600 text-white p-4 flex justify-between items-center">
          <div className="flex items-center">
            <h2 className="text-lg font-semibold">AI Assistant</h2>
            <button 
              onClick={askAboutDeveloper}
              className="ml-4 text-xs bg-blue-700 hover:bg-blue-800 px-2 py-1 rounded"
              title="Learn about the developer"
            >
              About Dev
            </button>
          </div>
          <button 
            onClick={toggleChatPanel}
            className="text-white hover:text-gray-200 focus:outline-none"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-4 bg-gray-50 relative">
          {showProactiveHelp && (
            <div className="proactive-help-notification bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded mb-4 relative">
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="font-bold">Need Help?</h4>
                  <p className="text-sm">It looks like you might need assistance. Can I help explain something?</p>
                </div>
                <div className="flex space-x-2">
                  <button 
                    onClick={offerProactiveHelp}
                    className="bg-blue-500 hover:bg-blue-600 text-white text-xs px-3 py-1 rounded"
                  >
                    Yes, Help
                  </button>
                  <button 
                    onClick={dismissProactiveHelp}
                    className="bg-gray-500 hover:bg-gray-600 text-white text-xs px-3 py-1 rounded"
                  >
                    Dismiss
                  </button>
                </div>
              </div>
            </div>
          )}
          
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full text-gray-500">
              <p>Start a conversation with the AI assistant...</p>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex justify-between items-center mb-2">
                <h3 className="text-sm font-medium text-gray-500">Conversation History</h3>
                <button 
                  onClick={() => setMessages([])}
                  className="text-xs text-red-500 hover:text-red-700"
                >
                  Clear Chat
                </button>
              </div>
              {messages.map((message) => (
                <div 
                  key={message.id} 
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div 
                    className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                      message.role === 'user' 
                        ? 'bg-blue-500 text-white rounded-br-none' 
                        : 'bg-gray-200 text-gray-800 rounded-bl-none'
                    }`}
                  >
                    <p>{message.content}</p>
                    <p className={`text-xs mt-1 ${message.role === 'user' ? 'text-blue-200' : 'text-gray-500'}`}>
                      {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-gray-200 text-gray-800 rounded-bl-none">
                    <p>Thinking...</p>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Chat Input */}
        <div className="border-t p-4 bg-white">
          <div className="flex">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Type your message..."
              className="flex-1 border rounded-l-lg p-2 resize-none h-12 focus:outline-none focus:ring-2 focus:ring-blue-300"
              rows={1}
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading || !inputValue.trim()}
              className={`bg-blue-600 text-white px-4 rounded-r-lg ${isLoading || !inputValue.trim() ? 'opacity-50' : 'hover:bg-blue-700'}`}
            >
              Send
            </button>
          </div>
        </div>
      </div>

      {/* Chat Toggle Button */}
      {!isOpen && (
        <button
          onClick={toggleChatPanel}
          className="absolute top-4 -left-12 bg-blue-600 text-white p-3 rounded-lg shadow-lg hover:bg-blue-700 focus:outline-none"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        </button>
      )}
    </div>
  );
};

export default ChatPanel;