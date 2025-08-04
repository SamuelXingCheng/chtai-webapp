module.exports = {
    content: [
      "./index.html",
      "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
          colors: {
            beige: '#FAF9F6',
            primary: '#181E2A',
          }
        }
      },
      plugins: [require('@tailwindcss/typography')],
  }
  