<script lang="ts">
	// Props
	let {
		isDarkMode = $bindable()
	}: {
		isDarkMode: boolean;
	} = $props();

	// Theme management functions
	function toggleTheme(): void {
		isDarkMode = !isDarkMode;
		localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
		updateThemeClass();
	}

	function updateThemeClass(): void {
		if (typeof document !== 'undefined') {
			const theme = isDarkMode ? 'dark' : 'light';
			document.documentElement.setAttribute('data-theme', theme);
		}
	}

	// Initialize theme from localStorage
	$effect(() => {
		if (typeof window !== 'undefined') {
			const savedTheme = localStorage.getItem('theme');
			const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
			isDarkMode = savedTheme ? savedTheme === 'dark' : prefersDark;
			updateThemeClass();
		}
	});

	// Expose public methods
	export function toggle(): void {
		toggleTheme();
	}

	export function setTheme(dark: boolean): void {
		isDarkMode = dark;
		localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
		updateThemeClass();
	}
</script>

<!-- This component manages theme state but doesn't render anything -->
