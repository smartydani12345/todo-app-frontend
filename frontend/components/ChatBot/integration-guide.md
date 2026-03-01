# Chat Panel Integration Guide

This document explains how to integrate the ChatPanel component with the existing dashboard.

## Integration Steps

1. Import the ChatPanel component in your dashboard page:

```jsx
import ChatPanel from '../components/ChatBot/ChatPanel';
```

2. Add the ChatPanel component to your dashboard JSX, typically as a sidebar that can be toggled open/closed:

```jsx
// Inside your dashboard component's return statement
return (
  <div className="dashboard-container">
    {/* Your existing dashboard content */}
    <main className="dashboard-content">
      {/* Existing dashboard components */}
    </main>
    
    {/* Chat panel component */}
    <ChatPanel />
  </div>
);
```

## Important Notes

- The ChatPanel component is designed to appear as a collapsible sidebar on the right side of the screen
- It can be toggled open/closed using the chat icon when closed, or the close button when open
- The component handles its own state for messages, input, and loading status
- It communicates with the backend API at `/api/chat` to process user requests

## Styling Considerations

- The component uses Tailwind CSS classes for styling
- Ensure your project has Tailwind CSS configured to properly render the component
- The component is responsive and will take full width on mobile devices