<!-- src/routes/social-test/+page.svelte -->
<script lang="ts">
	import { onMount } from '$lib/utils/svelte-lifecycle';
	import { isAuthenticated } from '$lib/services/auth';
	import {
		postToFacebook,
		postToInstagram,
		postToTikTok,
		postToFacebookGroup
	} from '$lib/services/social/SocialMediaService';
	import { showSuccess, showError } from '$lib/components/shared/ToastManager.svelte';

	// Authentication status
	let isFacebookAuthenticated = $state(false);
	let isInstagramAuthenticated = $state(false);
	let isTikTokAuthenticated = $state(false);

	// Loading states
	let isLoading = $state(false);

	// Mock image result for testing
	const mockImageResult = {
		dataUrl:
			'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==',
		width: 100,
		height: 100,
		mimeType: 'image/png'
	};

	// Mock sequence data
	const mockSequenceName = 'Test Sequence';
	const mockShareUrl = 'https://example.com/sequence/123';

	onMount(() => {
		// Check authentication status
		isFacebookAuthenticated = isAuthenticated('FACEBOOK');
		isInstagramAuthenticated = isAuthenticated('INSTAGRAM');
		isTikTokAuthenticated = isAuthenticated('TIKTOK');
	});

	// Test Facebook posting
	async function testFacebookPost() {
		isLoading = true;
		try {
			await postToFacebook(mockImageResult, mockSequenceName, mockShareUrl);
			showSuccess('Facebook post test completed');
		} catch (error) {
			showError('Facebook post test failed');
			console.error('Facebook post test error:', error);
		} finally {
			isLoading = false;
		}
	}

	// Test Instagram posting
	async function testInstagramPost() {
		isLoading = true;
		try {
			await postToInstagram(mockImageResult, mockSequenceName, mockShareUrl);
			showSuccess('Instagram post test completed');
		} catch (error) {
			showError('Instagram post test failed');
			console.error('Instagram post test error:', error);
		} finally {
			isLoading = false;
		}
	}

	// Test TikTok posting
	async function testTikTokPost() {
		isLoading = true;
		try {
			await postToTikTok(mockImageResult, mockSequenceName, mockShareUrl);
			showSuccess('TikTok post test completed');
		} catch (error) {
			showError('TikTok post test failed');
			console.error('TikTok post test error:', error);
		} finally {
			isLoading = false;
		}
	}

	// Test Facebook Group posting
	async function testFacebookGroupPost() {
		isLoading = true;
		try {
			await postToFacebookGroup(mockImageResult, mockSequenceName, mockShareUrl);
			showSuccess('Facebook Group post test completed');
		} catch (error) {
			showError('Facebook Group post test failed');
			console.error('Facebook Group post test error:', error);
		} finally {
			isLoading = false;
		}
	}
</script>

<div class="container">
	<h1>Social Media Integration Test</h1>

	<div class="status-section">
		<h2>Authentication Status</h2>
		<ul>
			<li>
				Facebook:
				<span class={isFacebookAuthenticated ? 'authenticated' : 'not-authenticated'}>
					{isFacebookAuthenticated ? 'Authenticated' : 'Not Authenticated'}
				</span>
			</li>
			<li>
				Instagram:
				<span class={isInstagramAuthenticated ? 'authenticated' : 'not-authenticated'}>
					{isInstagramAuthenticated ? 'Authenticated' : 'Not Authenticated'}
				</span>
			</li>
			<li>
				TikTok:
				<span class={isTikTokAuthenticated ? 'authenticated' : 'not-authenticated'}>
					{isTikTokAuthenticated ? 'Authenticated' : 'Not Authenticated'}
				</span>
			</li>
		</ul>
	</div>

	<div class="test-section">
		<h2>Test Social Media Posting</h2>

		<div class="button-group">
			<button onclick={testFacebookPost} disabled={isLoading}>
				{isLoading ? 'Testing...' : 'Test Facebook Post'}
			</button>

			<button onclick={testInstagramPost} disabled={isLoading}>
				{isLoading ? 'Testing...' : 'Test Instagram Post'}
			</button>

			<button onclick={testTikTokPost} disabled={isLoading}>
				{isLoading ? 'Testing...' : 'Test TikTok Post'}
			</button>

			<button onclick={testFacebookGroupPost} disabled={isLoading}>
				{isLoading ? 'Testing...' : 'Test Facebook Group Post'}
			</button>
		</div>
	</div>

	<div class="note-section">
		<h3>Notes</h3>
		<p>
			This page tests the social media integration functionality. When you click on a test button:
		</p>
		<ul>
			<li>If you're not authenticated, you'll be redirected to the platform's login page</li>
			<li>If you are authenticated, a simulated post will be attempted</li>
			<li>In a real implementation, the post would be sent to the platform's API</li>
		</ul>
	</div>
</div>

<style>
	.container {
		max-width: 800px;
		margin: 0 auto;
		padding: 2rem;
		font-family:
			system-ui,
			-apple-system,
			BlinkMacSystemFont,
			'Segoe UI',
			Roboto,
			sans-serif;
	}

	h1 {
		color: #333;
		margin-bottom: 2rem;
	}

	.status-section,
	.test-section,
	.note-section {
		margin-bottom: 2rem;
		padding: 1.5rem;
		border-radius: 8px;
		background-color: #f5f5f5;
	}

	.authenticated {
		color: #2ecc71;
		font-weight: bold;
	}

	.not-authenticated {
		color: #e74c3c;
		font-weight: bold;
	}

	.button-group {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
		margin-top: 1rem;
	}

	button {
		padding: 0.75rem 1.5rem;
		border: none;
		border-radius: 4px;
		background-color: #3498db;
		color: white;
		font-weight: bold;
		cursor: pointer;
		transition: background-color 0.3s;
	}

	button:hover:not(:disabled) {
		background-color: #2980b9;
	}

	button:disabled {
		background-color: #95a5a6;
		cursor: not-allowed;
	}

	ul {
		list-style-type: none;
		padding-left: 0;
	}

	li {
		margin-bottom: 0.5rem;
	}

	.note-section {
		background-color: #fffde7;
	}
</style>
