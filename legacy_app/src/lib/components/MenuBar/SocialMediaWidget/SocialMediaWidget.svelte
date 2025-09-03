<script lang="ts">
	const socialLinks = [
		{ src: '/social_icons/paypal.png', alt: 'PayPal', url: 'https://www.paypal.me/austencloud' },
		{ src: '/social_icons/venmo.png', alt: 'Venmo', url: 'https://venmo.com/austencloud' },
		{
			src: '/social_icons/github.png',
			alt: 'GitHub',
			url: 'https://github.com/austencloud/the-kinetic-constructor-web'
		},
		{
			src: '/social_icons/facebook.png',
			alt: 'Facebook',
			url: 'https://www.facebook.com/thekineticalphabet'
		},
		{
			src: '/social_icons/instagram.png',
			alt: 'Instagram',
			url: 'https://www.instagram.com/thekineticalphabet'
		},
		{
			src: '/social_icons/youtube.png',
			alt: 'YouTube',
			url: 'https://www.youtube.com/channel/UCbLHNRSASZS_gwkmRATH1-A'
		}
	];

	const openLink = (url: string) => window.open(url, '_blank');
</script>

<div class="social-container">
	{#each socialLinks as link}
		<button
			class="button"
			on:click={() => openLink(link.url)}
			on:keydown={(e) => e.key === 'Enter' && openLink(link.url)}
			aria-label={link.alt}
		>
			<img class="icon" src={link.src} alt={link.alt} />
		</button>
	{/each}
</div>

<style>
	/*
    1) The container: we let each cell define the button’s size
       with a CSS grid.
  */
	.social-container {
		display: grid;
		/* e.g., 3 columns, auto rows. Adjust as you prefer. */
		grid-template-columns: repeat(3, 1fr);
    gap: 4%;
	}

	/*
    2) The button: use aspect-ratio to keep it square.
       We do NOT fix a height or reference window size.
       The grid cell will define the button’s area.
  */
	.button {
		/* Fill the parent's height while maintaining aspect ratio
     or some limit.
  */
  width: clamp(40px, 6vw, 60px);
  height: clamp(40px, 6vw, 60px);

  aspect-ratio: 1 / 1; /* keep them circular */
  border-radius: 50%;
		display: flex;
		justify-content: center;
		align-items: center;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
		cursor: pointer;
		transition:
			transform 0.2s,
			box-shadow 0.2s,
			background-color 0.3s;
		border: none;
		outline: none;
		min-width: 40px; /* just to avoid being too tiny */
	}
	.button:hover {
		background-color: #f0f0f0;
		transform: scale(1.1);
		box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
	}

	.button:active {
		transform: scale(1);
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	}

	/*
    3) The icon: let it scale automatically using max-width/height
       inside the button’s area.
  */
	.icon {
		max-width: 70%;
		max-height: 70%;
		object-fit: contain; /* ensure it scales proportionally */
		transition: transform 0.2s;
	}

	.button:hover .icon {
		transform: scale(1.1);
	}
</style>
