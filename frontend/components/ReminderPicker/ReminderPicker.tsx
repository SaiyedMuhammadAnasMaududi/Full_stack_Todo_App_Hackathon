import React, { useState } from 'react';

interface ReminderPickerProps {
  value?: Date | string;
  onChange?: (date: Date | null) => void;
  label?: string;
  placeholder?: string;
  disabled?: boolean;
}

const ReminderPicker: React.FC<ReminderPickerProps> = ({
  value,
  onChange,
  label = 'Set Reminder',
  placeholder = 'Set a reminder time',
  disabled = false
}) => {
  const [selectedDateTime, setSelectedDateTime] = useState<string>(
    value instanceof Date ? value.toISOString().slice(0, 16) : typeof value === 'string' ? value.slice(0, 16) : ''
  );

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const dateTimeStr = e.target.value;
    setSelectedDateTime(dateTimeStr);

    if (dateTimeStr) {
      const date = new Date(dateTimeStr);
      if (onChange) {
        onChange(date);
      }
    } else {
      if (onChange) {
        onChange(null);
      }
    }
  };

  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {label}
        </label>
      )}
      <input
        type="datetime-local"
        value={selectedDateTime}
        onChange={handleChange}
        disabled={disabled}
        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed"
      />
    </div>
  );
};

export default ReminderPicker;