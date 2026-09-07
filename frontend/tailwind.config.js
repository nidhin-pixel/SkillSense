/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: "#0F2A43",
          light: "#1C3E5E",
          dark: "#081826",
        },
        paper: "#F4F6F8",
        gold: {
          DEFAULT: "#B8862F",
          light: "#D9A94F",
        },
        teal: {
          DEFAULT: "#1F7A6C",
          light: "#2E9C8B",
        },
        brick: "#B84A3C",
        slate: {
          text: "#1B2430",
          muted: "#5B6672",
          line: "#DEE3E8",
        },
      },
      fontFamily: {
        serif: ["Fraunces", "Georgia", "serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
