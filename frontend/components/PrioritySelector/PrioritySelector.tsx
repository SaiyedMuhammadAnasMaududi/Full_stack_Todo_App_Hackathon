import React, { useState } from 'react';

interface PrioritySelectorProps {
  value?: string;
  onChange?: (priority: string) => void;
  disabled?: boolean;
}

const PrioritySelector: React.FC<PrioritySelectorProps> = ({
  value = 'medium',
  onChange,
  disabled = false
}) => {
  const [selectedPriority, setSelectedPriority] = useState<string>(value);

  const handlePriorityChange = (priority: string) => {
    setSelectedPriority(priority);
    if (onChange) {
      onChange(priority);
    }
  };

  const priorityOptions = [
    { value: 'low', label: 'Low', className: 'text-green-600 bg-green-100' },
    { value: 'medium', label: 'Medium', className: 'text-yellow-600 bg-yellow-100' },
    { value: 'high', label: 'High', className: 'text-red-600 bg-red-100' },
  ];

  return (
    <div className="flex flex-wrap gap-2">
      {priorityOptions.map((option) => (
        <button
          key={option.value}
          type="button"
          onClick={() => handlePriorityChange(option.value)}
          disabled={disabled}
          className={`
            px-3 py-1 rounded-md text-sm font-medium transition-colors
            ${selectedPriority === option.value
              ? `${option.className} border-2 border-current ring-2 ring-offset-2 ring-opacity-50`
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }
            ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
          `}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
};

export default PrioritySelector;