import { useState, useCallback } from 'react';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/auth';

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

interface UseChatReturn {
  messages: Message[];
  conversations: Conversation[];
  isLoading: boolean;
  sendMessage: (message: string, conversationId?: number) => Promise<void>;
  loadConversation: (conversationId: number) => Promise<void>;
  loadConversations: () => Promise<void>;
  createNewConversation: () => void;
  error: string | null;
}

const useChat = (): UseChatReturn => {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(async (message: string, conversationId?: number) => {
    if (!user?.id) {
      setError('User not authenticated');
      return;
    }

    if (!message.trim()) {
      setError('Message cannot be empty');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Add user message optimistically
      const userMessage: Message = {
        id: Date.now(),
        sender_type: 'user',
        content: message,
        role: 'user',
        timestamp: new Date().toISOString(),
        sequence_number: messages.length + 1
      };

      setMessages(prev => [...prev, userMessage]);

      // Send to backend
      const requestBody: any = { message };
      if (conversationId) {
        requestBody.conversation_id = conversationId;
      }

      const response = await api.post(`/api/${user.id}/chat`, requestBody);

      // Add assistant response
      const assistantMessage: Message = {
        id: Date.now() + 1,
        sender_type: 'assistant',
        content: response.message,
        role: 'assistant',
        timestamp: response.timestamp,
        sequence_number: messages.length + 2
      };

      setMessages(prev => [...prev, assistantMessage]);

      // If this was a new conversation, update the conversation ID
      if (response.conversation_id && !conversationId) {
        // Reload conversations to include the new one
        await loadConversations();
      }

      // Add confirmation message if available
      if (response.confirmation_message) {
        const confirmationMessage: Message = {
          id: Date.now() + 2,
          sender_type: 'assistant',
          content: response.confirmation_message,
          role: 'assistant',
          timestamp: new Date().toISOString(),
          sequence_number: messages.length + 3
        };
        setMessages(prev => [...prev, confirmationMessage]);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to send message');

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
  }, [user, messages]);

  const loadConversation = useCallback(async (conversationId: number) => {
    if (!user?.id) {
      setError('User not authenticated');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await api.get(`/api/${user.id}/conversations/${conversationId}`);
      const convMessages = response.messages || [];

      setMessages(convMessages.map((msg: any) => ({
        id: msg.id,
        sender_type: msg.sender_type,
        content: msg.content,
        role: msg.role,
        timestamp: msg.timestamp,
        sequence_number: msg.sequence_number
      })));
    } catch (err: any) {
      setError(err.message || 'Failed to load conversation');
    } finally {
      setIsLoading(false);
    }
  }, [user]);

  const loadConversations = useCallback(async () => {
    if (!user?.id) {
      setError('User not authenticated');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await api.get(`/api/${user.id}/conversations`);
      setConversations(response.conversations || []);
    } catch (err: any) {
      setError(err.message || 'Failed to load conversations');
    } finally {
      setIsLoading(false);
    }
  }, [user]);

  const createNewConversation = useCallback(() => {
    setMessages([]);
  }, []);

  return {
    messages,
    conversations,
    isLoading,
    sendMessage,
    loadConversation,
    loadConversations,
    createNewConversation,
    error
  };
};

export default useChat;