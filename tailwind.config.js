// tailwind.config.js

module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/**/*.py"
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          DEFAULT: '#001F3F',      // darkest navy
          light: '#003366',        // lighter navy
          lighter: '#004080',      // for accents or hover
        },
      },
    },
  },
  plugins: [],
}
