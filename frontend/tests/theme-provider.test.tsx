import React from 'react';
import { render, act, waitFor } from '@testing-library/react';
import { ThemeProvider, useTheme } from '../components/ThemeProvider';

// Mock localStorage
const localStorageMock = (() => {
  let store: { [key: string]: string } = {};
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(), // Deprecated
    removeListener: jest.fn(), // Deprecated
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

const TestComponent: React.FC = () => {
  const { theme, setTheme, systemTheme } = useTheme();
  return (
    <div>
      <span data-testid="theme">{theme}</span>
      <span data-testid="system-theme">{systemTheme}</span>
      <button data-testid="toggle-theme" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
        Toggle Theme
      </button>
    </div>
  );
};

describe('ThemeProvider', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test('should provide default theme', () => {
    const { getByTestId } = render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    expect(getByTestId('theme').textContent).toBe('light'); // Default is light
    expect(getByTestId('system-theme').textContent).toBe('light');
  });

  test('should toggle theme', async () => {
    const { getByTestId } = render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    const toggleButton = getByTestId('toggle-theme');
    const themeSpan = getByTestId('theme');

    expect(themeSpan.textContent).toBe('light');

    act(() => {
      toggleButton.click();
    });

    expect(themeSpan.textContent).toBe('dark');

    act(() => {
      toggleButton.click();
    });

    expect(themeSpan.textContent).toBe('light');
  });

  test('should save theme to localStorage', async () => {
    const { getByTestId } = render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    const toggleButton = getByTestId('toggle-theme');

    // Toggle to dark theme
    act(() => {
      toggleButton.click();
    });

    expect(localStorage.getItem('theme')).toBe('dark');

    // Toggle back to light theme
    act(() => {
      toggleButton.click();
    });

    expect(localStorage.getItem('theme')).toBe('light');
  });

  test('should load theme from localStorage', () => {
    // Set a theme in localStorage before rendering
    localStorage.setItem('theme', 'dark');

    const { getByTestId } = render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    expect(getByTestId('theme').textContent).toBe('dark');
  });
});