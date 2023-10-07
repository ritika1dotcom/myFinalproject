/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./dist/**/*.{html,js}"],
  theme: {
    extend: {
      colors:
      {
        'black-dark':  '#00000050',
        'dull-white':  '#FFFFFFB3',
        'neon-blue': '2FB8FF',
        'soft-lilac-start': '#E1D5E7', // starting color for the gradient
        'soft-lilac-end': '#D3BCD9', // ending color for the gradient
      }
    },
  },
  plugins: [],
}

