/** @type {import('tailwindcss').Config} */
export default {
	darkMode: ["class"],
	content: [
		"./pages/**/*.{js,jsx}",
		"./components/**/*.{js,jsx}",
		"./app/**/*.{js,jsx}",
		"./src/**/*.{js,jsx}",
	],
	prefix: "",
	theme: {
		container: {
			center: true,
			padding: '2rem',
			screens: {
				'2xl': '1400px'
			}
		},
		extend: {
			colors: {
				// Background Colors
				'bg-primary': 'hsl(var(--bg-primary))',
				'bg-secondary': 'hsl(var(--bg-secondary))',
				'bg-tertiary': 'hsl(var(--bg-tertiary))',
				
				// Chat Bubble Colors
				'chat-sent': 'hsl(var(--chat-sent))',
				'chat-received': 'hsl(var(--chat-received))',
				'chat-sent-hover': 'hsl(var(--chat-sent-hover))',
				'chat-received-hover': 'hsl(var(--chat-received-hover))',
				
				// Text Colors
				'text-primary': 'hsl(var(--text-primary))',
				'text-secondary': 'hsl(var(--text-secondary))',
				'text-muted': 'hsl(var(--text-muted))',
				'text-accent': 'hsl(var(--text-accent))',
				
				// Accent Colors
				'accent-primary': 'hsl(var(--accent-primary))',
				'accent-secondary': 'hsl(var(--accent-secondary))',
				'accent-danger': 'hsl(var(--accent-danger))',
				
				// Border & Input
				'border-primary': 'hsl(var(--border-primary))',
				'border-secondary': 'hsl(var(--border-secondary))',
				'input-bg': 'hsl(var(--input-bg))',
				'input-border': 'hsl(var(--input-border))',
			},
			backgroundImage: {
				'gradient-primary': 'var(--gradient-primary)',
				'gradient-secondary': 'var(--gradient-secondary)',
				'gradient-dark': 'var(--gradient-dark)',
			},
			boxShadow: {
				'chat': 'var(--shadow-chat)',
				'glow': 'var(--shadow-glow)',
				'card': 'var(--shadow-card)',
			},
			borderRadius: {
				lg: 'var(--radius)',
				md: 'calc(var(--radius) - 2px)',
				sm: 'calc(var(--radius) - 4px)'
			},
			keyframes: {
				'accordion-down': {
					from: {
						height: '0'
					},
					to: {
						height: 'var(--radix-accordion-content-height)'
					}
				},
				'accordion-up': {
					from: {
						height: 'var(--radix-accordion-content-height)'
					},
					to: {
						height: '0'
					}
				}
			},
			animation: {
				'accordion-down': 'accordion-down 0.2s ease-out',
				'accordion-up': 'accordion-up 0.2s ease-out'
			}
		}
	},
	plugins: [require("tailwindcss-animate")],
}