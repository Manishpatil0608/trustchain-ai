import React, { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  // Read persisted theme from localStorage, default to 'dark'
  const [theme, setTheme] = useState(() => {
    const saved = localStorage.getItem('tc_theme');
    return saved === 'light' ? 'light' : 'dark';
  });

  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'light') {
      root.classList.remove('dark');
      root.classList.add('light');
      root.setAttribute('data-theme', 'light');
    } else {
      root.classList.remove('light');
      root.classList.add('dark');
      root.setAttribute('data-theme', 'dark');
    }
    localStorage.setItem('tc_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  const isDark = theme === 'dark';

  // Dynamic semantic tokens for Recharts and theme-aware visualizations
  const chartTheme = isDark
    ? {
        bg: '#0b101d',
        cardBg: '#080b13',
        grid: '#1e293b',
        border: '#1e293b',
        text: '#94a3b8',
        textPrimary: '#f8fafc',
        tooltipBg: '#080b13',
        tooltipBorder: '#334155',
        accent: '#00f0ff',
        trusted: '#10b981',
        suspicious: '#f59e0b',
        quarantined: '#ef4444',
        revoked: '#64748b',
        barBackground: '#1e293b',
      }
    : {
        bg: '#ffffff',
        cardBg: '#f8fafc',
        grid: '#e2e8f0',
        border: '#cbd5e1',
        text: '#64748b',
        textPrimary: '#0f172a',
        tooltipBg: '#ffffff',
        tooltipBorder: '#cbd5e1',
        accent: '#0284c7',
        trusted: '#059669',
        suspicious: '#d97706',
        quarantined: '#dc2626',
        revoked: '#64748b',
        barBackground: '#e2e8f0',
      };

  return (
    <ThemeContext.Provider value={{ theme, setTheme, toggleTheme, isDark, chartTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
