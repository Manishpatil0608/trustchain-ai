/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['Fira Code', 'JetBrains Mono', 'monospace'],
      },
      colors: {
        tc: {
          dark: '#040609',
          panel: '#0b0f19',
          border: '#1e2b45',
          cyan: '#00f0ff',
          success: '#00ff88',
          warning: '#ffaa00',
          danger: '#ff0044'
        }
      }
    },
  },
  plugins: [],
}