// tailwind.config.js
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
      },
      typography: (theme) => ({
        xs: {
          css: {
            fontSize: '0.75rem', // 12px
            lineHeight: '1.6',
          },
        },
        '3xl': {
          css: {
            fontSize: '1.875rem', // 30px
            lineHeight: '1.8',
          },
        },
      }),
    },
  },
  plugins: [require('@tailwindcss/typography')],
}
