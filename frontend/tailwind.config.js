/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fef8f6',
          100: '#fdeee9',
          200: '#fbd9cf',
          300: '#f8bfab',
          400: '#f39b7f',
          500: '#ec7756',
          600: '#d95c3e',
          700: '#b64a33',
          800: '#953f2f',
          900: '#7a372b',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Playfair Display', 'Georgia', 'serif'],
      },
    },
  },
  plugins: [],
}
