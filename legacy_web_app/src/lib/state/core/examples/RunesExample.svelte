<script lang="ts">
	import { createPersistentState, createPersistentObjectState } from '../runes';
	import { setContext } from 'svelte';

	// Example 1: Basic state with runes
	let count = $state(0);

	// Example 2: Derived state with runes
	const doubleCount = $derived(count * 2);

	// Example 3: Persistent state with runes
	let persistentCount = $state(createPersistentState('example_count', 0));

	// Example 4: Persistent object state with selective persistence
	const settings = createPersistentObjectState(
		'example_settings',
		{
			theme: 'light',
			fontSize: 16,
			showNotifications: true,
			temporaryValue: 'not persisted'
		},
		{
			persistFields: ['theme', 'fontSize', 'showNotifications']
		}
	);

	// Example 5: Context with runes
	const EXAMPLE_CONTEXT = Symbol('example-context');
	const contextValue = $state({ value: 'context example' });
	setContext(EXAMPLE_CONTEXT, contextValue);

	// Example 6: Effects with runes
	$effect(() => {
		console.log(`Count changed to ${count}, double is ${doubleCount}`);
	});

	// Example 7: Cleanup with runes
	$effect.root(() => {
		const interval = setInterval(() => {
			// Auto-increment the persistent count every 5 seconds
			persistentCount++;
		}, 5000);

		return () => {
			clearInterval(interval);
		};
	});

	// Action handlers
	function incrementCount() {
		count++;
	}

	function incrementPersistentCount() {
		persistentCount++;
	}

	function toggleTheme() {
		settings.theme = settings.theme === 'light' ? 'dark' : 'light';
	}

	function resetAll() {
		count = 0;
		persistentCount = 0;
		settings.theme = 'light';
		settings.fontSize = 16;
		settings.showNotifications = true;
	}
</script>

<div class="example-container">
	<h2>Svelte 5 Runes Examples</h2>

	<section>
		<h3>Basic State</h3>
		<p>Count: {count}</p>
		<button onclick={incrementCount}>Increment</button>
	</section>

	<section>
		<h3>Derived State</h3>
		<p>Double Count: {doubleCount}</p>
	</section>

	<section>
		<h3>Persistent State</h3>
		<p>Persistent Count: {persistentCount}</p>
		<p class="note">This value persists across page refreshes</p>
		<button onclick={incrementPersistentCount}>Increment Persistent</button>
	</section>

	<section>
		<h3>Persistent Object State</h3>
		<p>Theme: {settings.theme}</p>
		<p>Font Size: {settings.fontSize}px</p>
		<p>Show Notifications: {settings.showNotifications ? 'Yes' : 'No'}</p>
		<p>Temporary Value: {settings.temporaryValue}</p>
		<p class="note">Only theme, fontSize, and showNotifications persist</p>
		<button onclick={toggleTheme}>Toggle Theme</button>
		<button onclick={() => (settings.fontSize += 2)}>Increase Font Size</button>
		<button onclick={() => (settings.showNotifications = !settings.showNotifications)}>
			Toggle Notifications
		</button>
	</section>

	<section>
		<h3>Reset All</h3>
		<button onclick={resetAll}>Reset All Values</button>
	</section>
</div>

<style>
	.example-container {
		max-width: 600px;
		margin: 0 auto;
		padding: 20px;
		font-family:
			system-ui,
			-apple-system,
			sans-serif;
	}

	section {
		margin-bottom: 30px;
		padding: 15px;
		border: 1px solid #ddd;
		border-radius: 8px;
	}

	h2 {
		text-align: center;
		margin-bottom: 30px;
	}

	h3 {
		margin-top: 0;
		border-bottom: 1px solid #eee;
		padding-bottom: 10px;
	}

	button {
		margin-right: 10px;
		padding: 8px 12px;
		background: #4a90e2;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}

	button:hover {
		background: #3a80d2;
	}

	.note {
		font-size: 0.8em;
		color: #666;
		font-style: italic;
	}
</style>
