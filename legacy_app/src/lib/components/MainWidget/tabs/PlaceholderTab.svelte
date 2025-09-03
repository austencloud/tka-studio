<!-- src/lib/components/MainWidget/tabs/PlaceholderTab.svelte -->
<script lang="ts">
	import { fade, fly, scale } from 'svelte/transition';

	export let icon: string;
	export let title: string;
</script>

<div class="placeholder-content">
	<div class="placeholder-card">
		<div class="placeholder-icon">
			<div in:scale={{ duration: 400, delay: 200 }} class="emoji-glow">
				{icon}
			</div>
		</div>
		<h2 in:fly={{ duration: 300, delay: 100, y: 20 }} class="placeholder-title">
			{title}
		</h2>
		<p in:fade={{ duration: 300, delay: 300 }} class="placeholder-text">
			This feature is under development and will be available soon.
		</p>
		<div class="placeholder-progress" in:scale={{ duration: 400, delay: 400, start: 0.8 }}>
			<div class="progress-bar">
				<div class="progress-fill"></div>
			</div>
			<p class="progress-text">Coming Soon</p>
		</div>

		<div class="coming-soon-dots">
			<span></span>
			<span></span>
			<span></span>
		</div>
	</div>
</div>

<style>
	.placeholder-content {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 100%;
		width: 100%;
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		padding: 20px;
		box-sizing: border-box;
	}

	.placeholder-card {
		background: rgba(30, 40, 60, 0.6);
		backdrop-filter: blur(8px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 16px;
		padding: 40px;
		text-align: center;
		box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
		max-width: 400px;
		width: 100%;
		transition:
			transform 0.3s ease,
			box-shadow 0.3s ease;
	}

	.placeholder-card:hover {
		transform: translateY(-5px);
		box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
	}

	.placeholder-icon {
		font-size: 4rem;
		margin-bottom: 20px;
	}

	.placeholder-title {
		font-size: 2rem;
		margin: 0 0 15px 0;
		color: white;
	}

	.placeholder-text {
		color: rgba(255, 255, 255, 0.8);
		margin-bottom: 30px;
		font-size: 1.1rem;
	}

	.placeholder-progress {
		width: 100%;
	}

	.progress-bar {
		height: 8px;
		background: rgba(255, 255, 255, 0.2);
		border-radius: 4px;
		overflow: hidden;
		margin-bottom: 8px;
	}

	.progress-fill {
		height: 100%;
		background: linear-gradient(90deg, #6c9ce9, #1e3c72);
		border-radius: 4px;
		width: 0%;
		animation: loading 2s ease-in-out infinite alternate;
	}

	@keyframes loading {
		0% {
			width: 15%;
		}
		100% {
			width: 85%;
		}
	}

	.progress-text {
		font-size: 0.9rem;
		color: rgba(255, 255, 255, 0.6);
		margin: 0;
	}

	/* Animated emoji glow effect */
	.emoji-glow {
		animation: pulse 2s infinite ease-in-out;
		filter: drop-shadow(0 0 10px rgba(108, 156, 233, 0.8));
	}

	@keyframes pulse {
		0% {
			transform: scale(1);
			opacity: 1;
		}
		50% {
			transform: scale(1.1);
			opacity: 0.9;
		}
		100% {
			transform: scale(1);
			opacity: 1;
		}
	}

	/* Coming soon dots animation */
	.coming-soon-dots {
		margin-top: 20px;
		display: flex;
		justify-content: center;
		gap: 10px;
	}

	.coming-soon-dots span {
		width: 8px;
		height: 8px;
		background-color: #fff;
		border-radius: 50%;
		display: inline-block;
		opacity: 0.6;
	}

	.coming-soon-dots span:nth-child(1) {
		animation: blink 1.4s infinite 0.2s;
	}

	.coming-soon-dots span:nth-child(2) {
		animation: blink 1.4s infinite 0.4s;
	}

	.coming-soon-dots span:nth-child(3) {
		animation: blink 1.4s infinite 0.6s;
	}

	@keyframes blink {
		0% {
			transform: scale(1);
			opacity: 0.4;
		}
		20% {
			transform: scale(1.3);
			opacity: 1;
		}
		100% {
			transform: scale(1);
			opacity: 0.4;
		}
	}
</style>