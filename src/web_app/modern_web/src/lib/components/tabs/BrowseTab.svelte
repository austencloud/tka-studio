<!-- Browse Tab - Sequence library -->
<div class="browse-tab">
	<div class="tab-header glass-surface">
		<h1>Browse</h1>
		<p>Explore and manage your sequence library</p>
	</div>

	<div class="tab-content">
		<div class="placeholder-content">
			<h2>📚 Browse Tab</h2>
			<p>Sequence library and management will be implemented here.</p>
			<p class="coming-soon">🚧 Coming Soon: Sequence Gallery, Search & Filter, Import/Export</p>
		</div>
	</div>
</div>

<style>
	.browse-tab {
		display: flex;
		flex-direction: column;
		height: 100%;
		padding: var(--spacing-lg);
		gap: var(--spacing-lg);
	}

	.tab-header {
		padding: var(--spacing-lg);
		text-align: center;
	}

	.tab-header h1 {
		font-size: var(--font-size-2xl);
		margin-bottom: var(--spacing-sm);
		color: var(--foreground);
	}

	.tab-header p {
		color: var(--muted-foreground);
	}

	.tab-content {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.placeholder-content {
		text-align: center;
		max-width: 600px;
	}

	.placeholder-content h2 {
		font-size: var(--font-size-xl);
		margin-bottom: var(--spacing-md);
		color: var(--foreground);
	}

	.placeholder-content p {
		color: var(--muted-foreground);
		margin-bottom: var(--spacing-lg);
	}

	.coming-soon {
		background: rgba(255, 193, 7, 0.1);
		border: 1px solid rgba(255, 193, 7, 0.3);
		color: #ffc107;
		padding: var(--spacing-md);
		border-radius: 8px;
		margin-top: var(--spacing-lg);
	}
</style>
