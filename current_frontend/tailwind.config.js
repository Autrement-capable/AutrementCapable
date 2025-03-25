/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        text: {
          light: '#130727',
          dark: '#e4d8f8'
        },
        background: {
          light: '#ebe5fa',
          dark: '#0b051a'
        },
        primary: {
          light: '#3a167e',
          dark: '#a681e9'
        },
        secondary: {
          light: '#e878d0',
          dark: '#87176f'
        },
        accent: {
          light: '#cd237e',
          dark: '#dc328d'
        }
      }
    },
  },
  plugins: [],
}