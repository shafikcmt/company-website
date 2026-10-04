import defaultTheme from "tailwindcss/defaultTheme";
import typography from "@tailwindcss/typography";
import forms from "@tailwindcss/forms";

/**
 * Public site (Tailwind v3). Build with `npm run build:public`, or
 * `npm run tailwind:public` to watch while editing templates.
 *
 * Brand tokens come from the existing templates:
 *   navy    #093E61  logo navy (header / banners)
 *   amber   #F59E0B  CTA accent (dark #D97706 for text on white)
 *   ink     #111827  primary text
 *   muted   #4B5563  body copy
 *   surface #F9FAFB  alternating section background
 */
export default {
    content: {
        relative: true,
        files: [
            "./templates/**/*.{html,js}",
            "!./templates/admin/**/*",
            "!./templates/unfold/**/*",
            "./common/static/js/site.js",
            "./hapl/**/*.py",
        ],
    },
    theme: {
        extend: {
            colors: {
                navy: {
                    50: "#EEF5FA",
                    100: "#D6E6F1",
                    200: "#ADCDE4",
                    300: "#78A6C9",
                    400: "#3A76A3",
                    500: "#0E4A75",
                    600: "#093E61",
                    700: "#07344F",
                    800: "#06293F",
                    900: "#041F30",
                    950: "#02121D",
                    DEFAULT: "#093E61",
                    light: "#0E4A75",
                    dark: "#06293F",
                },
                amber: {
                    DEFAULT: "#F59E0B",
                    dark: "#D97706",
                },
                ink: "#111827",
                muted: "#4B5563",
                surface: "#F9FAFB",
            },
            fontFamily: {
                sans: ["Inter", ...defaultTheme.fontFamily.sans],
            },
            maxWidth: {
                site: "1600px",
            },
            boxShadow: {
                soft: "0 1px 2px rgb(9 62 97 / 0.04), 0 8px 24px -8px rgb(9 62 97 / 0.12)",
                lift: "0 2px 4px rgb(9 62 97 / 0.04), 0 24px 48px -12px rgb(9 62 97 / 0.22)",
            },
            transitionTimingFunction: {
                "out-expo": "cubic-bezier(0.16, 1, 0.3, 1)",
            },
            keyframes: {
                marquee: {
                    from: { transform: "translateX(0)" },
                    to: { transform: "translateX(-50%)" },
                },
            },
            animation: {
                marquee: "marquee var(--marquee-duration, 40s) linear infinite",
            },
        },
    },
    plugins: [typography, forms],
};
