import React, { useState } from 'react';

interface DatePickerProps {
  value?: Date | string;
  onChange?: (date: Date | null) => void;
  label?: string;
  placeholder?: string;
  disabled?: boolean;
  minDate?: Date;
  maxDate?: Date;
}

const DatePicker: React.FC<DatePickerProps> = ({
  value,
  onChange,
  label = 'Select Date',
  placeholder = 'Select a date',
  disabled = false,
  minDate,
  maxDate
}) => {
  const [selectedDate, setSelectedDate] = useState<string>(
    value instanceof Date ? value.toISOString().split('T')[0] : typeof value === 'string' ? value.split('T')[0] : ''
  );

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const dateStr = e.target.value;
    setSelectedDate(dateStr);

    if (dateStr) {
      const date = new Date(dateStr);
      // Set to end of day to ensure the selected date is preserved
      date.setHours(23, 59, 59, 999);
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
        type="date"
        value={selectedDate}
        onChange={handleChange}
        disabled={disabled}
        min={minDate?.toISOString().split('T')[0]}
        max={maxDate?.toISOString().split('T')[0]}
        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed"
      />
    </div>
  );
};

export default DatePicker;