/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        mono: ['"JetBrains Mono"', 'monospace'],
        display: ['"Orbitron"', 'monospace'],
      },
      colors: {
        cyber: {
          bg:      '#050a0f',
          panel:   '#0a1628',
          border:  '#0d2137',
          accent:  '#00d4ff',
          green:   '#00ff88',
          yellow:  '#ffd700',
          red:     '#ff4444',
          muted:   '#3a5a7a',
          text:    '#a8c8e8',
        }
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'scan': 'scan 3s linear infinite',
      },
      keyframes: {
        glow: {
          '0%':   { textShadow: '0 0 4px #00d4ff' },
          '100%': { textShadow: '0 0 16px #00d4ff, 0 0 32px #00d4ff' },
        },
        scan: {
          '0%':   { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100%)' },
        }
      }
    }
  },
  plugins: []
}
