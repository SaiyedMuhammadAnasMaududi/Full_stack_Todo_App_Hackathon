import React, { useState } from 'react';

interface RecurrenceControlsProps {
  isRecurring: boolean;
  recurrenceRule?: string;
  onRecurringChange: (isRecurring: boolean) => void;
  onRuleChange: (rule: string) => void;
  disabled?: boolean;
}

const RecurrenceControls: React.FC<RecurrenceControlsProps> = ({
  isRecurring,
  recurrenceRule = '',
  onRecurringChange,
  onRuleChange,
  disabled = false
}) => {
  const [selectedFrequency, setSelectedFrequency] = useState<string>(() => {
    if (!recurrenceRule) return 'no-repeat';
    if (recurrenceRule.includes('DAILY')) return 'daily';
    if (recurrenceRule.includes('WEEKLY')) return 'weekly';
    if (recurrenceRule.includes('MONTHLY')) return 'monthly';
    if (recurrenceRule.includes('YEARLY')) return 'yearly';
    return 'custom';
  });

  const frequencies = [
    { value: 'no-repeat', label: 'Does not repeat' },
    { value: 'daily', label: 'Daily' },
    { value: 'weekly', label: 'Weekly' },
    { value: 'monthly', label: 'Monthly' },
    { value: 'yearly', label: 'Yearly' },
    { value: 'custom', label: 'Custom...' },
  ];

  const handleToggleChange = () => {
    const newValue = !isRecurring;
    onRecurringChange(newValue);
    if (!newValue) {
      onRuleChange('');
    }
  };

  const handleFrequencyChange = (frequency: string) => {
    setSelectedFrequency(frequency);

    if (frequency === 'no-repeat') {
      onRecurringChange(false);
      onRuleChange('');
      return;
    }

    let rule = '';
    switch (frequency) {
      case 'daily':
        rule = 'RRULE:FREQ=DAILY';
        break;
      case 'weekly':
        rule = 'RRULE:FREQ=WEEKLY';
        break;
      case 'monthly':
        rule = 'RRULE:FREQ=MONTHLY';
        break;
      case 'yearly':
        rule = 'RRULE:FREQ=YEARLY';
        break;
      default:
        rule = recurrenceRule;
    }

    onRecurringChange(true);
    onRuleChange(rule);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center">
        <label className="flex items-center cursor-pointer">
          <div className="relative">
            <input
              type="checkbox"
              checked={isRecurring}
              onChange={handleToggleChange}
              disabled={disabled}
              className="sr-only"
            />
            <div
              className={`block w-10 h-6 rounded-full transition-colors ${
                isRecurring ? 'bg-blue-600' : 'bg-gray-300'
              }`}
            ></div>
            <div
              className={`absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition-transform ${
                isRecurring ? 'transform translate-x-4' : ''
              }`}
            ></div>
          </div>
          <span className="ml-3 text-sm font-medium text-gray-700">Recurring Task</span>
        </label>
      </div>

      {isRecurring && (
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Repeat frequency
            </label>
            <select
              value={selectedFrequency}
              onChange={(e) => handleFrequencyChange(e.target.value)}
              disabled={disabled}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed"
            >
              {frequencies.map((freq) => (
                <option key={freq.value} value={freq.value}>
                  {freq.label}
                </option>
              ))}
            </select>
          </div>

          {(selectedFrequency === 'custom') && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Custom recurrence rule (RRULE)
              </label>
              <input
                type="text"
                value={recurrenceRule}
                onChange={(e) => onRuleChange(e.target.value)}
                disabled={disabled}
                placeholder="Enter RRULE string (e.g., RRULE:FREQ=WEEKLY;BYDAY=MO)"
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed"
              />
              <p className="mt-1 text-xs text-gray-500">
                Format: RRULE:FREQ=[DAILY|WEEKLY|MONTHLY|YEARLY];[optional parameters]
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RecurrenceControls;