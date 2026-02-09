import React from 'react';

interface TagChipProps {
  tag: string;
  onRemove?: (tag: string) => void;
  isEditable?: boolean;
}

export const TagChip: React.FC<TagChipProps> = ({ tag, onRemove, isEditable = false }) => {
  return (
    <div className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100 mr-1 mb-1">
      {tag}
      {isEditable && onRemove && (
        <button
          type="button"
          className="ml-1 text-blue-500 hover:text-blue-700 focus:outline-none"
          onClick={() => onRemove(tag)}
          aria-label={`Remove tag ${tag}`}
        >
          ×
        </button>
      )}
    </div>
  );
};