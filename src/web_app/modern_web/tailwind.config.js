/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}', './src/app.html', './static/**/*.html'],
	theme: {
		extend: {
			// Custom color palette
			colors: {
				primary: {
					50: '#eff6ff',
					100: '#dbeafe',
					200: '#bfdbfe',
					300: '#93c5fd',
					400: '#60a5fa',
					500: '#3b82f6',
					600: '#2563eb',
					700: '#1d4ed8',
					800: '#1e40af',
					900: '#1e3a8a',
					950: '#172554',
				},
				secondary: {
					50: '#f8fafc',
					100: '#f1f5f9',
					200: '#e2e8f0',
					300: '#cbd5e1',
					400: '#94a3b8',
					500: '#64748b',
					600: '#475569',
					700: '#334155',
					800: '#1e293b',
					900: '#0f172a',
					950: '#020617',
				},
			},

			// Custom spacing
			spacing: {
				18: '4.5rem',
				88: '22rem',
				128: '32rem',
			},

			// Custom font families
			fontFamily: {
				sans: [
					'Inter',
					'ui-sans-serif',
					'system-ui',
					'-apple-system',
					'BlinkMacSystemFont',
					'"Segoe UI"',
					'Roboto',
					'"Helvetica Neue"',
					'Arial',
					'"Noto Sans"',
					'sans-serif',
					'"Apple Color Emoji"',
					'"Segoe UI Emoji"',
					'"Segoe UI Symbol"',
					'"Noto Color Emoji"',
				],
				mono: [
					'"Fira Code"',
					'ui-monospace',
					'SFMono-Regular',
					'"Menlo"',
					'Monaco',
					'Consolas',
					'"Liberation Mono"',
					'"Courier New"',
					'monospace',
				],
			},

			// Custom animations
			animation: {
				'fade-in': 'fadeIn 0.5s ease-in-out',
				'fade-out': 'fadeOut 0.5s ease-in-out',
				'slide-in': 'slideIn 0.3s ease-out',
				'slide-out': 'slideOut 0.3s ease-in',
				'bounce-subtle': 'bounceSubtle 2s infinite',
				'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
			},

			// Custom keyframes
			keyframes: {
				fadeIn: {
					'0%': { opacity: '0' },
					'100%': { opacity: '1' },
				},
				fadeOut: {
					'0%': { opacity: '1' },
					'100%': { opacity: '0' },
				},
				slideIn: {
					'0%': { transform: 'translateX(-100%)' },
					'100%': { transform: 'translateX(0)' },
				},
				slideOut: {
					'0%': { transform: 'translateX(0)' },
					'100%': { transform: 'translateX(100%)' },
				},
				bounceSubtle: {
					'0%, 100%': {
						transform: 'translateY(-5%)',
						animationTimingFunction: 'cubic-bezier(0.8, 0, 1, 1)',
					},
					'50%': {
						transform: 'translateY(0)',
						animationTimingFunction: 'cubic-bezier(0, 0, 0.2, 1)',
					},
				},
			},

			// Custom box shadows
			boxShadow: {
				soft: '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
				medium: '0 4px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
				hard: '0 10px 40px -10px rgba(0, 0, 0, 0.2), 0 20px 25px -5px rgba(0, 0, 0, 0.1)',
			},

			// Custom border radius
			borderRadius: {
				'4xl': '2rem',
				'5xl': '2.5rem',
			},
		},
	},
	plugins: [
		require('@tailwindcss/forms'),
		require('@tailwindcss/typography'),
		require('@tailwindcss/container-queries'),
	],

	// Dark mode configuration
	darkMode: 'class',

	// Safelist for dynamic classes
	safelist: [
		'animate-fade-in',
		'animate-fade-out',
		'animate-slide-in',
		'animate-slide-out',
		{
			pattern: /bg-(primary|secondary)-(50|100|200|300|400|500|600|700|800|900|950)/,
		},
		{
			pattern: /text-(primary|secondary)-(50|100|200|300|400|500|600|700|800|900|950)/,
		},
		{
			pattern: /border-(primary|secondary)-(50|100|200|300|400|500|600|700|800|900|950)/,
		},
	],
};
