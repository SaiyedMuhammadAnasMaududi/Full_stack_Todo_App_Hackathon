'use client';

import React, { useState, useEffect, useRef } from 'react';
import api from '@/lib/api';
import { useAuth } from '@/lib/useAuth';
import ChatWindow from './ChatWindow';
import { useRouter } from 'next/navigation';

interface Message {
  id: number;
  sender_type: 'user' | 'assistant';
  content: string;
  role: string;
  timestamp: string;
  sequence_number: number;
}

interface Conversation {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

const ChatBot: React.FC = () => {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [activeConversationId, setActiveConversationId] = useState<number | null>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Load conversations when user is available
  useEffect(() => {
    if (user && !authLoading) {
      loadConversations();
    }
  }, [user, authLoading]);

  const loadConversations = async () => {
    try {
      if (!user?.id) return;

      const response = await api.getConversations(user.id);
      setConversations(response.conversations || []);
    } catch (error) {
      console.error('Error loading conversations:', error);
    }
  };

  const loadConversation = async (conversationId: number) => {
    try {
      if (!user?.id) return;

      const response = await api.getConversation(user.id, conversationId);
      const convMessages = response.messages || [];

      setMessages(convMessages.map((msg: any) => ({
        id: msg.id,
        sender_type: msg.sender_type,
        content: msg.content,
        role: msg.role,
        timestamp: msg.timestamp,
        sequence_number: msg.sequence_number
      })));
      setActiveConversationId(conversationId);
    } catch (error) {
      console.error('Error loading conversation:', error);
    }
  };

  const startNewConversation = () => {
    setMessages([]);
    setActiveConversationId(null);
    setInputValue('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading || !user?.id) return;

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
      const response = await api.sendChatMessage(user.id, userInput, activeConversationId || undefined);

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
        // Reload conversations to include the new one
        loadConversations();
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

  if (authLoading) {
    return (
      <div className="flex justify-center items-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="flex flex-col items-center justify-center h-full p-4">
        <h2 className="text-xl font-semibold mb-4">Please log in to use the chatbot</h2>
        <button
          onClick={() => router.push('/login')}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
        >
          Login
        </button>
      </div>
    );
  }

  return (
    <div className="flex h-full w-full max-w-6xl mx-auto bg-white rounded-lg shadow-md overflow-hidden">
      {/* Conversations sidebar */}
      <div className="w-64 bg-gray-50 border-r flex flex-col">
        <div className="p-4 border-b">
          <button
            onClick={startNewConversation}
            className="w-full py-2 px-4 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            + New Chat
          </button>
        </div>

        <div className="flex-1 overflow-y-auto">
          <div className="p-2">
            <h3 className="text-sm font-medium text-gray-500 px-2 py-1">Recent Chats</h3>
            {conversations.length === 0 ? (
              <p className="text-xs text-gray-500 px-2 py-2">No conversations yet</p>
            ) : (
              conversations.map((conv) => (
                <div
                  key={conv.id}
                  onClick={() => loadConversation(conv.id)}
                  className={`p-2 rounded cursor-pointer text-sm ${
                    activeConversationId === conv.id
                      ? 'bg-blue-100 text-blue-700'
                      : 'hover:bg-gray-100'
                  }`}
                >
                  <div className="font-medium truncate">{conv.title || 'Untitled'}</div>
                  <div className="text-xs text-gray-500">
                    {conv.message_count} messages
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Main chat area */}
      <div className="flex-1 flex flex-col">
        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          handleSubmit={handleSubmit}
          inputValue={inputValue}
          setInputValue={setInputValue}
        />
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default ChatBot;