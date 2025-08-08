<script lang="ts">
	// No props needed - this is a static welcome section
</script>

<div class="welcome-section">
	<div class="welcome-content">
		<div class="welcome-header">
			<h3>Welcome to The Kinetic Alphabet</h3>
			<p>Visualize choreographed staff movements through interactive animations</p>
		</div>

		<div class="quick-start">
			<div class="step-item">
				<span class="step-icon">📚</span>
				<div class="step-text">
					<strong>Browse Library</strong>
					<span>Explore sequences by category or search by name</span>
				</div>
			</div>
			<div class="step-item">
				<span class="step-icon">▶️</span>
				<div class="step-text">
					<strong>Select & Play</strong>
					<span>Click any thumbnail to start the animation</span>
				</div>
			</div>
			<div class="step-item">
				<span class="step-icon">⚙️</span>
				<div class="step-text">
					<strong>Control Playback</strong>
					<span>Adjust speed, loop, and navigate through beats</span>
				</div>
			</div>
		</div>
	</div>
</div>

<style>
	/* Welcome Section */
	.welcome-section {
		flex: 1;
		display: flex;
		align-items: flex-start;
		justify-content: center;
		padding: 2rem;
		overflow-y: auto;
		min-height: 0;
	}

	.welcome-content {
		max-width: 500px;
		width: 100%;
		text-align: center;
		margin-top: 2rem;
	}

	.welcome-header h3 {
		margin: 0 0 0.5rem;
		font-size: 1.75rem;
		font-weight: 600;
		color: var(--color-text-primary);
		letter-spacing: -0.025em;
	}

	.welcome-header p {
		margin: 0 0 2rem;
		font-size: 1rem;
		color: var(--color-text-secondary);
		line-height: 1.5;
	}

	.quick-start {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		text-align: left;
	}

	.step-item {
		display: flex;
		align-items: flex-start;
		gap: 1rem;
		padding: 1rem;
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 8px;
		transition: all 0.2s ease;
	}

	.step-item:hover {
		background: var(--color-surface-hover);
		border-color: var(--color-primary);
		transform: translateY(-1px);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	}

	.step-icon {
		font-size: 1.25rem;
		flex-shrink: 0;
		margin-top: 0.125rem;
	}

	.step-text {
		flex: 1;
		min-width: 0;
	}

	.step-text strong {
		display: block;
		margin-bottom: 0.25rem;
		font-size: 0.95rem;
		font-weight: 600;
		color: var(--color-text-primary);
	}

	.step-text span {
		font-size: 0.85rem;
		color: var(--color-text-secondary);
		line-height: 1.4;
	}

	/* Mobile welcome section adjustments */
	@media (max-width: 768px) {
		.welcome-section {
			padding: 1rem;
		}

		.welcome-content {
			margin-top: 1rem;
		}

		.welcome-header h3 {
			font-size: 1.5rem;
		}

		.welcome-header p {
			font-size: 0.9rem;
			margin-bottom: 1.5rem;
		}

		.step-item {
			padding: 0.75rem;
			gap: 0.75rem;
		}

		.step-icon {
			font-size: 1.1rem;
		}

		.step-text strong {
			font-size: 0.9rem;
		}

		.step-text span {
			font-size: 0.8rem;
		}
	}
</style>
