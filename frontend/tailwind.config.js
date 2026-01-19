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
          50: '#fff5f3',
          100: '#ffe8e3',
          200: '#ffd4c7',
          300: '#ffb89f',
          400: '#ff9671',
          500: '#ff7a59',
          600: '#f85d3d',
          700: '#e94528',
          800: '#c13721',
          900: '#a03020',
        },
      },
    },
  },
  plugins: [],
}
