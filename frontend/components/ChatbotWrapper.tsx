'use client';

import { useState, useEffect } from 'react';
import { FiMessageSquare } from 'react-icons/fi';
import ChatAgent from '@/components/ChatAgent';
import { motion, AnimatePresence } from 'framer-motion';

const ChatbotWrapper = ({ userId }: { userId: string }) => {
  const [isChatbotOpen, setIsChatbotOpen] = useState(false);

  // Check if user has closed the chatbot before and remember preference
  useEffect(() => {
    const chatbotClosed = localStorage.getItem('chatbotClosed');
    if (chatbotClosed === 'true') {
      setIsChatbotOpen(false);
    } else {
      setIsChatbotOpen(true);
    }
  }, []);

  const toggleChatbot = () => {
    setIsChatbotOpen(!isChatbotOpen);
    localStorage.setItem('chatbotClosed', (!isChatbotOpen).toString());
  };

  const closeChatbot = () => {
    setIsChatbotOpen(false);
    localStorage.setItem('chatbotClosed', 'true');
  };

  return (
    <>
      <AnimatePresence>
        {isChatbotOpen ? (
          <ChatAgent
            userId={userId}
            isOpen={isChatbotOpen}
            onClose={closeChatbot}
          />
        ) : (
          <motion.button
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            onClick={toggleChatbot}
            className="fixed bottom-4 right-4 z-50 bg-gradient-to-r from-blue-600 to-purple-700 text-white p-4 rounded-full shadow-lg hover:from-blue-700 hover:to-purple-800 transition-all duration-300"
            title="Open AI Assistant"
          >
            <FiMessageSquare size={24} />
            <span className="absolute -top-1 -right-1 flex h-4 w-4">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-4 w-4 bg-green-500"></span>
            </span>
          </motion.button>
        )}
      </AnimatePresence>
    </>
  );
};

export default ChatbotWrapper;
