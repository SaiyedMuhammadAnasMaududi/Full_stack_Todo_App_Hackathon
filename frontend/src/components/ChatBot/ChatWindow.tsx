import React from 'react';
import MessageBubble from './MessageBubble';

interface Message {
  id: number;
  sender_type: 'user' | 'assistant';
  content: string;
  role: string;
  timestamp: string;
  sequence_number: number;
}

interface ChatWindowProps {
  messages: Message[];
  isLoading: boolean;
  handleSubmit: (e: React.FormEvent) => void;
  inputValue: string;
  setInputValue: (value: string) => void;
}

const ChatWindow: React.FC<ChatWindowProps> = ({
  messages,
  isLoading,
  handleSubmit,
  inputValue,
  setInputValue,
}) => {
  return (
    <div className="flex flex-col h-full">
      {/* Chat header */}
      <div className="border-b p-4 bg-gray-50">
        <h2 className="text-lg font-semibold">AI Task Assistant</h2>
        <p className="text-sm text-gray-500">Manage your tasks with natural language</p>
      </div>

      {/* Messages container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-25">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center text-gray-500">
            <h3 className="text-lg font-medium mb-2">Welcome to the AI Task Assistant!</h3>
            <p className="max-w-md">
              I can help you manage your tasks using natural language. Try saying things like:
            </p>
            <ul className="mt-2 text-left list-disc pl-5 space-y-1 max-w-md">
              <li>"Add a task: Buy groceries"</li>
              <li>"Show me my tasks"</li>
              <li>"Mark task 1 as complete"</li>
              <li>"Update my meeting time"</li>
            </ul>
          </div>
        ) : (
          messages.map((message) => (
            <MessageBubble
              key={message.id}
              message={message.content}
              sender={message.sender_type}
              timestamp={message.timestamp}
            />
          ))
        )}

        {isLoading && (
          <div className="flex items-center space-x-2 p-2">
            <div className="bg-blue-100 rounded-full p-2">
              <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
            <span className="text-gray-500">AI is thinking...</span>
          </div>
        )}
      </div>

      {/* Input area */}
      <div className="border-t p-4 bg-white">
        <form onSubmit={handleSubmit} className="flex space-x-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message here..."
            className="flex-1 border border-gray-300 rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className={`px-4 py-2 rounded-r-lg font-medium ${
              isLoading || !inputValue.trim()
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600'
            }`}
          >
            Send
          </button>
        </form>
        <p className="text-xs text-gray-500 mt-2 text-center">
          AI Assistant can help you manage tasks with natural language
        </p>
      </div>
    </div>
  );
};

export default ChatWindow;