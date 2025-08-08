import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest';
import { svgStringToImage } from './svgStringToImage.js';
import { Buffer } from 'buffer';

// Mock document/window objects for Node environment
const setupMocks = () => {
	// Mock window.Image
	const mockImage = vi.fn().mockImplementation(() => {
		const img = {
			onload: vi.fn(),
			onerror: vi.fn(),
			src: '',
			_src: ''
		};

		// Simulate image loading
		Object.defineProperty(img, 'src', {
			set(value) {
				this._src = value;
				setTimeout(() => {
					if (value.includes('data:image/svg+xml;base64,')) {
						this.onload && this.onload();
					} else {
						this.onerror && this.onerror(new Error('Invalid image data'));
					}
				}, 0);
				// Setters should not return values
			},
			get() {
				return this._src;
			}
		});

		return img;
	});

	// @ts-ignore - Mocking global objects for testing
	global.Image = mockImage;

	// Mock window for setTimeout
	const mockSetTimeout = vi.fn().mockImplementation((callback: Function, _timeout: number) => {
		callback();
		return 123; // fake timeout id
	});
	// @ts-ignore - Mocking global objects for testing
	global.setTimeout = mockSetTimeout;

	// @ts-ignore - Mocking global objects for testing
	global.clearTimeout = vi.fn();

	// Mock btoa for Base64 encoding in Node
	// @ts-ignore - Mocking global objects for testing
	global.btoa = (str: string) => Buffer.from(str).toString('base64');
};

// Test valid and malicious SVG strings
const validSvg =
	'<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="40" /></svg>';
const maliciousSvg = `<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <script>alert("XSS Attack")</script>
  <circle cx="50" cy="50" r="40" fill="red" onclick="alert('clicked')" />
  <a href="javascript:alert('XSS')"><text x="10" y="20">Click me</text></a>
</svg>`;

describe('svgStringToImage', () => {
	beforeAll(() => {
		setupMocks();
	});

	afterAll(() => {
		vi.clearAllMocks();
	});

	it('converts a valid SVG string to an image', async () => {
		const img = await svgStringToImage(validSvg, 100, 100);
		expect(img).toBeDefined();
		expect(img.src).toContain('data:image/svg+xml;base64,');
	});

	it('rejects invalid SVG input', async () => {
		await expect(svgStringToImage('not an svg', 100, 100)).rejects.toThrow('Invalid SVG string');
	});

	it('sanitizes malicious SVG content', async () => {
		const img = await svgStringToImage(maliciousSvg, 100, 100);

		// The SVG should be converted, but sanitized
		expect(img.src).toContain('data:image/svg+xml;base64,');

		// Check that malicious content was removed (decode the base64)
		const base64Part = img.src.split('base64,')[1];
		const decodedSvg = Buffer.from(base64Part, 'base64').toString();

		// Script tags should be removed
		expect(decodedSvg).not.toContain('<script>');

		// Event handlers should be removed
		expect(decodedSvg).not.toContain('onclick=');

		// JavaScript URLs should be removed
		expect(decodedSvg).not.toContain('javascript:');
	});

	it('handles timeout properly', async () => {
		// Override setTimeout to simulate timeout
		const originalSetTimeout = global.setTimeout;

		const mockTimeoutFn = vi.fn().mockImplementation((_callback: Function, _timeout: number) => {
			// Don't call the callback, simulating a timeout
			return 123; // fake timeout id
		});

		// @ts-ignore - Mocking global objects for testing
		global.setTimeout = mockTimeoutFn;

		const timeoutPromise = svgStringToImage(validSvg, 100, 100, 100);

		// Manually trigger the timeout by calling the error handler
		// Force the Image mock to reject
		const imgInstance = (global.Image as any).mock.results[0].value;
		imgInstance.onerror(new Error('Timed out'));

		await expect(timeoutPromise).rejects.toThrow();

		// Restore original setTimeout
		// @ts-ignore - Restoring mocked global object
		global.setTimeout = originalSetTimeout;
	});
});
