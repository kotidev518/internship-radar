// Tailwind CSS v4 uses CSS-based configuration via @import "tailwindcss" in globals.css.
// This file is kept empty to prevent Next.js from loading a v3-style config.
// All theme customization is done in src/app/globals.css.

import type { Config } from "tailwindcss"

const config: Config = {
    content: [
        './src/**/*.{ts,tsx}',
    ],
    theme: {
        extend: {},
    },
    plugins: [],
}

export default config
