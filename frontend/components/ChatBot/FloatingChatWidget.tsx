'use client';

import React, { useState, useEffect } from 'react';
import ChatWindow from './ChatWindow';
import { useAuth } from '@/lib/useAuth';
import api from '@/lib/api';

interface Message {
  id: number;
  sender_type: 'user' | 'assistant';
  content: string;
  role: string;
  timestamp: string;
  sequence_number: number;
}

interface FloatingChatWidgetProps {
  userId?: string;
}

const FloatingChatWidget: React.FC<FloatingChatWidgetProps> = ({ userId }) => {
  const { user } = useAuth();
  const effectiveUserId = userId || user?.id;
  const [isOpen, setIsOpen] = useState(false);
  const [hasUnread, setHasUnread] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [activeConversationId, setActiveConversationId] = useState<number | null>(null);

  // Simulate unread message indicator when new messages arrive
  useEffect(() => {
    // This would be triggered by new messages in a real implementation
    const handleNewMessage = () => {
      if (!isOpen) {
        setHasUnread(true);
      }
    };

    // Cleanup listener if needed
    return () => {};
  }, [isOpen]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (isOpen) {
      setHasUnread(false); // Clear unread indicator when opening
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading || !effectiveUserId) return;

    // Add user message to UI immediately
    const userMessage: Message = {
      id: Date.now(), // Temporary ID
      sender_type: 'user',
      content: inputValue,
      role: 'user',
      timestamp: new Date().toISOString(),
      sequence_number: messages.length + 1
    };

    setMessages(prev => [...prev, userMessage]);
    const userInput = inputValue;
    setInputValue('');
    setIsLoading(true);

    try {
      // Send message to backend
      const response = await api.sendChatMessage(effectiveUserId, userInput, activeConversationId || undefined);

      // Add assistant response to messages
      const assistantMessage: Message = {
        id: Date.now() + 1, // Temporary ID
        sender_type: 'assistant',
        content: response.message,
        role: 'assistant',
        timestamp: response.timestamp,
        sequence_number: messages.length + 2
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Update conversation ID if new conversation was created
      if (response.conversation_id && !activeConversationId) {
        setActiveConversationId(response.conversation_id);
      }
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to chat
      const errorMessage: Message = {
        id: Date.now() + 1,
        sender_type: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        role: 'assistant',
        timestamp: new Date().toISOString(),
        sequence_number: messages.length + 2
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen ? (
        <div className="relative">
          <div className="w-full max-w-[90vw] md:w-[350px] h-[400px] max-h-[70vh] bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden flex flex-col">
            <div className="bg-blue-600 text-white p-3 flex justify-between items-center">
              <span className="font-semibold text-sm">AI Assistant</span>
              <button
                onClick={toggleChat}
                className="text-white hover:text-gray-200 focus:outline-none"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
            <div className="flex-1 overflow-hidden">
              <ChatWindow
                messages={messages}
                isLoading={isLoading}
                handleSubmit={handleSubmit}
                inputValue={inputValue}
                setInputValue={setInputValue}
              />
            </div>
          </div>
        </div>
      ) : null}

      <button
        onClick={toggleChat}
        className={`flex items-center justify-center w-14 h-14 rounded-full shadow-lg transition-all duration-300 ${
          isOpen
            ? 'bg-red-500 hover:bg-red-600'
            : 'bg-blue-600 hover:bg-blue-700'
        } text-white`}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        {hasUnread && !isOpen && (
          <span className="absolute -top-1 -right-1 flex h-4 w-4">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-4 w-4 bg-red-500"></span>
          </span>
        )}
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      </button>
    </div>
  );
};

export default FloatingChatWidget;