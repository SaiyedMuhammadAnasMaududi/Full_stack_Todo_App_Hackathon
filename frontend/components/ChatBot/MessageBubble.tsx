import React from 'react';
import { format } from 'date-fns';

interface MessageBubbleProps {
  message: string;
  sender: 'user' | 'assistant';
  timestamp: string;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, sender, timestamp }) => {
  const isUser = sender === 'user';
  const formattedTime = format(new Date(timestamp), 'HH:mm');

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-2 ${
          isUser
            ? 'bg-blue-500 text-white rounded-br-none'
            : 'bg-gray-100 text-gray-800 rounded-bl-none'
        }`}
      >
        <div className="whitespace-pre-wrap">{message}</div>
        <div
          className={`text-xs mt-1 ${
            isUser ? 'text-blue-100' : 'text-gray-500'
          }`}
        >
          {formattedTime}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;