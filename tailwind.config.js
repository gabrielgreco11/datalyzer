/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
  
  './base.html','./index.html', './charts.html,', './sites.html', 'fokus_one_youtuber.html','./settings.html' ],
  theme: {
    extend: {
      animation: {
        typing: 'typing 0.75s steps(5), blink 1s infinite',
      },
      keyframes: {
        typing: {
          from: {
            width: '0'
          },
          to: {
            width: '6ch'
          },
        },
        blink: {
          from: {
            'border-right-color': 'transparent'
          },
          to: {
            'border-right-color': 'black'
          },
        },
      },
    },
  },
  plugins: [],
}

