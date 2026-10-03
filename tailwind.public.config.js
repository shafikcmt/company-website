import typography from "@tailwindcss/typography";
import forms from "@tailwindcss/forms";
import preline from "preline/plugin";
import taos from "taos/plugin";

export default {
    darkMode: "class",
    content: {
        relative: true,
        transform: (content) => content.replace(/taos:/g, ""),
        files: [
            "./node_modules/preline/preline.js",
            "./templates/**/*.{html,js,py}",
            "!./templates/admin/**/*.{html,js,py}",
            "./common/**/*.{html,js}",
            "./users/**/*.{html,js,py}",
            "./hapl/**/*.{html,js,py}",
        ],
    },
    theme: {
        extend: {
            colors: {
                "brand-navy": { light: "#0E4A75", DEFAULT: "#093E61", dark: "#06293F" },
                "brand-orange": { DEFAULT: "#F59E0B", dark: "#D97706" },
                foreground: "hsl(var(--foreground))",
                background: "hsl(var(--background))",
                card: "hsl(var(--card))",
                border: "hsl(var(--border))",
                primary: "hsl(var(--primary))",
                accent: "hsl(var(--accent))",
            },
            fontFamily: {
                sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
            },
        },
    },
    plugins: [
        typography,
        forms({ strategy: "class" }),
        preline,
        taos,
    ],
    safelist: [
        "!duration-[0ms]",
        "!delay-[0ms]",
        'html.js :where([class*="taos:"]:not(.taos-init))',
    ],
};
