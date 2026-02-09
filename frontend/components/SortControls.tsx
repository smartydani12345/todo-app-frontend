import React from 'react';

type SortField = 'created_at' | 'due_date' | 'priority' | 'title';
type SortOrder = 'asc' | 'desc';

interface SortControlsProps {
  currentSortField: SortField;
  currentSortOrder: SortOrder;
  onSortChange: (field: SortField, order: SortOrder) => void;
}

export const SortControls: React.FC<SortControlsProps> = ({
  currentSortField,
  currentSortOrder,
  onSortChange
}) => {
  const sortOptions: { value: SortField; label: string }[] = [
    { value: 'created_at', label: 'Created At' },
    { value: 'due_date', label: 'Due Date' },
    { value: 'priority', label: 'Priority' },
    { value: 'title', label: 'Title' }
  ];

  const handleFieldChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onSortChange(e.target.value as SortField, currentSortOrder);
  };

  const handleOrderChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onSortChange(currentSortField, e.target.value as SortOrder);
  };

  return (
    <div className="flex space-x-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Sort By
        </label>
        <select
          value={currentSortField}
          onChange={handleFieldChange}
          className="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
        >
          {sortOptions.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Order
        </label>
        <select
          value={currentSortOrder}
          onChange={handleOrderChange}
          className="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
        >
          <option value="asc">Ascending</option>
          <option value="desc">Descending</option>
        </select>
      </div>
    </div>
  );
};