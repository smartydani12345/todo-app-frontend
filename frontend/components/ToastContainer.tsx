'use client';

import React, { useEffect } from 'react';
import toast, { Toaster } from 'react-hot-toast';

export function ToastContainer() {
  return (
    <Toaster
      position="top-right"
      toastOptions={{
        duration: 4000,
        style: {
          background: '#1f2937',
          color: '#ffffff',
          borderRadius: '0.5rem',
          padding: '0.75rem',
          fontSize: '0.875rem',
        },
        success: {
          style: {
            background: '#10b981',
          },
        },
        error: {
          style: {
            background: '#ef4444',
          },
        },
      }}
    />
  );
}

// Export toast functions for use in other components
export { toast };