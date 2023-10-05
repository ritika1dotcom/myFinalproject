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
      }
       
      
    },
  },
  plugins: [],
}

