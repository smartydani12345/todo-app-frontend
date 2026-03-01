import React, { useState } from 'react';

interface GuidanceSystemProps {
  onGuidanceRequest: (request: string) => void;
}

const GuidanceSystem: React.FC<GuidanceSystemProps> = ({ onGuidanceRequest }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  
  const guidanceCategories = [
    { id: 'getting-started', name: 'Getting Started', icon: '🆕' },
    { id: 'tasks', name: 'Managing Tasks', icon: '✅' },
    { id: 'priorities', name: 'Setting Priorities', icon: '❗' },
    { id: 'due-dates', name: 'Due Dates', icon: '📅' },
    { id: 'tags', name: 'Using Tags', icon: '🏷️' },
    { id: 'filters', name: 'Filters & Sorting', icon: '🔍' },
    { id: 'troubleshooting', name: 'Troubleshooting', icon: '🔧' },
    { id: 'about-dev', name: 'About the Developer', icon: '👤' }
  ];

  const handleCategorySelect = (categoryId: string) => {
    setSelectedCategory(categoryId);
    let request = '';
    
    switch (categoryId) {
      case 'getting-started':
        request = 'How do I get started with this application?';
        break;
      case 'tasks':
        request = 'How do I create, edit, and manage tasks?';
        break;
      case 'priorities':
        request = 'How do I set priorities for tasks?';
        break;
      case 'due-dates':
        request = 'How do I set due dates for tasks?';
        break;
      case 'tags':
        request = 'How do I use tags to organize tasks?';
        break;
      case 'filters':
        request = 'How do I filter and sort my tasks?';
        break;
      case 'troubleshooting':
        request = 'I\'m having trouble with the application, can you help?';
        break;
      case 'about-dev':
        request = 'Tell me about the developer of this application';
        break;
      default:
        request = 'Can you help me with something?';
    }
    
    onGuidanceRequest(request);
  };

  return (
    <div className="guidance-system-container bg-blue-50 p-4 rounded-lg border border-blue-200">
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-lg font-semibold text-blue-800 flex items-center">
          <span className="mr-2">💡</span> Need Help?
        </h3>
        <button 
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-blue-600 hover:text-blue-800 focus:outline-none"
        >
          {isExpanded ? 'Collapse' : 'Expand'}
        </button>
      </div>
      
      {isExpanded && (
        <div className="guidance-content">
          <p className="text-sm text-gray-600 mb-3">
            Select a topic below or ask a specific question:
          </p>
          
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2 mb-4">
            {guidanceCategories.map((category) => (
              <button
                key={category.id}
                onClick={() => handleCategorySelect(category.id)}
                className={`guidance-category-btn flex flex-col items-center justify-center p-2 rounded-md text-xs sm:text-sm ${
                  selectedCategory === category.id 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-white text-gray-700 hover:bg-blue-100 border border-gray-200'
                }`}
                title={category.name}
              >
                <span className="text-lg mb-1">{category.icon}</span>
                <span>{category.name}</span>
              </button>
            ))}
          </div>
          
          <div className="quick-actions mt-3">
            <h4 className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">Quick Actions</h4>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => onGuidanceRequest('How do I create a new task?')}
                className="quick-action-btn px-3 py-1 bg-white text-blue-600 text-xs rounded-full border border-blue-200 hover:bg-blue-50"
              >
                Create Task
              </button>
              <button
                onClick={() => onGuidanceRequest('How do I mark a task as complete?')}
                className="quick-action-btn px-3 py-1 bg-white text-blue-600 text-xs rounded-full border border-blue-200 hover:bg-blue-50"
              >
                Complete Task
              </button>
              <button
                onClick={() => onGuidanceRequest('How do I edit a task?')}
                className="quick-action-btn px-3 py-1 bg-white text-blue-600 text-xs rounded-full border border-blue-200 hover:bg-blue-50"
              >
                Edit Task
              </button>
              <button
                onClick={() => onGuidanceRequest('Show me all features')}
                className="quick-action-btn px-3 py-1 bg-white text-blue-600 text-xs rounded-full border border-blue-200 hover:bg-blue-50"
              >
                All Features
              </button>
            </div>
          </div>
        </div>
      )}
      
      {!isExpanded && (
        <p className="text-xs text-gray-500 italic">
          Click Expand for help topics and quick actions
        </p>
      )}
    </div>
  );
};

export default GuidanceSystem;